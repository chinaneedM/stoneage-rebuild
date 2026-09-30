import tempfile
import unittest
from pathlib import Path

from tools.stoneage_shadowed_branch_dynamic_occupancy_probe import (
    _store_row_floor,
    analyze,
)


COORD="""StoneAge shadowed-branch static coordinate accessibility — R1
STATIC_COORDINATE_CHAIN|witness=1
CONSERVATIVE_NPC_BIRTH_OCCUPANCY_CHAIN|witness=1
RESOLUTION|SHADOWED_BRANCH_STATIC_COORDINATE_ACCESS_CLOSED
"""

STATE="""StoneAge state-gated recovered25 runtime world reachability — R1
GATED_TRANSPORT|source_floor=811|destination_floor=820|progression_witness=1
RESOLUTION|STATE_GATED_RUNTIME_WORLD_REACHABILITY_CLOSED
"""

LEGAL="""StoneAge shadowed-branch legal-state reachability audit — R1
EXCHANGE_CHAIN_WITNESS|ordinal=1|source_floor=2020|joint_level_values=20|reward_units=1|keyword_present=0|eventno_class=NEGATIVE_SENTINEL|classic_warp_hops_to_gate=1|state_domain_satisfiable=1
RESOLUTION|SHADOWED_BRANCH_LEGAL_STATE_REACHABILITY_AUDITED
"""


class DynamicOccupancyProbeTests(unittest.TestCase):

    def test_store_row_floor_parses_object_snapshot_prefix(self):
        self.assertEqual(
            _store_row_floor("ITEM|x=1|y=2|floor=811|rest"),
            ("ITEM",811),
        )
        self.assertEqual(
            _store_row_floor("GOLD|floor=2020|x=1|y=2|100"),
            ("GOLD",2020),
        )
        self.assertIsNone(_store_row_floor("bad row"))

    def test_no_snapshot_closes_deterministic_initial_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            audit=analyze(
                coordinate_report_text=COORD,
                state_gated_report_text=STATE,
                legal_state_report_text=LEGAL,
                bundle_root=Path(td),
            )
        self.assertEqual(audit.normal_snapshot_files,())
        self.assertTrue(audit.recovered_persistent_critical_blocker_free)
        self.assertTrue(audit.deterministic_initial_runtime_witness)

    def test_critical_item_or_char_snapshot_blocks_strong_witness(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"itemgold"
            p.write_text(
                "ITEM|x=1|y=2|floor=811|opaque\n"
                "CHAR|x=3|y=4|floor=2020|opaque\n"
                "GOLD|x=5|y=6|floor=811|100\n",
                encoding="utf-8",
            )
            audit=analyze(
                coordinate_report_text=COORD,
                state_gated_report_text=STATE,
                legal_state_report_text=LEGAL,
                bundle_root=Path(td),
            )
        self.assertEqual(audit.critical_item_rows,1)
        self.assertEqual(audit.critical_char_rows,1)
        self.assertEqual(audit.critical_gold_rows,1)
        self.assertFalse(audit.recovered_persistent_critical_blocker_free)
        self.assertFalse(audit.deterministic_initial_runtime_witness)

    def test_noncritical_snapshot_objects_do_not_block_critical_chain(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td)/"itemgold").write_text(
                "ITEM|x=1|y=2|floor=999|opaque\n"
                "CHAR|x=3|y=4|floor=1000|opaque\n",
                encoding="utf-8",
            )
            audit=analyze(
                coordinate_report_text=COORD,
                state_gated_report_text=STATE,
                legal_state_report_text=LEGAL,
                bundle_root=Path(td),
            )
        self.assertEqual(audit.normal_snapshot_rows,2)
        self.assertTrue(audit.deterministic_initial_runtime_witness)


if __name__=="__main__":
    unittest.main()
