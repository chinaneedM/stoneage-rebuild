import unittest

from tools.stoneage_enemy_rehp_probe import (
    analyze_rehp_domain,
    minimum_birth_max_hp,
)
from tools.stoneage_tw10_25_bridge_model import PetTemplateBridge


def template_row(
    tempno,
    skills=(),
    *,
    init=100,
    lvup=5,
    vital=20,
    strength=20,
    tough=20,
    dex=20,
):
    row = {
        "TEMPNO": tempno,
        "IMGNUMBER": 1000 + tempno,
        "MODAI": 1,
        "EARTHAT": 25,
        "WATERAT": 25,
        "FIREAT": 25,
        "WINDAT": 25,
        "SLOT": 7,
        "INITNUM": init,
        "LVUPPOINT": lvup,
        "BASEVITAL": vital,
        "BASESTR": strength,
        "BASETGH": tough,
        "BASEDEX": dex,
        "GET": 0,
        "RARE": 0,
        "SIZE": 0,
    }
    for index in range(1, 8):
        row[f"PETSKILL{index}"] = (
            skills[index - 1] if index <= len(skills) else -1
        )
    return row


def enemy(enemy_id, tempno, lo=1, hi=1, create_max=5):
    return {
        "id": enemy_id,
        "tempno": tempno,
        "lv_min": lo,
        "lv_max": hi,
        "create_max": create_max,
    }


def group(group_id, pairs):
    pairs = tuple(pairs)
    pairs = pairs + ((-1, -1),) * (10 - len(pairs))
    return {
        "id": group_id,
        "enemyids": tuple(enemy_id for enemy_id, _ in pairs),
        "enemyprobs": tuple(weight for _, weight in pairs),
    }


class EnemyReHpProbeTests(unittest.TestCase):
    def test_minimum_birth_hp_uses_low_offsets_and_nonvital_allocation(self):
        template = PetTemplateBridge.from_enemybase(template_row(10))
        result = minimum_birth_max_hp(
            template,
            level_min=1,
            level_max=3,
        )
        self.assertEqual(result["level"], 1)
        self.assertEqual(
            result["birth_offsets"],
            (-2, -2, -2, -2),
        )
        self.assertEqual(
            result["allocation_counts"],
            (0, 10, 0, 0),
        )
        # scale=100, bases become (18,28,18,18):
        # 4*18+28+18+18=136
        self.assertEqual(result["max_hp"], 136)

    def test_graph_counts_rehp_refs_and_cogroup_target_domain(self):
        rows = [
            template_row(10, (77, 77)),
            template_row(
                20,
                (),
                init=50,
                vital=12,
                strength=12,
                tough=12,
                dex=12,
            ),
            template_row(
                30,
                (),
                init=100,
                vital=30,
                strength=30,
                tough=30,
                dex=30,
            ),
        ]
        enemies = [
            enemy(100, 10),
            enemy(200, 20),
            enemy(300, 30),
        ]
        groups = [
            group(1, ((100, 50), (200, 50))),
            group(2, ((300, 100),)),
        ]
        result = analyze_rehp_domain(
            rehp_skill_ids=(77,),
            enemybase_rows=rows,
            enemy_rows=enemies,
            group_rows=groups,
        )
        self.assertEqual(result["rehp_slot_refs"], 2)
        self.assertEqual(result["rehp_tempnos"], (10,))
        self.assertEqual(result["caster_variant_ids"], (100,))
        self.assertEqual(result["rehp_group_ids"], (1,))
        self.assertEqual(
            result["target_variant_ids"],
            (100, 200),
        )
        self.assertNotIn(300, result["variant_minima"])

    def test_domain_marks_rand_lower_bound_unsafe_when_target_below_100(self):
        rows = [
            template_row(10, (77,)),
            template_row(
                20,
                (),
                init=10,
                lvup=1,
                vital=3,
                strength=3,
                tough=3,
                dex=3,
            ),
        ]
        result = analyze_rehp_domain(
            rehp_skill_ids=(77,),
            enemybase_rows=rows,
            enemy_rows=(
                enemy(100, 10),
                enemy(200, 20),
            ),
            group_rows=(
                group(
                    1,
                    ((100, 50), (200, 50)),
                ),
            ),
        )
        self.assertLess(
            result["minimum_target_max_hp"],
            100,
        )
        self.assertFalse(result["rand_power_domain_safe"])

    def test_zero_weight_cogroup_entry_is_not_a_reachable_target(self):
        rows = [
            template_row(10, (77,)),
            template_row(20),
        ]
        result = analyze_rehp_domain(
            rehp_skill_ids=(77,),
            enemybase_rows=rows,
            enemy_rows=(
                enemy(100, 10),
                enemy(200, 20),
            ),
            group_rows=(
                group(
                    1,
                    ((100, 100), (200, 0)),
                ),
            ),
        )
        self.assertEqual(
            result["target_variant_ids"],
            (100,),
        )


if __name__ == "__main__":
    unittest.main()
