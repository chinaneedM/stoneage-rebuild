"""Finite original-game *environment* test: two own x86 EXEs, no original payload.

Test Windows Server 2022 process-local zh-TW activeCodePage manifest.
The previously accepted P3E 8bpp palette/input gate does NOT automatically
transfer to the differently manifested process. Do not imply game launch.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess

SCHEMA = "stoneage.p3f.synthetic_process_acp_manifest.v1"
LAYERS = ("DEFAULT", "256COLOR", "WINXPSP3 256COLOR")
EXE_VARIANTS = ("plain_x86", "embedded_zh_tw_manifest")
STATUS_GO = "ACP950_AND_8BPP_SYNTHETIC_CANDIDATE_ONLY"
STATUS_BLOCKED = "PROCESS_ACP950_8BPP_NOT_YET_OBSERVED"


def candidate(report: dict) -> bool:
    cases = report["cases"]
    return any(
        pair["layer"] in ("256COLOR", "WINXPSP3 256COLOR")
        and pair["plain_x86"]["acp_before"] == 1252
        and pair["embedded_zh_tw_manifest"]["acp_before"] == 950
        and pair["embedded_zh_tw_manifest"]["acp_after_console950"] == 950
        and pair["embedded_zh_tw_manifest"]["display_bpp"] == 8
        and pair["embedded_zh_tw_manifest"]["ddraw_current"][2] == 8
        for pair in cases
    )


def validate(report: dict) -> bool:
    assert report["schema"] == SCHEMA
    assert report["original_client_downloaded"] is False
    assert report["original_client_executed"] is False
    assert report["world_entered"] is False
    assert report["palette_pixels_same_process_qualified"] is False
    assert report["mouse_input_same_process_qualified"] is False
    assert report["original_process_isolation_qualified"] is False
    assert report["original_server_contacted"] is False
    assert report["case_order"] == list(LAYERS)
    assert len(report["cases"]) == len(LAYERS)
    for item, layer in zip(report["cases"], LAYERS):
        assert item["layer"] == layer
        for variant in EXE_VARIANTS:
            data = item[variant]
            assert data["original_executed"] is False
            assert data["pointer_bytes"] == 4
            assert data["desktop_mode_changed"] is False
            assert data["cp950_installed"] is True
            assert data["cp950_sample_fallback"] is False
            assert data["cp950_sample_bytes"] == list("石器".encode("cp950"))
            assert data["acp_after_console950"] == data["acp_before"]
            assert data["ddraw_create"] == 0
            assert data["ddraw_current_result"] == 0
            assert data["ddraw_current"][2] == data["display_bpp"]
        # A manifest is not allowed to modify baseline identity or image architecture.
        assert item["plain_x86"]["pointer_bytes"] == item["embedded_zh_tw_manifest"]["pointer_bytes"]
    possible = candidate(report)
    assert report["synthetic_acp950_8bpp_candidate"] is possible
    assert report["status"] == (STATUS_GO if possible else STATUS_BLOCKED)
    return possible


def collect(exe: Path, compat: str) -> dict:
    env = os.environ.copy()
    env.pop("__COMPAT_LAYER", None)
    if compat != "DEFAULT":
        env["__COMPAT_LAYER"] = compat
    process = subprocess.run(
        [str(exe.resolve())], env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=35, check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(f"own x86 program failed rc={process.returncode}; {process.stderr[:240]}")
    return json.loads(process.stdout.strip())


def run(baseline: Path, manifested: Path) -> dict:
    assert baseline.resolve() != manifested.resolve(), "two distinct program images required"
    report = {
        "schema": SCHEMA,
        "description": "Only own synthetic x86 process-local manifest experiment",
        "case_order": list(LAYERS),
        "cases": [],
        "original_client_downloaded": False,
        "original_client_executed": False,
        "world_entered": False,
        "original_server_contacted": False,
        "palette_pixels_same_process_qualified": False,
        "mouse_input_same_process_qualified": False,
        "original_process_isolation_qualified": False,
        "status": STATUS_BLOCKED,
        "synthetic_acp950_8bpp_candidate": False,
    }
    for layer in LAYERS:
        report["cases"].append({
            "layer": layer,
            "plain_x86": collect(baseline, layer),
            "embedded_zh_tw_manifest": collect(manifested, layer),
        })
    report["synthetic_acp950_8bpp_candidate"] = candidate(report)
    report["status"] = STATUS_GO if report["synthetic_acp950_8bpp_candidate"] else STATUS_BLOCKED
    validate(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--manifested", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    if args.check:
        existing = json.loads(args.check.read_text(encoding="utf-8"))
        validate(existing)
        print("P3F_SYNTHETIC_MANIFEST_REPORT_REPLAY=PASS", existing["status"])
    else:
        if not (args.baseline and args.manifested and args.output):
            parser.error("baseline, manifested and output are all required")
        result = run(args.baseline, args.manifested)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print("P3F_SYNTHETIC_MANIFEST_PROBE=", result["status"])


if __name__ == "__main__":
    main()
