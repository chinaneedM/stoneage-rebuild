"""R59 pinned R28/R58 static-only savedata native-call bridge.

Cross-links previously authenticated numeric metadata. Does not execute any
original client/native API, load original savedata content or certify writes.
"""
import argparse
import hashlib
import json
from pathlib import Path

SCHEMA = "tw10-r59-existing-metadata-native-call-linkage"
R28_SCHEMA = "tw10-r28-original-call-supported-native-api-input-candidates"
R58_SCHEMA = "tw10-r58-original-rooted-shared-close-helper-static-inventory"
R28_BLOB = "3671661219120d45bd922e05b6df371523b42432"
R58_BLOB = "223b65683d37332546ada0fe034a81550b5e8ed8"
R58_SHA256 = "04fb0b586f1fcf87f647b1bc1276bde2505822e195646c4c9058c03c7f558fe8"


def require(test, reason):
    if not test:
        raise ValueError("R59 " + reason)


def unique(rows, predicate, reason):
    found = [x for x in rows if predicate(x)]
    require(len(found) == 1, reason)
    return found[0]


def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def derive(r28, r58):
    require(r28.get("schema") == R28_SCHEMA and r58.get("schema") == R58_SCHEMA, "source schema")
    require(r28.get("runtime_sha256") == r58.get("runtime_sha256") and
            r28.get("savedata_sha256") == r58.get("savedata_sha256"), "same original identity")
    for key in ("caller_return_effects_admitted", "native_io_executed", "original_bytes_published"):
        require(r28.get(key) is False, "R28 nonpromotion " + key)
    for key in ("actual_native_flush_close_or_persistence_proven", "native_code_executed",
                "original_bytes_published", "actual_helper_result_or_error_convention_proven"):
        require(r58.get(key) is False, "R58 nonpromotion " + key)
    write = unique(r28["contexts"], lambda c: c.get("api") == "WriteFile", "R28 WriteFile root")
    require(write.get("root_candidate_rva") == 0x4c5b4 and
            write.get("caller_rva") == 0x48c5e and
            write.get("entry_or_call_execution_proven") is False, "R28 original caller/root")
    graph = write.get("graph", {})
    require(graph.get("nodes") == 139 and graph.get("edges") == 156 and
            graph.get("frontier") == [] and graph.get("node_limit_hit") is False and
            graph.get("all_incoming_paths_proven") is False, "R28 bounded graph")
    require(write.get("caller_identity", {}).get("direct_target_rva") == 0x4c5b4,
            "R28 direct caller target")
    shared = unique(r58["contexts"], lambda c: c.get("root_candidate_rva") == 0x4a657,
                    "R58 shared helper")
    close = unique(r58["contexts"], lambda c: c.get("root_candidate_rva") == 0x4a53e,
                   "R58 close helper")
    require(shared.get("bounded_graph_complete") is True and
            close.get("bounded_graph_complete") is True, "R58 bounded roots")
    for c in (shared, close):
        require(c.get("actual_path_or_callee_effects_proven") is False, "R58 callee barrier")

    def bridge(c):
        return sorted([b["wrapper_root_rva"], b["call_site_rva"], b["target_rva"]]
                      for b in c["r57_caller_bridges"])
    require(bridge(shared) == [[0x4856c, 0x48586, 0x4a657],
                               [0x48bbc, 0x48c38, 0x4a657]], "shared R57 bridges")
    require(bridge(close) == [[0x4856c, 0x48596, 0x4a53e]], "close R57 bridge")
    sub = unique(shared["call_contexts"], lambda x: x.get("site_rva") == 0x4a683,
                 "R58 direct native-context subcall")
    require(sub["identity"].get("kind") == "direct" and
            sub["identity"].get("direct_target_rva") == 0x4c5b4,
            "R58 shared-to-native-context target")

    def native_site(rows, site, name, iat):
        x = unique(rows, lambda item: item.get("site_rva") == site, name + " site")
        ident = x["identity"]
        imp = ident.get("import_identity") or {}
        require(ident.get("kind") == "memory_indirect" and
                ident.get("import_slot_association_proven") is True and
                ident.get("runtime_target_or_effects_proven") is False and
                imp.get("name") == name and imp.get("iat_rva") == iat,
                name + " import-slot identity")
        return {"site_rva": site, "import_name": name, "iat_rva": iat,
                "memory_indirect_syntax_only": True, "executed_or_return_proven": False}

    writes = [native_site(write["api_sites"], 0x4c68c, "WriteFile", 0x520a4),
              native_site(write["api_sites"], 0x4c6f1, "WriteFile", 0x520a4)]
    require(all(x.get("site_in_candidate_graph") is True and
                x.get("actual_external_return_proven") is False
                for x in write["api_sites"] if x["site_rva"] in (0x4c68c, 0x4c6f1)),
            "R28 WriteFile graph/return barrier")
    cleanup = [native_site(close["call_contexts"], 0x4a5a3, "CloseHandle", 0x520a8),
               native_site(close["call_contexts"], 0x4a5ad, "GetLastError", 0x5208c)]
    return {
        "schema": SCHEMA,
        "sources": {"r28_git_blob": R28_BLOB, "r58_git_blob": R58_BLOB,
                    "r58_raw_sha256": R58_SHA256},
        "static_direct_edges": [
            {"from_rva": 0x48c38, "to_rva": 0x4a657, "wrapper": "write"},
            {"from_rva": 0x48586, "to_rva": 0x4a657, "wrapper": "close"},
            {"from_rva": 0x4a683, "to_rva": 0x4c5b4, "wrapper": "shared"},
            {"from_rva": 0x48c5e, "to_rva": 0x4c5b4, "wrapper": "write_direct"},
            {"from_rva": 0x48596, "to_rva": 0x4a53e, "wrapper": "close"},
        ],
        "r28_native_context_bounded_nodes": graph["nodes"],
        "r28_native_context_bounded_edges": graph["edges"],
        "writefile_import_sites": writes,
        "close_path_import_sites": cleanup,
        "r28_second_writefile_prior_graph_reached": False,
        "native_api_execution_or_effects_proven": False,
        "original_return_success_error_abi_alias_or_file_ownership_proven": False,
        "actual_savedata_written_bytes_flush_close_or_persistence_proven": False,
        "original_payload_schema_version_migration_or_server_authority_proven": False,
        "next": "R59 follow-on: native-context result/count paths and close/error predicate barriers",
    }


def inspect_raw(raw28, raw58):
    require(blob_sha(raw28) == R28_BLOB, "R28 immutable Git blob mismatch")
    require(blob_sha(raw58) == R58_BLOB and
            hashlib.sha256(raw58).hexdigest() == R58_SHA256,
            "R58 immutable Git blob/SHA256 mismatch")
    return derive(json.loads(raw28), json.loads(raw58))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--r28", type=Path, default=Path("research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R28-ORIGINAL.json"))
    p.add_argument("--r58", type=Path, default=Path("research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R58-ORIGINAL.json"))
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    result = inspect_raw(a.r28.read_bytes(), a.r58.read_bytes())
    if a.verify is not None:
        require(result == json.loads(a.verify.read_text()), "derived contract changed")
        print("TW10_R59_EXISTING_METADATA_BRIDGE=PASS; NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
