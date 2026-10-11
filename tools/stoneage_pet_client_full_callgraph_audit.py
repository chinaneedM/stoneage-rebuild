"""Pinned Bismarck late-descendant client-wide optional PET sender audit.

Scans the *complete tracked client source tree* from an exact Git checkout,
not GitHub default-branch indexed search. Source-only: no production binary,
real user-input invocation, or first-release feature promotion is implied.
"""
from pathlib import Path
import argparse
import hashlib
import re
import subprocess

PINNED = "999ffdf1d220ec6666eb65339180689c9caf1876"
CLIENT_TREE = "511d9b24376c6858b70ab3015e36f5007bfd565a"
BLOBS = {
    "client/resources/version.h": "35bd4446a740a189c1ad9439e30e61fe169d5f46",
    "client/stoneage/proto/protocol.h": "bb70087ef1b1915748da23935584eda2c8178cb0",
    "client/stoneage/proto/protocol.cpp": "17f1900d8845c15308a4b429905ec009e5fd4c0f",
    "client/stoneage.vcxproj": "373c0699a5df017f53e4ab7a7d64c3d6280a8578",
    "server/common/gmsv_server.h": "708fe1b9f73be4952677fda474f10e86d9a56306",
    "server/gmsv/include/version.h": "b3fc0c80705973bc8d088287c98a5d66171bb6c2",
}
SOURCE_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".inl", ".inc"}
SYMBOL = re.compile(r"\blssproto_PetItemEquip_send\s*\(")
MARK = "RESOLUTION|PET_CLIENT_FULL_PINNED_SOURCE_ONLY_PASS"

def demand(condition, message):
    if not condition:
        raise ValueError(message)

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])

def file_sha(root, path):
    return git(root, "hash-object", path).decode().strip()

def preprocessor(root, options):
    header = root / "client/resources/version.h"
    p = subprocess.run(
        ["g++", "-dM", "-E", "-x", "c++", *options, "-include", str(header), "-"],
        input="", capture_output=True, text=True, check=True, timeout=40
    )
    return set(re.findall(r"(?m)^#define\s+([A-Za-z_]\w*)", p.stdout))

def check(root):
    demand(git(root, "rev-parse", "HEAD").decode().strip() == PINNED,
           "source repository is not pinned original descendant commit")
    demand(git(root, "rev-parse", "HEAD:client").decode().strip() == CLIENT_TREE,
           "complete pinned client tree identity changed")
    for path, expected in BLOBS.items():
        demand(file_sha(root, path) == expected, "pinned source drift " + path)

    version = (root / "client/resources/version.h").read_text(encoding="utf-8-sig")
    demand(bool(re.search(r"(?m)^#define\s+_SA_VERSION_25\b", version)),
           "checked-in header initial version changed")
    demand(bool(re.search(r"#ifdef\s+_SA_VERSION_80[\s\S]*?#define\s+_PET_ITEM\b", version)),
           "8.0 PET feature version guard changed")
    vcx = (root / "client/stoneage.vcxproj").read_text(encoding="utf-8-sig")
    definitions = re.findall(r"<PreprocessorDefinitions>(.*?)</PreprocessorDefinitions>", vcx, re.S)
    demand(len(definitions) == 2 and all(
        "_SA_VERSION_SPECIAL" in d.split(";") and "_SA_VERSION_80" not in d
        and "_PET_ITEM" not in d for d in definitions),
        "checked-in Windows client project Debug/Release PET version flags changed")

    header_only = preprocessor(root, [])
    special = preprocessor(root, ["-D_SA_VERSION_SPECIAL"])
    forced_eight = preprocessor(root, ["-D_SA_VERSION_SPECIAL", "-D_SA_VERSION_80"])
    demand("_SA_VERSION_25" in header_only and "_SA_VERSION_80" not in header_only
           and "_PET_ITEM" not in header_only,
           "header-only default unexpectedly enables PET feature")
    demand("_SA_VERSION_25" in special and "_SA_VERSION_60" in special
           and "_SA_VERSION_80" not in special and "_PET_ITEM" not in special,
           "checked-in VS special version incorrectly treated as version 8")
    demand("_SA_VERSION_80" in forced_eight and "_PET_ITEM" in forced_eight,
           "counterfactual version8 failed to enable conditional PET feature")

    client_h = (root / "client/stoneage/proto/protocol.h").read_text(errors="replace")
    client_cpp = (root / "client/stoneage/proto/protocol.cpp").read_text(errors="replace")
    server_h = (root / "server/common/gmsv_server.h").read_text(errors="replace")
    demand("#define LSSPROTO_PET_ITEM_EQUIP_SEND 127" in client_h and
           "#define LSSPROTO_PET_ITEM_RECV 127" in server_h and
           "util_SendMesg(fd, LSSPROTO_PET_ITEM_EQUIP_SEND, szBuffer)" in client_cpp,
           "conditional optional packet number or client serializer changed")

    all_paths = [p for p in git(root, "ls-files", "-z", "--", "client").decode().split("\0")
                 if p]
    source_paths = sorted(p for p in all_paths if Path(p).suffix.lower() in SOURCE_EXT)
    demand(len(source_paths) >= 200, "pinned client C/C++/header source inventory unexpectedly truncated")
    inventory = hashlib.sha256()
    sites = []
    for path in source_paths:
        blob = file_sha(root, path)
        inventory.update(f"{path}|{blob}\n".encode("utf-8"))
        lines = (root / path).read_text(encoding="utf-8-sig", errors="replace").splitlines()
        for n, line in enumerate(lines, 1):
            if SYMBOL.search(line):
                if path == "client/stoneage/proto/protocol.h" and re.search(
                    r"\bvoid\s+lssproto_PetItemEquip_send\s*\(", line):
                    kind = "declaration"
                elif path == "client/stoneage/proto/protocol.cpp" and re.search(
                    r"\bvoid\s+lssproto_PetItemEquip_send\s*\(", line):
                    kind = "definition"
                else:
                    kind = "lexical_call_candidate"
                sites.append((kind, path, n))

    demand(("declaration", "client/stoneage/proto/protocol.h", 462) in sites,
           "pinned sender header declaration location changed")
    demand(("definition", "client/stoneage/proto/protocol.cpp", 2280) in sites,
           "pinned sender implementation location changed")
    # A complete source scan can prove only absent *syntactic* callers here;
    # indirect/dynamic/generated/external invocation and deployed binary remain OPEN.
    demand(len(sites) == 2 and not any(s[0] == "lexical_call_candidate" for s in sites),
           "unexpected PET emitter lexical caller found: " + repr(sites))
    summary = (
        "SOURCE_PET_CLIENT_GATE|pinned_commit=" + PINNED
        + "|client_tree=" + CLIENT_TREE
        + "|client_project_blob=" + BLOBS["client/stoneage.vcxproj"]
        + "|tracked_client_source_files=" + str(len(source_paths))
        + "|lexical_sender_sites=" + str(len(sites))
        + "|lexical_caller_candidates=0"
        + "|header_default_pet=0|vs_special_pet=0|counterfactual_80_pet=1"
        + "|client_sender_opcode=127|server_receiver_opcode=127"
        + "|runtime_packet_verified=0|deployed_client_binary_verified=0"
        + "|early_build_verified=0|inventory_sha256=" + inventory.hexdigest())
    return [summary, *[
        f"SOURCE_PET_CLIENT_SITE|kind={kind}|path={path}|line={n}"
        for kind, path, n in sites],
        "BOUNDARY|Full pinned tracked client source lexical scan and checked-in VS project/header preprocessor gates only; zero proven user-triggered packet; no deployed binary; no JSS1999/Taiwan1.0 inference",
        "OPEN|external/generated runtime client dispatch, optional version8 build, matching enabled server binary, actual item-owner transitions, natural alias and unique codes",
        MARK]

