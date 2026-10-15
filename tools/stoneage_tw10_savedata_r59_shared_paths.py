"""R59: bounded shared-helper syntax routes from accepted R58 derived-only rows.

Graph witnesses are possible *structural* paths under returning CALL assumptions.
They are not executed traces, call/ABI proof, memory persistence, or OS results.
"""
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

SOURCE_SHA = "04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8"
SCHEMA = "tw10-r59-shared-helper-three-way-static-route-contract"
ROOT, CALL, RETURN = 0x4A657, 0x4A683, 0x4A6B2
ERROR_FLAG, ALL_ONES = 0x4A69D, 0x4A6A1
BRANCHES = {
    0x4A66B: (0x4A66D, 0x4A6A4),
    0x4A671: (0x4A673, 0x4A6A4),
    0x4A67C: (0x4A67E, 0x4A6A4),
    0x4A68D: (0x4A68F, ERROR_FLAG),
    0x4A694: (0x4A696, 0x4A6A4),
}

def require(ok, why):
    if not ok:
        raise ValueError("R59 shared-helper route " + why)

def operand_signature(row):
    return [(x.get("kind"), x.get("register"), x.get("constant")) for x in row["operands"]]

def route(edges, start, end, required=(), forbidden=()):
    avoid = set(forbidden)
    needs = {at: (1 << i) for i, at in enumerate(required)}
    wanted = (1 << len(needs)) - 1
    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    todo = deque([(start, needs.get(start, 0), (start,))])
    seen = set()
    while todo:
        at, mask, path = todo.popleft()
        if at in avoid or (at, mask) in seen:
            continue
        seen.add((at, mask))
        if at == end and mask == wanted:
            return list(path)
        for nxt in sorted(graph.get(at, [])):
            todo.append((nxt, mask | needs.get(nxt, 0), path + (nxt,)))
    return None

def derive(report):
    require(report.get("schema") == "tw10-r58-original-rooted-shared-close-helper-static-inventory", "schema")
    contexts = report.get("contexts")
    require(isinstance(contexts, list) and len(contexts) == 2, "contexts")
    c = next((x for x in contexts if x.get("root_candidate_rva") == ROOT), None)
    require(c is not None and c.get("bounded_graph_complete") is True, "root closure")
    g = c["graph"]
    require(g["frontier"] == [] and g["node_limit_hit"] is False and
            g["nodes"] == 40 and g["edges"] == 44, "bounded metadata")
    ns = c["bounded_node_rvas"]
    edges = c["bounded_edges"]
    rows = c["instruction_shapes"]
    require(ns == sorted(set(ns)) and len(ns) == 40 and
            [x["site_rva"] for x in rows] == ns, "complete operand rows")
    require(edges == [list(x) for x in sorted({tuple(y) for y in edges})] and len(edges) == 44 and
            all(a in ns and b in ns for a,b in edges), "exact edge topology")
    by = {r["site_rva"]:r for r in rows}
    for at, successors in BRANCHES.items():
        require(tuple(sorted(b for a,b in edges if a == at)) == tuple(sorted(successors)), "branch successors " + hex(at))
    expected = {
        0x4A65D: ("xor", [("register","ebx",None),("register","ebx",None)]),
        CALL: ("call", [("immediate",None,0x400000+0x4C5B4)]),
        0x4A68B: ("cmp", [("register","eax",None),("register","edi",None)]),
        ERROR_FLAG: ("or", [("memory",None,None),("immediate",None,0x20)]),
        ALL_ONES: ("or", [("register","ebx",None),("immediate",None,0xffffffff)]),
        0x4A6AE: ("mov", [("register","eax",None),("register","ebx",None)]),
        RETURN: ("ret", []),
    }
    for at, (mn, operands) in expected.items():
        require(by[at]["mnemonic"] == mn and operand_signature(by[at]) == operands, "literal instruction " + hex(at))
    require(by[ERROR_FLAG]["operands"][0]["geometry"]["base_register"] == "esi" and
            by[ERROR_FLAG]["operands"][0]["geometry"]["relative_field_offset"] == 12,
            "error-flag object slot")
    calls = [x for x in c["call_contexts"] if x["site_rva"] == CALL]
    require(len(calls) == 1 and calls[0]["identity"]["direct_target_rva"] == 0x4C5B4, "call identity")
    bypass = route(edges, ROOT, RETURN, forbidden=(CALL,))
    via_without_flag = route(edges, ROOT, RETURN, required=(CALL,), forbidden=(ERROR_FLAG,))
    via_flag = route(edges, ROOT, RETURN, required=(CALL,ERROR_FLAG,ALL_ONES))
    require(all((bypass,via_without_flag,via_flag)), "three structural witness families")
    require(0x4A65D in bypass and 0x4A6AE in bypass and ALL_ONES not in bypass and
            not any(by[at]["mnemonic"] == "call" for at in bypass), "call-free candidate zero spelling")
    require(0x4A68B in via_without_flag and 0x4A68B in via_flag, "postcall compare provenance")
    return {
        "schema": SCHEMA, "original_derived_source_sha256": SOURCE_SHA,
        "shared_helper_root_rva": ROOT, "nested_context_root_rva": 0x4C5B4,
        "nested_call_site_rva": CALL, "ret_rva": RETURN,
        "bounded_graph_nodes":len(ns), "bounded_graph_edges":len(edges),
        "structural_call_free_candidate_zero_return":bypass,
        "structural_nested_call_without_error_flag_write":via_without_flag,
        "structural_nested_call_with_error_flag_and_all_ones_return":via_flag,
        "branch_sites_and_successors":[{"site_rva":at,"mnemonic":by[at]["mnemonic"],
                                         "successor_rvas":list(sorted(v))}
                                        for at,v in sorted(BRANCHES.items())],
        "all_three_path_families_are_syntax_witnesses_only":True,
        "actual_original_branch_feasibility_proven":False,
        "opaque_nested_call_preserves_edi_esi_ebx_or_memory_proven":False,
        "full_count_return_implies_native_write_executed":False,
        "all_ones_is_original_native_error_convention_proven":False,
        "actual_original_file_write_flush_close_or_persistence_proven":False,
        "original_executable_or_native_api_executed":False,
        "next":"R59 test caller/register/memory barriers and R28 native-root site reachability separately; never promote graph route to runtime I/O.",
    }

def read_source(path):
    raw=Path(path).read_bytes()
    require(len(raw)==124989 and hashlib.sha256(raw).hexdigest()==SOURCE_SHA, "immutable R58 source")
    return json.loads(raw)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--verify",type=Path)
    args=p.parse_args()
    out=derive(read_source(args.source))
    if args.verify:
        previous=json.loads(args.verify.read_text())
        require(json.dumps(out,sort_keys=True)==json.dumps(previous,sort_keys=True),"contract mismatch")
        print("TW10_R59_THREE_STATIC_ROUTE_FAMILIES=PASS; ACTUAL_NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(out,sort_keys=True))

if __name__ == "__main__":
    main()
