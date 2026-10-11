"""Fail-closed archival evidence-boundary gate for Taiwan 8.0 PET documentation.

This is an internal documentation consistency check, not verification of external
URLs or a claim to have compiled or executed an original game binary.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = "docs/specs/STONEAGE-PET-80-CONTEMPORARY-RELEASE-EVIDENCE-R1.md"
OTHER = (
    "docs/HISTORICAL-TIMELINE.md",
    "docs/SOURCE-REGISTRY.md",
    "docs/CURRENT-STATE.md",
)
ORIGINAL_ANNOUNCEMENT = "https://gnn.gamer.com.tw/detail.php?sn=20167"

EXPECTED_ROWS = {
    "Did contemporary reporting describe official Taiwan 8.0 PET equipment on launch?": "FACT (2005-06-08 press record)",
    "Is the checked-in pinned later Bismarck default PET feature enabled?": "NO in the previously accepted default source/profile gate",
    "Are the 2008/2009/2010 digital download URLs presently byte-verified?": "OPEN; none fetched/hashed/authenticated here",
    "Is there an original compatible enabled client/server binary pair with version identifiers and checked configuration?": "OPEN",
    "Was opcode 127 observed from an original game client to an original server?": "OPEN",
    "Are native PET item owner/unique code/save-load transitions reproducible without synthetic aliases?": "OPEN",
    "Does any result establish 1999 JSS or Taiwan 1.0 PET equipment?": "NO",
}

def validate(spec: str, timeline: str, registry: str, current: str) -> None:
    if ORIGINAL_ANNOUNCEMENT not in spec or ORIGINAL_ANNOUNCEMENT not in registry or ORIGINAL_ANNOUNCEMENT not in timeline:
        raise ValueError("Contemporaneous press citation missing")
    for needle in (
        "2005-06-08", "999ffdf1", "_PET_ITEM", "sa8_8016.rar",
        "sa_8002a", "No external binary", "not", "community",
    ):
        if needle not in spec:
            raise ValueError("Missing evidence/provenance boundary: " + needle)
    rows = {}
    for line in spec.splitlines():
        if not (line.startswith("| ") and line.endswith(" |")):
            continue
        fields = [part.strip() for part in line.strip("|").split("|")]
        if len(fields) != 2:
            raise ValueError("Malformed evidence matrix")
        rows[fields[0]] = fields[1]
    for question, expected in EXPECTED_ROWS.items():
        if rows.get(question) != expected:
            raise ValueError("Evidence matrix drift: " + question)
    if "SRC-PET-8-2005-CONTEMPORARY-LAUNCH-20261011" not in registry:
        raise ValueError("Source registry evidence block missing")
    if "Contemporary official 8.0 PET equipment reporting separated" not in timeline:
        raise ValueError("Historical timeline evidence block missing")
    if "PET 8.0 contemporary launch evidence and clean-binary retrieval leads" not in current:
        raise ValueError("Continuity receipt missing")
    if "2465 bounded closed +18 OPEN +3 historical UB" not in current:
        raise ValueError("Historical pressure boundary drift")
    if "no engine/design-stage transition" not in current:
        raise ValueError("Stage boundary drift")

def main() -> None:
    content = [(ROOT / p).read_text(encoding="utf-8") for p in (SPEC, *OTHER)]
    validate(*content)
    print("PET_80_CONTEMPORARY_RELEASE_EVIDENCE_BOUNDARY_PASS")

if __name__ == "__main__":
    main()
