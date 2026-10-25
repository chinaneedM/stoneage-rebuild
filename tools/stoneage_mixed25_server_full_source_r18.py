"""R18 lossless retained-source server file conservation, never a first-party server certification.

Replays two Git-blob-pinned records from one mixed/community saved bundle.
No proprietary script or original game binary bytes are reproduced.
"""
from __future__ import annotations
from collections import defaultdict
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json"
STATIC = "research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt"
GAME = "research/recovered/STONEAGE-25-GAMEPLAY-DATA-INVENTORY-R1.txt"
STATIC_BLOB = "78e8260e89928df76513799511d45c14a9e24dfc"
GAME_BLOB = "47157f638cce7023727035981da11f1faecc9c78"
PACK_SHA = "d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"
PREFIX = "/SA2.5服務端/gmsv/data/"
MASTER_NAMES = (
    "enemy.txt", "enemy2.txt", "enemybase.txt", "enemybase2.txt",
    "enemy1.txt", "enemybase1.txt", "group.txt", "group1.txt",
    "encount.txt", "ride.txt", "petskill.txt", "petskill1.txt",
    "npc/100/sb_kbu.arg",
)
PRIOR_MISSING = (
    "appear.txt", "autopk/autopkaward.txt", "autopk/autopkhistory.txt",
    "clean", "contract.txt", "DEADJOE", "effect.txt", "gmset.txt",
    "group.txt", "group1.txt", "history.txt", "inv.txt", "malayfia.txt",
    "raceman.txt", "racequiz.txt", "ride.txt", "titleconfig.txt",
    "titlename.txt",
)

def ensure(ok, detail):
    if not ok:
        raise ValueError(detail)

def git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def load_sources():
    static = (ROOT / STATIC).read_bytes()
    game = (ROOT / GAME).read_bytes()
    ensure(git_blob(static) == STATIC_BLOB, "source full-static Git blob changed")
    ensure(git_blob(game) == GAME_BLOB, "source candidate Git blob changed")
    return static.decode("utf-8"), game.decode("utf-8")

def parse(static, game):
    ensure("ALL-FILE SHA256" in static and PACK_SHA in static, "saved parent chain missing")
    digests = {}
    for line in static.splitlines():
        if not re.match(r"^[0-9a-f]{64}  /tmp/sa25/out/", line):
            continue
        if PREFIX not in line:
            continue
        rel = line.split(PREFIX,1)[1]
        ensure(rel and rel not in digests and ".." not in rel.split("/"), "duplicate/unsafe full-source path")
        digests[rel] = line[:64]
    candidates = {}
    server = []
    for line in game.splitlines():
        if line.startswith("CANDIDATE|server|"):
            bits = line.split("|")
            ensure(len(bits)==7 and bits[3] not in candidates, "prior candidate schema/double path")
            candidates[bits[3]] = dict(tags=bits[2],size=int(bits[4]),sha256=bits[6])
        if line.startswith("SERVER_FILE|"):
            bits = line.split("|")
            ensure(len(bits)==4, "full server path schema")
            rel,size,ext = bits[1],int(bits[2]),bits[3]
            sha = digests.get(rel)
            ensure(sha is not None and re.fullmatch(r"[0-9a-f]{64}",sha), "unmatched source physical hash: "+rel)
            old = candidates.get(rel)
            if old:
                ensure(old["size"]==size and old["sha256"]==sha, "source candidate not equal to full parent physical hash: "+rel)
            server.append(dict(path=rel,size=size,extension=ext,sha256=sha,
                               prior_candidate_tags=old["tags"] if old else None,
                               prior_candidate_selected=old is not None))
    ensure(len(candidates)==2227 and len(server)==2245, "source row counts unexpected")
    ensure(len({x["path"] for x in server})==2245, "source duplicated logical paths")
    ensure(all(k in {r["path"] for r in server} for k in candidates), "unmatched earlier selected candidate")
    return server, candidates

