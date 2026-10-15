"""R68: independent forward/reverse conservative EAX return-source candidates.

Unknown decoded rows and CALLs are barriers. Neither source algorithm carries
register or memory values across them. Graph reachability is not execution.
"""
import argparse
import hashlib
import json
from pathlib import Path

from tools.stoneage_tw10_savedata_r67_guard import BASE, validate

EAX_ALIASES = {"eax", "ax", "al", "ah"}
R67_SHA = "8bb5923de9a630a953de6c62cf9c10463aed9a4066db9a0aa97c7aaff338ab50"
R67_BLOB = "04162081d346b8c53424295de9fdc6b8f385b011"


def need(ok, why):
    if not ok:
        raise ValueError("R68 conservative source audit: " + why)


def killed(row, at):
    if row is None:
        return ("unknown_instruction", at)
    if row["mnemonic"] == "call":
        return ("opaque_call", at)
    writes = set(row["decoder_written_registers"])
    if writes & EAX_ALIASES:
        return ("full_eax_definition" if "eax" in writes else "partial_eax_unknown", at)
    return None


def reverse_sources(nodes, edges, rows, root, at):
    need(root in nodes and at in nodes, "reverse roots")
    incoming = {n: [] for n in nodes}
    for a, b in edges:
        incoming[b].append(a)
    pending = list(incoming[at])
    found = set()
    visited = set()
    if at == root:
        found.add(("unknown_entry", root))
    while pending:
        p = pending.pop()
        if p in visited:
            continue
        visited.add(p)
        barrier = killed(rows.get(p), p)
        if barrier:
            found.add(barrier)
        else:
            if p == root:
                found.add(("unknown_entry", root))
            pending.extend(incoming[p])
    return found


def forward_sources(nodes, edges, rows, root, at):
    """Separately traverse successors until a finite token-set fixed point."""
    before = {n: set() for n in nodes}
    before[root].add(("unknown_entry", root))
    after = {n: set() for n in nodes}
    for _ in range(len(nodes) + 2):
        changed = False
        for n in sorted(nodes):
            token = killed(rows.get(n), n)
            nxt = {token} if token else set(before[n])
            # No path from root means an unreachable component cannot invent a
            # reaching definition. The historical root graph is root-generated.
            if not before[n]:
                nxt = set()
            if nxt != after[n]:
                after[n] = nxt
                changed = True
            for a, b in edges:
                if a == n:
                    merged = before[b] | after[n]
                    if merged != before[b]:
                        before[b] = merged
                        changed = True
        if not changed:
            return before[at]
    raise ValueError("R68 conservative source audit: fixed-point bound")


def analyze(report):
    validate(report)
    nodes = set(report["bounded_graph_node_rvas"])
    edges = {tuple(e) for e in report["bounded_graph_edges"]}
    rows = {r["site_rva"]: r for r in report["decoded_instruction_rows"]}
    # Add already pinned R63 rows only; an absent row never becomes a no-op.
    prior = json.loads((BASE / "STONEAGE-TW10-SAVEDATA-POSTCALL-R63-DERIVED.json").read_bytes())
    for site in prior["sites"]:
        for r in site["decoded_instruction_rows"]:
            if r["site_rva"] in rows:
                need(rows[r["site_rva"]] == r, "overlapping prior rows")
            rows[r["site_rva"]] = r
    root, ret = 0x4C5B4, 0x4C760
    need(rows[ret]["mnemonic"] == "ret", "retained original RET")
    rev = reverse_sources(nodes, edges, rows, root, ret)
    fwd = forward_sources(nodes, edges, rows, root, ret)
    need(rev == fwd and bool(rev), "independent EAX source agreement")
    sources = [{"origin": kind, "site_rva": at,
                "decoded_definition": rows.get(at), "actual_eax_value_known": False}
               for kind, at in sorted(rev)]
    return {
        "schema": "tw10-r68-native-ret-conservative-eax-source-candidates",
        "source_r67_sha256": hashlib.sha256((json.dumps(report, sort_keys=True) + "\n").encode()).hexdigest(),
        "source_r67_git_blob": R67_BLOB,
        "root_rva": root, "ret_rva": ret,
        "bounded_graph_nodes": len(nodes), "bounded_graph_edges": len(edges),
        "available_decoded_rows_in_root": len(set(rows) & nodes),
        "missing_decoded_rows_are_opaque_barriers": True,
        "all_call_register_effects_are_opaque_barriers": True,
        "forward_and_reverse_source_sets_agree": True,
        "return_eax_source_candidates": sources,
        "original_actual_eax_or_native_bool_count_known": False,
        "actual_branch_path_frame_alias_or_preservation_proven": False,
        "actual_flush_close_or_disk_persistence_proven": False,
        "savedata_schema_or_server_authority_proven": False,
        "original_program_or_payload_executed": False,
        "stage_b_started": False,
    }


def inspect_raw(raw):
    need(hashlib.sha256(raw).hexdigest() == R67_SHA, "exact source R67 raw SHA256")
    need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == R67_BLOB, "source R67 Git blob")
    return analyze(json.loads(raw))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, default=BASE / "STONEAGE-TW10-SAVEDATA-NATIVE-TAIL-R67-ORIGINAL.json")
    p.add_argument("--verify", type=Path)
    a = p.parse_args()
    result = inspect_raw(a.report.read_bytes())
    if a.verify:
        need(result == json.loads(a.verify.read_bytes()), "exact source-candidate replay")
        print("TW10_R68_FORWARD_REVERSE_RETURN_SOURCES=PASS; ORIGINAL_NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
