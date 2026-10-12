#!/usr/bin/env python3
"""Strict, no-original-payload validator for TW1.0 R5 derived static metadata."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from tools.stoneage_tw10_savedata_instruction_probe import (
    RUNTIME_SHA256, SAVEDATA_SHA256, WORD_RVAS
)
from tools.stoneage_tw10_savedata_probe import FILE_APIS

MAX_REPORT = 18000
MAX_LOCAL = 256
MAX_RANGE = 2048
MAX_GRAPH = 31665
MAX_EDGES = 35092
MAX_EVENTS = 30
TOP_FIELDS = {
    "schema", "status", "original_runtime_sha256", "original_savedata_sha256",
    "entry_rva", "r4_graph_nodes", "r4_graph_edges", "r4_graph_limit_hit",
    "sites", "filename_argument_to_CreateFileA_proven",
    "ReadFile_WriteFile_buffer_size_proven", "native_save_io_executed",
    "original_bytes_published",
}
SITE_FIELDS = {
    "word_rva", "push_candidate_start_rva", "entrypoint_graph_min_hops",
    "predecessors", "local_graph", "actual_path_feasibility_proven",
    "filename_argument_to_file_api_proven", "native_read_write_size_proven",
}
PREDECESSORS = {"incoming_total", "incoming_sequential", "incoming_branch"}
LOCAL_GRAPH = {
    "visited_local", "limit_hit", "api_events",
    "api_counts", "createfilea_lexical_present"
}
API_EVENT = {"rva", "api", "dll"}
SAFE_DLL = re.compile(r"^[A-Za-z0-9_.-]{1,40}\.dll$",re.I)


def limited_int(n, maximum):
    if type(n) is not int or not 0 <= n <= maximum:
        raise ValueError("invalid bounded integer")
    return n


def parse_rva(v):
    if not isinstance(v,str) or not re.fullmatch(r"0x[0-9a-f]{1,8}",v):
        raise ValueError("invalid RVA field")
    return int(v,16)


def validate(text: str):
    if len(text.encode("utf-8")) > MAX_REPORT:
        raise ValueError("oversized report")
    try:
        root=json.loads(text)
    except (TypeError,ValueError) as exc:
        raise ValueError("invalid JSON document") from exc
    if not isinstance(root,dict) or set(root) != TOP_FIELDS:
        raise ValueError("R5 report schema mismatch")
    if root["schema"] != "stoneage-tw10-savedata-r5-static-api-neighborhood":
        raise ValueError("R5 report source schema mismatch")
    if root["status"] != "PINNED_ORIGINAL_STATIC_SURFACE_NOT_NATIVE_IO":
        raise ValueError("historical status improperly promoted")
    if (root["original_runtime_sha256"] != RUNTIME_SHA256
            or root["original_savedata_sha256"] != SAVEDATA_SHA256):
        raise ValueError("unrecognized original hashes")
    if parse_rva(root["entry_rva"]) != 0x4980a:
        raise ValueError("original PE entrypoint mismatch")
    if limited_int(root["r4_graph_nodes"],MAX_GRAPH) != MAX_GRAPH or (
            limited_int(root["r4_graph_edges"],MAX_EDGES) != MAX_EDGES):
        raise ValueError("accepted original R4 graph mismatch")
    for name in ("r4_graph_limit_hit", "filename_argument_to_CreateFileA_proven",
                 "ReadFile_WriteFile_buffer_size_proven","native_save_io_executed",
                 "original_bytes_published"):
        if type(root[name]) is not bool:
            raise ValueError("invalid original evidence boolean")
        if root[name]:
            raise ValueError("unjustified native/graph promotion")
    sites = root["sites"]
    if not isinstance(sites,list) or len(sites) != 4:
        raise ValueError("four sites required")
    named_api_rows = 0
    site_summaries = []
    for i,site in enumerate(sites):
        if not isinstance(site,dict) or set(site) != SITE_FIELDS:
            raise ValueError("R5 site fields mismatch")
        if (parse_rva(site["word_rva"]) != WORD_RVAS[i] or
                parse_rva(site["push_candidate_start_rva"]) != WORD_RVAS[i]-1):
            raise ValueError("unexpected original x86 word candidate")
        hops=limited_int(site["entrypoint_graph_min_hops"],MAX_GRAPH)
        preds=site["predecessors"]
        if not isinstance(preds,dict) or set(preds)!=PREDECESSORS:
            raise ValueError("invalid predecessor schema")
        for value in preds.values():
            limited_int(value,MAX_EDGES)
        if preds["incoming_total"] != preds["incoming_sequential"]+preds["incoming_branch"] or preds["incoming_total"] == 0:
            raise ValueError("graph predecessor counts inconsistent")
        g=site["local_graph"]
        if not isinstance(g,dict) or set(g) != LOCAL_GRAPH:
            raise ValueError("invalid local graph schema")
        visited=limited_int(g["visited_local"],MAX_LOCAL)
        if visited < 1 or type(g["limit_hit"]) is not bool or type(g["createfilea_lexical_present"]) is not bool:
            raise ValueError("invalid local graph presence flags")
        events=g["api_events"]
        counts=g["api_counts"]
        if not isinstance(events,list) or len(events)>MAX_EVENTS or not isinstance(counts,dict):
            raise ValueError("unbounded API list or counts")
        identified=Counter()
        unique=set()
        for event in events:
            if not isinstance(event,dict) or set(event) != API_EVENT:
                raise ValueError("unexpected API event fields")
            api=event["api"]
            dll=event["dll"]
            if api not in FILE_APIS or not isinstance(dll,str) or not SAFE_DLL.fullmatch(dll):
                raise ValueError("unknown original API metadata")
            pos=parse_rva(event["rva"])
            start=WORD_RVAS[i]-1
            if not start <= pos < start+MAX_RANGE:
                raise ValueError("event outside candidate neighborhood")
            key=(pos,dll.lower(),api)
            if key in unique:
                raise ValueError("duplicate file API event")
            unique.add(key)
            identified[api]+=1
        if dict(identified)!=counts:
            raise ValueError("API counts do not match events")
        if len(events)>visited:
            raise ValueError("API event count exceeds graph starts")
        if g["createfilea_lexical_present"] != (counts.get("CreateFileA",0)>0):
            raise ValueError("CreateFileA lexical indicator mismatch")
        for flag in ("actual_path_feasibility_proven",
                     "filename_argument_to_file_api_proven",
                     "native_read_write_size_proven"):
            if type(site[flag]) is not bool or site[flag]:
                raise ValueError("unjustified native path/argument promotion")
        named_api_rows += len(events)
        site_summaries.append({"word_rva":site["word_rva"],
                               "min_graph_hops":hops,
                               "incoming_total":preds["incoming_total"],
                               "local_file_api_events":len(events),
                               "lexical_createfilea":g["createfilea_lexical_present"]})
    return {
        "schema":"stoneage-tw10-r5-strict-static-report-guard",
        "status":"ACCEPTED_FORMAT_AND_STATIC_COUNTS_ONLY",
        "verified_original_identity":True,
        "site_count":4,
        "api_events":named_api_rows,
        "sites":site_summaries,
        "native_io_semantics_admitted":False,
        "dataflow_argument_proven":False,
        "contains_original_payload":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(validate(args.report.read_text(encoding="utf-8")),sort_keys=True))


if __name__=="__main__":
    main()
