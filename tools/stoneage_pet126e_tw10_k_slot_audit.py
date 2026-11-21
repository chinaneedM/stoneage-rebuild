"""PET126E private original-client verification. Never executes or republishes source EXE."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "research/recovered/STONEAGE-PET126E-TW10-K-STATUS-CAPTURE-STATIC-R1.json"


def digest_stream(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def audit(archive, receipt_path=RECEIPT):
    r = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    source = r["original_source"]
    archive = Path(archive)
    if archive.stat().st_size != source["archive_size"]:
        raise ValueError("Original ZIP size differs from the immutable evidence pin")
    if digest_stream(archive) != source["archive_sha256"]:
        raise ValueError("Original ZIP sha256 differs from the immutable evidence pin")

    with zipfile.ZipFile(archive) as z:
        if len(z.infolist()) != source["zip_crc_reverified_count"]:
            raise ValueError("Original ZIP member count mismatch")
        member = z.getinfo(source["exe_member"])
        if z.testzip() is not None:
            raise ValueError("Original ZIP CRC verification failed")
        b = z.read(member)

    if len(b) != source["exe_size"]:
        raise ValueError("Original compiled client member size mismatch")
    if hashlib.sha256(b).hexdigest() != source["exe_sha256"]:
        raise ValueError("Original compiled client member hash mismatch")

    for w in r["source_windows"]:
        start, end = w["start"], w["end"]
        if start < 0 or end <= start or end > len(b):
            raise ValueError("Invalid original EXE window bounds")
        if hashlib.sha256(b[start:end]).hexdigest() != w["sha256"]:
            raise ValueError("Original EXE window digest mismatch: " + w["id"])

    k = r["k_parser"]
    base = int(k["slot_struct_base_va"], 16)
    if k["stride"] != 108 or k["membership_flag_offset"] != 104:
        raise ValueError("Unexpected slot layout")
    if k["field_count"] != 20 or len(k["field_map"]) != 20:
        raise ValueError("Unexpected pet status field count")
    if k["membership_flag_width"] != 2:
        raise ValueError("Unexpected slot membership flag width")
    if int(k["membership_flag_va"], 16) != base + 104:
        raise ValueError("Slot flag and stride address mismatch")

    # The 20 original full/delta operations contain matching immediate
    # destination addresses in the same executable, not public source bytes.
    for field in k["field_map"]:
        expected = base + field["struct_offset"]
        full = struct.unpack_from("<I", b, field["full_address_immediate_offset"])[0]
        delta = struct.unpack_from("<I", b, field["delta_address_immediate_offset"])[0]
        if full != expected or delta != expected:
            raise ValueError("Full/delta original address mismatch at token "
                             + str(field["token"]))
    for offset in k["flag_address_immediate_positions"]:
        if struct.unpack_from("<I", b, offset)[0] != int(k["membership_flag_va"], 16):
            raise ValueError("Original presence flag destination mismatch")

    c = r["capture_join"]
    if c["count_total_slots"] != 5 or c["ui_loop_stride"] != k["stride"]:
        raise ValueError("Capture UI and status slot span differ")
    if int(c["ui_loop_end_exclusive_va"], 16) != base + 104 + 5 * 108:
        raise ValueError("Capture UI loop bound mismatch")
    return {
        "source_archive_sha256_match": True,
        "archive_members_crc_pass": source["zip_crc_reverified_count"],
        "source_exe_sha256_match": True,
        "source_windows_sha256_pass": len(r["source_windows"]),
        "same_destination_full_delta_field_pairs": len(k["field_map"]),
        "presence_flag_refs_verified": len(k["flag_address_immediate_positions"]),
        "slot_count": c["count_total_slots"],
        "original_exe_executed": False,
        "original_server_contacted": False,
        "new_official_pet_species_proven": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True,
                        help="Privately held qualified TW1 original source archive")
    args = parser.parse_args()
    print(json.dumps(audit(args.archive), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
