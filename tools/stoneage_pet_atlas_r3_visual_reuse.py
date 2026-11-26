"""Private atlas R3 exact early-to-later visual reuse plan.

No original PNG or source archive is read/published by this tool. Existing private
preview PNGs may be attached only to an exact RD or complete sequence proof.
The proof is of asset equivalence, never same official pet identity.
"""
import argparse
from collections import defaultdict, Counter
import hashlib
import json
from pathlib import Path
from tools.stoneage_pet_high_first_57_coverage import ROOT, PINS, blob, gzrows
from tools.stoneage_pet_high_first_66_motion_inheritance import EXTRA, sequence_tables

P = ROOT / "research/pets"
PINS_R3 = {
    "early": (P / "PET-DETAIL-EVIDENCE23-TW10-124-ORIGINAL-PRIVATE-VISUAL-ATLAS-R1.json", "a3e2584aec45262ebc91f98ec40f5e128e490dbe"),
    "portrait_pairs": (P / "PET-DETAIL-EVIDENCE33-FOUR-PC-PORTRAIT-PIXEL-PAIRS-R1.json", "c638bebc992604a9742dee14f2b8b613c38cf615"),
    "later": (P / "PET-HIGH-FIRST-74-UNIFIED-VISUAL-R1.json", "8c69875806d9dff353c60bc3834ec98197d1059d"),
    "portraits": (P / "PET-HIGH-FIRST-73-PORTRAIT-RESIDUAL-R1.json", "cc1548a2292b782e071e7e1109d67cee1fb3209c"),
    **{k: EXTRA[k] for k in ("tw10_receipt","tw10_groups","tw10_animations","tw10_frames","tw10_adrn","tw85_animation")},
    **{k: PINS[k] for k in ("groups","frames","native")},
}
def digest(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode()).hexdigest()

def exact_key(row, rd_field):
    return (row[rd_field], int(row["size"]), int(row["width"]), int(row["height"]))

def select_rd(rows, wanted, rd_field):
    selected = defaultdict(list)
    for r in rows:
        n = int(r["bitmapno"])
        if n in wanted:
            selected[n].append(exact_key(r, rd_field))
    # Do not silently select the last row of a collision.
    return {n: rs[0] for n, rs in selected.items() if len(rs) == 1 and rs[0][2] > 0 and rs[0][3] > 0}

