import unittest

from tools.stoneage_enemy_spawn_model import (
    EnemyBirthRolls,
    SIZE_BIG,
    SIZE_NORMAL,
    effective_spawn_capacity,
    materialize_spawn_plan,
    plan_enemy_spawns,
)
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def enemy(enemy_id, tempno, *, create_max, create_min=1, lv_min=3, lv_max=4):
    return EnemyVariantBridge.from_enemy(
        {
            "ID": enemy_id,
            "TEMPNO": tempno,
            "LV_MIN": lv_min,
            "LV_MAX": lv_max,
            "CREATEMAXNUM": create_max,
            "CREATEMINNUM": create_min,
            "TACTICS": 1,
            "EXP": 100,
            "DUELPOINT": 0,
            "STYLE": 0,
            "PETFLG": 1,
        }
    )


def template(tempno, name, *, size=SIZE_NORMAL):
    return PetTemplateBridge.from_enemybase(
        {
            "NAME": name,
            "TEMPNO": tempno,
            "INITNUM": 100,
            "LVUPPOINT": 5,
            "BASEVITAL": 20,
            "BASESTR": 20,
            "BASETGH": 20,
            "BASEDEX": 20,
            "IMGNUMBER": 10000 + tempno,
            "MODAI": 4,
            "EARTHAT": 50,
            "WATERAT": 50,
            "FIREAT": 0,
            "WINDAT": 0,
            "SLOT": 4,
            "SIZE": size,
        }
    )


def area(enemy_max=10):
    return EncounterAreaBridge.from_encount(
        {
            "INDEX": 21,
            "FLOOR": 1000,
            "X1": 0,
            "Y1": 0,
            "X2": 20,
            "Y2": 20,
            "PROB_MIN": 10,
            "PROB_MAX": 20,
            "ENEMY_MAX": enemy_max,
            "ZORDER": 1,
        }
    )


