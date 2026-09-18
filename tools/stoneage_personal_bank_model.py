#!/usr/bin/env python3
"""Reference model for StoneAge personal-bank transfer and persistence boundaries."""

from dataclasses import dataclass

PROFILE_GAVIN_IRISELIA = "gavin_iriselia"
PROFILE_BISMARCK = "bismarck"

GAVIN_IRISELIA_MAX_BANK_GOLD = 10_000_000
BISMARCK_MAX_BANK_GOLD = 100_000_000


@dataclass(frozen=True)
class PersonalBankState:
    cash: int
    bank_gold: int
    family_index: int = -1


@dataclass(frozen=True)
class BankTransferResult:
    accepted: bool
    reason: str
    state: PersonalBankState


def can_access_personal_bank(state):
    """Fixed Bankman/FAMILY_Bank gate: member, or residual personal balance."""
    return int(state.family_index) > 0 or int(state.bank_gold) >= 1


def apply_personal_bank_transfer(
    state,
    amount,
    *,
    max_cash,
    max_bank_gold,
    profile=PROFILE_GAVIN_IRISELIA,
):
    """Apply the FAMILY_Bank 'G' branch.

    Positive amount deposits carried Stone into CHAR_BANKGOLD.
    Negative amount withdraws from CHAR_BANKGOLD into carried Stone.
    """
    if profile not in (PROFILE_GAVIN_IRISELIA, PROFILE_BISMARCK):
        raise ValueError("unknown profile")

    if not can_access_personal_bank(state):
        return BankTransferResult(False, "qualification", state)

    amount = int(amount)
    cash = int(state.cash)
    bank = int(state.bank_gold)
    max_cash = int(max_cash)
    max_bank_gold = int(max_bank_gold)

    new_cash = cash - amount
    new_bank = bank + amount

    if new_cash < 0:
        return BankTransferResult(False, "cash_underflow", state)
    if new_cash > max_cash:
        return BankTransferResult(False, "cash_overflow", state)

    if new_bank < 0:
        reason = (
            "bank_underflow_explicit"
            if profile == PROFILE_BISMARCK
            else "bank_bounds"
        )
        return BankTransferResult(False, reason, state)
    if new_bank > max_bank_gold:
        return BankTransferResult(False, "bank_overflow", state)

    if amount > 0 and int(state.family_index) < 1:
        return BankTransferResult(False, "family_required_for_deposit", state)

    return BankTransferResult(
        True,
        "ok",
        PersonalBankState(
            cash=new_cash,
            bank_gold=new_bank,
            family_index=int(state.family_index),
        ),
    )


def command_scope(token):
    """FAMILY_Bank subcommands keep personal and shared-family money distinct."""
    token = str(token)
    if token == "G":
        return "personal_bank"
    if token == "T":
        return "family_shared_bank"
    if token == "I":
        return "reserved_noop"
    return "unknown"


def character_storage_key():
    """CHAR_BANKGOLD's integer-field serialization key."""
    return "bankgld"


def persistence_mode():
    """FAMILY_Bank mutates memory; standard character save persists the field."""
    return "deferred_standard_character_save"


def mutation_triggers_immediate_char_save():
    """No CHAR_charSave* call exists in the fixed common personal-bank branch."""
    return False
