"""Strict independent R13 derived-only report verifier; no runtime promotion."""
import argparse, json
from pathlib import Path
from tools.stoneage_tw10_savedata_mutations_r13 import (
    SCHEMA, STATUS, FLAGS, HELPER, GLOBAL_WRITES, RUNTIME_SHA256, SAVEDATA_SHA256,
)
EXPECTED_SITES = [*HELPER, *sorted(GLOBAL_WRITES)]
EXPECTED_SOURCES = ["imm", "ebx", "eax", "eax", "esi", "eax"]
WINDOWS = ((HELPER[0], HELPER[1], 13, [0x49dd1]),
           (min(GLOBAL_WRITES), max(GLOBAL_WRITES), 15, [0x49452]))
TOP = {"schema","status","runtime_sha256","savedata_sha256","r12_helper_states",
       "r12_import_slot_rva","store_candidates","linear_windows","static_candidate_scope"} | FLAGS

def unique(items):
    row = {}
    for k,v in items:
        if k in row: raise ValueError("duplicate JSON field")
        row[k] = v
    return row

def obj(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError("schema fields")
    return value

def integer(v, lo, hi):
    if type(v) is not int or not lo <= v <= hi:
        raise ValueError("integer range")
    return v

def validate(text):
    if type(text) is not str or len(text.encode("utf-8")) > 16000:
        raise ValueError("size")
    d = json.loads(text, object_pairs_hook=unique)
    obj(d, TOP)
    if (d["schema"] != SCHEMA or d["status"] != STATUS or
        d["runtime_sha256"] != RUNTIME_SHA256 or
        d["savedata_sha256"] != SAVEDATA_SHA256 or
        d["static_candidate_scope"] != "named-sites-only-no-reachability" or
        d["r12_helper_states"] != 32 or d["r12_import_slot_rva"] != 0x520f8):
        raise ValueError("original/R12 identity")
    if any(d[k] is not False for k in FLAGS): raise ValueError("promotion")
    rows = d["store_candidates"]
    if type(rows) is not list or len(rows) != 6: raise ValueError("store count")
    for i,(r,site) in enumerate(zip(rows, EXPECTED_SITES)):
        obj(r, {"site_rva","mnemonic_class","destination","destination_relative_field_offset",
                "expected_global_rva","source_operand","previous_destination_value_required",
                "address_inputs","value_input_registers","register_inputs_resolved",
                "executed_write_proven","effective_object_proven","named_caller_effect_admitted"})
        if r["site_rva"] != site or any(r[k] is not False for k in
           ("register_inputs_resolved","executed_write_proven","effective_object_proven",
            "named_caller_effect_admitted")):
            raise ValueError("site/promotion")
        dest = obj(r["destination"], {"store_rva","write_width_bytes","base_register",
           "index_register","index_scale","displacement_region","absolute_effective_rva",
           "effective_address_fully_known","table_or_object_ownership_proven"})
        if (dest["store_rva"] != site or dest["write_width_bytes"] != 4 or
            dest["index_register"] is not None or dest["index_scale"] != 1 or
            dest["table_or_object_ownership_proven"] is not False):
            raise ValueError("store shape")
        src = obj(r["source_operand"], {"kind","register","immediate","memory_input","width_bytes"})
        if src["width_bytes"] != 4 or src["memory_input"] is not None:
            raise ValueError("source width/shape")
        expected = EXPECTED_SOURCES[i]
        if i < 2:
            off = (-8,8)[i]
            if (dest["base_register"] != "ebp" or dest["displacement_region"] is not None or
                dest["absolute_effective_rva"] is not None or
                dest["effective_address_fully_known"] is not False or
                r["destination_relative_field_offset"] != off or
                r["expected_global_rva"] is not None or r["address_inputs"] != ["ebp"]):
                raise ValueError("frame-relative shape")
        else:
            target = GLOBAL_WRITES[site]
            region = obj(dest["displacement_region"], {"displacement_rva","section","raw_backed","writable"})
            if (dest["base_register"] is not None or
                dest["absolute_effective_rva"] != target or
                dest["effective_address_fully_known"] is not True or
                r["destination_relative_field_offset"] is not None or
                r["expected_global_rva"] != target or r["address_inputs"] != [] or
                region != {"displacement_rva":target,"section":".data",
                           "raw_backed":False,"writable":True}):
                raise ValueError("absolute .data geometry")
        if i == 0:
            if (r["mnemonic_class"] != "or" or
                r["previous_destination_value_required"] is not True or
                src != {"kind":"immediate_input","register":None,"immediate":0xffffffff,
                        "memory_input":None,"width_bytes":4} or
                r["value_input_registers"] != ["destination_memory"]):
                raise ValueError("R13 OR source")
        else:
            if (r["mnemonic_class"] != "mov" or
                r["previous_destination_value_required"] is not False or
                src != {"kind":"register_input","register":expected,"immediate":None,
                        "memory_input":None,"width_bytes":4} or
                r["value_input_registers"] != [expected]):
                raise ValueError("R13 MOV source")
    w = d["linear_windows"]
    if type(w) is not list or len(w) != 2: raise ValueError("window count")
    for row,(first,last,count,jumps) in zip(w,WINDOWS):
        obj(row, {"first_rva","last_site_rva","instruction_boundaries","jump_sites",
                  "same_executed_path_proven","function_boundary_proven",
                  "control_flow_conditions_proven"})
        offsets=row["instruction_boundaries"]
        if (row["first_rva"] != first or row["last_site_rva"] != last or
            type(offsets) is not list or len(offsets) != count or
            any(type(v) is not int for v in offsets) or
            offsets != sorted(set(offsets)) or
            offsets[0] != first or offsets[-1] != last or
            row["jump_sites"] != jumps or
            not set(jumps).issubset(offsets) or
            any(row[k] is not False for k in
                ("same_executed_path_proven","function_boundary_proven",
                 "control_flow_conditions_proven"))):
            raise ValueError("linear static scope")
    return {"schema":"tw10-r13-strict-original-derived-guard",
            "store_candidates":len(rows),"frame_stores":2,"global_write_candidates":4,
            "r12_helper_states":32,"named_effects_admitted":False,
            "native_io_executed":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(validate(a.report.read_text()),sort_keys=True))
if __name__=="__main__":
    main()
