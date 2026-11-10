"""INTEGRATION53: audited cross-carrier original quest NPC -> existing TW1 sprite groups.

Public checks replay source-certified derived indices, NOT private proprietary pixels.
"""
import hashlib
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-INTEGRATION53-THREE-DRAGONS-QUEST-NPC-TW10-SPR-SOURCE-BRIDGE-R1.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


class TestThreeDragonSourceArtworkCrosswalk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.source = {}
        for key, pointer in cls.r["upstream_public_git_blobs"].items():
            raw = (ROOT / pointer["path"]).read_bytes()
            assert blob_sha(raw) == pointer["git_blob"], key
            cls.source[key] = json.loads(raw)

    def test_all_upstream_source_blobs_are_original_and_unchanged(self):
        self.assertEqual(set(self.source), {"quest14", "pet07", "pet15", "pet10"})
        self.assertEqual(len(self.r["rows"]), 3)
        self.assertTrue(self.r["evidence_class"].endswith("NO_NEW_ORIGINAL_ASSET"))

    def test_three_quest_create_records_link_by_original_position_and_block_sha(self):
        q = self.source["quest14"]
        creates = q["original_create_rows"]
        self.assertEqual(len(creates), 4)
        for row in self.r["rows"]:
            c = row["quest14_source_create"]
            expected = next(x for x in creates if x["ordinal"] == c["ordinal"])
            self.assertEqual(c["original_block_sha256"], expected["original_sha256"])
            self.assertEqual(c["floor"], expected["floor"])
            self.assertEqual(c["xy"], expected["original_borncorner"][:2])
            self.assertEqual(c["graphic_alias"], expected["graphic_alias"])
            self.assertEqual(c["script_path"], expected["script_ref"])
            self.assertEqual(c["original_direction_literal"], expected["direction"])
            self.assertRegex(c["original_block_sha256"], SHA256)
        self.assertEqual([x["quest14_source_create"]["graphic_alias"] for x in self.r["rows"]],
                         [100384, 100385, 100386])

    def test_original_map_DAT_sha_exact_cell_and_dimensions_not_native_collision(self):
        maps = {x["floor"]: x for x in self.source["quest14"]["two_original_dat_maps"]}
        for row in self.r["rows"]:
            c = row["quest14_source_create"]
            m = row["original_map_DAT_source"]
            old = maps[c["floor"]]
            at = next(x for x in old["source_positions"] if x["create_ordinal"] == c["ordinal"])
            self.assertEqual(m["source_sha256"], old["original_sha256"])
            self.assertEqual(m["source_dimensions"], old["dimensions"])
            self.assertEqual(m["source_cell_three_u16"], at["actual_three_original_u16"])
            self.assertEqual(at["at"], c["xy"])
            self.assertEqual(m["source_cell_three_u16"][1:], [0, 49152])

    def test_static_quest_branch_is_literal_and_rewards_are_distinct(self):
        q = self.source["quest14"]
        found = []
        for row in self.r["rows"]:
            c = row["quest14_source_create"]
            script = row["original_script_source"]
            old = next(x for x in q["scripts"] if x["path"] == c["script_path"])
            link = next(x for x in q["catalog_relationships"]
                        if x["source_script"] == script["path"]
                        and x["relation"] == "dragon_source_condition_exchange_to_reward")
            self.assertEqual(script["source_sha256"], old["original_sha256"])
            self.assertEqual(script["source_event_first_predicate_sha256"], old["events"][0]["predicate_sha256"])
            self.assertEqual(script["source_getitem_literal"], old["events"][0]["actions"]["GetItem"])
            self.assertEqual(script["source_endsetflag_literal"], old["events"][0]["actions"]["EndSetFlg"])
            self.assertEqual(script["derived_quest_reward_item_id"], link["reward_item_id"])
            found.append(script["derived_quest_reward_item_id"])
        self.assertEqual(found, [2462, 2460, 2461])
        self.assertEqual(len({x["original_script_source"]["source_event_first_predicate_sha256"]
                              for x in self.r["rows"]}), 1)

    def test_TW10_original_SPR_source_segment_and_PET07_selected_three_sequences(self):
        old = self.source["pet07"]["source_groups"]
        for row in self.r["rows"]:
            got = row["original_TW10_retained_SPR"]
            base = next(x for x in old if x[0] == got["graphic_alias"])
            self.assertEqual(got["index"], base[1])
            self.assertEqual(got["segment_sha256"], base[2])
            self.assertEqual(got["full_original_sequence_count"], base[3])
            self.assertEqual(got["prior_PET07_selected_frame_positions"], base[4])
            expected = [{"action": x[0], "direction": x[1], "original_source_positions": x[2],
                         "source_animation_SHA256": x[3], "original_duration_literal": x[4]}
                        for x in base[5]]
            self.assertEqual(got["prior_PET07_selected_sequences"], expected)
            self.assertEqual([(x["action"], x["direction"]) for x in expected], [(0, 0), (2, 0), (1, 0)])

    def test_TW10_full_animation_group_coverage_inherits_PET15_not_new_decode(self):
        full = {x["graphic"]: x for x in self.source["pet15"]["groups"]}
        for row in self.r["rows"]:
            g = row["original_TW10_retained_SPR"]
            old = full[g["graphic_alias"]]
            self.assertEqual(g["index"], old["group_index"])
            self.assertEqual(g["segment_sha256"], old["segment_sha256"])
            self.assertEqual(g["full_original_sequence_count"], old["source_sequences"])
            self.assertEqual(g["fully_observable_sequences_as_previously_verified"], old["fully_observable_sequences"])
            self.assertEqual(g["full_original_frame_positions"], old["frame_positions"])
            self.assertEqual(g["full_original_distinct_bitmaps"], old["distinct_bitmaps"])
            self.assertEqual(g["observed_source_actions"], old["source_actions"])
            self.assertEqual(g["observed_source_directions"], old["source_directions"])
            self.assertEqual((g["full_original_sequence_count"], g["full_original_frame_positions"],
                              g["full_original_distinct_bitmaps"]), (56, 712, 232))

    def test_all_pet_template_candidates_exact_original_rows_not_species_claims(self):
        p10 = self.source["pet10"]["source_rows"]
        for row in self.r["rows"]:
            graphic = row["quest14_source_create"]["graphic_alias"]
            for file in ("enemybase.txt", "enemybase2.txt"):
                candidates = row["preserved_mixed25_pet_template_same_numeric_graphic_candidates"][file]
                exact = [x for x in p10[file] if x[2] == graphic]
                self.assertEqual(len(candidates), len(exact))
                for got, old in zip(candidates, exact):
                    self.assertEqual([got["physical_row_1based"], got["template_id"], got["graphic_alias"],
                                      got["petflg_literal"], got["source_row_sha256"]],
                                     [old[0], old[1], old[2], old[3], old[16]])
                    self.assertRegex(got["source_row_sha256"], SHA256)
                self.assertEqual({x["petflg_literal"] for x in candidates}, {0, 1})

    def test_alternative_template_tables_can_disagree_and_are_not_original_official_selection(self):
        for row in self.r["rows"]:
            t = row["preserved_mixed25_pet_template_same_numeric_graphic_candidates"]
            main = t["enemybase.txt"]
            alt = t["enemybase2.txt"]
            sameid = {x["template_id"]: x for x in main if x["petflg_literal"] == 1}
            altids = {x["template_id"]: x for x in alt if x["petflg_literal"] == 1}
            self.assertEqual(set(sameid), set(altids))
            for n in sameid:
                self.assertNotEqual(sameid[n]["source_row_sha256"], altids[n]["source_row_sha256"])
        self.assertFalse(self.r["no_native_or_identity_claims"]["mixed25_pet_template_rows_prove_quest_NPC_species_or_reward"])

    def test_guardian_from_different_floor_must_not_be_assigned_a_pet_sprite(self):
        x = self.r["excluded_same_source_guardian"]
        old = self.source["quest14"]["original_create_rows"][3]
        self.assertEqual((x["quest14_create_ordinal"], x["graphic_alias"], x["floor"], x["xy"]),
                         (3, old["graphic_alias"], old["floor"], old["original_borncorner"][:2]))
        self.assertNotIn(x["graphic_alias"], [row["original_TW10_retained_SPR"]["graphic_alias"]
                                             for row in self.r["rows"]])

    def test_summary_conservation_no_cross_group_bitmap_dedup_claim(self):
        s = self.r["summary"]
        sprites = [x["original_TW10_retained_SPR"] for x in self.r["rows"]]
        self.assertEqual(s["quest_NPC_source_rows_joined_to_TW10_SPR_groups"], 3)
        self.assertEqual(s["previously_observed_original_TW10_full_animation_sequences"],
                         sum(x["full_original_sequence_count"] for x in sprites))
        self.assertEqual(s["previously_observed_original_TW10_full_frame_positions"],
                         sum(x["full_original_frame_positions"] for x in sprites))
        self.assertEqual(s["previously_observed_original_TW10_distinct_bitmaps_by_group_sum_not_global_dedup"],
                         sum(x["full_original_distinct_bitmaps"] for x in sprites))
        self.assertEqual((s["new_original_DAT_bytes_recovered_this_unit"],
                          s["new_original_SPR_RD_pixel_bytes_decoded_this_unit"]), (0, 0))

    def test_original_history_and_identity_boundaries_not_promoted(self):
        state = self.r["preserved_current_original_git_blob"]
        self.assertEqual(state["sha"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(state["bytes"], 2709173)
        self.assertFalse(state["modified"])
        n = self.r["no_native_or_identity_claims"]
        self.assertTrue(n)
        self.assertTrue(all(x is False for x in n.values()))
        self.assertEqual(self.r["source_lineage"]["tw10_SPR_RD_PNG"],
                         "SEPARATE_TAIWAN_1_0_RETAIL_ORIGINAL_ARTWORK_PREVIOUSLY_PIXEL_DECODED")
        self.assertIsNone(self.r["overall_percent"])
        self.assertEqual(self.r["stage_A"], "7 PARTIAL + 2 OPEN")
        self.assertEqual((self.r["stage_B"], self.r["wiki"], self.r["R79"]),
                         ("GATED", "GATED", "PAUSED_NON_BLOCKING"))


if __name__ == "__main__":
    unittest.main()
