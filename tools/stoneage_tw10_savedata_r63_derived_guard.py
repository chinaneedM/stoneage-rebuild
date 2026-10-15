"""Independent R63 structural guard for *derived-only* TW1.0 postcall reports.

Passing this guard proves report shape, not provenance, API execution or
native persisted bytes. An independently pinned original Actions artifact is
required before any historical instruction syntax is accepted.
"""
import argparse
import json
from pathlib import Path

SCHEMA="tw10-r63-original-postwritefile-static-operand-window"
RUNTIME_SHA="cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
SITES=((0x4C68C,0x4C692),(0x4C6F1,0x4C6F7))
FALSE_FLAGS=(
    "original_executable_executed",
    "original_savedata_payload_read_or_published",
    "actual_abi_or_register_stack_memory_preservation_proven",
    "actual_native_writefile_return_count_or_success_proven",
    "actual_buffer_flush_close_or_disk_persistence_proven",
    "original_savedata_schema_migration_or_server_authority_proven",
)

def require(ok,why):
    if not ok:
        raise ValueError("R63 derived artifact guard: "+why)

def validate(d):
    require(isinstance(d,dict) and d.get("schema")==SCHEMA, "schema")
    require(d.get("runtime_sha256")==RUNTIME_SHA, "pinned runtime identity string")
    require(d.get("candidate_root_rva")==0x4C5B4 and
            d.get("candidate_graph_nodes")==139 and
            d.get("candidate_graph_edges")==156 and
            d.get("bounded_call_return_assumption_only") is True,
            "bounded candidate root and structural assumption")
    for k in FALSE_FLAGS:
        require(d.get(k) is False, "unqualified runtime/persistence field "+k)
    sites=d.get("sites")
    require(isinstance(sites,list) and len(sites)==2,"exact two postcalls")
    for report,(call,post) in zip(sites,SITES):
        require(report.get("call_rva")==call and report.get("postcall_rva")==post and
                report.get("window_address_lower")==call-32 and
                report.get("window_address_upper")==post+48,
                "exact bounded call/postcall address windows")
        require(report.get("import_name")=="WriteFile" and
                report.get("import_slot_rva")==0x520A4 and
                report.get("syntactic_call_continuation_edge") is True,
                "import and structural fallthrough")
        for field in ("actual_callee_return_or_native_effect_proven",
                      "actual_eax_return_register_value_proven",
                      "actual_flags_or_branch_feasibility_proven",
                      "native_api_result_eax_or_bytecount_proven"):
            require(report.get(field) is False,"no native effect proof "+field)
        rows=report.get("decoded_instruction_rows")
        require(isinstance(rows,list) and 2<=len(rows)<=48,"bounded nonempty decoded rows")
        addresses=[x.get("site_rva") for x in rows]
        require(all(type(a) is int and call-32<=a<=post+48 for a in addresses)
                and addresses==sorted(set(addresses)) and
                call in addresses and post in addresses,
                "unique complete address-aligned local rows")
        for row in rows:
            require(isinstance(row.get("mnemonic"),str) and row["mnemonic"] and
                    isinstance(row.get("operands"),list) and
                    row.get("actual_instruction_effect_or_value_known") is False,
                    "decoded shapes never evaluated")
            require(not any(k in row for k in ("bytes","raw_binary","source_code","original_payload")),
                    "no raw original code or payload fields")
        call_row=next(x for x in rows if x["site_rva"]==call)
        require(call_row["mnemonic"]=="call","authentic site must be syntactic CALL")
        require(report.get("postcall_instruction")==next(x for x in rows if x["site_rva"]==post),
                "postcall instruction replay equality")
        edges=report.get("bounded_local_edges")
        require(isinstance(edges,list) and
                all(isinstance(e,list) and len(e)==2 and e[0] in addresses and e[1] in addresses for e in edges),
                "all local edges must land inside decoded rows")
        require(edges==[list(e) for e in sorted({tuple(e) for e in edges})],
                "edges sorted and unique")
        require([call,post] in edges,"direct call continuation")
    require("original_runtime_bytes" not in d and "original_savedata_bytes" not in d,
            "no proprietary source surfaces")
    return {"schema":SCHEMA,"guard":"STRUCTURE_ONLY",
            "original_static_source_artifact_cryptographically_pinned":False,
            "native_result_or_disk_persistence_proven":False,
            "checked_sites":[post for _,post in SITES]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",required=True,type=Path)
    args=p.parse_args()
    result=validate(json.loads(args.report.read_text()))
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":
    main()
