"""Public numeric-source QUEST17 acceptance. No private commercial assets in CI."""
import hashlib
import json
import os
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path

from tools.stoneage_quest17_dino_ranch_source import (
    ROOT, PUBLIC_PATH, QUEST01_GIT_BLOB, MAP09_GIT_BLOB, SOURCE_CREATE,
    SOURCE_SCRIPTS, UNREFERENCED_ALTERNATES, MAP09_FLOORS, ITEM_IDS, PET_GROUPS,
    validate_report, parse_creates, parse_events, sha, crc,
)

QUEST01=ROOT/'research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
MAP09=ROOT/'research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json'
ITEM02=ROOT/'research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json'


def git_blob(b:bytes)->str:
    return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()


class Quest17OriginalSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(PUBLIC_PATH.read_text('utf-8'))
        cls.q=json.loads(QUEST01.read_text('utf-8'))
        cls.maps=json.loads(MAP09.read_text('utf-8'))
        cls.item02=json.loads(ITEM02.read_text('utf-8'))
        cls.scripts={x['path']:x['events'] for x in cls.r['source_scripts']}

    def test_01_git_blob_identity_and_source_conservation(self):
        if os.environ.get('STONEAGE_LOCAL_CROSS_INDEX_FIXTURE') != '1':
            self.assertEqual(git_blob(QUEST01.read_bytes()),QUEST01_GIT_BLOB)
            self.assertEqual(git_blob(MAP09.read_bytes()),MAP09_GIT_BLOB)
        self.assertEqual(self.r['historical_current_git_blob_unmodified'],
                         'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(self.r['original_npc_verified_member_count'],2205)
        self.assertEqual(len(self.r['source_manifest']),11)
        self.assertEqual({x['path'] for x in self.r['source_manifest']},
                         {SOURCE_CREATE,*SOURCE_SCRIPTS,*UNREFERENCED_ALTERNATES,'jaruga/event/event.template'})
        for v in self.r['source_manifest']:
            self.assertRegex(v['sha256'],r'^[0-9a-f]{64}$')
            self.assertRegex(v['crc32'],r'^[0-9a-f]{8}$')
            self.assertGreater(v['bytes'],0)

    def test_02_six_true_create_entries_and_two_verified_floors(self):
        creates=self.r['source_creates']
        self.assertEqual([x['script_ref'] for x in creates],SOURCE_SCRIPTS)
        self.assertEqual([(x['floor'],x['borncorner'][:2],x['graphic_alias']) for x in creates],[
            (201,[19,24],16017),(20901,[14,8],16018),(201,[19,13],16067),
            (201,[19,14],16036),(201,[19,15],16065),(20901,[22,16],16046)])
        refs=[x for x in self.q['source_creation_references'] if x['create_source_path']==SOURCE_CREATE]
        self.assertEqual(len(refs),6)
        for x in creates:
            y=next(v for v in refs if v['create_brace_ordinal']==x['ordinal'])
            self.assertEqual((y['floorid'],y['graphic_alias_numeric'],y['original_script_path']),
                             (x['floor'],x['graphic_alias'],x['script_ref']))

    def test_03_61_event_blocks_legacy_index_exact_sha(self):
        self.assertEqual([len(self.scripts[p]) for p in SOURCE_SCRIPTS],[25,4,10,10,10,2])
        old={(x['script_path'],x['script_block_ordinal']):x for x in self.q['source_event_blocks']
             if x['script_path'] in SOURCE_SCRIPTS}
        actual={(s,e['ordinal']):e for s,es in self.scripts.items() for e in es}
        self.assertEqual(set(actual),set(old))
        for key,e in actual.items():
            t=old[key]
            self.assertEqual((e['type'],e['event_no'],e['condition_sha256'],e['section_sha256']),
                (t['raw_type'],t['event_number'],t['condition_expression_decoded_cp950_UTF8_sha256'],
                 t['source_section_decoded_cp950_normalized_UTF8_sha256']))
        self.assertEqual(Counter(e['type'] for e in actual.values()),
                         Counter({'ACCEPT':51,'MESSAGE':9,'REQUEST':1}))
        self.assertEqual({e['event_no'] for e in actual.values()},{-1})

    def test_04_21_source_literal_payment_grid_not_formula(self):
        expected={
            2596:[14400,6300,2860,2160,1620,990,450],
            2595:[11200,4900,2275,1680,1260,770,350],
            2594:[6400,2800,1300,1030,780,480,200],
        }
        v=self.r['source_21_payment_literals']
        self.assertEqual(len(v),21)
        for wrist,amounts in expected.items():
            rows=[x for x in v if x['wristband_id']==wrist]
            self.assertEqual([x['source_getstone_literal'] for x in rows],amounts)
            self.assertEqual([(x['voucher_id'],x['voucher_quantity']) for x in rows],
                             [(2592,1),(2591,1),(2590,1),(2589,4),(2589,3),(2589,2),(2589,1)])
            for x in rows:
                script=self.scripts['jaruga/event/bait_01'][x['event_ordinal']]
                self.assertEqual(script['commands']['GetStone'],[str(x['source_getstone_literal'])])
                self.assertEqual(script['commands']['DelItem'],[x['original_delitem_literal']])
                self.assertIn(f'ITEM={wrist}',script['condition_literal'])
        self.assertEqual(self.r['source_command_totals']['GetStone'],21)

    def test_05_original_three_wristband_level_branch_boundaries(self):
        s=self.scripts['jaruga/event/bait_02']
        self.assertEqual([x['condition_literal'] for x in s[:3]],[
            'LV>29&ITEM=2593&ITEM!=2596',
            'LV>11&LV<30&ITEM=2593&ITEM!=2595',
            'LV>4&LV<12&ITEM=2593&ITEM!=2594',
        ])
        self.assertEqual([x['commands']['GetItem'] for x in s[:3]],
                         [['2596'],['2595'],['2594']])
        first=self.scripts['jaruga/event/bait_01']
        self.assertEqual(first[21]['type'],'REQUEST')
        self.assertEqual(first[21]['commands']['GetItem'],['2593'])
        self.assertEqual(first[23]['commands']['DelItem'],['2593'])
        self.assertEqual(first[24]['condition_literal'],'LV>0&LV<4')
        self.assertNotIn('GetItem',first[24]['commands'])

    def test_06_pet_group_predicates_and_six_exchange_sections_each(self):
        for path,(band,pet,alt) in PET_GROUPS.items():
            es=self.scripts[path]
            self.assertEqual(len(es),10)
            self.assertEqual([x['commands'].get('DelPet') for x in es[:6]],
              [['EVDEL'],['EVDEL'],*[ [f'PET>0-{pet}*{n}'] for n in (4,3,2,1)]])
            self.assertEqual([x['commands'].get('NotDel') for x in es[:6]],
              [[str(band)],[str(band)],None,None,None,None])
            self.assertTrue(all(f'PET>0-{pet}' in x['condition_literal'] for x in es[:6]))
            self.assertTrue(all(f'ITEM={band}' in x['condition_literal'] for x in es[:6]))
            self.assertEqual([x['commands']['GetItem'] for x in es[:6]],
              [['2591*1'],['2590*1'],['2589*4'],['2589*3'],['2589*2'],['2589*1']])
            self.assertEqual([x['commands']['GetItem'] for x in es[6:9]],
              [['2592*1'],['2592*1'],['2592*1']])
        self.assertEqual(self.r['source_command_totals']['DelPet'],18)
        self.assertEqual(self.r['source_command_totals']['NotDel'],6)

    def test_07_archived_legacy_variant_not_assumed_current(self):
        v=self.r['source_unreferenced_variants']
        self.assertEqual([x['path'] for x in v],UNREFERENCED_ALTERNATES)
        self.assertEqual([x['event_count'] for x in v],[18,18,18])
        self.assertEqual([x['source_command_counts']['DelPet'] for x in v],[14,14,14])
        self.assertEqual([x['source_command_counts']['GetItem'] for x in v],[17,17,17])
        self.assertTrue(all(x['create_file_reference_count_within_2205_retained_NPC_members']==0 for x in v))
        self.assertEqual([x['unreferenced_variant_events'] for x in self.r['pet_certificate_branches']],
                         [18,18,18])

    def test_08_eight_original_item_ids_sixteen_physical_rows(self):
        idx={x[0]:x for x in self.item02['rows']}
        self.assertEqual([x['item_id'] for x in self.r['source_items']],list(ITEM_IDS))
        for x in self.r['source_items']:
            old=idx[x['item_id']]
            self.assertEqual([t['sha256'] for t in x['source_rows']],old[1:3])
            self.assertEqual([t['original_column_count'] for t in x['source_rows']],[94,94])
            self.assertEqual([t['graphic_alias'] for t in x['source_rows']],[old[3],old[3]])
            self.assertEqual(x['source_image_alias'],old[3])
        self.assertEqual([x['source_image_alias'] for x in self.r['source_items']],
                         [24222]*5+[22120,22114,22118])

    def test_09_four_unique_TW1_candidate_png_source_namespaces(self):
        images=self.r['original_tw1_cross_carrier_candidate_images']
        self.assertEqual([i['alias'] for i in images],[22114,22118,22120,24222])
        for item in self.r['source_items']:
            image=next(i for i in images if i['alias']==item['source_image_alias'])
            self.assertEqual(item['cross_carrier_TW1_candidate_PNG_SHA256'],image['private_png_sha256'])
            self.assertTrue(image['candidate_only_other_TW1_original_source'])
        self.assertFalse(self.r['unverified']['actual_same_build_TW1_image_and_community_item'])

    def test_10_map09_exact_sha_and_original_DAT_not_claimed_reloaded(self):
        entry=self.r['source_map_qualification']
        self.assertEqual(len(entry['previously_verified_map09_DAT']),2)
        self.assertEqual(entry['original_DAT_cells_replayed_this_round'],0)
        for x in entry['previously_verified_map09_DAT']:
            old=self.maps['maps'][str(x['floor'])]
            self.assertEqual((x['sha256'],x['geometry']),(old['source_sha256'],old['geometry']))
            self.assertEqual((x['sha256'],x['geometry']),MAP09_FLOORS[x['floor']])
            self.assertTrue(old['independent_all_three_frames_equal'])
            self.assertFalse(x['source_DAT_bytes_replayed_this_round'])

    def test_11_all_factual_bounds_and_no_private_dialogue(self):
        s=PUBLIC_PATH.read_text('utf-8')
        for forbidden in ['NomalWindowMsg:','NomalMainMsg:','ThanksMsg:','AcceptMsg:',
                          'source-TW1-original-RD-candidates/alias-22114.png']:
            self.assertNotIn(forbidden,s)
        self.assertEqual(self.r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.r['stage_B'],self.r['wiki'],self.r['R79'],self.r['overall_percent']),
                         ('GATED','GATED','PAUSED_NON_BLOCKING',None))
        self.assertTrue(all(v is False for v in self.r['unverified'].values()))
        self.assertEqual(self.r['source_work_scope']['newly_found_original_source_bytes_outside_existing_private_archives'],0)
        self.assertEqual(self.r['next'],'QUEST18-DEDUP-AND-NEXT_SOURCE_READY_ORIGINAL_FAMILY')

    def test_12_public_full_ledger_replay(self):
        validate_report(self.r,quest01=self.q,maps=self.maps,items_shard=self.item02)

    def test_13_synthetic_cp950_chinese_byte_0x7d_brace_regression(self):
        raw=('NPCCREATE\n{\nfloorid=201\nborncorner=19,24,19,24\n'
             'graphicname=16017\nname=洞窟管理者\ndir=6\n'
             'enemy=changeevent|file:jaruga/event/bait_01\n}\n').encode('cp950')
        self.assertIn(b'\x7d',raw)
        self.assertEqual(len(parse_creates(raw)),1)
        self.assertEqual(parse_creates(raw)[0]['script_ref'],'jaruga/event/bait_01')
        self.assertEqual(parse_creates(raw)[0]['original_name'],'洞窟管理者')

    def test_14_synthetic_no_private_parser_and_mutations(self):
        src=(b'EventNo:-1\nTYPE:ACCEPT\nEVENT:LV>4&ITEM=2593\n'
             b'GetItem:2594\nNotDel:2593\nEventEnd\n')
        ev=parse_events(src)
        self.assertEqual(len(ev),1)
        self.assertEqual(ev[0]['commands'],{'GetItem':['2594'],'NotDel':['2593']})
        self.assertEqual(ev[0]['condition_sha256'],sha(b'LV>4&ITEM=2593'))
        with self.assertRaises(AssertionError):parse_events(src[:-len(b'EventEnd\n')])
        for mutate in ('source_event_total','source_items','pet_certificate_branches'):
            broken=deepcopy(self.r)
            if mutate=='source_event_total':broken[mutate]=60
            if mutate=='source_items':broken[mutate]=broken[mutate][:-1]
            if mutate=='pet_certificate_branches':broken[mutate][1]['wristband_id']=777
            with self.assertRaises(AssertionError):validate_report(broken)

    def test_15_cross_index_negative_mutations_rejected(self):
        broken=deepcopy(self.r)
        broken['source_scripts'][0]['events'][0]['condition_sha256']='0'*64
        with self.assertRaises(AssertionError):validate_report(broken,quest01=self.q)
        badmap=deepcopy(self.maps)
        badmap['maps']['201']['source_sha256']='f'*64
        with self.assertRaises(AssertionError):validate_report(self.r,maps=badmap)
        baditem=deepcopy(self.item02)
        for x in baditem['rows']:
            if x[0]==2592: x[1]='0'*64;break
        with self.assertRaises(AssertionError):validate_report(self.r,items_shard=baditem)


if __name__=='__main__':
    unittest.main()