def build():
    data = {}
    for k, (p, h) in PINS_R3.items():
        assert blob(p.read_bytes()) == h, k
        if p.suffix == ".json":
            data[k] = json.loads(p.read_bytes())
    early, late, portraits, pairs, motion = (data[k] for k in ("early","later","portraits","portrait_pairs","tw10_receipt"))
    assert len(early["profiles"]) == 124 and len(late["groups"]) == 1739
    assert len(portraits["aliases"]) == 508 and sum(map(len, portraits["aliases"].values())) == 512
    assert not any(portraits[k] for k in ("official_identity_verified","original_assets_published","original_runtime_verified"))
    candidates = {}
    for p in early["profiles"]:
        rd = p["original_album_RD"]
        if rd:
            candidates[(p["original_portrait_logical_alias"],rd["original_rd_bitmap_number"],rd["original_rd_sha256"])] = dict(
                early_pet_id=p["pet_id"], path=f"portraits/{p['source_graphic_number']}.png",
                source="TW10_ORIGINAL_RD_EXACT_LATER_BLOCK", size=rd["original_rd_bytes"])
    for p in pairs["records"]:
        for v in p["variants"]:
            assert v["matches_preserved_cn50_physical_rd"] and v["matches_wayi_patch_80_byte_record_and_preserved_tw85_rd"]
            candidates[(p["logical_portrait_alias"],v["physical_bitmap_number"],v["rd_sha256"])] = dict(
                early_pet_id=p["pet_id"], path=f"later-portraits/{v['physical_bitmap_number']}.png",
                source="MIXED25_ORIGINAL_RD_EXACT_LATER_BLOCK", size=v["rd_bytes"],
                pixel_sha256=v["indexed_pixels_sha256"])
    assert len(candidates) == 128
    all_portraits = {}
    available = {}
    for alias, refs in portraits["aliases"].items():
        all_portraits[alias] = []
        for i, n in refs:
            r = portraits["observations"][str(i)]
            assert (r["index"],r["bitmap"],r["alias"]) == (i,n,int(alias))
            assert r["grade"] == "STRICT_PIXEL_RECEIPT"
            all_portraits[alias].append(i)
            hit = candidates.get((int(alias),n,r["rd_sha256"]))
            if hit:
                assert (r["width"],r["height"],r["size"]) == (96,104,hit["size"])
                if "pixel_sha256" in hit:
                    assert hit["pixel_sha256"] == r["pixel_sha256"]
                available[str(i)] = dict(**hit, alias=int(alias), bitmap=n, later_adrn_index=i, rd_sha256=r["rd_sha256"],
                                         later_index_pixel_sha256=r["pixel_sha256"])
    assert len(available) == 128

    # All original group candidates with the identical complete SPR segment,
    # not merely the same graphic integer or name.
    by_key = defaultdict(list)
    for i, g in late["groups"].items():
        if g["status"] != "NO_POSITIVE_PET_LINK_IN_COMPARED_SOURCES":
            by_key[(g["graphic"],g["spr_sha256"])].append(int(i))
    src_groups = {}
    dst_groups = {}
    links = []
    for p in early["profiles"]:
        i, graphic, sha = p["source_spr_group_index"],p["source_graphic_number"],p["original_sprite_segment_sha256"]
        for j in by_key[(graphic,sha)]:
            sg = dict(graphic=graphic,animation_headers=p["original_source_animation_sequences"])
            assert src_groups.setdefault(i,sg) == sg
            assert dst_groups.setdefault(j,sg) == sg
            links.append((p,i,j))
    assert links
    # The original ordered headers and frame descriptors must agree as well.
    es = sequence_tables(src_groups, EXTRA["tw10_animations"][0], EXTRA["tw10_frames"][0])
    ls = sequence_tables(dst_groups, EXTRA["tw85_animation"][0], PINS["frames"][0])
    want = {f[0] for x in es.values() for a in x.values() for f in a["frames"] if f[0] is not None}
    early_rd = select_rd(gzrows(EXTRA["tw10_adrn"][0]),want,"rd_block_sha256")
    late_rd = select_rd(gzrows(PINS["native"][0]),want,"rd_sha256")
    excluded = set(motion["bounded_bitmaps"]) | set(motion["unrendered_bitmaps"])
    good = {n for n in want if n not in excluded and n in early_rd and early_rd[n] == late_rd.get(n)}
    available_motion = {}
    for p,i,j in links:
        assert es[i] == ls[j], (i,j)
        sequences = []
        for k,s in es[i].items():
            # An actual private full sequence requires every frame, including
            # the exact original offsets/sound words, with strict RD matches.
            if not s["frames"] or any(f[0] not in good for f in s["frames"]):
                continue
            sequences.append(dict(index=k,direction=s["direction"],action=s["action"],duration=s["duration"],
                                  frame_count=s["count"],descriptor_sha256=digest(s["frames"])))
        assert str(j) not in available_motion
        available_motion[str(j)] = dict(early_pet_id=p["pet_id"],early_group_index=i,later_group_index=j,
                                        graphic=p["source_graphic_number"],spr_sha256=p["original_sprite_segment_sha256"],
                                        all_source_sequences=len(es[i]),exact_sequences=sequences,
                                        source="TW10_PREVIEW_EXACT_TW85_SPR_AND_STRICT_RD_NOT_OFFICIAL_IDENTITY")
    summary = dict(
        original_early_profiles=len(early["profiles"]),later_portrait_aliases=len(all_portraits),
        later_portrait_physical_rows=sum(map(len,all_portraits.values())),exact_reusable_portrait_rows=len(available),
        exact_spr_group_candidates=len(available_motion),
        groups_with_any_exact_sequence=sum(bool(r["exact_sequences"]) for r in available_motion.values()),
        groups_with_all_exact_sequences=sum(len(r["exact_sequences"])==r["all_source_sequences"] for r in available_motion.values()),
        exact_sequence_occurrences=sum(len(r["exact_sequences"]) for r in available_motion.values()),
        exact_frame_occurrences=sum(s["frame_count"] for r in available_motion.values() for s in r["exact_sequences"]),
        distinct_strict_exact_motion_bitmaps=len(good),official_species_count=None,
        original_assets_published=False,original_runtime_verified=False)
    return dict(schema="stoneage.pet.atlas_r3.cross_version_exact_visual_reuse.r1",summary=summary,
                input_git_blobs={str(p.relative_to(ROOT)):h for p,h in PINS_R3.values()},
                portrait_rows_by_alias=all_portraits,available_portraits=available,available_motion=available_motion)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    d=build()
    a.output.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    print("PET_ATLAS_R3_SUMMARY="+json.dumps(d["summary"],sort_keys=True))
if __name__=="__main__":
    main()
