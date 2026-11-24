"""PET54 acceptance: original derived receipts, bounded static result and distinct later source."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import urllib.request
from tools.stoneage_pet_high_first_54_accept import main as preflight

ROOT=Path(__file__).resolve().parents[1]
REPORT="research/pets/PET-HIGH-FIRST-54-EGG-ROLE-AND-FUNCTION-ACCEPTED-R1.json"
def sha(b): return hashlib.sha256(b).hexdigest()
def git_blob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    preflight()
    r=json.loads((ROOT/REPORT).read_bytes())
    inputs=[]
    for p,b in r["source_pins"].items():
        data=(ROOT/p).read_bytes()
        assert git_blob(data)==b
        inputs.append(data)
    a,n,s=map(json.loads,inputs)
    assert (len(inputs[1]),sha(inputs[1]),git_blob(inputs[1]))==(427240,"254dbb336efb194a0c10e4801c0a5ea091839133e5db2c0f7af860c545ae58a1","0b0e787110e95b17d1593be7534d25c9a9d191ce")
    assert (len(inputs[2]),sha(inputs[2]),git_blob(inputs[2]))==(49994,"a846432596125251300dae90a7e2a421e17aa7ec790da381d133797bc14e4d46","937c14dc4c727c2ab6be2bf73d5620ff7dc3aa82")
    c=r["custody"]
    for k,i,run,job,art,zb,zsha in (
        ("original_scan",1,45467953788,138707808416,14956965438,55641,"bbef41bff6900b8fc3709e7352f6c404fadf0846fd82e9234eb6241defd47b72"),
        ("function_scan",2,45469473230,138713181004,14956176883,67875,"57e71fde4060a6b54d6da5793aadeff4f1dd8b888c5ca1d22d356dfb2617795d")):
        z=c[k]
        assert (z["run"],z["job"],z["artifact"],z["zip_bytes"],z["zip_sha256"])==(run,job,art,zb,zsha)
        assert (z["json_bytes"],z["json_sha256"],z["json_git_blob"])==(len(inputs[i]),sha(inputs[i]),git_blob(inputs[i]))
    assert c["zip_and_json_verified_independently"] and c["function_scan"]["prior_json_in_zip_byte_identical"]
    assert s["prior_report_git_blob"]==git_blob(inputs[1]) and s["prior_report_sha256"]==sha(inputs[1])
    assert s["prior_zip_sha256"]==c["original_scan"]["zip_sha256"]
    assert n["custody"]["unique_member_count"]==2207 and n["custody"]["member_bytes"]==2300545
    assert n["custody"]["headers_visited"]==7954 and len(n["custody"]["range_receipts"])==184 and n["custody"]["range_bytes"]==12013836
    hits=n["npc_hits"]
    assert len(hits)==765 and sum(bool(x["numeric_collisions"]) for x in hits)==33
    assert not any(x["typed_reference_candidates"] or x["ascii_term_labels"] for x in hits)
    assert Counter(t for x in hits for t in x["cp950_term_labels"])=={"合成":730,"飼料":1,"融合":1}
    q=s["probe"]
    assert q["function"]=="_NPC_EventAddEgg" and q["start_address"]==4896128 and q["next_text_symbol_address"]==4897696
    assert q["next_text_symbols"]==["_NPC_EventAddPet"] and q["body_instruction_count"]==409
    assert len(q["direct_calls_or_external_jumps"])==49
    assert [(x["containing_symbols"],x["site"]) for x in q["direct_incoming_calls_or_jumps"]]==[(["_NPC_EventAdd"],4905870),(["_NPC_AcceptDel"],4918854)]
    assert not q["target_id_immediate_candidates"] and not q["indirect_call_resolution_complete"]
    o=r["original_executable"]
    assert o["sha256"]==s["executable_sha256"]==n["exe"]["sha256"]
    assert o["body_sha256"]==q["body_disassembly_sha256"] and o["incoming"]==q["direct_incoming_calls_or_jumps"]
    assert set(o["selected_calls"]) <= {name for x in q["direct_calls_or_external_jumps"] for name in x["symbol_candidates"]}
    assert o["target_id_immediates"]==[]
    later=r["later_comparison"]
    assert (later["repo"],later["commit"],later["path"],later["git_blob"])==("gavinlinasd/StoneAge","1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56","gmsv/src/npc/npc_exchangeman.c","5d74290ed6f27163e0698b4375d5dc5e187c77c4")
    url="https://raw.githubusercontent.com/"+later["repo"]+"/"+later["commit"]+"/"+later["path"]
    with urllib.request.urlopen(url,timeout=45) as resp: code=resp.read(2000001)
    assert len(code)<=2000000 and git_blob(code)==later["git_blob"]
    body=code[code.index(b"BOOL NPC_EventAddEgg(int meindex, int talker, char *buff2,int mode)"):]
    body=body[:body.index(b"BOOL NPC_EventDelItem(")]
    for token in (b'enemyid = atoi( buf3)',b'petid = atoi( buf3)',b'raise = atoi( buf3)',b'petid = ENEMY_getInt( i, ENEMY_TEMPNO)',b'ENEMY_createPetFromEnemyIndex( talker, i)',b'CHAR_FUSIONBEIT, 1',b'CHAR_FUSIONCODE, -1',b'CHAR_FUSIONRAISE, raise',b'CHAR_FUSIONINDEX, petid',b'CHAR_FUSIONTIMELIMIT, (int)time( NULL)'):
        assert token in body
    assert b'NPC_EventAddEgg( meindex, talker, buff2,0)' in code and b'NPC_EventAddEgg( meindex, talker, buff2,1)' in code
    assert later["parameter_order"]==["egg_enemy_instance_id","offspring_enemy_instance_id","raise_count"]
    assert not any(later[k] for k in ("same_build_or_deployment_verified","original_argument_layout_verified","actual_hatching_verified"))
    assert len(r["rows"])==3
    for i,(x,y) in enumerate(zip(r["rows"],a["rows"])):
        assert (x["position"],x["name"],x["template_id"],x["graphic"],x["grade"],x["source_preflight_row"])==(y["position"],y["name"],y["template_id"],y["graphic"],y["role"],i)
        assert x["selected_instance_id"]==y["source_pairs"][0]["instances"][0]["instance_id"]
        assert x["retain_strict_gap"] and x["official_first_release"] is None and not any(x[k] for k in ("official_acquisition_verified","original_getegg_mapping_verified","later_code_mapping_to_this_template_verified"))
    assert r["strict_gap_count"]==67 and r["official_species_count"] is None and r["official_acquisition_closed"]==0
    assert not any(r[k] for k in ("runtime_executed","actual_hatch_result_verified","original_assets_published"))
    print("PET54_FINAL_PASS: original function entry and later source grammar independently bounded; 67 strict gaps")
if __name__=="__main__":
    main()
