"""R19: byte-verified bounded string candidates from the authentic TW1 retail runtime.
Research metadata only. No game executable, graphics, dialogue corpus, or scripts in Git.
A decoded C-string is not evidence of an in-game NPC, pet, quest, or screen.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

EXPECTED = {
    "StoneAge/sa_3.exe": (425984, "cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a"),
    "StoneAge/StoneAge.exe": (409600, "9b280068063b4398e5c8901b881daa1f13576201e475efede3127b59cdad2867"),
}
CSTRING = re.compile(rb"[\x20-\x7e\x80-\xff]{4,96}\x00")
ENCODINGS = ("cp950", "gb18030", "cp932")
MAX_SAMPLES = 64

def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def han_count(s: str) -> int:
    return sum(0x3400 <= ord(c) <= 0x9fff for c in s)

def bounded_candidates(data: bytes, max_samples: int = MAX_SAMPLES):
    if max_samples < 1 or max_samples > MAX_SAMPLES:
        raise ValueError("invalid bounded limit")
    rows = []
    positions = 0
    qualified = 0
    per_encoding = {x: 0 for x in ENCODINGS}
    seen = set()
    for m in CSTRING.finditer(data):
        positions += 1
        raw = m.group()[:-1]
        if not any(b >= 128 for b in raw):
            continue
        for enc in ENCODINGS:
            try:
                val = raw.decode(enc, "strict")
            except (UnicodeError, LookupError):
                continue
            if not (2 <= len(val) <= 32 and han_count(val) >= 2):
                continue
            if any((not c.isprintable()) for c in val):
                continue
            if han_count(val) / len(val) < 0.36:
                continue
            key = (m.start(), enc)
            if key in seen:
                raise AssertionError("duplicate byte position/encoding")
            seen.add(key)
            qualified += 1
            per_encoding[enc] += 1
            if len(rows) < max_samples:
                rows.append({
                    "source_file_offset": m.start(),
                    "byte_count": len(raw),
                    "source_bytes_sha256": digest(raw),
                    "source_candidate_codec": enc,
                    "decoded_short_label": val if len(val) <= 12 else None,
                    "source_nul_terminated": True,
                    "entity_id": None, "bitmap_id": None, "spr_group_id": None,
                    "npc_quest_pet_identity_qualified": False,
                })
    return {
        "nul_terminated_ascii_or_highbyte_windows": positions,
        "candidate_decode_occurrences": qualified,
        "candidate_by_codec": per_encoding,
        "sampling_limit": max_samples,
        "sampled_candidate_count": len(rows),
        "sampling_truncated": qualified > max_samples,
        "candidates": rows,
    }

def analyze_executables(named: dict[str, bytes]):
    if set(named) != set(EXPECTED):
        raise ValueError("both authenticated original executable paths required")
    out = {}
    for path, (length, sha) in EXPECTED.items():
        raw = named[path]
        if len(raw) != length or digest(raw) != sha:
            raise ValueError("original executable identity mismatch for " + path)
        out[path] = {"original_file_length": length, "original_sha256": sha, **bounded_candidates(raw)}
    return {
        "schema": "stoneage.tw10.original_executable_text_candidate.r19",
        "task": "EARLY-OFFICIAL-NAMED-CONTENT-SOURCE-19",
        "source_region_version": "TW_WAEI_JSS_RETAIL_1_0_REDUMP_104630",
        "method": "NUL_TERMINATED_CP950_GB18030_CP932_HEURISTIC_NOT_GAME_CONTENT_PROOF",
        "executable_observations": out,
        "original_executable_executed": False,
        "source_bytes_or_full_strings_embedded": False,
        "original_npc_pet_quest_identity_mappings_proven": 0,
        "actual_runtime_string_selection_proven": False,
        "early_official_server_master_acquired": False,
        "missing": [
            "An authenticated same-build NPC/pet/quest master with name + runtime ID + graphics/SPR key",
            "Or original TW1 runtime execution/selection proving a decoded client label is an actual in-game entity",
            "Or independently authenticated original operator patch/data payload with an exact named-entity to image/animation join",
        ],
        "outcome": "FINITE_ORIGINAL_BYTE_TEXT_SURFACE_OBSERVED_PROVENANCE_STILL_OPEN",
        "stage_a": "7 PARTIAL + 2 OPEN",
        "stage_b_and_wiki": "GATED",
        "savedata_r79": "PAUSED_NON_BLOCKING",
        "overall_restoration_percent": None,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--disc-image", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    from tools.stoneage_tw10_technical_probe import find_rows, extract_row
    image, rows, _, _ = find_rows(args.disc_image)
    try:
        members = {}
        with tempfile.TemporaryDirectory() as tmp:
            for path in EXPECTED:
                found = [r for r in rows if r["path"] == path and not r["is_dir"]]
                if len(found) != 1:
                    raise ValueError("missing/ambiguous original disc member " + path)
                target = Path(tmp) / Path(path).name
                extract_row(image, found[0], target)
                members[path] = target.read_bytes()
                target.unlink()
        result = analyze_executables(members)
    finally:
        image.close()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("R19_ORIGINAL_EXE_BYTES_IDENTITIES=PASS")
    for path, obs in result["executable_observations"].items():
        print("R19_CANDIDATES", path, obs["candidate_decode_occurrences"], obs["sampled_candidate_count"])
    print("R19_DERIVED_REPORT_SHA256=" + digest(args.output.read_bytes()))
    print("R19_NAMED_NPC_PET_QUEST_RESOURCE_JOIN=OPEN")

if __name__ == "__main__":
    main()
