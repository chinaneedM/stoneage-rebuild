"""World34 R2: qualify mapped PE source bytes before the RAR CRC failure.

Private, read-only verification. Never run the original EXE, launch an
account/server process, or publish any original binary or itemset contents.
The prefix is deliberately *not* accepted as a complete original EXE.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD34-R2-MAPPED-PE-SOURCE-R1.json"
W31 = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD31-RECOVERY-SOURCE-R1.json"
W33 = ROOT / "research/recovered/STONEAGE-STAGE-A-WORLD33-BATTLE-ITEM-GATE-SOURCE-R1.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sections(raw):
    if raw[:2] != b"MZ":
        raise ValueError("not an MZ executable prefix")
    pe = struct.unpack_from("<I", raw, 0x3c)[0]
    if raw[pe:pe + 4] != b"PE\0\0":
        raise ValueError("not the expected PE header")
    n, oh_size = struct.unpack_from("<H", raw, pe + 6)[0], struct.unpack_from("<H", raw, pe + 20)[0]
    base = struct.unpack_from("<I", raw, pe + 24 + 28)[0]
    if n != 5 or base != 0x400000:
        raise ValueError("unexpected original PE layout")
    ptr, count = struct.unpack_from("<II", raw, pe + 12)
    rows = []
    for index in range(n):
        entry = pe + 24 + oh_size + 40 * index
        name = raw[entry:entry + 8].rstrip(b"\0").decode("ascii")
        rva = struct.unpack_from("<I", raw, entry + 12)[0]
        size, offset = struct.unpack_from("<II", raw, entry + 16)
        if size and offset + size > len(raw):
            raise ValueError("file-backed PE section crosses the decoded prefix")
        rows.append((name, base + rva, size, offset))
    return (ptr, count), rows


def reader(raw, pe_rows):
    def read(start, end):
        for _, va, size, offset in pe_rows:
            if size and va <= start < end <= va + size:
                return raw[offset + start - va:offset + end - va]
        raise ValueError(f"unmapped exact original PE window {start:#x}..{end:#x}")
    return read


def verify(server_prefix, client, itemset, *, report=None, w31=None, w33=None):
    r = report or json.loads(REPORT.read_bytes())
    w31 = w31 or json.loads(W31.read_bytes())
    w33 = w33 or json.loads(W33.read_bytes())
    s = r["gmsv_decompression"]
    if len(server_prefix) != s["verified_common_output_prefix_bytes"] or digest(server_prefix) != s["prefix_sha256"]:
        raise ValueError("the exact bounded server decoded prefix is not present")
    if len(client) != 561152 or digest(client) != "ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16":
        raise ValueError("client source does not match WORLD33")
    if digest(itemset) != "a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688":
        raise ValueError("configured original itemset differs")
    (ptr, count), server_rows = sections(server_prefix)
    if (ptr, count) != (r["pe"]["coff_symbol_table_file_offset"], r["pe"]["coff_symbol_count"]):
        raise ValueError("source COFF boundary is not pinned")
    if ptr + count * 18 <= len(server_prefix):
        raise ValueError("expected COFF symbol-record cutoff was not encountered")
    expected_sections = {x["name"]: x for x in r["pe"]["sections"]}
    for name, va, size, offset in server_rows:
        if size:
            q = expected_sections[name]
            if (va, size, offset, offset + size) != (q["virtual_address"], q["raw_bytes"], q["raw_offset"], q["raw_end"]):
                raise ValueError("mapped source layout changed")
            if digest(server_prefix[offset:offset + size]) != q["sha256"]:
                raise ValueError("section source bytes changed")
        elif name != ".bss":
            raise ValueError("unexpected zero-byte section")
    sr = reader(server_prefix, server_rows)
    client_pe, client_entries = sections_any(client)
    cr = reader(client, client_entries)
    for original, read, windows in [
        ("WORLD31", sr, w31["program"]["emulator_source_windows"]),
        ("WORLD33 server", sr, w33["program"]["server_windows"]),
        ("WORLD33 client", cr, w33["program"]["client_windows"]),
    ]:
        for start, end, expected in windows:
            if digest(read(start, end)) != expected:
                raise ValueError(f"{original} exact historical original window differs: {start:#x}")
    for edge in r["qualified_code_evidence"]["additional_static_call_sites"]:
        pos, kind = edge["address"], edge["kind"]
        raw = sr(pos, pos + (6 if kind == "indirect" else 5))
        if digest(raw) != edge["sha256"]:
            raise ValueError(f"original source call differs: {edge['role']}")
        if kind == "indirect":
            if raw[:2] != bytes((0xff, 0x95)) or struct.unpack_from("<i", raw, 2)[0] != -0x11c:
                raise ValueError("indirect item callback pointer source differs")
        else:
            if raw[0] != {"call":0xe8,"jump":0xe9}[kind] or pos + 5 + struct.unpack_from("<i", raw, 1)[0] != edge["destination"]:
                raise ValueError(f"original source relative call differs: {edge['role']}")
    original = itemset.splitlines(keepends=True)
    for row in r["item_original_rows"]:
        physical = next((x for x in w33["source_class_witnesses"] if x["row"]["id"] == row["id"]), None)
        if physical is None:
            raise ValueError("WORLD33 source row missing")
        line_no = physical["row"]["line"]
        raw = original[line_no - 1]
        if digest(raw) != row["row_sha256"] or digest(raw) != physical["row"]["row_sha256"]:
            raise ValueError("original complete CP950 row differs")
        fields = raw.rstrip(b"\r\n").split(b",")
        if (len(fields) != 94 or int(fields[16]) != row["id"] or
                fields[10] != b"ITEM_useRecovery" or
                int(fields[20]) != row["fieldtype"] or int(fields[21]) != row["target"] or
                digest(fields[3]) != row["argument_sha256"] or
                fields[3].decode("cp950") != row["argument"]):
            raise ValueError("original item fields differ")
    return {"pinned_server_windows":18, "pinned_client_windows":5,
            "validated_item_rows":len(r["item_original_rows"]),
            "new_static_call_sites":len(r["qualified_code_evidence"]["additional_static_call_sites"]),
            "full_member_crc_validated":False, "full_callback_return_replayed":False}


def sections_any(raw):
    if raw[:2] != b"MZ":
        raise ValueError("client is not MZ")
    pe = struct.unpack_from("<I", raw, 0x3c)[0]
    if raw[pe:pe+4] != b"PE\0\0":
        raise ValueError("client is not PE")
    n, oh = struct.unpack_from("<H", raw, pe+6)[0], struct.unpack_from("<H", raw, pe+20)[0]
    base = struct.unpack_from("<I", raw, pe+24+28)[0]
    rows=[]
    for i in range(n):
        e=pe+24+oh+40*i
        name=raw[e:e+8].rstrip(b"\0").decode("ascii")
        rva=struct.unpack_from("<I",raw,e+12)[0]
        size,off=struct.unpack_from("<II",raw,e+16)
        if size and off+size>len(raw):
            raise ValueError("client section raw bytes outside file")
        rows.append((name,base+rva,size,off))
    return (base,n),rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("decoded_gmsv_prefix", type=Path)
    p.add_argument("original_sa_2903", type=Path)
    p.add_argument("configured_itemset", type=Path)
    args=p.parse_args()
    result=verify(args.decoded_gmsv_prefix.read_bytes(),args.original_sa_2903.read_bytes(),args.configured_itemset.read_bytes())
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
