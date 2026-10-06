import unittest

from tools.stoneage_battle_guardian_model import GuardianRegistration
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_GUARD,
    BATTLE_COM_NONE,
    BATTLE_COM_S_BECOMEFOX,
    BATTLE_COM_S_RENZOKU,
    BattleCombatProfile,
    BattleCommand,
    OrdinaryAttackRolls,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_becomefox_reference_model import FOX_IMAGE, FoxState
from tools.stoneage_becomefox_runtime_state import (
    BecomeFoxRuntimeOverlay,
    FoxParticipantRuntime,
    PROFILE_GAVIN,
)
from tools.stoneage_enemy_ai_becomefox_bridge import (
    CALLBACK_NAME,
    EnemyAiBecomeFoxSubmission,
)
from tools.stoneage_singleplayer_battle import BattleParticipant


def actor(pid,side,kind,*,hp=1000,attack=100,defense=20,quick=50,level=10):
    return BattleParticipant(
        participant_id=pid,side=side,kind=kind,level=level,
        hp=hp,max_hp=max(hp,1000),attack=attack,defense=defense,quick=quick,
        name=pid,fixed_vital=40,
    )


def profile(dex=100):
    return BattleCombatProfile(
        fixed_dex=dex,fixed_luck=0,
        earth=0,water=0,fire=0,wind=0,
        weapon_critical=0,counter_weapon_type="fist",
    )


def rolls(*,dodge=10000,retarget=None,guard=None):
    return OrdinaryAttackRolls(
        critical_roll_1_10000=10000,
        damage_roll=0,
        dodge_roll_1_10000=dodge,
        guard_roll_1_100=guard,
        retarget_roll=retarget,
    )


def submission(target=5):
    return EnemyAiBecomeFoxSubmission(
        participant_id="caster",skill_slot=2,skill_id=625,
        callback=CALLBACK_NAME,source_target_slot=target,
        source_profile=PROFILE_GAVIN,
    )


def main_event(result,pid):
    return next(
        event for event in result.events
        if event.participant_id==pid and not event.is_counter
        and event.result!="status_tick"
    )


