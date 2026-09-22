import unittest
from dataclasses import replace

from tools.stoneage_battle_guardian_model import GuardianRegistration

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_CAPTURE,
    BATTLE_COM_COMBO,
    BATTLE_COM_ESCAPE,
    BATTLE_COM_GUARD,
    BATTLE_COM_S_GUARDIAN_ATTACK,
    BATTLE_COM_S_GUARDIAN_GUARD,
    BATTLE_COM_S_STATUSCHANGE,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    ComboExecutionRolls,
    CounterAttemptRolls,
    OrdinaryAttackRolls,
    OrdinaryCaptureContext,
    OrdinaryCaptureRolls,
    OrdinaryEscapeContext,
    OrdinaryEscapeRolls,
    apply_base_combo_rewrite,
    battle_command3_high,
    battle_command3_low,
    pack_battle_command3,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
    BaseStatusCombatProfile,
    BaseStatusTurnRolls,
    STATUS_POISON,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid, side, kind, *, hp=100, attack=100, defense=70, quick=50, level=10):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=hp,
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
    )


def profile(
    dex=100,
    luck=0,
    earth=0,
    water=0,
    fire=0,
    wind=0,
    counter_weapon_type="fist",
):
    return BattleCombatProfile(
        fixed_dex=dex,
        fixed_luck=luck,
        earth=earth,
        water=water,
        fire=fire,
        wind=wind,
        counter_weapon_type=counter_weapon_type,
    )


