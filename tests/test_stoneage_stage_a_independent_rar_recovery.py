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

    def test_native_warp_witness_links_two_distinct_direct_edges(self):
        native = load("STONEAGE-STAGE-A-DOJO-NATIVE-WARP-WITNESS-R1.json")
        self.assertEqual(native["parent_RAR_sha256"], self.receipt["archive"]["sha256"])
        gmsv = native["members_by_relative_archive_path"]["SA2.5服務端/gmsv/gmsv.exe"]
        self.assertEqual((gmsv["bytes"], gmsv["crc32"]), (1897867, "6e31b63a"))
        self.assertEqual(
            {key: row["work_int_slot"] for key, row in native["NPCEnemyInit_original_keys"].items()},
            {"dieact": 0x54, "warpfl": 0x55, "warpx": 0x56, "warpy": 0x57},
        )
        self.assertEqual(native["Warp_template"]["functionset"], "Warp")
        edges = native["static_direct_edges"]
        self.assertEqual(
            [(row["kind"], row["site_va"], row["to_va"]) for row in edges],
            [("call", 0x495cf2, 0x440730), ("jmp", 0x490f9d, 0x4904d0),
             ("call", 0x490c02, 0x440730)],
        )
        code = native["GMSV_PE32_i386_sections"][".text"]
        for edge in edges:
            self.assertEqual(edge["site_file_offset"], edge["site_va"] - code["VA"] + code["file_offset"])
        self.assertTrue(native["bounds"]["both_decoders_full_byte_equal_and_RAR_CRC_passed"])
        self.assertFalse(native["bounds"]["server_or_client_executed"])
        self.assertFalse(native["bounds"]["live_coordinate_or_packet_observed"])

    def test_bounded_route_replay_matches_every_source_config(self):
        result = load("STONEAGE-STAGE-A-DOJO-ORIGINAL-ROUTE-BOUNDED-REPLAY-R1.json")
        self.assertEqual(result["source_archive_sha256"], self.receipt["archive"]["sha256"])
        original = self.receipt["floor3021"]["original_NPCEnemy_ARG_route"]
        x86 = result["x86_probe"]
        self.assertEqual(x86["shared_warp_function_entry_stop"], "0x440730")
        self.assertEqual(x86["enemy"],
                         [[row[0], row[6], row[3], 0x495cf2] for row in original["rows"]])
        target = original["independent_CREATE_exit_target"]
        centers = [row[2] for row in original["rows"]]
        self.assertEqual(x86["warp"], [
            [[x + 6, y + delta], target, 0x490c02]
            for x, y in centers for delta in (2, 3)
        ])
        self.assertEqual(x86["observed_positive_count"], 300)
        negatives = x86["negative"]
        self.assertEqual(set(negatives), {
            "dieact_zero_synthetic", "out_of_bounds_synthetic", "same_position",
            "wrong_event", "wrong_object", "wrong_x",
        })
        self.assertTrue(all(not row["warp_called"] for row in negatives.values()))
        self.assertEqual(negatives["dieact_zero_synthetic"]["stop"], "0x495d66")
        self.assertFalse(x86["warp_function_body_executed"])
        boot = result["full_program_launch"]
        self.assertTrue(boot["qemu_no_network_card"])
        self.assertEqual(boot["guest_network_interfaces"], ["lo"])
        self.assertEqual(boot["windows_cmd_exit"], 0)
        self.assertIn(9200, boot["observed_guest_tcp_listen_ports"])
        traced = boot["instrumented_second_run"]
        self.assertTrue(traced["gmsv_executable_loaded"])
        self.assertTrue(traced["matching_cygwin_loaded"])
        self.assertEqual((traced["gmsv_bind_port"], traced["gmsv_listen_return"]), (9065, 0))
        self.assertEqual(
            [(row["seconds_after_gmsv_launch"], row["listen_ports"]) for row in traced["guest_snapshots"]],
            [(28, [9200]), (56, [9200]), (84, [9200])],
        )
        self.assertFalse(traced["sustained_game_listener_observed"])
        self.assertFalse(traced["saac_gmsv_handshake_observed"])
        readiness = boot["readiness_checked_run"]
        self.assertTrue(readiness["waited_for_saac_listener_before_starting_gmsv"])
        self.assertEqual(
            [(row["seconds_after_gmsv_launch"], row["listen_ports"]) for row in readiness["guest_snapshots"]],
            [(7, [9065, 9200]), (14, [9065, 9200]), (21, [9065, 9200]), (28, [9065, 9200])],
        )
        self.assertEqual(readiness["native_console_reported_map_files_found"], 716)
        self.assertFalse(readiness["map_initialization_finished_observed"])
        inventory = result["same_archive_server_map_inventory"]
        self.assertEqual(inventory["ls2map_magic_files"], readiness["native_console_reported_map_files_found"])
        self.assertEqual(inventory["strict_shape_match"], 714)
        self.assertEqual(len(inventory["trailing_byte_exceptions"]), 2)
        self.assertEqual(inventory["floor3008"]["dimensions"], [40, 40])
        self.assertFalse(inventory["trailing_byte_exceptions_cause_runtime_failure_verified"])
        long_run = boot["long_readiness_checked_run"]
        self.assertEqual(
            [(row["seconds_after_gmsv_launch"], row["listen_ports"]) for row in long_run["guest_snapshots"]],
            [(seconds, [9065, 9200]) for seconds in range(15, 91, 15)],
        )
        self.assertEqual(long_run["native_console_correct_map_files_and_completed"], 716)
        self.assertEqual((long_run["native_console_npc_files_searched"], long_run["native_console_correct_templates"]),
                         (2203, 119))
        self.assertFalse(long_run["template_loader_message_static_witness"]["message_itself_demonstrates_fatal_error"])
        self.assertFalse(long_run["established_tcp_socket_observed"])
        self.assertFalse(boot["full_client_server_login_or_warp_observed"])
        self.assertFalse(result["historical_official_deployment_verified"])

    def test_historical_attribution_and_runtime_remain_open(self):
        bounds = self.receipt["bounds"]
        for flag in ("authenticated_early_official_deployment", "native_client_or_server_executed",
                     "third_plane_collision_or_event_execution_verified", "raw_proprietary_data_in_public_git"):
            self.assertFalse(bounds[flag])
        self.assertEqual(bounds["stage_A_families"], {"PARTIAL": 7, "OPEN": 2})
        self.assertIsNone(bounds["overall_percent"])


if __name__ == "__main__":
    unittest.main()
