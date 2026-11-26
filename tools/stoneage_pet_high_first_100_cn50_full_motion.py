"""PET100: full named CN50 action coverage and exact original RD read targets.
This is a preflight over verified metadata and retained pixel receipts, not a new extraction.
"""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
from tools.stoneage_pet_high_first_57_coverage import ROOT, blob, gzrows
from tools.stoneage_pet_high_first_66_motion_inheritance import sequence_tables
PINS = {
    "album": ("research/pets/PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json", "98fea71c051dfa887b91154a8a72d17c67b57744"),
    "manifest": ("research/recovered/cn50-resource-metadata/MANIFEST-R1.json", "5063cf2fade4e0739ac35c38a90dfff1a43db960"),
    "groups": ("research/recovered/cn50-resource-metadata/SPR-GROUP-R1.tsv.gz", "f4a41ba999167185b55a42c89ece9e24d456e637"),
    "animations": ("research/recovered/cn50-resource-metadata/SPR-ANIMATION-R1.tsv.gz", "0da62abce6aecd476ca95f6fc2a8679105d0b09d"),
    "frames": ("research/recovered/cn50-resource-metadata/SPR-FRAME-R1.tsv.gz", "6e98e5fea26a69aa5c7042bab1707c7a330c6bf7"),
    "adrn": ("research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz", "127670eaf2bc19ba9d15776d090a8307058f729d"),
    "cn_receipt": ("research/pets/PET-HIGH-FIRST-11-PC-INDEXED-PIXEL-RECEIPTS-R1.json.gz", "6ba6e7f9772c90dd1bad05f012e330f43ea41158"),
    "tw67": ("research/pets/PET-HIGH-FIRST-67-BULK-PIXELS-R1.json.gz", "1801e69665de0d67ea7d15dce5396c267bb65374"),
    "tw68": ("research/pets/PET-HIGH-FIRST-68-RD-BOUNDARY-R1.json", "3648e9b85a85cdb95b6c5207c548de8ecf177d5a"),
    "tw71": ("research/pets/PET-HIGH-FIRST-71-BULK-NAMED-PIXELS-R1.json.gz", "157cdf72e74ecb328a15e16771cb36e18735ca08"),
    "tw10_receipt": ("research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json", "e1cac6980353d09353de43fec0948bfcd84d49e6"),
    "tw10_manifest": ("research/recovered/tw10-resource-metadata/MANIFEST-R1.txt", "6154dcf806163b82cb96af344e6a644143d15f56"),
    "tw10_groups": ("research/recovered/tw10-resource-metadata/SPR-GROUP-R1.tsv.gz", "5ec65f043848fb3260bc04c94847b45fb1706d36"),
    "tw10_animations": ("research/recovered/tw10-resource-metadata/SPR-ANIMATION-R1.tsv.gz", "90b19256f465effa6a8b6964a3777f7b31e3004c"),
    "tw10_frames": ("research/recovered/tw10-resource-metadata/SPR-FRAME-R1.tsv.gz", "ec374e9ab30c54d29de453c51f30fa1fb0df1fd1"),
    "tw10_adrn": ("research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz", "e389540f9962d1868c42b1edfe2acc7c83387ff1"),
}
def path(k):
    return ROOT / PINS[k][0]
def read(k):
    raw = path(k).read_bytes()
    assert blob(raw) == PINS[k][1], k
    return raw
def obj(k):
    raw = read(k)
    return json.loads(gzip.decompress(raw) if path(k).suffix == ".gz" else raw)
def key(d, size="size", sha="rd_sha256"):
    h = d[sha]
    assert len(bytes.fromhex(h)) == 32
    return (h, int(d[size]), int(d["width"]), int(d["height"]))
STRICT = "STRICT_EXACT_RD_RECEIPT"
BOUNDED = "BOUNDED_EXACT_RD_RECEIPT"
NEED = "READ_ORIGINAL_REQUIRED"
MISSING = "NO_ADRN_RECORD"
AMBIGUOUS = "AMBIGUOUS_DIFFERENT_RD"
def classify(candidates, strict, bounded):
    if not candidates:
        return MISSING
    keys = {key(x) for x in candidates}
    if len(keys) != 1:
        return AMBIGUOUS
    k = next(iter(keys))
    return STRICT if k in strict else BOUNDED if k in bounded else NEED
def selftest():
    a = dict(rd_sha256="ab"*32,size=17,width=1,height=1)
    b = dict(a,width=2)
    assert classify([],{}, {}) == MISSING
    assert classify([a,b],{key(a):1},{}) == AMBIGUOUS
    assert classify([a,a],{key(a):1},{}) == STRICT
    assert classify([a],{},{key(a):1}) == BOUNDED
    assert classify([a],{}, {}) == NEED