class BattleRoundModelTests(unittest.TestCase):
    def test_prepare_round_sorts_descending_and_requires_explicit_tie(self):
        a = actor("a", "player", "player", quick=80)
        b = actor("b", "enemy", "enemy", quick=60)
        commands = {
            "a": BattleCommand(BATTLE_COM_WAIT),
            "b": BattleCommand(BATTLE_COM_WAIT),
        }
        prepared = prepare_battle_round(
            (a, b),
            commands,
            {"a": 0, "b": 0},
        )
        self.assertEqual(
            tuple(x.participant.participant_id for x in prepared.ordered_entries),
            ("a", "b"),
        )

        with self.assertRaisesRegex(ValueError, "tie_break_order"):
            prepare_battle_round(
                (a, b),
                commands,
                {"a": 20, "b": 0},
            )

    def test_base_combo_rewrite_groups_sorted_contiguous_same_target_attacks(self):
        p1=actor("p1","player","player",quick=100)
        p2=actor("p2","player","pet",quick=90)
        p3=actor("p3","player","pet",quick=80)
        enemy=actor("enemy","enemy","enemy",quick=10)
        prepared=prepare_battle_round(
            (p1,p2,p3,enemy),
            {
                "p1":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "p2":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "p3":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"p1":0,"p2":0,"p3":0,"enemy":0},
        )
        rewritten=apply_base_combo_rewrite(
            prepared,
            {
                "p1":profile(),
                "p2":profile(),
                "p3":profile(),
                "enemy":profile(),
            },
            # Only the starter consumes a roll; joiners need no roll.
            {"p1":50},
        )
        first_three=rewritten.ordered_entries[:3]
        self.assertEqual(
            tuple(entry.command.command1 for entry in first_three),
            (BATTLE_COM_COMBO,BATTLE_COM_COMBO,BATTLE_COM_COMBO),
        )
        self.assertEqual(
            len({entry.combo_id for entry in first_three}),
            1,
        )
        self.assertGreater(first_three[0].combo_id,0)

    def test_base_combo_enemy_start_boundary_is_inclusive_twenty_percent(self):
        e1=actor("e1","enemy","enemy",quick=100)
        e2=actor("e2","enemy","enemy",quick=90)
        player=actor("player","player","player",quick=10)
        commands={
            "e1":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            "e2":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            "player":BattleCommand(BATTLE_COM_WAIT),
        }
        prepared=prepare_battle_round(
            (e1,e2,player),commands,{"e1":0,"e2":0,"player":0}
        )
        profiles={"e1":profile(),"e2":profile(),"player":profile()}
        hit=apply_base_combo_rewrite(prepared,profiles,{"e1":20})
        self.assertEqual(hit.ordered_entries[0].command.command1,BATTLE_COM_COMBO)
        self.assertEqual(hit.ordered_entries[1].command.command1,BATTLE_COM_COMBO)

        miss=apply_base_combo_rewrite(
            prepared,profiles,{"e1":21,"e2":100}
        )
        self.assertEqual(miss.ordered_entries[0].command.command1,BATTLE_COM_ATTACK)
        self.assertEqual(miss.ordered_entries[1].command.command1,BATTLE_COM_ATTACK)

    def test_base_combo_throwing_weapon_breaks_chain(self):
        p1=actor("p1","player","player",quick=100)
        p2=actor("p2","player","pet",quick=90)
        p3=actor("p3","player","pet",quick=80)
        enemy=actor("enemy","enemy","enemy",quick=10)
        prepared=prepare_battle_round(
            (p1,p2,p3,enemy),
            {
                "p1":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "p2":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "p3":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"p1":0,"p2":0,"p3":0,"enemy":0},
        )
        rewritten=apply_base_combo_rewrite(
            prepared,
            {
                "p1":profile(),
                "p2":profile(counter_weapon_type="bow"),
                "p3":profile(),
                "enemy":profile(),
            },
            {"p1":1,"p3":100},
        )
        self.assertEqual(
            tuple(entry.command.command1 for entry in rewritten.ordered_entries[:3]),
            (BATTLE_COM_ATTACK,BATTLE_COM_ATTACK,BATTLE_COM_ATTACK),
        )

    def test_combo_execution_skips_dodge_and_applies_total_on_last_member(self):
        p1=actor("p1","player","player",attack=60,quick=100)
        p2=actor("p2","player","pet",attack=60,quick=90)
        enemy=actor("enemy","enemy","enemy",hp=300,defense=70,quick=10)
        prepared=prepare_battle_round(
            (p1,p2,enemy),
            {
                "p1":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "p2":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"p1":0,"p2":0,"enemy":0},
        )
        prepared=apply_base_combo_rewrite(
            prepared,
            {"p1":profile(),"p2":profile(),"enemy":profile()},
            {"p1":1},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"p1":0,"p2":1,"enemy":10},
            profiles={"p1":profile(),"p2":profile(),"enemy":profile()},
            attack_rolls={},
            combo_rolls_by_starter_id={
                "p1":ComboExecutionRolls(
                    (
                        OrdinaryAttackRolls(
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                        OrdinaryAttackRolls(
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                    )
                )
            },
            defense_profile="newpower_70pct",
        )
        combo_events=[event for event in result.events if event.is_combo]
        self.assertEqual(len(combo_events),2)
        self.assertEqual(
            tuple(event.participant_id for event in combo_events),
            ("p1","p2"),
        )
        self.assertEqual(combo_events[0].target_hp_before,300)
        self.assertEqual(combo_events[0].target_hp_after,300)
        self.assertEqual(combo_events[1].target_hp_before,300)
        self.assertLess(combo_events[1].target_hp_after,300)
        self.assertEqual(
            300-result.hp_by_participant_id["enemy"],
            sum(event.damage for event in combo_events),
        )
        self.assertEqual(
            combo_events[1].profit_participant_ids,
            ("p1","p2"),
        )
        self.assertEqual(result.events[-1].result,"wait")

    def test_sleep_one_suppresses_turn_even_when_it_expires(self):
        player=actor("player","player","player",quick=100)
        enemy=actor("enemy","enemy","enemy",quick=20)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={},
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(
                    status=BaseBattleStatusState(sleep=1),
                    work_quick=100,
                ),
                "enemy":BaseBattleStatusRuntime(work_quick=20),
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].result,"status_tick")
        self.assertEqual(result.events[1].result,"status_no_action")
        self.assertEqual(result.hp_by_participant_id["enemy"],100)
        self.assertEqual(
            result.base_status_runtime_by_participant_id["player"].status.sleep,
            0,
        )

    def test_positive_damage_wakes_slower_sleeping_actor_before_its_turn(self):
        player=actor("player","player","player",hp=200,attack=100,quick=50)
        enemy=actor("enemy","enemy","enemy",hp=200,attack=60,quick=100)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(
                    status=BaseBattleStatusState(sleep=2),
                    work_quick=50,
                ),
                "enemy":BaseBattleStatusRuntime(work_quick=100),
            },
            defense_profile="newpower_70pct",
        )
        player_attack=[
            event for event in result.events
            if event.participant_id=="player" and event.result=="normal"
        ]
        self.assertEqual(len(player_attack),1)
        runtime=result.base_status_runtime_by_participant_id["player"]
        self.assertEqual(runtime.status.sleep,0)
        self.assertEqual(runtime.damage_count,1)

    def test_confusion_can_rewrite_wait_into_same_round_attack(self):
        player=actor("player","player","player",attack=60,quick=100)
        enemy=actor("enemy","enemy","enemy",hp=200,quick=20)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(
                    status=BaseBattleStatusState(confusion=2),
                    work_quick=100,
                ),
                "enemy":BaseBattleStatusRuntime(work_quick=20),
            },
            base_status_rolls_by_participant_id={
                "player":BaseStatusTurnRolls(
                    confusion_action_roll_1_100=1,
                    confusion_side_roll_0_1=1,
                    confusion_pos_roll_0_9=9,
                )
            },
            defense_profile="newpower_70pct",
        )
        attack=[
            event for event in result.events
            if event.participant_id=="player" and event.result=="normal"
        ]
        self.assertEqual(len(attack),1)
        self.assertEqual(attack[0].resolved_target_slot,10)
        self.assertLess(result.hp_by_participant_id["enemy"],200)

    def test_confusion_provenance_does_not_leak_to_later_actor(self):
        p1=actor("p1","player","player",attack=60,quick=100)
        p2=actor("p2","player","pet",attack=60,quick=90)
        enemy=actor("enemy","enemy","enemy",quick=20)
        prepared=prepare_battle_round(
            (p1,p2,enemy),
            {
                "p1":BattleCommand(BATTLE_COM_WAIT),
                "p2":BattleCommand(BATTLE_COM_ATTACK,command2=0),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"p1":0,"p2":0,"enemy":0},
        )
        with self.assertRaisesRegex(ValueError,"same-side ordinary attacks"):
            resolve_ordinary_round(
                prepared,
                slots={"p1":0,"p2":1,"enemy":10},
                profiles={
                    "p1":profile(),"p2":profile(),"enemy":profile(),
                },
                attack_rolls={
                    "p1":OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                    ),
                    "p2":OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                    ),
                },
                base_status_runtime_by_participant_id={
                    "p1":BaseBattleStatusRuntime(
                        status=BaseBattleStatusState(confusion=2),
                        work_quick=100,
                    ),
                    "p2":BaseBattleStatusRuntime(work_quick=90),
                    "enemy":BaseBattleStatusRuntime(work_quick=20),
                },
                base_status_rolls_by_participant_id={
                    "p1":BaseStatusTurnRolls(
                        confusion_action_roll_1_100=1,
                        confusion_side_roll_0_1=1,
                        confusion_pos_roll_0_9=9,
                    )
                },
                defense_profile="newpower_70pct",
            )

    def test_guard_is_active_before_slow_guard_actor_turn(self):
        player = actor("player", "player", "player", quick=20)
        enemy = actor("enemy", "enemy", "enemy", quick=100)
        prepared = prepare_battle_round(
            (player, enemy),
            {
                "player": BattleCommand(BATTLE_COM_GUARD),
                "enemy": BattleCommand(BATTLE_COM_ATTACK, command2=0),
            },
            {"player": 0, "enemy": 0},
        )
        result = resolve_ordinary_round(
            prepared,
            slots={"player": 0, "enemy": 10},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "enemy": OrdinaryAttackRolls(
                    dodge_roll_1_10000=None,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    guard_roll_1_100=1,
                    minimum_damage_roll_0_1=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.action_order, ("enemy", "player"))
        self.assertEqual(result.events[0].result, "allguard")
        self.assertEqual(result.events[0].damage, 0)
        self.assertEqual(result.hp_by_participant_id["player"], 100)

    def test_command3_halves_match_fixed_battle_macros(self):
        packed=pack_battle_command3(low=3,high=4)
        self.assertEqual(packed,0x00040003)
        self.assertEqual(battle_command3_low(packed),3)
        self.assertEqual(battle_command3_high(packed),4)

    def test_defensive_guardian_setup_effect_registers_selected_target(self):
        player=actor("player","player","player",hp=200,quick=20)
        pet=actor("pet","player","pet",hp=200,quick=10)
        enemy=actor("enemy","enemy","enemy",hp=200,attack=100,quick=100)
        prepared=prepare_battle_round(
            (player,pet,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet":BattleCommand(BATTLE_COM_GUARD,command2=0),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"pet":5,"enemy":10},
            profiles={
                "player":profile(),
                "pet":profile(),
                "enemy":profile(),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    guard_roll_1_100=100,
                )
            },
            command_setup_effects_by_participant_id={
                "pet":BattleCommandSetupEffects(
                    guardian_flag=True,
                    guardian_for_slot=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        attack=result.events[0]
        self.assertTrue(attack.guardian_redirected)
        self.assertEqual(attack.guardian_slot,5)
        self.assertEqual(result.hp_by_participant_id["player"],200)
        self.assertLess(result.hp_by_participant_id["pet"],200)

    def test_command_setup_attack_and_defense_power_feed_physical_resolution(self):
        player=actor(
            "player","player","player",
            hp=300,attack=100,defense=70,quick=100,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            hp=300,attack=100,defense=70,quick=20,
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"enemy":0},
        )
        baseline=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        boosted=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            command_setup_effects_by_participant_id={
                "player":BattleCommandSetupEffects(attack_power=200),
                "enemy":BattleCommandSetupEffects(defense_power=140),
            },
            defense_profile="newpower_70pct",
        )
        self.assertNotEqual(
            baseline.events[0].damage,
            boosted.events[0].damage,
        )

    def test_guardian_attack_command_auto_registers_front_row_owner(self):
        player=actor("player","player","player",hp=200,quick=20)
        pet=actor("pet","player","pet",hp=200,attack=80,quick=10)
        enemy=actor("enemy","enemy","enemy",hp=200,attack=100,quick=100)
        prepared=prepare_battle_round(
            (player,pet,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet":BattleCommand(
                    BATTLE_COM_S_GUARDIAN_ATTACK,
                    command2=10,
                ),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"pet":5,"enemy":10},
            profiles={
                "player":profile(),
                "pet":profile(),
                "enemy":profile(),
            },
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "pet":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            defense_profile="newpower_70pct",
        )
        enemy_attack=[
            event for event in result.events
            if event.participant_id=="enemy"
        ][0]
        self.assertTrue(enemy_attack.guardian_redirected)
        self.assertEqual(enemy_attack.guarded_target_slot,0)
        self.assertEqual(enemy_attack.guardian_slot,5)
        self.assertEqual(result.hp_by_participant_id["player"],200)
        self.assertLess(result.hp_by_participant_id["pet"],200)

    def test_guardian_attack_front_row_pet_does_not_invent_owner_registration(self):
        pet=actor("pet","player","pet",hp=200,attack=80,quick=10)
        enemy=actor("enemy","enemy","enemy",hp=200,attack=100,quick=100)
        prepared=prepare_battle_round(
            (pet,enemy),
            {
                "pet":BattleCommand(
                    BATTLE_COM_S_GUARDIAN_ATTACK,
                    command2=10,
                ),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"pet":0,"enemy":10},
            profiles={"pet":profile(),"enemy":profile()},
            attack_rolls={
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "pet":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            defense_profile="newpower_70pct",
        )
        enemy_attack=[
            event for event in result.events
            if event.participant_id=="enemy"
        ][0]
        self.assertFalse(enemy_attack.guardian_redirected)

    def test_enum_only_guardian_guard_is_not_executable_common_handler(self):
        pet=actor("pet","player","pet")
        prepared=prepare_battle_round(
            (pet,),
            {"pet":BattleCommand(BATTLE_COM_S_GUARDIAN_GUARD)},
            {"pet":0},
        )
        with self.assertRaises(ValueError):
            resolve_ordinary_round(
                prepared,
                slots={"pet":5},
                profiles={"pet":profile()},
                attack_rolls={},
                defense_profile="newpower_70pct",
            )

    def test_guardian_redirects_after_dodge_and_before_damage(self):
        player=actor("player","player","player",attack=100,quick=100)
        target=actor("target","enemy","enemy",hp=200,quick=20)
        guardian=actor("guardian","enemy","enemy",hp=200,quick=10)
        prepared=prepare_battle_round(
            (player,target,guardian),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "target":BattleCommand(BATTLE_COM_WAIT),
                "guardian":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"target":0,"guardian":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"target":10,"guardian":11},
            profiles={
                "player":profile(),
                "target":profile(),
                "guardian":profile(),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        attack=result.events[0]
        self.assertTrue(attack.guardian_redirected)
        self.assertEqual(attack.guarded_target_slot,10)
        self.assertEqual(attack.guardian_slot,11)
        self.assertEqual(attack.resolved_target_slot,11)
        self.assertEqual(result.hp_by_participant_id["target"],200)
        self.assertLess(result.hp_by_participant_id["guardian"],200)

    def test_original_target_dodge_prevents_guardian_redirect(self):
        player=actor("player","player","player",quick=100)
        target=actor("target","enemy","enemy",hp=200,quick=20)
        guardian=actor("guardian","enemy","enemy",hp=200,quick=10)
        prepared=prepare_battle_round(
            (player,target,guardian),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "target":BattleCommand(BATTLE_COM_WAIT),
                "guardian":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"target":0,"guardian":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"target":10,"guardian":11},
            profiles={
                "player":profile(dex=100),
                "target":profile(dex=10000),
                "guardian":profile(),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=1,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        attack=result.events[0]
        self.assertEqual(attack.result,"dodge")
        self.assertFalse(attack.guardian_redirected)
        self.assertEqual(result.hp_by_participant_id["target"],200)
        self.assertEqual(result.hp_by_participant_id["guardian"],200)

    def test_throwing_weapon_and_bad_status_block_guardian(self):
        player=actor("player","player","player",attack=100,quick=100)
        target=actor("target","enemy","enemy",hp=200,quick=20)
        guardian=actor("guardian","enemy","enemy",hp=200,quick=10)
        prepared=prepare_battle_round(
            (player,target,guardian),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "target":BattleCommand(BATTLE_COM_WAIT),
                "guardian":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"target":0,"guardian":0},
        )
        thrown=resolve_ordinary_round(
            prepared,
            slots={"player":0,"target":10,"guardian":11},
            profiles={
                "player":profile(counter_weapon_type="bow"),
                "target":profile(),
                "guardian":profile(),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        self.assertFalse(thrown.events[0].guardian_redirected)
        self.assertLess(thrown.hp_by_participant_id["target"],200)
        self.assertEqual(thrown.hp_by_participant_id["guardian"],200)

        sleeping=resolve_ordinary_round(
            prepared,
            slots={"player":0,"target":10,"guardian":11},
            profiles={
                "player":profile(),
                "target":profile(),
                "guardian":profile(),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(work_quick=100),
                "target":BaseBattleStatusRuntime(work_quick=20),
                "guardian":BaseBattleStatusRuntime(
                    status=BaseBattleStatusState(sleep=2),
                    work_quick=10,
                ),
            },
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        self.assertFalse(sleeping.events[0].guardian_redirected)
        self.assertLess(sleeping.hp_by_participant_id["target"],200)

    def test_guardian_zero_damage_is_forced_to_one_normal(self):
        player=actor(
            "player","player","player",
            attack=1,quick=100,
        )
        target=actor("target","enemy","enemy",hp=200,quick=20)
        guardian=actor(
            "guardian","enemy","enemy",
            hp=200,defense=1000,quick=10,
        )
        prepared=prepare_battle_round(
            (player,target,guardian),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "target":BattleCommand(BATTLE_COM_WAIT),
                "guardian":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"target":0,"guardian":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"target":10,"guardian":11},
            profiles={
                "player":profile(),
                "target":profile(),
                "guardian":profile(),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=0,
                )
            },
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        attack=result.events[0]
        self.assertTrue(attack.guardian_redirected)
        self.assertEqual(attack.result,"normal")
        self.assertEqual(attack.damage,1)
        self.assertEqual(result.hp_by_participant_id["guardian"],199)

    def test_guardian_statuschange_applies_status_to_guardian(self):
        pet=actor("pet","player","pet",attack=100,quick=100,level=20)
        target=actor("target","enemy","enemy",hp=200,quick=20,level=10)
        guardian=actor(
            "guardian","enemy","enemy",
            hp=200,quick=200,level=10,
        )
        prepared=prepare_battle_round(
            (pet,target,guardian),
            {
                "pet":BattleCommand(
                    BATTLE_COM_S_STATUSCHANGE,
                    command2=10,
                    command3=pack_battle_command3(low=1,high=3),
                ),
                "target":BattleCommand(BATTLE_COM_WAIT),
                "guardian":BattleCommand(BATTLE_COM_WAIT),
            },
            {"pet":0,"target":0,"guardian":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"pet":0,"target":10,"guardian":11},
            profiles={
                "pet":profile(luck=10),
                "target":profile(),
                "guardian":profile(),
            },
            attack_rolls={
                "pet":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            base_status_combat_profiles_by_participant_id={
                "guardian":BaseStatusCombatProfile(
                    vital=25,strength=25,tough=25,dex=25,
                    resistance_by_status={STATUS_POISON:5},
                )
            },
            status_application_rolls_by_attack_id={"pet":44},
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        attack=[
            event for event in result.events
            if event.participant_id=="pet"
        ][0]
        self.assertTrue(attack.guardian_redirected)
        self.assertTrue(attack.status_application_resolution.check.success)
        self.assertEqual(
            result.base_status_runtime_by_participant_id[
                "guardian"
            ].status.poison,
            4,
        )
        self.assertEqual(
            result.base_status_runtime_by_participant_id[
                "target"
            ].status.poison,
            0,
        )

    def test_guardian_redirect_forces_attack_continuation_false(self):
        player=actor(
            "player","player","player",
            hp=200,attack=60,quick=100,
        )
        target=actor(
            "target","enemy","enemy",
            hp=200,attack=60,quick=50,
        )
        guardian=actor(
            "guardian","enemy","enemy",
            hp=200,quick=40,
        )
        prepared=prepare_battle_round(
            (player,target,guardian),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "target":BattleCommand(BATTLE_COM_ATTACK,command2=0),
                "guardian":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"target":0,"guardian":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"target":10,"guardian":11},
            profiles={
                "player":profile(dex=100),
                "target":profile(dex=200),
                "guardian":profile(),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "target":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=1,
                    damage_roll=0,
                ),
            },
            counter_rolls_by_attack_id={
                "player":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=1,
                        attack_rolls=OrdinaryAttackRolls(
                            dodge_roll_1_10000=10000,
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                    ),
                ),
            },
            guardian_registrations_by_defender_slot={
                10:GuardianRegistration(guardian_slot=11)
            },
            defense_profile="newpower_70pct",
        )
        self.assertTrue(result.events[0].guardian_redirected)
        self.assertFalse(any(event.is_counter for event in result.events))

    def test_statuschange_command_runs_ordinary_attack_then_applies_status(self):
        pet=actor("pet","player","pet",attack=100,quick=100,level=20)
        enemy=actor("enemy","enemy","enemy",hp=200,quick=20,level=10)
        prepared=prepare_battle_round(
            (pet,enemy),
            {
                "pet":BattleCommand(
                    BATTLE_COM_S_STATUSCHANGE,
                    command2=10,
                    command3=pack_battle_command3(low=1,high=3),
                ),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"pet":0,"enemy":10},
            profiles={"pet":profile(luck=10),"enemy":profile()},
            attack_rolls={
                "pet":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            base_status_runtime_by_participant_id={
                "pet":BaseBattleStatusRuntime(work_quick=100),
                "enemy":BaseBattleStatusRuntime(work_quick=20),
            },
            base_status_combat_profiles_by_participant_id={
                "enemy":BaseStatusCombatProfile(
                    vital=25,strength=25,tough=25,dex=25,
                    resistance_by_status={STATUS_POISON:5},
                )
            },
            status_application_rolls_by_attack_id={"pet":44},
            defense_profile="newpower_70pct",
        )
        event=result.events[0]
        self.assertEqual(event.command1,BATTLE_COM_S_STATUSCHANGE)
        self.assertEqual(event.result,"normal")
        self.assertGreater(event.damage,0)
        self.assertIsNotNone(event.status_application_resolution)
        self.assertTrue(event.status_application_resolution.check.success)
        self.assertEqual(
            event.status_application_resolution.turn_written,
            4,
        )
        # Enemy is slower, so its own StatusSeq runs later in this same round:
        # the newly written poison 4 decrements to 3 before round end.
        self.assertEqual(
            result.base_status_runtime_by_participant_id["enemy"].status.poison,
            3,
        )

    def test_statuschange_dodge_consumes_no_status_rng_or_profile(self):
        pet=actor("pet","player","pet",quick=100)
        enemy=actor("enemy","enemy","enemy",quick=20)
        prepared=prepare_battle_round(
            (pet,enemy),
            {
                "pet":BattleCommand(
                    BATTLE_COM_S_STATUSCHANGE,
                    command2=10,
                    command3=pack_battle_command3(low=1,high=3),
                ),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"pet":0,"enemy":10},
            profiles={
                "pet":profile(dex=100),
                "enemy":profile(dex=10000),
            },
            attack_rolls={
                "pet":OrdinaryAttackRolls(
                    dodge_roll_1_10000=1,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].result,"dodge")
        self.assertIsNone(result.events[0].status_application_resolution)

    def test_normal_attack_applies_recovered_damage_to_hp(self):
        player = actor("player", "player", "player", quick=100)
        enemy = actor("enemy", "enemy", "enemy", quick=50)
        prepared = prepare_battle_round(
            (player, enemy),
            {
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            {"player": 0, "enemy": 0},
        )
        result = resolve_ordinary_round(
            prepared,
            slots={"player": 0, "enemy": 10},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].result, "normal")
        self.assertEqual(result.events[0].damage, 95)
        self.assertEqual(result.hp_by_slot[10], 5)
        self.assertEqual(result.events[1].result, "wait")

    def test_dodge_short_circuits_damage_and_critical(self):
        player = actor("player", "player", "player", quick=100)
        enemy = actor("enemy", "enemy", "enemy", quick=50)
        prepared = prepare_battle_round(
            (player, enemy),
            {
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            {"player": 0, "enemy": 0},
        )
        result = resolve_ordinary_round(
            prepared,
            slots={"player": 0, "enemy": 10},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=1,
                    critical_roll_1_10000=1,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].result, "dodge")
        self.assertEqual(result.events[0].damage, 0)
        self.assertEqual(result.hp_by_slot[10], 100)

    def test_critical_adds_raw_defense_level_ratio_term(self):
        player = actor("player", "player", "player", quick=100)
        enemy = actor("enemy", "enemy", "enemy", quick=50)
        prepared = prepare_battle_round(
            (player, enemy),
            {
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            {"player": 0, "enemy": 0},
        )
        result = resolve_ordinary_round(
            prepared,
            slots={"player": 0, "enemy": 10},
            profiles={"player": profile(), "enemy": profile()},
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=1,
                    damage_roll=0,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].result, "critical")
        self.assertEqual(result.events[0].damage, 130)
        self.assertEqual(result.hp_by_slot[10], 0)

    def test_active_drunk_does_not_pre_tick_counter_before_actor_turn(self):
        player=actor(
            "player","player","player",
            hp=200,attack=60,defense=70,quick=100,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            hp=200,attack=60,defense=70,quick=50,
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={
                "player":profile(dex=100),
                "enemy":profile(dex=200),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            counter_rolls_by_attack_id={
                "player":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=1,
                        attack_rolls=OrdinaryAttackRolls(
                            dodge_roll_1_10000=10000,
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                    ),
                ),
                "enemy":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=10000,
                        attack_rolls=None,
                    ),
                ),
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(work_quick=100),
                "enemy":BaseBattleStatusRuntime(
                    status=BaseBattleStatusState(drunk=2),
                    work_quick=50,
                ),
            },
            defense_profile="newpower_70pct",
        )
        counter=[
            event for event in result.events
            if event.is_counter and event.participant_id=="enemy"
        ][0]
        self.assertEqual(counter.result,"counter_normal")
        # Counter occurs during the faster player's action, before enemy's own
        # later StatusSeq. Drunk is decremented only when enemy's turn arrives.
        self.assertEqual(
            result.base_status_runtime_by_participant_id[
                "enemy"
            ].status.drunk,
            1,
        )

    def test_counter_positive_damage_updates_damage_wakeup_runtime(self):
        player=actor(
            "player","player","player",
            hp=200,attack=60,defense=70,quick=100,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            hp=200,attack=60,defense=70,quick=50,
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={
                "player":profile(dex=100),
                "enemy":profile(dex=200),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=1,
                    damage_roll=0,
                ),
            },
            counter_rolls_by_attack_id={
                "player":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=1,
                        attack_rolls=OrdinaryAttackRolls(
                            dodge_roll_1_10000=10000,
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                    ),
                ),
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(
                    work_quick=100,
                    damage_count=7,
                ),
                "enemy":BaseBattleStatusRuntime(work_quick=50),
            },
            defense_profile="newpower_70pct",
        )
        counter=[
            event for event in result.events
            if event.is_counter and event.participant_id=="enemy"
        ][0]
        self.assertGreater(counter.damage,0)
        # Enemy's later main attack is critical and therefore does not start a
        # second counter chain, but it still also causes positive damage. The
        # runtime count therefore records both the counter hit and later hit.
        self.assertEqual(
            result.base_status_runtime_by_participant_id[
                "player"
            ].damage_count,
            9,
        )

    def test_counter_chain_uses_defender_first_and_scales_positive_damage(self):
        player=actor(
            "player","player","player",
            hp=40,attack=60,defense=70,quick=100,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            hp=100,attack=80,defense=70,quick=50,
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={
                "player":profile(dex=100),
                "enemy":profile(dex=200),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                # Required by the submitted later action even though the
                # counter kills its target before that action executes.
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            counter_rolls_by_attack_id={
                "player":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=1,
                        attack_rolls=OrdinaryAttackRolls(
                            dodge_roll_1_10000=10000,
                            critical_roll_1_10000=10000,
                            damage_roll=0,
                        ),
                    ),
                ),
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].participant_id,"player")
        self.assertEqual(result.events[0].result,"normal")
        self.assertEqual(result.events[0].damage,18)
        counter=result.events[1]
        self.assertTrue(counter.is_counter)
        self.assertEqual(counter.counter_attempt,1)
        self.assertEqual(counter.participant_id,"enemy")
        self.assertEqual(counter.result,"counter_normal")
        self.assertEqual(counter.damage,42)
        self.assertEqual(counter.target_hp_before,40)
        self.assertEqual(counter.target_hp_after,0)
        self.assertEqual(result.hp_by_participant_id["player"],0)
        self.assertEqual(result.events[2].result,"no_target")

    def test_throwing_weapon_counter_gate_stops_chain_without_attack_rng(self):
        player=actor("player","player","player",attack=60,quick=100)
        enemy=actor("enemy","enemy","enemy",attack=60,quick=50)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={
                "player":profile(dex=100),
                "enemy":profile(dex=200,counter_weapon_type="bow"),
            },
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "enemy":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
            },
            counter_rolls_by_attack_id={
                "player":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=None,
                        attack_rolls=None,
                    ),
                ),
                # The enemy's later ordinary attack also reaches the player
                # counter check; the same bow gate prevents RNG there.
                "enemy":(
                    CounterAttemptRolls(
                        counter_check_roll_1_10000=None,
                        attack_rolls=None,
                    ),
                ),
            },
            defense_profile="newpower_70pct",
        )
        counter_events=[event for event in result.events if event.is_counter]
        self.assertEqual(len(counter_events),2)
        self.assertTrue(
            all(event.result=="counter_blocked_weapon" for event in counter_events)
        )
        self.assertTrue(
            all(
                not event.counter_check_resolution.rng_consumed
                for event in counter_events
            )
        )

    def test_dead_submitted_target_retargets_at_execution_time(self):
        player = actor(
            "player", "player", "player",
            hp=100, attack=200, defense=70, quick=100,
        )
        pet = actor(
            "pet", "player", "pet",
            hp=100, attack=150, defense=60, quick=80,
        )
        enemy0 = actor(
            "enemy0", "enemy", "enemy",
            hp=50, attack=10, defense=20, quick=50,
        )
        enemy1 = actor(
            "enemy1", "enemy", "enemy",
            hp=100, attack=10, defense=20, quick=40,
        )
        prepared = prepare_battle_round(
            (player, pet, enemy0, enemy1),
            {
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "pet": BattleCommand(BATTLE_COM_ATTACK, command2=10),
                "enemy0": BattleCommand(BATTLE_COM_WAIT),
                "enemy1": BattleCommand(BATTLE_COM_WAIT),
            },
            {"player": 0, "pet": 0, "enemy0": 0, "enemy1": 0},
        )
        result = resolve_ordinary_round(
            prepared,
            slots={"player": 0, "pet": 1, "enemy0": 10, "enemy1": 11},
            profiles={
                "player": profile(),
                "pet": profile(),
                "enemy0": profile(),
                "enemy1": profile(),
            },
            attack_rolls={
                "player": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                ),
                "pet": OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    retarget_roll=0,
                ),
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].resolved_target_slot, 10)
        self.assertEqual(result.hp_by_slot[10], 0)
        self.assertEqual(result.events[1].participant_id, "pet")
        self.assertTrue(result.events[1].retargeted)
        self.assertEqual(result.events[1].resolved_target_slot, 11)
        self.assertEqual(result.events[2].participant_id, "enemy0")
        self.assertEqual(result.events[2].result, "skipped_dead")

    def test_same_side_live_target_is_outside_status_free_seam(self):
        player = actor("player", "player", "player", quick=100)
        pet = actor("pet", "player", "pet", quick=80)
        enemy = actor("enemy", "enemy", "enemy", quick=40)
        prepared = prepare_battle_round(
            (player, pet, enemy),
            {
                "player": BattleCommand(BATTLE_COM_ATTACK, command2=1),
                "pet": BattleCommand(BATTLE_COM_WAIT),
                "enemy": BattleCommand(BATTLE_COM_WAIT),
            },
            {"player": 0, "pet": 0, "enemy": 0},
        )
        with self.assertRaisesRegex(ValueError, "same-side"):
            resolve_ordinary_round(
                prepared,
                slots={"player": 0, "pet": 1, "enemy": 10},
                profiles={
                    "player": profile(),
                    "pet": profile(),
                    "enemy": profile(),
                },
                attack_rolls={
                    "player": OrdinaryAttackRolls(
                        dodge_roll_1_10000=10000,
                        critical_roll_1_10000=10000,
                        damage_roll=0,
                    )
                },
                defense_profile="newpower_70pct",
            )


    def test_capture_executes_in_action_order_and_exits_target_without_hp_damage(self):
        player=actor("player","player","player",quick=100,level=10)
        enemy=replace(
            actor("enemy","enemy","enemy",quick=20,level=10,hp=10),
            max_hp=100,
            capturable=True,
            capture_default=11,
        )
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_CAPTURE,command2=10),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"enemy":0},
        )
        resolved=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={
                "player":profile(dex=30,luck=3),
                "enemy":profile(dex=15),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            capture_contexts={
                "player":OrdinaryCaptureContext(
                    attacker_charm=50,
                    occupied_pet_slots=(0,2),
                ),
            },
            capture_rolls={
                "player":OrdinaryCaptureRolls(capture_roll_1_100=1),
            },
        )
        event=resolved.events[0]
        self.assertEqual(event.result,"capture_success")
        self.assertEqual(event.target_hp_before,10)
        self.assertEqual(event.target_hp_after,10)
        self.assertEqual(event.capture_resolution.assigned_pet_slot,1)
        self.assertEqual(resolved.exited_participant_ids,("enemy",))
        self.assertEqual(resolved.hp_by_participant_id["enemy"],10)


    def test_escape_runs_in_action_order_and_skips_active_pet_after_player_exit(self):
        player=actor("player","player","player",quick=100,level=10)
        pet=actor("pet","player","pet",quick=80,level=10)
        enemy=actor("enemy","enemy","enemy",quick=20,level=10)
        prepared=prepare_battle_round(
            (player,pet,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ESCAPE),
                "pet":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"pet":1,"enemy":10},
            profiles={
                "player":profile(luck=3),
                "pet":profile(),
                "enemy":profile(),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            escape_contexts={
                "player":OrdinaryEscapeContext(
                    stored_escape_count_before=0,
                ),
            },
            escape_rolls={
                "player":OrdinaryEscapeRolls(1),
            },
        )
        self.assertEqual(result.events[0].result,"escape_success")
        self.assertEqual(result.events[0].escape_resolution.probability,100)
        self.assertEqual(
            result.events[0].escape_resolution.stored_escape_count_after,
            1,
        )
        self.assertEqual(result.events[1].result,"skipped_exited")
        self.assertEqual(
            result.escaped_participant_ids,
            ("player","pet"),
        )
        self.assertEqual(result.hp_by_participant_id["player"],100)
        self.assertEqual(result.hp_by_participant_id["pet"],100)

    def test_failed_escape_keeps_actor_in_round_and_reports_incremented_counter(self):
        player=actor("player","player","player",quick=100,level=10)
        enemy=actor("enemy","enemy","enemy",quick=20,level=30)
        prepared=prepare_battle_round(
            (player,enemy),
            {
                "player":BattleCommand(BATTLE_COM_ESCAPE),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"enemy":10},
            profiles={"player":profile(luck=2),"enemy":profile()},
            attack_rolls={},
            defense_profile="newpower_70pct",
            escape_contexts={
                "player":OrdinaryEscapeContext(
                    stored_escape_count_before=0,
                ),
            },
            escape_rolls={"player":OrdinaryEscapeRolls(40)},
        )
        event=result.events[0]
        self.assertEqual(event.result,"escape_failed")
        self.assertFalse(event.escape_resolution.exits_battle)
        self.assertEqual(event.escape_resolution.probability,40)
        self.assertEqual(event.escape_resolution.stored_escape_count_after,1)
        self.assertEqual(result.escaped_participant_ids,())

    def test_pet_escape_command_is_source_ignored_without_rng(self):
        player=actor("player","player","player",quick=20)
        pet=actor("pet","player","pet",quick=100)
        enemy=actor("enemy","enemy","enemy",quick=10)
        prepared=prepare_battle_round(
            (player,pet,enemy),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "pet":BattleCommand(BATTLE_COM_ESCAPE),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            {"player":0,"pet":0,"enemy":0},
        )
        result=resolve_ordinary_round(
            prepared,
            slots={"player":0,"pet":1,"enemy":10},
            profiles={
                "player":profile(),
                "pet":profile(),
                "enemy":profile(),
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
        )
        self.assertEqual(result.events[0].participant_id,"pet")
        self.assertEqual(result.events[0].result,"escape_ignored_pet")
        self.assertIsNone(result.events[0].escape_resolution)



if __name__ == "__main__":
    unittest.main()
