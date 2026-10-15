"""R61: source-pinned native WriteFile postcall / frame-preservation gap ledger.

This is an original-derived metadata audit, not an original executable trace.
Do not infer native return values, actual byte count, ABI preservation or disk persistence.
"""
import argparse
import hashlib
import json
from pathlib import Path

BLOBS = {
    28: "3671661219120d45bd922e05b6df371523b42432",
    44: "39c1c0f673747fb560cc285d627490e5cd38047a",
    45: "1e7fb71cec336c1b4fc531d4f4a6933c9f66d415",
}
SCHEMA = "tw10-r61-native-postcall-missing-evidence-ledger"
ROOT = 0x4C5B4
SITES = ((0x4C68C, 0x4C692, True), (0x4C6F1, 0x4C6F7, False))

def need(ok, reason):
    if not ok:
        raise ValueError("R61 evidence gate: " + reason)

def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

def one(items, predicate, label):
    hits = [x for x in items if predicate(x)]
    need(len(hits) == 1, label)
    return hits[0]

def derive(r28, r44, r45):
    for n, d in ((28, r28), (44, r44), (45, r45)):
        need(d.get("static_only") is True and d.get("native_io_executed") is False, f"R{n} source status")
        need(d.get("runtime_sha256") == r28.get("runtime_sha256") and
             d.get("savedata_sha256") == r28.get("savedata_sha256"), f"R{n} source identity")
    for flag in ("caller_return_effects_admitted", "actual_paths_frames_or_argument_values_proven"):
        need(r28.get(flag) is False, "R28 non-promotion "+flag)
    for flag in ("actual_esp_stack_contents_or_frame_preservation_proven",
                 "original_size_product_or_api_byte_count_proven"):
        need(r44.get(flag) is False, "R44 non-promotion "+flag)
    for flag in ("actual_write_frame_preservation_or_callee_effects_proven",
                 "actual_entry_count_or_api_transferred_bytes_proven"):
        need(r45.get(flag) is False, "R45 non-promotion "+flag)

    w28 = one(r28["contexts"], lambda x: x.get("api") == "WriteFile", "R28 write context")
    c44 = one(r44["native_contexts"], lambda x: x.get("native_root_candidate_rva") == ROOT, "R44 write root")
    w45 = one(r45["native_api_contexts"], lambda x: x.get("site_rva") == SITES[0][0], "R45 first write call")
    for label, obj in (("R28", w28), ("R44", c44), ("R45", w45)):
        g = obj["graph"]
        need(g["nodes"] == 139 and g["edges"] == 156 and
             g["frontier"] == [] and g["node_limit_hit"] is False,
             label+" bounded native context")
    need(w28["root_candidate_rva"] == ROOT and
         c44["wrapper_root_candidate_rva"] is not None and
         w45["root_candidate_rva"] == ROOT and w45["api"] == "WriteFile",
         "cross-report root identity")
    need(len(c44["inherited_stack_effect_candidates"]) == 139,
         "R44 original bounded stack candidate scope")
    need(w45["actual_native_handle_buffer_count_return_or_io_proven"] is False,
         "R45 actual native effect")
    ident = w45["identity"]
    need(ident["kind"] == "memory_indirect" and
         ident["import_identity"]["name"] == "WriteFile" and
         ident["import_identity"]["iat_rva"] == 0x520A4 and
         ident["runtime_target_or_effects_proven"] is False,
         "R45 imported WriteFile identity")
    shapes = w45["direct_definition_shapes"]
    need(w45["direct_definitions_truncated"] is False and
         len(shapes) == w45["direct_definition_count"] == 9 and
         len(set(x["site_rva"] for x in shapes)) == 9 and
         all(x["site_rva"] < SITES[0][0] for x in shapes),
         "R45 pre-call definitions only; no forged postcall shape")
    need(len(w45["bounded_node_rvas"]) == 139 and
         SITES[0][0] in w45["bounded_node_rvas"] and
         SITES[1][0] in w45["bounded_node_rvas"],
         "R45 candidate graph includes both sites")

    records = []
    for site, after, prior in SITES:
        s = one(w28["api_sites"], lambda x: x["site_rva"] == site, "R28 WriteFile site")
        need(s["conditional_post_call_rva"] == after and
             s["prior_graph_site_reached"] is prior and
             s["actual_external_return_proven"] is False and
             s["site_in_candidate_graph"] is True and
             s["identity"]["import_identity"]["name"] == "WriteFile" and
             s["identity"]["import_identity"]["iat_rva"] == 0x520A4 and
             s["identity"]["runtime_target_or_effects_proven"] is False,
             "R28 site/earlier graph/unknown native result")
        q = one(w28["inputs"]["queries"],
                lambda x: x["site_rva"] == after and x["register"] == "eax",
                "R28 exact postcall EAX")
        need(q["actual_register_value_known"] is False and
             q["candidates_truncated"] is False and
             q["dependency_queries"] == [] and len(q["reaching_candidates"]) == 1 and
             q["reaching_candidates"][0] == {"origin": "unknown_call", "rva": site, "semantic": None},
             "R28 native EAX remains opaque")
        records.append({
            "site_rva":site,"post_call_rva":after,"prior_graph_site_reached":prior,
            "bounded_root_contains_site": True,"postcall_eax_source":"unknown_call",
            "instruction_at_postcall_verified_from_these_reports":False,
            "native_return_value_or_written_count_known":False,
        })
    return {
        "schema":SCHEMA,
        "source_git_blobs":{"R28":BLOBS[28],"R44":BLOBS[44],"R45":BLOBS[45]},
        "original_static_candidate_root_rva":ROOT,
        "graph_node_count":139,"graph_edge_count":156,
        "postcall_sites":records,
        "r44_structural_stack_candidates":139,
        "r45_first_write_precall_definition_rows":9,
        "r45_second_write_site_member_of_bounded_graph":True,
        "source_discovery_note":"R44 supplies bounded stack effects and R45 pre-call definitions; neither proves native post-call value or caller frame preservation.",
        "precise_missing_evidence":[
            "decode and independently pin operand/mnemonic/condition at R28 WriteFile postcall 0x4c692 and 0x4c6f7",
            "derive complete site-local branch successor and flag-definition inventory in 0x4c5b4, including feasible predecessors to each imported WriteFile",
            "separate native API return EAX from number-of-bytes-written pointer/alias and caller-visible byte count",
            "prove returning-CALL and register/stack/frame/memory-clobber assumptions between 0x4a683 -> 0x4c5b4 and 0x48c5e -> 0x4c5b4",
            "establish executable path, actual OS result and durable persistence only with separate evidence"
        ],
        "these_pinned_reports_reconstruct_complete_postcall_instruction_inventory":False,
        "actual_native_api_executed":False,
        "actual_call_return_or_frame_abi_memory_alias_proven":False,
        "actual_savedata_written_bytes_flush_close_or_persistence_proven":False,
        "next":"R62 narrowly scoped original-derived 0x4c5b4 postcall instruction/branch inventory only after source-custody and duplicate-evidence check"
    }

def inspect(raw):
    for number, content in raw.items():
        need(blob(content)==BLOBS[number], f"R{number} immutable Git blob")
    return derive(*(json.loads(raw[n]) for n in (28,44,45)))

def main():
    p=argparse.ArgumentParser()
    for n in (28,44,45):
        p.add_argument(f"--r{n}",type=Path,
                       default=Path(f"research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R{n}-ORIGINAL.json"))
    p.add_argument("--verify",type=Path)
    a=p.parse_args()
    out=inspect({n:getattr(a,f"r{n}").read_bytes() for n in (28,44,45)})
    if a.verify:
        need(out==json.loads(a.verify.read_text()),"contract replay mismatch")
        print("TW10_R61_POSTCALL_GAP_LEDGER=PASS; ORIGINAL_NATIVE_WRITE=OPEN")
    else:
        print(json.dumps(out,sort_keys=True))

if __name__=="__main__":
    main()