def build():
    static,game=load_sources()
    files,candidates=parse(static,game)
    omitted=[r for r in files if not r["prior_candidate_selected"]]
    groups=defaultdict(list)
    for f in files:
        groups[f["sha256"]].append(dict(path=f["path"],size=f["size"]))
    dup=[dict(sha256=k,occurrences=v) for k,v in sorted(groups.items()) if len(v)>1]
    file_by_path={r["path"]:r for r in files}
    master=[dict(relative_path=key,in_full_original_tree=key in file_by_path,
                 in_prior_candidate_subset=key in candidates,
                 bytes=file_by_path[key]["size"] if key in file_by_path else None,
                 sha256=file_by_path[key]["sha256"] if key in file_by_path else None)
            for key in MASTER_NAMES]
    return {
        "schema":"stoneage.mixed25.server_full_source_conservation.r18",
        "date":"2026-10-25",
        "work_package":"EARLY-OFFICIAL-SERVER-MASTER-DATA-SOURCE-18_OR_EXACT_DOWNLOAD_PAYLOAD_CARRIER",
        "source_claim":"ARCHIVED_MIXED_COMMUNITY_PRESERVATION_ACTUAL_FILE_HASHES_NOT_OFFICIAL_RELEASE",
        "source_parent":{
            "source_url":"https://www.lab.welovesa.com/viewthread.php?extra=&page=1&tid=219",
            "source_date_context":"2012-04-07/08 preservation/service dates, NOT official launch",
            "source_package_size":361255180,
            "source_package_sha256":PACK_SHA,
            "static_inventory_path":STATIC, "static_inventory_git_blob":STATIC_BLOB,
            "gameplay_inventory_path":GAME, "gameplay_inventory_git_blob":GAME_BLOB,
            "payload_downloaded_this_round":False,
            "source_files_deleted":False},
        "summary":{
            "server_all_files":len(files),
            "server_all_bytes":sum(r["size"] for r in files),
            "prior_gameplay_candidate_rows":len(candidates),
            "prior_candidate_bytes":sum(r["size"] for r in files if r["prior_candidate_selected"]),
            "prior_unselected_but_original_file_rows":len(omitted),
            "prior_unselected_but_original_file_bytes":sum(r["size"] for r in omitted),
            "all_file_hash_crosschecks_missing":0,
            "prior_candidate_sha_conflicts":0,
            "content_sha256_unique":len(groups),
            "content_sha256_repeated_groups":len(dup),
            "content_sha256_duplicate_occurrence_excess":len(files)-len(groups),
            "extracted_real_bytes_deleted":0,
            "npc_subtree_file_count":sum(r["path"].startswith("npc/") for r in files),
            "early_official_server_roster_restored":0,
            "early_official_quest_master_restored":0,
            "early_official_pet_species_restored":0},
        "vocabulary_boundary":{
            "namespaces_proven_not_compatible":"MIXED25 old enemy/enemybase filename namespace is not evidence of 2012 GMSV enemy1/enemybase1 or early official TW10 release; numeric IDs cannot cross these scopes",
            "quest_origin_policy":"BASE_GAME_QUEST/PERMANENT_VERSION_QUEST/OPERATOR_EVENT_QUEST/ORIGIN_UNRESOLVED",
            "file_path_tokens_are_not_quest_event_classification":True,
            "client_download_patch_218_219_bytes_acquired":False,
            "source_is_clean_official_build":False},
        "master_presence":master,
        "omitted_from_previous_candidate":omitted,
        "duplicate_content_groups":dup,
        "all_server_occurrences":files
    }

def validate(doc):
    source=build()
    ensure(doc==source, "entire R18 derived index differs from two exact archived source files")
    stats=doc["summary"]
    ensure((stats["server_all_files"],stats["server_all_bytes"],
      stats["prior_gameplay_candidate_rows"],stats["prior_unselected_but_original_file_rows"],
      stats["prior_unselected_but_original_file_bytes"],stats["content_sha256_unique"],
      stats["content_sha256_repeated_groups"],stats["content_sha256_duplicate_occurrence_excess"])
      ==(2245,10465523,2227,18,731424,2121,53,124),"conservation stats")
    ensure([r["path"] for r in doc["omitted_from_previous_candidate"]]==list(PRIOR_MISSING),
           "not all omitted source files retained in correct original order")
    presence={x["relative_path"]:x for x in doc["master_presence"]}
    ensure(all(not presence[p]["in_full_original_tree"] for p in ("enemy1.txt","enemybase1.txt")),
           "foreign later enemy1 master injected")
    ensure(all(presence[p]["in_full_original_tree"] for p in ("group.txt","group1.txt","ride.txt")),
           "source file omitted again")
    ensure(not doc["vocabulary_boundary"]["source_is_clean_official_build"] and
           not doc["vocabulary_boundary"]["client_download_patch_218_219_bytes_acquired"],
           "community archive / 2001 patch misattribution")
    ensure(stats["early_official_pet_species_restored"]==
           stats["early_official_quest_master_restored"]==
           stats["early_official_server_roster_restored"]==0,
           "unverified early original NPC pet quest upgrade")
    return doc

if __name__=="__main__":
    v=validate(json.loads(OUTPUT.read_bytes()))
    print(json.dumps(v["summary"],sort_keys=True))
