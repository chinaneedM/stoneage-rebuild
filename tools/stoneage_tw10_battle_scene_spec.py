"""Evidence-bounded Taiwan v1 battle-scene index and candidate SAB layout.

V1 source directly proves SAB envelope/record sizes and address-table custody.
20x20 big-endian u16 interpretation is lineage-supported, not an original v1
runtime decode/select call. Never attach an actual palette or UI coordinates.
"""
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_DATA = _ROOT / "research/recovered/STONEAGE-TW10-BATTLE-DATASET-R1.txt"


def indexed_battle_resources(path=_DATA):
    """Return original order of all 233 address records with category boundaries."""
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("ADDRESS_RECORD|label=battle|"):
            continue
        parts = dict(chunk.split("=", 1) for chunk in line.split("|")[1:] if "=" in chunk)
        record = {k: parts[k] for k in ("name", "category", "sha256")}
        for key in ("index", "offset", "size", "match_count"):
            record[key] = int(parts[key])
        records.append(record)
    if len(records) != 233:
        raise ValueError("expected 233 original TW1.0 battle address records")
    categories = [r["category"] for r in records]
    if categories.count("battle_map") != 218 or categories.count("palette") != 15:
        raise ValueError("battle-map/palette categories cannot be conflated")
    expected_offset = 0
    for i, record in enumerate(records):
        if record["index"] != i or record["offset"] != expected_offset:
            raise ValueError("original address order/contiguity violated")
        size = 804 if record["category"] == "battle_map" else 708
        if record["size"] != size or record["match_count"] != 1:
            raise ValueError("unexpected v1 battle record size/path ambiguity")
        expected_offset += size
    if expected_offset != 185892:
        raise ValueError("battle resource container size mismatch")
    return records


def decode_sab_candidate(payload):
    """Interpret an 804-byte SAB file as lineage 20x20 big-endian IDs, not v1 proof."""
    if type(payload) is not bytes or len(payload) != 804 or payload[:4] != b"SAB ":
        raise ValueError("requires one exact original-size SAB envelope (804 bytes)")
    ids = [int.from_bytes(payload[i:i + 2], "big") for i in range(4, 804, 2)]
    if len(ids) != 400:
        raise ValueError("invalid candidate tile count")
    return {
        "candidate_grid": [ids[r * 20:(r + 1) * 20] for r in range(20)],
        "grid_width": 20, "grid_height": 20,
        "layout_evidence": "LINEAGE_SUPPORTED_NOT_DIRECT_V1_DRAW_CALL",
        "selected_battle_map_index": None,
        "selected_palette": None,
        "selected_animation": None,
        "original_runtime_selection_verified": False,
    }


def pet_graphic_identity_boundary(graphic_id):
    """Retain a source-typed pet graphic identity; no unverified SPR/ADRN lookup."""
    if type(graphic_id) is not int or graphic_id < 0:
        raise ValueError("requires an already-decoded nonnegative graphic integer")
    return {
        "graphic_identity": graphic_id,
        "identity_name_evidence": "EARLY_GENERATED_PROTOCOL_LINEAGE",
        "v1_spr_group": None, "v1_adrn_bitmap": None,
        "v1_draw_call_verified": False,
    }
