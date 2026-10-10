import hashlib
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_enemy_original_drop_audit as audit

class OriginalEnemyDropTests(unittest.TestCase):
    def test_original_enemy_function_pin_has_no_stub(self):
        p=audit.PINS.read_text()
        self.assertIn("source_functions_sha256",p)
        for profile in ("gavin","bismarck"):
            raw={"ENEMY_createEnemy":"native code"}
            pins={"ENEMY_createEnemy":hashlib.sha256(b"native code").hexdigest()}
            audit.factory.allocator.item.pet.player.validate_bodies(raw,pins)
            with self.assertRaisesRegex(ValueError,"dependency drift"):
                audit.factory.allocator.item.pet.player.validate_bodies({"ENEMY_createEnemy":"stub"},pins)

    def test_source_uses_complete_original_enemy_body(self):
        with patch.object(audit.attack,"pp_file",return_value="preprocessed"),patch.object(audit.attack,"definition",side_effect=lambda _,n:n):
            for profile in ("gavin","bismarck"):
                self.assertEqual(audit.source_bodies(profile,Path("/tmp")),{"ENEMY_createEnemy":"ENEMY_createEnemy"})

    def test_actual_positive_branch_and_full_oracle(self):
        for profile in ("gavin","bismarck"):
            c=audit.extra_controls(profile)
            for marker in ("ENEMY_createEnemy(0,2)","==before_item_count+1",
                           "rng_count==zero_draws+1+","ENEMY_ITEMPROB1",
                           "indexOfExistItems[CHAR_STARTITEMARRAY]==3",
                           "whole 256 original item array",
                           "whole previous battle arena", "source_table_immutable=1",
                           "memcpy(reward_items,before_spawn", "master[ENEMY_STYLE]=master_style"):
                if marker=="whole previous battle arena":
                    marker="previous battle arena"
                self.assertIn(marker,c)
            for unresolved in ("ITEM_TYPE","ITEM_FIELD","LEAK_EXPECTED","DATA_FIELDS","FACTORY_TABLE_ORACLE"):
                self.assertNotIn(unresolved,c)
            self.assertLess(c.index("whole 256 original item array"),c.index("memcpy(reward_items,before_spawn"))
            self.assertIn("source table immutable",c)
        self.assertIn("ITEM_gTable",audit.extra_controls("bismarck"))
        self.assertNotIn("ITEM_gTable",audit.extra_controls("gavin"))

    def test_factory_and_prior_controls_retained(self):
        for profile in ("gavin","bismarck"):
            self.assertIn("ITEM_makeItemAndRegist(1)",audit.factory.factory_controls(profile))
            self.assertIn("REAL_HEADER_ITEM_ALLOCATOR",audit.factory.allocator.controls(profile))
            self.assertIn("REAL_HEADER_ENEMY_POSITIVE_DROP",audit.extra_controls(profile))

if __name__=="__main__":unittest.main()
