"""Reconcile actual retained pixel receipts with PET57's residual graphics."""

import argparse
from collections import Counter, defaultdict
import gzip
import json

from tools.stoneage_pet_high_first_57_coverage import P, ROOT, TARGET, PINS, blob, gzrows


OUTPUT = P / "PET-HIGH-FIRST-59-RESIDUAL-PIXEL-RECEIPTS-R1.json"
INPUTS = {
    "coverage": (TARGET, "c291a0a597ba1b6270191c561f10401293df161e"),
    "frames": PINS["frames"],
    "bindings": (
        ROOT / "research/recovered/tw85-frame-bitmap-r29/BITMAP-BINDINGS-R29.tsv.gz",
        "fd024d9b30ed478ece7810a0207b157fd627a629",
    ),
    "cn50": (P / "PET-HIGH-FIRST-11-PC-INDEXED-PIXEL-RECEIPTS-R1.json.gz", "6ba6e7f9772c90dd1bad05f012e330f43ea41158"),
    "tw85": (P / "PET-HIGH-FIRST-12-TW85-INDEXED-PIXELS-R1.json.gz", "1e384d3faf93502e4e91b124fcc1a49761ca7d97"),
    "tw85_long": (P / "PET-HIGH-FIRST-13-TW85-LONG-AND-SPECIAL-R1.json.gz", "97fb8ffecda20d139ce0e72b7fb3548ef72d98dc"),
}


