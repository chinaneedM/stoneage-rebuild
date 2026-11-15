#!/usr/bin/env python3
"""Rebuild the Taiwan 1.0 client name-to-SPR evidence from the authenticated P3H ZIP."""

import argparse
import json
import struct
from collections import defaultdict
from hashlib import file_digest, sha256
from pathlib import Path
from zipfile import ZipFile

from tools.stoneage_tw10_technical_probe import pe_sections
from tools.stoneage_waei_tw10_spr_diff import validate_spr

ROOT = Path(__file__).resolve().parents[1]
DISC_INVENTORY = "research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt"
ARCHIVE_SIZE = 372626292
ARCHIVE_SHA = "3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24"
TABLE_VA = 0x45AF58
FIRST_GRAPHIC = 100250
TABLE_ROWS = 181
TABLE_STRIDE = 28
CODE_WINDOWS = {
    "status_message_graphic_store": (0x42FEE8, 0x42FEFD),
    "album_registration_and_lookup": (0x424FA0, 0x425020),
    "owned_pet_album_lookup_and_label": (0x42843E, 0x428519),
}


def digest(raw):
    return sha256(raw).hexdigest()


def inspect_archive(archive, disc_inventory):
    expected = {}
    for line in disc_inventory.splitlines():
        if line.startswith("CORE_FILE|"):
            fields = dict(item.split("=", 1) for item in line.split("|")[1:])
            if fields["category"] != "installer_support":
                path = "source/" + fields["path"].removeprefix("StoneAge/")
                expected[path] = (int(fields["size"]), fields["sha256"])
    with archive.open("rb") as source:
        archive_sha = file_digest(source, "sha256").hexdigest()
    if (archive.stat().st_size, archive_sha) != (ARCHIVE_SIZE, ARCHIVE_SHA):
        raise ValueError("P3H archive size or SHA-256 mismatch")
    with ZipFile(archive) as z:
        members = z.infolist()
        if len(members) != 379 or len({i.filename for i in members}) != len(members):
            raise ValueError("P3H member inventory mismatch")
        actual = {}
        for member in members:
            with z.open(member) as source:
                member_sha = file_digest(source, "sha256").hexdigest()
            if member.filename.startswith("source/"):
                actual[member.filename] = (member.file_size, member_sha)
        if len(expected) != 375 or actual != expected:
            raise ValueError("P3H original members differ from retail disc inventory")
        selected = ("source/sa_3.exe", "source/StoneAge.exe", "source/data/spradrn_1.bin",
                    "source/data/spr_1.bin", "source/data/adrn_1.bin", "source/data/real_1.bin")
        files = {
            name: {"bytes": actual[name][0], "sha256": actual[name][1],
                   "crc32": f"{z.getinfo(name).CRC:08x}"}
            for name in selected
        }
        source = {"bytes": ARCHIVE_SIZE, "sha256": archive_sha, "members_crc_verified": len(members),
                  "original_disc_files_sha256_matched": len(actual), "files": files}
        result = inspect_album(z)
    return {"schema": "stoneage.pet39.tw10_retail_client_album.r1", "archive": source,
            **result, "official_live_release_roster_verified": False,
            "historical_pet_count": None, "native_client_executed": False}


