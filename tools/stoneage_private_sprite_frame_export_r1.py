"""Export authenticated TW1 sprite frame PNGs to an offline/private modern viewer.

Inputs MUST pass the existing original full-file/RD/SPR hash gates.
Never treats selected Palet_0 initial RGB as a verified in-game scene palette.
Never creates/modifies files inside the public repository or uploads assets.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re

from tools.stoneage_original_animation_lab import (
    ORIGINALS, ROOT, timeline, preview,
)

SCHEMA = "stoneage.private_original_sprite_observer_frames.r1"
DATA_START = '<script id="pack" type="application/json">'
DATA_END = '</script>'
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'


def unpack(html: str, custody: dict) -> list[tuple[str, bytes]]:
    """Extract only already validated in-memory source PNGs, never HTML/javascript."""
    if html.count(DATA_START) != 1:
        raise ValueError("original source pack marker missing/ambiguous")
    block = html.split(DATA_START, 1)[1]
    if DATA_END not in block:
        raise ValueError("unclosed original pack")
    data = json.loads(block.split(DATA_END, 1)[0])
    if data["timeline"] != custody["timeline"]:
        raise ValueError("preview/custody source timeline mismatch")
    frames = data["timeline"]["frames"]
    if not frames or len(frames) > 512:
        raise ValueError("no original frames or unbounded expansion")
    witnesses = {str(row["bitmapno"]): row for row in custody["bitmap_witnesses"]}
    if len(witnesses) != len(custody["bitmap_witnesses"]):
        raise ValueError("duplicated source witness")
    if set(data["images"]) != set(witnesses):
        raise ValueError("source bitmap set mismatch")
    files = []
    for pos, frame in enumerate(frames):
        bitmap_no = str(frame["bmp_no"])
        if bitmap_no not in witnesses:
            raise ValueError("source frame bitmap lacks original RD witness")
        encoded = data["images"][bitmap_no]
        if not encoded.startswith("data:image/png;base64,"):
            raise ValueError("unexpected PNG URI")
        png = base64.b64decode(encoded.split(",", 1)[1], validate=True)
        if not png.startswith(PNG_MAGIC):
            raise ValueError("non-PNG source image")
        w = witnesses[bitmap_no]
        key = "private_indexed_color_png_sha256" if "private_indexed_color_png_sha256" in w else "private_grayscale_png_sha256"
        if hashlib.sha256(png).hexdigest() != w[key]:
            raise ValueError("original source PNG digest mismatch")
        files.append((f"frame-{pos:03}.png", png))
    return files


def export_private(target: Path, files: list[tuple[str, bytes]], custody: dict) -> Path:
    target = target.expanduser().resolve()
    root = ROOT.resolve()
    if target == root or root in target.parents or not target.is_dir() or any(target.iterdir()):
        raise ValueError("private output MUST be an empty existing directory outside repository")
    if not files or len(files) > 512 or len(set(name for name, _ in files)) != len(files):
        raise ValueError("invalid frame export set")
    for name, raw in files:
        if not re.fullmatch(r"frame-\d{3}\.png", name) or not raw.startswith(PNG_MAGIC):
            raise ValueError("unexpected private asset")
    manifest = {
        "schema": SCHEMA,
        "source": "TW_WAEI_1_0",
        "interface_language": "zh-CN",
        "original_source_files": custody["original_files"],
        "original_source_status": custody["source_status"],
        "source_timeline": custody["timeline"],
        "file_count": len(files),
        "files": [{"path":name, "sha256":hashlib.sha256(raw).hexdigest(),
                   "byte_length":len(raw)} for name, raw in files],
        "original_game_client_launched": False,
        "original_game_world_entered": False,
        "scene_palette_selection_verified": False,
        "sprite_entity_name_verified": False,
        "fps_original_verified": False,
        "synthetic_preview_only": True,
    }
    try:
        for name, raw in files:
            (target / name).write_bytes(raw)
        manifest_file = target / "source-manifest.json"
        with manifest_file.open("x", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except BaseException:
        for name, _ in files:
            (target / name).unlink(missing_ok=True)
        (target / "source-manifest.json").unlink(missing_ok=True)
        raise
    return manifest_file


def main():
    parser = argparse.ArgumentParser(description="Original TW1 source qualified frames for PRIVATE modern observer")
    parser.add_argument("--original-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--spr-no", type=int, default=100000)
    parser.add_argument("--direction", type=int, default=0)
    parser.add_argument("--action", type=int, default=6)
    parser.add_argument("--palette", type=Path)
    args = parser.parse_args()
    t = timeline(args.spr_no, args.direction, args.action)
    paths = {name: args.original_dir / name for name in ORIGINALS}
    if args.palette is not None:
        from tools.stoneage_tw10_palette import original_rgb
        colors = original_rgb(args.palette)
    else:
        colors = None
    html, custody = preview(t, paths, color_table=colors)
    frame_files = unpack(html, custody)
    manifest = export_private(args.output_dir, frame_files, custody)
    print(f"PRIVATE_ORIGINAL_SPR_FRAME_PREVIEW_WRITTEN={len(frame_files)}; manifest={manifest}")
    print("NOT_ORIGINAL_IN_GAME_PALETTE_OR_AUTHENTIC_CLIENT_GAMEPLAY")


if __name__ == "__main__":
    main()
