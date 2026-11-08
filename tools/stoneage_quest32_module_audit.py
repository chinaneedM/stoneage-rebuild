"""QUEST32: audit public QUEST08-31 selected scripts against the original QUEST01 census.

This checks publication metadata and SHA joins, not private bytes, gameplay,
historical deployment, or a complete inventory of all possible quests.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = Path("research/recovered")
CATALOG = "STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json"
CATALOG_BLOB = "52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2"
SNAPSHOT = "STONEAGE-QUEST32-MODULE-DEDUPE-AUDIT-R1.json"

# Script-bearing keys vary between original source reports. Preserve this
# explicit schema mapping rather than guessing or counting unrelated rows.
SPECS = (
    ("08", "MINING-APPRAISAL-AND-LIMITSHOP-SOURCE", "source_scripts"),
    ("09", "DREAM-CAVE-ORIGINAL-CONTROLS", "source_event_scripts"),
    ("10", "QUARRY-SPIRITS-ORIGINAL-SOURCE", "source_event_scripts"),
    ("11", "TWO-TRIBES-ORIGINAL-SOURCE", "source_event_scripts"),
    ("12", "MINING-COMPETITION-ORIGINAL-SOURCE", "scripts"),
    ("13", "GOA-ULI-LETTERS-ORIGINAL-SOURCE", "scripts"),
    ("14", "DRAGON-NEST-ORIGINAL-SOURCE", "scripts"),
    ("15", "BANDIT-EVENT20-ORIGINAL-SOURCE", "original_scripts"),
    ("16", "AXE-WOOD-SOURCE", "source_event_blocks"),
    ("17", "DINO-RANCH-SOURCE", "source_scripts"),
    ("18", "GIIRU-SINK-SOURCE", "original_script_rows"),
    ("19", "MARJU-POST-TREASUREBAG-SOURCE", "original_scripts"),
    ("20", "FIVE-BROTHERS-MODULE-REVIEW", "original_scripts"),
    ("21", "LIULI-ORIGINAL-SOURCE-COMPARISON", "source_scripts"),
    ("22", "HEKISEI-ORIGINAL-SOURCE-AND-THREE-SCENES", "source_scripts"),
    ("23", "PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES", "source_scripts"),
    ("24", "PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES", "source_scripts"),
    ("25", "FOUR-ISLAND-TOUR-ROUTES-SOURCE", "source_scripts"),
    ("26", "SHELL-FLOWER-FLAG2-SOURCE", "source_scripts"),
    ("27", "AXE-LETTER-EVENT3-5-SOURCE", "source_scripts"),
    ("28", "HERB-MEDICINE-FOUR-SCENES-SOURCE", "source_scripts"),
    ("29", "SPIRIT-KING-EVENT69-SOURCE", "source_event_scripts"),
    ("30", "DINOSAUR-COLLECTOR-EVENT35-SOURCE", "source_script"),
    ("31", "FOUR-VILLAGE-EVENT09-12-SOURCE", "source_scripts"),
)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def source_sha(row: dict) -> str:
    for field in ("sha256", "original_sha256", "source_sha256", "source_file_sha"):
        if row.get(field):
            return row[field]
    raise ValueError("missing original source SHA: " + str(row.get("path")))


def audit(root: Path = ROOT) -> dict:
    catalog_bytes = (root / REC / CATALOG).read_bytes()
    if git_blob(catalog_bytes) != CATALOG_BLOB:
        raise ValueError("QUEST01 catalog Git blob changed: new audit required")
    catalog = json.loads(catalog_bytes)
    if (len(catalog["source_scripts"]), len(catalog["source_event_blocks"])) != (295, 1349):
        raise ValueError("QUEST01 census unexpectedly changed")
    indexed = {r["path"]: r["original_sha256"] for r in catalog["source_scripts"]}
    if len(indexed) != 295:
        raise ValueError("duplicate path inside QUEST01 catalog")
    selected = {}
    per_quest = {}
    observations = 0
    for quest, name, field in SPECS:
        path = root / REC / ("STONEAGE-QUEST" + quest + "-" + name + "-R1.json")
        report = json.loads(path.read_text(encoding="utf-8"))
        source = report[field]
        rows = [source] if field == "source_script" else source
        paths_here = set()
        for row in rows:
            key = row["path"]
            sha = source_sha(row)
            if key in paths_here:
                raise ValueError("duplicate source script inside QUEST" + quest + ": " + key)
            paths_here.add(key)
            if key in indexed and indexed[key] != sha:
                raise ValueError("QUEST01 script SHA mismatch: " + quest + "/" + key)
            if key in selected and selected[key]["sha"] != sha:
                raise ValueError("cross-report same-path SHA conflict: " + key)
            current = selected.setdefault(key, {"sha": sha, "quests": []})
            current["quests"].append(quest)
            observations += 1
        per_quest[quest] = len(rows)
    unselected = sorted(set(indexed) - set(selected))
    leftovers = Counter("/".join(p.split("/")[:-1]) for p in unselected)
    duplicated = {p: r["quests"] for p, r in sorted(selected.items()) if len(r["quests"]) > 1}
    outside = sorted(set(selected) - set(indexed))
    return {
        "report_count": len(SPECS),
        "quest_range": ["08", "31"],
        "catalogue_scripts": len(indexed),
        "catalogue_event_TYPE_sections": len(catalog["source_event_blocks"]),
        "report_script_occurrences": observations,
        "distinct_selected_paths": len(selected),
        "matched_catalogue_paths": len(set(selected) & set(indexed)),
        "outside_catalogue_paths": outside,
        "catalogue_not_selected": len(unselected),
        "cross_report_duplicate_paths": duplicated,
        "remaining_by_directory": dict(sorted(leftovers.items())),
        "per_quest_script_occurrences": per_quest,
    }


def verify_snapshot(root: Path = ROOT) -> dict:
    expected = json.loads((root / REC / SNAPSHOT).read_text(encoding="utf-8"))
    actual = audit(root)
    if actual != expected["derived"]:
        raise ValueError("QUEST32 publication snapshot disagrees with current derived files")
    return actual


if __name__ == "__main__":
    print(json.dumps(verify_snapshot(), ensure_ascii=False, sort_keys=True, indent=2))
