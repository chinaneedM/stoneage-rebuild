"""Verify the published receipts without requiring the private source archive."""

from collections import Counter
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "research/recovered"


def load(name):
    return json.loads((ROOT / name).read_bytes())


class IndependentRarRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = load("STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json")
        cls.map01 = load("STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json")
        cls.map03 = load("STONEAGE-MAP-SCENE-MODULE-03-98-ORIGINAL-MAP-SOURCE-AND-12-INDEX-R1.json")
        cls.prior_route = load("STONEAGE-STAGE-A-3021-3022-ORIGINAL-STATIC-ROUTE-CONTENT-R1.json")

    def test_every_previous_failed_map_member_is_reconciled(self):
        r = self.receipt
        self.assertEqual(r["archive"], {
            "bytes": self.map01["original_rar_bytes"],
            "sha256": self.map01["original_rar_sha256"],
            "RAR_member_headers": self.map01["full_rar_header_entries_seen"],
        })
        self.assertEqual({d["name"] for d in r["decoders"]}, {"7-Zip", "UnRAR"})
        expected = self.map01["source_extraction_errors_not_reclassified_as_corruption"]
        rows = r["recovered_MAP01_failures"]
        self.assertEqual(len({(x["group"], x["name"]) for x in rows}), 63)
        self.assertEqual(
            [[x["group"], x["name"], x["bytes"], x["prior_libarchive_emitted_bytes"],
              x["prior_libarchive_error"]] for x in rows], expected,
        )
        self.assertEqual(Counter(x["name"].lower().rsplit(".", 1)[1] for x in rows),
                         {"dat": 40, "map": 23})
        for row in rows:
            with self.subTest(member=row["name"], group=row["group"]):
                w, h = row["dimensions"]
                self.assertGreater(w, 0)
                self.assertGreater(h, 0)
                width_per_cell = 6 if row["name"].lower().endswith(".dat") else 2
                self.assertEqual(row["bytes"], 8 + width_per_cell * w * h)
                self.assertRegex(row["crc32"], r"^[0-9a-f]{8}$")
                self.assertRegex(row["sha256"], r"^[0-9a-f]{64}$")
        v = r["verification"]
        self.assertEqual(v["selected_members_byte_equal"], 3060)
        self.assertEqual(v["selected_members_RAR_CRC_equal"], 3060)
        self.assertEqual(v["previous_MAP01_success_rows_rechecked"], 2990)
        self.assertEqual(v["previous_MAP01_success_rows_outside_scope"], 0)
        self.assertEqual(v["recovered_MAP01_rows"], len(rows))

    def test_four_floors_match_rar_headers_and_fill_the_prior_join(self):
        priority = self.receipt["priority_four_floors"]
        self.assertEqual(
            {k: (v["dimensions"], v["crc32"]) for k, v in priority.items()},
            {"100": ([800, 800], "aa7a58ad"), "200": ([800, 1200], "8315f313"),
             "3000": ([150, 150], "8a628975"), "3021": ([407, 144], "c0d8a645")},
        )
        self.assertEqual(self.receipt["integration02_floor_source_coverage"], {
            "previously_qualified": 56, "now_crc_qualified_structured_client_DAT": 60,
            "new_floors": [100, 200, 3000, 3021],
            "associated_static_GetPet_CREATE": 2, "associated_static_NPCEnemy_CREATE": 105,
        })

    def test_client_server_payloads_and_source_names_stay_separate(self):
        a = self.receipt["floor3021"]
        b = self.receipt["floor3022_control"]
        self.assertEqual(a["cells_per_plane"], 407 * 144)
        self.assertEqual(a["client_vs_same_archive_server_unequal_values"], [14080, 42921])
        self.assertEqual(a["client_DAT"]["sha256"], self.receipt["priority_four_floors"]["3021"]["sha256"])
        self.assertEqual(a["server_LS2MAP"]["crc32"], "5d7be038")
        self.assertNotEqual(a["server_LS2MAP"]["sha256"], a["prior_public_other_source_LS2MAP_sha256"])
        self.assertEqual(sum(n for _, n in a["client_event_counts"]), a["cells_per_plane"])
        for label, expected in (("sb_dou", 100), ("npcgen_warp", 200)):
            group = a["original_config_center_DAT_values"][label]
            self.assertEqual(group["coordinates"], expected)
            self.assertEqual([sum(n for _, n in values) for values in group["DAT_plane_value_counts"]],
                             [expected] * 3)
        pair = a["public_vs_private_server_file"]
        self.assertTrue(pair["byte_equal_payload_after_44_byte_header"])
        self.assertEqual(pair["header_differing_offsets_zero_based"], [8, 9, 10, 11, 13, 14, 15, 16, 17, 19])
        self.assertNotEqual(pair["private_full_name_field_sha256"], pair["public_full_name_field_sha256"])
        self.assertEqual(b["client_vs_same_archive_server_unequal_values"], [0, 0])
        self.assertEqual(b["client_plane_sha256_u16be"][:2], b["server_plane_sha256_u16be"])
        prior_dat = self.prior_route["floor3022_original_client_DAT"]
        self.assertEqual(b["client_DAT"], {
            "sha256": prior_dat["sha256"], "crc32": prior_dat["crc32"], "bytes": prior_dat["size_bytes"],
        })

    def test_dojo_challenge_parameters_and_exit_configs_stay_separate(self):
        dojo = self.receipt["floor3021"]["original_NPCEnemy_ARG_route"]
        self.assertEqual(dojo["source_template"]["functionset"], "NPCEnemy")
        self.assertEqual(dojo["literal_ARG_target_categories"], {
            "within_column": 90, "next_column": 9, "other_floor_3008": 1,
        })
        self.assertEqual(dojo["independently_recovered_ARG_members"], 100)
        self.assertEqual(dojo["matched_CHAR09_original_ARG_sha256_rows"], 100)
        self.assertEqual(dojo["literal_ENEMYNO_in_original_order"], list(range(564, 581)))
        self.assertEqual(dojo["literal_ENEMYPETNO_in_original_order"], list(range(687, 721)))
        self.assertEqual(dojo["independent_CREATE_exit_target"], [3022, 1, 7])
        self.assertEqual(dojo["independent_CREATE_exit_configurations"], 200)
        rows = dojo["rows"]
        self.assertEqual([row[0] for row in rows], list(range(1, 101)))
        self.assertEqual([row[1] for row in rows], list(range(0, 300, 3)))
        self.assertEqual(sum(row[4] for row in rows), dojo["source_ARG_total_bytes"])
        for row, following in zip(rows, rows[1:]):
            next_x, next_y = following[2]
            self.assertEqual(row[3], [3021, next_x, next_y + (2 if row[0] % 10 else 4)])
        self.assertEqual(rows[-1][3], [3008, 20, 20])
        self.assertEqual(dojo["last_ARG_target_client_DAT"]["dimensions"], [40, 40])
        self.assertFalse(dojo["original_runtime_trigger_verified"])

    def test_real_payload_replays_and_preserves_unresolved_aliases(self):
        r = self.receipt
        art = r["source_art_and_dojo_config"]
        self.assertEqual(art["real_15.bin"], {
            "bytes": 763908374, "crc32": "bd8bab8d",
            "sha256": "c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d",
        })
        graphics = r["same_archive_map_graphics"]
        self.assertEqual(graphics["structured_client_DAT_members"], 995)
        self.assertEqual(graphics["short_or_empty_DAT_members"], 16)
        self.assertEqual(graphics["unique_alias_counts_by_status"], {
            "dual_decoded_original_index_pixels": 5168, "missing_alias": 2111, "duplicate_alias": 4,
        })
        old = {x["graphic_alias"]: x for x in self.map03["map1000_twelve_early_TW1_unmapped_graphics_later_index_and_positions"]}
        rows = {x["alias"]: x for x in graphics["map1000_prior_TW1_missing_aliases"]}
        self.assertEqual(set(rows), set(old))
        decoded = [row for row in rows.values() if row["status"] == "dual_decoded_original_index_pixels"]
        self.assertEqual(len(decoded), 11)
        self.assertEqual(sum(row["occurrences"] for row in decoded), 12)
        self.assertEqual(rows[22413]["status"], "missing_alias")
        self.assertEqual(rows[22413]["ADRN_ordinals"], [])
        for row in decoded:
            prior = old[row["alias"]]
            self.assertEqual(row["ADRN_ordinals"], [prior["original_ADRN_record_ordinal"]])
            self.assertEqual(row["ADRN_record_sha256"], prior["original_ADRN_record_sha256"])
            self.assertGreaterEqual(row["REAL_offset"], 315842228)
            self.assertLessEqual(row["REAL_offset"] + row["RD_bytes"], art["real_15.bin"]["bytes"])
            self.assertRegex(row["index_sha256"], r"^[0-9a-f]{64}$")
        preview = graphics["private_preview"]["frames"]
        self.assertEqual(preview["1000"]["decoded_aliases_omitted_from_color_preview_for_reserved_palette_slots"],
                         [11208])
        self.assertEqual(preview["3021"]["unresolved_markers"], [])
        self.assertEqual(preview["3022"]["unresolved_markers"], [])

    def test_historical_attribution_and_runtime_remain_open(self):
        bounds = self.receipt["bounds"]
        for flag in ("authenticated_early_official_deployment", "native_client_or_server_executed",
                     "third_plane_collision_or_event_execution_verified", "raw_proprietary_data_in_public_git"):
            self.assertFalse(bounds[flag])
        self.assertEqual(bounds["stage_A_families"], {"PARTIAL": 7, "OPEN": 2})
        self.assertIsNone(bounds["overall_percent"])


if __name__ == "__main__":
    unittest.main()
