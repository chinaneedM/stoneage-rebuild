"""INTEGRATION04: source-bound original x86 capture → item → pet template → visual carrier.
Reads only previously published derived evidence; it never runs original binaries.
"""
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / "research" / "recovered"
OUTPUT = RECOVERED / "STONEAGE-INTEGRATION04-COMPILED-CAPTURE-PET-ITEM-SPR-SOURCE-BRIDGE-R1.json"
SCHEMA = "stoneage.integration04.source_separated_original_compiled_capture_item_pet_template_visual_graph.r1"
ARCHIVE = "d71e2e6766e8ac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5"


def source_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def reconstruct(pet11, pet12, pet13, world):
    tw10 = {x["compiled_char_int_key53"]: x for x in pet11["capture_candidate_links"]}
    tw85 = {x["capture_source_key53_candidate"]: x for x in pet12["groups"]}
    templates = {x["compiled_capture_key53"]: x for x in pet13["templates"]}
    assert len(templates) == 11 and len(world["compiled_requirement_replays"]) == 11
    assert len(tw10) == 2 and len(tw85) == 6 and not (set(tw10) & set(tw85))
    assert pet13["source_archive_full_sha256"] == world["source_archive_sha256"] == ARCHIVE
    rows = []
    for replay in world["compiled_requirement_replays"]:
        key = replay["target_key_53"]
        source = templates[key]
        required = replay["compiled_item_ids"]
        assert required == source["capture_required_item_IDs"]
        assert len(required) == len(replay["item_table_presence"])
        assert replay["complete"]["capture_result_flag"] == 1
        assert replay["complete"]["before"]["actor_int_44"] + 1 == replay["complete"]["after"]["actor_int_44"]
        omitted = []
        for m in replay["missing_cases"]:
            assert m["omitted_item_id"] in required
            assert m["trace"]["capture_result_flag"] == 0
            assert m["trace"]["score"] is None
            assert not m["trace"]["guest_writes"]
            omitted.append(m["omitted_item_id"])
        assert sorted(omitted) == sorted(required)
        if key in tw10:
            assert tw10[key]["original_source_graphic_no"] == source["original_graphic_numeric_ID"]
            assert tw10[key]["same_12byte_SPRADRN_record_in_TW1_and_mixed25"] is True
            visual = "TW10_PRIVATE_ORIGINAL_RD_PIXEL_OBSERVED_CROSS_ARCHIVE_12BYTE_SPRADRN_EQUAL"
        elif key in tw85:
            assert tw85[key]["graphic_no"] == source["original_graphic_numeric_ID"]
            assert tw85[key]["full_original_RD_pixels_read_now"] == 0
            visual = "TW85_COMMUNITY_SOURCE_SPR_AND_RD_INDEX_PET12_PIXELS_NOT_READ"
        else:
            visual = "NO_PET11_OR_PET12_PIXEL_OR_ANIMATION_CARRIER"
        rows.append({
            "compiled_capture_work_key_53": key,
            "original_x86_fixture_required_item_ids": required,
            "preserved_item_master_numeric_presence": replay["item_table_presence"],
            "omitted_individual_required_items_fail_before_scoring": omitted,
            "original_x86_isolated_function_entry_fixture_capture_success": True,
            "original_x86_isolated_success_incremented_capture_counter": True,
            "source_same_archive_template_id": source["original_template_numeric_ID"],
            "source_same_archive_original_template_row_sha256": source["original_physical_line_including_newline_sha256"],
            "source_same_archive_graphic_numeric_id": source["original_graphic_numeric_ID"],
            "source_same_archive_petflag_literal": source["original_PETFLG"],
            "source_same_archive_base_stats_literals": source["original_base_stats_literal"],
            "source_same_archive_attribute_literals": source["original_earth_water_fire_wind_literals"],
            "source_same_archive_seven_skill_slot_numeric_candidates": source["original_seven_skill_slots_nullable"],
            "original_graphic_source_grade": visual,
            "source_graphic_link_is_numeric_only_even_if_visual_record_equal": True,
            "original_game_same_deployment_species_identity_verified": False,
            "native_original_game_real_encounter_and_capture_proven": False
        })
    return sorted(rows, key=lambda x: x["compiled_capture_work_key_53"])


