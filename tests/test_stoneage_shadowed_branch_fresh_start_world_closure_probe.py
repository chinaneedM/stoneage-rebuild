import unittest

from tools.stoneage_shadowed_branch_fresh_start_world_closure_probe import (
    analyze,
)


class FreshStartWorldClosureProbeTests(unittest.TestCase):

    def test_full_join_requires_all_fresh_start_and_world_prerequisites(self):
        audit=analyze(
            stone_text="FRESH_START_ECONOMIC_CHAIN|witness=1\n",
            leveling_closure_text=(
                "FRESH_START_LEVELING_TO_TARGET|witness=1\n"
            ),
            progression_text=(
                "COUNT|branch_full_orphan_closure|1\n"
                "COUNT|branch_returns_to_preexisting_reached|1\n"
                "PROGRESSION_WITNESS|same_level_witness=1|"
                "combined_state_progression_witness=1\n"
                "RESOLUTION|SHADOWED_BRANCH_PROGRESSION_WITNESS_CLOSED\n"
            ),
            world_text=(
                "COUNT|materializable_floor_ids|826\n"
                "COUNT|state_gated_reachable_floor_ids|826\n"
                "COUNT|remaining_unreachable_floor_ids|0\n"
            ),
        )
        self.assertTrue(audit.full_world)

    def test_missing_leveling_witness_keeps_world_open(self):
        audit=analyze(
            stone_text="FRESH_START_ECONOMIC_CHAIN|witness=1\n",
            leveling_closure_text=(
                "FRESH_START_LEVELING_TO_TARGET|witness=0\n"
            ),
            progression_text=(
                "COUNT|branch_full_orphan_closure|1\n"
                "COUNT|branch_returns_to_preexisting_reached|1\n"
                "PROGRESSION_WITNESS|same_level_witness=1|"
                "combined_state_progression_witness=1\n"
                "RESOLUTION|SHADOWED_BRANCH_PROGRESSION_WITNESS_CLOSED\n"
            ),
            world_text=(
                "COUNT|materializable_floor_ids|826\n"
                "COUNT|state_gated_reachable_floor_ids|826\n"
                "COUNT|remaining_unreachable_floor_ids|0\n"
            ),
        )
        self.assertFalse(audit.full_world)


if __name__=="__main__":
    unittest.main()