class BecomeFoxOrderedRoundTests(unittest.TestCase):
    def resolve_transform_round(self,*,guardian=False,draw=0,target_kind="pet"):
        pet=actor("pet","player",target_kind,attack=100,defense=0,quick=70)
        caster=actor("caster","enemy","enemy",attack=180,defense=10,quick=100)
        dummy=actor("dummy","enemy","enemy",hp=2000,defense=0,quick=10)
        participants=[caster,pet,dummy]
        commands={
            "caster":BattleCommand(BATTLE_COM_S_BECOMEFOX,command2=5),
            "pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
            "dummy":BattleCommand(BATTLE_COM_NONE),
        }
        kwargs={}
        slots={"caster":15,"pet":5,"dummy":16}
        profiles={"caster":profile(120),"pet":profile(90),"dummy":profile(80)}
        initiatives={"caster":0,"pet":0,"dummy":0}
        if guardian:
            guard=actor("guard","player","pet",hp=2000,defense=0,quick=20)
            participants=[caster,pet,guard,dummy]
            commands["guard"]=BattleCommand(BATTLE_COM_GUARD)
            slots["guard"]=6
            profiles["guard"]=profile(80)
            initiatives["guard"]=0
            kwargs["guardian_registrations_by_defender_slot"]={
                5:GuardianRegistration(guardian_slot=6,guardian_flag=True)
            }
        prepared=prepare_battle_round(participants,commands,initiatives)
        return resolve_ordinary_round(
            prepared,
            slots=slots,
            profiles=profiles,
            attack_rolls={
                "caster":rolls(guard=100 if guardian else None),
                "pet":rolls(),
            },
            defense_profile="newpower_70pct",
            becomefox_submissions_by_participant_id={"caster":submission()},
            becomefox_draws_by_participant_id={"caster":draw},
            becomefox_current_turn=4,
            becomefox_target_petflag_by_participant_id=(
                {"pet":1} if target_kind!="player" else {}
            ),
            becomefox_base_image_by_participant_id=(
                {"pet":101111} if target_kind!="player" else {}
            ),
            becomefox_attacker_pig_marker_by_participant_id={"caster":-1},
            **kwargs,
        )

    def test_hit_transforms_then_later_pet_action_uses_80pct_powers(self):
        transformed=self.resolve_transform_round()
        event=main_event(transformed,"caster")
        self.assertEqual(event.command1,BATTLE_COM_S_BECOMEFOX)
        self.assertTrue(event.becomefox_decision.draw_consumed)
        self.assertTrue(event.becomefox_decision.transformed)
        fox=transformed.becomefox_overlay.runtime_by_participant_id["pet"].state
        self.assertEqual(fox.fox_round,4)
        self.assertEqual(fox.base_image,FOX_IMAGE)
        self.assertEqual((fox.attack_power,fox.defence_power,fox.quick),(80,0,56))

        pet=actor("pet","player","pet",attack=100,defense=0,quick=70)
        caster=actor("caster","enemy","enemy",attack=180,defense=10,quick=100)
        dummy=actor("dummy","enemy","enemy",hp=2000,defense=0,quick=10)
        prepared=prepare_battle_round(
            (caster,pet,dummy),
            {
                "caster":BattleCommand(BATTLE_COM_ATTACK,command2=5),
                "pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
                "dummy":BattleCommand(BATTLE_COM_NONE),
            },
            {"caster":0,"pet":0,"dummy":0},
        )
        baseline=resolve_ordinary_round(
            prepared,slots={"caster":15,"pet":5,"dummy":16},
            profiles={"caster":profile(120),"pet":profile(90),"dummy":profile(80)},
            attack_rolls={"caster":rolls(),"pet":rolls()},
            defense_profile="newpower_70pct",
        )
        self.assertGreater(
            main_event(baseline,"pet").damage,
            main_event(transformed,"pet").damage,
        )

    def test_recovery_happens_after_expiring_actor_uses_reduced_powers(self):
        pet=actor("pet","player","pet",attack=100,defense=20,quick=70)
        dummy=actor("dummy","enemy","enemy",hp=2000,defense=0,quick=10)
        prepared=prepare_battle_round(
            (pet,dummy),
            {"pet":BattleCommand(BATTLE_COM_ATTACK,command2=16),
             "dummy":BattleCommand(BATTLE_COM_NONE)},
            {"pet":0,"dummy":0},
        )
        overlay=BecomeFoxRuntimeOverlay({
            "pet":FoxParticipantRuntime(
                PROFILE_GAVIN,
                FoxState(
                    base_image=FOX_IMAGE,base_base_image=101111,
                    attack_power=100,defence_power=20,quick=70,
                    fix_str=100,fix_tough=20,fix_dex=70,
                    fox_round=4,ride_pet=-1,petfall=0,
                ),
            )
        })
        expired=resolve_ordinary_round(
            prepared,slots={"pet":5,"dummy":16},
            profiles={"pet":profile(90),"dummy":profile(80)},
            attack_rolls={"pet":rolls()},
            defense_profile="newpower_70pct",
            becomefox_overlay=overlay,becomefox_current_turn=7,
        )
        baseline=resolve_ordinary_round(
            prepared,slots={"pet":5,"dummy":16},
            profiles={"pet":profile(90),"dummy":profile(80)},
            attack_rolls={"pet":rolls()},
            defense_profile="newpower_70pct",
        )
        self.assertLess(
            main_event(expired,"pet").damage,
            main_event(baseline,"pet").damage,
        )
        self.assertFalse(expired.becomefox_overlay.runtime_by_participant_id)
        self.assertEqual(
            expired.base_status_runtime_by_participant_id["pet"].work_quick,70
        )

    def test_player_target_consumes_reached_draw_but_never_transforms(self):
        result=self.resolve_transform_round(target_kind="player")
        event=main_event(result,"caster")
        self.assertTrue(event.becomefox_decision.draw_consumed)
        self.assertFalse(event.becomefox_decision.transformed)
        self.assertFalse(result.becomefox_overlay.runtime_by_participant_id)

    def test_dodge_blocks_transform_and_owns_no_becomefox_draw(self):
        pet=actor("pet","player","pet",attack=100,defense=0,quick=70)
        caster=actor("caster","enemy","enemy",attack=180,defense=10,quick=100)
        prepared=prepare_battle_round(
            (caster,pet),
            {"caster":BattleCommand(BATTLE_COM_S_BECOMEFOX,command2=5),
             "pet":BattleCommand(BATTLE_COM_NONE)},
            {"caster":0,"pet":0},
        )
        result=resolve_ordinary_round(
            prepared,slots={"caster":15,"pet":5},
            profiles={"caster":profile(1),"pet":profile(1000)},
            attack_rolls={"caster":rolls(dodge=1)},
            defense_profile="newpower_70pct",
            becomefox_submissions_by_participant_id={"caster":submission()},
            becomefox_draws_by_participant_id={"caster":None},
            becomefox_current_turn=2,
            becomefox_target_petflag_by_participant_id={"pet":1},
            becomefox_base_image_by_participant_id={"pet":101111},
            becomefox_attacker_pig_marker_by_participant_id={"caster":-1},
        )
        event=main_event(result,"caster")
        self.assertEqual(event.result,"dodge")
        self.assertFalse(event.becomefox_decision.draw_consumed)
        self.assertFalse(event.becomefox_decision.transformed)

    def test_guardian_redirect_damages_guardian_but_foxes_original_target(self):
        result=self.resolve_transform_round(guardian=True)
        event=main_event(result,"caster")
        self.assertTrue(event.guardian_redirected)
        self.assertEqual(event.guarded_target_slot,5)
        self.assertEqual(event.guardian_slot,6)
        self.assertTrue(event.becomefox_decision.transformed)
        self.assertIn("pet",result.becomefox_overlay.runtime_by_participant_id)
        self.assertNotIn("guard",result.becomefox_overlay.runtime_by_participant_id)

    def test_active_fox_demotes_disallowed_special_command_to_none(self):
        pet=actor("pet","player","pet",quick=70)
        dummy=actor("dummy","enemy","enemy",quick=10)
        prepared=prepare_battle_round(
            (pet,dummy),
            {
                "pet":BattleCommand(BATTLE_COM_S_RENZOKU,command2=16,command3=2),
                "dummy":BattleCommand(BATTLE_COM_NONE),
            },
            {"pet":0,"dummy":0},
        )
        overlay=BecomeFoxRuntimeOverlay({
            "pet":FoxParticipantRuntime(
                PROFILE_GAVIN,
                FoxState(
                    base_image=FOX_IMAGE,base_base_image=101111,
                    attack_power=100,defence_power=20,quick=70,
                    fix_str=100,fix_tough=20,fix_dex=70,
                    fox_round=1,ride_pet=-1,petfall=0,
                ),
            )
        })
        result=resolve_ordinary_round(
            prepared,slots={"pet":5,"dummy":16},
            profiles={"pet":profile(),"dummy":profile()},
            attack_rolls={},
            defense_profile="newpower_70pct",
            becomefox_overlay=overlay,becomefox_current_turn=2,
        )
        event=main_event(result,"pet")
        self.assertEqual(event.command1,BATTLE_COM_NONE)
        self.assertEqual(event.result,"status_no_action")
        self.assertIn("pet",result.becomefox_overlay.runtime_by_participant_id)


if __name__=="__main__":
    unittest.main()
