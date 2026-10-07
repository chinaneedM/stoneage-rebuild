import unittest

from tools.stoneage_becomefox_reference_model import FOX_IMAGE, FoxState
from tools.stoneage_becomefox_runtime_state import (
    BecomeFoxRuntimeOverlay,
    FoxParticipantRuntime,
    PROFILE_BISMARCK,PROFILE_GAVIN,PROFILE_IRIS,
    arrange_guard_active,petin_accessor_profile,
)


def fox(profile=PROFILE_GAVIN,roundno=3,**changes):
    values=dict(
        base_image=FOX_IMAGE,base_base_image=101743,
        attack_power=40,defence_power=26,quick=30,
        fix_str=41,fix_tough=27,fix_dex=33,
        fox_round=roundno,ride_pet=-1,petfall=0,
    )
    values.update(changes)
    return FoxParticipantRuntime(profile,FoxState(**values))


class BecomeFoxRuntimeStateTests(unittest.TestCase):
    def test_ride_bearing_fox_state_cannot_enter_bounded_runtime(self):
        for profile in (PROFILE_GAVIN, PROFILE_IRIS, PROFILE_BISMARCK):
            with self.subTest(profile=profile):
                with self.assertRaisesRegex(ValueError, "ride"):
                    fox(profile, ride_pet=0)

    def test_source_profile_controls_arrange_and_petin_accessor_only(self):
        self.assertTrue(arrange_guard_active(PROFILE_GAVIN))
        self.assertTrue(arrange_guard_active(PROFILE_IRIS))
        self.assertFalse(arrange_guard_active(PROFILE_BISMARCK))
        self.assertEqual(petin_accessor_profile(PROFILE_GAVIN),"ordinary_int")
        self.assertEqual(petin_accessor_profile(PROFILE_IRIS),"ordinary_int")
        self.assertEqual(petin_accessor_profile(PROFILE_BISMARCK),"work_int")

    def test_overlay_carries_active_state_and_action_rewrite_is_not_transform_time(self):
        overlay=BecomeFoxRuntimeOverlay.empty().with_transformed("pet",fox())
        before=overlay.runtime_by_participant_id["pet"].state
        self.assertEqual((before.attack_power,before.defence_power,before.quick),(40,26,30))
        overlay,prepared=overlay.prepare_actor_action("pet")
        self.assertIsNotNone(prepared)
        self.assertEqual(
            (prepared.state.attack_power,prepared.state.defence_power,prepared.state.quick),
            (32,21,26),
        )

    def test_recovery_is_after_action_and_strictly_greater_than_two_turns(self):
        overlay=BecomeFoxRuntimeOverlay({"pet":fox(roundno=4)})
        overlay,_=overlay.prepare_actor_action("pet")
        hold,tick=overlay.recover_after_actor_action("pet",current_turn=6,battle_slot=7)
        self.assertFalse(tick.recovered)
        self.assertIn("pet",hold.runtime_by_participant_id)
        done,tick=hold.recover_after_actor_action("pet",current_turn=7,battle_slot=7)
        self.assertTrue(tick.recovered)
        self.assertEqual(tick.notify_owner_slot,2)
        self.assertNotIn("pet",done.runtime_by_participant_id)

    def test_successful_retransform_replaces_marker_without_double_overlay(self):
        overlay=BecomeFoxRuntimeOverlay({"pet":fox(roundno=2)})
        refreshed=fox(roundno=5,attack_power=32,defence_power=21,quick=26)
        overlay=overlay.with_transformed("pet",refreshed)
        self.assertEqual(len(overlay.runtime_by_participant_id),1)
        self.assertEqual(overlay.runtime_by_participant_id["pet"].state.fox_round,5)

    def test_retain_and_teardown_are_fail_closed(self):
        overlay=BecomeFoxRuntimeOverlay({"a":fox(),"b":fox(PROFILE_BISMARCK)})
        self.assertEqual(set(overlay.retain_participants({"b"}).runtime_by_participant_id),{"b"})
        self.assertFalse(overlay.teardown().runtime_by_participant_id)

    def test_inactive_state_cannot_enter_persistent_overlay(self):
        inactive=FoxState(
            base_image=101743,base_base_image=101743,
            attack_power=40,defence_power=26,quick=30,
            fix_str=40,fix_tough=26,fix_dex=30,
            fox_round=-1,ride_pet=-1,petfall=0,
        )
        with self.assertRaises(ValueError):
            FoxParticipantRuntime(PROFILE_GAVIN,inactive)


if __name__=="__main__":
    unittest.main()
