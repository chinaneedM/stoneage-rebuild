"""Modifyattack is per-action state and cannot enter native combo rewriting."""
import unittest

from tests.test_stoneage_modifyattack_runtime import actor, hit, submission
from tests.test_stoneage_lighttakeed_runtime import session
from tools.stoneage_battle_round_model import BATTLE_COM_ATTACK, BATTLE_COM_WAIT, BattleCommand, BattleCombatProfile
from tools.stoneage_battle_state_model import begin_persistent_battle, resolve_persistent_ordinary_round


class ModifyAttackPersistentRuntimeTests(unittest.TestCase):
    def test_following_ordinary_round_does_not_replay_helper_or_change_powers(self):
        player=actor('player','player','player',hp=5000)
        enemy=actor('enemy','enemy','enemy',quick=200)
        state=begin_persistent_battle(session(player,enemy),slots={'player':0,'enemy':10})
        args=dict(commands={'player':BattleCommand(BATTLE_COM_WAIT),'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0)},
            initiative_random_subtracts={'player':0,'enemy':0},
            profiles={'player':BattleCombatProfile(100,0,100,0,0,0),'enemy':BattleCombatProfile(100,0,0,0,0,0)},
            attack_rolls={'enemy':hit()},defense_profile='newpower_70pct')
        first=resolve_persistent_ordinary_round(state,**args,
            modifyattack_submissions_by_participant_id={'enemy':submission()},modifyattack_rand_by_participant_id={'enemy':0})
        second=resolve_persistent_ordinary_round(first.after,**args)
        event=next(e for e in first.round.events if e.modifyattack_skill_id is not None)
        ordinary=next(e for e in second.round.events if e.participant_id=='enemy' and e.damage is not None)
        self.assertEqual(ordinary.damage,event.modifyattack_damage_before)
        self.assertTrue(all(e.modifyattack_skill_id is None for e in second.round.events))
        self.assertEqual(second.after.hp_by_participant_id['player'],5000-event.damage-ordinary.damage)
        self.assertEqual((second.after.session.enemies[0].attack,second.after.session.enemies[0].defense),(enemy.attack,enemy.defense))
        self.assertEqual(dict(second.after.carried_commands_by_participant_id),{})

    def test_persistent_combo_rewrite_cannot_start_or_join_with_modifyattack(self):
        player=actor('player','player','player',hp=5000)
        enemy=actor('enemy','enemy','enemy',quick=200)
        enemy2=actor('enemy2','enemy','enemy',quick=100)
        from dataclasses import replace
        state=begin_persistent_battle(replace(session(player,enemy),enemies=(enemy,enemy2)),
            slots={'player':0,'enemy':10,'enemy2':11})
        for enemy2_quick in (100,300):
            state=begin_persistent_battle(replace(session(player,enemy),enemies=(enemy,replace(enemy2,quick=enemy2_quick))),
                slots={'player':0,'enemy':10,'enemy2':11})
            result=resolve_persistent_ordinary_round(state,
                commands={'player':BattleCommand(BATTLE_COM_WAIT),'enemy':BattleCommand(BATTLE_COM_ATTACK,command2=0),
                          'enemy2':BattleCommand(BATTLE_COM_ATTACK,command2=0)},
                initiative_random_subtracts={'player':0,'enemy':0,'enemy2':0},
                profiles={'player':BattleCombatProfile(100,0,100,0,0,0),'enemy':BattleCombatProfile(100,0,0,0,0,0),
                          'enemy2':BattleCombatProfile(100,0,0,0,0,0)},
                attack_rolls={'enemy':hit(),'enemy2':hit()},defense_profile='newpower_70pct',
                combo_start_rolls_1_100={'enemy2':1},
                modifyattack_submissions_by_participant_id={'enemy':submission()},modifyattack_rand_by_participant_id={'enemy':0})
            self.assertEqual(len([e for e in result.round.events if e.modifyattack_skill_id is not None]),1)
            self.assertFalse(any(e.result.startswith('combo') for e in result.round.events))


if __name__=='__main__':
    unittest.main()
