"""R64: independently reconcile pinned R63 original-static TEST/Jcc syntax with R28 PUSH candidates.

An API return register is not the output byte-count pointer. Structural paths,
ABI argument positions, register/stack aliases and native success remain OPEN.
"""
import argparse
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_savedata_r63_derived_guard import validate as validate_r63

SCHEMA="tw10-r64-postwritefile-test-flags-physical-count-pointer-audit"
R63_JSON_SHA="91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd"
R28_BLOB="3671661219120d45bd922e05b6df371523b42432"
SITES=((0x4C68C,0x4C692),(0x4C6F1,0x4C6F7))
NONPROMOTION=(
  "original_native_writefile_executed",
  "actual_writefile_bool_return_known",
  "actual_bytes_written_memory_pointer_validated",
  "actual_bytes_written_memory_contents_known",
  "actual_stack_frame_register_callee_preservation_proven",
  "actual_branches_executed_or_conditions_resolved",
  "actual_flush_close_or_disk_persistence_proven",
  "original_savedata_payload_evaluated_or_published",
)
def need(ok,why):
    if not ok:
        raise ValueError("R64 static scope: "+why)
def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
def one(rows,pred,label):
    x=[a for a in rows if pred(a)]
    need(len(x)==1,label)
    return x[0]
def signature(op):
    return {"kind":op.get("kind"),"register":op.get("register"),"constant":op.get("constant"),
            "width_bytes":op.get("width_bytes"),"geometry":op.get("geometry")}