def derive():
    manifest = obj("manifest")
    table = {x["name"]: x for x in manifest["tables"]}
    for k in ("groups","animations","frames","adrn"):
        raw = read(k)
        entry = table[path(k).name]
        assert (len(raw),hashlib.sha256(raw).hexdigest()) == (entry["bytes"],entry["sha256"])
    album = obj("album")["records"]
    assert len(album) == 305 and len({r["ordinal"] for r in album}) == 305
    wanted = {(g["spr_group"],g["sha256"]) for r in album for g in r["spr_groups"]}
    group_matches = defaultdict(list)
    groups = {}
    for g in gzrows(path("groups")):
        idx = int(g["index"])
        pair = (int(g["spr_no"]),g["segment_sha256"])
        if pair not in wanted:
            continue
        assert idx not in groups
        groups[idx] = dict(graphic=pair[0],sha256=pair[1],animation_headers=int(g["anim_count"]))
        group_matches[pair].append(idx)
    assert set(group_matches) == wanted
    position_groups = {r["ordinal"]: sorted({i for g in r["spr_groups"] for i in group_matches[(g["spr_group"],g["sha256"])]}) for r in album}
    seq = sequence_tables(groups,path("animations"),path("frames"))
    target = {f[0] for ss in seq.values() for a in ss.values() for f in a["frames"] if f[0] is not None}
    # Keep exact content keys; no inference from bitmap number, name or SPR hash alone.
    strict, bounded = {}, {}
    def add(pool, k, source, ref):
        other = bounded if pool is strict else strict
        assert k not in other, (source,ref,k)
        pool.setdefault(k,dict(source=source,ref=ref))
    cn = obj("cn_receipt")
    assert len(cn["cn50_observed_blocks"]) == 1536
    for n, r in cn["cn50_observed_blocks"].items():
        assert len(bytes.fromhex(r["index_pixels_sha256"])) == 32
        add(strict,key(r,"rd_bytes"),"CN50_PET11",int(n))
    r67 = obj("tw67")
    for n,r in r67["observations"].items():
        if r["status"] == "DUAL_DECODED_INDEX_PIXELS":
            assert len(bytes.fromhex(r["index_pixels_sha256"])) == 32
            add(strict,key(r),"TW85_PET67",int(n))
    del r67
    r68 = obj("tw68")
    for n,r in r68["observations"].items():
        assert len(bytes.fromhex(r["canvas_prefix_sha256"])) == 32
        add(bounded,key(r),"TW85_PET68_BOUNDED",int(n))
    del r68
    r71 = obj("tw71")
    for n,r in r71["observations"].items():
        if r["grade"] == "STRICT_PIXEL_RECEIPT":
            assert len(bytes.fromhex(r["strict"]["index_pixels_sha256"])) == 32
            add(strict,key(r),"TW85_PET71",int(n))
        elif r["grade"] == "BOUNDED_CANVAS_RECEIPT":
            assert len(bytes.fromhex(r["boundary"]["canvas_prefix_sha256"])) == 32
            add(bounded,key(r),"TW85_PET71_BOUNDED",int(n))
    del r71
    early = obj("tw10_receipt")
    early_manifest = read("tw10_manifest").decode()
    assert early["source_bitmap_statuses"] == {"strict":32150,"terminal_zero_outside_canvas":5}
    assert not early["unrendered_bitmaps"]
    for name,(size,h) in early["source_members"].items():
        if name != "Palet_1.sap":
            assert f"SOURCE|name={name}|bytes={size}|sha256={h}" in early_manifest
    for k in ("tw10_groups","tw10_animations","tw10_frames","tw10_adrn"):
        raw = read(k)
        assert f"DATASET|name={path(k).name}|bytes={len(raw)}|sha256={hashlib.sha256(raw).hexdigest()}" in early_manifest
    eg = {r["group_index"]:dict(graphic=r["graphic"],animation_headers=r["source_sequences"],sha256=r["segment_sha256"]) for r in early["groups"]}
    for g in gzrows(path("tw10_groups")):
        i = int(g["index"])
        if i in eg:
            assert (int(g["spr_no"]),int(g["anim_count"]),g["segment_sha256"]) == (eg[i]["graphic"],eg[i]["animation_headers"],eg[i]["sha256"])
    es = sequence_tables(eg,path("tw10_animations"),path("tw10_frames"))
    en = {f[0] for ss in es.values() for a in ss.values() for f in a["frames"]}
    assert None not in en and len(en) == 32155
    excluded = set(early["bounded_bitmaps"])
    assert len(excluded) == 5 and excluded <= en
    seen = set()
    early_strict = en-excluded
    for r in gzrows(path("tw10_adrn")):
        n = int(r["bitmapno"])
        if n in early_strict:
            assert n not in seen
            seen.add(n)
            add(strict,key(r,sha="rd_block_sha256"),"TW10_PET15_STRICT_SCOPE",n)
    assert seen == early_strict
    # Original CN50 bitmap numbers are unique in the pinned full resource index.
    native = defaultdict(list)
    for r in gzrows(path("adrn")):
        n = int(r["bitmapno"])
        if n not in target:
            continue
        native[n].append(dict(index=int(r["index"]),bitmap=n,offset=int(r["adder"]),size=int(r["size"]),width=int(r["width"]),height=int(r["height"]),rd_sha256=r["rd_block_sha256"],attr_sha256=r["attr_sha256"]))
    grades = {}; targets = {}; bitmap_refs = {}; source_counts = Counter()
    for n in sorted(target):
        rr = native[n]
        g = classify(rr,strict,bounded)
        grades[n] = g
        receipt = None
        if g in (STRICT,BOUNDED):
            receipt = (strict if g == STRICT else bounded)[key(rr[0])]
            source_counts[receipt["source"]] += 1
        elif g == NEED:
            for r in rr:
                targets[r["index"]] = r
        bitmap_refs[n] = dict(grade=g,native_candidates=rr,receipt=receipt)
    frame_counts = Counter(); seq_counts = Counter(); group_counts = Counter()
    group_results = {}
    for i,g in sorted(groups.items()):
        counts = Counter()
        sequences = []
        for j,a in seq[i].items():
            nums = [f[0] for f in a["frames"] if f[0] is not None]
            c = Counter(grades[n] for n in nums)
            counts.update(c); frame_counts.update(c)
            state = "SENTINEL_ONLY" if not nums else "INCOMPLETE" if any(k not in (STRICT,BOUNDED) for k in c) else "BOUNDED_COMPLETE" if c[BOUNDED] else "STRICT_COMPLETE"
            seq_counts[state] += 1
            sequences.append(dict(animation=j,direction=a["direction"],action=a["action"],duration=a["duration"],grade=state,frame_grades=dict(c),unresolved_bitmaps=sorted({n for n in nums if grades[n] not in (STRICT,BOUNDED)})))
        states = [r["grade"] for r in sequences if r["grade"] != "SENTINEL_ONLY"]
        state = "NO_NONEMPTY_SEQUENCES" if not states else "INCOMPLETE" if "INCOMPLETE" in states else "BOUNDED_COMPLETE" if "BOUNDED_COMPLETE" in states else "STRICT_COMPLETE"
        group_counts[state] += 1
        group_results[i] = dict(**g,grade=state,frame_grades=dict(counts),sequences=sequences)
    position_counts = Counter(); positions = []
    for a in album:
        ids = position_groups[a["ordinal"]]
        states = [group_results[i]["grade"] for i in ids]
        state = "NO_LINKED_SOURCE_GROUP" if not ids else "ALL_STRICT" if all(x=="STRICT_COMPLETE" for x in states) else "ALL_CANVAS_COMPLETE" if all(x in ("STRICT_COMPLETE","BOUNDED_COMPLETE") for x in states) else "SOURCE_GAPS_REMAIN"
        position_counts[state] += 1
        positions.append(dict(ordinal=a["ordinal"],name=a["compiled_name"],row_sha256=a["exe_row_sha256"],group_indices=ids,grade=state))
    assert sum(position_counts.values()) == 305
    assert sum(seq_counts.values()) == sum(g["animation_headers"] for g in groups.values())
    assert sum(frame_counts.values()) == sum(1 for ss in seq.values() for a in ss.values() for f in a["frames"] if f[0] is not None)
    assert sum(Counter(grades.values()).values()) == len(target)
    summary = dict(positions=305,physical_groups=len(groups),distinct_bitmaps=len(target),bitmap_grade=dict(Counter(grades.values())),
        frame_grade=dict(frame_counts),sequence_grade=dict(seq_counts),group_grade=dict(group_counts),position_grade=dict(position_counts),
        exact_receipt_sources=dict(source_counts),read_target_native_rows=len(targets),read_target_distinct_rd_keys=len({key(r) for r in targets.values()}),
        official_species_count=None,official_closures=0,new_original_bytes=0,original_runtime_verified=False)
    return dict(schema="stoneage.pet100.cn50.full_motion_preflight.r1",summary=summary,
        source_pins={p:h for p,h in PINS.values()},source_manifest=manifest["source"],positions=positions,groups=group_results,
        bitmap_refs=bitmap_refs,read_targets=targets,original_assets_published=False,
        limitations=["Named physical groups only; no same-deployment identity proof.","Selected prior exact RD receipts are a conservative reuse pool, not exhaustive.","Unresolved targets require exact original bytes; no pixel or runtime claim.","Strict and bounded receipt classes cannot be merged."])
def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path);p.add_argument("--selftest",action="store_true")
    a = p.parse_args()
    selftest()
    if a.selftest:
        return
    r = derive()
    if a.output:
        a.output.write_bytes(gzip.compress((json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode(),compresslevel=6,mtime=0))
    print("PET100_SUMMARY="+json.dumps(r["summary"],sort_keys=True,separators=(",",":")),flush=True)
if __name__ == "__main__":
    main()
