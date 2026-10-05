import unittest

from tools.stoneage_2battletimid_reference_model import (
    PROFILE_BIG5,
    PROFILE_UTF8,
    resolve_2battletimid_setup,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
)
from tools.stoneage_battle_state_model import (
    ACTIVE,
    active_participants,
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_ai_2battletimid_bridge import (
    EnemyAiTwoBattleTimidSubmission,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


RAW_OPTION=b"-\xa7\xf0%50+\xb1\xd3%30\xa9R%60"


def actor(
    pid,
    side,
    kind,
    *,
    hp=500,
    attack=100,
    defense=0,
    quick=50,
    level=20,
    source_pet_slot=None,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=level,
        hp=hp,
        max_hp=max(1,hp),
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
        source_pet_slot=source_pet_slot,
    )


def profile(*,dex=100):
    return BattleCombatProfile(
        fixed_dex=dex,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def attack_rolls():
    return OrdinaryAttackRolls(
        dodge_roll_1_10000=10000,
        critical_roll_1_10000=10000,
        damage_roll=0,
        minimum_damage_roll_0_1=1,
    )


def session(player,enemies,*,pets=()):
    encounter=EncounterRequest(
        position=MapPosition(2000,10,10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(20),
        level=5,
        max_enemy_count=max(1,len(enemies)),
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=tuple(pets),
        enemies=tuple(enemies),
    )


def submission(
    *,
    profile_name=PROFILE_BIG5,
    target_slot=5,
    participant_id="enemy",
    fixed_strength=200,
    fixed_toughness=0,
    fixed_dex=100,
):
    fixed=(fixed_strength,fixed_toughness,fixed_dex)
    setup=resolve_2battletimid_setup(
        RAW_OPTION,
        profile=profile_name,
        target_slot=target_slot,
        skill_array=0,
        packed_com3_before=0,
        fixed_powers=fixed,
        powers_before=fixed,
        valid_actor=True,
    )
    return EnemyAiTwoBattleTimidSubmission(
        participant_id=participant_id,
        skill_slot=3,
        skill_id=636,
        callback="PETSKILL_2BattleTimid",
        source_target_slot=target_slot,
        profile=profile_name,
        raw_option=RAW_OPTION,
        setup=setup,
    )


class TwoBattleTimidRuntimeTests(unittest.TestCase):
    def make_state(self,*,noreturn=False,pet_slot=5,with_second_enemy=False):
        player=actor(
            "player","player","player",
            hp=120,defense=0,quick=20,
        )
        pet=actor(
            "pet:0","player","pet",
            hp=500,attack=80,defense=0,quick=10,source_pet_slot=0,
        )
        enemy=actor(
            "enemy","enemy","enemy",
            hp=500,attack=200,defense=0,quick=100,
        )
        enemies=[enemy]
        slots={"player":0,"pet:0":pet_slot,"enemy":10}
        if with_second_enemy:
            enemy2=actor(
                "enemy:2","enemy","enemy",
                hp=500,attack=300,defense=0,quick=90,
            )
            enemies.append(enemy2)
            slots["enemy:2"]=11
        state=begin_persistent_battle(
            session(player,enemies,pets=(pet,)),
            slots=slots,
            default_pet_slot=0,
            pet_noreturn_by_participant_id={"pet:0":bool(noreturn)},
        )
        return state

    @staticmethod
    def skill_event(result):
        return next(
            event for event in result.round.events
            if event.two_battletimid_skill_id==636
        )

    def resolve_pet_round(
        self,
        state,
        *,
        draw=59,
        sub=None,
        extra_enemy_attack=False,
    ):
        sub=sub or submission()
        commands={
            "player":BattleCommand(BATTLE_COM_WAIT),
            "pet:0":BattleCommand(BATTLE_COM_WAIT),
            "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=5),
        }
        initiatives={"player":0,"pet:0":0,"enemy":0}
        profiles={
            "player":profile(),
            "pet:0":profile(),
            "enemy":profile(),
        }
        attacks={"enemy":attack_rolls()}
        if extra_enemy_attack:
            commands["enemy:2"]=BattleCommand(BATTLE_COM_ATTACK,command2=0)
            initiatives["enemy:2"]=0
            profiles["enemy:2"]=profile()
            attacks["enemy:2"]=attack_rolls()
        return resolve_persistent_ordinary_round(
            state,
            commands=commands,
            initiative_random_subtracts=initiatives,
            profiles=profiles,
            attack_rolls=attacks,
            defense_profile="newpower_70pct",
            two_battletimid_submissions_by_participant_id={"enemy":sub},
            two_battletimid_rolls_by_participant_id={"enemy":draw},
            tie_break_order=("enemy","enemy:2","player","pet:0"),
        )

    def test_big5_successful_recall_clears_selection_but_preserves_owned_pet(self):
        state=self.make_state(noreturn=False)
        result=self.resolve_pet_round(state,draw=59)
        event=self.skill_event(result)

        self.assertEqual(event.two_battletimid_profile,PROFILE_BIG5)
        self.assertEqual(event.two_battletimid_resolution.chance,60)
        self.assertEqual(event.two_battletimid_resolution.rng_draws,1)
        self.assertTrue(event.two_battletimid_resolution.pet_recall_requested)
        self.assertTrue(event.two_battletimid_resolution.pet_withdrawn)
        self.assertEqual(event.two_battletimid_resolution.status_notifications,2)
        self.assertEqual(event.two_battletimid_resolution.bs_frames,1)
        self.assertIsNone(result.after.default_pet_slot)
        self.assertIn("pet:0",result.after.battle_exited_participant_ids)
        self.assertEqual(len(result.after.session.allied_pets),1)
        self.assertGreater(result.after.hp_by_participant_id["pet:0"],0)
        self.assertTrue(any(
            event.participant_id=="pet:0" and event.result=="skipped_exited"
            for event in result.round.events
        ))

        active_ids={
            str(participant.participant_id)
            for participant in active_participants(result.after)
        }
        self.assertNotIn("pet:0",active_ids)

        follow=resolve_persistent_ordinary_round(
            result.after,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={},
            defense_profile="newpower_70pct",
        )
        self.assertNotIn(
            "pet:0",
            {str(x.participant_id) for x in active_participants(follow.after)},
        )

    def test_noreturn_block_keeps_default_and_pet_active_same_and_next_round(self):
        state=self.make_state(noreturn=True)
        result=self.resolve_pet_round(state,draw=59)
        event=self.skill_event(result)

        self.assertTrue(event.two_battletimid_resolution.pet_recall_requested)
        self.assertFalse(event.two_battletimid_resolution.pet_withdrawn)
        self.assertEqual(event.two_battletimid_resolution.status_notifications,2)
        self.assertEqual(event.two_battletimid_resolution.bs_frames,0)
        self.assertEqual(result.after.default_pet_slot,0)
        self.assertNotIn("pet:0",result.after.battle_exited_participant_ids)
        self.assertTrue(any(
            event.participant_id=="pet:0" and event.result=="wait"
            for event in result.round.events
        ))
        self.assertIn(
            "pet:0",
            {str(x.participant_id) for x in active_participants(result.after)},
        )

    def test_utf8_profile_keeps_powers_and_has_zero_recall_chance(self):
        state=self.make_state(noreturn=False)
        sub=submission(profile_name=PROFILE_UTF8)
        self.assertEqual(sub.setup.powers,(200,0,100))
        result=self.resolve_pet_round(state,draw=0,sub=sub)
        event=self.skill_event(result)
        self.assertEqual(event.two_battletimid_profile,PROFILE_UTF8)
        self.assertEqual(event.two_battletimid_resolution.chance,0)
        self.assertEqual(event.two_battletimid_resolution.rng_draws,1)
        self.assertFalse(event.two_battletimid_resolution.pet_recall_requested)
        self.assertEqual(result.after.default_pet_slot,0)

    def test_pet_target_requires_authoritative_noreturn_and_owner_aligned_slot(self):
        player=actor("player","player","player",quick=20)
        pet=actor(
            "pet:0","player","pet",
            hp=500,quick=10,source_pet_slot=0,
        )
        enemy=actor("enemy","enemy","enemy",attack=200,quick=100)
        missing=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,)),
            slots={"player":0,"pet:0":5,"enemy":10},
            default_pet_slot=0,
        )
        with self.assertRaisesRegex(ValueError,"NORETURN"):
            self.resolve_pet_round(missing,draw=59)

        misaligned=begin_persistent_battle(
            session(player,(enemy,),pets=(pet,)),
            slots={"player":0,"pet:0":6,"enemy":10},
            default_pet_slot=0,
            pet_noreturn_by_participant_id={"pet:0":False},
        )
        with self.assertRaisesRegex(ValueError,"owner-aligned"):
            self.resolve_pet_round(
                misaligned,
                draw=59,
                sub=submission(target_slot=6),
            )

    def test_successful_recall_precedes_later_player_death_penalty(self):
        state=self.make_state(noreturn=False,with_second_enemy=True)
        result=self.resolve_pet_round(
            state,
            draw=59,
            extra_enemy_attack=True,
        )
        recall=self.skill_event(result)
        self.assertTrue(recall.two_battletimid_resolution.pet_withdrawn)
        death=next(
            event for event in result.round.events
            if (
                event.resolved_target_slot==0
                and event.target_hp_after==0
            )
        )
        self.assertEqual(death.participant_id,"enemy:2")
        self.assertIsNone(result.after.default_pet_slot)
        self.assertEqual(
            result.after.pending_pet_variable_ai_by_participant_id["pet:0"],
            0,
        )

    def test_player_target_consumes_event_draw_without_recall(self):
        player=actor("player","player","player",hp=500,quick=20)
        enemy=actor("enemy","enemy","enemy",attack=200,quick=100)
        state=begin_persistent_battle(
            session(player,(enemy,)),
            slots={"player":0,"enemy":10},
        )
        sub=submission(target_slot=0)
        result=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={"player":0,"enemy":0},
            profiles={"player":profile(),"enemy":profile()},
            attack_rolls={"enemy":attack_rolls()},
            defense_profile="newpower_70pct",
            two_battletimid_submissions_by_participant_id={"enemy":sub},
            two_battletimid_rolls_by_participant_id={"enemy":59},
        )
        event=self.skill_event(result)
        self.assertEqual(event.two_battletimid_resolution.rng_draws,1)
        self.assertFalse(event.two_battletimid_resolution.pet_recall_requested)
        self.assertEqual(event.two_battletimid_resolution.bs_frames,0)


if __name__ == "__main__":
    unittest.main()
