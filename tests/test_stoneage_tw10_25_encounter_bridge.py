import unittest

from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
    active_encounter_area,
    choose_enemy,
    choose_group,
    effective_enemy_count_limit,
    weighted_choice,
)


def enemy_row(enemy_id, tempno, *, lv_min=1, lv_max=1, create_max=1, petflg=1):
    return {
        "ID": enemy_id,
        "TEMPNO": tempno,
        "LV_MIN": lv_min,
        "LV_MAX": lv_max,
        "CREATEMAXNUM": create_max,
        "CREATEMINNUM": 1,
        "TACTICS": 1,
        "EXP": -1,
        "DUELPOINT": 0,
        "STYLE": 0,
        "PETFLG": petflg,
    }


class Taiwan25EncounterBridgeTests(unittest.TestCase):
    def test_enemy_variant_keeps_enemy_and_enemybase_identities_distinct(self):
        enemy = EnemyVariantBridge.from_enemy(
            enemy_row(700, 88, lv_min=5, lv_max=3, create_max=4)
        )
        self.assertEqual((enemy.level_min, enemy.level_max), (3, 5))
        self.assertEqual(enemy.variant_ref.namespace, "enemy.ID")
        self.assertEqual(enemy.variant_ref.template_id, 700)
        self.assertEqual(enemy.pet_template_ref.namespace, "enemybase.TEMPNO")
        self.assertEqual(enemy.pet_template_ref.template_id, 88)
        self.assertEqual(enemy.choose_level(0), 3)
        self.assertEqual(enemy.choose_level(2), 5)
        with self.assertRaises(ValueError):
            enemy.choose_level(3)

    def test_enemy_variant_preserves_ten_item_probability_slots(self):
        row=enemy_row(700,88)
        row.update({
            "ITEM1":501,
            "ITEMPROB1":125,
            "ITEM10":999,
            "ITEMPROB10":1000,
        })
        enemy=EnemyVariantBridge.from_enemy(row)
        self.assertEqual(len(enemy.drop_slots),10)
        self.assertEqual(enemy.drop_slots[0],(501,125))
        self.assertEqual(enemy.drop_slots[1],(-1,0))
        self.assertEqual(enemy.drop_slots[9],(999,1000))

    def test_group_accepts_exact_recovered_probe_field_names(self):
        row = {
            "GROUP_ID": 100,
            "APPEAR_ITEM": 500,
            "NOT_APPEAR_ITEM": 600,
            "ENEMY_ID1": 700,
            "CREATE_PROB1": 70,
            "ENEMY_ID2": 701,
            "CREATE_PROB2": 30,
        }
        group = GroupBridge.from_group(row)
        self.assertEqual(group.appear_by_item_id, 500)
        self.assertEqual(group.not_appear_by_item_id, 600)
        self.assertEqual(group.enemy_slots[:2], ((700, 70), (701, 30)))
        self.assertTrue(group.is_eligible((500,)))
        self.assertFalse(group.is_eligible(()))
        self.assertFalse(group.is_eligible((500, 600)))

    def test_group_resolver_rejects_unresolved_positive_identity(self):
        group = GroupBridge.from_group(
            {
                "GROUP_ID": 100,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            }
        )
        with self.assertRaises(KeyError):
            group.resolved_enemy_choices({})

    def test_encounter_accepts_exact_recovered_probe_field_names(self):
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21,
                "FLOOR": 1000,
                "X1": 20,
                "Y1": 30,
                "X2": 10,
                "Y2": 5,
                "PROB_MIN": 10,
                "PROB_MAX": 20,
                "ENEMY_MAX": 6,
                "ZORDER": 3,
                "GROUP_ID1": 100,
                "GROUP_PROB1": 80,
                "GROUP_ID2": 101,
                "GROUP_PROB2": 20,
            }
        )
        self.assertEqual((area.min_x, area.min_y, area.max_x, area.max_y), (10, 5, 20, 30))
        self.assertEqual((area.probability_min, area.probability_max), (10, 20))
        self.assertEqual(area.enemy_max_num, 6)
        self.assertTrue(area.contains(1000, 15, 10))
        self.assertFalse(area.contains(1001, 15, 10))

    def test_zorder_selects_highest_matching_area(self):
        low = EncounterAreaBridge.from_encount(
            {
                "INDEX": 1, "FLOOR": 1, "X1": 0, "Y1": 0, "X2": 10, "Y2": 10,
                "PROB_MIN": 0, "PROB_MAX": 10, "ENEMY_MAX": 3, "ZORDER": 1,
            }
        )
        high = EncounterAreaBridge.from_encount(
            {
                "INDEX": 2, "FLOOR": 1, "X1": 0, "Y1": 0, "X2": 10, "Y2": 10,
                "PROB_MIN": 0, "PROB_MAX": 10, "ENEMY_MAX": 3, "ZORDER": 5,
            }
        )
        self.assertEqual(
            active_encounter_area((low, high), floor=1, x=5, y=5).index,
            2,
        )

    def test_weighted_group_then_enemy_selection_stays_two_stage(self):
        e700 = EnemyVariantBridge.from_enemy(enemy_row(700, 88, create_max=2))
        e701 = EnemyVariantBridge.from_enemy(enemy_row(701, 89, create_max=4))
        enemies = {700: e700, 701: e701}
        g100 = GroupBridge.from_group(
            {"GROUP_ID": 100, "ENEMY_ID1": 700, "CREATE_PROB1": 100}
        )
        g101 = GroupBridge.from_group(
            {"GROUP_ID": 101, "ENEMY_ID1": 701, "CREATE_PROB1": 100}
        )
        groups = {100: g100, 101: g101}
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21, "FLOOR": 1, "X1": 0, "Y1": 0, "X2": 10, "Y2": 10,
                "PROB_MIN": 0, "PROB_MAX": 10, "ENEMY_MAX": 5, "ZORDER": 1,
                "GROUP_ID1": 100, "GROUP_PROB1": 30,
                "GROUP_ID2": 101, "GROUP_PROB2": 70,
            }
        )
        self.assertEqual(choose_group(area, groups, roll=0).group_id, 100)
        selected_group = choose_group(area, groups, roll=99)
        self.assertEqual(selected_group.group_id, 101)
        self.assertEqual(choose_enemy(selected_group, enemies, roll=0).enemy_id, 701)

    def test_positive_weight_unresolved_group_is_hard_error(self):
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21, "FLOOR": 1, "X1": 0, "Y1": 0, "X2": 10, "Y2": 10,
                "PROB_MIN": 0, "PROB_MAX": 10, "ENEMY_MAX": 5, "ZORDER": 1,
                "GROUP_ID1": 9999, "GROUP_PROB1": 10,
            }
        )
        with self.assertRaises(KeyError):
            area.resolved_group_choices({}, ())

    def test_effective_enemy_count_limit_uses_area_and_create_max(self):
        area = EncounterAreaBridge.from_encount(
            {
                "INDEX": 21, "FLOOR": 1, "X1": 0, "Y1": 0, "X2": 10, "Y2": 10,
                "PROB_MIN": 0, "PROB_MAX": 10, "ENEMY_MAX": 5, "ZORDER": 1,
            }
        )
        enemies = (
            EnemyVariantBridge.from_enemy(enemy_row(700, 88, create_max=2)),
            EnemyVariantBridge.from_enemy(enemy_row(701, 89, create_max=9)),
        )
        self.assertEqual(effective_enemy_count_limit(area, enemies), 5)

    def test_weighted_choice_rejects_out_of_range_roll(self):
        self.assertEqual(weighted_choice((("a", 2), ("b", 3)), 0), "a")
        self.assertEqual(weighted_choice((("a", 2), ("b", 3)), 4), "b")
        with self.assertRaises(ValueError):
            weighted_choice((("a", 2), ("b", 3)), 5)


if __name__ == "__main__":
    unittest.main()
