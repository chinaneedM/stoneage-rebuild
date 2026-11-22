import unittest

from tools.stoneage_player_growth_model import (
    LEGACY_CUMULATIVE_EXP,
    PER_LEVEL_EXP,
)
from tools.stoneage_pet_growth_model import (
    PetLevelGrowthRolls,
    VARIABLE_AI_LEVELUP_DELTA,
    advance_pet_growth,
    allocation_counts,
    individualize_growth_base,
    pack_growth_base,
    pet_level_increments,
    pet_rank_from_template_base,
    resolve_pet_exp_growth_transition,
    unpack_growth_base,
)


class PetGrowthModelTests(unittest.TestCase):
    def test_rank_thresholds(self):
        self.assertEqual(pet_rank_from_template_base(25,25,25,25),0)
        self.assertEqual(pet_rank_from_template_base(24,24,24,23),1)
        self.assertEqual(pet_rank_from_template_base(23,23,22,22),2)
        self.assertEqual(pet_rank_from_template_base(22,21,21,21),3)
        self.assertEqual(pet_rank_from_template_base(20,20,20,20),4)
        self.assertEqual(pet_rank_from_template_base(10,10,10,10),5)

    def test_pack_roundtrip(self):
        base=(21,22,23,24)
        self.assertEqual(unpack_growth_base(pack_growth_base(*base)),base)

    def test_birth_offsets(self):
        self.assertEqual(
            individualize_growth_base((20,20,20,20),(-2,-1,1,2)),
            (18,19,21,22),
        )
        with self.assertRaises(ValueError):
            individualize_growth_base((20,20,20,20),(-3,0,0,0))

    def test_ten_rolls_always_sum_to_ten(self):
        counts=allocation_counts([0,0,0,1,1,2,2,2,3,3])
        self.assertEqual(counts,(3,2,3,2))
        self.assertEqual(sum(counts),10)

    def test_level_increment_uses_base_plus_allocations_times_rank_roll(self):
        increments=pet_level_increments(
            growth_base=(20,20,20,20),
            rank=0,
            allocation_rolls=[0,0,0,1,1,2,2,2,3,3],
            rank_roll=500,
        )
        self.assertEqual(increments,(115,110,115,110))

    def test_multi_level_growth_consumes_one_explicit_roll_bundle_per_level(self):
        transition=advance_pet_growth(
            growth_base=(20,20,20,20),
            rank=0,
            current_internal_stats=(2000,2000,2000,2000),
            current_variable_ai=0,
            level_rolls=(
                PetLevelGrowthRolls(
                    (0,0,0,1,1,2,2,2,3,3),
                    500,
                ),
                PetLevelGrowthRolls(
                    (3,3,3,2,2,1,1,1,0,0),
                    450,
                ),
            ),
        )
        self.assertEqual(
            transition.per_level_increments,
            ((115,110,115,110),(99,103,99,103)),
        )
        self.assertEqual(
            transition.end_internal_stats,
            (2214,2213,2214,2213),
        )
        self.assertEqual(transition.levels_gained,2)
        self.assertEqual(
            transition.end_variable_ai,
            2*VARIABLE_AI_LEVELUP_DELTA,
        )

    def test_variable_ai_levelup_delta_clamps_at_stable_limit(self):
        transition=advance_pet_growth(
            growth_base=(20,20,20,20),
            rank=0,
            current_internal_stats=(2000,2000,2000,2000),
            current_variable_ai=9800,
            level_rolls=(
                PetLevelGrowthRolls((0,0,0,1,1,2,2,2,3,3),500),
            ),
        )
        self.assertEqual(transition.end_variable_ai,10000)
    def test_legacy_pet_exp_crossing_keeps_cumulative_exp_and_applies_growth(self):
        transition=resolve_pet_exp_growth_transition(
            4,10,490,500,
            profile=LEGACY_CUMULATIVE_EXP,
            next_max_exp_by_level={5:900},
            growth_base=(18,19,21,22),
            rank=4,
            current_internal_stats=(1800,1900,2100,2200),
            current_variable_ai=0,
            level_rolls=(
                PetLevelGrowthRolls(
                    (0,0,0,1,1,2,2,2,3,3),
                    530,
                ),
            ),
        )
        self.assertEqual(
            (transition.end_level,transition.end_exp,transition.next_max_exp),
            (5,500,900),
        )
        self.assertEqual(transition.levels_gained,1)
        self.assertEqual(
            transition.growth.end_internal_stats,
            (1911,2011,2227,2327),
        )
        self.assertEqual(transition.growth.end_variable_ai,500)

    def test_per_level_pet_exp_crossing_consumes_requirement(self):
        transition=resolve_pet_exp_growth_transition(
            4,10,490,500,
            profile=PER_LEVEL_EXP,
            next_max_exp_by_level={5:400},
            growth_base=(18,19,21,22),
            rank=4,
            current_internal_stats=(1800,1900,2100,2200),
            current_variable_ai=0,
            level_rolls=(
                PetLevelGrowthRolls(
                    (0,0,0,1,1,2,2,2,3,3),
                    530,
                ),
            ),
        )
        self.assertEqual(
            (transition.end_level,transition.end_exp,transition.next_max_exp),
            (5,0,400),
        )

    def test_pet_exp_transition_has_no_implicit_growth_rng(self):
        with self.assertRaisesRegex(ValueError,'exactly one growth roll bundle'):
            resolve_pet_exp_growth_transition(
                4,10,490,500,
                profile=LEGACY_CUMULATIVE_EXP,
                next_max_exp_by_level={5:900},
                growth_base=(18,19,21,22),
                rank=4,
                current_internal_stats=(1800,1900,2100,2200),
                current_variable_ai=0,
                level_rolls=(),
            )
        with self.assertRaisesRegex(ValueError,'exactly one growth roll bundle'):
            resolve_pet_exp_growth_transition(
                4,10,100,500,
                profile=LEGACY_CUMULATIVE_EXP,
                next_max_exp_by_level={},
                growth_base=(18,19,21,22),
                rank=4,
                current_internal_stats=(1800,1900,2100,2200),
                current_variable_ai=0,
                level_rolls=(
                    PetLevelGrowthRolls((0,)*10,530),
                ),
            )

    def test_rank_range_validation(self):
        with self.assertRaises(ValueError):
            pet_level_increments((20,20,20,20),5,[0]*10,549)
        self.assertEqual(
            pet_level_increments((20,20,20,20),5,[0]*10,550)[0],
            165,
        )


