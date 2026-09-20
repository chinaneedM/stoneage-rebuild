#!/usr/bin/env python3
"""Inventory Taiwan StoneAge v1.0 gameplay LSSPROTO message shapes.

The accepted retail sa_3.exe is consumed transiently. Output contains only
derived protocol names, xref RVAs, helper-call counts and callback RVAs.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from tools.stoneage_tw10_technical_probe import find_rows, extract_row
from tools.stoneage_tw10_mapcache_binary_probe import image_layout
from tools.stoneage_tw10_receive_map_join_probe import all_string_xrefs
from tools.stoneage_tw10_protocol_handoff_probe import linear_slice_calls

# Baseline protocol names preserved by the old generated LSSPROTO source family.
# Later macro-gated messages are intentionally excluded from this R1 inventory.
PROTOCOL_NAMES = (
    "W", "W2", "XYD", "EV", "EN", "DU", "EO", "BU", "JB", "LB",
    "RS", "RD", "B", "SKD", "ID", "PI", "DI", "DG", "DP", "I",
    "MI", "SI", "MSG", "PMSG", "PME", "AB", "ABI", "DAB", "AAB",
    "L", "TK", "MC", "M", "C", "CA", "CD", "R", "S", "D", "FS",
    "HL", "PR", "KS", "AC", "MU", "PS", "ST", "DT", "FT", "SKUP",
    "KN", "WN", "EF", "SE", "SP", "ClientLogin", "CreateNewChar",
    "CharDelete", "CharLogin", "CharList", "CharLogout", "ProcGet",
    "PlayerNumGet", "Echo", "Shutdown", "NU", "TD", "FM", "WO",
)

SEND_RANGE = (0x18C00, 0x19730)
RECV_RANGE = (0x19730, 0x1AA8A)

SEND_HELPERS = {
    0x1B480: "header",
    0x1B0B0: "int",
    0x1B0F0: "string",
    0x1B060: "append",
    0x1B3F0: "send",
}
RECV_HELPERS = {
    0x1B120: "int",
    0x1B140: "string",
    0x1B4C0: "wrap",
}

# Expected shapes come only from the old generated descendant protocol surface.
# They are comparison controls, never primary evidence.
EXPECTED = {
    ("send", "C"): (1, 0),
    ("recv", "C"): (0, 1),
    ("recv", "CA"): (0, 1),
    ("recv", "CD"): (0, 1),
    ("send", "S"): (0, 1),
    ("recv", "S"): (0, 1),
    ("recv", "I"): (0, 1),
    ("send", "MI"): (2, 0),
    ("recv", "SI"): (2, 0),
    ("recv", "PME"): (7, 1),
    ("send", "KS"): (1, 0),
    ("recv", "KS"): (2, 0),
    ("send", "PS"): (3, 1),
    ("recv", "PS"): (4, 0),
    ("send", "SKUP"): (1, 0),
    ("recv", "SKUP"): (1, 0),
    ("send", "WN"): (5, 1),
    ("recv", "WN"): (4, 1),
    ("recv", "EF"): (2, 1),
    ("recv", "SE"): (4, 0),
    ("recv", "RS"): (0, 1),
    ("recv", "RD"): (0, 1),
    ("recv", "B"): (0, 1),
    ("recv", "D"): (3, 1),
    ("recv", "MC"): (8, 1),
    ("send", "M"): (5, 0),
    ("recv", "M"): (5, 1),
    ("send", "CreateNewChar"): (12, 1),
}


def collect_protocol_xrefs(data, base, sections):
    rows = []
    for name in PROTOCOL_NAMES:
        for occurrence, string_rva, ins in all_string_xrefs(
            data, base, sections, name
        ):
            rva = ins.address - base
            region = None
            if SEND_RANGE[0] <= rva < SEND_RANGE[1] and ins.mnemonic == "push":
                region = "send"
            elif RECV_RANGE[0] <= rva < RECV_RANGE[1] and ins.mnemonic == "mov":
                region = "recv"
            if region is None:
                continue
            rows.append(
                {
                    "name": name,
                    "occurrence": occurrence,
                    "string_rva": string_rva,
                    "instruction_rva": rva,
                    "mnemonic": ins.mnemonic,
                    "region": region,
                }
            )
    # Exact duplicates can arise when source strings are represented more than once.
    uniq = {}
    for row in rows:
        uniq[(row["region"], row["instruction_rva"], row["name"])] = row
    return sorted(
        uniq.values(),
        key=lambda x: (
            0 if x["region"] == "send" else 1,
            x["instruction_rva"],
            x["name"],
        ),
    )


def summarize_slice(calls, helpers):
    counts = {"int": 0, "string": 0, "header": 0, "append": 0, "send": 0, "wrap": 0}
    nonhelpers = []
    for callsite, target in calls:
        label = helpers.get(target)
        if label is None:
            nonhelpers.append((callsite, target))
        else:
            counts[label] = counts.get(label, 0) + 1
    return counts, nonhelpers


def region_slices(data, base, sections, xrefs, region):
    selected = [x for x in xrefs if x["region"] == region]
    lo, hi = SEND_RANGE if region == "send" else RECV_RANGE
    helpers = SEND_HELPERS if region == "send" else RECV_HELPERS
    result = []
    for index, row in enumerate(selected):
        start = row["instruction_rva"]
        end = selected[index + 1]["instruction_rva"] if index + 1 < len(selected) else hi
        if not (lo <= start < end <= hi):
            continue
        _insns, calls_va = linear_slice_calls(
            data, base, sections, base + start, base + end
        )
        calls = [(site - base, target - base) for site, target in calls_va]
        counts, nonhelpers = summarize_slice(calls, helpers)
        result.append((row, end, counts, nonhelpers, calls))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin", required=True)
    args = ap.parse_args()

    print("StoneAge Taiwan v1.0 gameplay protocol shape inventory — R1")
    print("SCOPE|accepted-retail-disc|derived-binary-metadata-only|no-payload")
    print(
        f"REGIONS|send=0x{SEND_RANGE[0]:x}-0x{SEND_RANGE[1]:x}|"
        f"recv=0x{RECV_RANGE[0]:x}-0x{RECV_RANGE[1]:x}"
    )

    img, rows, layout, joliet = find_rows(args.bin)
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    try:
        by_path = {r["path"]: r for r in rows if not r["is_dir"]}
        row = by_path.get("StoneAge/sa_3.exe")
        if row is None:
            raise SystemExit("sa_3.exe missing")
        exe = root / "sa_3.exe"
        extract_row(img, row, exe)
        data, _pe, base, sections, _imports = image_layout(exe)
        xrefs = collect_protocol_xrefs(data, base, sections)

        for region in ("send", "recv"):
            selected = [x for x in xrefs if x["region"] == region]
            print(
                f"REGION_SUMMARY|region={region}|protocol_xrefs={len(selected)}|"
                f"unique_names={len({x['name'] for x in selected})}"
            )
            for row, end, counts, nonhelpers, calls in region_slices(
                data, base, sections, xrefs, region
            ):
                print(
                    f"PROTOCOL|region={region}|name={row['name']}|"
                    f"xref_rva=0x{row['instruction_rva']:x}|string_rva=0x{row['string_rva']:x}|"
                    f"occurrence={row['occurrence']}|slice_end_rva=0x{end:x}|"
                    f"int_fields={counts.get('int',0)}|string_fields={counts.get('string',0)}|"
                    f"wrap_calls={counts.get('wrap',0)}|append_calls={counts.get('append',0)}|"
                    f"header_calls={counts.get('header',0)}|send_calls={counts.get('send',0)}|"
                    f"nonhelper_calls={len(nonhelpers)}"
                )
                for order, (callsite, target) in enumerate(calls, 1):
                    print(
                        f"CALL|region={region}|name={row['name']}|order={order}|"
                        f"callsite_rva=0x{callsite:x}|target_rva=0x{target:x}"
                    )
                for order, (callsite, target) in enumerate(nonhelpers, 1):
                    print(
                        f"NONHELPER|region={region}|name={row['name']}|order={order}|"
                        f"callsite_rva=0x{callsite:x}|target_rva=0x{target:x}"
                    )

                expected = EXPECTED.get((region, row["name"]))
                if expected is not None:
                    observed = (counts.get("int", 0), counts.get("string", 0))
                    print(
                        f"SHAPE_COMPARE|region={region}|name={row['name']}|"
                        f"observed_int={observed[0]}|observed_string={observed[1]}|"
                        f"lineage_int={expected[0]}|lineage_string={expected[1]}|"
                        f"exact={int(observed == expected)}"
                    )
    finally:
        img.close()
        td.cleanup()


if __name__ == "__main__":
    main()