class EnemySpawnModelTests(unittest.TestCase):
    def test_effective_capacity_uses_area_max_and_sum_of_slot_create_max(self):
        enemies = {
            700: enemy(700, 88, create_max=2),
            701: enemy(701, 89, create_max=4),
        }
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 70,
                "ENEMY_ID2": 701,
                "CREATE_PROB2": 30,
            }
        )
        self.assertEqual(
            effective_spawn_capacity(area(5), group, enemies),
            5,
        )
        self.assertEqual(
            effective_spawn_capacity(area(10), group, enemies),
            6,
        )

    def test_each_spawn_slot_is_weighted_again_and_create_max_rejections_consume_rolls(self):
        enemies = {
            700: enemy(700, 88, create_max=2),
            701: enemy(701, 89, create_max=4),
        }
        templates = {
            88: template(88, "Wolf"),
            89: template(89, "Tiger"),
        }
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 70,
                "ENEMY_ID2": 701,
                "CREATE_PROB2": 30,
            }
        )
        plan = plan_enemy_spawns(
            area(5),
            group,
            enemies,
            templates,
            entry_count_roll=5,
            selection_rolls=(0, 0, 0, 99, 99, 99),
        )
        self.assertEqual(plan.initial_target_count, 5)
        self.assertEqual(plan.actual_count, 5)
        self.assertEqual(plan.selection_attempts, 6)
        self.assertEqual(
            tuple(v.enemy_id for v in plan.variants),
            (700, 700, 701, 701, 701),
        )

    def test_duplicate_group_slots_multiply_same_variant_capacity(self):
        enemies = {700: enemy(700, 88, create_max=1)}
        templates = {88: template(88, "Wolf")}
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 50,
                "ENEMY_ID2": 700,
                "CREATE_PROB2": 50,
            }
        )
        plan = plan_enemy_spawns(
            area(5),
            group,
            enemies,
            templates,
            entry_count_roll=2,
            selection_rolls=(0, 99),
        )
        self.assertEqual(plan.actual_count, 2)
        self.assertEqual(tuple(v.enemy_id for v in plan.variants), (700, 700))

    def test_create_min_is_declared_but_not_enforced_by_fixed_spawn_core(self):
        enemies = {
            700: enemy(700, 88, create_max=5, create_min=4),
        }
        templates = {88: template(88, "Wolf")}
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            }
        )
        plan = plan_enemy_spawns(
            area(5),
            group,
            enemies,
            templates,
            entry_count_roll=1,
            selection_rolls=(0,),
        )
        self.assertEqual(enemies[700].create_min_declared, 4)
        self.assertFalse(plan.create_min_enforced)
        self.assertEqual(plan.actual_count, 1)

    def test_sixth_big_enemy_reduces_target_count(self):
        enemies = {700: enemy(700, 88, create_max=10)}
        templates = {88: template(88, "Big", size=SIZE_BIG)}
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            }
        )
        plan = plan_enemy_spawns(
            area(10),
            group,
            enemies,
            templates,
            entry_count_roll=6,
            selection_rolls=(0, 0, 0, 0, 0, 0),
        )
        self.assertEqual(plan.initial_target_count, 6)
        self.assertEqual(plan.final_target_count, 5)
        self.assertEqual(plan.actual_count, 5)

    def test_big_enemy_after_first_five_swaps_with_normal_front_slot(self):
        enemies = {
            700: enemy(700, 88, create_max=5),
            701: enemy(701, 89, create_max=1),
        }
        templates = {
            88: template(88, "Normal", size=SIZE_NORMAL),
            89: template(89, "Big", size=SIZE_BIG),
        }
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 50,
                "ENEMY_ID2": 701,
                "CREATE_PROB2": 50,
            }
        )
        plan = plan_enemy_spawns(
            area(6),
            group,
            enemies,
            templates,
            entry_count_roll=6,
            selection_rolls=(0, 0, 0, 0, 0, 50),
        )
        self.assertEqual(plan.actual_count, 6)
        self.assertEqual(plan.variants[0].enemy_id, 701)
        self.assertEqual(
            tuple(v.enemy_id for v in plan.variants[1:]),
            (700, 700, 700, 700, 700),
        )

    def test_spawn_layout_requires_explicit_size_metadata(self):
        enemies = {700: enemy(700, 88, create_max=1)}
        templates = {
            88: PetTemplateBridge.from_enemybase(
                {
                    "NAME": "Unknown Size",
                    "TEMPNO": 88,
                    "INITNUM": 100,
                    "LVUPPOINT": 5,
                    "BASEVITAL": 20,
                    "BASESTR": 20,
                    "BASETGH": 20,
                    "BASEDEX": 20,
                    "IMGNUMBER": 10088,
                    "MODAI": 4,
                    "EARTHAT": 50,
                    "WATERAT": 50,
                    "FIREAT": 0,
                    "WINDAT": 0,
                    "SLOT": 4,
                }
            )
        }
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            }
        )
        with self.assertRaises(ValueError):
            plan_enemy_spawns(
                area(1),
                group,
                enemies,
                templates,
                entry_count_roll=1,
                selection_rolls=(0,),
            )

    def test_birth_materialization_is_independent_for_each_selected_enemy(self):
        enemies = {
            700: enemy(700, 88, create_max=1, lv_min=3, lv_max=4),
            701: enemy(701, 89, create_max=1, lv_min=5, lv_max=5),
        }
        templates = {
            88: template(88, "Wolf"),
            89: template(89, "Tiger"),
        }
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 50,
                "ENEMY_ID2": 701,
                "CREATE_PROB2": 50,
            }
        )
        plan = plan_enemy_spawns(
            area(2),
            group,
            enemies,
            templates,
            entry_count_roll=2,
            selection_rolls=(0, 50),
        )
        spawned = materialize_spawn_plan(
            plan,
            templates,
            birth_rolls=(
                EnemyBirthRolls(
                    level_roll=1,
                    birth_offsets=(-2, -1, 0, 1),
                    spawn_allocation_rolls=(0, 0, 1, 1, 2, 2, 3, 3, 0, 1),
                ),
                EnemyBirthRolls(
                    level_roll=0,
                    birth_offsets=(2, 1, 0, -1),
                    spawn_allocation_rolls=(3, 3, 2, 2, 1, 1, 0, 0, 3, 2),
                ),
            ),
        )
        self.assertEqual(tuple(x.participant.level for x in spawned), (4, 5))
        self.assertEqual(
            tuple(x.participant.source_variant_id for x in spawned),
            (700, 701),
        )
        self.assertEqual(
            tuple(x.participant.name for x in spawned),
            ("Wolf", "Tiger"),
        )
        self.assertNotEqual(
            spawned[0].birth.individualized_growth_base,
            spawned[1].birth.individualized_growth_base,
        )

    def test_insufficient_selection_rolls_are_not_silently_filled(self):
        enemies = {700: enemy(700, 88, create_max=2)}
        templates = {88: template(88, "Wolf")}
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            }
        )
        with self.assertRaises(ValueError):
            plan_enemy_spawns(
                area(2),
                group,
                enemies,
                templates,
                entry_count_roll=2,
                selection_rolls=(0,),
            )


if __name__ == "__main__":
    unittest.main()
