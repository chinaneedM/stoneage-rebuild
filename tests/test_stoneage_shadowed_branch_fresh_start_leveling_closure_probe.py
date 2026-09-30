import unittest

from tools.stoneage_shadowed_branch_fresh_start_leveling_closure_probe import (
    LevelingClosureAudit,
    _ordered_area_point,
)


class _Map:
    width=4
    height=3


class _Nav:
    def __init__(self,labels):
        self.map=_Map()
        self.labels=dict(labels)

    def component(self,point):
        return self.labels.get(tuple(point))


class FreshStartLevelingClosureProbeTests(unittest.TestCase):

    def test_ordered_area_point_joins_before_and_after_components(self):
        origin=_Nav({(0,0):1,(1,0):1,(2,0):2})
        continuation=_Nav({(0,0):7,(1,0):8,(2,0):8})
        area={"x1":0,"y1":0,"x2":2,"y2":0}
        self.assertEqual(
            _ordered_area_point(origin,{1},continuation,{8},area),
            (1,0),
        )

    def test_ordered_area_point_rejects_independent_reachability(self):
        origin=_Nav({(0,0):1,(1,0):1})
        continuation=_Nav({(0,0):7,(1,0):7})
        area={"x1":0,"y1":0,"x2":1,"y2":0}
        self.assertIsNone(
            _ordered_area_point(origin,{1},continuation,{8},area)
        )

    def test_closure_requires_reward_chain_and_ordered_combat_source(self):
        closed=LevelingClosureAudit(
            combat_witness_variants=3,
            ordered_source_to_award_witnesses=1,
            ordered_source_hometowns=1,
            ambiguous_encounter_keys=0,
            unresolved_reverse_map_floors=0,
            leveling_reward_chain=True,
        )
        self.assertTrue(closed.leveling_to_target)
        self.assertFalse(
            LevelingClosureAudit(
                combat_witness_variants=3,
                ordered_source_to_award_witnesses=0,
                ordered_source_hometowns=0,
                ambiguous_encounter_keys=0,
                unresolved_reverse_map_floors=0,
                leveling_reward_chain=True,
            ).leveling_to_target
        )


if __name__=="__main__":
    unittest.main()
