"""Check the Stage A review manifest; optionally replay named existing suites.

This validates derived evidence and reference models, never original gameplay.
Only the Python standard library and committed repository files are required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "research/recovered/STONEAGE-STAGE-A-CONSOLIDATED-REVIEW-R1.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_relative(path: str) -> bytes:
    target = (ROOT / path).resolve()
    require(target.is_relative_to(ROOT), "path outside repository")
    return target.read_bytes()


def validate(packet: dict) -> dict:
    require(packet["schema"] == "stoneage.stage_a.consolidated_review.r1", "schema")
    require(packet["status"] == "READY_FOR_JOINT_REVIEW_NOT_STAGE_A_ACCEPTANCE", "review status")
    for flag in ("stage_a_accepted", "joint_user_review_completed", "stage_b_started",
                 "new_original_server_content", "original_playthrough_certified"):
        require(packet[flag] is False, f"unauthorized promotion: {flag}")
    require(packet["stage_b_gate"] == "GATED", "Stage B gate")
    require(packet["historical_restoration_percentage"] is None, "percentage without denominator")
    require(packet["savedata_r79"] == "PAUSED_NON_BLOCKING", "R79 work order")
    require(packet["next_priority"] == "STAGE-A-JOINT-REVIEW-01", "next review")
    require(packet["continue_without_explicit_design_decision"] == "STAGE_A_ONLY", "continue scope")

    pins = packet["source_pins"]
    require(len({pin["path"] for pin in pins.values()}) == len(pins), "duplicate source path")
    for key, pin in pins.items():
        body = read_relative(pin["path"])
        git_blob = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
        require((len(body), hashlib.sha256(body).hexdigest(), git_blob) ==
                (pin["bytes"], pin["sha256"], pin["git_blob"]), f"source custody: {key}")

    triage = json.loads(read_relative(pins["triage"]["path"]))
    portfolio = json.loads(read_relative(pins["portfolio"]["path"]))
    rows = packet["families"]
    require(len(rows) == 9 and len({r["id"] for r in rows}) == 9, "nine unique families")
    gates = {r["id"]: r["gate"] for r in rows}
    require(gates == triage["system_gates"] ==
            {r["id"]: r["gate"] for r in portfolio["families"]}, "family gate drift")
    require(packet["playflows"] == triage["integrated_playflow_profiles"], "playflow scope drift")
    require(packet["blockers"] == triage["blockers"], "blocker/reopen drift")
    for row in rows:
        require(all(row.get(k) for k in ("label", "usable_spec", "original_gap",
                    "source_refs", "replay_refs", "reopen")), f"incomplete family: {row['id']}")
        require(set(row["source_refs"]) <= pins.keys(), "unknown family source")

    prefixes = packet["preserved_historical_prefixes"]
    required_prefixes = {"README.md", "docs/PROJECT-CONTINUITY-PROTOCOL-R1.md",
                         "docs/CURRENT-STATE.md", "docs/DESIGN-DECISIONS.md",
                         "docs/HISTORICAL-TIMELINE.md", "docs/SOURCE-REGISTRY.md",
                         "docs/RESTORATION-ROADMAP-R2.md", "docs/RESTORATION-PHASE-GATE-R1.md"}
    require(len(prefixes) == len(required_prefixes) and
            {p["path"] for p in prefixes} == required_prefixes, "incomplete continuity inventory")
    for prefix in prefixes:
        old = read_relative(prefix["path"])[:prefix["bytes"]]
        require(len(old) == prefix["bytes"] and hashlib.sha256(old).hexdigest() ==
                prefix["sha256"], f"historical prefix changed: {prefix['path']}")

    replays = packet["replays"]
    require(len({r["id"] for r in replays}) == len(replays), "duplicate replay id")
    replay_ids = {r["id"] for r in replays}
    known_flows = {r["id"] for r in packet["playflows"]}
    covered = set()
    all_modules = []
    for row in replays:
        require(row["scope"] in {"DERIVED_EVIDENCE_AUDIT", "SYNTHETIC_REFERENCE_MODEL",
                                  "SOURCE_SHAPE_AND_SYNTHETIC_PROJECTION"}, "replay scope")
        require(row["original_game_execution"] is False, "original execution overclaim")
        require(bool(row["does_not_prove"]), "replay limitation absent")
        require(bool(row["playflow_refs"]) and set(row["playflow_refs"]) <= known_flows, "unknown flow")
        covered.update(row["playflow_refs"])
        require(bool(row["modules"]), "empty replay modules")
        for module in row["modules"]:
            require(re.fullmatch(r"tests\.test_stoneage_[a-z0-9_]+", module) is not None,
                    "invalid replay module")
            path = module.replace(".", "/") + ".py"
            require(path in {p["path"] for p in pins.values()}, "unpinned replay module")
            all_modules.append(module)
    require(covered == known_flows, "missing playflow review entry")
    require(len(all_modules) == len(set(all_modules)), "repeated replay module")
    for row in rows:
        require(set(row["replay_refs"]) <= replay_ids, "unknown family replay")

    doc = read_relative(packet["review_document"]).decode("utf-8")
    require(all(row["id"] in doc for row in rows), "review document misses family")
    for link in re.findall(r"\]\(([^)]+)\)", doc):
        if "://" not in link and not link.startswith("#"):
            target = (ROOT / packet["review_document"]).parent / link.split("#", 1)[0]
            require(target.resolve().is_relative_to(ROOT) and target.is_file(), f"broken review link: {link}")
    return {"status": "PASS", "families": len(rows), "source_pins": len(pins),
            "playflows": len(known_flows), "blockers": len(packet["blockers"]),
            "historical_prefixes": len(packet["preserved_historical_prefixes"]),
            "replay_groups": len(replays), "stage_a_accepted": False,
            "stage_b_gate": "GATED", "original_game_execution": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    try:
        packet = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = validate(packet)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
        if args.replay:
            for row in packet["replays"]:
                print(f"REPLAY {row['id']} | {row['scope']} | {row['does_not_prove']}", flush=True)
                subprocess.run([sys.executable, "-m", "unittest", *row["modules"], "-v"],
                               cwd=ROOT, check=True)
    except (KeyError, ValueError, OSError, TypeError, subprocess.CalledProcessError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