class Integration04EvidenceQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.sources = {}
        for key, pin in cls.output["source_pins"].items():
            data = (ROOT / pin["path"]).read_bytes()
            assert source_blob_sha(data) == pin["sha"], (key, pin)
            cls.sources[key] = json.loads(data)

    def verify(self, d):
        self.assertEqual(d["schema"], SCHEMA)
        self.assertEqual(d["baseline_main_head"], "bfdcb70407988baa1660389b66e07ada85a0763a")
        self.assertEqual(d["historical_CURRENT_blob_untouched"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(d["source_original_mixed25_RAR_sha256"], ARCHIVE)
        self.assertEqual(d["source_original_mixed25_compiled_GMSV_sha256"], self.sources["world37"]["source_exe_sha256"])
        rows = reconstruct(*(self.sources[k] for k in ("pet11", "pet12", "pet13", "world37")))
        self.assertEqual(d["rows"], rows)
        self.assertEqual(len(rows), 11)
        self.assertEqual(len({r["compiled_capture_work_key_53"] for r in rows}), 11)
        presence = sorted({item for r in rows for item, grade in zip(
            r["original_x86_fixture_required_item_ids"], r["preserved_item_master_numeric_presence"]
        ) if grade == "ONLY_ALTERNATE"})
        self.assertEqual(presence, [20247, 20253, 20259])
        self.assertEqual(d["summary"]["original_compiled_condition_keys"], 11)
        self.assertEqual(d["summary"]["source_same_archive_template_numeric_candidates"], 11)
        self.assertEqual(d["summary"]["isolated_original_x86_fixture_success_conditions"], 11)
        self.assertEqual(d["summary"]["required_item_omission_failures_before_score"], 13)
        self.assertEqual(d["summary"]["required_item_ids_only_in_alternate_source_master"], presence)
        visual = {}
        for r in rows:
            key = r["original_graphic_source_grade"]
            visual[key] = visual.get(key, 0) + 1
        self.assertEqual(d["summary"]["visual_grade_counts"], visual)
        self.assertEqual(sorted(visual.values()), [2, 3, 6])
        self.assertEqual(d["summary"]["template_PETFLG_zero_with_isolated_fixture_capture_success"], [8])
        self.assertEqual(d["summary"]["exact_compiled_capture_to_original_spr_native_runtime_links"], 0)
        self.assertEqual(d["summary"]["original_official_same_deployment_proven"], 0)
        self.assertIsNone(d["summary"]["historical_species_population_derived"])
        flags = d["boundaries"]
        self.assertIs(flags["compiled_x86_replay_is_from_the_original_isolated_instruction_path_with_synthetic_initial_state"], True)
        for k in [
            "original_binary_run_or_source_bytes_newly_replayed_in_INTEGRATION04",
            "mixed25_template_selected_by_actual_compiled_loader_proven",
            "PETFLG_zero_proves_natural_wild_capture_impossible",
            "PETFLG_zero_fixture_success_proves_natural_wild_capture_possible",
            "TW10_or_TW85_visuals_and_mixed25_server_files_original_official_same_deployment",
            "missing_visual_scope_means_original_species_or_sprite_absent",
            "real_native_original_game_world_entered",
            "original_proprietary_bytes_or_images_published"
        ]:
            self.assertIs(flags[k], False, k)
        self.assertEqual(flags["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual(flags["stage_B_and_wiki"], "GATED")
        self.assertEqual(flags["R79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(flags["overall_percent"])

    def test_exact_full_source_derived_replay(self):
        self.verify(self.output)

    def test_reject_fabricated_item_master_coverage(self):
        bad = copy.deepcopy(self.output)
        row = next(r for r in bad["rows"] if r["compiled_capture_work_key_53"] == 777)
        row["preserved_item_master_numeric_presence"] = ["IN_BOTH"]
        with self.assertRaises(AssertionError):
            self.verify(bad)

    def test_reject_petflag_zero_silently_promoted(self):
        bad = copy.deepcopy(self.output)
        row = next(r for r in bad["rows"] if r["compiled_capture_work_key_53"] == 8)
        row["source_same_archive_petflag_literal"] = 1
        with self.assertRaises(AssertionError):
            self.verify(bad)

    def test_reject_missing_item_failure_dropped(self):
        bad = copy.deepcopy(self.output)
        row = next(r for r in bad["rows"] if r["compiled_capture_work_key_53"] == 1105)
        row["omitted_individual_required_items_fail_before_scoring"].pop()
        with self.assertRaises(AssertionError):
            self.verify(bad)

    def test_reject_visual_index_promoted_to_real_pixels(self):
        bad = copy.deepcopy(self.output)
        row = next(r for r in bad["rows"] if r["compiled_capture_work_key_53"] == 962)
        row["original_graphic_source_grade"] = "TW10_PRIVATE_ORIGINAL_RD_PIXEL_OBSERVED_CROSS_ARCHIVE_12BYTE_SPRADRN_EQUAL"
        with self.assertRaises(AssertionError):
            self.verify(bad)

    def test_reject_claim_of_original_runtime_species_mapping(self):
        bad = copy.deepcopy(self.output)
        bad["rows"][0]["original_game_same_deployment_species_identity_verified"] = True
        with self.assertRaises(AssertionError):
            self.verify(bad)

    def test_reject_claim_of_native_capture_or_official_deployment(self):
        bad = copy.deepcopy(self.output)
        bad["boundaries"]["real_native_original_game_world_entered"] = True
        with self.assertRaises(AssertionError):
            self.verify(bad)

    def test_reject_wrong_compiled_capture_requirement(self):
        bad = copy.deepcopy(self.output)
        bad["rows"][0]["original_x86_fixture_required_item_ids"] = [999999]
        with self.assertRaises(AssertionError):
            self.verify(bad)


if __name__ == "__main__":
    unittest.main()
