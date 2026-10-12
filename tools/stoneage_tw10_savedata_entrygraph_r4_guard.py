#!/usr/bin/env python3
"""Strict JSON contract for derived TW1.0 R4 entrypoint graph reports.

No original payload is read or executed. The report is insufficient by itself
to establish dynamic reachability or ownership of the savedata.dat string.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

RUNTIME_SHA = "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"
SAVEDATA_SHA = "5b26f54a9723cd2c5275f964457094fdf1fc33ca086cdaf55bb5350dfb04f3f9"
WORDS = ("0x40065", "0x400e5", "0x40116", "0x402a1")
STARTS = ("0x40064", "0x400e4", "0x40115", "0x402a0")
MAX_INPUT = 9000
MAX_NODES = 120000
MAX_EDGES = 240000
TOP = {
    "schema", "scope", "runtime_sha256", "savedata_sha256",
    "entry_rva", "text_rva", "text_raw_size", "entry_in_text",
    "graph_limit_hit", "graph_statistics", "sites",
    "original_runtime_reachability_admitted", "savedata_io_semantics_admitted",
    "fixed_128_byte_schema_admitted", "original_bytes_published",
}
SITE = {
    "word_rva", "push_candidate_start_rva", "entrypoint_graph_candidate_seen",
    "entrypoint_graph_word_overlap_count", "entrypoint_graph_incoming_edges",
    "independently_proven_executed_code", "data_ownership_proven",
}
STATS = {
    "entry_outside_text", "outside_text", "decode_failure",
    "terminal_instruction", "indirect_transfer",
    "branch_target_outside_text", "fallthrough_outside_text",
    "decoded_nodes", "direct_or_fallthrough_edges", "pending_at_stop",
}


def nonnegative(n, limit):
    if type(n) is not int or not 0 <= n <= limit:
        raise ValueError("invalid integer bound")
    return n


def address(s):
    if not isinstance(s, str) or not re.fullmatch(r"0x[0-9a-f]{1,8}", s):
        raise ValueError("invalid hexadecimal RVA")
    return int(s, 16)


def validate(report: str):
    if len(report.encode("utf-8")) > MAX_INPUT:
        raise ValueError("oversized derived metadata")
    try:
        data = json.loads(report)
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid JSON report") from exc
    if not isinstance(data, dict) or set(data) != TOP:
        raise ValueError("invalid R4 report schema")
    if (data["schema"] != "tw10-savedata-four-word-entrygraph-r4"
            or data["scope"] != "verified-original-bytes-bounded-entrypoint-direct-graph"):
        raise ValueError("unrecognized source report scope")
    if data["runtime_sha256"] != RUNTIME_SHA or data["savedata_sha256"] != SAVEDATA_SHA:
        raise ValueError("source hash identity mismatch")
    for name in ("entry_in_text", "graph_limit_hit",
                 "original_runtime_reachability_admitted",
                 "savedata_io_semantics_admitted",
                 "fixed_128_byte_schema_admitted", "original_bytes_published"):
        if type(data[name]) is not bool:
            raise ValueError("invalid boolean")
    for name in ("original_runtime_reachability_admitted",
                 "savedata_io_semantics_admitted",
                 "fixed_128_byte_schema_admitted", "original_bytes_published"):
        if data[name]:
            raise ValueError("unjustified original-runtime promotion")
    entry_rva = address(data["entry_rva"])
    text_rva = address(data["text_rva"])
    text_len = nonnegative(data["text_raw_size"], 425984)
    if not text_len or text_rva+text_len > 0xffffffff:
        raise ValueError("invalid executable text bounds")
    actual_entry_inside = text_rva <= entry_rva < text_rva+text_len
    if actual_entry_inside != data["entry_in_text"]:
        raise ValueError("incorrect original entry/text relation")
    stats = data["graph_statistics"]
    if not isinstance(stats, dict) or not set(stats) <= STATS:
        raise ValueError("unrecognized graph statistics")
    for value in stats.values():
        nonnegative(value, MAX_EDGES)
    nodes = stats.get("decoded_nodes",0)
    edges = stats.get("direct_or_fallthrough_edges",0)
    nonnegative(nodes, MAX_NODES)
    nonnegative(edges, MAX_EDGES)
    if data["entry_in_text"] and ("decoded_nodes" not in stats or "direct_or_fallthrough_edges" not in stats):
        raise ValueError("missing graph totals")
    if not data["entry_in_text"] and (nodes or edges or stats.get("entry_outside_text") != 1):
        raise ValueError("entrypoint-outside-text report inconsistent")
    sites = data["sites"]
    if not isinstance(sites, list) or len(sites) != 4:
        raise ValueError("exact original four-site report required")
    for index, site in enumerate(sites):
        if not isinstance(site, dict) or set(site) != SITE:
            raise ValueError("invalid site row schema")
        if (site["word_rva"] != WORDS[index] or
                site["push_candidate_start_rva"] != STARTS[index]):
            raise ValueError("unexpected original candidate site")
        for flag in ("entrypoint_graph_candidate_seen",
                     "independently_proven_executed_code", "data_ownership_proven"):
            if type(site[flag]) is not bool:
                raise ValueError("invalid site boolean")
        if site["independently_proven_executed_code"] or site["data_ownership_proven"]:
            raise ValueError("unjustified code/data ownership promotion")
        overlap = nonnegative(site["entrypoint_graph_word_overlap_count"],MAX_NODES)
        incoming = nonnegative(site["entrypoint_graph_incoming_edges"],MAX_EDGES)
        if overlap > nodes or incoming > edges:
            raise ValueError("graph site count exceeds graph totals")
        if site["entrypoint_graph_candidate_seen"] and overlap < 1:
            raise ValueError("observed candidate requires instruction overlap")
        if not data["entry_in_text"] and (overlap or incoming or site["entrypoint_graph_candidate_seen"]):
            raise ValueError("outside entrypoint cannot observe candidate")
    return {
        "schema":"tw10-entrygraph-r4-strict-derived-guard-r1",
        "status":"DERIVED_STATIC_GRAPH_ONLY",
        "word_sites":4,
        "entry_in_text":data["entry_in_text"],
        "graph_limit_hit":data["graph_limit_hit"],
        "graph_nodes":nodes,
        "graph_edges":edges,
        "observed_candidate_starts":sum(int(s["entrypoint_graph_candidate_seen"]) for s in sites),
        "native_runtime_proven":False,
        "actual_data_ownership_proven":False,
        "contains_original_payload":False,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(validate(args.report.read_text(encoding="utf-8")), sort_keys=True))


if __name__ == "__main__":
    main()
