import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_warpman_ingress_gate_probe import (
    DIALOGUE_OR_PAYMENT,
    NEW_EVENT_GATED_DIALOGUE,
    PLAIN_ALLFREE_DIALOGUE,
    TIME_GATED_DIALOGUE,
    _classify,
    analyze,
)


class _Orphan:
    def __init__(self, floor_id):
        self.floor_id = floor_id


class _Reachability:
    reached_floor_ids = frozenset({811})
    orphan_rows = (_Orphan(820),)


class WarpManIngressGateProbeTests(unittest.TestCase):

    def test_gate_classifier_keeps_time_new_event_and_payment_distinct(self):
        base = dict(
            free_present=True,
            allfree_present=True,
            payment_path_present=False,
            money_present=False,
            talk_event_present=False,
            warp_msg_present=False,
            over_marker_present=False,
        )
        self.assertEqual(
            _classify(new_warpman=False, newtime_present=False, **base),
            PLAIN_ALLFREE_DIALOGUE,
        )
        self.assertEqual(
            _classify(
                new_warpman=False,
                newtime_present=False,
                **{**base, "payment_path_present": True},
            ),
            DIALOGUE_OR_PAYMENT,
        )
        self.assertEqual(
            _classify(
                new_warpman=True,
                newtime_present=False,
                **{**base, "talk_event_present": True},
            ),
            NEW_EVENT_GATED_DIALOGUE,
        )
        self.assertEqual(
            _classify(new_warpman=False, newtime_present=True, **base),
            TIME_GATED_DIALOGUE,
        )

    @patch(
        "tools.stoneage_warpman_ingress_gate_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_fixture_reports_gate_shape_without_raw_condition_payload(
        self,
        _reachability,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "template").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=W\nFunctionSet=WarpMan\n}\n"
            )
            (root / "create").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=811\nBornCenter=1,1\n"
                b"Enemy=W|file:w.arg\n}\n"
            )
            (root / "w.arg").write_bytes(
                b"WARP:820,1,2;500,3,4\n"
                b"FREE:ALLFREE\n"
                b"FreeMsg:secret dialogue\n"
                b"CHECKPARTY:FALSE\n"
            )

            audit = analyze(root)
            self.assertEqual(len(audit.rows), 1)
            row = audit.rows[0]
            self.assertEqual(row.source_floor, 811)
            self.assertEqual(row.target_floor, 820)
            self.assertEqual(row.classification, PLAIN_ALLFREE_DIALOGUE)
            self.assertEqual(row.total_warp_candidates, 2)
            self.assertTrue(row.checkparty_explicit_false)


if __name__ == "__main__":
    unittest.main()
