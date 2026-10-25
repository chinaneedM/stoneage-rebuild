#!/usr/bin/env python3
"""Read-only archaeological observation lab for the accepted TW1.0 retail client.

Outputs a LOCAL grayscale palette-index PNG (not historical color) and custody
metadata outside this public repository. Does not run original executables.
WAV audit verifies original bytes; local HTML file chooser handles playback.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import wave
import zlib
from pathlib import Path

from tools.stoneage_rd_codec import RDDecodeError, decode_rd_block

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt"
INVENTORY_BLOB_SHA = "564233902b10c60760d4f93b1ea65d4dd1469206"
PINNED = {
    "adrn_1.bin": (10079680, "47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8"),
    "real_1.bin": (315842228, "408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13"),
}
RECORD_SIZE = 80
MAX_PIXELS = 8_000_000
MODE = "SOURCE_PALETTE_INDEX_AS_GRAYSCALE_NOT_HISTORICAL_COLOR"
SOURCE = "TW_WAEI_JSS_1_0_ACCEPTED_RETAIL_REDUMP_104630"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git_blob_hash(b: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()

def check_original(path: Path, expected: tuple[int,str]):
    if not path.is_file():
        raise ValueError("missing original local file: " + str(path))
    if path.stat().st_size != expected[0] or sha256_file(path) != expected[1]:
        raise ValueError("original client source length or SHA-256 mismatch: " + path.name)

def safe_output(path: Path) -> Path:
    if path.suffix.lower() != ".png":
        raise ValueError("private PNG output must use .png")
    out = path.expanduser().resolve()
    if out == ROOT or ROOT in out.parents or out == INVENTORY:
        raise ValueError("copyrighted image output must be outside the public repository")
    if out.exists() or out.with_suffix(".json").exists():
        raise ValueError("output exists; cannot overwrite existing research evidence")
    if not out.parent.is_dir() or not out.parent.exists():
        raise ValueError("create an external private output directory first")
    return out

def get_record(adrn_path: Path, *, index: int | None=None, bitmapno: int | None=None):
    if (index is None) == (bitmapno is None):
        raise ValueError("choose exactly one record index or bitmapno")
    count = adrn_path.stat().st_size // RECORD_SIZE
    if adrn_path.stat().st_size % RECORD_SIZE:
        raise ValueError("invalid ADRN record length")
    with adrn_path.open("rb") as f:
        if index is not None:
            if not 0 <= index < count:
                raise ValueError("record index outside authenticated inventory")
            f.seek(index * RECORD_SIZE)
            records = [(index, f.read(RECORD_SIZE))]
        else:
            records = []
            for i in range(count):
                b = f.read(RECORD_SIZE)
                if struct.unpack_from("<I", b)[0] == bitmapno:
                    records.append((i,b))
                    if len(records) > 1:
                        raise ValueError("bitmap number not unique in source inventory")
    if len(records) != 1:
        raise ValueError("bitmap number absent in authenticated source")
    i, raw = records[0]
    bitmap, offset, size, xoff, yoff, width, height = struct.unpack_from("<IIIiiii", raw)
    if size < 16 or width <= 0 or height <= 0 or width * height > MAX_PIXELS:
        raise ValueError("unsupported original special/oversized image dimensions")
    return {
        "index": i, "bitmapno": bitmap, "adder": offset, "size": size,
        "xoff": xoff, "yoff": yoff, "width": width, "height": height,
        "source_adrn_record_sha256": hashlib.sha256(raw).hexdigest(),
    }

def chunk(tag: bytes, body: bytes) -> bytes:
    payload = tag + body
    return struct.pack(">I", len(body)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xffffffff)

def gray_png(pixels: bytes, width: int, height: int) -> bytes:
    if width <= 0 or height <= 0 or width * height != len(pixels) or len(pixels) > MAX_PIXELS:
        raise ValueError("invalid PNG dimensions or pixels")
    rows = b"".join(b"\x00" + pixels[y*width:(y+1)*width] for y in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")

def build_bitmap(adrn: Path, real: Path, *, index=None, bitmapno=None, expected=None):
    """Only full pinned original files are admitted by CLI; tests inject synthetic pins."""
    expected = PINNED if expected is None else expected
    check_original(adrn, expected["adrn_1.bin"])
    check_original(real, expected["real_1.bin"])
    row = get_record(adrn, index=index, bitmapno=bitmapno)
    if row["adder"] + row["size"] > real.stat().st_size:
        raise ValueError("RD slice exceeds actual REAL file length")
    with real.open("rb") as f:
        f.seek(row["adder"])
        original_block = f.read(row["size"])
    if len(original_block) != row["size"]:
        raise ValueError("short authentic RD block")
    rd_header, pixels = decode_rd_block(original_block, authoritative_block_size=row["size"])
    if rd_header["width_s"] != row["width"] or rd_header["height_s"] != row["height"]:
        raise RDDecodeError("ADRN/RD original geometric metadata mismatch")
    png = gray_png(pixels, row["width"], row["height"])
    custody = {
        "schema": "stoneage.original_observation_lab.bitmap_v1",
        "source_claim": "ORIGINAL_TW10_RD_BYTES_DECODED_TO_PALETTE_INDICES_ONLY",
        "sample": SOURCE,
        "file_id": {"adrn_path": "StoneAge/data/adrn_1.bin",
                    "real_path": "StoneAge/data/real_1.bin"},
        "source_sha256": {"adrn_1.bin": expected["adrn_1.bin"][1],
                           "real_1.bin": expected["real_1.bin"][1]},
        "record": row,
        "original_rd_block_sha256": hashlib.sha256(original_block).hexdigest(),
        "rd_flag": rd_header["flag"],
        "decoded_palette_index_sha256": hashlib.sha256(pixels).hexdigest(),
        "preview_png_sha256": hashlib.sha256(png).hexdigest(),
        "preview_mode": MODE,
        "original_palette_verified": False,
        "original_colors_reproduced": False,
        "original_client_executed": False,
        "npc_name": None, "pet_species": None,
        "quest_origin": "ORIGIN_UNRESOLVED",
        "server_entity_binding_verified": False,
        "historical_gameplay_screenshot": False,
    }
    return png, custody

def pinned_wav_inventory(path: Path = INVENTORY):
    raw=path.read_bytes()
    if git_blob_hash(raw) != INVENTORY_BLOB_SHA:
        raise ValueError("archived original client inventory changed")
    out={}
    for line in raw.decode("utf-8").splitlines():
        if line.startswith("CORE_FILE|") and "|category=audio_" in line:
            fields=dict(part.split("=",1) for part in line.split("|")[1:])
            out[fields["path"]] = (int(fields["size"]), fields["sha256"])
    if len(out) < 120:
        raise ValueError("insufficient original audio inventory records")
    return out

def inspect_wav(wav_path: Path, original_path: str, expected=None):
    if expected is None:
        expected=pinned_wav_inventory()
    if original_path not in expected or not original_path.endswith(".wav") or not original_path.startswith("StoneAge/data/"):
        raise ValueError("not a pinned original loose WAV")
    check_original(wav_path, expected[original_path])
    with wave.open(str(wav_path), "rb") as w:
        channels, rate, frames = w.getnchannels(), w.getframerate(), w.getnframes()
        width, compression = w.getsampwidth(), w.getcomptype()
    if channels <= 0 or rate <= 0 or width <= 0:
        raise ValueError("invalid source WAV format")
    return {
        "schema": "stoneage.original_observation_lab.wav_v1",
        "sample": SOURCE,
        "original_path": original_path,
        "original_sha256": expected[original_path][1],
        "format": {"channels": channels, "sample_rate_hz": rate,
                   "sample_width_bytes": width, "frames": frames,
                   "duration_seconds": round(frames / rate, 8), "compression": compression},
        "original_audio_bytes_written": False,
        "audio_played_or_heard_by_assistant": False,
        "in_game_sound_event_verified": False,
        "npc_pet_battle_sound_identity": None,
    }

def main():
    ap=argparse.ArgumentParser(description="Private/local TW1.0 original resource observation; no ROM or game execution")
    sub=ap.add_subparsers(dest="command",required=True)
    image=sub.add_parser("bitmap",help="Authenticated original indexed pixels -> private grayscale PNG")
    image.add_argument("--adrn",type=Path,required=True)
    image.add_argument("--real",type=Path,required=True)
    choice=image.add_mutually_exclusive_group(required=True)
    choice.add_argument("--index",type=int)
    choice.add_argument("--bitmapno",type=int)
    image.add_argument("--output",type=Path,required=True)
    sound=sub.add_parser("wav",help="Read-only source-verified loose WAV structure; no sound event naming")
    sound.add_argument("--file",type=Path,required=True)
    sound.add_argument("--original-path",required=True)
    args=ap.parse_args()
    if args.command=="bitmap":
        out=safe_output(args.output)
        png, custody=build_bitmap(args.adrn,args.real,index=args.index,bitmapno=args.bitmapno)
        with out.open("xb") as f: f.write(png)
        try:
            with out.with_suffix(".json").open("x",encoding="utf-8") as f:
                json.dump(custody,f,ensure_ascii=False,sort_keys=True,indent=2)
                f.write("\n")
        except Exception:
            out.unlink()
            raise
        print("PRIVATE_GRAYSCALE_PREVIEW="+str(out))
        print(json.dumps(custody,ensure_ascii=False,sort_keys=True))
    else:
        print(json.dumps(inspect_wav(args.file,args.original_path),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
