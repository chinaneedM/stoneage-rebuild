"""Replay joint-pet-panel compatibility for six same-ID variants from PET76."""
from collections import Counter
from itertools import product
import json

from tools.stoneage_pet_detail30_base_panel import project_pet_source_base_panel
from tools.stoneage_pet_high_first_76_master import REPORT, REPORT_BLOB, ROOT, blob, inputs
from tools.stoneage_pet_high_first_tw75_conditional_ranges import ALLOCATIONS, project


WITNESSES = ROOT / "research/pets/PET-HIGH-FIRST-77-PLAYER-PANEL-WITNESSES-R1.json"


def birth_deltas():
    # Each offset is selected independently before the shared ten-point allocation.
    deltas = {
        tuple(offset + count for offset, count in zip(offsets, counts, strict=True))
        for offsets in product(range(-2, 3), repeat=4)
        for counts in ALLOCATIONS
    }
    assert len(deltas) == 14270
    return deltas


def panels(base, initnum, deltas):
    result = set()
    for delta in deltas:
        internal = [(value + offset) * initnum for value, offset in zip(base, delta, strict=True)]
        panel = project_pet_source_base_panel(internal)
        result.add((panel.max_hp, panel.attack, panel.defense, panel.quick))
    return result


def marginal_bounds(panels):
    return [[min(column), max(column)] for column in zip(*panels)]


def derive():
    source = json.loads(WITNESSES.read_bytes())
    assert source["schema"] == "stoneage.pet77.reposted_classic_pc_panel_witnesses.r1"
    assert source["source"]["evidence"] == "SEARCH_INDEX_EXCERPTS_ONLY_DIRECT_FETCH_403"
    assert source["source"]["original_sample_dates"] is None
    assert source["source"]["original_executable_or_server_build"] is None
    assert not any(source[k] for k in ("initial_level_and_equipment_verified", "official_same_deployment_verified",
                                       "observed_levelup_rolls_verified"))
    raw = REPORT.read_bytes()
    assert blob(raw) == REPORT_BLOB
    variants = {r["template_id"]: r for r in json.loads(raw)["rows"] if r["selected_fields_differing_from_claim"]}
    d = inputs()
    claims = d["master"]["pet_flag_1_field_projections"]
    ranges = d["birth"]["rows"]
    deltas = birth_deltas()

    summary = Counter()
    by_template = []
    for tid, row in variants.items():
        assert set(row["selected_fields_differing_from_claim"]) == {"base"}
        index = row["position"]
        a = claims[index]
        b = {**a, **row["selected_fields_differing_from_claim"], "row_sha256": row["selected_row_sha256"]}
        witnesses = [w for w in source["rows"] if w["template_id"] == tid]
        assert witnesses and all(w["name"] == a["name"] and w["final_level"] > 1 for w in witnesses)
        model_a = panels(a["base"], a["initnum"], deltas)
        model_b = panels(b["base"], b["initnum"], deltas)
        assert marginal_bounds(model_a) == ranges[index]["level1_unmodified_work_panel_marginal_ranges"]
        assert marginal_bounds(model_b) == project(b)["level1_unmodified_work_panel_marginal_ranges"]
        for witness in witnesses:
            panel = tuple(witness["initial"])
            supported = (panel in model_a, panel in model_b)
            summary[supported] += 1
        by_template.append(dict(template_id=tid, name=a["name"], samples=len(witnesses),
                                claimed_hp_range=marginal_bounds(model_a)[0],
                                saved_hp_range=marginal_bounds(model_b)[0],
                                claimed_only_joint_panels=len(model_a - model_b),
                                saved_only_joint_panels=len(model_b - model_a)))

    assert len(by_template) == 6 and summary == {(True, True): 12} and len(source["rows"]) == 12
    assert len({(w["template_id"], tuple(w["initial"])) for w in source["rows"]}) == 11
    assert len({(w["template_id"], w["final_level"], tuple(w["final"])) for w in source["rows"]}) == 12
    return dict(rows=12, distinct_initial_panels_by_template=11, compatible_with_both=12,
                single_variant_resolved=0, model="CONDITIONAL_LV1_UNMODIFIED_LATER_PC_PANEL",
                by_template=by_template)


if __name__ == "__main__":
    print(json.dumps(derive(), ensure_ascii=False, sort_keys=True))
