"""Profit-boundary behavior and fail-closed modern clear projection."""
from dataclasses import FrozenInstanceError, replace
import unittest

from tools.stoneage_default_pet_exit_model import DefaultPetExitAuthority
from tools.stoneage_profit_exit_scan_model import (
    ProfitExitCharacter, ProfitExitSnapshot, resolve_profit_exit_scan,
    project_profit_exit_status_clear,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime, BaseBattleStatusState,
)
from tools.stoneage_nocast_runtime_state import (
    NocastParticipantRuntime, NocastRoundOverlay, PreparedWeakenPowers,
)


def fixture(*, side=0, owner_slot=0, selection="paired", ultimate=True,
            owner_hp=0, pet_hp=0, no_risk=False, statuses=(9,) * 10):
    # Deliberately reverse dictionary insertion order: entry order is authority.
    chars = {
        "enemy": ProfitExitCharacter("enemy", "enemy", 10, 20, (1-side)*10,
                                    status_counters=statuses, command=99),
        "carried": ProfitExitCharacter("carried", "pet", 10, 0, None,
                                      battle_mode="none", battle_index=77,
                                      status_counters=statuses, command=99),
        "paired": ProfitExitCharacter("paired", "pet", 10, pet_hp, side*10+owner_slot+5,
                                     ultimate=True, status_counters=statuses, command=99),
        "owner": ProfitExitCharacter("owner", "player", 11, owner_hp, side*10+owner_slot,
                                    ultimate=ultimate, status_counters=statuses, command=99),
    }
    authority = DefaultPetExitAuthority("owner", selection, ("paired", "carried"),
                                       {"paired": chars["paired"].occupied_slot})
    return ProfitExitSnapshot(chars, authority, side, no_risk)


def scan(snapshot):
    return resolve_profit_exit_scan(snapshot, recipient_id="enemy")


