"""R5: acquire exact preserved source in isolated runner; export two RD/PNG privately.

This is a static research extractor, NOT original-game execution.
Originals and PNG leave runner only via CMS encryption. Public output = safe hashes.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct
import subprocess
import zipfile

from tools.stoneage_private_scene_source_r2 import (
    ROOT, BUNDLE_SIZE, BUNDLE_SHA, acquire_bundle, qualify_carrier, extract_selected, fingerprint
)
from tools.stoneage_private_scene_graphic_join_r1 import ADRN_SHA, ADRN_SIZE, REAL_SIZE, REAL_SHA
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_tw10_palette import initial_rgb

CERT_SHA = "d6765f98e33e0e9716e75f3a602e5accc81529f259d469aac097fa4d0cbaf793"
SAP_SHA = "32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0"
ROWS = (
    (5009, 1624, 2381236, 1698, -32, -24, 64, 47,
     "3cf451aafd8c99141768a6e4a2997ae134f6d516cf597b52d1314c72c47d183a"),
    (5015, 1630, 2389112, 1656, -32, -24, 64, 47,
     "eb4eed3611e893c4c53cd100891f1a946c28ef3ee31702c8c9ee24c96f086238"),
)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def get_rows(adrn):
    require(len(adrn) == ADRN_SIZE and sha(adrn) == ADRN_SHA,
            "whole original ADRN identity failed")
    found = {r[0]: [] for r in ROWS}
    for idx in range(len(adrn)//80):
        logical = struct.unpack_from("<i", adrn, idx*80+76)[0]
        if logical in found:
            found[logical].append(idx)
    require(all(found[r[0]] == [r[1]] for r in ROWS),
            "missing/duplicate original logical ID candidate")
    for logical, idx, offset, size, x, y, w, h, digest in ROWS:
        record = adrn[idx*80:(idx+1)*80]
        require(sha(record) == digest and
                struct.unpack_from("<7i", record) == (idx,offset,size,x,y,w,h),
                "pinned original 80-byte record drift")
        require(0 <= offset and size > 16 and offset+size <= REAL_SIZE,
                "RD range exceeds preserved REAL")
    return found

def rgba_candidate(indices, width, height, rgb):
    require(len(indices) == width*height and len(rgb) == 256*3,
            "source image dimensions or palette mismatch")
    # Only 16..239 + key0 are covered by this program/SAP color witness.
    if any(v != 0 and not 16 <= v <= 239 for v in indices):
        return None
    return bytes(ch for y in range(height-1,-1,-1)
                 for v in indices[y*width:(y+1)*width]
                 for ch in (*rgb[v*3:v*3+3], 0 if v == 0 else 255))

def extract_two(adrn, real_file, palette):
    from PIL import Image
    get_rows(adrn)
    if palette is not None:
        require(len(palette)==708 and sha(palette)==SAP_SHA, "private SAP source conflict")
    colors = initial_rgb(palette) if palette is not None else None
    files = {}
    rows = []
    with real_file.open("rb") as r:
        require(real_file.stat().st_size == REAL_SIZE, "REAL source extent changed")
        for logical, idx, offset, size, x, y, width, height, rec_sha in ROWS:
            r.seek(offset)
            rd = r.read(size)
            require(len(rd) == size, "short original RD block")
            hdr, pixels = decode_rd_block(rd, authoritative_block_size=size)
            require((hdr["width_s"],hdr["height_s"]) == (width,height),
                    "RD original geometry conflicts with same-carrier ADRN")
            indexed = Image.frombytes("L", (width,height),pixels)
            buf = io.BytesIO(); indexed.save(buf,format="PNG")
            files[f"map-id-{logical:05d}-indices.png"] = buf.getvalue()
            files[f"map-id-{logical:05d}.rd"] = rd
            rgba = rgba_candidate(pixels,width,height,colors) if colors else None
            if rgba is not None:
                buf = io.BytesIO()
                Image.frombytes("RGBA",(width,height),rgba).save(buf,format="PNG")
                files[f"map-id-{logical:05d}-source-color-candidate.png"] = buf.getvalue()
            rows.append({
              "map_id":logical,"original_adrn_index":idx,"original_record_sha256":rec_sha,
              "original_real_offset":offset,"original_RD_bytes":size,"RD_sha256":sha(rd),
              "RD_flag":hdr["flag"],"RD_stored_size_untrusted":hdr["stored_size"],
              "dimensions":[width,height],"ADRN_signed_offset":[x,y],
              "palette_indices_sha256":sha(pixels),"palette_slot_range":[min(pixels),max(pixels)],
              "reserved_palette_slots":sorted(set(v for v in pixels if v not in (0,) and not 16<=v<=239)),
              "candidate_RGBA_sha256":sha(rgba) if rgba else None,
              "color_candidate_is_original_runtime":False,
              "original_game_executable_executed":False,
            })
    return rows,files

def run(args):
    work = args.work.resolve()
    output = args.output_dir.resolve()
    require(work != ROOT and ROOT not in work.parents and output != ROOT and ROOT not in output.parents,
            "private original extraction must remain outside public repository")
    require(not work.exists() and not output.exists(),"refuse existing private work/output path")
    cert = args.certificate.resolve()
    require(cert.is_file() and sha(cert.read_bytes()) == CERT_SHA,
            "private transfer certificate drift")
    work.mkdir(parents=True,mode=0o700)
    output.mkdir(parents=True,mode=0o700)
    report = {"schema":"stoneage.private_scene_missing_real.r5",
              "status":"STARTED","source_role":"PRESERVED_COMMUNITY_MIXED25_NOT_OFFICIAL_TW1",
              "original_world_entered":False,"original_client_executed":False,
              "raw_pixels_published_to_git":False,"source_originals_published_in_artifact":False}
    try:
        bundle = (qualify_carrier(args.carrier.resolve()) and args.carrier.resolve()
                  if args.carrier else acquire_bundle(work,report))
        report["carrier"] = {"bytes":BUNDLE_SIZE,"sha256":BUNDLE_SHA}
        report["carrier_reused_offline"] = args.carrier is not None
        selected = extract_selected(bundle,work)
        require(fingerprint(selected["data/adrn_15.bin"]) == {"bytes":ADRN_SIZE,"sha256":ADRN_SHA},
                "ADRN preserved member drift")
        require(fingerprint(selected["data/real_15.bin"]) == {"bytes":REAL_SIZE,"sha256":REAL_SHA},
                "REAL preserved member drift")
        # No file named original palette here: input palette is private and SHA-qualified.
        palette = args.palette.read_bytes() if args.palette else None
        rows, files = extract_two(selected["data/adrn_15.bin"].read_bytes(),
                                  selected["data/real_15.bin"],palette)
        private = work/"scene-r5-private.zip"
        with zipfile.ZipFile(private,"x",zipfile.ZIP_DEFLATED) as z:
            for name,content in sorted(files.items()):
                z.writestr(name,content)
        report.update(status="SOURCE_TWO_RD_PIXEL_IMAGES_DECODED",
                      exact_RD_rows=rows,source_real_sha256=REAL_SHA,
                      encrypted_private_member_count=len(files),
                      private_zip_bytes=private.stat().st_size,
                      private_zip_sha256=sha(private.read_bytes()))
        cipher=output/"scene-r5-encrypted-observation.der"
        subprocess.run(["openssl","cms","-encrypt","-binary","-aes-256-cbc",
                       "-in",str(private),"-out",str(cipher),"-outform","DER",str(cert)],
                       check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=60)
        report["encrypted_transfer"] = fingerprint(cipher)
        report["status"]="TWO_SOURCE_RD_PIXELS_ENCRYPTED_PRIVATE"
        print("TWO_ACTUAL_SOURCE_RD_DECODED=PASS; ORIGINAL_WORLD_ENTERED=FALSE")
    except Exception as exc:
        report["status"]="FAILED"
        report["failure"]={"type":type(exc).__name__,"message":str(exc)[:180]}
        raise
    finally:
        (output/"source-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
        if work.exists(): shutil.rmtree(work)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--work",type=Path,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    ap.add_argument("--certificate",type=Path,required=True)
    ap.add_argument("--carrier",type=Path)
    ap.add_argument("--palette",type=Path)
    run(ap.parse_args())
if __name__=="__main__": main()
