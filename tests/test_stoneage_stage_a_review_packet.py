"""Reject losses or scope promotions in the user-facing review manifest."""
from copy import deepcopy
import json
import unittest

from tools.stoneage_stage_a_review_packet import DEFAULT, validate


class ReviewPacketBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(DEFAULT.read_text(encoding="utf-8"))

    def test_committed_packet_and_link_targets(self):
        result = validate(self.packet)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["original_game_execution"])

    def test_forged_acceptance_or_original_execution_is_rejected(self):
        for key in ("stage_a_accepted", "joint_user_review_completed", "stage_b_started",
                    "new_original_server_content", "original_playthrough_certified"):
            with self.subTest(key=key):
                candidate = deepcopy(self.packet)
                candidate[key] = True
                with self.assertRaisesRegex(ValueError, "promotion"):
                    validate(candidate)
        candidate = deepcopy(self.packet)
        candidate["replays"][0]["original_game_execution"] = True
        with self.assertRaisesRegex(ValueError, "execution overclaim"):
            validate(candidate)

    def test_source_digest_and_historical_prefix_corruption(self):
        candidate = deepcopy(self.packet)
        candidate["source_pins"]["foundation"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source custody"):
            validate(candidate)
        candidate = deepcopy(self.packet)
        candidate["preserved_historical_prefixes"][2]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "historical prefix"):
            validate(candidate)

    def test_omitted_history_and_omitted_family_are_rejected(self):
        candidate = deepcopy(self.packet)
        candidate["preserved_historical_prefixes"] = []
        with self.assertRaisesRegex(ValueError, "incomplete continuity"):
            validate(candidate)
        candidate = deepcopy(self.packet)
        candidate["families"].pop()
        with self.assertRaisesRegex(ValueError, "nine unique"):
            validate(candidate)

    def test_disappearing_flow_and_unpinned_replay_are_rejected(self):
        candidate = deepcopy(self.packet)
        candidate["playflows"].pop()
        with self.assertRaisesRegex(ValueError, "playflow scope"):
            validate(candidate)
        candidate = deepcopy(self.packet)
        candidate["replays"][0]["modules"] = ["tests.test_stoneage_nonexistent"]
        with self.assertRaisesRegex(ValueError, "unpinned replay"):
            validate(candidate)


if __name__ == "__main__":
    unittest.main()
