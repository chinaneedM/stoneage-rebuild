"""PET126F private-only custody audit. Reads lawful local archives; never executes game files or publishes art."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research/recovered/STONEAGE-PET126F-SOURCE-CUSTODY-SEVEN-DIMENSION-RESIDUAL-R1.json"


def stream_sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_local_archives(original_path, observer_path, receipt_path=RECEIPT):
    receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    custody = receipt["private_custody_rechecked_this_session"]
    source = custody["tw1_original_archive"]
    derived = custody["pet15_derived_private_observer"]
    original_path, observer_path = Path(original_path), Path(observer_path)
    for p, pin in ((original_path, source), (observer_path, derived)):
        if p.stat().st_size != pin["bytes"] or stream_sha256(p) != pin["sha256"]:
            raise ValueError("Archive identity/size does not match PET126F receipt: " + p.name)

    with zipfile.ZipFile(original_path) as z:
        if len(z.infolist()) != source["members"] or z.testzip() is not None:
            raise ValueError("Original TW1 archive member count/CRC invalid")
        members = [x for x in z.infolist() if x.filename.startswith("source/")]
        if len(members) != source["source_members"]:
            raise ValueError("Original TW1 source member count changed")
        extension_counts = Counter(os.path.splitext(x.filename)[1].lower() for x in members)
        if dict(extension_counts) != source["source_extension_counts"]:
            raise ValueError("Original TW1 source extension census changed")
        for name, expected in source["verified_member_hashes"].items():
            info = z.getinfo(name)
            h = hashlib.sha256()
            with z.open(info) as stream:
                for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                    h.update(chunk)
            if info.file_size != expected["bytes"] or h.hexdigest() != expected["sha256"]:
                raise ValueError("Original TW1 member differs: " + name)

    with zipfile.ZipFile(observer_path) as z:
        infos = z.infolist()
        if len(infos) != derived["zip_members"] or z.testzip() is not None:
            raise ValueError("Original-derived private observer ZIP count/CRC invalid")
        private_receipts = json.loads(z.read("private-bitmap-receipts.json"))
        pngs = [i for i in infos if i.filename.startswith("images/") and i.filename.endswith(".png")]
        if len(pngs) != derived["rendered_png_count"]:
            raise ValueError("Derived PNG count changed")
        if len(private_receipts) != derived["receipt_entry_count"]:
            raise ValueError("Private PNG receipt count changed")
        ids = {i.filename[7:-4] for i in pngs}
        if ids != set(private_receipts):
            raise ValueError("Derived PNG IDs differ from private receipts")
        statuses = Counter(record["status"] for record in private_receipts.values())
        if statuses != Counter({
            "strict": derived["strict_decode_receipt_count"],
            "terminal_zero_outside_canvas": derived["bounded_terminal_zero_outside_canvas_count"],
        }):
            raise ValueError("Derived bitmap status counts differ")
        bad = 0
        for info in pngs:
            key = info.filename[7:-4]
            if hashlib.sha256(z.read(info)).hexdigest() != private_receipts[key]["candidate_png_sha256"]:
                bad += 1
        if bad != derived["png_sha256_mismatches"]:
            raise ValueError("Rendered PNG byte SHA differs from private receipt")
    return {
        "original_client_zip_sha256_verified": True,
        "original_client_zip_member_crc_verified": source["members"],
        "original_source_member_count": source["source_members"],
        "source_core_files_sha256_verified": len(source["verified_member_hashes"]),
        "private_derived_zip_sha256_verified": True,
        "private_derived_zip_member_crc_verified": derived["zip_members"],
        "private_derived_png_and_receipt_key_matches": len(pngs),
        "private_derived_png_individual_sha256_matches": len(pngs) - bad,
        "strict_vs_bounded": dict(statuses),
        "independent_official_client_builds_discovered": 0,
        "game_client_executed": False,
        "official_server_contacted": False,
        "commercial_bytes_published": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True, help="Private original TW1 client ZIP")
    parser.add_argument("--observer", type=Path, required=True, help="Private PET15 derived observer ZIP")
    parser.add_argument("--receipt", type=Path, default=RECEIPT)
    args = parser.parse_args()
    print(json.dumps(verify_local_archives(args.original, args.observer, args.receipt),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
