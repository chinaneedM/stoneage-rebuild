import unittest

from tools.stoneage_shadowed_branch_fresh_start_spatial_probe import (
    FreshStartFloorAudit,
    SpawnFloorWitness,
    _award_floor,
    _shortest_path,
)


LEGAL="""StoneAge shadowed-branch legal-state reachability audit — R1
EXCHANGE_CHAIN_WITNESS|ordinal=1|source_floor=2020|joint_level_values=20|reward_units=1
EXCHANGE_CHAIN_WITNESS|ordinal=2|source_floor=2020|joint_level_values=20|reward_units=1
RESOLUTION|SHADOWED_BRANCH_LEGAL_STATE_REACHABILITY_AUDITED
"""


class FreshStartSpatialProbeTests(unittest.TestCase):

    def test_award_floor_requires_single_floor(self):
        self.assertEqual(_award_floor(LEGAL),2020)
        with self.assertRaises(ValueError):
            _award_floor(
                LEGAL.replace(
                    "ordinal=2|source_floor=2020",
                    "ordinal=2|source_floor=9999",
                )
            )

    def test_shortest_directed_path(self):
        graph={1:(2,3),2:(4,),3:(5,),5:(4,)}
        self.assertEqual(_shortest_path(graph,1,4),(1,2,4))
        self.assertIsNone(_shortest_path(graph,4,1))

    def test_audit_closure_distinguishes_normal_and_variants(self):
        audit=FreshStartFloorAudit(
            award_floor=9,
            witnesses=(
                SpawnFloorWitness(1,"NORMAL_HOMETOWN",(1,9)),
                SpawnFloorWitness(2,"NORMAL_HOMETOWN",(2,3,9)),
                SpawnFloorWitness(8,"LATER_VARIANT",None),
            ),
        )
        self.assertTrue(audit.normal_closed)
        self.assertFalse(audit.all_source_known_closed)


if __name__=="__main__":
    unittest.main()
