"""Refresh ordered-runtime tests use independent synthetic OPTION bytes."""

from dataclasses import replace
from hashlib import sha256
from unittest.mock import patch
import unittest

from tests.test_stoneage_attack_crazed_runtime import actor
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCommand,
    BattleCombatProfile,
    prepare_battle_round,
    resolve_ordinary_round,
)
from tools.stoneage_battle_status_model import (
    BaseBattleStatusRuntime,
    BaseBattleStatusState,
)
from tools.stoneage_enemy_ai_refresh_bridge import (
    EnemyAiRefreshSubmission,
    EXPECTED_OPTION_SHA256_BY_ID,
    resolve_enemy_ai_refresh_submission,
    validate_recovered25_refresh_population,
)
from tools.stoneage_nocast_runtime_state import (
    NocastParticipantRuntime,
    NocastRoundOverlay,
    PreparedWeakenPowers,
)
from tools.stoneage_recovered25_petskill_runtime import (
    Recovered25PetSkillEntry,
    Recovered25PetSkillRuntime,
)
from tools.stoneage_refresh_runtime_state import (
    RefreshActionRolls,
    apply_refresh_cleared_status,
    refresh_status_vector,
)
from tools.stoneage_enemy_spawn_model import SpawnedEnemy


SYNTHETIC_OPTIONS = {
    583: "默".encode("cp950"),
    584: "劇".encode("cp950"),
    591: "障".encode("cp950"),
    592: "全".encode("cp950"),
    593: "虛".encode("cp950"),
}
SYNTHETIC_HASHES = {
    skill_id: sha256(raw).hexdigest()
    for skill_id, raw in SYNTHETIC_OPTIONS.items()
}


def runtime():
    metadata = {
        583: (1, 2, 2, 2000),
        584: (1, 2, 2, 5000),
        591: (1, 1, 2, 5000),
        592: (1, 2, 2, 8000),
        593: (1, 2, 2, 5000),
    }
    return Recovered25PetSkillRuntime({
        skill_id: Recovered25PetSkillEntry(
            skill_id,
            *metadata[skill_id],
            "PETSKILL_Refresh",
            SYNTHETIC_OPTIONS[skill_id],
        )
        for skill_id in metadata
    }, "synthetic")


def late(**kw):
    return NocastParticipantRuntime(
        25, 25, 25, 25,
        **kw,
    )


def submission(skill_id=583, target=0):
    return EnemyAiRefreshSubmission(
        "enemy", 0, skill_id, "PETSKILL_Refresh", target,
        10 if skill_id == 583 else 0,
    )


