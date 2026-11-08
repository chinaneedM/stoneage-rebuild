"""QUEST30: derived-only source identities and negative evidence fences."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
Q=REC/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
C=REC/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
S=REC/'STONEAGE-QUEST30-DINOSAUR-COLLECTOR-EVENT35-SOURCE-R1.json'
W=REC/'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-21-GETPET-QUEST-BRANCHES-R1.json'
M=REC/'STONEAGE-QUEST05-598-ORIGINAL-CREATE-FLOOR-MAP-AND-WARP-CROSSWALK-R1.json'
Q09=REC/'STONEAGE-QUEST09-DREAM-CAVE-ORIGINAL-CONTROLS-R1.json'


def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

class DinosaurCollectorDerivedEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(S.read_text());cls.q=json.loads(Q.read_text());cls.c=json.loads(C.read_text())
        cls.script=cls.d['source_script'];cls.events=cls.script['events']

    def test_existing_indices_and_entire_history_immutability(self):
        self.assertEqual(self.d['existing_indices'][0]['git_blob'],gitblob(Q.read_bytes()))
        self.assertEqual(self.d['existing_indices'][1]['git_blob'],gitblob(C.read_bytes()))
        self.assertEqual(self.d['initial_remote']['preserved_CURRENT_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual((self.d['dedupe']['QUEST01_indexed_original_scripts'],self.d['dedupe']['QUEST01_indexed_original_TYPE']),(295,1349))
        self.assertEqual((self.d['dedupe']['new_original_script_files'],self.d['dedupe']['new_original_TYPE_sections']),(0,0))

    def test_all_eight_original_sections_preexist_without_counter_inflation(self):
        old=[x for x in self.q['source_event_blocks'] if x['script_path']==self.script['path']]
        self.assertEqual(len(old),len(self.events))
        self.assertEqual(len(old),8)
        for o,e in zip(old,self.events,strict=True):
            self.assertEqual(e['ordinal'],o['script_block_ordinal'])
            self.assertEqual((e['section_sha256'],e['condition_sha256'],e['event_no'],e['type'],e['source_type_line']),
                (o['source_section_decoded_cp950_normalized_UTF8_sha256'],
                 o['condition_expression_decoded_cp950_UTF8_sha256'],o['event_number'],o['raw_type'],o['source_type_line']))
        self.assertEqual([e['event_no'] for e in self.events],[35,-1,-1,35,-1,-1,-1,-1])

    def test_three_source_files_and_create_range_not_single_spawn(self):
        old={row[0]:row for row in self.c['source_files']}
        for f in self.d['source_files']:
            self.assertEqual((f['bytes'],f['sha256'],f['crc32']),tuple(old[f['path']][1:4]))
        c=self.d['source_NPC_create']
        original=next(r for r in self.c['create_rows'] if r[0]==c['file'] and r[1]==c['ordinal'])
        self.assertEqual((c['source_block_sha256'],c['floor'],c['source_borncorner_four_integers'],c['original_graphic_alias']),
            (original[4],original[5],original[7],original[6]))
        self.assertEqual(c['source_script'],original[15][0][0])
        self.assertTrue(c['range_not_proven_single_spawn_point'])
        self.assertEqual(c['source_borncorner_four_integers'],[230,180,525,200])
        self.assertEqual(c['original_functionset'],'ExChangeMan')

    def test_first_reward_preserves_pet_constraints_and_flag35(self):
        e=self.events[0]
        self.assertEqual(e['condition_literal'],'LV>0&PET=25-221*1&PET=25-222*1&ITEM=2607&NOWEV=35')
        self.assertEqual(e['commands']['DelPet'],['PET=25-221*1,PET=25-222*1'])
        self.assertEqual((e['commands']['DelItem'],e['commands']['GetPet'],e['commands']['EndSetFlg']),(['2607'],['93'],['35']))
        self.assertTrue(self.d['original_variants_and_uncertainties']['first_reward_has_EndSetFlg35'])

    def test_second_reward_cannot_rewrite_evdel_or_comma(self):
        e=self.events[4]
        self.assertEqual(e['commands']['GetPet'],['341'])
        self.assertEqual(e['commands']['DelPet'],['EVDEL'])
        self.assertEqual(e['condition_literal'].count(','),1)
        self.assertNotIn('EndSetFlg',e['commands'])
        self.assertTrue(self.d['original_variants_and_uncertainties']['second_run_original_DelPet_is_EVDEL'])
        self.assertFalse(self.d['original_variants_and_uncertainties']['original_DelPet_EVDEL_interpreted_as_specific_pets'])

    def test_two_intake_steps_preserve_different_pet_pairs(self):
        self.assertEqual(self.events[2]['commands']['DelPet'],['PET=25-223*1,PET=25-224*1'])
        self.assertEqual(self.events[6]['commands']['DelPet'],['PET=25-291*1,PET=25-294*1'])
        self.assertEqual(self.events[2]['commands']['GetItem'],['2607'])
        self.assertEqual(self.events[6]['commands']['GetItem'],['2607'])
        self.assertNotEqual(self.events[2]['condition_literal'],self.events[6]['condition_literal'])
        self.assertFalse(self.d['original_variants_and_uncertainties']['original_PET25_minus_ID_encoding_interpreted_as_verified_level_or_species'])

    def test_item2607_two_original_rows_and_cross_source_role_discrepancy(self):
        idx={row[0]:row for n in range(1,8) for row in json.loads((REC/'item-module-01'/f'STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json').read_text())['rows']}
        item=self.d['source_2607_item_row']
        self.assertEqual(item['item_ID'],2607)
        self.assertEqual([x['sha256'] for x in item['original_two_94_column_rows']],idx[2607][1:3])
        self.assertEqual([x['image_alias'] for x in item['original_two_94_column_rows']],[22102,22102])
        self.assertEqual(item['source_record_discrepancy'],'NPC_SOURCE_CALLS_CAPTURE_PROOF_ITEMSET_NAMES_RING')
        self.assertFalse(item['mismatch_cause_known'])
        self.assertFalse(item['dialogue_name_and_itemset_source_name_assumed_identical'])

    def test_prior_world21_instance_to_template_relationship(self):
        prior={r['source_GetPet_operand']:r for r in self.d['prior_WORLD21_existing_GetPet_instances']}
        self.assertEqual({i:(v['prior_template_id'],v['prior_template_graphic_alias']) for i,v in prior.items()},
                         {93:(171,100319),341:(274,100362)})
        for x in prior.values():self.assertTrue(x['original_enemy_instance_not_template_id'])
        if W.exists():
            self.assertEqual(gitblob(W.read_bytes()),self.d['prior_WORLD21_git_blob'])
            world=json.loads(W.read_text())
            lookup={r['getpet_integer']:r for r in world['original_enemy_instance_to_template_lookups']}
            for i,v in prior.items():
                self.assertEqual((lookup[i]['template_id_via_enemy_field4'],lookup[i]['original_template_graphic_id']),
                                 (v['prior_template_id'],v['prior_template_graphic_alias']))

    def test_quest09_has_other_seimu_sources_not_same_script(self):
        old=set(self.d['dedupe']['QUEST09_existing_seimu_scripts'])
        self.assertEqual(old,{'seimu/event/event01_1','seimu/event/event01_2'})
        self.assertNotIn(self.script['path'],old)
        if Q09.exists():
            j=json.loads(Q09.read_text())
            self.assertIn('seimu/event/event01_1',json.dumps(j))
            self.assertIn('seimu/event/event01_2',json.dumps(j))
            self.assertNotIn(self.script['path'],json.dumps(j))

    def test_missing_dat_is_collection_scoped_not_claim_of_original_absence(self):
        m=self.d['prior_QUEST05_map_floor100']
        self.assertEqual((m['source_floor_id'],m['existing_source_MAP_status']),(100,'NO_MATCHING_DAT_IN_955'))
        self.assertTrue(m['no_matching_DAT_in_this_collection_not_proof_original_floor_absent'])
        if M.exists():
            self.assertEqual(gitblob(M.read_bytes()),m['prior_QUEST05_git_blob'])
            j=json.loads(M.read_text())
            self.assertEqual(next(x['map_status'] for x in j['floors'] if x['source_floor_id']==100),m['existing_source_MAP_status'])

    def test_source_boundaries_and_gate_status_untouched(self):
        for k,v in self.d['boundaries'].items():
            self.assertEqual(v,'UNRESOLVED' if k=='original_task_origin' else False)
        self.assertEqual(self.d['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.d['stage_B'],self.d['wiki'],self.d['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(self.d['overall_percent'])

if __name__=='__main__':unittest.main()