class ProfitExitScanTests(unittest.TestCase):
    def test_owner_first_suppresses_paired_death_on_both_sides_and_edge_slots(self):
        for side in (0, 1):
            for slot in (0, 4):
                with self.subTest(side=side, slot=slot):
                    result = scan(fixture(side=side, owner_slot=slot))
                    self.assertEqual(result.processed_death_ids, ("owner",))
                    after = result.after.characters
                    self.assertEqual(after["paired"].death_count, 0)
                    self.assertEqual(after["owner"].dead_pet_count, 0)
                    self.assertEqual(after["paired"].variable_ai_delta, -1000)
                    self.assertEqual(after["paired"].hp, 1)
                    self.assertFalse(after["paired"].isdie)
                    self.assertIsNone(after["paired"].occupied_slot)

    def test_pet_first_on_separate_boundary_clears_later_penalty_selection(self):
        first = scan(fixture(owner_hp=20))
        self.assertEqual(first.processed_death_ids, ("paired",))
        self.assertIsNone(first.after.authority.selected_pet_id)
        chars = dict(first.after.characters)
        chars["owner"] = replace(chars["owner"], hp=0)
        second = scan(replace(first.after, characters=chars))
        self.assertEqual(second.processed_death_ids, ("owner",))
        self.assertEqual(second.after.characters["paired"].variable_ai_delta, -1000)
        self.assertEqual(second.after.characters["owner"].dead_pet_count, 1)
        self.assertEqual(second.after.characters["owner"].charm_delta, -4)

    def test_no_selection_still_removes_paired_entry(self):
        result = scan(fixture(selection=None))
        self.assertIsNone(result.after.characters["paired"].occupied_slot)
        self.assertEqual(result.after.characters["paired"].variable_ai_delta, 0)
        self.assertEqual(result.status_cleared_ids, ("owner", "paired", "carried"))

    def test_carried_selected_exit_fails_without_substituting_paired(self):
        result = scan(fixture(selection="carried"))
        exits = [e.participant_id for e in result.effects if e.kind == "exit_request"]
        self.assertEqual(exits, ["carried", "owner"])
        self.assertEqual(result.after.characters["carried"].battle_index, 77)
        self.assertEqual(result.after.characters["carried"].variable_ai_delta, -1000)
        self.assertIsNone(result.after.characters["paired"].occupied_slot)

    def test_selected_and_paired_occupied_identities_remain_distinct(self):
        before = fixture(selection="carried")
        chars = dict(before.characters)
        chars["carried"] = replace(chars["carried"], occupied_slot=6, hp=20,
                                    battle_index=0, battle_mode="battle")
        before = replace(before, characters=chars, authority=replace(before.authority,
                            occupied_pet_slots={"paired": 5, "carried": 6}))
        result = scan(before)
        self.assertEqual(result.processed_death_ids, ("owner",))
        self.assertIsNone(result.after.characters["paired"].occupied_slot)
        self.assertIsNone(result.after.characters["carried"].occupied_slot)
        self.assertEqual(result.after.characters["carried"].battle_index, -1)

    def test_alive_ultimate_does_not_create_death(self):
        result = scan(fixture(owner_hp=20, pet_hp=20))
        self.assertEqual(result.processed_death_ids, ())
        self.assertEqual(result.effects, ())

    def test_prior_isdie_prevents_second_death(self):
        before = fixture(owner_hp=0, pet_hp=20)
        chars = dict(before.characters)
        chars["owner"] = replace(chars["owner"], isdie=True, death_count=8)
        result = scan(replace(before, characters=chars))
        self.assertEqual(result.processed_death_ids, ())
        self.assertEqual(result.after.characters["owner"].death_count, 8)

    def test_normal_owner_then_pet_ultimate_are_both_processed(self):
        result = scan(fixture(ultimate=False))
        self.assertEqual(result.processed_death_ids, ("owner", "paired"))
        self.assertEqual(result.after.characters["paired"].variable_ai_delta, -1100)
        self.assertEqual(result.after.characters["owner"].charm_delta, -2)
        self.assertEqual(result.after.characters["owner"].command, 0)
        self.assertEqual(result.status_cleared_ids, ())

    def test_no_risk_ultimate_pet_still_counts(self):
        result = scan(fixture(owner_hp=20, no_risk=True))
        self.assertEqual(result.after.characters["owner"].dead_pet_count, 1)
        self.assertEqual(result.after.characters["paired"].variable_ai_delta, 0)

    def test_level10_penalty_divisor(self):
        before = fixture()
        chars = dict(before.characters)
        chars["owner"] = replace(chars["owner"], level=10)
        result = scan(replace(before, characters=chars))
        self.assertEqual(result.after.characters["owner"].charm_delta, -2)
        self.assertEqual(result.after.characters["paired"].variable_ai_delta, -500)

    def test_repeated_scan_keeps_pending_profit_and_has_no_effects(self):
        first = scan(fixture())
        second = scan(first.after)
        self.assertEqual(second.after, first.after)
        self.assertEqual(second.effects, ())
        self.assertEqual(second.processed_death_ids, ())

    def test_single_player_enemy_profit_preserves_prior_awards(self):
        before = fixture(owner_hp=20, pet_hp=20)
        chars = dict(before.characters)
        chars["owner"] = replace(chars["owner"], pending_exp=37, kill_count=2)
        chars["enemy"] = replace(chars["enemy"], hp=0, reward_exp=100, ultimate=True)
        first = resolve_profit_exit_scan(replace(before, characters=chars), recipient_id="owner")
        self.assertEqual(first.after.characters["owner"].pending_exp, 137)
        self.assertEqual(first.after.characters["owner"].kill_count, 3)
        self.assertFalse(first.after.characters["enemy"].valid)
        self.assertTrue(first.after.characters["enemy"].enemy_ultimate)
        second = resolve_profit_exit_scan(first.after, recipient_id="owner")
        self.assertEqual(second.after, first.after)

    def test_warp_is_explicit_request_before_owner_exit(self):
        before = replace(fixture(), elder_destination=(8000, 1, 2))
        result = scan(before)
        self.assertEqual(result.warp_requests, (("owner", (8000, 1, 2)),))
        kinds = [(e.kind, e.participant_id) for e in result.effects]
        self.assertLess(kinds.index(("warp_request", "owner")), kinds.index(("exit_request", "owner")))

    def test_native_exp_intermediate_overflow_is_rejected_before_division(self):
        before = fixture(owner_hp=20, pet_hp=20)
        chars = dict(before.characters)
        chars["owner"] = replace(chars["owner"], level=16)
        chars["enemy"] = replace(chars["enemy"], hp=0, reward_exp=200_000_000)
        with self.assertRaisesRegex(ValueError, "intermediate product"):
            resolve_profit_exit_scan(replace(before, characters=chars), recipient_id="owner")
        self.assertEqual(before.characters["owner"].pending_exp, 0)

    def test_inputs_and_results_cannot_be_mutated(self):
        before = fixture()
        after = scan(before).after
        self.assertEqual(before.characters["owner"].hp, 0)
        self.assertEqual(before.authority.occupied_pet_slots, {"paired": 5})
        with self.assertRaises(TypeError):
            after.characters["owner"] = before.characters["owner"]
        with self.assertRaises(FrozenInstanceError):
            after.characters["owner"].hp = 0

    def test_bad_occupancy_and_missing_roster_fail_closed(self):
        before = fixture()
        with self.assertRaisesRegex(ValueError, "occupancy drift"):
            replace(before, authority=replace(before.authority, occupied_pet_slots={}))
        chars = dict(before.characters)
        chars.pop("carried")
        with self.assertRaisesRegex(ValueError, "complete non-mail"):
            replace(before, characters=chars)

    def test_pet_or_missing_recipient_fail_closed(self):
        for pid in ("paired", "carried", "unknown"):
            with self.subTest(pid=pid), self.assertRaises(ValueError):
                resolve_profit_exit_scan(fixture(), recipient_id=pid)

    def test_inconsistent_side_and_duplicate_slot_fail_closed(self):
        before = fixture()
        with self.assertRaises(ValueError):
            replace(before, player_side=1)
        chars = dict(before.characters)
        chars["carried"] = replace(chars["carried"], occupied_slot=5)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            replace(before, characters=chars)


