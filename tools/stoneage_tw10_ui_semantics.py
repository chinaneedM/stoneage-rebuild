"""Evidence-bounded decoded-record projection for TW1.0 UI source study.

Input is a complete ALREADY TOKENIZED record (never a wire parser or renderer).
Emitted names are early-lineage interpretations of original compiled positions.
Partial update/mask merging, actual graphical selection and original server rules
are explicitly outside this reference projector.
"""
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_CROSSWALK = _ROOT / "research/recovered/STONEAGE-TW10-UI-SEMANTICS-R1.json"


def crosswalk():
    return json.loads(_CROSSWALK.read_text(encoding="utf-8"))


def project_decoded_full_record(surface_id, record_key, values):
    """Project synthetic decoded full-record positions; do not infer screen layout."""
    if not isinstance(values, (list, tuple)):
        raise ValueError("values must be a complete decoded ordered tuple/list")
    spec = crosswalk()
    matching = [s for s in spec["surfaces"] if s["id"] == surface_id]
    if len(matching) != 1:
        raise ValueError("unknown UI evidence surface")
    matches = [r for r in matching[0]["record_contracts"] if r["schema_record"] == record_key]
    if len(matches) != 1:
        raise ValueError("record not original-v1 evidence input for this surface")
    record = matches[0]
    if len(values) != record["field_count"]:
        raise ValueError("partial update or surplus later-version fields not supported")
    items = []
    for field, value in zip(record["fields"], values):
        t = field["wire_type"]
        if t in ("decimal_int", "base62_int"):
            if type(value) is not int:
                raise ValueError("decoded integer expected at token " + str(field["position"]))
        elif t == "escaped_string":
            if type(value) is not str:
                raise ValueError("already-decoded string expected at token " + str(field["position"]))
        else:
            raise ValueError("unknown wire field type " + t)
        items.append({"token": field["position"], "lineage_name": field["name"],
                      "value": value, "position_evidence": field["position_evidence"],
                      "semantic_evidence": field["semantic_evidence"]})
    return {"surface": surface_id, "record": record_key, "decoded_full_record": items,
            "historical_layout": None, "visual_resource_selection": None,
            "original_display_verified": False,
            "warning": "RESEARCH PROJECTION ONLY; NOT ORIGINAL GUI EXECUTION"}


def classify_v1_received_battle_envelope(command):
    """V1 compiled B receive callback's second-byte routing only, not battle UI."""
    if not isinstance(command, str) or len(command) < 2 or command[0] != "B":
        raise ValueError("original B callback requires a B-prefixed command with discriminator")
    proof = crosswalk()["battle_receive"]
    branch = command[proof["second_byte_offset"]]
    key = branch if branch in ("C", "P", "A", "U") else "default"
    facts = proof["branches"][key]
    return {"branch": key, "direct_behavior": facts["direct_behavior"],
            "original_display_verified": False, "animation_id": None,
            "scene_map_id": None}


if __name__ == "__main__":
    import unittest
    unittest.main(module="tests.test_stoneage_tw10_ui_semantics")
