import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from tools.stoneage_shadowed_branch_legal_state_reachability_probe import (
    ExchangeWitness,
    ReachabilityChainAudit,
    WarpGate,
    _distance,
    _event_gate_domain_satisfiable,
    _eventno_class,
    _reachable,
    _reward_units,
    emit,
)


class LegalStateReachabilityProbeTests(unittest.TestCase):

    def test_directed_floor_distance_and_closure(self):
        graph={1:{2},2:{3,4},4:{5}}
        self.assertEqual(_distance(graph,1,5),3)
        self.assertEqual(_distance(graph,5,1),-1)
        self.assertEqual(_reachable(graph,2),{2,3,4,5})

    def test_eventno_class_preserves_ungated_negative_sentinel(self):
        self.assertEqual(
            _eventno_class(b"TYPE:ACCEPT|EventNo:12|GetItem:20"),
            "NONNEGATIVE_FLAG",
        )
        self.assertEqual(
            _eventno_class(b"TYPE:ACCEPT|EventNo:-1|GetItem:20"),
            "NEGATIVE_SENTINEL",
        )
        self.assertTrue(
            _event_gate_domain_satisfiable("NEGATIVE_SENTINEL")
        )
        self.assertTrue(
            _event_gate_domain_satisfiable("NONNEGATIVE_FLAG")
        )
        self.assertFalse(
            _event_gate_domain_satisfiable("MISSING_OR_MULTIPLE")
        )

    def test_reward_units_counts_target_quantity_only(self):
        record=b"GetItem:20*2,30|GetItem:20"
        self.assertEqual(_reward_units(record,20),3)
        self.assertEqual(_reward_units(record,30),1)

    def test_emit_marks_closed_legal_state_chain(self):
        audit=ReachabilityChainAudit(
            gate=WarpGate(
                source_floor=811,
                destination_floor=820,
                joint_levels=(50,51),
            ),
            exchange_witnesses=(
                ExchangeWitness(
                    source_floor=2020,
                    joint_level_count=2,
                    reward_units=1,
                    keyword_present=False,
                    eventno_class="NONNEGATIVE_FLAG",
                    floor_path_length_to_ingress=7,
                    state_domain_satisfiable=True,
                ),
            ),
            branch_floor_ids=(820,821,822),
            branch_reached_from_entry=(820,821,822),
            missing_argument_files=0,
        )
        out=io.StringIO()
        with redirect_stdout(out):
            emit(audit)
        text=out.getvalue()
        self.assertIn("LEGAL_STATE_CHAIN|witness=1",text)
        self.assertIn("all_target_floors_reachable=1",text)
        self.assertNotIn("item_id=",text)


if __name__=="__main__":
    unittest.main()
