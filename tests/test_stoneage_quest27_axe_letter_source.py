"""Source-bounded axe-letter chain and item drop-flag evidence."""
import json
import unittest

from tools.stoneage_quest27_axe_letter_source import OUTPUT, CREATE, SCRIPTS, QUEST01, CHAR01, Q05, WORLD23, load
from tools.stoneage_itemset_schema_probe import SCHEMA


class AxeLetterSourceEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(OUTPUT.read_text());cls.q=load(QUEST01);cls.ch=load(CHAR01)
        cls.scripts={s['path']:s for s in cls.r['source_scripts']}

    def test_original_four_files_and_reversed_CREATE_script_order_remain_exact(self):
        files={r[0]:r for r in self.ch['source_files']}
        self.assertEqual(len(self.r['source_manifest']),4)
        for s in self.r['source_manifest']:self.assertEqual((s['bytes'],s['sha256'],s['crc32']),tuple(files[s['path']][1:4]))
        rows={r[1]:r for r in self.ch['create_rows'] if r[0]==CREATE}
        for c in self.r['source_creates']:
            row=rows[c['create_ordinal']]
            self.assertEqual((c['block_sha256'],c['floor'],c['borncorner'],c['graphic_alias'],c['direction']),
                             (row[4],row[5],row[7],row[6],row[10]))
            self.assertEqual(c['script_path'],row[15][0][0]);self.assertEqual(c['functionset'],'ExChangeMan')
        self.assertEqual([c['script_path'] for c in self.r['source_creates']],list(reversed(SCRIPTS)))
        self.assertEqual([c['floor'] for c in self.r['source_creates']],[1400,1300])

    def test_five_sections_preserve_exact_old_QUEST01_hashes_and_physical_order(self):
        old={(b['script_path'],b['script_block_ordinal']):b for b in self.q['source_event_blocks']}
        for p,s in self.scripts.items():
            for e in s['events']:
                b=old[p,e['ordinal']]
                self.assertEqual(e['section_sha256'],b['source_section_decoded_cp950_normalized_UTF8_sha256'])
                self.assertEqual(e['condition_sha256'],b['condition_expression_decoded_cp950_UTF8_sha256'])
        self.assertEqual([e['event_no'] for e in self.scripts[SCRIPTS[0]]['events']],[3,5])
        self.assertEqual([e['event_no'] for e in self.scripts[SCRIPTS[1]]['events']],[5,3,-1])
        self.assertEqual(self.r['existing_QUEST01_TYPE_sections'],5);self.assertEqual(self.r['new_original_script_discoveries'],0)
        self.assertTrue(all(n>0 for n in self.r['existing_WORLD23_mentions_in_serialized_report'].values()))

    def test_item_and_flag_links_form_the_original_four_step_contract(self):
        steps=self.r['source_item_and_flag_link_order']
        self.assertEqual([(s['script_path'],s['event_ordinal'],s['event_no'],s['source_create_ordinal']) for s in steps],
                         [(SCRIPTS[1],1,3,0),(SCRIPTS[0],0,3,1),(SCRIPTS[0],1,5,1),(SCRIPTS[1],0,5,0)])
        self.assertEqual([s['condition_literal'] for s in steps],['LV>0','NOWEV=3&ITEM=2416','ENDEV=3','NOWEV=5&ITEM=2423'])
        self.assertEqual([s['commands'] for s in steps],[{'GetItem':['2416']},{'DelItem':['2416'],'EndSetFlg':['3']},
            {'GetItem':['2423']},{'GetItem':['2448'],'DelItem':['2423'],'EndSetFlg':['5']}])
        self.assertEqual([s['source_floor'] for s in steps],[1400,1300,1300,1400])

    def test_final_message_retains_comma_instead_of_requiring_both_flags(self):
        e=self.scripts[SCRIPTS[1]]['events'][2]
        self.assertEqual((e['type'],e['condition_literal'],e['commands']),('MESSAGE','ENDEV=3,ENDEV=5',{}))
        self.assertFalse(self.r['boundaries']['comma_condition_interpreted'])

    def test_six_item_rows_match_both_canonical_tables_and_preserve_shared_axe_art(self):
        public={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        self.assertEqual([i['item_ID'] for i in self.r['source_items']],[2416,2423,2448])
        for item in self.r['source_items']:
            self.assertEqual([r['sha256'] for r in item['source_rows']],public[item['item_ID']][1:3])
        a,letter,reward=self.r['source_items']
        self.assertEqual((a['cross_carrier_candidate_alias'],a['candidate_PNG_sha256']),
                         (reward['cross_carrier_candidate_alias'],reward['candidate_PNG_sha256']))
        self.assertNotEqual(a['source_rows'][0]['sha256'],reward['source_rows'][0]['sha256'])

    def test_original_column79_difference_is_not_promoted_to_a_native_drop_test(self):
        self.assertEqual((SCHEMA[78],SCHEMA[79]),(('dropatlogout','bool'),('vanishatdrop','bool')))
        fields=self.r['source_drop_field_values'];self.assertEqual(len(fields),6)
        self.assertEqual([r['column78_dropatlogout'] for r in fields],[0]*6)
        self.assertEqual([r['column79_vanishatdrop'] for r in fields],[1,1,1,1,0,0])
        for r in fields:self.assertTrue(r['named_by_existing_descendant94_schema']);self.assertFalse(r['original_loader_or_drop_executed'])
        self.assertFalse(self.r['boundaries']['source_dialogue_claim_treated_as_actual_drop_observation'])

    def test_map_qualification_is_reused_without_cross_source_native_scene_claim(self):
        old=[r for r in load(Q05)['floors'] if r['source_floor_id'] in (1300,1400)]
        self.assertEqual(self.r['source_map_metadata_reused'],old)
        self.assertFalse(self.r['boundaries']['original_DAT_or_NPC_sprite_replayed'])

    def test_all_native_and_official_boundaries_and_stage_gates_remain_open(self):
        for k,v in self.r['boundaries'].items():self.assertEqual(v,'UNRESOLVED' if k=='quest_origin' else False)
        self.assertEqual(self.r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.r['stage_B'],self.r['wiki'],self.r['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(self.r['overall_percent'])


if __name__=='__main__':unittest.main()
