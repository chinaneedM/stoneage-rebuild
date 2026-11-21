#!/usr/bin/env python3
"""PET126R: complete source-separated original classic-PC CN50 compiled album.

Produces *derived names, typed integers, hashes and version-qualified candidate
asset joins* from source-hashed original executable plus previously authenticated
same-CAB SPR group metadata. Never executes or republishes proprietary code/art.
An ordinal or bitmap number is not an original 5.0 SPR selector or live pet ID.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from tools.stoneage_pet126l_cn50_table_graphic_probe import (
    ROOT, STRIDE, ROWS, TABLE_OFFSET, TABLE_SHA, digest, qualified_resources,
    read_gz_rows, source_rows, RESOURCE_DIR
)
from tools.stoneage_pet126m_cn50_pe_album_xrefs import (
    parse_objdump, pe32_text_identity
)
from tools.stoneage_pet126k_cn50_original_exe_probe import EXPECTED

PET39 = ROOT / "research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
PET126L = ROOT / "research/recovered/STONEAGE-PET126L-CN50-COMPILED-NAME-SAME-CAB-KEY-AUDIT-R1.json"
FIRST_TW10_GRAPHIC = 100250
# The field at +24 is the source name-table tail integer, not a certified SPR ID.
FIELDS = (0, 4, 20, 24)
GRAPHIC_LITERALS = (100250, 100430, 100431, 100611)

def instruction_exact_sites(code, candidates, cap=10):
    """Exact hexadecimal literal tokens, not substring or guessed code flow."""
    results={}
    for name, expected in candidates.items():
        hits=[]
        for i,row in enumerate(code):
            if expected in (int(token,16) for token in re.findall(r"0x[0-9a-fA-F]+",row["instruction"])):
                hits.append({"va":hex(row["address"]),
                    "instruction":row["instruction"],
                    "preceding":[x["instruction"] for x in code[max(0,i-4):i]],
                    "following":[x["instruction"] for x in code[i+1:i+5]]})
        results[name]={"exact_token_occurrences":len(hits),"bounded_first_contexts":hits[:cap],
                       "contexts_truncated":len(hits)>cap}
    return results

def album_index(raw_rows, group_rows, tw_records):
    """All 362 real named/blank positions; full names are factual metadata only."""
    if len(raw_rows)!=362:
        raise ValueError("original-album-physical-slot-count-changed")
    grp={}
    for row in group_rows:
        key=int(row["spr_no"])
        if key in grp:
            raise ValueError("original-CN50-SPR-group-key-duplicated")
        grp[key]={"index":int(row["index"]),"sha256":row["segment_sha256"]}
    if len(grp)!=1185:
        raise ValueError("same-CAB-SPR-group-total-mismatch")
    tw={int(x["graphic_number"])-FIRST_TW10_GRAPHIC:x for x in tw_records}
    if len(tw)!=124:
        raise ValueError("authenticated-retail-TW10-source-album-changed")
    out=[]
    for row in raw_rows:
        ordinal=int(row["ordinal"])
        name=row["name"]
        filled=row["raw_i32"]!=-1
        number=FIRST_TW10_GRAPHIC+ordinal
        sprite=grp.get(number)
        prior=tw.get(ordinal)
        exact=bool(prior and sprite and sprite["sha256"]==prior["spr_original_segment_sha256"])
        out.append({
          "record_key":"CN50_CLIENT_COMPILED_ALBUM_SLOT:"+str(ordinal),
          "carrier":"CN50_THIRD_PARTY_PRESERVED_PC_5_0_CAB",
          "ordinal":ordinal,
          "source_exe_row_offset":TABLE_OFFSET+ordinal*STRIDE,
          "source_exe_row_sha256":digest(row["raw_record"]),  # no original bytes retained
          "label_as_compiled_GB18030":name if filled else None,
          "source_raw_first_i32":row["raw_i32"],
          "source_raw_trailing_u32":row["raw_u32"],
          "source_kind":"COMPILED_LOCAL_PET_ALBUM_NAME" if filled else "COMPILED_ALBUM_EMPTY_SLOT",
          "TW10_ordinal_based_graphic_hypothesis":number,
          "same_CAB_SPR_group_for_hypothesis_present":bool(sprite),
          "same_CAB_SPR_group_hash_for_hypothesis":sprite["sha256"] if sprite else None,
          "TW10_retail_ordinal_is_named":bool(prior),
          "TW10_retail_exact_same_SPR_segment_at_this_ordinal":exact if prior else None,
          "CN50_name_to_SPR_native_selector_proven":False,
          "original_official_live_pet_release_proven":False,
          "original_server_species_identifier":None,
          "source_graded_candidate_only":True
        })
    return out

def inspect(path:Path):
    original=path.read_bytes()
    if (len(original),hashlib.sha256(original).hexdigest())!=EXPECTED["sa_5000.exe"]:
        raise ValueError("original-classic-PC-source-EXE-SHA-mismatch")
    rows=source_rows(original)
    previous=json.loads(PET126L.read_text("utf-8"))
    if previous["original_table_sha256"]!=TABLE_SHA or previous["original_program_sha256"]!=EXPECTED["sa_5000.exe"][1]:
        raise ValueError("prior-same-carrier-source-chain-broken")
    manifest=qualified_resources()
    tw=json.loads(PET39.read_text("utf-8"))
    if tw["archive"]["sha256"]!="3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24":
        raise ValueError("authenticated-retail-TW10-source-changed")
    original_group_rows=list(read_gz_rows(RESOURCE_DIR/"SPR-GROUP-R1.tsv.gz"))
    if len(original_group_rows)!=manifest["metrics"]["spr"]["groups"]:
        raise ValueError("original-same-CAB-SPR-key-count-changed")
    # Raw 28B hashed in RAM only, not published to the repository.
    for row in rows:
        off=TABLE_OFFSET+row["ordinal"]*STRIDE
        row["raw_record"]=original[off:off+STRIDE]
    entries=album_index(rows,original_group_rows,tw["records"])
    for row in rows:
        del row["raw_record"]

    imagebase,text=pe32_text_identity(original)
    # This source table is mapped to the original file-backed PE .data section.
    from tools.stoneage_pet126l_cn50_table_graphic_probe import exact_pointer_literals
    xref=exact_pointer_literals(original,TABLE_OFFSET)
    if [z["file_offset"] for z in xref["literal_va_locations"]] != [199700,200343,214772]:
        raise ValueError("known-three-native-name-references-changed")
    tableva=imagebase+xref["table_rva"]
    dis=subprocess.run(["objdump","-d","-M","intel","-j",".text",str(path)],
        capture_output=True,text=True,timeout=90)
    if dis.returncode:
        raise ValueError("original-binary-static-disassembly-failed")
    code=parse_objdump(dis.stdout)
    if len(code)!=131461:
        raise ValueError("original-compiled-text-decoding-changed")
    candidates={
      "table_start_va":tableva,
      **{"table_start_plus_"+str(delta):tableva+delta for delta in FIELDS if delta},
      **{"possible_TW10_graphic_literal_"+str(no):no for no in GRAPHIC_LITERALS}
    }
    sites=instruction_exact_sites(code,candidates)
    if sites["table_start_va"]["exact_token_occurrences"]<3:
        raise ValueError("original-name-table-three-source-references-missing")
    filled=[x for x in entries if x["label_as_compiled_GB18030"] is not None]
    blanks=[x for x in entries if x["label_as_compiled_GB18030"] is None]
    prior_n=[x for x in filled if x["TW10_retail_ordinal_is_named"]]
    result={
      "schema":"stoneage.pet126r.cn50_pc_original_compiled_album_source_separated_names_and_candidate_art.r1",
      "date":"2026-11-21",
      "active_module":"PET",
      "scope":"ORIGINAL_CLASSIC_PC_ONLY",
      "source":{
        "original_exe_name":"sa_5000.exe","original_exe_sha256":hashlib.sha256(original).hexdigest(),
        "original_exe_bytes":len(original),
        "original_compiled_table_sha256":TABLE_SHA,
        "source_cab_sha256":manifest["source"]["cab_sha256"],
        "carrier_grade":"THIRD_PARTY_PRESERVED_CN50_CLASSIC_PC_NOT_CERTIFIED_ORIGINAL_OFFICIAL_PRESSING",
        "source_original_exe_executed":False,
        "source_commercial_EXE_or_sprite_published":False,
        "same_CAB_derived_SPR_metadata_SHA_pinned":True,
        "TW10_independent_authenticated_retail_client_reference":"research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
      },
      "metrics":{
        "physical_compiled_album_slots":len(entries),
        "compiled_source_named_rows":len(filled),
        "compiled_source_empty_rows":len(blanks),
        "CN50_source_name_rows_with_hypothesis_SPR_group":sum(x["same_CAB_SPR_group_for_hypothesis_present"] for x in filled),
        "CN50_source_blank_rows_with_hypothesis_SPR_group":sum(x["same_CAB_SPR_group_for_hypothesis_present"] for x in blanks),
        "named_TW10_retail_ordinal_source_pairs":len(prior_n),
        "named_TW10_pairs_with_exact_CN50_source_sprite_hash":sum(x["TW10_retail_exact_same_SPR_segment_at_this_ordinal"] for x in prior_n),
        "CN50_full_original_SPR_groups":len(original_group_rows),
        "official_newly_released_species_proven":0,
        "historical_total_species":None
      },
      "original_source_native_table_and_graphic_literal_sites":sites,
      "source_table_original_mapping_va":hex(tableva),
      "catalogue_record_status":"CN50_CLIENT_COMPILED_ALBUM_NAME_PLUS_ORDINAL_GRAPHIC_HYPOTHESIS_ONLY",
      "records":entries,
      "negative_boundaries":{
        "TW10_ordinal_graphic_formula_applies_natively_to_CN50":False,
        "CN50_same_build_name_to_SPR_selector_proven":False,
        "CN50_same_build_alias_u32_to_portrait_runtime_proven":False,
        "source_CAB_is_independently_certified_official_pressing":False,
        "same_resource_segment_cross_version_is_same_species_or_live_release":False,
        "native_original_exe_ever_executed":False,
        "original_server_master_or_actual_obtainability_recovered":False,
        "new_official_species_count":0,
        "pet_module_closed":False,
        "2026_year_audited":False,
        "stage_a":"7_PARTIAL_2_OPEN","stage_b_wiki":"GATED","r79":"PAUSED_NON_BLOCKING",
        "overall_completion_percent":None,
        "historical_CURRENT_git_blob_preserved":"c89e0e33537990aa2132b47c40fef49a985a935c"
      },
      "next":"Pursue actual original same-build native code showing CN50 album ordinal/last U32 into sprite/portrait selector; no value on numeric-only equality; otherwise source-bound PET seven-dimension terminal review."
    }
    if (result["metrics"]["physical_compiled_album_slots"],
        result["metrics"]["compiled_source_named_rows"],
        result["metrics"]["compiled_source_empty_rows"])!=(362,305,57):
        raise ValueError("original-album-name-count-changed")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--program",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    out=inspect(args.program)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n","utf-8")
    print("PET126R_ORIGINAL_PC_SOURCE_CATALOGUE|SLOTS="+str(out["metrics"]["physical_compiled_album_slots"])+"|NAMED="+str(out["metrics"]["compiled_source_named_rows"])+"|TW10_EXACT_SPR="+str(out["metrics"]["named_TW10_pairs_with_exact_CN50_source_sprite_hash"])+"|NO_LIVE_PET_PROMOTION",flush=True)

if __name__=="__main__": main()
