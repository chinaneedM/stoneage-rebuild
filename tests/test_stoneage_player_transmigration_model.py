import unittest

from tools.stoneage_player_transmigration_model import (
    apply_core_transmigration,
    core_eligibility,
    inherited_total_points,
    source_rounding,
)


class PlayerTransmigrationModelTests(unittest.TestCase):
    def test_first_four_require_matching_pet_and_core_events(self):
        ok,reason=core_eligibility(80,0,(39,40,42,46),(693,),0)
        self.assertEqual((ok,reason),(True,"ok"))
        self.assertEqual(core_eligibility(79,0,(39,40,42,46),(693,),0)[1],"level")
        self.assertEqual(core_eligibility(80,0,(39,40,42),(693,),0)[1],"event_flags")
        self.assertEqual(core_eligibility(80,0,(39,40,42,46),(694,),0)[1],"required_pet")
        self.assertEqual(core_eligibility(80,0,(39,40,42,46),(693,),1)[1],"unspent_points")

    def test_fifth_requires_all_four_core_pets(self):
        flags=(39,40,42,46)
        self.assertEqual(core_eligibility(80,4,flags,(693,694,695,696),0),(True,"ok"))
        self.assertEqual(core_eligibility(80,4,flags,(693,694,695),0)[1],"required_pets")
        self.assertEqual(core_eligibility(80,5,flags,(693,694,695,696),0)[1],"max_transmigrations")

    def test_source_rounding_is_literal_not_python_round(self):
        self.assertEqual(source_rounding(2.3,1),2.8)
        self.assertEqual(source_rounding(2.3,2),2.35)

    def test_inherited_total_formula(self):
        self.assertEqual(inherited_total_points((1000,500,300,200),1,4,80),1)
        self.assertEqual(inherited_total_points((10000,5000,3000,2000),1,20,130),32)

    def test_reset_and_proportional_inheritance(self):
        out=apply_core_transmigration((1000,500,300,200),80,4,0)
        self.assertEqual(out["transmigrations"],1)
        self.assertEqual(out["level"],1)
        self.assertEqual(out["exp"],0)
        self.assertEqual(out["free_stat_points"],10)
        self.assertEqual(out["accumulated_quests"],4)
        self.assertEqual(out["accumulated_levels"],80)
        self.assertEqual(out["trans_equation"],(4<<16)+80)
        self.assertEqual(out["inherited_total_formula_result"],1)
        self.assertEqual(
            (out["vital"],out["strength"],out["toughness"],out["dexterity"]),
            (100,75,65,60),
        )

    def test_level_accumulation_is_capped_at_130_per_transmigration(self):
        out=apply_core_transmigration((10000,5000,3000,2000),140,20,0)
        self.assertEqual(out["accumulated_levels"],130)
        self.assertEqual(out["inherited_total_formula_result"],32)


if __name__=="__main__":
    unittest.main()
