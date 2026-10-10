import json
import unittest
from tools.stoneage_player_battle_audit import PIN_PATH, cases_for, player_delta, expected_packets


class PlayerBattleTests(unittest.TestCase):
    def setUp(self):self.pins=json.loads(PIN_PATH.read_text())
    def identity(self,p):
        from pathlib import Path
        i=self.pins['profiles'][p]['identity'].copy()
        prior=json.loads((PIN_PATH.parents[2]/i['accepted_pool_pin_path']).read_text())['profiles'][p]['identity']
        from tools.stoneage_default_template_audit import digest
        self.assertEqual(digest(json.dumps(prior,sort_keys=True,separators=(',',':'))),i['accepted_pool_identity_sha256'])
        i['accepted_pool_identity']=prior;return i

    def test_solo_path_pins_actual_party_pet_exp_and_effect_helpers(self):
        for p in self.pins['profiles']:
            for n in ('BATTLE_PartyNewEntry','BATTLE_PetDefaultEntry','BATTLE_ClearGetExp','CHAR_sendBattleEffect'):
                self.assertIn(n,self.identity(p)['functions'])
                self.assertNotIn(n,self.pins['profiles'][p]['unreachable_traps'])

    def test_player_compliance_skill_lookup_and_Lua_empty_registry_are_explicit(self):
        self.assertIn('_CHAR_getIntPSkill',self.identity('gavin')['functions'])
        for n in ('FindLua','EquipEffectFunction','getPartyNum'):
            self.assertIn(n,self.identity('bismarck')['functions'])
        for n in ('lua_pcall','lua_type','strcmptail'):
            self.assertIn(n,self.pins['profiles']['bismarck']['unreachable_traps'])
        self.assertIn('controlled empty',self.identity('bismarck')['Bismarck_Lua_scope'])

    def test_all_selected_records_have_four_RNG_modes(self):
        rows=cases_for([3,9,21])
        self.assertEqual(len(rows),12)
        self.assertEqual(set(rows),{(3,0,1),(3,1,2),(3,2,3),(3,3,1),(9,0,2),(9,1,3),(9,2,1),(9,3,2),(21,0,3),(21,1,1),(21,2,2),(21,3,3)})

    def test_healthy_player_Exit_keeps_live_object_and_clears_battle_state(self):
        for p in self.pins['profiles']:
            i=self.identity(p);ev=i['accepted_pool_identity']['accepted_entry_identity']['enum_values']
            before={ev['CHAR_WORKOBJINDEX']:0,ev['CHAR_WORKGETEXP']:777,ev['CHAR_WORKBATTLEINDEX']:-1,ev['CHAR_WORKBATTLEMODE']:0}
            entered=player_delta(p,i,before,2,False);exited=player_delta(p,i,before,2,True)
            self.assertEqual(entered[ev['CHAR_WORKBATTLEINDEX']],2)
            self.assertEqual(exited[ev['CHAR_WORKBATTLEMODE']],6)
            self.assertNotIn(ev['CHAR_WORKOBJINDEX'],entered);self.assertNotIn(ev['CHAR_WORKOBJINDEX'],exited)
            self.assertNotIn(ev['CHAR_WORKBATTLEINDEX'],exited)
            self.assertEqual(exited[ev['CHAR_WORKGETEXP']],0)

    def test_Bismarck_show_time_and_no_cast_are_profile_specific(self):
        i=self.identity('bismarck');ev=i['accepted_pool_identity']['accepted_entry_identity']['enum_values']
        before={ev['CHAR_WORKNOCAST']:777}
        self.assertEqual(player_delta('bismarck',i,before,1,False)[ev['CHAR_WORKNOCAST']],0)
        after=player_delta('bismarck',i,before,1,True)
        self.assertEqual(after[ev['CHAR_WORKNOCAST']],0)
        self.assertEqual(after[ev['CHAR_WORK_SHOWBATTLETIME']],1002)

    def test_Gavin_network_start_payload_is_exact(self):
        self.assertEqual(expected_packets('gavin',self.identity('gavin'),2,False),
                         [1,1,1,1,7,1,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2])

    def test_Bismarck_network_start_preserves_receive_time_difference(self):
        self.assertEqual(expected_packets('bismarck',self.identity('bismarck'),2,False),
                         [1,1,0,1,7,1,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1])

    def test_Exit_network_tail_has_monitor_status_skill_NC_and_world_XYD(self):
        for p in self.pins['profiles']:
            tail=expected_packets(p,self.identity(p),1,True)
            self.assertEqual(tail[11:13],[1,1]);self.assertGreater(tail[13],0)
            self.assertEqual(tail[14:24],[int(p=='bismarck'),1,1,7,0,1,7,1,1,0])
            self.assertEqual(tail[-1],5 if p=='gavin' else 4)

    def test_collector_signatures_and_real_headers_are_pinned(self):
        for p in self.pins['profiles']:
            i=self.identity(p)
            self.assertEqual(len(i['collector_signature_sha256']),10)
            self.assertTrue(any(x.endswith('/battle.h') for x in i['header_dependency_closure']))
            self.assertTrue(any(x.endswith('/char_base.h') for x in i['header_dependency_closure']))
            self.assertIn('descriptor7',i['adapters'])

    def test_profit_advanced_actor_and_Iris_boundaries_remain_open(self):
        for p,row in self.pins['profiles'].items():
            for n in ('BATTLE_GetExp','BATTLE_GetDuelPoint','NPC_Util_getEnemy','Doujyou_GetEnemy'):
                self.assertIn(n,row['unreachable_traps'])
            self.assertFalse(row['identity']['player_all_fields_independent_oracle'])
            self.assertIn('healthy solo',row['identity']['scope'])
        self.assertIn('OPEN',self.pins['iris_execution'])


if __name__=='__main__':unittest.main()
