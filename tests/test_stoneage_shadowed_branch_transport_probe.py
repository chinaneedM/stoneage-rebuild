import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_shadowed_branch_transport_probe import (
    AIRPLANE,
    FMWARPMAN,
    WARPMAN,
    _airplane_floor_transitions,
    _fmwarpman_destinations,
    _warpman_destinations,
    analyze,
)


class _Orphan:
    def __init__(self, floor_id):
        self.floor_id = floor_id


class _Reachability:
    reached_floor_ids = frozenset({100, 810})
    orphan_rows = (_Orphan(829), _Orphan(831))


class ShadowedBranchTransportProbeTests(unittest.TestCase):

    def test_destination_parsers_follow_closed_source_shapes(self):
        self.assertEqual(
            _warpman_destinations(
                b"WARP:829,1,2;831,3,4|FREE:1"
            ),
            (829, 831),
        )
        self.assertEqual(
            _fmwarpman_destinations(
                b"WARP1:829,5,6|WARP2:831,7,8|ID:1"
            ),
            (829, 831),
        )
        self.assertEqual(
            _airplane_floor_transitions(
                source_floor=100,
                data=b"routenum:1|routeto1:100,1,1;829,2,2;831,3,3",
            ),
            ((100, 829), (829, 831)),
        )

    @patch(
        "tools.stoneage_shadowed_branch_transport_probe."
        "load_ordered_runtime_reachability",
        return_value=_Reachability(),
    )
    def test_realistic_npc_fixture_finds_only_reachable_to_shadowed_ingress(
        self,
        _runtime,
    ):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "templates").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=W\nFunctionSet=WarpMan\n}\n"
                b"{\nTemplateName=F\nFunctionSet=FMWarpMan\n}\n"
                b"{\nTemplateName=A\nFunctionSet=Airplane\n}\n"
                b"{\nTemplateName=B\nFunctionSet=Bus\n}\n"
            )
            (root / "creates").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=100\nBornCenter=1,1\nEnemy=W|file:w.arg\n}\n"
                b"{\nFloorId=810\nBornCenter=1,1\nEnemy=F|file:f.arg\n}\n"
                b"{\nFloorId=100\nBornCenter=1,1\nEnemy=A|file:a.arg\n}\n"
                b"{\nFloorId=100\nBornCenter=1,1\nEnemy=B|file:b.arg\n}\n"
            )
            (root / "w.arg").write_bytes(b"WARP:829,1,2;500,3,4\n")
            (root / "f.arg").write_bytes(
                b"WARP1:831,1,1\nWARP2:500,2,2\nID:1\n"
            )
            (root / "a.arg").write_bytes(
                b"routenum:1\nrouteto1:100,1,1;829,2,2;831,3,3\n"
            )
            (root / "b.arg").write_bytes(
                b"routenum:1\nrouteto1:1,1;2,2\n"
            )

            audit = analyze(root)
            ingress = {
                (edge.kind, edge.source_floor, edge.destination_floor)
                for edge in audit.potential_ingress
            }
            self.assertEqual(
                ingress,
                {
                    (WARPMAN, 100, 829),
                    (FMWARPMAN, 810, 831),
                    (AIRPLANE, 100, 829),
                },
            )
            self.assertEqual(audit.counts["Bus:refs"], 1)
            self.assertEqual(audit.counts["bus_cross_floor_edges"], 0)

    def test_airplane_chain_does_not_fake_reachability_of_later_route_leg(self):
        # Reachability is evaluated against the canonical classic-Warp closure
        # for each derived edge. A route leg starting on a currently shadowed
        # floor is not reported as ingress just because an earlier leg might
        # hypothetically carry the vehicle there.
        edges = _airplane_floor_transitions(
            source_floor=100,
            data=b"routenum:1|routeto1:829,1,1;831,2,2",
        )
        self.assertEqual(edges, ((100, 829), (829, 831)))


if __name__ == "__main__":
    unittest.main()
