"""R60: original-derived close-path predicates versus opaque native WriteFile results.

Static bounded CFG shape only. Never execute source binary/Win32 APIs or infer
savedata persistence, native success, EAX semantics or runtime branch feasibility.
"""
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

SCHEMA = "tw10-r60-writefile-opaque-return-and-close-predicate-static-contract"
R28_BLOB = "3671661219120d45bd922e05b6df371523b42432"
R58_BLOB = "223b65683d37332546ada0fe034a81550b5e8ed8"
R58_SHA256 = "04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8"
CLOSE_ROOT = 0x4A53E
CLOSE_CALL, ERROR_CALL = 0x4A5A3, 0x4A5AD
RET = 0x4A5F0
ZERO, ONES = 0x4A5D4, 0x4A5E9


def require(test, reason):
    if not test:
        raise ValueError("R60 close/nativestatus: " + reason)


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def instruction(row, mnemonic, operands):
    require(row["mnemonic"] == mnemonic, "mnemonic " + hex(row["site_rva"]))
    actual = [(o.get("kind"), o.get("register"), o.get("constant")) for o in row["operands"]]
    require(actual == operands, "operands " + hex(row["site_rva"]))


def path(edges, root, target, required=(), banned=()):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    need = {r: 1 << i for i, r in enumerate(required)}
    full = (1 << len(need)) - 1
    todo = deque([(root, need.get(root, 0), (root,))])
    seen = set()
    while todo:
        at, mask, history = todo.popleft()
        if at in banned or (at, mask) in seen:
            continue
        seen.add((at, mask))
        if at == target and mask == full:
            return list(history)
        for nxt in sorted(graph.get(at, [])):
            todo.append((nxt, mask | need.get(nxt, 0), history + (nxt,)))
    return None


