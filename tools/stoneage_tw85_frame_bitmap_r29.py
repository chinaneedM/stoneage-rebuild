"""R29: whole-corpus source-qualified TW85 SPR frame to SAME-PACKAGE ADRN/REAL join.

Consume only immutable original-byte-derived metadata from the same preserved
community carrier. Keep physical positions, all repeated IDs, sentinels and
missing mappings. This is NOT an identified pet, actual rendered pixels,
authenticated clean official build, scene selector, or original client run.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_resource_metadata import DeterministicGzipTsv

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"research/recovered"
R28=BASE/"tw85-spr137-r28"
R06=BASE/"adrn129-tw85-real-pair"
INPUTS={
 "R28_GROUP":(R28/"SPR-GROUP-R28.tsv.gz","bba57495fb4df36bd41e967033e799ea021cde3c7d11e982c50a1fdd5f9b1c18"),
 "R28_FRAME":(R28/"SPR-FRAME-R28.tsv.gz","d5e026801e743fed481847fe69da4a235c14d8019d3824d64182bc2821645142"),
 "R28_SOURCE":(R28/"SOURCE-DERIVED-R28.json","1726d1220102532d6c4bfa59ea36a6048c0623a2838394338bff5496de504af9"),
 "R06_NATIVE":(R06/"NATIVE-R1.tsv.gz","495928a0a44d7c81bf1d6ef7b06d26decfc5096803fbd60b9e8e0aa9752a45ce"),
 "R06_REPORT":(R06/"REPORT-R1.json",None),
 "CARRIER":(BASE/"STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json","4ea7b43a7e3427ab4443afe801ae7d3e156e6193e1d42ce1b261f733e07de1d8")
}
PROVENANCE="UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_TW85_SAME_INSTALLER_CARRIER"
FIELDS=("bitmapno","occurrences","native_candidates","native_indices","complete_rd_content_keys","sizes","widths","heights","qualification")
GROUP_FIELDS=("group_index","spr_no","source_scope","frame_occurrences","sentinel_frames","mapped_frames","missing_frames","single_frames","multiple_same_rd_frames","multiple_different_rd_frames","distinct_bitmap_ids","missing_bitmap_ids","distinct_mapped_rd_contents","raw_sound_word_occurrences")


def need(x,message):
    if not x:raise ValueError(message)


def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()


def rows(path):
    with gzip.open(path,"rt",encoding="utf-8",newline="") as f:
        yield from csv.DictReader(f,delimiter="\t")


def verify_inputs():
    pins={}
    for label,(path,want) in INPUTS.items():
        need(path.is_file(),"missing permanent source: "+label)
        actual=digest(path)
        if want:need(actual==want,"source bytes drift: "+label)
        pins[label]={"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":actual}
    carrier=json.loads(INPUTS["CARRIER"][0].read_bytes())
    r28=json.loads(INPUTS["R28_SOURCE"][0].read_bytes())
    native=json.loads(INPUTS["R06_REPORT"][0].read_bytes())
    need(r28["source"]=="TW85-INSTALLER-MSI-CLIENT_UNVERIFIED_COMMUNITY_PRESERVED"
         and native["schema"]=="stoneage.adrn129_tw85_real_pair.r1","source domain promoted")
    need(native["source_pins"][pins["CARRIER"]["path"]]["sha256"]==pins["CARRIER"]["sha256"],
         "native index source not the same saved client carrier")
    need(r28["source_inventory"]==pins["CARRIER"]["path"],
         "R28 pair not from identical claimed client sample")
    inventory=carrier["inspection"]["inventory"]["samples"][0]
    need(inventory["sample_id"]=="TW85-INSTALLER-MSI-CLIENT" and inventory["file_count"]==557,
         "sample ID or file inventory changed")
    files=inventory["files"]
    for name,old in {
      "spradrn_137.bin":r28["pair"]["spradrn_137.bin"],
      "spr_137.bin":r28["pair"]["spr_137.bin"],
      "adrn_158.bin":native["containers"]["adrn"],
      "real_158.bin":native["containers"]["real"]
    }.items():
        actual=[x for x in files if x["path"].endswith("/data/"+name)]
        need(len(actual)==1 and actual[0]["size"]==old["bytes"] and actual[0]["sha256"]==old["sha256"],
             "same preserved 557-file carrier member differs: "+name)
    need(native["tables"]["NATIVE-R1.tsv.gz"]["sha256"]==pins["R06_NATIVE"]["sha256"],
         "native REAL RD-verified table was not source qualified")
    need(r28["parsed"]["groups"]==1739 and r28["parsed"]["frames"]==735666,
         "R28 source bounds changed")
    return pins,r28,native


def rd_status(row,real_extent):
    """Use the already-audited strict original RD header and bounded flag0 exception."""
    off,size,w,h=int(row["adder"]),int(row["size"]),int(row["width"]),int(row["height"])
    if size<16 or off<0 or off+size>real_extent or row["rd_status"] not in ("HEADER_MATCH","HEADER_MISMATCH"):
        return "INVALID"
    if (w,h)!=(int(row["rd_width"]),int(row["rd_height"])):return "INVALID"
    if int(row["rd_size"])==size:return "VALID_HEADER"
    if int(row["rd_flag"])==0 and w>0 and h>0 and size==16+w*h:
        return "VALID_FLAG0_ADRN_SIZE"
    return "INVALID"


def classification(candidates):
    if not candidates:return "MISSING_SAME_SAMPLE_ADRN_ID"
    if len(candidates)==1:return "SINGLE_ORIGINAL_RD_RECORD"
    unique={(x["size"],x["rd_sha256"]) for x in candidates}
    return ("MULTIPLE_SAME_COMPLETE_RD" if len(unique)==1 else "MULTIPLE_DIFFERENT_COMPLETE_RD")


def build(out):
    out=Path(out)
    need(not (out==ROOT or ROOT in out.resolve().parents) or
         "research/recovered" not in str(out.resolve().relative_to(ROOT)),"only output temporary derivations before acceptance")
    out.mkdir(parents=True,exist_ok=True)
    pins,r28,report=verify_inputs()
    native_index=defaultdict(list);seen_native=Counter();source_qualification=Counter()
    extent=report["containers"]["real"]["bytes"]
    for pos,r in enumerate(rows(INPUTS["R06_NATIVE"][0])):
        need(int(r["index"])==pos,"original native ADRN physical sequence changed")
        status=rd_status(r,extent)
        need(status!="INVALID","unqualified original RD structure:"+str(pos))
        source_qualification[status]+=1
        bitmap=int(r["bitmapno"])
        seen_native[bitmap]+=1
        native_index[bitmap].append({
          "index":pos,"size":int(r["size"]),"width":int(r["width"]),
          "height":int(r["height"]),"rd_sha256":r["rd_sha256"],
          "record_sha256":r["record_sha256"],"source_qualification":status
        })
    need(sum(seen_native.values())==416220 and len(seen_native)==416192,
         "complete native original ADRN count changed")
    groups=list(rows(INPUTS["R28_GROUP"][0]))
    need(len(groups)==1739 and [int(g["index"]) for g in groups]==list(range(1739)),
         "R28 group physical index drift")
    exact_r28=set()
    for relationship in r28["joins"]["reference_relationships"]["CN50"]:
        need(relationship["relation"]=="SAME_ID_AND_EXACT_FULL_SPR_SEGMENT",
             "old CN5 source confidence changed")
        exact_r28.add(int(relationship["tw85_index"]))
    need(len(exact_r28)==1185,"R28 CN5 source overlap changed")
    by_id=Counter();group_stats=[]
    total=Counter();sources=Counter();mappings=Counter()
    bitmap_groups=defaultdict(set);sample_unknown=[]
    last_group=-1
    g=None;bits=set();missing_bits=set();rd_bits=set();row_stats=None
    def finish_group():
        if row_stats is not None:
            row_stats["distinct_bitmap_ids"]=len(bits)
            row_stats["missing_bitmap_ids"]=len(missing_bits)
            row_stats["distinct_mapped_rd_contents"]=len(rd_bits)
            need(row_stats["frame_occurrences"]==row_stats["sentinel_frames"]+
                 row_stats["mapped_frames"]+row_stats["missing_frames"],"group frame conservation broken")
            group_stats.append(row_stats.copy())
    for f in rows(INPUTS["R28_FRAME"][0]):
        idx=int(f["group_index"])
        need(0<=idx<len(groups) and idx>=last_group,"original frame group order mutated")
        if idx!=last_group:
            finish_group()
            need(idx==last_group+1,"empty/omitted frame group requires explicit source review")
            g=groups[idx];bits=set();missing_bits=set();rd_bits=set()
            row_stats={k:0 for k in GROUP_FIELDS if k not in ("group_index","spr_no","source_scope")}
            row_stats.update({"group_index":idx,"spr_no":int(g["spr_no"]),
                "source_scope":"EXACT_CN50_SPR_SEGMENT" if idx in exact_r28 else "R28_UNMATCHED_CN50_SPR_SEGMENT"})
            sources[row_stats["source_scope"]]+=1
            last_group=idx
        need(f["spr_no"]==g["spr_no"],"frame source ID changed")
        row_stats["frame_occurrences"]+=1;total["frames"]+=1
        if int(f["sound_no"])!=0:row_stats["raw_sound_word_occurrences"]+=1
        bitmap=int(f["bmp_no"]);flag=int(f["sentinel"])
        need(flag==int(bitmap==0xffffffff),"sentinel normalization drift")
        if flag:
            row_stats["sentinel_frames"]+=1;total["sentinel_frames"]+=1
            continue
        bits.add(bitmap);by_id[bitmap]+=1;bitmap_groups[bitmap].add(idx)
        candidates=native_index.get(bitmap,[])
        kind=classification(candidates)
        mappings[kind]+=1
        if not candidates:
            row_stats["missing_frames"]+=1
            missing_bits.add(bitmap)
            if len(sample_unknown)<30:sample_unknown.append({"index":idx,"spr_no":int(g["spr_no"]),
                                                           "bmp_no":bitmap,"frame_offset":int(f["offset"])})
        else:
            row_stats["mapped_frames"]+=1
            row_stats["single_frames"]+=int(len(candidates)==1)
            row_stats["multiple_same_rd_frames"]+=int(kind=="MULTIPLE_SAME_COMPLETE_RD")
            row_stats["multiple_different_rd_frames"]+=int(kind=="MULTIPLE_DIFFERENT_COMPLETE_RD")
            for c in candidates:rd_bits.add((c["size"],c["rd_sha256"]))
    finish_group()
    need(len(group_stats)==1739 and total["frames"]==735666 and total["sentinel_frames"]==4759,
         "R28 full frame source conservation failed")
    need(sum(by_id.values())==total["frames"]-total["sentinel_frames"],
         "mapped+missing nonsentinel row conservation failed")
    need(sum(mappings.values())==sum(by_id.values()),"classification conservation failed")
    need(sources["R28_UNMATCHED_CN50_SPR_SEGMENT"]==554,"unmatched group category drift")
    need(all(row["group_index"]==index and row["spr_no"]==int(groups[index]["spr_no"])
             for index,row in enumerate(group_stats)),
         "per-group original identity/order drift")
    links=out/"BITMAP-BINDINGS-R29.tsv.gz"
    with DeterministicGzipTsv(links) as stream:
        stream.write("\t".join(FIELDS)+"\n")
        for number in sorted(by_id):
            cc=native_index.get(number,[])
            values={
              "bitmapno":number,"occurrences":by_id[number],"native_candidates":len(cc),
              "native_indices":",".join(str(x["index"]) for x in cc),
              "complete_rd_content_keys":",".join(str(x["size"])+":"+x["rd_sha256"] for x in cc),
              "sizes":",".join(str(x["size"]) for x in cc),
              "widths":",".join(str(x["width"]) for x in cc),
              "heights":",".join(str(x["height"]) for x in cc),
              "qualification":classification(cc)
            }
            stream.write("\t".join(str(values[k]) for k in FIELDS)+"\n")
    group_output=out/"GROUP-MATERIAL-R29.tsv.gz"
    with DeterministicGzipTsv(group_output) as stream:
        stream.write("\t".join(GROUP_FIELDS)+"\n")
        for row in group_stats:
            stream.write("\t".join(str(row[k]) for k in GROUP_FIELDS)+"\n")
    buckets={}
    for scope in ("EXACT_CN50_SPR_SEGMENT","R28_UNMATCHED_CN50_SPR_SEGMENT"):
        selected=[g for g in group_stats if g["source_scope"]==scope]
        buckets[scope]={"groups":len(selected),
          **{key:sum(g[key] for g in selected) for key in GROUP_FIELDS
             if key not in ("group_index","spr_no","source_scope","distinct_bitmap_ids","missing_bitmap_ids","distinct_mapped_rd_contents")},
          "group_distinct_bitmap_sum_not_global_unique":sum(g["distinct_bitmap_ids"] for g in selected),
          "groups_with_missing_ids":sum(g["missing_bitmap_ids"]>0 for g in selected)}
    summary={
       "schema":"stoneage.tw85_frame_to_bitmap_same_saved_carrier.r29",
       "source_pins":pins,"source_grade":PROVENANCE,
       "original_paired_members":["spradrn_137.bin","spr_137.bin","adrn_158.bin","real_158.bin"],
       "native_records":416220,"native_unique_ids":416192,
       "native_multiple_number_extra_occurrences":sum(n-1 for n in seen_native.values()),
       "source_structural_qualification":dict(sorted(source_qualification.items())),
       "original_frame_occurrences":total["frames"],
       "original_sentinel_frame_occurrences":total["sentinel_frames"],
       "frame_mapping_classifications":dict(sorted(mappings.items())),
       "distinct_referenced_bitmap_ids":len(by_id),
       "referenced_number_classes":dict(sorted(Counter(classification(native_index.get(n,[])) for n in by_id).items())),
       "original_group_occurrences":len(groups),
       "scope_buckets":buckets,"sample_missing_positions":sample_unknown,
       "tables":{path.name:{"bytes":path.stat().st_size,"sha256":digest(path)}
                 for path in (links,group_output)},
       "boundaries":{
         "same_saved_carrier_verified_against_full_file_inventory":True,
         "all_frames_joined_without_collapsing_duplicate_positions":True,
         "source_original_RD_headers_and_block_SHA_verified_in_prior_source_run":True,
         "actual_RD_pixels_reacquired_or_rendered_this_run":False,
         "named_pet_avatar_npc_or_action_identified":False,
         "clean_official_pressing_authenticated":False,
         "unmatched_R28_group_count_equates_to_new_species":False,
         "missing_id_equates_to_no_image_in_all_versions":False,
         "duplicate_bitmapno_runtime_winner_identified":False,
         "original_client_executed":False,
         "new_original_package_bytes_downloaded":False,
         "original_proprietary_asset_bytes_published":0,
         "overall_completion_percent":None,"stage_a":"7_PARTIAL_2_OPEN",
         "stage_b_wiki":"GATED","r79":"PAUSED_NON_BLOCKING"
       },
       "next":"REVIEW_R29_BOUND_MISSING_FRAME_IDS_AND_RESOLVE_ONLY_MATERIAL_GAME_VISIBLE_GAP_30"
    }
    (out/"REPORT-R29.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    return summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=build(a.out)
    print(json.dumps({"status":"PASS","frames":result["original_frame_occurrences"],
                      "sentinels":result["original_sentinel_frame_occurrences"],
                      "mapping":result["frame_mapping_classifications"],
                      "scope_buckets":result["scope_buckets"]},sort_keys=True))


if __name__=="__main__":main()
