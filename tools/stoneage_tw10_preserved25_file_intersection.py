"""Replay a bounded TW1.0 <-> preserved-2.5 SHA256 metadata intersection.

Uses historical derived file manifests already versioned in Git.
Does NOT download/inspect original client bytes or certify a clean 2.5 distribution.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TW = "research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt"
BRIDGE = "research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt"
REPORT = "research/recovered/STONEAGE-TW10-PRESERVED25-FILE-SHA-INTERSECTION-R1.json"
GIT_BLOBS = {
    TW: "564233902b10c60760d4f93b1ea65d4dd1469206",
    BRIDGE: "78e8260e89928df76513799511d45c14a9e24dfc",
}
TW_CORE = re.compile(
    r"^CORE_FILE\|category=([^|]+)\|path=StoneAge/(.*?)\|size=(\d+)\|sha256=([0-9a-f]{64})$")
BRIDGE_HASH = re.compile(r"^([0-9a-f]{64})  (.+)$")
BRIDGE_ROOT = "/SA2.5主程式/stoneage2.5/"


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def replay():
    contents = {}
    for path, expected in GIT_BLOBS.items():
        raw = (ROOT / path).read_bytes()
        if git_blob(raw) != expected:
            raise ValueError("source Git blob changed: " + path)
        contents[path] = raw.decode("utf-8")
    tw = []
    for line in contents[TW].splitlines():
        m = TW_CORE.fullmatch(line)
        if m:
            cat, path, size, sha = m.groups()
            tw.append({"path": path, "category": cat, "size": int(size), "sha256": sha})
    index = {}
    after_marker = False
    bridge_rows = 0
    for line in contents[BRIDGE].splitlines():
        if line == "ALL-FILE SHA256":
            after_marker = True
            continue
        if not after_marker:
            continue
        m = BRIDGE_HASH.fullmatch(line)
        if m and BRIDGE_ROOT in m.group(2):
            sha, path = m.groups()
            bridge_rows += 1
            index.setdefault(sha, []).append(path.split(BRIDGE_ROOT, 1)[1])
    matches = [{**item, "bridge_paths": index[item["sha256"]]} for item in tw
               if item["sha256"] in index]
    unmatched = [item for item in tw if item["sha256"] not in index]
    bycat = {}
    for x in tw:
        c = bycat.setdefault(x["category"], {
            "original_core_files": 0, "sha256_matched_core_files": 0,
            "sha256_unmatched_core_files": 0, "matched_original_bytes": 0})
        c["original_core_files"] += 1
        if x["sha256"] in index:
            c["sha256_matched_core_files"] += 1
            c["matched_original_bytes"] += x["size"]
        else:
            c["sha256_unmatched_core_files"] += 1
    return {
        "counts": {
            "original_core_file_count": len(tw),
            "bridge_client_subtree_file_count": bridge_rows,
            "original_core_matched_files": len(matches),
            "original_core_unmatched_files": len(unmatched),
            "matched_cross_archive_path_occurrences": sum(len(x["bridge_paths"]) for x in matches),
            "original_core_matched_byte_sum": sum(x["size"] for x in matches)},
        "by_original_file_category": bycat,
        "matched": matches, "unmatched": unmatched}


def validate():
    expected = json.loads((ROOT / REPORT).read_text(encoding="utf-8"))
    actual = replay()
    for field, value in actual.items():
        if expected[field] != value:
            raise ValueError("existing derived report drift: " + field)
    if expected["sources"]["tw10_git_blob"] != GIT_BLOBS[TW] or \
            expected["sources"]["bridge25_git_blob"] != GIT_BLOBS[BRIDGE]:
        raise ValueError("source provenance mismatch")
    if actual["counts"] != {
        "original_core_file_count": 383,
        "bridge_client_subtree_file_count": 2302,
        "original_core_matched_files": 235,
        "original_core_unmatched_files": 148,
        "matched_cross_archive_path_occurrences": 237,
        "original_core_matched_byte_sum": 3882018}:
        raise ValueError("unexpected counts")
    if any(expected["boundaries"][name] for name in (
        "tw10_original_server_data_recovered",
        "bridge25_clean_official_distribution_proven",
        "cross_version_pet_species_identity_proven",
        "all_quest_data_recovered",
        "source_bytes_newly_downloaded_this_run")):
        raise ValueError("unsupported historical claim")
    return actual["counts"]


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "counts": validate()}, sort_keys=True))
