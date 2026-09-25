#!/usr/bin/env python3
"""Bounded CAB-directory probe for Stoneage-5 DATA1.CAB inside the IA BIN/CUE.

Reads only a small prefix of DATA1.CAB plus CFDATA headers. It does not
download the 612 MB cabinet and does not extract proprietary payloads.
"""
from __future__ import annotations

import struct

from tools.stoneage_sa_arena_ia_probe import SECTOR, clean, logical_sector_read
from tools.stoneage_stoneage5_msi_probe import find_entry, load_root

CAB_PREFIX_LIMIT = 512 * 1024
TARGET_SUFFIXES = (".exe", ".bin", ".txt")
COMP_NAMES = {0: "NONE", 1: "MSZIP", 2: "QUANTUM", 3: "LZX"}


def iso_file_slice(bin_url, entry, track, start, length):
    size = int(entry["size"])
    start = int(start)
    length = int(length)
    if start < 0 or length < 0 or start + length > size:
        raise ValueError("slice-out-of-range")
    if length == 0:
        return b"", 206, ""
    first_sector = start // SECTOR
    end = start + length
    last_sector = (end + SECTOR - 1) // SECTOR
    count = last_sector - first_sector
    status, content_range, data, honored = logical_sector_read(
        bin_url,
        int(entry["extent"]) + first_sector,
        count,
        int(track["index_frames"]),
        str(track["mode"]),
    )
    if not honored:
        raise RuntimeError(
            f"range-not-honored status={status} content_range={content_range}"
        )
    offset = start - first_sector * SECTOR
    return data[offset:offset + length], status, content_range


def _cstr(buf, pos):
    end = buf.find(b"\x00", pos)
    if end < 0:
        raise ValueError("unterminated-cab-string")
    raw = buf[pos:end]
    for enc in ("utf-8", "gb18030", "cp1252"):
        try:
            return raw.decode(enc), end + 1
        except UnicodeDecodeError:
            pass
    return raw.decode("latin1", "replace"), end + 1


def parse_cab_header(buf):
    if len(buf) < 36 or buf[:4] != b"MSCF":
        raise ValueError("not-ms-cabinet")
    cb_cabinet = struct.unpack_from("<I", buf, 8)[0]
    coff_files = struct.unpack_from("<I", buf, 16)[0]
    version_minor = buf[24]
    version_major = buf[25]
    c_folders, c_files, flags, set_id, i_cabinet = struct.unpack_from("<HHHHH", buf, 26)
    pos = 36
    cb_cfheader = cb_cffolder = cb_cfdata = 0
    if flags & 0x0004:
        if len(buf) < pos + 4:
            raise ValueError("short-reserve-header")
        cb_cfheader = struct.unpack_from("<H", buf, pos)[0]
        cb_cffolder = buf[pos + 2]
        cb_cfdata = buf[pos + 3]
        pos += 4 + cb_cfheader
    prev_cab = prev_disk = next_cab = next_disk = ""
    if flags & 0x0001:
        prev_cab, pos = _cstr(buf, pos)
        prev_disk, pos = _cstr(buf, pos)
    if flags & 0x0002:
        next_cab, pos = _cstr(buf, pos)
        next_disk, pos = _cstr(buf, pos)
    return {
        "cb_cabinet": cb_cabinet,
        "coff_files": coff_files,
        "version_major": version_major,
        "version_minor": version_minor,
        "c_folders": c_folders,
        "c_files": c_files,
        "flags": flags,
        "set_id": set_id,
        "i_cabinet": i_cabinet,
        "cb_cfheader": cb_cfheader,
        "cb_cffolder": cb_cffolder,
        "cb_cfdata": cb_cfdata,
        "folder_table_offset": pos,
        "prev_cab": prev_cab,
        "prev_disk": prev_disk,
        "next_cab": next_cab,
        "next_disk": next_disk,
    }


def parse_cab_folders(buf, header):
    pos = int(header["folder_table_offset"])
    reserve = int(header["cb_cffolder"])
    rows = []
    for index in range(int(header["c_folders"])):
        if pos + 8 + reserve > len(buf):
            raise ValueError("short-folder-table")
        coff_cab_start, c_cfdata, type_compress = struct.unpack_from("<IHH", buf, pos)
        rows.append({
            "index": index,
            "coff_cab_start": coff_cab_start,
            "c_cfdata": c_cfdata,
            "type_compress": type_compress,
            "compress_base": type_compress & 0x000F,
            "compress_name": COMP_NAMES.get(type_compress & 0x000F, "UNKNOWN"),
            "compress_param": type_compress >> 8,
        })
        pos += 8 + reserve
    return tuple(rows)


def parse_cab_files(buf, header):
    pos = int(header["coff_files"])
    rows = []
    for index in range(int(header["c_files"])):
        if pos + 16 > len(buf):
            raise ValueError("short-file-table")
        cb_file, uoff_folder_start, i_folder, date, time, attribs = struct.unpack_from(
            "<IIHHHH", buf, pos
        )
        pos += 16
        name, pos = _cstr(buf, pos)
        rows.append({
            "index": index,
            "name": name,
            "size": cb_file,
            "uoff_folder_start": uoff_folder_start,
            "i_folder": i_folder,
            "date": date,
            "time": time,
            "attribs": attribs,
        })
    return tuple(rows), pos


