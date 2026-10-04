import unittest

from tools.stoneage_enemy_ai_wildviolent_bridge import (
    CONDITIONAL_EXECUTION_CHARSET,
    EnemyAiWildViolentSubmission,
    validate_recovered25_wildviolent_population,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_wildviolent_model import (
    CALLBACK_NAME,
    resolve_wildviolent_setup,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    BattleCommandSetupEffects,
    OrdinaryAttackRolls,
    WildViolentRolls,
    _resolve_nonbow_multihit_baseline,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
    BaseStatusTurnRolls,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def synthetic_setup(target=0, packed=0x1234):
    return resolve_wildviolent_setup(
        option="攻%95防%-35避30".encode("cp950"),
        execution_charset="cp950",
        profile="gavin",
        target_slot=target,
        fixed_strength=100,
        fixed_toughness=100,
        attack_power_before=80,
        defense_power_before=90,
        packed_com3_before=packed,
    )


class WildViolentTypedAdmissionTests(unittest.TestCase):
    def test_typed_submission_keeps_symbolic_identity_and_conditional_charset(self):
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",
            skill_slot=0,
            skill_id=541,
            callback=CALLBACK_NAME,
            source_target_slot=0,
            setup=setup,
        )
        self.assertEqual(submission.conditional_execution_charset,CONDITIONAL_EXECUTION_CHARSET)
        self.assertEqual(submission.semantic_command_name,"BATTLE_COM_S_WILDVIOLENTATTACK")
        self.assertEqual(submission.setup.packed_com3 & 0xffff,0x2345)
        self.assertEqual(submission.setup.option.additive_dodge_percent_points,30)

    def test_unreferenced_652_cannot_be_selected_submission(self):
        with self.assertRaisesRegex(ValueError,"selected ID"):
            EnemyAiWildViolentSubmission(
                participant_id="enemy",
                skill_slot=0,
                skill_id=652,
                callback=CALLBACK_NAME,
                source_target_slot=0,
                setup=synthetic_setup(),
            )

    def test_population_validator_rejects_nonexact_synthetic_rows(self):
        bad=Recovered25PetSkillRuntime(
            skills={
                541:Recovered25PetSkillEntry(
                    541,1,6,2,1000,CALLBACK_NAME,
                    "攻%95防%-35避30".encode("cp950"),
                ),
                652:Recovered25PetSkillEntry(
                    652,1,6,2,1000,CALLBACK_NAME,
                    "攻%60防%-50避50".encode("cp950"),
                ),
            },
            source_file="petskill.txt",
        )
        with self.assertRaisesRegex(ValueError,"metadata/OPTION hash drift"):
            validate_recovered25_wildviolent_population(bad)
    def test_nonbow_runtime_repeats_original_target_and_divides_each_hit(self):
        actor=BattleParticipant("enemy","enemy","enemy",20,500,500,100,100,100,"enemy")
        defender=BattleParticipant("player","player","player",20,1000,1000,10,0,50,"player")
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3)
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        result=_resolve_nonbow_multihit_baseline(
            actor=actor,actor_slot=10,command=command,action_value=100,
            by_slot={0:defender,10:actor},hp_by_slot={0:1000,10:500},
            profiles={
                "player":BattleCombatProfile(fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0),
                "enemy":BattleCombatProfile(fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0),
            },
            command_by_slot={0:BattleCommand(0),10:command},
            rolls=WildViolentRolls(3,(hit,hit,hit)),
            defense_profile="newpower_70pct",
            setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            wildviolent_submission=submission,
        )
        self.assertEqual(len(result.events),3)
        self.assertEqual([event.wildviolent_hit_index for event in result.events],[0,1,2])
        self.assertTrue(all(event.original_target_slot==0 for event in result.events))
        self.assertTrue(all(event.wildviolent_attack_count==3 for event in result.events))
        self.assertTrue(all(event.wildviolent_dodge_percent_points==30 for event in result.events))
        self.assertLess(result.hp_by_slot[0],1000)


    def test_action_roll_bundle_closes_three_and_ten_boundaries(self):
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,
            damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        self.assertEqual(len(WildViolentRolls(3,(hit,)*3).hit_rolls),3)
        self.assertEqual(len(WildViolentRolls(10,(hit,)*10).hit_rolls),10)
        with self.assertRaisesRegex(ValueError,"3..10"):
            WildViolentRolls(2,(hit,)*2)
        with self.assertRaisesRegex(ValueError,"3..10"):
            WildViolentRolls(11,(hit,)*11)
        with self.assertRaisesRegex(ValueError,"exactly count-roll"):
            WildViolentRolls(3,(hit,)*2)

    def test_dead_original_retargets_each_later_wildviolent_hit(self):
        actor=BattleParticipant(
            "enemy","enemy","enemy",20,500,500,100,100,100,"enemy"
        )
        original=BattleParticipant(
            "original","player","pet",20,1,1,10,0,50,"original"
        )
        p1=BattleParticipant("p1","player","pet",20,1000,1000,10,0,50,"p1")
        p2=BattleParticipant("p2","player","pet",20,1000,1000,10,0,50,"p2")
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(
            BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3
        )
        hits=(
            OrdinaryAttackRolls(
                critical_roll_1_10000=10000,damage_roll=0,
                dodge_roll_1_10000=10000,
            ),
            OrdinaryAttackRolls(
                critical_roll_1_10000=10000,damage_roll=0,
                dodge_roll_1_10000=10000,retarget_roll=0,
            ),
            OrdinaryAttackRolls(
                critical_roll_1_10000=10000,damage_roll=0,
                dodge_roll_1_10000=10000,retarget_roll=1,
            ),
        )
        result=_resolve_nonbow_multihit_baseline(
            actor=actor,actor_slot=10,command=command,action_value=100,
            by_slot={0:original,1:p1,2:p2,10:actor},
            hp_by_slot={0:1,1:1000,2:1000,10:500},
            profiles={
                "original":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "p1":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "p2":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            command_by_slot={
                0:BattleCommand(BATTLE_COM_WAIT),
                1:BattleCommand(BATTLE_COM_WAIT),
                2:BattleCommand(BATTLE_COM_WAIT),
                10:command,
            },
            rolls=WildViolentRolls(3,hits),
            defense_profile="newpower_70pct",
            setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            wildviolent_submission=submission,
        )
        self.assertEqual(
            tuple(event.resolved_target_slot for event in result.events),
            (0,1,2),
        )
        self.assertEqual(result.hp_by_slot[0],0)
        self.assertTrue(result.events[1].retargeted)
        self.assertTrue(result.events[2].retargeted)

    def _status_suppression_case(self, status, status_rolls=None, attack_rolls=None):
        actor=BattleParticipant(
            "enemy","enemy","enemy",20,500,500,100,100,100,"enemy"
        )
        defender=BattleParticipant(
            "player","player","player",20,1000,1000,10,0,50,"player"
        )
        setup=synthetic_setup(target=0,packed=0x2345)
        submission=EnemyAiWildViolentSubmission(
            participant_id="enemy",skill_slot=0,skill_id=541,
            callback=CALLBACK_NAME,source_target_slot=0,setup=setup,
        )
        command=BattleCommand(
            BATTLE_COM_ATTACK,command2=0,command3=setup.packed_com3
        )
        prepared=prepare_battle_round(
            (defender,actor),
            {
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":command,
            },
            {"player":0,"enemy":0},
        )
        kwargs=dict(
            slots={"player":0,"enemy":10},
            profiles={
                "player":BattleCombatProfile(
                    fixed_dex=50,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
                "enemy":BattleCombatProfile(
                    fixed_dex=100,fixed_luck=0,earth=0,water=0,fire=0,wind=0
                ),
            },
            attack_rolls=dict(attack_rolls or {}),
            wildviolent_submissions_by_participant_id={"enemy":submission},
            command_setup_effects_by_participant_id={
                "enemy":BattleCommandSetupEffects(
                    attack_power=setup.attack_power,
                    defense_power=setup.defense_power,
                )
            },
            base_status_runtime_by_participant_id={
                "player":BaseBattleStatusRuntime(work_quick=50),
                "enemy":BaseBattleStatusRuntime(
                    status=status,work_quick=100
                ),
            },
            base_status_rolls_by_participant_id=(
                {} if status_rolls is None else {"enemy":status_rolls}
            ),
            defense_profile="newpower_70pct",
        )
        return prepared,kwargs

    def test_sleep_suppresses_action_time_rng_and_rejects_preconsumption(self):
        prepared,kwargs=self._status_suppression_case(
            BaseBattleStatusState(sleep=2)
        )
        result=resolve_ordinary_round(prepared,**kwargs)
        self.assertFalse(
            any(event.wildviolent_skill_id is not None for event in result.events)
        )
        hit=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        with self.assertRaisesRegex(ValueError,"unused WildViolentAttack"):
            resolve_ordinary_round(
                prepared,
                **kwargs,
                wildviolent_rolls_by_attack_id={
                    "enemy":WildViolentRolls(3,(hit,hit,hit))
                },
            )

    def test_confusion_rewrite_suppresses_wildviolent_semantic_action(self):
        ordinary=OrdinaryAttackRolls(
            critical_roll_1_10000=10000,damage_roll=0,
            dodge_roll_1_10000=10000,
        )
        prepared,kwargs=self._status_suppression_case(
            BaseBattleStatusState(confusion=2),
            BaseStatusTurnRolls(
                confusion_action_roll_1_100=1,
                confusion_side_roll_0_1=0,
                confusion_pos_roll_0_9=0,
            ),
            {"enemy":ordinary},
        )
        result=resolve_ordinary_round(prepared,**kwargs)
        ticks=[
            event for event in result.events
            if event.participant_id=="enemy"
            and event.status_tick_resolution is not None
        ]
        self.assertEqual(len(ticks),1)
        self.assertTrue(ticks[0].status_tick_resolution.confusion_rewrote_command)
        self.assertFalse(
            any(event.wildviolent_skill_id is not None for event in result.events)
        )
        with self.assertRaisesRegex(ValueError,"unused WildViolentAttack"):
            resolve_ordinary_round(
                prepared,
                **kwargs,
                wildviolent_rolls_by_attack_id={
                    "enemy":WildViolentRolls(3,(ordinary,ordinary,ordinary))
                },
            )


if __name__=="__main__":
    unittest.main()
