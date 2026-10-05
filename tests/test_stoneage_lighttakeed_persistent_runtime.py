"""Multi-round witnesses for transferred reaction charges and power lifetime."""

import unittest

from tests.test_stoneage_lighttakeed_runtime import (
    actor, attack_rolls, profile, session, submission,
)
from tools.stoneage_battle_damage_react_model import BaseDamageReactState
from tools.stoneage_battle_round_model import (
    BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BattleCommand,
)
from tools.stoneage_battle_state_model import (
    begin_persistent_battle, resolve_persistent_ordinary_round,
)
from tools.stoneage_lighttakeed_model import (
    PROFILE_BISMARCK_COPY_PLUS_ONE, PROFILE_GAVIN_IRIS_COPY,
)


class LighttakeedPersistentRuntimeTests(unittest.TestCase):
    def test_transferred_vanish_is_consumed_by_later_ordinary_hits(self):
        for source_profile, transferred in (
            (PROFILE_GAVIN_IRIS_COPY, 1),
            (PROFILE_BISMARCK_COPY_PLUS_ONE, 2),
        ):
            with self.subTest(profile=source_profile):
                player=actor("player","player","player",hp=1000,quick=10)
                enemy=actor("enemy","enemy","enemy",hp=1000,quick=100)
                state=begin_persistent_battle(
                    session(player,enemy),
                    slots={"player":0,"enemy":10},
                    base_damage_react_state_by_participant_id={
                        "player":BaseDamageReactState(vanish=2),
                        "enemy":BaseDamageReactState(),
                    },
                )
                first=resolve_persistent_ordinary_round(
                    state,
                    commands={
                        "player":BattleCommand(BATTLE_COM_WAIT),
                        "enemy":BattleCommand(BATTLE_COM_ATTACK,command2=0),
                    },
                    initiative_random_subtracts={"player":0,"enemy":0},
                    profiles={"player":profile(),"enemy":profile()},
                    attack_rolls={"enemy":attack_rolls()},
                    defense_profile="newpower_70pct",
                    lighttakeed_submissions_by_participant_id={
                        "enemy":submission(enemy=enemy,profile_name=source_profile),
                    },
                )
                state=first.after
                self.assertEqual(
                    state.base_damage_react_state_by_participant_id["enemy"].vanish,
                    transferred,
                )
                # Subsequent ordinary player attacks must consume the received
                # charges, never replay the previous semantic submission.
                for remaining in range(transferred-1,-1,-1):
                    result=resolve_persistent_ordinary_round(
                        state,
                        commands={
                            "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                            "enemy":BattleCommand(BATTLE_COM_WAIT),
                        },
                        initiative_random_subtracts={"player":0,"enemy":0},
                        profiles={"player":profile(),"enemy":profile()},
                        attack_rolls={"player":attack_rolls()},
                        defense_profile="newpower_70pct",
                    )
                    state=result.after
                    self.assertEqual(state.hp_by_participant_id["enemy"],1000)
                    self.assertEqual(
                        state.base_damage_react_state_by_participant_id["enemy"].vanish,
                        remaining,
                    )
                    self.assertTrue(all(
                        event.lighttakeed_skill_id is None
                        for event in result.round.events
                    ))
                # An exhausted counter stops protecting on the next hit.
                exhausted=resolve_persistent_ordinary_round(
                    state,
                    commands={
                        "player":BattleCommand(BATTLE_COM_ATTACK,command2=10),
                        "enemy":BattleCommand(BATTLE_COM_WAIT),
                    },
                    initiative_random_subtracts={"player":0,"enemy":0},
                    profiles={"player":profile(),"enemy":profile()},
                    attack_rolls={"player":attack_rolls()},
                    defense_profile="newpower_70pct",
                )
                self.assertLess(exhausted.after.hp_by_participant_id["enemy"],1000)
                # Callback work powers belong to the submitted action, not the
                # next round's persistent base participant attributes.
                self.assertEqual(
                    (state.session.enemies[0].attack,state.session.enemies[0].defense),
                    (enemy.attack,enemy.defense),
                )


if __name__=="__main__":
    unittest.main()