def dos_datetime(date, time):
    if not date:
        return ""
    year = 1980 + ((date >> 9) & 0x7F)
    month = (date >> 5) & 0x0F
    day = date & 0x1F
    hour = (time >> 11) & 0x1F
    minute = (time >> 5) & 0x3F
    second = (time & 0x1F) * 2
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return ""
    return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"


def main():
    print("StoneAge Stoneage-5 DATA1.CAB bounded directory probe — R1")
    print(
        "SCOPE|ISO9660-DATA1.CAB-prefix+cabinet-directory+CFDATA-headers|"
        "no-full-cab-download|no-payload-extraction|no-proprietary-payload-commit"
    )
    meta, cue_name, cue_bytes, track, bin_row, bin_url, info, entries = load_root()
    cab = find_entry(entries, "DATA1.CAB")
    if cab is None:
        raise RuntimeError("DATA1.CAB-not-found")
    want = min(CAB_PREFIX_LIMIT, int(cab["size"]))
    prefix, status, cr = iso_file_slice(bin_url, cab, track, 0, want)
    header = parse_cab_header(prefix)
    folders = parse_cab_folders(prefix, header)
    if int(header["coff_files"]) >= len(prefix):
        raise RuntimeError("file-table-beyond-prefix")
    files, file_table_end = parse_cab_files(prefix, header)

    print(
        f"CAB|name=DATA1.CAB|iso_size={cab['size']}|iso_extent={cab['extent']}|"
        f"prefix_bytes={len(prefix)}|status={status}|content_range={clean(cr)}|"
        f"signature=MSCF|cabinet_size={header['cb_cabinet']}|"
        f"version={header['version_major']}.{header['version_minor']}|"
        f"folders={header['c_folders']}|files={header['c_files']}|"
        f"flags=0x{header['flags']:04x}|set_id={header['set_id']}|"
        f"cabinet_index={header['i_cabinet']}|coff_files={header['coff_files']}|"
        f"file_table_end={file_table_end}"
    )
    print(
        f"SPAN|prev_cab={clean(header['prev_cab'])}|prev_disk={clean(header['prev_disk'])}|"
        f"next_cab={clean(header['next_cab'])}|next_disk={clean(header['next_disk'])}"
    )

    for folder in folders:
        print(
            f"FOLDER|index={folder['index']}|coff_cab_start={folder['coff_cab_start']}|"
            f"data_blocks={folder['c_cfdata']}|compress={folder['compress_name']}|"
            f"type_compress=0x{folder['type_compress']:04x}|"
            f"compress_param={folder['compress_param']}"
        )
        try:
            raw, st, crr = iso_file_slice(
                bin_url, cab, track, int(folder["coff_cab_start"]),
                8 + int(header["cb_cfdata"])
            )
            if len(raw) >= 8:
                csum, cb_data, cb_uncomp = struct.unpack_from("<IHH", raw, 0)
                print(
                    f"CFDATA0|folder={folder['index']}|status={st}|checksum=0x{csum:08x}|"
                    f"compressed_bytes={cb_data}|uncompressed_bytes={cb_uncomp}|"
                    f"content_range={clean(crr)}"
                )
        except Exception as exc:
            print(
                f"CFDATA0_ERROR|folder={folder['index']}|kind={type(exc).__name__}|"
                f"message={clean(exc)}"
            )

    print(f"COUNT|cab_files|{len(files)}")
    targets = [
        f for f in files
        if f["name"].lower().endswith(TARGET_SUFFIXES)
        or f["name"].lower().endswith(".sab")
        or f["name"].lower().endswith(".sap")
    ]
    print(f"COUNT|target_inventory|{len(targets)}")
    for f in files:
        lname = f["name"].lower()
        if lname.endswith(TARGET_SUFFIXES):
            print(
                f"FILE|index={f['index']}|name={clean(f['name'])}|size={f['size']}|"
                f"folder={f['i_folder']}|uoff={f['uoff_folder_start']}|"
                f"end={f['uoff_folder_start'] + f['size']}|"
                f"mtime={dos_datetime(f['date'],f['time'])}|attribs=0x{f['attribs']:04x}"
            )
    sab = [f for f in files if f["name"].lower().endswith(".sab")]
    sap = [f for f in files if f["name"].lower().endswith(".sap")]
    if sab:
        print(
            f"SUMMARY|sab_count={len(sab)}|sab_first={clean(sab[0]['name'])}|"
            f"sab_last={clean(sab[-1]['name'])}|sab_folder_ids="
            + ",".join(str(x) for x in sorted({f['i_folder'] for f in sab}))
        )
    if sap:
        print(
            f"SUMMARY|sap_count={len(sap)}|sap_first={clean(sap[0]['name'])}|"
            f"sap_last={clean(sap[-1]['name'])}|sap_folder_ids="
            + ",".join(str(x) for x in sorted({f['i_folder'] for f in sap}))
        )
    print(
        "EVIDENCE_BOUNDARY|cabinet structure and file metadata are byte-derived from "
        "the preserved optical object; no large cabinet payload or game resource "
        "body is downloaded or committed by this probe."
    )


if __name__ == "__main__":
    main()