def inspect_album(z):
    program = z.read("source/sa_3.exe")
    pe = pe_sections(program)
    data_section = next(s for s in pe["sections"] if s["name"] == ".data")
    delta = TABLE_VA - pe["image_base"] - data_section["virtual_addr"]
    table_size = TABLE_ROWS * TABLE_STRIDE
    if not 0 <= delta <= data_section["raw_size"] - table_size:
        raise ValueError("compiled album range lies outside original .data")
    start = data_section["raw_ptr"] + delta
    table = program[start:start + table_size]
    text_section = next(s for s in pe["sections"] if s["name"] == ".text")
    text_va = pe["image_base"] + text_section["virtual_addr"]
    code_windows = {}
    for label, (begin, end) in CODE_WINDOWS.items():
        if not text_va <= begin < end <= text_va + text_section["raw_size"]:
            raise ValueError("compiled lookup window lies outside original .text")
        offset = text_section["raw_ptr"] + begin - text_va
        code_windows[label] = {"start_va": begin, "end_va_exclusive": end,
                               "sha256": digest(program[offset:offset + end - begin])}

    spr = z.read("source/data/spr_1.bin")
    groups, total_sequences, total_frames = validate_spr(spr, z.read("source/data/spradrn_1.bin"))
    by_graphic = {group[1]: group for group in groups}
    if len(by_graphic) != len(groups):
        raise ValueError("ambiguous SPR graphic IDs")

    adrn = z.read("source/data/adrn_1.bin")
    aliases = defaultdict(list)
    for pos in range(0, len(adrn), 80):
        bitmap, offset, size = struct.unpack_from("<III", adrn, pos)
        alias = struct.unpack_from("<I", adrn, pos + 76)[0]
        if alias:
            aliases[alias].append((bitmap, offset, size))

    rows, empty, portrait_spans = [], [], []
    for index in range(TABLE_ROWS):
        local = index * TABLE_STRIDE
        original = table[local:local + TABLE_STRIDE]
        slot, label_field, face = struct.unpack("<i20sI", original)
        label, terminator, padding = label_field.partition(b"\0")
        if not terminator or any(padding):
            raise ValueError(f"invalid album name field at row {index}")
        name = label.decode("cp950", errors="strict")
        graphic = FIRST_GRAPHIC + index
        if slot == -1:
            if (name, face) != ("無", 0):
                raise ValueError(f"invalid album placeholder at row {index}")
            empty.append(graphic)
            continue
        if slot < 0 or not name or not face or graphic not in by_graphic:
            raise ValueError(f"invalid populated album row {index}")
        group, _, begin, end, sequences, frames, _ = by_graphic[graphic]
        row = {
            "id": f"TW10_CLIENT_ALBUM:{graphic}", "source": "AUTHENTICATED_TW10_RETAIL_CLIENT",
            "evidence": "CLIENT_PET_IDENTITY_CANDIDATE", "name_as_written": name,
            "graphic_number": graphic, "source_file_offset": start + local,
            "source_row_sha256": digest(original), "spr_group_index": group,
            "spr_original_segment_sha256": digest(spr[begin:end]),
            "source_sequences": sequences, "source_frame_positions": frames,
            "portrait_logical_alias": face, "portrait_rd": None,
            "official_live_release_confirmed": False,
        }
        references = aliases[face]
        if len(references) > 1:
            raise ValueError(f"ambiguous same-build portrait alias {face}")
        if references:
            bitmap, offset, size = references[0]
            portrait_spans.append((offset, size, bitmap, row))
        rows.append(row)

    with z.open("source/data/real_1.bin") as real:
        for offset, size, bitmap, row in sorted(portrait_spans):
            real.seek(offset)
            raw = real.read(size)
            if len(raw) != size or not raw.startswith(b"RD"):
                raise ValueError(f"invalid original portrait RD for bitmap {bitmap}")
            row["portrait_rd"] = {"bitmap_number": bitmap, "offset": offset,
                                  "bytes": size, "sha256": digest(raw)}

    return {
        "table": {"file_offset": start, "virtual_address": TABLE_VA, "rows": TABLE_ROWS,
                  "stride": TABLE_STRIDE, "first_graphic": FIRST_GRAPHIC,
                  "sha256": digest(table), "placeholder_graphics": empty,
                  "placeholder_graphics_with_spr": sorted(set(empty) & by_graphic.keys())},
        "client_spr": {"groups": len(groups), "sequences": total_sequences, "frame_positions": total_frames},
        "compiled_lookup_windows": code_windows,
        "records": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    inventory = (ROOT / DISC_INVENTORY).read_text(encoding="utf-8")
    print(json.dumps(inspect_archive(args.archive, inventory), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