def derive(r28, r58):
    require(r28.get("schema") == "tw10-r28-original-call-supported-native-api-input-candidates",
            "R28 source schema")
    require(r58.get("schema") == "tw10-r58-original-rooted-shared-close-helper-static-inventory",
            "R58 source schema")
    require(r28["runtime_sha256"] == r58["runtime_sha256"] and
            r28["savedata_sha256"] == r58["savedata_sha256"], "same source identity")
    require(r28.get("native_io_executed") is False and
            r28.get("caller_return_effects_admitted") is False and
            r58.get("native_code_executed") is False and
            r58.get("actual_native_flush_close_or_persistence_proven") is False and
            r58.get("actual_helper_result_or_error_convention_proven") is False,
            "source execution/nonpromotion")
    write = [x for x in r28["contexts"] if x["api"] == "WriteFile"]
    require(len(write) == 1 and write[0]["root_candidate_rva"] == 0x4C5B4,
            "R28 native root")
    write = write[0]
    require(write["graph"]["nodes"] == 139 and write["graph"]["edges"] == 156 and
            write["graph"]["frontier"] == [] and
            write["graph"]["node_limit_hit"] is False and
            write["graph"]["all_incoming_paths_proven"] is False, "R28 graph bounds")
    after = []
    for at, post, prior in ((0x4C68C, 0x4C692, True), (0x4C6F1, 0x4C6F7, False)):
        sites = [s for s in write["api_sites"] if s["site_rva"] == at]
        require(len(sites) == 1, "R28 WriteFile call-site identity")
        s = sites[0]
        ident = s["identity"]
        require(s["conditional_post_call_rva"] == post and
                s["prior_graph_site_reached"] is prior and
                s["actual_external_return_proven"] is False and
                ident["kind"] == "memory_indirect" and
                ident["import_identity"]["name"] == "WriteFile" and
                ident["import_identity"]["iat_rva"] == 0x520A4 and
                ident["runtime_target_or_effects_proven"] is False,
                "R28 imported call and earlier coverage barrier")
        q = [x for x in write["inputs"]["queries"]
             if x["site_rva"] == post and x["register"] == "eax"]
        require(len(q) == 1 and q[0]["actual_register_value_known"] is False and
                q[0]["dependency_queries"] == [] and
                len(q[0]["reaching_candidates"]) == 1 and
                q[0]["reaching_candidates"][0]["origin"] == "unknown_call" and
                q[0]["reaching_candidates"][0]["rva"] == at and
                q[0]["reaching_candidates"][0]["semantic"] is None,
                "R28 post-call EAX unknown source")
        after.append({"writefile_site_rva": at, "conditional_post_call_rva": post,
                      "prior_graph_site_reached": prior,
                      "eax_reaching_source": "unknown_call",
                      "eax_value_or_native_written_count_proven": False})

    close = [x for x in r58["contexts"] if x["root_candidate_rva"] == CLOSE_ROOT]
    require(len(close) == 1 and close[0]["bounded_graph_complete"] is True and
            close[0]["actual_path_or_callee_effects_proven"] is False, "R58 close root")
    close = close[0]
    g = close["graph"]
    nodes = close["bounded_node_rvas"]
    edges = close["bounded_edges"]
    require(g["nodes"] == 66 and g["edges"] == 73 and g["frontier"] == [] and
            g["node_limit_hit"] is False and g["returning_call_assumption_only"] is True and
            len(nodes) == 66 and nodes == sorted(set(nodes)) and
            len(edges) == 73 and
            edges == [list(x) for x in sorted({tuple(y) for y in edges})] and
            all(a in nodes and b in nodes for a, b in edges),
            "R58 exact bounded graph")
    rows = close["instruction_shapes"]
    require(close["instruction_shapes_truncated"] is False and
            [x["site_rva"] for x in rows] == nodes, "R58 full instruction inventory")
    by = {x["site_rva"]: x for x in rows}
    reg = lambda x: ("register", x, None)
    imm = lambda x: ("immediate", None, x)
    mem = ("memory", None, None)
    expected = {
        CLOSE_CALL: ("call", [mem]),
        0x4A5A9: ("test", [reg("eax"), reg("eax")]),
        0x4A5AB: ("jne", [("immediate", None, 0x400000 + 0x4A5B7)]),
        ERROR_CALL: ("call", [mem]),
        0x4A5B3: ("mov", [reg("ebp"), reg("eax")]),
        0x4A5B7: ("xor", [reg("ebp"), reg("ebp")]),
        0x4A5C7: ("test", [reg("ebp"), reg("ebp")]),
        0x4A5C9: ("je", [("immediate", None, 0x400000 + ZERO)]),
        0x4A5CC: ("call", [("immediate", None, 0x400000 + 0x4C953)]),
        ZERO: ("xor", [reg("eax"), reg("eax")]),
        ONES: ("or", [reg("eax"), imm(0xffffffff)]),
        RET: ("ret", []),
        0x4A5D8: ("and", [mem, imm(0)]),
        0x4A5DF: ("mov", [mem, imm(9)]),
    }
    for at, (mn, operands) in expected.items():
        require(at in by, "R58 instruction missing " + hex(at))
        instruction(by[at], mn, operands)
    calls = {x["site_rva"]: x["identity"] for x in close["call_contexts"]}
    for site, name, iat in ((CLOSE_CALL, "CloseHandle", 0x520A8),
                            (ERROR_CALL, "GetLastError", 0x5208C)):
        ident = calls[site]
        require(ident["kind"] == "memory_indirect" and
                ident["import_identity"]["name"] == name and
                ident["import_identity"]["iat_rva"] == iat and
                ident["runtime_target_or_effects_proven"] is False,
                "R58 Win32 import identity " + name)
    for branch, successors in {
        0x4A54C: (0x4A552, 0x4A5D8),
        0x4A5AB: (ERROR_CALL, 0x4A5B7),
        0x4A5C9: (0x4A5CB, ZERO),
    }.items():
        require(tuple(sorted(b for a, b in edges if a == branch)) ==
                tuple(sorted(successors)), "branch successor " + hex(branch))

    scenarios = {
        "early_range_guard_all_ones_without_native_close":
            {"must": [0x4A5D8, 0x4A5DF, ONES], "ban": [CLOSE_CALL, ERROR_CALL, ZERO]},
        "close_handle_nonzero_test_shape_skips_getlasterror_and_zero_return":
            {"must": [CLOSE_CALL, 0x4A5A9, 0x4A5AB, 0x4A5B7, 0x4A5C9, ZERO],
             "ban": [ERROR_CALL, ONES]},
        "close_handle_zero_test_shape_getlasterror_then_zero_return":
            {"must": [CLOSE_CALL, 0x4A5AB, ERROR_CALL, 0x4A5B3, 0x4A5C7, 0x4A5C9, ZERO],
             "ban": [0x4A5B7, 0x4A5CC, ONES]},
        "close_handle_zero_test_shape_getlasterror_nonzero_error_helper_all_ones":
            {"must": [CLOSE_CALL, 0x4A5AB, ERROR_CALL, 0x4A5B3, 0x4A5C7, 0x4A5C9, 0x4A5CC, ONES],
             "ban": [0x4A5B7, ZERO]},
    }
    witnesses = {}
    for label, cfg in scenarios.items():
        candidate = path(edges, CLOSE_ROOT, RET, required=tuple(cfg["must"]),
                         banned=tuple(cfg["ban"]))
        require(candidate is not None and candidate[-1] == RET, "missing conditional witness " + label)
        witnesses[label] = candidate

    return {
        "schema": SCHEMA,
        "source_git_blobs": {"R28": R28_BLOB, "R58": R58_BLOB},
        "source_r58_sha256": R58_SHA256,
        "native_write_root_rva": 0x4C5B4,
        "writefile_postcall_eax_provenance": after,
        "close_root_rva": CLOSE_ROOT,
        "close_import_sites": [{"site_rva": CLOSE_CALL, "api": "CloseHandle", "iat_rva": 0x520A8},
                               {"site_rva": ERROR_CALL, "api": "GetLastError", "iat_rva": 0x5208C}],
        "close_bounded_nodes": len(nodes),
        "close_bounded_edges": len(edges),
        "close_structural_candidate_routes": witnesses,
        "structural_call_returns_and_branch_feasibility_assumed_not_proven": True,
        "closehandle_or_getlasterror_original_result_known": False,
        "call_clobber_frame_stack_alias_register_preservation_proven": False,
        "test_or_jump_native_success_error_mapping_proven": False,
        "getlasterror_is_original_savedata_error_code_proven": False,
        "original_writefile_bytecount_or_success_proven": False,
        "original_close_flush_disk_persistence_proven": False,
        "original_executable_payload_or_native_api_executed": False,
        "next": "R61 exact R28 native-context postcall operand/control inventory and cross-function ABI preservation; originals only for precisely missing evidence",
    }


def inspect_raw(raw28, raw58):
    require(git_blob(raw28) == R28_BLOB and git_blob(raw58) == R58_BLOB and
            len(raw58) == 124989 and hashlib.sha256(raw58).hexdigest() == R58_SHA256,
            "immutable original-derived report custody")
    return derive(json.loads(raw28), json.loads(raw58))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--r28", type=Path, default=Path("research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json"))
    p.add_argument("--r58", type=Path, default=Path("research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json"))
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    contract = inspect_raw(a.r28.read_bytes(), a.r58.read_bytes())
    if a.verify:
        require(contract == json.loads(a.verify.read_text()), "replay contract drift")
        print("TW10_R60_CLOSE_PREDICATE_STRUCTURAL=PASS; WRITEFILE_EAX=OPEN; PERSISTENCE=OPEN")
    else:
        print(json.dumps(contract, sort_keys=True))


if __name__ == "__main__":
    main()
