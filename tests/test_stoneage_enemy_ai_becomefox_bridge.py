from dataclasses import replace
from types import SimpleNamespace
import unittest

from tools.stoneage_becomefox_reference_model import FoxState
from tools.stoneage_becomefox_runtime_state import PROFILE_BISMARCK,PROFILE_GAVIN
from tools.stoneage_enemy_ai_becomefox_bridge import (
    resolve_enemy_ai_becomefox_submission,
    validate_recovered25_becomefox_population,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,Recovered25PetSkillRuntime,
)


def runtime():
    return Recovered25PetSkillRuntime({
        625:Recovered25PetSkillEntry(
            625,1,1,2,3000,"PETSKILL_BecomeFox",b""
        )
    },"synthetic")


def spawned(tempno=148):
    graphic,base={
        148:(101743,(32,40,26,30,150)),
        149:(101744,(28,45,22,32,150)),
    }[tempno]
    return SimpleNamespace(
        participant=SimpleNamespace(
            participant_id=f"enemy:{tempno}",side="enemy",kind="enemy"
        ),
        template=SimpleNamespace(
            tempno=tempno,graphic_id=graphic,
            base_vital=base[0],base_strength=base[1],
            base_toughness=base[2],base_dexterity=base[3],ai=base[4],
            skill_slot_ids=(0,0,625,0,0,0,0),
        ),
    )


class EnemyAiBecomeFoxBridgeTests(unittest.TestCase):
    def resolve(self,*,actor=None,rt=None,profile=PROFILE_GAVIN,slot=2,target=5):
        return resolve_enemy_ai_becomefox_submission(
            actor or spawned(),skill_slot=slot,target_slot=target,
            petskill_runtime=rt or runtime(),source_profile=profile,
        )

    def test_both_exact_templates_admit_only_runtime_index2_id625(self):
        for tempno in (148,149):
            got=self.resolve(actor=spawned(tempno))
            self.assertEqual((got.skill_slot,got.skill_id,got.source_target_slot),(2,625,5))
            self.assertEqual(got.semantic_command_name,"BATTLE_COM_S_BECOMEFOX")

    def test_population_metadata_option_and_extra_rows_fail_closed(self):
        rt=runtime()
        for field,value in (
            ("target",3),("cost",3),("illegal",0),("option_bytes",b"x"),
            ("function_name","PETSKILL_BecomePig"),
        ):
            rows=dict(rt.skills)
            rows[625]=replace(rows[625],**{field:value})
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_recovered25_becomefox_population(
                    Recovered25PetSkillRuntime(rows,"mutated")
                )
        rows=dict(rt.skills)
        rows[700]=replace(rows[625],skill_id=700)
        with self.assertRaisesRegex(ValueError,"population"):
            validate_recovered25_becomefox_population(
                Recovered25PetSkillRuntime(rows,"extra")
            )

    def test_template_slot_stats_ai_actor_and_profile_are_exact(self):
        for field,value in (
            ("graphic_id",101744),("base_vital",33),("base_strength",41),
            ("base_toughness",27),("base_dexterity",31),("ai",151),
            ("skill_slot_ids",(0,625,0,0,0,0,0)),
        ):
            actor=spawned()
            setattr(actor.template,field,value)
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.resolve(actor=actor)
        for key,value in (("side","player"),("kind","pet")):
            actor=spawned()
            setattr(actor.participant,key,value)
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.resolve(actor=actor)
        with self.assertRaises(ValueError):
            self.resolve(profile="unknown")

    def test_postattack_preserves_profile_arrange_divergence_and_draw_ownership(self):
        state=FoxState(
            base_image=101743,base_base_image=101743,
            attack_power=40,defence_power=26,quick=30,
            fix_str=40,fix_tough=26,fix_dex=30,
            fox_round=-1,ride_pet=-1,petfall=0,
        )
        old=self.resolve(profile=PROFILE_GAVIN)
        decision,active=old.postattack(
            state,attack_result="ARRANGE",target_alive=True,
            draw_mod_100=None,target_is_player=False,target_petflag=1,
            attacker_pig_marker=-1,current_turn=4,
        )
        self.assertFalse(decision.draw_consumed)
        self.assertIsNone(active)

        new=self.resolve(profile=PROFILE_BISMARCK)
        decision,active=new.postattack(
            state,attack_result="ARRANGE",target_alive=True,
            draw_mod_100=0,target_is_player=False,target_petflag=1,
            attacker_pig_marker=-1,current_turn=4,
        )
        self.assertTrue(decision.transformed)
        self.assertIsNotNone(active)
        self.assertEqual(active.state.fox_round,4)

    def test_player_and_petflag_rejection_still_consume_reached_draw(self):
        state=FoxState(
            base_image=101743,base_base_image=101743,
            attack_power=40,defence_power=26,quick=30,
            fix_str=40,fix_tough=26,fix_dex=30,
            fox_round=-1,ride_pet=-1,petfall=0,
        )
        submission=self.resolve()
        for kwargs in (
            dict(target_is_player=True,target_petflag=1),
            dict(target_is_player=False,target_petflag=0),
        ):
            decision,active=submission.postattack(
                state,attack_result="HIT",target_alive=True,draw_mod_100=0,
                attacker_pig_marker=-1,current_turn=1,**kwargs
            )
            self.assertTrue(decision.draw_consumed)
            self.assertFalse(decision.transformed)
            self.assertIsNone(active)


if __name__=="__main__":
    unittest.main()
