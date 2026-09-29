import unittest
from pathlib import Path

from tools.stoneage_map_delivery_model import (
    CACHE_ACCEPT,
    MATERIALIZE_MAP_RECT,
    NO_HISTORICAL_CLIENT_FILE_ASSERTION,
    REQUEST_MAP_RECT,
    SERVER_AUTHORITY_INTERNAL_MAP,
    MapRectangle,
    build_singleplayer_materialization_plans,
    parse_server_only_payload_report,
    receive_map_check,
    receive_map_payload,
)
from tools.stoneage_singleplayer_world import LATER_RECOVERED


REPORT = (
    "research/recovered/"
    "STONEAGE-25-MISSING-WARP-DESTINATION-PAYLOADS-R1.txt"
)


class MapDeliveryModelTests(unittest.TestCase):

    def test_mc_match_accepts_cache_and_mismatch_requests_same_rectangle(self):
        rect = MapRectangle(20002, 0, 0, 27, 27)
        accepted = receive_map_check(
            rectangle=rect,
            cache_checksum_matches=True,
        )
        missing = receive_map_check(
            rectangle=rect,
            cache_checksum_matches=False,
        )

        self.assertEqual(accepted.action, CACHE_ACCEPT)
        self.assertEqual(missing.action, REQUEST_MAP_RECT)
        self.assertEqual(missing.rectangle, rect)

    def test_m_payload_materializes_requested_rectangle(self):
        rect = MapRectangle(20004, 5, 6, 20, 21)
        decision = receive_map_payload(rectangle=rect)
        self.assertEqual(decision.action, MATERIALIZE_MAP_RECT)
        self.assertEqual(decision.rectangle, rect)

    def test_real_server_only_report_builds_four_local_materialization_plans(self):
        parsed = parse_server_only_payload_report(
            Path(REPORT).read_text(encoding="utf-8")
        )
        plans = build_singleplayer_materialization_plans(
            parsed,
            source_ref=REPORT,
        )

        self.assertEqual(
            {plan.floor_id for plan in plans},
            {20002, 20004, 20006, 20009},
        )
        self.assertEqual(
            {
                plan.floor_id: (plan.width, plan.height)
                for plan in plans
            },
            {
                20002: (50, 100),
                20004: (80, 80),
                20006: (80, 40),
                20009: (100, 100),
            },
        )
        for plan in plans:
            self.assertEqual(plan.evidence_role, LATER_RECOVERED)
            self.assertEqual(
                plan.runtime_authority,
                SERVER_AUTHORITY_INTERNAL_MAP,
            )
            self.assertEqual(
                plan.historical_client_file_claim,
                NO_HISTORICAL_CLIENT_FILE_ASSERTION,
            )
            self.assertFalse(plan.network_required)
            self.assertFalse(plan.legacy_cache_file_required)

    def test_truncated_server_only_report_is_rejected(self):
        text = Path(REPORT).read_text(encoding="utf-8")
        rows = [
            line for line in text.splitlines()
            if line.startswith("MISSING_DAT_DESTINATION|")
        ]
        self.assertEqual(len(rows), 4)
        truncated = text.replace(rows[0] + "\n", "", 1)
        with self.assertRaisesRegex(ValueError, "id count drift"):
            parse_server_only_payload_report(truncated)

    def test_server_only_parser_refuses_historical_promotion_inputs(self):
        text = Path(REPORT).read_text(encoding="utf-8")
        promoted = text.replace(
            "EVIDENCE_ROLE|LATER_RECOVERED",
            "EVIDENCE_ROLE|EARLY_MEMBERSHIP_PROVEN",
            1,
        )
        with self.assertRaisesRegex(ValueError, "LATER_RECOVERED"):
            parse_server_only_payload_report(promoted)


if __name__ == "__main__":
    unittest.main()
