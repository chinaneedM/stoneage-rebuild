"""PET-DETAIL30 source-bounded 2016 PC template1 birth/upgrade baseline."""
import unittest

from tools.stoneage_pet_growth_model import (
    PetLevelGrowthRolls, advance_pet_growth, project_pet_birth,
)
from tools.stoneage_pet_detail30_base_panel import (
    project_pet_source_base_panel,
)


class SameCommitDescendantPanelTests(unittest.TestCase):
    def test_template1_birth_then_level2_panel(self):
        # 2016 community PC enemybase1 first row: INITNUM10, BASE20/12/15/25.
        # At level=1 the LVUPPOINT term is multiplied by 0; the supplied
        # zero is NOT a claim about the configuration's LVUPPOINT text.
        draw = (0,0,0,1,1,2,2,3,3,3)
        birth = project_pet_birth(
            template_base=(20,12,15,25),
            init_num=10, lvup_point=0, level=1,
            offsets=(-2,1,2,0), birth_rolls=draw,
        )
        self.assertEqual(birth.rank,5)
        self.assertEqual(birth.individualized_growth_base,(18,13,17,25))
        self.assertEqual(birth.packed_alloc_point,0x120d1119)
        self.assertEqual(birth.birth_allocation_counts,(3,2,2,3))
        self.assertEqual(birth.internal_stats,(210,150,190,280))
        self.assertEqual(
            project_pet_source_base_panel(birth.internal_stats).__dict__,
            {"max_hp":14,"attack":2,"defense":2,"quick":2},
        )
        growth = advance_pet_growth(
            growth_base=birth.individualized_growth_base,
            rank=birth.rank,
            current_internal_stats=birth.internal_stats,
            current_variable_ai=0,
            level_rolls=(PetLevelGrowthRolls(draw,550),),
        )
        self.assertEqual(growth.per_level_increments,((115,82,104,154),))
        self.assertEqual(growth.end_internal_stats,(325,232,294,434))
        self.assertEqual(growth.end_variable_ai,500)
        self.assertEqual(
            project_pet_source_base_panel(growth.end_internal_stats).__dict__,
            {"max_hp":22,"attack":3,"defense":3,"quick":4},
        )
        self.assertEqual(birth.individualized_growth_base,(18,13,17,25))

    def test_reject_invalid_base_input(self):
        for value in ((),(1,2,3),(1,2,3,4,5),(-1,2,3,4)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                project_pet_source_base_panel(value)

    def test_does_not_confuse_hidden_stats_with_panel(self):
        panel=project_pet_source_base_panel((210,150,190,280))
        self.assertNotEqual(
            (panel.max_hp,panel.attack,panel.defense,panel.quick),
            (210,150,190,280),
        )


if __name__=="__main__":
    unittest.main()
