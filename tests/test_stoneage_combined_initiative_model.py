import unittest

from tools.stoneage_combined_initiative_model import (
    CombinedInitiativeDomain,
    PROFILE_BISMARCK_FIXED15,
    PROFILE_GAVIN_IRIS_30PCT,
    resolve_combined_initiative,
)


class CombinedInitiativeTests(unittest.TestCase):
    def test_gavin_iris_uses_explicit_thirty_percent_range(self):
        result=resolve_combined_initiative(
            profile=PROFILE_GAVIN_IRIS_30PCT,
            work_quick=80,
            random_subtract=30,
        )
        self.assertEqual(result.base_work,100)
        self.assertEqual(result.max_random_subtract,30)
        self.assertEqual(result.action_value,70)
        self.assertEqual(result.rng_draws_consumed,1)

    def test_bismarck_uses_fixed_zero_to_fifteen_range(self):
        result=resolve_combined_initiative(
            profile=PROFILE_BISMARCK_FIXED15,
            work_quick=80,
            random_subtract=15,
        )
        self.assertEqual(result.base_work,100)
        self.assertEqual(result.max_random_subtract,15)
        self.assertEqual(result.action_value,85)

    def test_profile_must_be_explicit_and_known(self):
        for profile in ("", "original", "gavin"):
            with self.subTest(profile=profile):
                with self.assertRaisesRegex(
                    CombinedInitiativeDomain,"profile must be explicit"
                ):
                    resolve_combined_initiative(
                        profile=profile,work_quick=80,random_subtract=0
                    )

    def test_profile_specific_range_is_fail_closed(self):
        for profile,draw in (
            (PROFILE_GAVIN_IRIS_30PCT,31),
            (PROFILE_BISMARCK_FIXED15,16),
            (PROFILE_BISMARCK_FIXED15,-1),
        ):
            with self.subTest(profile=profile,draw=draw):
                with self.assertRaisesRegex(
                    CombinedInitiativeDomain,"outside profile range"
                ):
                    resolve_combined_initiative(
                        profile=profile,work_quick=80,random_subtract=draw
                    )

    def test_no_silent_older_common_core_clamp(self):
        result=resolve_combined_initiative(
            profile=PROFILE_BISMARCK_FIXED15,
            work_quick=-19,
            random_subtract=15,
        )
        self.assertEqual(result.base_work,1)
        self.assertEqual(result.action_value,-14)

    def test_scaled_negative_upper_bound_is_not_admitted(self):
        with self.assertRaisesRegex(
            CombinedInitiativeDomain,"negative scaled RAND upper bound"
        ):
            resolve_combined_initiative(
                profile=PROFILE_GAVIN_IRIS_30PCT,
                work_quick=-21,
                random_subtract=0,
            )

    def test_int32_witnesses_are_required(self):
        for kwargs in (
            {"work_quick":1.0,"random_subtract":0},
            {"work_quick":2**31-1,"random_subtract":0},
            {"work_quick":80,"random_subtract":1.0},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(CombinedInitiativeDomain):
                    resolve_combined_initiative(
                        profile=PROFILE_BISMARCK_FIXED15,**kwargs
                    )


if __name__=="__main__":
    unittest.main()
