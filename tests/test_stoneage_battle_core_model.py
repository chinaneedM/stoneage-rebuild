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
    BattleDropItem,
    DropRecipientTicket,
    DropAllocationRoll,
    BattleDropAllocation,
    BattleDropSettlement,
    enemy_item_probability_hit,
    allocate_battle_drop_items,
    settle_player_battle_drops,
    BattleCaptureInputs,
    BattleCaptureResolution,
    first_empty_pet_slot,
    battle_capture_probability,
    resolve_battle_capture_attempt,
    BattleEscapeInputs,
    BattleEscapeResolution,
    resolve_battle_escape_attempt,
    BattleNormalDeathInputs,
    BattleNormalDeathResolution,
    resolve_battle_normal_death_penalty,
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


    def test_enemy_drop_probability_preserves_fixed_and_legacy_scales(self):
        self.assertFalse(enemy_item_probability_hit(0,None))
        self.assertTrue(enemy_item_probability_hit(1,0))
        self.assertFalse(enemy_item_probability_hit(1,1))
        self.assertTrue(enemy_item_probability_hit(1000,999))
        self.assertTrue(enemy_item_probability_hit(100,99,fixed_itemprob=False))
        with self.assertRaises(ValueError):
            enemy_item_probability_hit(0,0)
        with self.assertRaises(ValueError):
            enemy_item_probability_hit(1001,0)

    def test_drop_allocation_routes_pet_ticket_to_owner_without_deduping_tickets(self):
        items=(BattleDropItem('item:a',101),BattleDropItem('item:b',102))
        result=allocate_battle_drop_items(
            items,
            (
                DropRecipientTicket('player:hero','player:hero'),
                DropRecipientTicket('pet:ally','player:hero'),
            ),
            (DropAllocationRoll(0),DropAllocationRoll(1)),
        )
        self.assertIsInstance(result,BattleDropAllocation)
        self.assertEqual(result.pending_by_player_entry_id['player:hero'],items)
        self.assertEqual(result.destroyed_items,())

    def test_drop_buffer_full_branch_discards_or_replaces_with_explicit_rng(self):
        old=(
            BattleDropItem('old:0',10),
            BattleDropItem('old:1',11),
            BattleDropItem('old:2',12),
        )
        discarded=allocate_battle_drop_items(
            (BattleDropItem('new:discard',20),),
            (DropRecipientTicket('player','player'),),
            (DropAllocationRoll(0,False,None),),
            pending_by_player_entry_id={'player':old},
        )
        self.assertEqual(discarded.pending_by_player_entry_id['player'],old)
        self.assertEqual(discarded.destroyed_items,(BattleDropItem('new:discard',20),))
        replaced=allocate_battle_drop_items(
            (BattleDropItem('new:keep',21),),
            (DropRecipientTicket('player','player'),),
            (DropAllocationRoll(0,True,1),),
            pending_by_player_entry_id={'player':old},
        )
        self.assertEqual(
            replaced.pending_by_player_entry_id['player'],
            (old[0],BattleDropItem('new:keep',21),old[2]),
        )
        self.assertEqual(replaced.destroyed_items,(old[1],))

    def test_drop_buffer_rng_is_not_consumed_before_buffer_is_full(self):
        with self.assertRaises(ValueError):
            allocate_battle_drop_items(
                (BattleDropItem('item',10),),
                (DropRecipientTicket('player','player'),),
                (DropAllocationRoll(0,False,None),),
            )

    def test_drop_settlement_uses_first_empty_bag_slots_and_destroys_overflow(self):
        items=(
            BattleDropItem('item:0',10),
            BattleDropItem('item:1',11),
            BattleDropItem('item:2',12),
        )
        result=settle_player_battle_drops(items,tuple(range(18)))
        self.assertIsInstance(result,BattleDropSettlement)
        self.assertEqual(dict(result.inventory_additions_by_slot),{18:items[0],19:items[1]})
        self.assertEqual(result.destroyed_items,(items[2],))
        dead=settle_player_battle_drops(items,(),player_alive=False)
        self.assertEqual(dict(dead.inventory_additions_by_slot),{})
        self.assertEqual(dead.destroyed_items,items)


    def test_capture_probability_matches_stable_formula_and_sleep_bonus(self):
        base=BattleCaptureInputs(
            attacker_level=10,attacker_charm=50,attacker_fixed_dex=30,
            attacker_fixed_luck=3,target_level=10,target_hp=10,
            target_max_hp=100,target_fixed_dex=15,target_capture_default=11,
        )
        self.assertAlmostEqual(battle_capture_probability(base),24.0)
        asleep=BattleCaptureInputs(**{**base.__dict__,"target_sleep":1})
        self.assertAlmostEqual(battle_capture_probability(asleep),39.0)

    def test_capture_probability_caps_only_upper_end_at_99(self):
        high=BattleCaptureInputs(99,100,999,5,1,1,100,0,100,
            temporary_capture_modifier=999)
        self.assertEqual(battle_capture_probability(high),99.0)
        low=BattleCaptureInputs(1,1,0,0,99,100,1,999,-100)
        self.assertLess(battle_capture_probability(low),0.0)

    def test_capture_roll_uses_strict_less_than(self):
        inputs=BattleCaptureInputs(10,50,30,3,10,10,100,15,11)
        success=resolve_battle_capture_attempt(inputs,roll_1_100=23)
        self.assertIsInstance(success,BattleCaptureResolution)
        self.assertTrue(success.success)
        self.assertEqual(success.assigned_pet_slot,0)
        failed=resolve_battle_capture_attempt(inputs,roll_1_100=24)
        self.assertFalse(failed.success)
        self.assertEqual(failed.failure_reason,'capture_roll_failed')

    def test_capture_gates_do_not_consume_rng_and_pick_all_pet_only_bypasses_level(self):
        too_high=BattleCaptureInputs(1,100,30,5,7,1,100,10,30)
        result=resolve_battle_capture_attempt(too_high,roll_1_100=None)
        self.assertEqual(result.failure_reason,'target_level_too_high')
        self.assertFalse(result.rng_consumed)
        bypass=BattleCaptureInputs(**{**too_high.__dict__,"pick_all_pet":True})
        result=resolve_battle_capture_attempt(bypass,roll_1_100=1)
        self.assertTrue(result.rng_consumed)
        nonpet=BattleCaptureInputs(**{**bypass.__dict__,"target_capturable":False})
        result=resolve_battle_capture_attempt(nonpet,roll_1_100=None)
        self.assertEqual(result.failure_reason,'target_not_capturable')
        self.assertFalse(result.rng_consumed)

    def test_capture_pet_capacity_is_checked_after_successful_rng(self):
        inputs=BattleCaptureInputs(
            50,100,100,5,1,1,100,1,50,
            occupied_pet_slots=(0,1,2,3,4),
        )
        result=resolve_battle_capture_attempt(inputs,roll_1_100=1)
        self.assertFalse(result.success)
        self.assertTrue(result.rng_consumed)
        self.assertEqual(result.failure_reason,'pet_slots_full')
        self.assertEqual(result.capture_modifier_after,0)

    def test_capture_first_empty_pet_slot_is_ascending_zero_to_four(self):
        self.assertEqual(first_empty_pet_slot((0,2,4)),1)
        self.assertEqual(first_empty_pet_slot((0,1,2,3,4)),-1)

    def test_capture_missing_required_item_consumes_no_rng(self):
        inputs=BattleCaptureInputs(
            50,100,100,5,1,1,100,1,50,
            required_items_present=False,temporary_capture_modifier=25,
        )
        result=resolve_battle_capture_attempt(inputs,roll_1_100=None)
        self.assertEqual(result.failure_reason,'missing_required_items')
        self.assertFalse(result.rng_consumed)
        self.assertEqual(result.capture_modifier_after,0)


    def test_escape_first_attempt_preserves_source_double_increment(self):
        result=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,
                actor_kind='player',
                actor_fixed_luck=3,
                stored_escape_count_before=0,
                opponent_levels=(10,),
            ),
            roll_1_100=99,
        )
        self.assertIsInstance(result,BattleEscapeResolution)
        self.assertEqual(result.stored_escape_count_after,1)
        self.assertEqual(result.effective_escape_count,2)
        self.assertEqual(result.probability,100)
        self.assertTrue(result.check_success)

    def test_escape_strict_less_than_and_failure_keeps_incremented_counter(self):
        result=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,
                actor_kind='player',
                actor_fixed_luck=2,
                opponent_levels=(30,),
            ),
            roll_1_100=40,
        )
        # 40*2 - 2*(30-10) = 40; strict '<' therefore fails on roll 40.
        self.assertEqual(result.probability,40)
        self.assertFalse(result.check_success)
        self.assertFalse(result.exits_battle)
        self.assertEqual(result.stored_escape_count_after,1)

    def test_escape_player_luck_is_clamped_and_chance_has_no_upper_cap(self):
        result=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=1,
                actor_kind='player',
                actor_fixed_luck=999,
                opponent_levels=(99,),
            ),
            roll_1_100=100,
        )
        self.assertEqual(result.effective_luck,5)
        self.assertEqual(result.probability,190)
        self.assertTrue(result.check_success)

    def test_escape_enemy_rare_maps_to_source_luck_bands(self):
        rare0=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,actor_kind='enemy',actor_rare=0,
                opponent_levels=(10,),
            ),
            roll_1_100=1,
        )
        rare1=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,actor_kind='enemy',actor_rare=1,
                opponent_levels=(10,),
            ),
            roll_1_100=1,
        )
        rare2=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,actor_kind='enemy',actor_rare=2,
                opponent_levels=(10,),
            ),
            roll_1_100=1,
        )
        self.assertEqual(
            (rare0.effective_luck,rare1.effective_luck,rare2.effective_luck),
            (1,3,5),
        )
        self.assertEqual(
            (rare0.probability,rare1.probability,rare2.probability),
            (60,100,190),
        )

    def test_escape_abio_subtracts_100_before_integer_average(self):
        result=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,
                actor_kind='player',
                actor_fixed_luck=1,
                opponent_levels=(50,51),
                opponent_abio_flags=(True,False),
            ),
            roll_1_100=1,
        )
        # (-100+50+51)/2 truncates toward zero to 0.
        self.assertEqual(result.average_opponent_level,0)
        self.assertEqual(result.probability,80)

    def test_escape_no_opponents_still_consumes_rng_at_probability_100(self):
        failed=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,actor_kind='player',opponent_levels=(),
            ),
            roll_1_100=100,
        )
        self.assertEqual(failed.probability,100)
        self.assertTrue(failed.rng_consumed)
        self.assertFalse(failed.check_success)

    def test_pvp_escape_check_returns_true_without_rng(self):
        result=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=10,actor_kind='player',pvp=True,
            ),
            roll_1_100=None,
        )
        self.assertTrue(result.check_success)
        self.assertTrue(result.exits_battle)
        self.assertFalse(result.rng_consumed)
        self.assertIsNone(result.probability)

    def test_forced_escape_still_consumes_check_rng_but_exits_on_failure(self):
        result=resolve_battle_escape_attempt(
            BattleEscapeInputs(
                actor_level=1,actor_kind='player',actor_fixed_luck=1,
                opponent_levels=(99,),forced_exit=True,
            ),
            roll_1_100=100,
        )
        self.assertFalse(result.check_success)
        self.assertTrue(result.exits_battle)
        self.assertTrue(result.rng_consumed)


    def test_normal_player_death_penalty_is_per_death_and_low_level_halves(self):
        high=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PLAYER,
                victim_level=11,
                default_pet_present=True,
            )
        )
        self.assertIsInstance(high,BattleNormalDeathResolution)
        self.assertEqual(high.player_charm_delta,-2)
        self.assertEqual(high.default_pet_variable_ai_delta,-100)
        self.assertTrue(high.clears_victim_command)

        low=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PLAYER,
                victim_level=10,
                default_pet_present=True,
            )
        )
        self.assertEqual(low.player_charm_delta,-1)
        self.assertEqual(low.default_pet_variable_ai_delta,-50)

    def test_normal_player_death_without_active_pet_does_not_invent_pet_penalty(self):
        result=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PLAYER,
                victim_level=50,
                default_pet_present=False,
            )
        )
        self.assertEqual(result.player_charm_delta,-2)
        self.assertEqual(result.default_pet_variable_ai_delta,0)

    def test_normal_pet_death_uses_owner_level_and_increments_dead_pet_count(self):
        high=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PET,
                victim_level=20,
                owner_level=11,
            )
        )
        self.assertEqual(high.victim_pet_variable_ai_delta,-500)
        self.assertEqual(high.owner_dead_pet_count_delta,1)
        self.assertTrue(high.clears_victim_command)

        low=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PET,
                victim_level=99,
                owner_level=10,
            )
        )
        self.assertEqual(low.victim_pet_variable_ai_delta,-250)
        self.assertEqual(low.owner_dead_pet_count_delta,1)

    def test_normal_death_penalty_is_disabled_for_pvp_or_norisk(self):
        pvp=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PLAYER,
                victim_level=50,
                pve_battle=False,
                default_pet_present=True,
            )
        )
        no_risk=resolve_battle_normal_death_penalty(
            BattleNormalDeathInputs(
                victim_kind=PET,
                victim_level=50,
                owner_level=50,
                no_risk=True,
            )
        )
        self.assertEqual(pvp,BattleNormalDeathResolution())
        self.assertEqual(no_risk,BattleNormalDeathResolution())



if __name__=="__main__":
    unittest.main()
