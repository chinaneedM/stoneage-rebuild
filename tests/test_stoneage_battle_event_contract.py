import unittest
from dataclasses import replace
from types import MappingProxyType

from tools.stoneage_battle_event_contract import (
    BattleExecutionEvent,
    BattleIntent,
    BattleRoundTransition,
    BattleStateSnapshot,
    build_battle_round_transition,
)
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK,
    BATTLE_COM_WAIT,
    BattleCommand,
    OrdinaryRoundEvent,
    ResolvedOrdinaryRound,
)
from tools.stoneage_battle_state_model import (
    FINISHED,
    PLAYER_WIN,
    PersistentRoundResult,
    begin_persistent_battle,
)
from tools.stoneage_singleplayer_battle import BattleParticipant, BattleSession
from tools.stoneage_singleplayer_domain import GroupEncounterRequest, MapPosition


def _fixture_state():
    position = MapPosition(floor_id=100, x=5, y=6)
    encounter = GroupEncounterRequest(
        area_index=0,
        position=position,
        group_id=1,
        max_enemy_count=1,
    )
    player = BattleParticipant(
        participant_id="player",
        side="player",
        kind="player",
        level=10,
        hp=100,
        max_hp=100,
        attack=80,
        defense=70,
        quick=60,
        name="Hero",
    )
    enemy = BattleParticipant(
        participant_id="enemy:1",
        side="enemy",
        kind="enemy",
        level=5,
        hp=40,
        max_hp=40,
        attack=30,
        defense=20,
        quick=20,
        name="Enemy",
    )
    session = BattleSession(
        origin_position=position,
        encounter=encounter,
        player=player,
        allied_pets=(),
        enemies=(enemy,),
    )
    return begin_persistent_battle(
        session,
        slots={"player": 0, "enemy:1": 10},
    )


def _resolved_transition(*, finished=False):
    before = _fixture_state()
    commands = MappingProxyType({
        "player": BattleCommand(BATTLE_COM_ATTACK, command2=10),
        "enemy:1": BattleCommand(BATTLE_COM_WAIT),
    })
    hp = MappingProxyType({"player": 100, "enemy:1": 0 if finished else 25})
    event = OrdinaryRoundEvent(
        participant_id="player",
        slot=0,
        command1=BATTLE_COM_ATTACK,
        action_value=70,
        result="hit",
        original_target_slot=10,
        resolved_target_slot=10,
        damage=15 if not finished else 40,
        target_hp_before=40,
        target_hp_after=25 if not finished else 0,
    )
    round_result = ResolvedOrdinaryRound(
        events=(event,),
        hp_by_participant_id=hp,
        hp_by_slot=MappingProxyType({
            0: 100,
            10: 0 if finished else 25,
        }),
        action_order=("player", "enemy:1"),
    )
    if finished:
        after = replace(
            before,
            hp_by_participant_id=hp,
            turn=1,
            phase=FINISHED,
            result=PLAYER_WIN,
            winning_side=0,
            last_commands=commands,
        )
    else:
        after = replace(
            before,
            hp_by_participant_id=hp,
            turn=1,
            last_commands=commands,
        )
    return PersistentRoundResult(
        before=before,
        round=round_result,
        after=after,
    )


class BattleEventContractTests(unittest.TestCase):

    def test_active_round_exposes_protocol_free_typed_layers(self):
        transition = build_battle_round_transition(_resolved_transition())

        self.assertIsInstance(transition, BattleRoundTransition)
        self.assertIsInstance(transition.before, BattleStateSnapshot)
        self.assertEqual(
            [intent.participant_id for intent in transition.intents],
            ["player", "enemy:1"],
        )
        self.assertTrue(
            all(isinstance(intent, BattleIntent) for intent in transition.intents)
        )
        self.assertEqual(transition.intents[0].command.command1, BATTLE_COM_ATTACK)
        self.assertEqual(transition.intents[1].command.command1, BATTLE_COM_WAIT)

        self.assertEqual(transition.before.turn, 0)
        self.assertEqual(transition.after.turn, 1)
        self.assertEqual(transition.turn_sync.previous_turn, 0)
        self.assertEqual(transition.turn_sync.completed_turn, 1)
        self.assertEqual(
            transition.turn_sync.action_order,
            ("player", "enemy:1"),
        )

        self.assertEqual(len(transition.events), 1)
        self.assertIsInstance(transition.events[0], BattleExecutionEvent)
        self.assertEqual(transition.events[0].sequence, 0)
        self.assertEqual(transition.events[0].event.result, "hit")
        self.assertEqual(transition.events[0].event.damage, 15)
        self.assertIsNone(transition.termination)

    def test_finished_round_emits_typed_termination(self):
        transition = build_battle_round_transition(
            _resolved_transition(finished=True)
        )
        self.assertEqual(transition.after.phase, FINISHED)
        self.assertIsNotNone(transition.termination)
        self.assertEqual(transition.termination.turn, 1)
        self.assertEqual(transition.termination.result, PLAYER_WIN)
        self.assertEqual(transition.termination.winning_side, 0)

    def test_intents_are_slot_ordered_not_mapping_ordered(self):
        result = _resolved_transition()
        reversed_commands = MappingProxyType({
            "enemy:1": result.after.last_commands["enemy:1"],
            "player": result.after.last_commands["player"],
        })
        result = replace(
            result,
            after=replace(result.after, last_commands=reversed_commands),
        )
        transition = build_battle_round_transition(result)
        self.assertEqual(
            [intent.slot for intent in transition.intents],
            [0, 10],
        )

    def test_turn_drift_is_rejected(self):
        result = _resolved_transition()
        drifted = replace(
            result,
            after=replace(result.after, turn=2),
        )
        with self.assertRaisesRegex(ValueError, "advance exactly one round"):
            build_battle_round_transition(drifted)

    def test_command_without_before_state_slot_is_rejected(self):
        result = _resolved_transition()
        commands = dict(result.after.last_commands)
        commands["ghost"] = BattleCommand(BATTLE_COM_WAIT)
        malformed = replace(
            result,
            after=replace(
                result.after,
                last_commands=MappingProxyType(commands),
            ),
        )
        with self.assertRaisesRegex(
            ValueError,
            "absent from before-state slots",
        ):
            build_battle_round_transition(malformed)


if __name__ == "__main__":
    unittest.main()
