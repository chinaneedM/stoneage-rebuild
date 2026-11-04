"""Verify evidence-limited GMSV/SAAC original configuration source receipt.

This public test does not extract private binaries or prove a native handshake.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-STAGE-A-GMSV-SAAC-ORIGINAL-CONFIG-PRECONDITIONS-R1.json"
NATIVE = ROOT / "research/recovered/STONEAGE-STAGE-A-DOJO-ORIGINAL-ROUTE-BOUNDED-REPLAY-R1.json"


class OriginalConfigPreconditionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.native = json.loads(NATIVE.read_text(encoding="utf-8"))

    def test_archive_identity_and_nonpromotion(self):
        r, old = self.report, self.native
        self.assertEqual(r["source_archive_sha256"], old["source_archive_sha256"])
        self.assertEqual(r["source_archive_byte_length"], 361255180)
        self.assertEqual(r["preserved_current_state_blob"], old["preserved_current_state_blob"])
        self.assertIn("COMMUNITY_MIXED25", r["source_scope"])
        self.assertFalse(r["server_to_account_handshake_verified"])
        self.assertFalse(r["npc_create_event_runtime_verified"])
        self.assertFalse(r["original_client_login_verified"])
        self.assertFalse(r["original_dojo_warp_in_full_game_verified"])
        self.assertFalse(r["official_jss1999_tw10_cn182_deployment_verified"])
        self.assertFalse(r["public_ci_reextracts_private_rar"])
        self.assertIsNone(r["overall_percent"])

    def test_member_custody_and_static_port_relation(self):
        r = self.report
        members = r["extracted_member_receipts"]
        self.assertEqual([m["relative_path"] for m in members],
                         ["gmsv/setup.cf", "gmsv/setup.cf.bak", "saac/acserv.cf"])
        self.assertEqual([m["source_bytes"] for m in members], [9715, 9719, 807])
        for m in members:
            self.assertRegex(m["sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(m["rar_crc32"], r"^[0-9a-f]{8}$")
        c = r["static_original_configuration"]
        self.assertTrue(c["gmsv_account_server_loopback"])
        self.assertEqual(c["gmsv_account_server_port"], c["saac_listen_port"])
        self.assertEqual(c["gmsv_game_listen_port"], 9065)
        self.assertEqual(c["gmsv_npc_template_capacity_config"], 256)
        self.assertEqual(c["gmsv_npc_create_capacity_config"], 8192)
        self.assertTrue(c["gmsv_and_saac_account_auth_values_equal"])
        self.assertTrue(c["gmsv_backup_and_saac_account_auth_values_equal"])
        self.assertEqual(c["gmsv_live_backup_differing_line_count"], 1)
        self.assertEqual(c["gmsv_live_backup_only_differing_field"], "PET1")
        self.assertFalse(c["raw_credential_values_published"])
        self.assertFalse(c["credential_value_digests_published"])

    def test_prior_original_execution_is_not_a_new_handshake(self):
        r = self.report["prior_verified_original_guest_run"]
        native = self.native["full_program_launch"]
        long = native["long_readiness_checked_run"]
        self.assertEqual(r["sampled_seconds_after_gmsv_launch"],
                         [s["seconds_after_gmsv_launch"] for s in long["guest_snapshots"]])
        self.assertEqual(r["sampled_listener_ports"], [9065, 9200])
        for snapshot in long["guest_snapshots"]:
            self.assertEqual(snapshot["listen_ports"], [9065, 9200])
        self.assertEqual(r["reported_maps_correct"], long["native_console_correct_map_files_and_completed"])
        self.assertEqual(r["npc_files_searched"], long["native_console_npc_files_searched"])
        self.assertEqual(r["correct_npc_templates_reported"], long["native_console_correct_templates"])
        self.assertFalse(r["established_tcp_socket_observed"])
        self.assertFalse(long["established_tcp_socket_observed"])
        self.assertFalse(native["same_archive_client_started"])

    def test_unsafe_interpretation_rejected(self):
        c = dict(self.report["static_original_configuration"])
        c["gmsv_and_saac_account_auth_values_equal"] = False
        self.assertNotEqual(c["gmsv_and_saac_account_auth_values_equal"],
                            self.report["static_original_configuration"]["gmsv_and_saac_account_auth_values_equal"])
        self.assertEqual(self.report["stage_a_status"], "7_PARTIAL_2_OPEN")
        self.assertEqual(self.report["stage_b_wiki_status"], "GATED")
        self.assertEqual(self.report["r79_status"], "PAUSED_NON_BLOCKING")


if __name__ == "__main__":
    unittest.main()
