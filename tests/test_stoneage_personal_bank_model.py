import unittest

from tools.stoneage_personal_bank_model import (
    BISMARCK_MAX_BANK_GOLD,
    GAVIN_IRISELIA_MAX_BANK_GOLD,
    PROFILE_BISMARCK,
    PROFILE_GAVIN_IRISELIA,
    PersonalBankState,
    apply_personal_bank_transfer,
    can_access_personal_bank,
    character_storage_key,
    command_scope,
    mutation_triggers_immediate_char_save,
    persistence_mode,
)


class PersonalBankModelTests(unittest.TestCase):
    def test_current_family_member_can_open_empty_personal_account(self):
        self.assertTrue(can_access_personal_bank(PersonalBankState(100, 0, 1)))

    def test_nonmember_with_zero_balance_is_denied(self):
        self.assertFalse(can_access_personal_bank(PersonalBankState(100, 0, -1)))

    def test_former_member_with_residual_balance_can_open_to_withdraw(self):
        self.assertTrue(can_access_personal_bank(PersonalBankState(100, 1, -1)))

    def test_positive_amount_deposits_cash_into_personal_bank(self):
        result = apply_personal_bank_transfer(
            PersonalBankState(1000, 500, 2),
            200,
            max_cash=1_000_000,
            max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
        )
        self.assertTrue(result.accepted)
        self.assertEqual(result.state.cash, 800)
        self.assertEqual(result.state.bank_gold, 700)

    def test_negative_amount_withdraws_bank_into_cash(self):
        result = apply_personal_bank_transfer(
            PersonalBankState(1000, 500, -1),
            -200,
            max_cash=1_000_000,
            max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
        )
        self.assertTrue(result.accepted)
        self.assertEqual(result.state.cash, 1200)
        self.assertEqual(result.state.bank_gold, 300)

    def test_former_member_cannot_add_new_deposit(self):
        state = PersonalBankState(1000, 500, -1)
        result = apply_personal_bank_transfer(
            state,
            100,
            max_cash=1_000_000,
            max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "family_required_for_deposit")
        self.assertEqual(result.state, state)

    def test_deposit_cannot_exceed_carried_cash_or_bank_cap(self):
        state = PersonalBankState(100, GAVIN_IRISELIA_MAX_BANK_GOLD - 50, 1)
        self.assertFalse(
            apply_personal_bank_transfer(
                state,
                101,
                max_cash=1_000_000,
                max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
            ).accepted
        )
        self.assertFalse(
            apply_personal_bank_transfer(
                state,
                51,
                max_cash=1_000_000,
                max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
            ).accepted
        )

    def test_withdrawal_cannot_overdraw_bank_or_overflow_carried_cash(self):
        state = PersonalBankState(999_900, 500, -1)
        self.assertFalse(
            apply_personal_bank_transfer(
                state,
                -501,
                max_cash=1_000_000,
                max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
            ).accepted
        )
        self.assertFalse(
            apply_personal_bank_transfer(
                state,
                -101,
                max_cash=1_000_000,
                max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
            ).accepted
        )

    def test_zero_transfer_is_source_valid_when_account_is_accessible(self):
        state = PersonalBankState(500, 0, 1)
        result = apply_personal_bank_transfer(
            state,
            0,
            max_cash=1_000_000,
            max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
        )
        self.assertTrue(result.accepted)
        self.assertEqual(result.state, state)

    def test_bismarck_and_older_two_lineages_have_different_fixed_bank_caps(self):
        self.assertEqual(GAVIN_IRISELIA_MAX_BANK_GOLD, 10_000_000)
        self.assertEqual(BISMARCK_MAX_BANK_GOLD, 100_000_000)

        near_old_cap = PersonalBankState(1, 10_000_000, 1)
        old = apply_personal_bank_transfer(
            near_old_cap,
            1,
            max_cash=1_000_000,
            max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
            profile=PROFILE_GAVIN_IRISELIA,
        )
        later = apply_personal_bank_transfer(
            near_old_cap,
            1,
            max_cash=100_000_000,
            max_bank_gold=BISMARCK_MAX_BANK_GOLD,
            profile=PROFILE_BISMARCK,
        )
        self.assertFalse(old.accepted)
        self.assertTrue(later.accepted)

    def test_underflow_outcome_is_same_but_later_branch_reports_explicit_path(self):
        state = PersonalBankState(0, 5, -1)
        old = apply_personal_bank_transfer(
            state,
            -6,
            max_cash=1_000_000,
            max_bank_gold=GAVIN_IRISELIA_MAX_BANK_GOLD,
            profile=PROFILE_GAVIN_IRISELIA,
        )
        later = apply_personal_bank_transfer(
            state,
            -6,
            max_cash=100_000_000,
            max_bank_gold=BISMARCK_MAX_BANK_GOLD,
            profile=PROFILE_BISMARCK,
        )
        self.assertFalse(old.accepted)
        self.assertFalse(later.accepted)
        self.assertEqual(old.reason, "bank_bounds")
        self.assertEqual(later.reason, "bank_underflow_explicit")

    def test_personal_and_shared_family_bank_are_distinct_commands(self):
        self.assertEqual(command_scope("G"), "personal_bank")
        self.assertEqual(command_scope("T"), "family_shared_bank")
        self.assertEqual(command_scope("I"), "reserved_noop")

    def test_bankgold_is_part_of_standard_character_serialization(self):
        self.assertEqual(character_storage_key(), "bankgld")
        self.assertEqual(persistence_mode(), "deferred_standard_character_save")
        self.assertFalse(mutation_triggers_immediate_char_save())


if __name__ == "__main__":
    unittest.main()
