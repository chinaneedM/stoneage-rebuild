"""R28 independent, complete bounded replay of the derived native SPR137 archive.

No proprietary source payload required. Reconstruct all SPR bytes in *streaming
hashes* from numeric decoded records, enforce exact physical coverage, replay
TW1/CN5 reference joins and verify source/ACTIONS provenance scope.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import struct

from tools.stoneage_tw85_spr137_material_r28 import (
    ORIGINALS, REFERENCES, REFERENCE_SHA256, compare, pinned_reference_groups,
    sha_file, require,
)

SOURCE_NAMES = ("GROUP", "ANIMATION", "FRAME")
SIZES = {"GROUP": 90388, "ANIMATION": 1007113, "FRAME": 5262729}
SHAS = {
    "GROUP": "bba57495fb4df36bd41e967033e799ea021cde3c7d11e982c50a1fdd5f9b1c18",
    "ANIMATION": "46aeb0628a2d7a66bf52644dfc80b1c063b4b32dcb1894a31bd2268c136eb86e",
    "FRAME": "d5e026801e743fed481847fe69da4a235c14d8019d3824d64182bc2821645142",
}
SOURCE_REPORT_SIZE = 284271
SOURCE_REPORT_SHA = "1726d1220102532d6c4bfa59ea36a6048c0623a2838394338bff5496de504af9"
RUN = 40321448446
JOB = 121567221678
ARTIFACT = 12648799786
ZIP_SHA = "6123e489e7fefa4a8914a7973ba37f103285289ad20e12c80f4985b4202853b8"


def rows(path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f, delimiter="\t")


def archive(directory):
    d = Path(directory)
    report_path = d / "SOURCE-DERIVED-R28.json"
    require(report_path.stat().st_size == SOURCE_REPORT_SIZE
            and sha_file(report_path) == SOURCE_REPORT_SHA,
            "source JSON differs from independently verified original artifact")
    r = json.loads(report_path.read_text(encoding="utf-8"))
    require(r["schema"] == "stoneage.tw85_original_spr137_material.r28"
            and r["source"] == "TW85-INSTALLER-MSI-CLIENT_UNVERIFIED_COMMUNITY_PRESERVED",
            "unqualified source grade")
    require(r["pair"] == {k: {"bytes": v[0], "sha256": v[1]} for k,v in ORIGINALS.items()},
            "pair source hash or size changed")
    for name in SOURCE_NAMES:
        path = d / ("SPR-" + name + "-R28.tsv.gz")
        require(path.stat().st_size == SIZES[name] and sha_file(path) == SHAS[name],
                "derived source bytes changed: " + name)
        require(r["outputs"][name] == {"bytes":SIZES[name],"sha256":SHAS[name]},
                "derived source manifest changed: " + name)
    gs = list(rows(d / "SPR-GROUP-R28.tsv.gz"))
    ai = iter(rows(d / "SPR-ANIMATION-R28.tsv.gz"))
    fi = iter(rows(d / "SPR-FRAME-R28.tsv.gz"))
    physical = []
    count_animations = count_frames = sentinel = 0
    group_keys = Counter()
    for index,g in enumerate(gs):
        require(int(g["index"]) == index, "original group order changed")
        group_keys[int(g["spr_no"])] += 1
        cursor = int(g["offset"])
        hasher = hashlib.sha256()
        for animation_index in range(int(g["anim_count"])):
            a = next(ai)
            require((int(a["group_index"]),a["spr_no"],int(a["anim_index"]),int(a["offset"]))
                    == (index,g["spr_no"],animation_index,cursor),
                    "animation source index, original order or offset drift")
            hasher.update(struct.pack("<HHII",int(a["direction"]),int(a["anim_no"]),
                                      int(a["duration"]),int(a["frame_count"])))
            cursor += 12
            count_animations += 1
            for frame_index in range(int(a["frame_count"])):
                f = next(fi)
                require((int(f["group_index"]),f["spr_no"],int(f["anim_index"]),
                         int(f["frame_index"]),int(f["offset"]))
                        == (index,g["spr_no"],animation_index,frame_index,cursor),
                        "frame/source order and physical position drift")
                bitmap = int(f["bmp_no"])
                flag = int(bitmap == 0xffffffff)
                require(int(f["sentinel"]) == flag, "bitmap sentinel flag promoted")
                hasher.update(struct.pack("<IhhH",bitmap,int(f["pos_x"]),
                                          int(f["pos_y"]),int(f["sound_no"])))
                cursor += 10
                count_frames += 1
                sentinel += flag
            require(cursor == int(a["end_offset"]), "truncated animation extent")
        require(cursor == int(g["end_offset"]) == int(g["next_offset"]),
                "unparsed source bytes or group extent discrepancy")
        require(hasher.hexdigest() == g["segment_sha256"],
                "full indexed SPR segment hash drift")
        physical.append((int(g["offset"]),cursor))
    require(next(ai,None) is None and next(fi,None) is None,
            "unconsumed animation or frame source records")
    physical.sort()
    require(physical[0][0] == 0 and physical[-1][1] == ORIGINALS["spr_137.bin"][0]
            and all(a[1] == b[0] for a,b in zip(physical,physical[1:])),
            "original indexed physical spans not exactly conserved")
    require((len(gs),count_animations,count_frames,sentinel) == (1739,113737,735666,4759),
            "full source row/sentinel counts changed")
    require(r["parsed"] == {
        "groups":1739,"animations":113737,"frames":735666,"sentinel_frames":4759,
        "exact_group_spans":1739,"spr_bytes":8721504,
        "nonmonotonic_index_offset_transitions":1,
        "physical_offset_order_distinct_from_record_order":True,
    }, "original parse evidence changed")
    require(r["joins"] == compare(gs,pinned_reference_groups()),
            "full same-ID segment link changed relative to pinned TW1/CN5 tables")
    rel = r["joins"]["reference_relationships"]
    occurrences = {key: {int(x["tw85_index"]) for x in values} for key,values in rel.items()}
    require((len(occurrences["TW10"]),len(occurrences["CN50"]),
             len(occurrences["TW10"] & occurrences["CN50"])) == (464,1185,464),
            "historical source subset relationships changed")
    require(all(x["relation"] == "SAME_ID_AND_EXACT_FULL_SPR_SEGMENT"
                for values in rel.values() for x in values),
            "same numeric ID incorrectly treated as unchanged bytes")
    duplicates = {str(k):v for k,v in group_keys.items() if v>1}
    require(duplicates == {"101866":3,"101990":2,"101991":2},
            "original repeated numeric keys lost")
    limits = r["limitations"]
    require(all(limits[key] is False for key in (
        "publisher_clean_build_verified","original_program_executed",
        "server_species_or_npc_identified",
        "source_bitmap_rd_payloads_available_in_this_pair",
        "original_rendered_pixels_available_in_this_pair",
        "fps_or_gameplay_action_meaning_proven",
        "original_payload_files_in_public_artifact",
        "cross_version_same_deployed_build_proven")),
        "source evidence boundary promoted")
    require(limits["restoration_percent"] is None
            and limits["stage_a"] == "7_PARTIAL_2_OPEN"
            and limits["stage_b_wiki"] == "GATED"
            and limits["r79"] == "PAUSED_NON_BLOCKING",
            "project phase promoted by native archive")
    return {
        "schema":"stoneage.tw85_spr137_independent_archive_r28",
        "status":"PASS",
        "original_pair_sha256_verified_at_source":{k:v[1] for k,v in ORIGINALS.items()},
        "source_run":RUN,"source_job":JOB,"artifact_id":ARTIFACT,
        "artifact_zip_sha256_independently_checked":ZIP_SHA,
        "source_head":"8d82dd9093e8399595fadbdc960664222ea0290d",
        "derived":{name:{"bytes":SIZES[name],"sha256":SHAS[name]} for name in SOURCE_NAMES},
        "json":{"bytes":SOURCE_REPORT_SIZE,"sha256":SOURCE_REPORT_SHA},
        "complete_spr_bytes_reencoded_as_streaming_segment_hashes":True,
        "complete_physical_range_conserved":True,
        "groups":len(gs),"animations":count_animations,"frames":count_frames,
        "sentinel_frames":sentinel,"exact_tw10_group_rows":len(occurrences["TW10"]),
        "exact_cn50_group_rows":len(occurrences["CN50"]),
        "tw10_within_cn50_overlap":len(occurrences["TW10"] & occurrences["CN50"]),
        "not_exactly_present_in_these_two_sources":len(gs)-len(occurrences["TW10"]|occurrences["CN50"]),
        "repeated_numeric_keys":duplicates,
        "same_build_or_species_identity_verified":False,
        "original_assets_or_audio_in_git":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dir",type=Path,required=True)
    p.add_argument("--receipt",type=Path)
    a=p.parse_args()
    result=archive(a.dir)
    if a.receipt:
        a.receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