def trace(r63,r28):
    validate_r63(r63)
    need(r28.get("schema")=="tw10-r28-original-call-supported-native-api-input-candidates"
         and r28.get("static_only") is True and r28.get("native_io_executed") is False
         and r28.get("caller_return_effects_admitted") is False,
         "R28 immutable source semantics")
    w=one(r28["contexts"],lambda x:x.get("api")=="WriteFile","R28 write candidate root")
    need(w["root_candidate_rva"]==0x4C5B4 and
         w["graph"]["nodes"]==139 and w["graph"]["edges"]==156 and
         w["graph"]["frontier"]==[] and not w["graph"]["node_limit_hit"],
         "R28 bounded native context")

    contexts=[]
    for report,(call,post) in zip(r63["sites"],SITES):
        need(report["call_rva"]==call and report["postcall_rva"]==post,
             "R63 exact ordered call/post pair")
        rows=report["decoded_instruction_rows"]
        by={x["site_rva"]:x for x in rows}
        edges=[tuple(e) for e in report["bounded_local_edges"]]
        out=lambda p:sorted(b for a,b in edges if a==p)
        postrow=by[post]
        need(postrow["mnemonic"]=="test" and len(postrow["operands"])==2,
             "accepted R63 postcall TEST spelling")
        need("eflags" in postrow["decoder_written_registers"],
             "TEST must write flag register metadata")
        need(len(out(post))==1,"single structural continuation after TEST")
        nxt=out(post)[0]
        immediate=by[nxt]
        is_conditional=immediate["mnemonic"].startswith("j") and immediate["mnemonic"] not in ("jmp","ljmp")
        if is_conditional:
            # R63 stores only edges whose *both* endpoints lie within the narrow
            # bounded operand window. A second target may be outside that window.
            need(1<=len(out(nxt))<=2,"conditional branch local successors")
        # Unknown native EAX can be a TEST operand; even then its runtime value is not proven.
        exact_eax_operand=any(x.get("kind")=="register" and x.get("register")=="eax"
                             for x in postrow["operands"])
        s=one(w["api_sites"],lambda x:x["site_rva"]==call,
              "pinned R28 exact native import call")
        need(s["conditional_post_call_rva"]==post and s["actual_external_return_proven"] is False
             and s["identity"]["import_identity"]["name"]=="WriteFile"
             and s["identity"]["import_identity"]["iat_rva"]==0x520A4,
             "R28 exact native import/return barrier")
        queries=[q for q in w["inputs"]["queries"] if
                 q["site_rva"]==post and q["register"]=="eax"]
        need(len(queries)==1 and not queries[0]["actual_register_value_known"] and
             queries[0]["reaching_candidates"]==[
                {"origin":"unknown_call","rva":call,"semantic":None}],
             "EAX remains unknown opaque API return")
        pushes=s["push_candidates"]
        need(len(pushes)==5 and
             sorted(p["conditional_pre_call_esp_offset"] for p in pushes)==[0,4,8,12,16],
             "R28 five distinct *conditional* stack suffix offsets")
        stack=[]
        for p in sorted(pushes,key=lambda v:v["conditional_pre_call_esp_offset"]):
            at=p["site_rva"];row=by.get(at)
            need(row is not None and row["mnemonic"]=="push" and len(row["operands"])==1,
                 "source R63 physical PUSH row missing "+hex(at))
            need(row["operands"][0]==p["input"],"R28/R63 decoded PUSH operand mismatch "+hex(at))
            stack.append({
                "push_rva":at,
                "conditional_pre_call_esp_offset":p["conditional_pre_call_esp_offset"],
                "decoded_operand":row["operands"][0],
                "original_pushed_value_known":False,
                "original_stack_slot_or_parameter_binding_proven":False
            })
        count_slot=one(stack,lambda x:x["conditional_pre_call_esp_offset"]==12,
                       "conditional fourth argument memory location")
        contexts.append({
            "native_call_rva":call,
            "postcall_test_rva":post,
            "test_operand_signatures":[signature(x) for x in postrow["operands"]],
            "test_decoder_read_registers":postrow["decoder_read_registers"],
            "test_decoder_written_registers":postrow["decoder_written_registers"],
            "test_direct_successor_rva":nxt,
            "immediate_successor_mnemonic":immediate["mnemonic"],
            "immediate_successor_is_conditional_jump":is_conditional,
            "immediate_branch_successors":out(nxt) if is_conditional else [],
            "both_branch_successors_inside_r63_window":is_conditional and len(out(nxt))==2,
            "postcall_test_has_explicit_eax_operand":exact_eax_operand,
            "native_eax_from_opaque_unknown_call":True,
            "structural_flag_source_candidate":is_conditional,
            "actual_flags_or_branch_values_known":False,
            "physical_push_candidates":stack,
            "win32_x86_stdcall_bytes_written_pointer_position_candidate":
                {"conditional_pre_call_esp_offset":12,
                 "original_rva":count_slot["push_rva"],
                 "operand":count_slot["decoded_operand"],
                 "depends_on_unproven_stdcall_frame_and_callee_preservation":True,
                 "actual_pointer_or_written_bytes_proven":False},
            "api_bool_return_eax_is_separate_from_count_pointer_memory":True,
            "actual_native_api_count_success_or_disk_write_proven":False,
        })
    return {
        "schema":SCHEMA,
        "r63_original_derived_json_sha256":R63_JSON_SHA,
        "r28_git_blob":R28_BLOB,
        "native_candidate_root_rva":0x4C5B4,
        "postcall_contexts":contexts,
        "call_fallthrough_and_frame_values_assumed_not_proven":True,
        "separates_bool_like_eax_from_lpnumberofbyteswritten_position":True,
        **{flag:False for flag in NONPROMOTION},
        "next":"R65 independent exact control-flag predecessor and dynamic memory/ABI barriers; no native result or persistence promotion"
    }
def inspect_raw(raw63,raw28):
    need(hashlib.sha256(raw63).hexdigest()==R63_JSON_SHA,"exact R63 accepted original-derived JSON SHA256")
    need(git_blob(raw28)==R28_BLOB,"R28 immutable original-derived Git blob")
    return trace(json.loads(raw63),json.loads(raw28))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--r63",required=True,type=Path)
    parser.add_argument("--r28",type=Path,default=Path(
      "research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json"))
    parser.add_argument("--verify",type=Path)
    a=parser.parse_args()
    report=inspect_raw(a.r63.read_bytes(),a.r28.read_bytes())
    if a.verify:
        need(report==json.loads(a.verify.read_text()),"exact derived-only replay")
        print("TW10_R64_TEST_AND_ARGUMENT_POSITION=PASS; NATIVE_WRITE_AND_PERSISTENCE=OPEN")
    else:
        print(json.dumps(report,sort_keys=True))
if __name__=="__main__":
    main()
