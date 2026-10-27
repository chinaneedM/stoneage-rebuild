"""Acquire one fixed preserved carrier and privately observe real map artwork.

No original executable runs. Public output is metadata; originals and previews
leave a runner only as CMS ciphertext to a caller-supplied certificate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.request
import zipfile

from tools.stoneage_native_album_source_r36 import PARTS, PREFIX
from tools.stoneage_wayi85_sixpart_acquisition import direct_link
from tools.stoneage_private_scene_graphic_join_r1 import (
    ADRN_SIZE, ADRN_SHA, REAL_SIZE, REAL_SHA, sha_file, join, export_private,
    resolve_ids, is_later_draw_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_SIZE = 361255180
BUNDLE_SHA = "d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"
MAP_SHA = "62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90"
SELECTED = {
    "data/adrn_15.bin": (ADRN_SIZE, ADRN_SHA),
    "data/real_15.bin": (REAL_SIZE, REAL_SHA),
    "map/1001.dat": (5408, MAP_SHA),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def fingerprint(path):
    return {"bytes": path.stat().st_size, "sha256": sha_file(path)}

def bounded_copy(source, target, expected_size, expected_sha=None):
    """Never accept HTML, truncation, or a stream exceeding its declared size."""
    digest = hashlib.sha256()
    total = 0
    while block := source.read(1024 * 1024):
        total += len(block)
        require(total <= expected_size, "stream exceeds fixed byte budget")
        target.write(block)
        digest.update(block)
    require(total == expected_size, "short source stream")
    require(expected_sha is None or digest.hexdigest() == expected_sha,
            "source complete SHA256 mismatch")
    return {"bytes": total, "sha256": digest.hexdigest()}

def acquire_bundle(work, report):
    bundle = work / "preserved-mixed25.rar"
    report["parts"] = []
    with bundle.open("xb") as output:
        for key, size in PARTS:
            public_url = "https://www.mediafire.com/file/" + key + "/"
            request = urllib.request.Request(public_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=60) as response:
                page = response.read(4 * 1024 * 1024 + 1)
                require(len(page) <= 4 * 1024 * 1024, "source download page extent")
                referer = response.geturl()
            payload = urllib.request.Request(direct_link(page.decode("utf-8", "replace")),
                headers={"User-Agent": "Mozilla/5.0", "Referer": referer})
            with urllib.request.urlopen(payload, timeout=180) as response:
                info = bounded_copy(response, output, size)
            report["parts"].append({"public_download_page": public_url, **info})
    require(fingerprint(bundle) == {"bytes": BUNDLE_SIZE, "sha256": BUNDLE_SHA},
            "whole preserved carrier identity conflict")
    report["bundle"] = fingerprint(bundle)
    return bundle

def extract_selected(bundle, work):
    import libarchive
    found = {}
    with libarchive.file_reader(str(bundle)) as archive:
        for entry in archive:
            name = entry.pathname.replace("\\", "/")
            if not name.startswith(PREFIX):
                continue
            relative = name[len(PREFIX):].lower()
            if relative not in SELECTED:
                continue
            require(relative not in found, "duplicate selected archive path")
            expected_size, expected_sha = SELECTED[relative]
            require(entry.isfile and entry.size == expected_size, "selected archive type/extent drift")
            target = work / Path(relative).name
            digest = hashlib.sha256()
            total = 0
            with target.open("xb") as out:
                for block in entry.get_blocks():
                    total += len(block)
                    require(total <= expected_size, "decompressed source extent exceeded")
                    digest.update(block)
                    out.write(block)
            require(total == expected_size and digest.hexdigest() == expected_sha,
                    "selected full member SHA256 mismatch")
            found[relative] = target
    require(set(found) == set(SELECTED), "fixed original source member absent")
    return found

def observe(selected, work):
    from tools.stoneage_local_runtime_core import WorldRegionRequest, load_runtime_bootstrap_file
    from tools.stoneage_recovered25_world_profile_adapter import Recovered25WorldProfileAdapter
    from tools.stoneage_recovered25_region_payload import Recovered25RegionPayloadSource
    profile = load_runtime_bootstrap_file(ROOT / "game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json")
    adapter = Recovered25WorldProfileAdapter.from_repository(profile)
    source = Recovered25RegionPayloadSource(profile=profile, adapter=adapter,
        client_dat_dir=work, server_map_root=work)
    adrn = selected["data/adrn_15.bin"].read_bytes()
    chosen = None
    # Deterministic bounded 3x3 search: centre first, then original row order.
    windows = [(14, 14)] + [(x, y) for y in range(0, 28, 3) for x in range(0, 28, 3)]
    for x, y in windows:
        region = source.materialize_region(WorldRegionRequest(floor_id=1001,
            x1=x, y1=y, x2=x+2, y2=y+2, world_profile="recovered25"))
        ids = {n for n in (*region.payload.tile_ids, *region.payload.object_ids)
               if is_later_draw_candidate(n)}
        if not 1 <= len(ids) <= 16:
            continue
        rows = resolve_ids(adrn, ids, REAL_SIZE)
        if sum(len(r) == 1 and 0 < r[0]["width"] * r[0]["height"] <= 8000000
               and r[0]["width"] > 0 and r[0]["height"] > 0 for r in rows.values()) >= 1:
            chosen = region
            break
    require(chosen is not None, "no bounded resolvable original image viewport")
    report, pngs = join(chosen, adrn, selected["data/real_15.bin"])
    require(len(pngs) > 0 and report["source_pins_match_preserved_bundle"],
            "real source image qualification did not succeed")
    preview = work / "observation"
    preview.mkdir()
    export_private(preview, report, pngs)
    # Include bounded source RD bytes for independent decoding after transfer.
    with selected["data/real_15.bin"].open("rb") as real:
        for resource in report["resources"]:
            if not resource["rendered_artwork"]:
                continue
            row = resource["occurrences"][0]
            real.seek(row["offset"])
            (preview / (resource["filename"] + ".rd")).write_bytes(real.read(row["size"]))
    archive = work / "scene02-private-observation.zip"
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as out:
        for path in sorted(preview.iterdir()):
            out.write(path, path.name)
        out.write(selected["map/1001.dat"], "source-map-1001.dat")
        out.write(selected["data/adrn_15.bin"], "source-adrn_15.bin")
    return report, archive

def seal(source, certificate, destination):
    subprocess.run(["openssl", "cms", "-encrypt", "-binary", "-aes-256-cbc",
        "-in", str(source), "-out", str(destination), "-outform", "DER",
        str(certificate)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return {"plaintext": fingerprint(source), "ciphertext": fingerprint(destination)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--certificate", type=Path, required=True)
    a = p.parse_args()
    work = a.work.resolve()
    output = a.output_dir.resolve()
    require(ROOT not in work.parents and work != ROOT and ROOT not in output.parents and output != ROOT,
            "proprietary sources/transfer must remain outside repository")
    work.mkdir(mode=0o700, parents=True, exist_ok=False)
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    report = {"schema": "stoneage.private_scene_source.r2", "status": "NOT_ACQUIRED",
        "source_class": "COMMUNITY_MIXED25_NOT_AUTHENTICATED_OFFICIAL_BUILD",
        "original_executable_executed": False, "original_world_entered": False,
        "authentic_scene_rendered": False, "raw_originals_published": False,
        "private_durable_custody_confirmed": False, "actual_visual_inspection_completed": False}
    try:
        bundle = acquire_bundle(work, report)
        report["status"] = "CARRIER_HASH_VERIFIED"
        selected = extract_selected(bundle, work)
        report["selected_members"] = {key: fingerprint(path) for key, path in selected.items()}
        report["observation"], archive = observe(selected, work)
        report["private_transfers"] = {
            "observation": seal(archive, a.certificate, output / "observation.der"),
            "carrier": seal(bundle, a.certificate, output / "carrier.der"),
        }
        report["status"] = "REAL_SOURCE_PIXELS_EXPORTED_AND_ENCRYPTED_NOT_YET_VISUALLY_INSPECTED"
    except Exception as exc:
        report["error"] = {"type": type(exc).__name__, "message": str(exc)[:400]}
        raise
    finally:
        (output / "source-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
        print(json.dumps(report, ensure_ascii=False))
        shutil.rmtree(work)

if __name__ == "__main__":
    main()