def derive():
    data = {}
    for key, (path, expected) in INPUTS.items():
        raw = path.read_bytes()
        assert blob(raw) == expected, (key, "source identity")
        if key not in ("frames", "bindings"):
            data[key] = json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)
    data["tw85_long"] = data["tw85_long"]["observations"]
    assert data["tw85_long"]["source_files"] == data["tw85"]["source_files"]

    coverage = data["coverage"]
    groups = {}
    positions = defaultdict(list)
    for row in coverage["rows"]:
        for group in row["tw85_physical_groups"]:
            index = group["group_index"]
            assert index not in groups or groups[index] == group
            groups[index] = group
            positions[index].append(row["position"])
    by_hash = {g["segment_sha256"]: index for index, g in groups.items()}
    assert len(by_hash) == len(groups) == 66

    frames = defaultdict(list)
    for row in gzrows(INPUTS["frames"][0]):
        index = int(row["group_index"])
        if index in groups:
            assert int(row["spr_no"]) == groups[index]["graphic"]
            bitmap = None if row["sentinel"] == "1" else int(row["bmp_no"])
            animation = int(row["anim_index"])
            assert int(row["frame_index"]) == len(frames[index, animation])
            frames[index, animation].append([bitmap, *(int(row[k]) for k in ("pos_x", "pos_y", "sound_no"))])

    bindings = {}
    numbers = {f[0] for sequence in frames.values() for f in sequence if f[0] is not None}
    for row in gzrows(INPUTS["bindings"][0]):
        number = int(row["bitmapno"])
        if number in numbers:
            indices = [int(n) for n in row["native_indices"].split(",")]
            digests = [entry.split(":", 1)[1] for entry in row["complete_rd_content_keys"].split(",")]
            assert len(indices) == len(digests)
            bindings[number] = dict(zip(indices, digests))
    assert bindings.keys() == numbers

    direct = defaultdict(list)
    exact_decoded = set()
    for key in ("tw85", "tw85_long"):
        source = data[key]
        decoded = {int(i): b for i, b in source["observed_blocks"].items()
                   if b["status"] == "DUAL_DECODED_INDEX_PIXELS"}
        for record, block in decoded.items():
            bitmap = block["bitmap"]
            if bitmap in numbers and bindings[bitmap].get(record) == block["rd_sha256"]:
                if set(bindings[bitmap].values()) == {block["rd_sha256"]}:
                    exact_decoded.add(bitmap)
        for sample in source["sequences"]:
            index, animation = sample["physical_group"], sample["animation_index"]
            if index not in groups:
                continue
            assert (groups[index]["graphic"], groups[index]["segment_sha256"]) == (sample["spr"], sample["spr_segment_sha256"])
            assert sample["frames"] == frames[index, animation]
            bitmaps = [f[0] for f in sample["frames"] if f[0] is not None]
            indices = [source["frame_bitmap_to_adrn_index"][str(n)] for n in bitmaps]
            if indices and all(i in decoded and decoded[i]["rd_sha256"] == bindings[n].get(i)
                               for i, n in zip(indices, bitmaps)):
                direct[index].append(dict(source=key, animation=animation, nonsentinel_positions=len(indices)))

    other = defaultdict(list)
    for record in data["cn50"]["cn50_album"]:
        sample = record["sample"]
        if not sample or sample["group_sha256"] not in by_hash:
            continue
        index, animation = by_hash[sample["group_sha256"]], sample["animation_index"]
        assert sample["spr"] == groups[index]["graphic"] and sample["frames"] == frames[index, animation]
        bitmaps = [f[0] for f in sample["frames"] if f[0] is not None]
        blocks = data["cn50"]["cn50_observed_blocks"]
        if bitmaps and all(blocks[str(n)]["index_pixels_sha256"] and
                           set(bindings[n].values()) == {blocks[str(n)]["rd_sha256"]} for n in bitmaps):
            other[index].append(dict(source="cn50", ordinal=record["ordinal"], animation=animation,
                                     nonsentinel_positions=len(bitmaps)))

    total = Counter()
    observed = Counter()
    for (index, _), sequence in frames.items():
        total[index] += sum(f[0] is not None for f in sequence)
        observed[index] += sum(f[0] in exact_decoded for f in sequence)
    for index, group in groups.items():
        assert total[index] == group["mapped_frames"]
    rows = [
        dict(group=index, graphic=groups[index]["graphic"], positions=positions[index],
             nonsentinel_frame_positions=total[index], with_direct_exact_block_receipt=observed[index],
             tw85_complete_samples=direct[index], cn50_exact_spr_and_rd_complete_samples=other[index])
        for index in sorted(groups)
    ]

    portraits = {}
    cn_records = defaultdict(list)
    for row in data["cn50"]["cn50_album"]:
        if row["portrait_selected_bitmap"] is not None:
            cn_records[str(row["portrait_alias"])].append(row)
    for alias, rows_for_alias in coverage["portrait_alias_candidates"].items():
        native = {x["native_index"]: x for row in rows_for_alias for x in row["native_candidates"]}
        matches = []
        for key in ("tw85", "tw85_long"):
            source = data[key]
            for index, bitmap in source["portraits_by_original_alias"].get(alias, []):
                if index not in native:
                    continue
                b = source["observed_blocks"][str(index)]
                if b["status"] == "DUAL_DECODED_INDEX_PIXELS":
                    assert (bitmap, b["adrn_sha256"], b["rd_sha256"]) == (
                        native[index]["bitmapno"], native[index]["adrn_sha256"], native[index]["rd_sha256"])
                    matches.append(dict(source=key, native_index=index))
        if not matches:
            for row in cn_records[alias]:
                b = data["cn50"]["cn50_observed_blocks"][str(row["portrait_selected_bitmap"])]
                if b["index_pixels_sha256"]:
                    matches.extend(dict(source="cn50", ordinal=row["ordinal"], native_index=index)
                                   for index, value in native.items()
                                   if (b["rd_sha256"], b["width"], b["height"]) ==
                                      (value["rd_sha256"], value["width"], value["height"]))
        portraits[alias] = matches

    missing = [row["group"] for row in rows if not row["tw85_complete_samples"] and not row["cn50_exact_spr_and_rd_complete_samples"]]
    summary = dict(
        physical_groups=len(rows),
        same_carrier_complete_sample_groups=sum(bool(row["tw85_complete_samples"]) for row in rows),
        additional_cn50_exact_sample_groups=sum(bool(row["cn50_exact_spr_and_rd_complete_samples"])
                                                and not row["tw85_complete_samples"] for row in rows),
        groups_without_complete_sample_in_compared_receipts=missing,
        nonsentinel_frame_positions=sum(total.values()),
        nonsentinel_positions_with_direct_exact_block_receipt=sum(observed.values()),
        portrait_candidates_with_same_carrier_receipt=sum(any(m["source"] != "cn50" for m in v) for v in portraits.values()),
        additional_portrait_candidates_with_cn50_exact_rd_receipt=sum(any(m["source"] == "cn50" for m in v) for v in portraits.values()),
        portrait_candidates_without_compared_receipt=sum(not v for v in portraits.values()),
        strict_acquisition_gaps=coverage["summary"]["strict_gap_count"],
        new_official_acquisition_closures=0,
    )
    return dict(schema="stoneage.pet59.residual_pixel_receipt_crosswalk.r1",
                inputs={k: dict(path=str(p.relative_to(ROOT)), git_blob=h) for k, (p, h) in INPUTS.items()},
                summary=summary, groups=rows, portrait_candidates=portraits,
                original_assets_published=False, new_original_bytes_reacquired=False,
                official_identity_verified=False, native_runtime_verified=False,
                scope="Previously verified index pixel receipts only. Matched samples do not certify full animation, palette, pet name or live release.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = derive()
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    if args.write:
        OUTPUT.write_bytes(raw)
    else:
        assert OUTPUT.read_bytes() == raw
    print("PET59", json.dumps(report["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
