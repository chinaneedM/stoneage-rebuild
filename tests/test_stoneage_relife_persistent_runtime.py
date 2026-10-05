import unittest

from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
)
from tools.stoneage_battle_state_model import (
    ACTIVE,
    begin_persistent_battle,
    resolve_persistent_ordinary_round,
)
from tools.stoneage_enemy_ai_relife_bridge import EnemyAiReLifeSubmission
from tools.stoneage_enemy_relife_model import EnemyReLifeRolls
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import (
    EncounterRequest,
    EnemyVariantId,
    MapPosition,
    PetTemplateId,
)


def participant(
    pid,side,kind,*,hp=100,max_hp=None,attack=100,defense=20,quick=50,
    reward_exp=None,
):
    return BattleParticipant(
        participant_id=pid,
        side=side,
        kind=kind,
        level=10,
        hp=hp,
        max_hp=hp if max_hp is None else max_hp,
        attack=attack,
        defense=defense,
        quick=quick,
        name=pid,
        fixed_vital=40,
        reward_exp=reward_exp,
    )


def session(player,enemies):
    encounter=EncounterRequest(
        position=MapPosition(2000,10,10),
        area_index=1,
        group_id=1,
        enemy_variant_id=EnemyVariantId(10),
        pet_template_id=PetTemplateId(20),
        level=5,
        max_enemy_count=len(enemies),
    )
    return BattleSession(
        origin_position=encounter.position,
        encounter=encounter,
        player=player,
        allied_pets=(),
        enemies=tuple(enemies),
        ride_pet=None,
    )


def profile():
    return BattleCombatProfile(
        fixed_dex=100,
        fixed_luck=0,
        earth=0,
        water=0,
        fire=0,
        wind=0,
    )


def relife_submission():
    return EnemyAiReLifeSubmission(
        participant_id="enemy:caster",
        skill_slot=4,
        skill_id=500,
        callback="ENEMYSKILL_ReLife",
        source_attack_target_slot=0,
    )


class ReLifePersistentRuntimeTests(unittest.TestCase):
    def initial_state(self):
        player=participant(
            "player","player","player",
            hp=500,attack=200,defense=20,quick=200,
        )
        caster=participant(
            "enemy:caster","enemy","enemy",
            hp=500,attack=100,defense=20,quick=100,reward_exp=1,
        )
        victim=participant(
            "enemy:victim","enemy","enemy",
            hp=1,max_hp=101,attack=10,defense=0,quick=20,reward_exp=7,
        )
        return begin_persistent_battle(
            session(player,(caster,victim)),
            slots={"player":0,"enemy:caster":10,"enemy:victim":11},
        )

    def test_ordinary_death_persists_as_revivable_then_reenters_living_set(self):
        state=self.initial_state()
        profiles={
            "player":profile(),
            "enemy:caster":profile(),
            "enemy:victim":profile(),
        }
        first=resolve_persistent_ordinary_round(
            state,
            commands={
                "player":BattleCommand(BATTLE_COM_ATTACK,command2=11),
                "enemy:caster":BattleCommand(BATTLE_COM_WAIT),
                "enemy:victim":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={
                "player":0,"enemy:caster":0,"enemy:victim":0,
            },
            profiles=profiles,
            attack_rolls={
                "player":OrdinaryAttackRolls(
                    dodge_roll_1_10000=10000,
                    critical_roll_1_10000=10000,
                    damage_roll=0,
                    minimum_damage_roll_0_1=1,
                )
            },
            defense_profile="newpower_70pct",
        )
        self.assertEqual(first.after.phase,ACTIVE)
        self.assertEqual(first.after.hp_by_participant_id["enemy:victim"],0)
        self.assertEqual(
            first.after.revivable_dead_participant_ids,
            ("enemy:victim",),
        )
        exp_after_kill=int(
            first.after.pending_exp_by_participant_id["player"]
        )
        self.assertGreaterEqual(exp_after_kill,7)

        second=resolve_persistent_ordinary_round(
            first.after,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:caster":BattleCommand(BATTLE_COM_ATTACK,command2=0),
            },
            initiative_random_subtracts={
                "player":0,"enemy:caster":0,
            },
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
            enemy_relife_submissions_by_participant_id={
                "enemy:caster":relife_submission(),
            },
            enemy_relife_rolls_by_participant_id={
                "enemy:caster":EnemyReLifeRolls(0,55),
            },
            enemy_relife_retarget_rolls_by_participant_id={
                "enemy:caster":None,
            },
        )
        self.assertEqual(
            second.after.hp_by_participant_id["enemy:victim"],
            55,
        )
        self.assertEqual(second.after.revivable_dead_participant_ids,())
        self.assertEqual(
            int(second.after.pending_exp_by_participant_id["player"]),
            exp_after_kill,
        )
        revive=next(
            event for event in second.round.events
            if event.result=="enemy_relife"
        )
        self.assertEqual(revive.resolved_target_slot,11)
        self.assertEqual(
            revive.enemy_relife_resolution.selected_participant_id,
            "enemy:victim",
        )

        third=resolve_persistent_ordinary_round(
            second.after,
            commands={
                "player":BattleCommand(BATTLE_COM_WAIT),
                "enemy:caster":BattleCommand(BATTLE_COM_WAIT),
                "enemy:victim":BattleCommand(BATTLE_COM_WAIT),
            },
            initiative_random_subtracts={
                "player":0,"enemy:caster":0,"enemy:victim":0,
            },
            profiles=profiles,
            attack_rolls={},
            defense_profile="newpower_70pct",
        )
        self.assertEqual(third.after.turn,3)
        self.assertEqual(
            set(third.round.action_order),
            {"player","enemy:caster","enemy:victim"},
        )

    def test_revivable_state_rejects_ultimate_or_exit_overlap(self):
        state=self.initial_state()
        from dataclasses import replace
        with self.assertRaisesRegex(
            ValueError,"battle-exited participants cannot remain revivable"
        ):
            replace(
                state,
                hp_by_participant_id={
                    **dict(state.hp_by_participant_id),
                    "enemy:victim":0,
                },
                battle_exited_participant_ids=("enemy:victim",),
                revivable_dead_participant_ids=("enemy:victim",),
            )


if __name__=="__main__":
    unittest.main()
