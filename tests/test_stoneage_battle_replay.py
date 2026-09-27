import unittest
from unittest.mock import MagicMock, sentinel

from tools.stoneage_battle_event_contract import (
    BattleRoundTransition,
    BattleStateSnapshot,
)
from tools.stoneage_battle_replay import (
    BattleReplay,
    battle_replay_from_transition,
    begin_battle_replay,
)
from tools.stoneage_battle_state_model import FINISHED


def _snapshot(state, *, phase="active"):
    snapshot = MagicMock(spec=BattleStateSnapshot)
    snapshot.state = state
    snapshot.phase = phase
    return snapshot


def _transition(before, after, *, events=(), termination=None):
    transition = MagicMock(spec=BattleRoundTransition)
    transition.before = before
    transition.after = after
    transition.events = tuple(events)
    transition.termination = termination
    return transition


class BattleReplayTests(unittest.TestCase):

    def test_replay_appends_contiguous_transitions_and_flattens_events(self):
        s0 = _snapshot(sentinel.state0)
        s1 = _snapshot(sentinel.state1)
        s2 = _snapshot(sentinel.state2)
        t1 = _transition(s0, s1, events=(sentinel.event1,))
        t2 = _transition(s1, s2, events=(sentinel.event2, sentinel.event3))

        replay = begin_battle_replay(s0).append(t1).append(t2)

        self.assertIsInstance(replay, BattleReplay)
        self.assertIs(replay.current, s2)
        self.assertEqual(
            replay.events,
            (sentinel.event1, sentinel.event2, sentinel.event3),
        )
        self.assertFalse(replay.finished)

    def test_replay_rejects_state_discontinuity(self):
        s0 = _snapshot(sentinel.state0)
        unrelated = _snapshot(sentinel.other_state)
        s1 = _snapshot(sentinel.state1)
        transition = _transition(unrelated, s1)

        with self.assertRaisesRegex(ValueError, "does not match current state"):
            begin_battle_replay(s0).append(transition)

    def test_replay_rejects_append_after_terminal_transition(self):
        s0 = _snapshot(sentinel.state0)
        s1 = _snapshot(sentinel.state1, phase=FINISHED)
        terminal = _transition(
            s0,
            s1,
            termination=sentinel.termination,
        )
        replay = battle_replay_from_transition(terminal)

        self.assertTrue(replay.finished)
        with self.assertRaisesRegex(ValueError, "after battle termination"):
            replay.append(_transition(s1, _snapshot(sentinel.state2)))

    def test_constructor_rejects_transition_after_termination(self):
        s0 = _snapshot(sentinel.state0)
        s1 = _snapshot(sentinel.state1, phase=FINISHED)
        s2 = _snapshot(sentinel.state2)
        terminal = _transition(
            s0,
            s1,
            termination=sentinel.termination,
        )
        extra = _transition(s1, s2)

        with self.assertRaisesRegex(ValueError, "after termination"):
            BattleReplay(initial=s0, transitions=(terminal, extra))


if __name__ == "__main__":
    unittest.main()
