import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tools.stoneage_state_gated_runtime_world_reachability_probe import (
    compute_state_gated_reachability,
    parse_progression_witness,
)


REPORT = """StoneAge shadowed-branch joined progression witness — R1
COUNT|combined_progression_witness|1
COUNT|branch_full_orphan_closure|1
PROGRESSION_WITNESS|acquisition_source_floors=1|ingress_source_floor=811|ingress_target_floor=820|classic_path_after_acquisition=1|min_classic_hops=1|same_level_witness=1|nondecreasing_level_witness=1|combined_state_progression_witness=1
RESOLUTION|SHADOWED_BRANCH_PROGRESSION_WITNESS_CLOSED
"""


def _edge(source,destination):
    return SimpleNamespace(
        source=SimpleNamespace(floor_id=source),
        destination=SimpleNamespace(floor_id=destination),
    )


class StateGatedWorldReachabilityTests(unittest.TestCase):

    def test_parse_requires_closed_combined_progression(self):
        witness=parse_progression_witness(REPORT)
        self.assertEqual(witness.source_floor,811)
        self.assertEqual(witness.destination_floor,820)
        with self.assertRaises(ValueError):
            parse_progression_witness(
                REPORT.replace(
                    "COUNT|combined_progression_witness|1",
                    "COUNT|combined_progression_witness|0",
                )
            )

    @patch(
        "tools.stoneage_state_gated_runtime_world_reachability_probe."
        "load_ordered_runtime_reachability"
    )
    def test_gated_edge_closes_classic_orphan_component(self,mock_load):
        extension=SimpleNamespace(
            materializable_floor_ids=frozenset({1,2,3,4}),
            stable_world=SimpleNamespace(by_floor={1:object()}),
            resolved_by_floor={2:object(),3:object(),4:object()},
        )
        runtime=SimpleNamespace(
            base=SimpleNamespace(extension=extension),
            topology=SimpleNamespace(
                legacy_warps=(
                    _edge(1,2),
                    _edge(3,4),
                )
            ),
        )
        mock_load.return_value=SimpleNamespace(
            runtime=runtime,
            reached_floor_ids=frozenset({1,2}),
        )
        local_report=REPORT.replace(
            "ingress_source_floor=811",
            "ingress_source_floor=2",
        ).replace(
            "ingress_target_floor=820",
            "ingress_target_floor=3",
        )
        audit=compute_state_gated_reachability(
            progression_text=local_report
        )
        self.assertEqual(
            audit.state_gated_reached_floor_ids,
            frozenset({1,2,3,4}),
        )
        self.assertEqual(audit.newly_reached_floor_ids,(3,4))
        self.assertEqual(audit.remaining_unreachable_floor_ids,())
        self.assertEqual(
            audit.counts["classic_reachable_floor_ids"],
            2,
        )
        self.assertEqual(
            audit.counts["state_gated_reachable_floor_ids"],
            4,
        )


if __name__=="__main__":
    unittest.main()
