from dataclasses import replace
import hashlib
from types import SimpleNamespace
import unittest
from unittest import mock

import tools.stoneage_enemy_ai_combined_bridge as bridge
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)


OPTIONS={
    627:b"marker|6|21|139|159|169|179|189",
    629:b"marker|5|139|159|169|179|189",
    630:b"marker|1|306",
    632:b"marker|1|240",
    637:b"marker|1|61",
    646:b"marker|6|20|21|22|23|24|25",
    648:b"marker|6|71|81|91|101|121|61",
}
META={
    627:(1,3,2,2000),
    629:(1,3,2,2000),
    630:(1,3,2,2000),
    632:(1,1,2,5000),
    637:(1,2,2,20000),
    646:(1,2,2,20000),
    648:(1,2,2,20000),
}
FUNCTIONS={
    20:"MAGIC_Recovery",21:"MAGIC_Recovery",22:"MAGIC_Recovery",
    23:"MAGIC_Recovery",24:"MAGIC_Recovery",25:"MAGIC_Recovery",
    61:"MAGIC_StatusRecovery",71:"MAGIC_StatusRecovery",
    81:"MAGIC_StatusRecovery",91:"MAGIC_StatusRecovery",
    101:"MAGIC_StatusRecovery",121:"MAGIC_StatusRecovery",
    139:"MAGIC_StatusChange",159:"MAGIC_StatusChange",
    169:"MAGIC_StatusChange",179:"MAGIC_StatusChange",
    189:"MAGIC_StatusChange",240:"MAGIC_AttReverse",
    306:"MAGIC_AttMagic",
}


def runtime():
    skills={}
    for skill_id,raw in OPTIONS.items():
        field,target,cost,illegal=META[skill_id]
        skills[skill_id]=Recovered25PetSkillEntry(
            skill_id,field,target,cost,illegal,
            "PETSKILL_Combined",raw,
        )
    return Recovered25PetSkillRuntime(
        skills=skills,source_file="petskill.txt"
    )


def expected_rows(rt):
    rows=[]
    for skill_id in sorted(OPTIONS):
        entry=rt.skills[skill_id]
        marker,declared,effective,magic_ids,well=bridge._option_structure(
            entry.option_bytes
        )
        rows.append((
            skill_id,entry.field,entry.target,entry.cost,entry.illegal,
            0,len(entry.option_bytes),
            hashlib.sha256(entry.option_bytes).hexdigest(),
            False,marker,declared,effective,magic_ids,well,
        ))
    return tuple(rows)


def magic_rows():
    rows=[]
    for magic_id in sorted(FUNCTIONS):
        function=FUNCTIONS[magic_id]
        rows.append((
            magic_id,function,
            hashlib.sha256(function.encode("ascii")).hexdigest(),
            1,8,0,None,0,
            hashlib.sha256(b"").hexdigest(),False,
        ))
    return tuple(rows)


def spawned(skill_id):
    return SimpleNamespace(
        participant=SimpleNamespace(participant_id="enemy"),
        template=SimpleNamespace(
            skill_slot_ids=(skill_id,0,0,0,0,0,0)
        ),
    )


class CombinedBridgeTests(unittest.TestCase):
    def resolve(self,skill_id,draw=0,target=2,rt=None):
        rt=runtime() if rt is None else rt
        with (
            mock.patch.object(
                bridge,"EXPECTED_EXACT_ROWS",expected_rows(rt)
            ),
            mock.patch.object(
                bridge,"EXPECTED_EXACT_MAGIC_ROWS",magic_rows()
            ),
        ):
            return bridge.resolve_enemy_ai_combined_submission(
                spawned(skill_id),
                skill_slot=0,
                target_slot=target,
                petskill_runtime=rt,
                draw_index=draw,
            )

    def test_id627_owns_one_explicit_selection_draw(self):
        first=self.resolve(627,draw=0)
        last=self.resolve(627,draw=5)
        self.assertEqual(first.selection.selected_magic_id,21)
        self.assertEqual(first.magic.function_name,"MAGIC_Recovery")
        self.assertEqual(last.selection.selected_magic_id,189)
        self.assertEqual(last.magic.function_name,"MAGIC_StatusChange")
        self.assertEqual(first.selection.rng_draws_consumed,1)
        self.assertEqual(first.magic.direct_item_index,0)
        self.assertEqual(first.semantic_command_name,"BATTLE_COM_JYUJYUTU")

    def test_single_choice_positive_rows_have_exact_crosslinks(self):
        attreverse=self.resolve(632)
        statusrecovery=self.resolve(637)
        self.assertEqual(attreverse.selection.selected_magic_id,240)
        self.assertEqual(attreverse.magic.function_name,"MAGIC_AttReverse")
        self.assertEqual(statusrecovery.selection.selected_magic_id,61)
        self.assertEqual(
            statusrecovery.magic.function_name,"MAGIC_StatusRecovery"
        )

    def test_zero_reference_family_rows_remain_data_only(self):
        for skill_id in (629,630,646,648):
            with self.subTest(skill_id=skill_id):
                rt=runtime()
                with (
                    mock.patch.object(
                        bridge,"EXPECTED_EXACT_ROWS",expected_rows(rt)
                    ),
                    mock.patch.object(
                        bridge,"EXPECTED_EXACT_MAGIC_ROWS",magic_rows()
                    ),
                ):
                    with self.assertRaisesRegex(
                        ValueError,"positively referenced"
                    ):
                        bridge.resolve_enemy_ai_combined_submission(
                            spawned(skill_id),skill_slot=0,target_slot=0,
                            petskill_runtime=rt,draw_index=0,
                        )

    def test_full_family_metadata_drift_is_fail_closed(self):
        rt=runtime()
        skills=dict(rt.skills)
        skills[629]=replace(skills[629],field=2)
        drift=Recovered25PetSkillRuntime(
            skills=skills,source_file="petskill.txt"
        )
        # Expectations come from the original good corpus, not the drifted one.
        with (
            mock.patch.object(
                bridge,"EXPECTED_EXACT_ROWS",expected_rows(rt)
            ),
            mock.patch.object(
                bridge,"EXPECTED_EXACT_MAGIC_ROWS",magic_rows()
            ),
        ):
            with self.assertRaisesRegex(ValueError,"exact row drift"):
                bridge.resolve_enemy_ai_combined_submission(
                    spawned(627),skill_slot=0,target_slot=0,
                    petskill_runtime=drift,draw_index=0,
                )

    def test_callback_population_drift_is_fail_closed(self):
        rt=runtime()
        skills=dict(rt.skills)
        skills[649]=replace(skills[648],skill_id=649)
        drift=Recovered25PetSkillRuntime(
            skills=skills,source_file="petskill.txt"
        )
        with (
            mock.patch.object(
                bridge,"EXPECTED_EXACT_ROWS",expected_rows(rt)
            ),
            mock.patch.object(
                bridge,"EXPECTED_EXACT_MAGIC_ROWS",magic_rows()
            ),
        ):
            with self.assertRaisesRegex(ValueError,"population"):
                bridge.resolve_enemy_ai_combined_submission(
                    spawned(627),skill_slot=0,target_slot=0,
                    petskill_runtime=drift,draw_index=0,
                )

    def test_target_and_reduced_draw_domains_are_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"target"):
            self.resolve(627,target=10)
        with self.assertRaisesRegex(ValueError,"draw_index"):
            self.resolve(627,draw=6)


if __name__=="__main__":
    unittest.main()
