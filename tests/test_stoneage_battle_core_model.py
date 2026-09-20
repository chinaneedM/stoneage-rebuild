import math
import unittest

from tools.stoneage_battle_core_model import (
    ENEMY, PET, PLAYER,
    attribute_adjusted_damage,
    attribute_core_damage,
    critical_bonus,
    critical_damage,
    critical_per_10000,
    elemental_vector,
    field_attribute_power,
    dodge_per_10000,
    early_action_value,
    early_item_action_value,
    effective_defense_newpower,
    effective_defense_preserved_old,
    guard_damage,
    guard_multiplier,
    initiative_total,
    physical_base_damage,
    raw_counter_basis,
    BattleKillProfit,
    BattleKillProfitScan,
    KillProfitRecipient,
    KillProfitScanEnemy,
    battle_exp_from_enemy,
    battle_kill_profit,
    battle_kill_profit_scan,
    ride_pet_exp_from_enemy,
)


class BattleCoreModelTests(unittest.TestCase):
    def test_older_action_value_profile(self):
        self.assertEqual(early_action_value(80,0),100)
        self.assertEqual(early_action_value(80,30),70)
        with self.assertRaises(ValueError):
            early_action_value(80,31)
        self.assertEqual(early_item_action_value(80,30),85)
        self.assertEqual(initiative_total(80,20,False),80)
        self.assertEqual(initiative_total(80,20,True),100)

    def test_defense_profiles_are_kept_separate(self):
        self.assertAlmostEqual(effective_defense_newpower(100),70.0)
        self.assertAlmostEqual(effective_defense_newpower(100,True),140.0)
        self.assertAlmostEqual(
            effective_defense_preserved_old(100,50,40),
            59.0,
        )

    def test_piecewise_damage(self):
        self.assertEqual(physical_base_damage(60,70,1),1)
        self.assertEqual(physical_base_damage(70,70,4),4)
        self.assertEqual(physical_base_damage(100,70,0),53)
        self.assertEqual(physical_base_damage(100,70,12),65)

    def test_elemental_vector_and_attribute_core(self):
        self.assertEqual(elemental_vector(0,0,0,0),(0,0,0,0,100))
        self.assertEqual(elemental_vector(25,25,25,25),(25,25,25,25,0))
        # Neutral-on-neutral preserves ordinary damage.
        self.assertEqual(
            attribute_core_damage(100,(0,0,0,0),(0,0,0,0)),
            100,
        )
        # Fire overcomes wind and is weak against water in the stable table.
        self.assertEqual(
            attribute_core_damage(100,(0,0,100,0),(0,0,0,100)),
            150,
        )
        self.assertEqual(
            attribute_core_damage(100,(0,0,100,0),(0,100,0,0)),
            60,
        )

    def test_field_attribute_ratio_and_critical_addition(self):
        self.assertEqual(field_attribute_power((0,0,0,0),"none",0),0.5)
        self.assertAlmostEqual(
            field_attribute_power((100,0,0,0),"earth",100),
            1.0,
        )
        self.assertEqual(
            attribute_adjusted_damage(
                100,
                (100,0,0,0),
                (0,0,0,0),
                field_attr="earth",
                field_power=100,
            ),
            300,
        )
        self.assertEqual(critical_damage(60,100,50,25),160)

    def test_guard_distribution_edges(self):
        cases={
            1:0.0,25:0.0,26:0.1,50:0.1,51:0.2,70:0.2,
            71:0.3,85:0.3,86:0.4,95:0.4,96:0.5,100:0.5,
        }
        for roll,mult in cases.items():
            self.assertEqual(guard_multiplier(roll),mult)
        self.assertEqual(guard_damage(101,26),10)

    def test_dodge_relationship_modifier(self):
        # player -> non-player reduces defender DEX to 60%.
        per=dodge_per_10000(
            100,100,0,
            attacker_type=PLAYER,defender_type=ENEMY,
        )
        expected=int(math.sqrt((100-60)/0.02)*(60/100)*100)
        self.assertEqual(per,expected)
        self.assertLessEqual(per,7500)

    def test_critical_relationship_and_bonus(self):
        per=critical_per_10000(
            100,100,attacker_luck=0,weapon_critical=0,
            attacker_type=PLAYER,defender_type=ENEMY,
        )
        expected=int(math.sqrt((100-60)/0.09)*100)
        self.assertEqual(per,expected)
        self.assertEqual(critical_bonus(100,50,25),100)

    def test_battle_exp_level_gap_decay(self):
        base=1500
        self.assertEqual(battle_exp_from_enemy(base,5,10),1500)
        self.assertEqual(battle_exp_from_enemy(base,15,10),1500)
        self.assertEqual(battle_exp_from_enemy(base,16,10),1400)
        self.assertEqual(battle_exp_from_enemy(base,29,10),100)
        self.assertEqual(battle_exp_from_enemy(base,30,10),1)
        self.assertEqual(battle_exp_from_enemy(base,60,10),1)

    def test_ride_pet_exp_applies_sixty_percent_after_decay(self):
        base=1500
        self.assertEqual(ride_pet_exp_from_enemy(base,10,10),900)
        self.assertEqual(ride_pet_exp_from_enemy(base,29,10),60)
        self.assertEqual(ride_pet_exp_from_enemy(base,30,10),0)

    def test_kill_profit_attack_list_does_not_split_exp(self):
        profit=battle_kill_profit(
            1500,
            10,
            (
                KillProfitRecipient('player',16,PLAYER),
                KillProfitRecipient('pet:0',29,PET),
            ),
        )
        self.assertIsInstance(profit,BattleKillProfit)
        self.assertEqual(
            dict(profit.direct_exp_by_participant_id),
            {'player':1400,'pet:0':100},
        )
        self.assertEqual(
            dict(profit.kill_count_delta_by_participant_id),
            {'player':1,'pet:0':1},
        )
        self.assertEqual(
            dict(profit.pet_variable_ai_delta_by_participant_id),
            {'pet:0':1},
        )

    def test_kill_profit_ride_pet_uses_its_own_level_and_can_receive_zero(self):
        profit=battle_kill_profit(
            1500,
            10,
            (
                KillProfitRecipient(
                    'player',10,PLAYER,
                    ride_pet_id='ride:2',
                    ride_pet_level=30,
                ),
            ),
        )
        self.assertEqual(
            dict(profit.direct_exp_by_participant_id),
            {'player':1500},
        )
        self.assertEqual(
            dict(profit.ride_exp_by_participant_id),
            {'ride:2':0},
        )
        self.assertEqual(
            dict(profit.kill_count_delta_by_participant_id),
            {'player':1,'ride:2':1},
        )

    def test_pet_kill_loyalty_delta_distinguishes_higher_enemy_and_norisk(self):
        higher=battle_kill_profit(
            100,
            10,
            (KillProfitRecipient('pet:0',5,PET),),
        )
        self.assertEqual(
            dict(higher.pet_variable_ai_delta_by_participant_id),
            {'pet:0':20},
        )
        norisk=battle_kill_profit(
            100,
            10,
            (KillProfitRecipient('pet:0',5,PET),),
            norisk=True,
        )
        self.assertEqual(
            dict(norisk.pet_variable_ai_delta_by_participant_id),
            {},
        )

    def test_profit_scan_counter_shape_credits_actual_counter_actor(self):
        scan=battle_kill_profit_scan(
            (
                KillProfitScanEnemy('enemy:0',10,1500,0,False),
            ),
            (
                KillProfitRecipient('counter:pet',16,PET),
            ),
        )
        self.assertIsInstance(scan,BattleKillProfitScan)
        self.assertEqual(scan.claimed_enemy_ids,('enemy:0',))
        self.assertEqual(
            dict(scan.direct_exp_by_participant_id),
            {'counter:pet':1400},
        )
        self.assertEqual(
            dict(scan.pet_variable_ai_delta_by_participant_id),
            {'counter:pet':1},
        )

    def test_profit_scan_combo_shape_credits_every_attack_list_member(self):
        scan=battle_kill_profit_scan(
            (
                KillProfitScanEnemy('enemy:0',10,1500,0,False),
            ),
            (
                KillProfitRecipient('player:a',10,PLAYER),
                KillProfitRecipient('player:b',16,PLAYER),
            ),
        )
        self.assertEqual(
            dict(scan.direct_exp_by_participant_id),
            {'player:a':1500,'player:b':1400},
        )
        self.assertEqual(
            dict(scan.kill_count_delta_by_participant_id),
            {'player:a':1,'player:b':1},
        )

    def test_profit_scan_deferred_status_death_belongs_to_next_profit_trigger(self):
        scan=battle_kill_profit_scan(
            (
                # The status tick has already reduced this enemy to zero, but
                # no profit routine ran yet, so ISDIE is still false.
                KillProfitScanEnemy('status-dead',10,100,0,False),
                # An already processed corpse is not awarded again.
                KillProfitScanEnemy('already-claimed',10,200,0,True),
                KillProfitScanEnemy('still-alive',10,300,1,False),
            ),
            (
                # This can be an unrelated later ordinary/counter/magic profit
                # trigger; the source scan has no stored status owner here.
                KillProfitRecipient('next-trigger',10,PLAYER),
            ),
        )
        self.assertEqual(scan.claimed_enemy_ids,('status-dead',))
        self.assertEqual(
            dict(scan.direct_exp_by_participant_id),
            {'next-trigger':100},
        )

    def test_profit_scan_claims_all_unprocessed_dead_entries_in_one_call(self):
        scan=battle_kill_profit_scan(
            (
                KillProfitScanEnemy('dead:a',10,100,0,False),
                KillProfitScanEnemy('dead:b',10,250,-5,False),
            ),
            (KillProfitRecipient('player',10,PLAYER),),
        )
        self.assertEqual(scan.claimed_enemy_ids,('dead:a','dead:b'))
        self.assertEqual(
            dict(scan.direct_exp_by_participant_id),
            {'player':350},
        )
        self.assertEqual(
            dict(scan.kill_count_delta_by_participant_id),
            {'player':2},
        )

    def test_counter_is_only_raw_basis(self):
        value=raw_counter_basis(
            100,100,attacker_type=PLAYER,defender_type=ENEMY)
        self.assertGreater(value,0)
        # The final counter probability also needs weapon matchup and luck.
        self.assertIsInstance(value,int)


if __name__=="__main__":
    unittest.main()
