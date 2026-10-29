#!/usr/bin/env python3
"""Bounded, source-qualified follow-on to R63: JP2003 development gallery slots 2 and 3.

Original JPEG and HTML bytes are never written to the public repository or artifacts.
The output is only metadata, with no original game/binary execution.
"""
import argparse
import hashlib
import io
import json
import urllib.request
from pathlib import Path
from PIL import Image
from tools.stoneage_jp2003_battle_field_visual_source import Page, page, wrapper

ROOT = Path(__file__).resolve().parents[1]
R63 = ROOT / "research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1.json"
R63_BLOB = "e84da9c7db1b8792a643d18b191761efa0d73e88"
BASE = "https://www.4gamer.net/store/shots/stoneage/"
ORDINALS = (2, 3)
URLS = [BASE + "pages/image%04d.html" % i for i in ORDINALS] + [BASE + "images/image%04d.jpg" % i for i in ORDINALS]
MATERIAL_SCOPE = "JP_BOTHTEC_2003_DEVELOPMENT_GALLERY_NOT_ORIGINAL_1999_OR_TW1_OR_CN_BUILD"


def ensure(ok, label):
    if not ok:
        raise ValueError(label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def existing_gallery_refs():
    raw = R63.read_bytes()
    ensure(git_blob(raw) == R63_BLOB, "R63 source report changed")
    old = json.loads(raw.decode("utf-8"))
    ensure(old["extracted"]["gallery"]["development_notice"] is True, "development qualifier missing")
    ensure(old["extracted"]["gallery"]["gallery_date_label"] == "12th Dec. 2003", "gallery date moved")
    ensure(len(old["extracted"]["gallery"]["reference_rows"]) == 15, "gallery size changed")
    return old["extracted"]["gallery"]["reference_rows"]


def jpeg(raw):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        ensure(im.format == "JPEG" and im.mode == "RGB" and getattr(im, "n_frames", 1) == 1, "unexpected original-image container")
        ensure((im.width, im.height) == (640, 480), "gallery JPEG dimension changed; revise source scope")
        return {"bytes": len(raw), "sha256": sha(raw), "format": im.format,
                "width": im.width, "height": im.height, "mode": im.mode, "frames": getattr(im, "n_frames", 1),
                "complete_decode": True}


def derive(raws):
    ensure(len(raws) == 4, "exactly two wrappers and two original JPEGs expected")
    refs = existing_gallery_refs()
    rows = []
    for j, ordinal in enumerate(ORDINALS):
        stem = "image%04d" % ordinal
        ensure(refs[ordinal] == {
            "href": "pages/" + stem + ".html",
            "src": "thumbnails/" + stem + ".jpg", "alt": stem
        }, "pinned 2003 gallery slot attribution changed")
        w = wrapper(raws[j], ordinal)
        im = jpeg(raws[j + 2])
        ensure(w["image_src_as_written"] == "../images/" + stem + ".jpg", "image path differs")
        rows.append({
            "ordinal": ordinal, "gallery_reference": refs[ordinal],
            "wrapper_url": URLS[j], "wrapper": w,
            "wrapper_bytes": len(raws[j]), "wrapper_sha256": sha(raws[j]),
            "original_jpeg_url": URLS[j + 2], "original_jpeg": im,
            "visual_description": None, "visual_description_reviewed": False,
            "historical_capture_date": None, "original_native_resolution": None,
            "original_build_hash_or_id": None, "original_pet_name_or_id": None
        })
    return {
        "schema": "stoneage.jp2003_gallery_slots_2_3.source_r1",
        "baseline_source_R63_git_blob": R63_BLOB,
        "reference_gallery_label": "12th Dec. 2003",
        "reference_gallery_development_build_notice": True,
        "scope": MATERIAL_SCOPE, "source_rows": rows,
        "source_count": 2, "raw_http_original_bytes_published": False,
        "original_game_client_executed": False,
        "original_server_interaction_verified": False,
        "picture_visual_content_reviewed_by_human": False,
        "official_early1999_or_tw1_build_authenticated": False,
        "stage_a": "7_PARTIAL_2_OPEN", "stage_b_and_wiki": "GATED",
        "R79": "PAUSED_NON_BLOCKING", "overall_restoration_percentage": None
    }


def get_bounded(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": BASE + "index.html"})
    with urllib.request.urlopen(req, timeout=40) as stream:
        ensure(stream.status == 200 and stream.geturl() == url, "source redirect or non-200")
        raw = stream.read(2_000_001)
        ensure(len(raw) <= 2_000_000 and raw, "source missing or unexpectedly large")
        return raw



PUBLISHED = ROOT / "research/recovered/STONEAGE-JP2003-GALLERY-SLOTS-02-03-SOURCE-R1.json"
EXPECTED_SOURCE = (
    (2, 185950, "8f5c642bcdfffb75fd2f1bb4851db09be2016a97a2acb339cf6a4c2fd773d10a",
     "eb81231f5aa623dc17be46bc4915d92439bc542ab86275cb439589c17b5a33da"),
    (3, 185778, "2e681e3a93a763f6b78ef4325d9b5f939438c5c57fbc93684df5a960f36a6384",
     "5ece5743d1573ea331fd4007f0b170d16d9d16c81a3cc373e25efc3c9a2c3ab2"),
)


def verify_published(report):
    refs = existing_gallery_refs()
    ensure(report["schema"] == "stoneage.jp2003_gallery_slots_2_3.source_r1", "wrong archived schema")
    ensure(report["scope"] == MATERIAL_SCOPE and report["baseline_source_R63_git_blob"] == R63_BLOB,
           "source lineage altered")
    ensure(report["reference_gallery_label"] == "12th Dec. 2003"
           and report["reference_gallery_development_build_notice"] is True, "development date or scope altered")
    ensure(report["source_count"] == 2 and len(report["source_rows"]) == 2
           and report["http_response_url_binding_verified"] is True, "original remote-source verification missing")
    for k, (ordinal, length, file_sha, html_sha) in enumerate(EXPECTED_SOURCE):
        row = report["source_rows"][k]
        ensure(row["ordinal"] == ordinal and row["gallery_reference"] == refs[ordinal], "gallery identity altered")
        ensure(row["wrapper_url"] == URLS[k] and row["original_jpeg_url"] == URLS[k + 2], "source URL altered")
        ensure(row["wrapper_bytes"] == 1914 and row["wrapper_sha256"] == html_sha
               and row["wrapper"]["ordinal"] == ordinal
               and row["wrapper"]["image_src_as_written"] == "../images/image%04d.jpg" % ordinal,
               "wrapper evidence altered")
        ensure(row["original_jpeg"] == {
            "bytes": length, "sha256": file_sha, "format": "JPEG",
            "width": 640, "height": 480, "mode": "RGB",
            "frames": 1, "complete_decode": True
        }, "JPEG identity or decoded pixel structure altered")
        for key in ("visual_description", "historical_capture_date",
                    "original_native_resolution", "original_build_hash_or_id", "original_pet_name_or_id"):
            ensure(row[key] is None, "unproven original identity or visual interpretation promoted")
        ensure(row["visual_description_reviewed"] is False, "unperformed visual judgment claimed")
    for key in ("raw_http_original_bytes_published", "original_game_client_executed",
                "original_server_interaction_verified", "picture_visual_content_reviewed_by_human",
                "official_early1999_or_tw1_build_authenticated"):
        ensure(report[key] is False, "unproven game-world/rights status promoted: " + key)
    ensure(report["overall_restoration_percentage"] is None
           and report["stage_a"] == "7_PARTIAL_2_OPEN"
           and report["stage_b_and_wiki"] == "GATED"
           and report["R79"] == "PAUSED_NON_BLOCKING", "historical project status was silently upgraded")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fetch", action="store_true")
    p.add_argument("--inputs", type=Path, nargs=4)
    p.add_argument("--output", type=Path)
    p.add_argument("--check-published", action="store_true")
    args = p.parse_args()
    if args.check_published:
        ensure(not args.fetch and not args.inputs and not args.output, "check-published is isolated")
        verify_published(json.loads(PUBLISHED.read_text(encoding="utf-8")))
        print("SCENE27 published current-source identities validated: 2 JPEG, 640x480, no original runtime claim")
        return
    ensure(args.output is not None, "--output required for source acquisition")
    ensure(args.fetch != bool(args.inputs), "provide exactly one input method")
    raws = [get_bounded(url) for url in URLS] if args.fetch else [path.read_bytes() for path in args.inputs]
    result = derive(raws)
    # Distinct-image guard. HTTPS fetched URL equality, not JPEG internal metadata, binds each remote response to its slot.
    swapped = [raws[0], raws[1], raws[3], raws[2]]
    reversed_result = derive(swapped)
    ensure([r["original_jpeg"]["sha256"] for r in reversed_result["source_rows"]]
           != [r["original_jpeg"]["sha256"] for r in result["source_rows"]],
           "two image responses identical; paired slot identity unresolved")
    result["http_response_url_binding_verified"] = bool(args.fetch)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source": "JP2003_R63_GALLERY_TWO_NEW_SLOTS", "success": True,
                      "evidence": [{"ordinal": row["ordinal"], "bytes": row["original_jpeg"]["bytes"],
                                    "sha256": row["original_jpeg"]["sha256"],
                                    "pixels": [row["original_jpeg"]["width"], row["original_jpeg"]["height"]]}
                                   for row in result["source_rows"]],
                      "images_retained_in_repository": False, "visual_manual_reviewed": False}))


if __name__ == "__main__":
    main()