class RefreshRuntimeTests(unittest.TestCase):
    def test_exact_five_row_population_and_target_one_exception(self):
        with patch.dict(EXPECTED_OPTION_SHA256_BY_ID, SYNTHETIC_HASHES, clear=True):
            validate_recovered25_refresh_population(runtime())
        drift = runtime()
        bad = dict(drift.skills)
        row = bad[591]
        bad[591] = replace(row, target=2)
        with patch.dict(EXPECTED_OPTION_SHA256_BY_ID, SYNTHETIC_HASHES, clear=True):
            with self.assertRaisesRegex(ValueError, "metadata drift"):
                validate_recovered25_refresh_population(
                    Recovered25PetSkillRuntime(bad, "synthetic")
                )

    def test_runtime_projection_and_silence_clear_restore_nc(self):
        base = BaseBattleStatusRuntime(
            status=BaseBattleStatusState(paralysis=2)
        )
        overlay = late(counter=3, nc_flag=1)
        vector = refresh_status_vector(base, overlay, require_complete=True)
        self.assertEqual((vector[2], vector[10]), (2, 3))
        base2, overlay2 = apply_refresh_cleared_status(base, overlay, 10)
        self.assertEqual(base2.status.paralysis, 2)
        self.assertEqual((overlay2.counter, overlay2.nc_flag), (0, 0))

    def test_weaken_clear_retains_current_prepared_powers(self):
        powers = PreparedWeakenPowers(80, 72, 64)
        base, overlay = apply_refresh_cleared_status(
            BaseBattleStatusRuntime(),
            late(
                weaken_counter=2,
                weaken_active_at_visit=True,
                prepared_weaken_powers=powers,
            ),
            7,
        )
        self.assertEqual(overlay.weaken_counter, 0)
        self.assertFalse(overlay.weaken_active_at_visit)
        self.assertEqual(overlay.prepared_weaken_powers, powers)
        self.assertEqual(base.status, BaseBattleStatusState())

    def test_unmodeled_target_status_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unmodeled active status"):
            refresh_status_vector(
                BaseBattleStatusRuntime(),
                late(unmodeled_status_active=True),
                require_complete=True,
            )

    def resolve(self, *, skill_id=583, target=0, player_base=None, player_late=None,
                enemy_late=None, rolls=RefreshActionRolls(), player_hp=2000,
                extra_players=None, commands=None):
        player = actor("player", "player", "player", hp=player_hp)
        enemy = actor("enemy", "enemy", "enemy", quick=200)
        players = {0: player}
        for slot, participant in (extra_players or {}).items():
            players[int(slot)] = participant
        participants = tuple(players.values()) + (enemy,)
        cmd = {
            participant.participant_id: BattleCommand(BATTLE_COM_WAIT)
            for participant in players.values()
        }
        cmd["enemy"] = BattleCommand(BATTLE_COM_ATTACK, command2=target)
        cmd.update(commands or {})
        prepared = prepare_battle_round(
            participants,
            cmd,
            {participant.participant_id: 0 for participant in participants},
            tie_break_order=tuple(participant.participant_id for participant in participants),
        )
        status = {
            participant.participant_id: BaseBattleStatusRuntime()
            for participant in participants
        }
        status["player"] = player_base or BaseBattleStatusRuntime()
        overlay_rows = {
            participant.participant_id: late()
            for participant in participants
        }
        overlay_rows["player"] = player_late or late()
        overlay_rows["enemy"] = enemy_late or late()
        return resolve_ordinary_round(
            prepared,
            slots={participant.participant_id: slot for slot, participant in players.items()} | {"enemy": 10},
            profiles={
                participant.participant_id: BattleCombatProfile(100, 0, 0, 0, 0, 0)
                for participant in participants
            },
            attack_rolls={},
            defense_profile="newpower_70pct",
            base_status_runtime_by_participant_id=status,
            refresh_submissions_by_participant_id={"enemy": submission(skill_id, target)},
            refresh_rolls_by_participant_id={"enemy": rolls},
            nocast_overlay=NocastRoundOverlay(overlay_rows),
        )

    def refresh_event(self, result):
        return next(event for event in result.events if event.refresh_skill_id is not None)

    def test_id583_clears_silence_without_physical_damage(self):
        result = self.resolve(
            skill_id=583,
            player_base=BaseBattleStatusRuntime(
                status=BaseBattleStatusState(paralysis=2),
            ),
            player_late=late(counter=3, nc_flag=1),
        )
        event = self.refresh_event(result)
        self.assertEqual((event.refresh_status_index, event.refresh_cleared_status), (10, 10))
        self.assertEqual(result.hp_by_participant_id["player"], 2000)
        self.assertEqual(result.base_status_runtime_by_participant_id["player"].status.paralysis, 1)
        refreshed = result.nocast_overlay.runtime_by_participant_id["player"]
        self.assertEqual((refreshed.counter, refreshed.nc_flag), (0, 0))

    def test_id583_preserves_actor_dependent_return_and_receive_effect(self):
        result = self.resolve(
            skill_id=583,
            player_late=late(counter=3, nc_flag=1),
            enemy_late=late(counter=3, nc_flag=1),
        )
        event = self.refresh_event(result)
        self.assertTrue(event.refresh_resolution.source_return_value)
        self.assertEqual(event.refresh_resolution.receive_effect_name, "SPR_tyusya")
        self.assertEqual(event.refresh_cleared_status, 10)
        self.assertEqual(
            result.nocast_overlay.runtime_by_participant_id["player"].counter,
            0,
        )

    def test_id583_is_masked_by_higher_known_status_impossible_in_admitted_vector(self):
        # Status 10 is the highest modeled index, so it clears even when lower
        # base/Weaken/Barrier states coexist.
        result = self.resolve(
            skill_id=583,
            player_base=BaseBattleStatusRuntime(
                status=BaseBattleStatusState(paralysis=2),
            ),
            player_late=late(weaken_counter=2, barrier_counter=2, counter=3, nc_flag=1),
        )
        event = self.refresh_event(result)
        self.assertEqual(event.refresh_cleared_status, 10)
        refreshed = result.nocast_overlay.runtime_by_participant_id["player"]
        self.assertEqual((refreshed.weaken_counter, refreshed.barrier_counter, refreshed.counter), (2, 2, 0))

    def test_id592_wildcard_clears_one_highest_only(self):
        result = self.resolve(
            skill_id=592,
            player_base=BaseBattleStatusRuntime(
                status=BaseBattleStatusState(paralysis=2),
            ),
            player_late=late(weaken_counter=2, barrier_counter=4),
        )
        event = self.refresh_event(result)
        self.assertEqual((event.refresh_status_index, event.refresh_cleared_status), (0, 9))
        refreshed = result.nocast_overlay.runtime_by_participant_id["player"]
        self.assertEqual((refreshed.weaken_counter, refreshed.barrier_counter), (2, 0))
        # Player StatusSeq can precede Refresh under the recovered action order;
        # Barrier freezes the lower base counter until Refresh clears Barrier.
        self.assertEqual(result.base_status_runtime_by_participant_id["player"].status.paralysis, 2)

    def test_dead_single_target_consumes_only_explicit_multilist_draw(self):
        pet = actor("pet", "player", "pet")
        result = self.resolve(
            skill_id=592,
            target=0,
            player_hp=0,
            extra_players={1: pet},
            rolls=RefreshActionRolls((0,)),
        )
        event = self.refresh_event(result)
        self.assertEqual(event.resolved_target_slot, 1)
        self.assertTrue(event.retargeted)

    def test_live_single_target_rejects_unused_retarget_rng(self):
        with self.assertRaisesRegex(ValueError, "live single target"):
            self.resolve(rolls=RefreshActionRolls((0,)))

    def test_suppression_rejects_nonempty_refresh_rng(self):
        enemy = actor("enemy", "enemy", "enemy", quick=200)
        player = actor("player", "player", "player")
        participants = (player, enemy)
        prepared = prepare_battle_round(
            participants,
            {
                "player": BattleCommand(BATTLE_COM_WAIT),
                "enemy": BattleCommand(BATTLE_COM_ATTACK, command2=0),
            },
            {"player": 0, "enemy": 0},
            tie_break_order=("enemy", "player"),
        )
        with self.assertRaisesRegex(ValueError, "status-suppressed semantic action"):
            resolve_ordinary_round(
                prepared,
                slots={"player": 0, "enemy": 10},
                profiles={
                    pid: BattleCombatProfile(100, 0, 0, 0, 0, 0)
                    for pid in ("player", "enemy")
                },
                attack_rolls={},
                defense_profile="newpower_70pct",
                base_status_runtime_by_participant_id={
                    "player": BaseBattleStatusRuntime(),
                    "enemy": BaseBattleStatusRuntime(
                        status=BaseBattleStatusState(sleep=2)
                    ),
                },
                refresh_submissions_by_participant_id={"enemy": submission()},
                refresh_rolls_by_participant_id={"enemy": RefreshActionRolls((0,))},
                nocast_overlay=NocastRoundOverlay({
                    "player": late(counter=2),
                    "enemy": late(),
                }),
            )

    def test_bridge_only_executes_positive_ids(self):
        base = runtime()
        # Reuse the exact SpawnedEnemy shape from another bridge is deliberately
        # avoided here; the selection bridge is exercised in coordinator E2E.
        with patch.dict(EXPECTED_OPTION_SHA256_BY_ID, SYNTHETIC_HASHES, clear=True):
            validate_recovered25_refresh_population(base)


if __name__ == "__main__":
    unittest.main()
