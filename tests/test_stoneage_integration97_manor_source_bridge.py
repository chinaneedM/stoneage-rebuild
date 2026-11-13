"""Source-bounded, public-metadata-only manor/shop/warpman replay.

Tests do not load original commercial NPC scripts or claim native gameplay.
"""
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / 'research/recovered/STONEAGE-INTEGRATION97-FOUR-MANOR-SOURCE-GATES-SHOPS-R1.json').read_text())
MAP = json.loads((ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json').read_text())
ITEM01_PATH = ROOT / 'research/recovered/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json'

class ManorSourceBridgeTests(unittest.TestCase):
    def test_identity_and_private_custody(self):
        self.assertEqual(D['schema'],'stoneage.integration97_four_manor_original_create_warpman_shop_source.r1')
        c=D['custody']
        self.assertEqual(c['private_zip_bytes'],995176)
        self.assertEqual(c['private_zip_sha256'],'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(c['all_zip_entries_crc_passed'],2205)
        self.assertEqual(c['source_parent_RAR_sha256_historical_not_reread_this_round'],'d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5')

    def test_active_and_backup_filename_separation(self):
        a=D['source_configuration_files_4_create_5_bak']
        self.assertEqual(len(a),9)
        self.assertEqual([v['source_blocks_not_runtime_NPCs'] for v in a],[9,8,8,8,6,8,8,8,8])
        self.assertEqual([v['shop_blocks'] for v in a[:4]],[5,5,5,5])
        self.assertEqual([v['warpman_blocks'] for v in a[:4]],[4,3,3,3])
        self.assertTrue(all(v['file'].endswith('.create') for v in a[:4]))
        self.assertTrue(all(v['file'].endswith('.create.bak') for v in a[4:]))
        self.assertTrue(all(v['configuration_filename_role']=='SOURCE_BAK_FILENAME_NOT_ESTABLISHED_LOADED' for v in a[4:]))

    def test_all_source_create_references_are_unique_and_bounded(self):
        blocks=D['active_named_create_blocks']
        self.assertEqual(len(blocks),33)
        self.assertEqual(len({(b['create_file'],b['create_index_zero_based']) for b in blocks}),33)
        self.assertEqual(Counter(b['original_type'] for b in blocks),{'npcgen_shop':20,'npcgen_warpman':13})
        self.assertEqual(len({b['original_handler_file'] for b in blocks}),33)
        files={x['file']:x for x in D['source_configuration_files_4_create_5_bak']}
        for b in blocks:
            self.assertRegex(b['create_byte_window_sha256'],r'^[0-9a-f]{64}$')
            self.assertRegex(b['original_handler_full_SHA256'],r'^[0-9a-f]{64}$')
            lo,hi=b['create_byte_span'];self.assertGreaterEqual(lo,0);self.assertLess(lo,hi)
            self.assertLessEqual(hi,files[b['create_file']]['file_size'])
            self.assertNotIn('.bak',b['create_file'])

    def test_original_20_shop_files_are_prior_item01_not_new_merchants(self):
        shops=D['referenced_shop_files_prior_ITEM01_already_known'];self.assertEqual(len(shops),20)
        self.assertEqual(sum(len(s['ItemList_numeric_IDs_static']) for s in shops),45)
        self.assertEqual({s['source_buy_rate_literal'] for s in shops},{'1.0'})
        self.assertEqual({s['source_sell_rate_literal'] for s in shops},{'0.5'})
        # When in a real repo checkout, additionally prove overlap with pre-existing ITEM01, not a fresh shop discovery.
        if ITEM01_PATH.exists():
            j=json.loads(ITEM01_PATH.read_text())
            existing={x['path']:x for x in j['shop_argument_rows']}
            refs={(x['create_path'],x['argument_path'],x['argument_sha256']) for x in j['npcgen_shop_creation_rows']}
            for s in shops:
                key=s['handler_file'].removeprefix('npc/')
                self.assertIn(key,existing)
                self.assertEqual(s['handler_SHA256'],existing[key]['source_sha256'])
                self.assertEqual(s['ItemList_numeric_IDs_static'],existing[key]['expanded_candidate_IDs_not_proven_runtime'])
                self.assertIn((s['create_file'].removeprefix('npc/'),key,s['handler_SHA256']),refs)
        else:
            self.assertFalse(bool(__import__('os').environ.get('GITHUB_ACTIONS')), 'ITEM01 index must exist on CI checkout')

    def test_guard_event_blocks_are_literal_not_executed(self):
        guards=D['guard_handler_files_new_crossmodule_access_relationship'];self.assertEqual(len(guards),13)
        allrows=[r for g in guards for r in g['source_event_sections_static_not_execution']]
        self.assertEqual(len(allrows),43)
        self.assertEqual(sum(r['WARP_literal_target']==[0,0,0] for r in allrows),13)
        self.assertEqual(sum(r['WARP_literal_target']!=[0,0,0] for r in allrows),30)
        self.assertEqual(sum(r['DelItem_source_literal'] is not None for r in allrows),17)
        self.assertEqual(sum(r['source_event_tag']=='NEWWARPMAN' for r in allrows),13)
        for r in allrows:
            self.assertRegex(r['FREE_literal'],r'^(?:LV>0|LV>0&MANOR=[0-3]|ITEM=\d+)$')
            if r['DelItem_source_literal']:
                self.assertEqual(r['FREE_literal'],'ITEM='+str(r['DelItem_source_literal']['item_id']))
                self.assertEqual(r['DelItem_source_literal']['count'],1)

    def test_four_family_shops_cross_link_gate_item_conditions(self):
        shops={s['handler_file']:s for s in D['referenced_shop_files_prior_ITEM01_already_known']}
        self.assertEqual(set(D['family_pass_invitation_crossfile_bridge']),{'1','2','3','4'})
        for i in range(1,5):
            f=D['family_pass_invitation_crossfile_bridge'][str(i)]
            self.assertEqual(f['MANOR_literal_index'],i-1)
            self.assertEqual(f['invitation_item_ID_literal'],19000+i)
            self.assertEqual(f['pass_item_ID_literal'],19329+i)
            self.assertEqual(shops[f'npc/family/npc/shop{i}_5']['ItemList_numeric_IDs_static'],[19329+i])
            self.assertTrue(f['prior_shop_ItemList_same_pass_ID'])
            self.assertEqual(f['guard_member_predicate_rows'],4 if i==1 else 3)
            self.assertEqual(f['guard_invitation_predicate_rows'],3 if i==1 else 2)
            self.assertEqual(f['guard_pass_predicate_rows'],2)

    def test_21_prior_DAT_floors_replay_and_inbounds(self):
        prior={v[0]:v for v in MAP['per_floor_source_rows']}
        rows=D['prior_MAP04_Dat_numeric_join_no_new_DAT_reads']
        self.assertEqual(len(rows),21)
        dims={r['floor']:(r['DAT_width'],r['DAT_height']) for r in rows}
        for r in rows:
            other=prior[f"{r['floor']}.dat"]
            self.assertEqual([r['DAT_sha256'],r['DAT_width'],r['DAT_height']],other[2:5])
        for b in D['active_named_create_blocks']:
            w,h=dims[b['floor']]
            self.assertTrue(0<=b['spawn'][0]<w and 0<=b['spawn'][1]<h)
        positives=0
        for g in D['guard_handler_files_new_crossmodule_access_relationship']:
            for r in g['source_event_sections_static_not_execution']:
                fl,x,y=r['WARP_literal_target']
                if fl:
                    w,h=dims[fl]
                    self.assertTrue(0<=x<w and 0<=y<h)
                    positives+=1
        self.assertEqual(positives,30)

    def test_prior_CHAR01_42_full_files_and_33_exact_create_windows(self):
        previous = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
        if not previous.exists():
            self.assertFalse(bool(__import__('os').environ.get('GITHUB_ACTIONS')), 'CHAR01 prior index required in GitHub checkout')
            return
        prior=json.loads(previous.read_text())
        actual={x[0]:x for x in prior['source_files']}
        config=D['source_configuration_files_4_create_5_bak']
        all_files=[(x['file'],x['file_size'],x['full_SHA256']) for x in config]
        all_files.extend((x['handler_file'],x['handler_bytes'],x['handler_SHA256']) for x in D['referenced_shop_files_prior_ITEM01_already_known'])
        all_files.extend((x['handler_file'],x['handler_bytes'],x['handler_SHA256']) for x in D['guard_handler_files_new_crossmodule_access_relationship'])
        self.assertEqual(len(all_files),42)
        for path,nbytes,digest in all_files:
            old=actual[path.removeprefix('npc/')]
            self.assertEqual((old[1],old[2]),(nbytes,digest))
        by_key={(r[0],r[1]):r for r in prior['create_rows']}
        for v in D['active_named_create_blocks']:
            old=by_key[(v['create_file'].removeprefix('npc/'),v['create_index_zero_based'])]
            self.assertEqual(old[2:4],v['create_byte_span'])
            self.assertEqual(old[4],v['create_byte_window_sha256'])
            self.assertEqual(old[5],v['floor'])
            self.assertEqual(old[6],v['graphicname'])
            self.assertEqual(old[7][:2],v['spawn'])
            self.assertEqual(old[11],v['original_type'])
            self.assertTrue(any(row[0]==v['original_handler_file'].removeprefix('npc/') and row[2]==v['original_handler_full_SHA256'] for row in old[15]))

    def test_derived_counts_reconcile(self):
        c=D['counts'];self.assertEqual(c['active_named_create_files'],4)
        self.assertEqual(c['backup_filename_only_files'],5)
        self.assertEqual(c['active_named_create_configurations'],33)
        self.assertEqual(c['source_shop_create_configurations'],20)
        self.assertEqual(c['source_warpman_create_configurations'],13)
        self.assertEqual(c['guard_literal_event_sections'],43)
        self.assertEqual(c['guard_fallback_warp_zero_static'],13)
        self.assertEqual(c['guard_nonzero_warp_literal_branches'],30)
        self.assertEqual(c['guard_explicit_DelItem_occurrences'],17)
        self.assertEqual(c['prior_MAP04_matched_distinct_floor_ids'],21)
        self.assertEqual(c['active_CREATE_spawn_in_prior_DAT_bounds'],33)
        self.assertEqual(c['guard_nonzero_target_in_prior_DAT_bounds'],30)

    def test_version_runtime_and_copyright_guards(self):
        b=D['bounds']
        for k in ('native_warp_party_membership_or_item_consumption_executed',
                  'native_shop_trade_prices_CostFame_executed',
                  'same_historical_official_deployment_TW1_or_mainland182_proven',
                  'original_DAT_files_or_MAP04_pixels_re_read_this_work_unit',
                  'source_handler_dialogues_reproduced_in_public',
                  'original_client_native_gameplay_executed'):
            self.assertIs(b[k],False,k)
        self.assertEqual(b['Stage_A'],'7 PARTIAL + 2 OPEN')
        self.assertEqual(b['Stage_B'],'GATED')
        self.assertEqual(b['wiki'],'GATED')
        self.assertIsNone(b['overall_completion_percentage'])
        self.assertNotIn('NomalMsg',json.dumps(D))
        self.assertNotIn('PartyMsg',json.dumps(D))

if __name__=='__main__':unittest.main()