class PetDetail30SameSourcePanelTests(unittest.TestCase):
    """2016 PC template1, explicit simulated RNG; no early official claim."""

    def test_template1_birth_then_levelup_baseline_panel(self):
        from tools.stoneage_pet_growth_model import (
            project_pet_birth, project_pet_source_base_panel,
        )
        # Actual later-PC enemybase1 template1 has INITNUM=10 and four
        # base bytes 20/12/15/25, graphic100250. The Lv1 term makes
        # LVUPPOINT irrelevant; zero here is NOT the template's field.
        draws = (0,0,0,1,1,2,2,3,3,3)
        birth = project_pet_birth(
            template_base=(20,12,15,25),
            init_num=10,
            lvup_point=0,
            level=1,
            offsets=(-2,1,2,0),
            birth_rolls=draws,
        )
        self.assertEqual(birth.rank, 5)
        self.assertEqual(birth.individualized_growth_base,(18,13,17,25))
        self.assertEqual(birth.packed_alloc_point,0x120d1119)
        self.assertEqual(birth.birth_allocation_counts,(3,2,2,3))
        self.assertEqual(birth.internal_stats,(210,150,190,280))
        born_panel=project_pet_source_base_panel(birth.internal_stats)
        self.assertEqual(
            (born_panel.max_hp,born_panel.attack,born_panel.defense,born_panel.quick),
            (14,2,2,2),
        )

        levelup=advance_pet_growth(
            growth_base=birth.individualized_growth_base,
            rank=birth.rank,
            current_internal_stats=birth.internal_stats,
            current_variable_ai=0,
            level_rolls=(PetLevelGrowthRolls(draws,550),),
        )
        self.assertEqual(levelup.per_level_increments,((115,82,104,154),))
        self.assertEqual(levelup.end_internal_stats,(325,232,294,434))
        self.assertEqual(levelup.end_variable_ai,500)
        after_panel=project_pet_source_base_panel(levelup.end_internal_stats)
        self.assertEqual(
            (after_panel.max_hp,after_panel.attack,after_panel.defense,after_panel.quick),
            (22,3,3,4),
        )
        # Lv-up neither rerolls stored base nor ranks this individual again.
        self.assertEqual(birth.individualized_growth_base,(18,13,17,25))
        self.assertEqual(birth.rank,5)

    def test_base_panel_rejects_invalid_vectors(self):
        from tools.stoneage_pet_growth_model import project_pet_source_base_panel
        for value in ((),(1,2,3),(1,2,3,4,5),(-1,2,3,4)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                project_pet_source_base_panel(value)

    def test_baseline_panel_is_not_raw_internal_values(self):
        from tools.stoneage_pet_growth_model import project_pet_source_base_panel
        output = project_pet_source_base_panel((210,150,190,280))
        self.assertNotEqual(output.max_hp,210)
        self.assertNotEqual(output.attack,150)
        self.assertNotEqual(output.defense,190)
        self.assertNotEqual(output.quick,280)



if __name__=="__main__":
    unittest.main()
