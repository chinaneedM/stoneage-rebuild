"""INTEGRATION47: public, source-bounded Poru scene and NPC joins.

All inputs are rights-safe DERIVED records already committed in the repo.
Actual commercial DAT, dialogue, sprites, and original image bytes were
independently checked in private custody, not shipped into public Actions.
"""
from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "research" / "recovered"
NAMES = {
    "q23": "STONEAGE-QUEST23-PORU-FOUR-STONES-SOURCE-AND-NINE-SCENES-R1.json",
    "q24": "STONEAGE-QUEST24-PORU-FLAG63-FUNCTIONS-AND-FOUR-SCENES-R1.json",
    "i47": "STONEAGE-INTEGRATION47-PORU-13-SCENE-SOURCE-GRAPH-R1.json",
}
SOURCE_BLOBS = {
    "QUEST23": "303bafb317e5d5911c4a9bc23ac4ab90066b9b80",
    "QUEST24": "c7150d08cace8da3d6b5411036818e1baacb46dc",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def read_inputs():
    raw = {key: (BASE / path).read_bytes() for key, path in NAMES.items()}
    return {key: json.loads(b) for key, b in raw.items()}, raw


def audit_sources(d):
    """Reject material misjoins; never infer native runtime from static files."""
    r, q23, q24 = d["i47"], d["q23"], d["q24"]
    assert r["schema"] == "stoneage.integration47.poru_13_scene_source_graph_and_63_64_boundary_r1"
    assert r["remote_start"]["historical_CURRENT_blob"] == "c89e0e33537990aa2132b47c40fef49a985a935c"
    assert r["remote_start"]["historical_CURRENT_bytes"] == 2709173
    assert r["remote_start"]["modified"] is False
    for label, upstream in (("QUEST23", "q23"), ("QUEST24", "q24")):
        s = r["source_reports"][label]
        assert s["git_path"] == "research/recovered/" + NAMES[upstream]
        assert s["git_blob"] == SOURCE_BLOBS[label]
        assert s["original_npc_source_manifest_occurrences_sha256_reverified"] == len(d[upstream]["source_manifest"])
        assert s["private_zip_all_CRC_valid"] is True
        assert len(s["private_zip_sha256"]) == 64
    per_source = {"QUEST23": q23, "QUEST24": q24}
    scenes = r["scene_floors"]
    assert len(scenes) == 13 and [x["floor"] for x in scenes] == sorted({x["floor"] for x in scenes})
    assert {x["source"] for x in scenes} == set(per_source)
    for label, original in per_source.items():
        original_scenes = {s["floor"]: s for s in original["original_scene_observations"]}
        actual = [s for s in scenes if s["source"] == label]
        assert len(actual) == len(original_scenes)
        assert set(x["floor"] for x in actual) == set(original_scenes)
        for row in actual:
            s = original_scenes[row["floor"]]
            w, h = s["geometry"]
            assert row["dimensions"] == [w, h]
            assert row["DAT_bytes"] == 8 + 6 * w * h == s["original_DAT_bytes"]
            assert row["DAT_sha256"] == s["original_DAT_sha256"]
            assert row["source_high_value_draw_occurrences"] == s["source_draw_positions"]
            assert row["source_unique_high_value_aliases"] == s["unique_source_images"]
            assert row["candidate_RGBA_sha256_private"] == s["three_candidate_RGBA_sha256"]["combined"]
            assert row["candidate_canvas_dimensions"] == s["canvas_size"]
            assert row["source_low_1_99_occurrences_uninterpreted"] >= 0
            assert row["candidate_pixel_and_DAT_replayed"] is True
    material = r["material_result"]
    assert material["original_DAT_scene_count"] == len(scenes)
    assert material["original_high_value_draw_occurrences_across_13_scenes"] == sum(x["source_high_value_draw_occurrences"] for x in scenes)
    assert material["original_low_1_99_occurrences_untreated"] == sum(x["source_low_1_99_occurrences_uninterpreted"] for x in scenes)
    assert material["source_create_records_occurrences_QUEST23"] == len(q23["source_creates"])
    assert material["source_create_records_occurrences_QUEST24"] == len(q24["source_creates"])
    assert material["source_manifest_file_occurrences_sha256_verified"] == len(q23["source_manifest"]) + len(q24["source_manifest"])
    assert material["candidate_TW1_tile_aliases_in_QUEST23"] == 913
    assert material["candidate_TW1_tile_aliases_in_QUEST24"] == 490
    assert material["shared_aliases_same_PNG_bytes"] == 78
    assert material["shared_aliases_different_PNG_bytes"] == 0
    assert material["candidate_TW1_unique_tile_aliases_union"] == 913 + 490 - 78 == 1325
    overlap = r["shared_TW1_image_aliases_actually_byte_equal"]
    assert len(overlap) == 78
    assert len({x["alias"] for x in overlap}) == 78
    assert all(type(x["alias"]) is int and x["alias"] > 99 and len(x["png_sha256"]) == 64 for x in overlap)
    # The overlap hashes depend on private actual PNG files and are not reproduced by public CI.
    g = r["source_graph"]
    edge = g["strict_map_warp_edge"]
    params = next(s for s in q24["actual_source_warpman_parameters"] if s["path"] == "poru/wpm_5509_35_35")
    assert params["source_values"] == {"WARP": "5510,16,49", "FREE": "ITEM=2414", "MONEY": "-1"}
    created = next(s for s in q24["source_creates"] if s["floor"] == 5509 and params["path"] in s["argument_paths"])
    assert "WarpMan" in [x["source_functionset"] for x in created["source_bindings"]]
    assert edge["source_floor"] == 5509 and edge["source_NPC_xy"] == created["borncenter"][:2] == [37, 35]
    assert edge["source_create_path"] == created["source_create_path"]
    assert edge["source_create_ordinal"] == created["source_create_ordinal"]
    assert edge["source_create_block_sha256"] == created["original_block_sha256"]
    assert edge["source_function"] == "WarpMan"
    assert [edge["destination_floor"], *edge["destination_xy"]] == [int(n) for n in params["source_values"]["WARP"].split(",")]
    assert edge["literal_FREE"] == params["source_values"]["FREE"]
    assert edge["literal_MONEY"] == params["source_values"]["MONEY"]
    assert edge["parameter_sha256"] == next(x["sha256"] for x in q24["source_manifest"] if x["path"] == params["path"])
    assert edge["source_cell_three_original_u16"] == [407, 0, 49152]
    assert edge["destination_cell_three_original_u16"] == [4204, 44, 49152]
    assert edge["actual_original_warp_observed"] is False
    assert edge["reciprocal_edge_from_target_proven"] is False
    adjacent = g["adjacent_nonwarp_NPC"]
    original_neighbor = next(x for x in q24["source_creates"] if x["floor"] == 5510 and "poru/wpm_5510_16_50" in x["argument_paths"])
    assert adjacent["source_xy"] == original_neighbor["borncenter"][:2] == [16, 50]
    assert adjacent["source_create_block_sha256"] == original_neighbor["original_block_sha256"]
    assert adjacent["source_cell_three_original_u16"] == [4206, 0, 49152]
    assert adjacent["source_function"] == q24["wpm_named_dialogue"]["source_functionset"] == "ExChangeMan"
    assert adjacent["actual_TYPE"] == q24["wpm_named_dialogue"]["actual_type"] == "MESSAGE"
    assert adjacent["script_path"] == q24["wpm_named_dialogue"]["path"]
    assert adjacent["script_sha256"] == next(x["sha256"] for x in q24["source_manifest"] if x["path"] == adjacent["script_path"])
    assert adjacent["has_WARP_field"] is False
    assert adjacent["coordinate_manhattan_distance_from_warp_destination"] == 1
    assert adjacent["original_NPC_dialogue_or_entry_executed"] is False
    assert g["proven_same_version_physical_map_edges_count"] == 1
    assert g["authenticated_world_map_from_these_scenes"] is False
    flag63 = g["Q24_flag63_provider"]
    source_flag63 = q24["flag63_bridge"]
    assert flag63["script"] == source_flag63["provider_script"] == "poru/boy04"
    assert flag63["event_ordinal"] == source_flag63["event_ordinal"] == 1
    assert flag63["source_condition"] == source_flag63["original_provider_condition"] == "NOWEV=63"
    assert flag63["source_GetPet"] == 352 == int(source_flag63["original_provider_commands"]["GetPet"][0])
    assert flag63["source_EndSetFlg"] == source_flag63["original_provider_commands"]["EndSetFlg"][0] == "63"
    assert flag63["existing_late_pet_graphic_candidate"] == source_flag63["original_GetPet_352_existing_WORLD21_lookup"]["original_template_graphic_id"]
    assert source_flag63["next_source_QUEST23_request_conditions"] == ["ENDEV=63"]
    assert flag63["actual_pet_reward_or_save_observed"] is False
    finale = g["Q23_flag64_four_stones"]
    source_finale = q23["four_stones_finale"]
    for key, upstream in (("script", "script"), ("event_ordinal", "event_ordinal"), ("source_condition", "original_condition"), ("source_DelItem_literal", "original_DelItem_literal"), ("source_EndSetFlg", "EndSetFlg_literal")):
        assert finale[key] == source_finale[upstream]
    assert finale["source_GetPet"] == int(source_finale["GetPet_instance_literal"]) == 310
    assert finale["source_transition_63_to_64_runtime_proven"] is False
    diff = g["noncoincident_four_item_conditions"]
    assert diff["Q24_script"] == q24["source_four_object_message_difference"]["script"]
    assert diff["Q24_MESSAGE_condition"] == q24["source_four_object_message_difference"]["original_message_condition"]
    assert diff["Q23_finale_condition"] == source_finale["original_condition"]
    assert set(diff["shared_explicit_item_ids"]) == {18556, 18557, 18559}
    assert diff["Q24_only_condition_item"] == 18544 and diff["Q23_only_finale_item"] == 18558
    assert diff["do_not_silently_rewrite_or_unify"] is True
    missing = g["floor500_boundary"]
    assert missing["Q23_floor500_source_creates"] == sum(x["floor"] == 500 for x in q23["source_creates"])
    assert missing["Q24_floor500_source_creates"] == sum(x["floor"] == 500 for x in q24["source_creates"])
    assert missing["DAT_in_955_original_MAP09"] is False and missing["original_floor500_scene_rebuilt"] is False
    assert r["guards"]["historical_stage_A"] == {"PARTIAL": 7, "OPEN": 2}
    for k, expected in (("stage_B", "GATED"), ("wiki", "GATED"), ("R79", "PAUSED_NON_BLOCKING"), ("overall_percent", None)):
        assert r["guards"][k] == expected
    for key in ("private_original_DAT_RDs_PNGs_scripts_published", "TW1_original_client_native_scene_executed", "native_WarpMan_or_event_branch_executed", "official_early_same_server_deployment"):
        assert r["guards"][key] is False
    for key in ("one_WarpMan_edge_is_not_a_complete_Poru_world_route", "Q23_and_Q24_already_cataloged_scripts_not_newly_discovered", "source_low_1_99_not_asserted_as_collision", "candidate_tile_alias_count_not_pet_or_object_entity_count"):
        assert r["guards"][key] is True
    assert material["new_original_DAT_acquired"] == material["new_original_NPC_scripts_acquired"] == material["new_original_RD_decoded"] == 0


class Integration47Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.raw = read_inputs()

    def test_01_upstream_git_blob_exact(self):
        for label, file_key in (("QUEST23", "q23"), ("QUEST24", "q24")):
            self.assertEqual(git_blob_sha(self.raw[file_key]), SOURCE_BLOBS[label])

    def test_02_all_bounded_sources_replay(self):
        audit_sources(self.data)

    def test_03_reject_invented_scene(self):
        d = copy.deepcopy(self.data)
        d["i47"]["scene_floors"].append(dict(d["i47"]["scene_floors"][0], floor=90099))
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_04_reject_source_DAT_digest_reassignment(self):
        d = copy.deepcopy(self.data)
        d["i47"]["scene_floors"][3]["DAT_sha256"] = "0" * 64
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_05_reject_source_pixel_hash_promotion(self):
        d = copy.deepcopy(self.data)
        d["i47"]["scene_floors"][3]["candidate_RGBA_sha256_private"] = "a" * 64
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_06_reject_wrong_destination(self):
        d = copy.deepcopy(self.data)
        d["i47"]["source_graph"]["strict_map_warp_edge"]["destination_floor"] = 500
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_07_reject_file_name_masquerading_as_WarpMan(self):
        d = copy.deepcopy(self.data)
        d["i47"]["source_graph"]["adjacent_nonwarp_NPC"]["source_function"] = "WarpMan"
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_08_reject_invented_reciprocal_warp(self):
        d = copy.deepcopy(self.data)
        d["i47"]["source_graph"]["strict_map_warp_edge"]["reciprocal_edge_from_target_proven"] = True
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_09_reject_flag_or_item_misjoin(self):
        d = copy.deepcopy(self.data)
        d["i47"]["source_graph"]["Q24_flag63_provider"]["source_GetPet"] = 310
        with self.assertRaises(AssertionError): audit_sources(d)
        d = copy.deepcopy(self.data)
        d["i47"]["source_graph"]["noncoincident_four_item_conditions"]["Q24_only_condition_item"] = 18558
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_10_reject_bogus_floor500_qualification(self):
        d = copy.deepcopy(self.data)
        d["i47"]["source_graph"]["floor500_boundary"]["DAT_in_955_original_MAP09"] = True
        with self.assertRaises(AssertionError): audit_sources(d)

    def test_11_reject_hist_model_promotion(self):
        for key in ("official_early_same_server_deployment", "native_WarpMan_or_event_branch_executed", "private_original_DAT_RDs_PNGs_scripts_published"):
            d = copy.deepcopy(self.data)
            d["i47"]["guards"][key] = True
            with self.assertRaises(AssertionError): audit_sources(d)

    def test_12_reject_original_contents_as_entities(self):
        d = copy.deepcopy(self.data)
        d["i47"]["material_result"]["candidate_TW1_unique_tile_aliases_union"] = 1403
        with self.assertRaises(AssertionError): audit_sources(d)


if __name__ == "__main__":
    unittest.main()