def parse_line(line):
    parts = [x.split("=", 1) for x in line.split("|")[1:]]
    if not parts or any(len(x) != 2 for x in parts) or len(set(x[0] for x in parts)) != len(parts):
        raise ValueError("invalid duplicated/malformed audit data")
    return dict(parts)

def validate(report):
    lines = report.splitlines()
    if len(lines) != 6 or lines[-1] != MARK:
        raise ValueError("missing ordered full-tree PET acceptance and boundary")
    demand(lines[0].startswith("SOURCE_PET_CLIENT_GATE|"), "missing client gate")
    main = parse_line(lines[0])
    expected = {
        "pinned_commit": PINNED, "client_tree": CLIENT_TREE,
        "client_project_blob": BLOBS["client/stoneage.vcxproj"],
        "lexical_sender_sites": "2", "lexical_caller_candidates": "0",
        "header_default_pet": "0", "vs_special_pet": "0",
        "counterfactual_80_pet": "1",
        "client_sender_opcode": "127", "server_receiver_opcode": "127",
        "runtime_packet_verified": "0", "deployed_client_binary_verified": "0",
        "early_build_verified": "0",
    }
    demand(set(main) == set(expected) | {"tracked_client_source_files", "inventory_sha256"},
           "PET source summary schema drift")
    demand(all(main[k] == v for k, v in expected.items()), "source claim inflated or missing")
    demand(main["tracked_client_source_files"].isdigit() and
           int(main["tracked_client_source_files"]) >= 200 and
           bool(re.fullmatch(r"[a-f0-9]{64}", main["inventory_sha256"])),
           "invalid whole-client inventory")
    expected_sites = [
        {"kind": "declaration", "path": "client/stoneage/proto/protocol.h", "line": "462"},
        {"kind": "definition", "path": "client/stoneage/proto/protocol.cpp", "line": "2280"},
    ]
    demand([parse_line(line) for line in lines[1:3]] == expected_sites
           and all(line.startswith("SOURCE_PET_CLIENT_SITE|") for line in lines[1:3]),
           "pinned PET sender source sites missing or changed")
    demand(lines[3].startswith("BOUNDARY|") and
           "no JSS1999/Taiwan1.0 inference" in lines[3] and
           lines[4].startswith("OPEN|"), "missing non-promotion boundary")
    return main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkout", type=Path, required=True)
    args = ap.parse_args()
    report = "\n".join(check(args.checkout)) + "\n"
    validate(report)
    print(report, end="")

if __name__ == "__main__":
    main()
