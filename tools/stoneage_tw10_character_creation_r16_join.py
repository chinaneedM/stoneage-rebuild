"""Independent bounded create-body source/selector crosswalk from archived original metadata."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOGIN="research/recovered/STONEAGE-TW10-LOGIN-AVATAR-CATALOG-R1.json"
ANIM="research/recovered/STONEAGE-TW10-ANIMATION-SELECTOR-R101.json"
BLOBS={LOGIN:"d09ff9961f677b7e0b212fbfc8c290cc04892c14",ANIM:"4623037e3ef703ae7bf81acc9a5ba35eaa587517"}

def need(x,m):
    if not x: raise ValueError(m)
def gitblob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def load():
    out={}
    for p,s in BLOBS.items():
        b=(ROOT/p).read_bytes()
        need(gitblob(b)==s,"wrong original derived Git blob "+p)
        out[p]=json.loads(b)
    return out
def index_ops(rows):
    out={}
    for row in rows:
        need(row["site_rva"] not in out,"duplicate bounded instruction")
        out[row["site_rva"]]=row
    return out
def qualify(login,anim):
    need(login["schema"]=="stoneage.tw10.login_avatar.catalog.r1", "login schema")
    need(anim["schema"]=="stoneage.tw10.animation-selector.r101","selector schema")
    need(anim["runtime"]["sha256"]=="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a","runtime lineage")
    fields=login["create_payload_fields"]
    need(len(fields)==13,"original CreateNewChar field count")
    body=next(f for f in fields if f["lineage_name"]=="body_image_id")
    face=next(f for f in fields if f["lineage_name"]=="face_image_id")
    need(body["position"]==3 and face["position"]==4,"protocol order drift")
    need(body["static_operand_source"]["address_rva"]==20934812
         and face["static_operand_source"]["address_rva"]==20936876,"sender joins differ")
    writers=login["selector_writer_inventory"]
    b=writers["lineage_body_candidate"]
    f=writers["lineage_face_candidate"]
    need(b["address_rva"]==20934812 and f["address_rva"]==20936876,"producer/consumer disagree")
    need(len(b["write_candidates"])==1 and len(f["write_candidates"])==2,"producer inventory drift")
    i=index_ops(b["write_candidates"][0]["bounded_operand_operations"])
    patterns={
      71006:("mov",["register","mem"]),71013:("mov",["register","mem"]),
      71020:("lea",["register","mem"]),71036:("add",["register","register"]),
      71038:("mov",["mem","register"])
    }
    for site,(name,types) in patterns.items():
        need(site in i and i[site]["mnemonic"]==name
            and [op["kind"] for op in i[site]["operands"]]==types,"bounded body writer pivot drift "+str(site))
    src=i[71013]["operands"][1]
    need(src["displacement"]==4558376 and src["base"] is None and src["index"]=="ecx"
         and src["scale"]==4,"source indexed table")
    dynamic=i[71006]["operands"][1]
    need(dynamic["displacement"]==24739232 and dynamic["index"]=="ecx" and dynamic["scale"]==4,"second dynamic source")
    mul=i[71020]["operands"][1]
    need(mul["base"]=="eax" and mul["index"]=="eax" and mul["scale"]==4,"factor five source")
    add=i[71036]["operands"]
    need([a["name"] for a in add]==["esi","edx"],"source accumulator")
    store=i[71038]["operands"]
    need(store[0]["displacement"]==25129116 and store[0]["base"] is None
         and store[1]["name"]=="esi","body global dest")
    need(all(not x["runtime_value_verified"] for x in (body["static_operand_source"],face["static_operand_source"])),"actual values falsely promoted")
    need(not login["runtime_resource_selection_verified"] and login["original_character_count"] is None,"identity incorrectly certified")
    need(anim["source_tables"]["SPR-GROUP-R1.tsv.gz"]["rows"]==464, "original SPR group count drift")
    return {
        "schema":"stoneage.tw10.creation_body_crosswalk.r16",
        "source_git_blobs":BLOBS,
        "executable_sha256":anim["runtime"]["sha256"],
        "create_message":{"body_field_position":3,"face_field_position":4,
                         "body_global_rva":20934812,"face_global_rva":20936876},
        "body_writer_bounded_source":{"indexed_table_va":4558376,
             "table_index_register":"ecx","index_scale":4,
             "dynamic_second_source_va":24739232,
             "syntactic_composition":"esi = dword[0x458e28 + ecx*4] + 5 * eax_pre_lea",
             "source_read_rva":71013,"source_store_rva":71038},
        "original_spr_group_count":464,
        "actual_table_length":None,"original_selector_ecx_value":None,
        "original_body_id":None,"original_face_id":None,"original_character_total":None,
        "current_proof":"STATIC_BOUNDED_SYNTAX_ONLY",
        "original_client_executed":False,"same_build_avatar_identity_certified":False,
        "later_version_character_counts_inferred":False,
    }
def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    sources=load()
    report=qualify(sources[LOGIN],sources[ANIM])
    result=json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result)
    print(result)
if __name__=="__main__":main()