class ProfitExitStatusProjectionTests(unittest.TestCase):
    def fixture(self, *, deep_poison=0):
        counters = (9,) * 7 + (deep_poison, 9, 9)
        result = scan(fixture(statuses=counters))
        base = {pid: BaseBattleStatusRuntime(BaseBattleStatusState(9,9,9,9,9,9),
                                            work_quick=17, damage_count=3)
                for pid in result.before.characters}
        late = NocastRoundOverlay({pid: NocastParticipantRuntime(1,2,3,4,
            counter=9, barrier_counter=9, weaken_counter=9, nc_flag=1,
            weaken_active_at_visit=True, barrier_active_at_visit=True,
            prepared_weaken_powers=PreparedWeakenPowers(8,9,10)) for pid in base})
        return result, base, late

    def test_clear_base_overlay_visit_flags_and_cached_powers_including_carried(self):
        result, base, overlay = self.fixture()
        projected = project_profit_exit_status_clear(result, base_runtime=base, overlay=overlay)
        self.assertEqual(projected.recalculation_required_ids, ("owner", "paired", "carried"))
        for pid in projected.recalculation_required_ids:
            p = projected.overlay.runtime_by_participant_id[pid]
            self.assertEqual((p.counter, p.barrier_counter, p.weaken_counter), (0,0,0))
            self.assertFalse(p.weaken_active_at_visit)
            self.assertFalse(p.barrier_active_at_visit)
            self.assertIsNone(p.prepared_weaken_powers)
            self.assertEqual(p.nc_flag, 1)  # No fabricated feature-on NC packet.
            self.assertEqual(projected.base_runtime[pid].status, BaseBattleStatusState())
            self.assertEqual(projected.base_runtime[pid].work_quick, 17)
            self.assertEqual(projected.base_runtime[pid].damage_count, 3)
        self.assertIs(projected.base_runtime["enemy"], base["enemy"])
        self.assertIs(projected.overlay.runtime_by_participant_id["enemy"], overlay.runtime_by_participant_id["enemy"])
        self.assertEqual(overlay.runtime_by_participant_id["owner"].counter, 9)
        self.assertEqual(base["owner"].status.poison, 9)

    def test_active_deep_poison_is_rejected(self):
        result, base, overlay = self.fixture(deep_poison=9)
        with self.assertRaisesRegex(ValueError, "deep poison"):
            project_profit_exit_status_clear(result, base_runtime=base, overlay=overlay)

    def test_unmodeled_active_status_is_rejected(self):
        result, base, overlay = self.fixture()
        late = dict(overlay.runtime_by_participant_id)
        late["owner"] = replace(late["owner"], unmodeled_status_active=True)
        with self.assertRaisesRegex(ValueError, "unmodeled"):
            project_profit_exit_status_clear(result, base_runtime=base, overlay=NocastRoundOverlay(late))

    def test_missing_late_overlay_is_rejected(self):
        result, base, _ = self.fixture()
        with self.assertRaisesRegex(ValueError, "explicit overlay"):
            project_profit_exit_status_clear(result, base_runtime=base, overlay=None)

    def test_snapshot_overlay_mismatch_is_rejected(self):
        result, base, overlay = self.fixture()
        late = dict(overlay.runtime_by_participant_id)
        late["paired"] = replace(late["paired"], counter=0)
        with self.assertRaisesRegex(ValueError, "snapshot"):
            project_profit_exit_status_clear(result, base_runtime=base, overlay=NocastRoundOverlay(late))

    def test_base_snapshot_mismatch_is_rejected(self):
        result, base, overlay = self.fixture()
        base["carried"] = replace(base["carried"], status=BaseBattleStatusState())
        with self.assertRaisesRegex(ValueError, "snapshot"):
            project_profit_exit_status_clear(result, base_runtime=base, overlay=overlay)

    def test_no_overlay_allowed_when_all_late_counters_absent(self):
        result = scan(fixture(statuses=(0,) * 10))
        base = {pid: BaseBattleStatusRuntime() for pid in result.before.characters}
        projected = project_profit_exit_status_clear(result, base_runtime=base, overlay=None)
        self.assertIsNone(projected.overlay)
        self.assertEqual(projected.recalculation_required_ids, result.status_cleared_ids)


if __name__ == "__main__":
    unittest.main()
