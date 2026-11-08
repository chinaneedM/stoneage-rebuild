"""Accept source links without executing private assets or original conditions."""
import json
import unittest

from tools.stoneage_quest26_shell_flower_source import OUTPUT, CREATE, SCRIPTS, QUEST01, CHAR01, Q05, Q24, Q25, load
from tools.stoneage_quest17_dino_ranch_source import sha


class ShellFlowerFlag2Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(OUTPUT.read_text()); cls.q=load(QUEST01); cls.ch=load(CHAR01)
        cls.scripts={s['path']:s for s in cls.r['source_scripts']}

    def test_four_original_files_and_two_configs_match_existing_source_catalogue(self):
        index={r[0]:r for r in self.ch['source_files']}
        self.assertEqual({f['path'] for f in self.r['source_manifest']}, {CREATE,*SCRIPTS,'jaruga/event/event.template'})
        for f in self.r['source_manifest']:
            self.assertEqual((f['bytes'],f['sha256'],f['crc32']),tuple(index[f['path']][1:4]))
        old={r[1]:r for r in self.ch['create_rows'] if r[0]==CREATE}
        for c in self.r['source_creates']:
            row=old[c['create_ordinal']]
            self.assertEqual((c['block_sha256'],c['floor'],c['graphic_alias'],c['borncorner'],c['borncenter'],c['direction']),
                             (row[4],row[5],row[6],row[7],row[8],row[10]))
            self.assertEqual(c['script_path'],row[15][0][0]);self.assertEqual(c['functionset'],'ExChangeMan')
        self.assertEqual([c['floor'] for c in self.r['source_creates']],[2000,1000])
        self.assertEqual([c['borncorner'] for c in self.r['source_creates']],[[55,92,55,92],[57,124,57,124]])

    def test_six_existing_sections_are_full_old_source_not_new_original_discovery(self):
        old={(b['script_path'],b['script_block_ordinal']):b for b in self.q['source_event_blocks']}
        for path,s in self.scripts.items():
            self.assertEqual([e['type'] for e in s['events']],['CLEAN','ACCEPT','REQUEST'])
            self.assertEqual([e['event_no'] for e in s['events']],[-1,2,2])
            for e in s['events']:
                b=old[path,e['ordinal']]
                self.assertEqual(e['section_sha256'],b['source_section_decoded_cp950_normalized_UTF8_sha256'])
                self.assertEqual(e['condition_sha256'],b['condition_expression_decoded_cp950_UTF8_sha256'])
                self.assertEqual(e['condition_sha256'],sha(e['condition_literal'].encode()))
                self.assertTrue(e['exact_EventEnd_found'])
        self.assertEqual(self.r['existing_QUEST01_TYPE_sections'],6)
        self.assertEqual(self.r['new_original_script_discoveries'],0)

    def test_CLEAN_flags_and_SP_groups_preserve_both_original_comma_conditions(self):
        expected=[('ENDEV=2&ITEM!=2414&SP=0,ENDEV=2&ITEM!=2414&SP=3',[0,3]),
                  ('ENDEV=2&ITEM!=2415&SP=1,ENDEV=2&ITEM!=2415&SP=2',[1,2])]
        for path,(condition,sp) in zip(SCRIPTS,expected,strict=True):
            e=self.scripts[path]['events'][0]
            self.assertEqual(e['condition_literal'],condition);self.assertEqual(e['source_SP_literals_in_order'],sp)
            self.assertEqual(e['commands'],{'CleanFlg':['2']})
        self.assertEqual(len(self.r['source_flag2_controls']),4)
        self.assertEqual([c['field'] for c in self.r['source_flag2_controls']],['CleanFlg','EndSetFlg']*2)

    def test_two_accepts_exchange_opposite_items_and_set_same_flag(self):
        for path,incoming,outgoing in zip(SCRIPTS,[2415,2414],[2414,2415],strict=True):
            e=self.scripts[path]['events'][1]
            self.assertEqual(e['condition_literal'],f'NOWEV=2&ITEM={incoming}')
            self.assertEqual(e['commands'],{'GetItem':[str(outgoing)],'DelItem':[str(incoming)],'EndSetFlg':['2']})
            self.assertEqual(e['source_SP_literals_in_order'],[])
        self.assertEqual(self.r['old_QUEST01_flag2_setters'],[
            {'script_path':b['script_path'],'event_ordinal':b['script_block_ordinal'],
             'section_sha256':b['source_section_decoded_cp950_normalized_UTF8_sha256']}
            for b in self.q['source_event_blocks'] if 2 in b['end_set_flags']])

    def test_requests_keep_distinct_SP_literals_and_bare_item_amounts(self):
        for path,item,condition,sp in zip(SCRIPTS,[2414,2415],
                ['LV>0&SP=1,LV>0&SP=2','LV>0&SP=0,LV>0&SP=3'],[[1,2],[0,3]],strict=True):
            e=self.scripts[path]['events'][2]
            self.assertEqual(e['condition_literal'],condition);self.assertEqual(e['source_SP_literals_in_order'],sp)
            self.assertEqual(e['commands'],{'GetItem':[str(item)]})

    def test_tour_flag2_joins_cover_exact_39_old_consumers_not_flags20_or28(self):
        old=load(Q25);expected=[]
        for s in old['source_scripts']:
            for e in s['events']:
                tokens=e['condition_literal'].replace('&',',').split(',')
                if 'ENDEV=2' in tokens:
                    expected.append(dict(script_path=s['path'],event_ordinal=e['ordinal'],type=e['type'],
                                         condition_literal=e['condition_literal'],section_sha256=e['section_sha256']))
        self.assertEqual(self.r['existing_QUEST25_ENDEV2_consumers'],expected);self.assertEqual(len(expected),39)
        self.assertEqual(len({e['script_path'] for e in expected}),16)
        self.assertNotIn('sainasu/event/oev_0cd',{e['script_path'] for e in expected})

    def test_shell_links_reuse_Poru_gates_and_alternative_grant_without_sole_source_claim(self):
        old=load(Q24)
        self.assertEqual(self.r['existing_QUEST24_same_item2414_gates'],old['actual_source_warpman_parameters'])
        self.assertEqual(self.r['existing_QUEST24_alternative_item2414_grant'],old['meat_shell_source'])
        for g in self.r['existing_QUEST24_same_item2414_gates']:
            self.assertEqual(g['source_values']['FREE'],'ITEM=2414')
        self.assertEqual(self.r['existing_QUEST24_alternative_item2414_grant']['commands']['GetItem'],['2414'])

    def test_both_original_item_table_rows_and_existing_shell_icon_match_prior_evidence(self):
        public={r[0]:r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        self.assertEqual([x['item_ID'] for x in self.r['source_items']],[2414,2415])
        for item in self.r['source_items']:
            for col,row in enumerate(item['source_rows'],1):self.assertEqual(row['sha256'],public[item['item_ID']][col])
        old=next(x for x in load(Q24)['core_items'] if x['item_ID']==2414)
        self.assertEqual(self.r['source_items'][0]['candidate_PNG_sha256'],old['candidate_PNG_sha256'])
        self.assertEqual(self.r['source_items'][0]['original_RD_sha256'],old['original_RD_sha256'])

    def test_map_statuses_preserve_missing_and_unqualified_source_gaps(self):
        old=[m for m in load(Q05)['floors'] if m['source_floor_id'] in (1000,2000)]
        self.assertEqual(self.r['source_map_metadata_reused'],old)
        self.assertEqual([m['map_status'] for m in old],['NO_MATCHING_DAT_IN_955','DAT_PRESENT_GT99_QUALIFIED_RD_MISSING'])

    def test_source_relations_never_promote_runtime_deployment_or_completion(self):
        for k,v in self.r['boundaries'].items():self.assertEqual(v,'UNRESOLVED' if k=='quest_origin' else False)
        self.assertEqual(self.r['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.r['stage_B'],self.r['wiki'],self.r['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(self.r['overall_percent'])


if __name__=='__main__':
    unittest.main()
