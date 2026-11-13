"""INTEGRATION87: source-bound public numeric census, not original-game execution."""
import copy
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIR = ROOT / "research" / "recovered"
def load(name):
    return json.loads((DIR / name).read_text(encoding="utf-8"))

class GetPet2DOriginalSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = load("STONEAGE-INTEGRATION87-36-GETPET-TW10-SPR-2D-BRIDGE-R1.json")
        cls.world = load("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json")
        cls.tw = load("STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json")
        cls.i62 = load("STONEAGE-INTEGRATION62-QUEST30-TWO-GETPET-TW1-29-RD-PIXELS-R1.json")
        cls.i66 = load("STONEAGE-INTEGRATION66-FOUR-ISLAND-TOUR-15-PET-TW1-ORIGINAL-PIXELS-R1.json")
        cls.i67 = load("STONEAGE-INTEGRATION67-SPIRIT-KING-THREE-GETPET-TW1-ORIGINAL-PIXELS-R1.json")

    def test_source_replay_all_36_numeric_template_and_spr_joins(self):
        rows = self.out["rows"]
        self.assertEqual(36, len(rows))
        self.assertEqual(36, len({x["source_getpet_integer"] for x in rows}))
        self.assertEqual(36, len({x["tw10_matching_spr_numeric_graphic"] for x in rows}))
        w = {x["getpet_integer"]: x for x in self.world["original_enemy_instance_to_template_lookups"]}
        t = {x[0]: x for x in self.tw["source_groups"]}
        self.assertEqual(set(w), {x["source_getpet_integer"] for x in rows})
        for r in rows:
            with self.subTest(pet=r["source_getpet_integer"]):
                e = w[r["source_getpet_integer"]]
                g = t[e["original_template_graphic_id"]]
                self.assertEqual(e["template_id_via_enemy_field4"], r["mixed25_template_numeric_id"])
                self.assertEqual(e["enemy_master_line_sha256"], r["mixed25_enemy_instance_line_sha256"])
                self.assertEqual(e["template_master_line_sha256"], r["mixed25_template_source_line_sha256"])
                self.assertEqual(e["original_template_petflag_raw"], r["mixed25_template_petflag_raw"])
                self.assertEqual(e["original_template_graphic_id"], r["tw10_matching_spr_numeric_graphic"])
                self.assertEqual(g[1:5], [r["tw10_source_spr_group_index"], r["tw10_source_full_spr_segment_sha256"],
                                          r["tw10_original_animation_record_count"], r["tw10_source_selected_frame_positions"]])
                self.assertEqual(g[6], r["tw10_selected_unique_bitmap_numeric_count"])
                self.assertEqual(3, len(r["tw10_selected_original_action_direction0"]))
                for act, source_act in zip(r["tw10_selected_original_action_direction0"], g[5]):
                    self.assertEqual([act["original_action_code"], act["original_direction_code"],
                                      act["original_frame_positions"], act["original_bitmap_sequence_u32le_sha256"],
                                      act["original_duration_word"]], source_act)

    def test_all_original_getpet_occurrences_preserved(self):
        actual = {}
        count = 0
        for s in self.world["source_GetPet_scripts_and_event_blocks"]:
            for c in s["commands"]:
                for n in c["raw_integer_tokens_in_order"]:
                    count += 1
                    actual.setdefault(n, []).append((s["path"], s["source_sha256"], c["getpet_line_sha256"],
                                                       bool(s["is_named_backup"])))
        self.assertEqual(44, count)
        self.assertEqual(36, len(actual))
        self.assertEqual(count, self.out["summary"]["source_getpet_command_numeric_occurrences"])
        for r in self.out["rows"]:
            source = {(x["source_script_path"], x["source_script_sha256"], x["source_command_line_sha256"],
                       x["source_is_named_backup"]) for x in r["original_script_occurrences"]}
            self.assertEqual(set(actual[r["source_getpet_integer"]]), source)
            self.assertEqual(len(actual[r["source_getpet_integer"]]), len(r["original_script_occurrences"]))

    def test_existing_source_pixel_decode_error_retained(self):
        invalid = {x["graphic"]: x for x in self.tw["source_renderable_sequences_excluded"]}
        rows = {x["tw10_matching_spr_numeric_graphic"]: x for x in self.out["rows"]}
        self.assertEqual({100401}, set(rows) & set(invalid))
        bad = rows[100401]
        self.assertEqual(1481, bad["source_getpet_integer"])
        self.assertEqual([82729], bad["tw10_selected_known_strict_decode_exception"]["source_bitmap_numeric_ids"])
        self.assertFalse(bad["tw10_selected_original_action_direction0"][0]["original_pixels_all_strictly_decodable"])
        self.assertTrue(all(x["original_pixels_all_strictly_decodable"] for x in bad["tw10_selected_original_action_direction0"][1:]))
        self.assertEqual(0, self.out["summary"]["new_original_picture_discovery"])

    def test_original_prior_specialized_integration_is_not_new_discovery(self):
        c = {"INTEGRATION62": {x["source_GetPet_ID"] for x in self.i62["source_qualified_two_rewards"]},
             "INTEGRATION66": {x["source_instance_id"] for r in self.i66["route_terminal_sources"] for x in r["occurrences"]},
             "INTEGRATION67": {x["original_getpet_instance_id"] for x in self.i67["original_pet_reward_source_joins"]}}
        self.assertEqual({k: sorted(v) for k, v in c.items()}, self.out["prior_source_specialized_instance_ids"])
        for row in self.out["rows"]:
            self.assertEqual(sorted(k for k,v in c.items() if row["source_getpet_integer"] in v),
                             sorted(row["prior_specialized_integration_numbers"]))

    def test_cross_version_claims_remain_false(self):
        n = self.out["negative_evidence"]
        self.assertTrue(n["known_graphic_100401_action0_has_unrenderable_bitmap_82729"])
        self.assertTrue(all(v is False for k,v in n.items() if k != "known_graphic_100401_action0_has_unrenderable_bitmap_82729"))
        self.assertEqual(0, self.out["summary"]["new_native_original_pet_reward_execution"])
        self.assertEqual(0, self.out["summary"]["new_original_sprite_bytes_acquired"])
        self.assertEqual(0, self.out["private_source_independent_numeric_audit"]["new_original_pixel_decode_count"])
        self.assertFalse(any("original_cp950_fields" in json.dumps(r) for r in self.out["rows"]))

    def test_tampering_does_not_accidentally_pass_source_check(self):
        original = self.out["rows"][0]
        altered = copy.deepcopy(original)
        altered["tw10_matching_spr_numeric_graphic"] += 1
        e = next(x for x in self.world["original_enemy_instance_to_template_lookups"]
                 if x["getpet_integer"] == altered["source_getpet_integer"])
        self.assertNotEqual(altered["tw10_matching_spr_numeric_graphic"], e["original_template_graphic_id"])
        self.assertEqual(original["tw10_matching_spr_numeric_graphic"], e["original_template_graphic_id"])

if __name__ == "__main__":
    unittest.main()
