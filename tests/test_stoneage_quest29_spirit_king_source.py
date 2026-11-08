"""Public derived-evidence acceptance for QUEST29; original bytes are never CI inputs."""
import json
from collections import Counter
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'
REPORT=REC/'STONEAGE-QUEST29-SPIRIT-KING-EVENT69-SOURCE-R1.json'
QUEST01=REC/'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
CHAR01=REC/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'

class KingEvent69OriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(REPORT.read_text('utf8'))
        cls.q=json.loads(QUEST01.read_text('utf8'))
        cls.ch=json.loads(CHAR01.read_text('utf8'))
        cls.old_files={row[0]:row for row in cls.ch['source_files']}

    def test_deduped_295_scripts_1349_events_14_path_groups(self):
        d=self.d['quest_module_dedupe'];q=self.q
        self.assertEqual((d['whole_QUEST01_source_script_paths'],d['whole_QUEST01_source_TYPE_blocks']),
                         (len(q['source_scripts']),len(q['source_event_blocks'])))
        self.assertEqual((len(q['source_scripts']),len(q['source_event_blocks'])),(295,1349))
        grouped=Counter(x['path'].rsplit('/',1)[0] for x in q['source_scripts'])
        self.assertEqual(len(grouped),14)
        self.assertEqual({x['path']:x['source_scripts'] for x in d['original_directory_groups_not_number_of_distinct_quests']},dict(grouped))
        self.assertEqual(sum(x['TYPE_blocks'] for x in d['original_directory_groups_not_number_of_distinct_quests']),1349)
        self.assertEqual((d['existing_QUEST01_295_script_index'],d['existing_QUEST01_event_blocks']), (13,71))
        self.assertEqual((d['new_original_scripts_discovered_this_package'],d['new_original_event_sections_discovered_this_package']),(0,0))

    def test_all_36_original_file_metadata_only_and_full_source_sha(self):
        self.assertEqual(len(self.d['full_original_source_manifest']),36)
        for r in self.d['full_original_source_manifest']:
            self.assertEqual((r['bytes'],r['sha256'],r['crc32']),tuple(self.old_files[r['path']][1:4]))
            self.assertRegex(r['sha256'],r'^[a-f0-9]{64}$')

    def test_exact_25_create_ordinals_template_reference_and_floor(self):
        rows={(r[0],r[1]):r for r in self.ch['create_rows']}
        cs=self.d['source_creates'];self.assertEqual(len(cs),25)
        self.assertEqual(Counter(x['create_path'] for x in cs),
                         {'king/event69_alpha.create':24,'giiru/event/event30.create':1})
        templates={(x[0],x[1]):x for x in self.ch['template_rows']}
        for c in cs:
            x=rows[(c['create_path'],c['create_ordinal'])]
            self.assertEqual((c['source_block_sha256'],c['source_byte_span'],c['floor'],c['borncorner'],c['direction'],c['graphic_alias']),
                (x[4],[x[2],x[3]],x[5],x[7],x[10],x[6]))
            self.assertEqual((c['source_parameter_path'],c['source_parameter_sha256']),
                             (x[15][0][0],x[15][0][2]))
            self.assertEqual((c['template_path'],c['template_ordinal']),tuple(x[13][0]))
            self.assertEqual(c['template_functionset'],templates[tuple(x[13][0])][4])
        self.assertEqual(len(self.d['source_scene_floors']),20)

    def test_13_source_scripts_and_71_event_sections_are_previously_indexed(self):
        s=self.d['source_event_scripts'];self.assertEqual(len(s),13)
        old={x['path']:x for x in self.q['source_scripts']}
        old_blocks={(x['script_path'],x['script_block_ordinal']):x for x in self.q['source_event_blocks']}
        self.assertEqual(sum(len(x['events']) for x in s),71)
        for x in s:
            self.assertTrue(x['path'].startswith('king/event69_'))
            self.assertEqual((x['bytes'],x['sha256'],x['crc32']),
                             (old[x['path']]['original_size'],old[x['path']]['original_sha256'],old[x['path']]['original_crc32']))
            for e in x['events']:
                b=old_blocks[(x['path'],e['ordinal'])]
                self.assertEqual((e['source_type_line'],e['section_sha256'],e['condition_sha256'],e['type'],e['event_no']),
                    (b['source_type_line'],b['source_section_decoded_cp950_normalized_UTF8_sha256'],
                     b['condition_expression_decoded_cp950_UTF8_sha256'],b['raw_type'],b['event_number']))
                self.assertTrue(e['exact_EventEnd_found'])
        self.assertEqual(self.d['source_event_totals']['types'],{'ACCEPT':24,'MESSAGE':44,'REQUEST':3})

    def test_48_item_ids_96_rows_link_item01_7_shards(self):
        rows={}
        for i in range(1,8):
            d=json.loads((REC/f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json').read_text('utf8'))
            for r in d['rows']:
                self.assertNotIn(r[0],rows);rows[r[0]]=r
        items=self.d['source_items'];self.assertEqual(len(items),48)
        self.assertEqual(self.d['item_source_coverage']['original_94column_rows'],96)
        for i in items:
            self.assertEqual(len(i['source_rows']),2)
            r=rows[i['item_ID']]
            self.assertEqual([x['sha256'] for x in i['source_rows']],r[1:3])
            self.assertEqual([x['source_image_alias'] for x in i['source_rows']],r[3:5])
            self.assertEqual(i['original_rows_identical'],r[1]==r[2])

    def test_item_bitmap_gap_is_not_misread_as_deleted_content(self):
        items=self.d['source_items'];coverage=self.d['item_source_coverage']
        yes=[x for x in items if x['cross_carrier_TW1_candidate']]
        no=[x['item_ID'] for x in items if not x['cross_carrier_TW1_candidate']]
        self.assertEqual(len(yes),5)
        self.assertEqual(len(no),43)
        self.assertEqual(no,coverage['missing_TW1_candidate_item_IDs'])
        self.assertEqual(coverage['cross_carrier_TW1_qualified_IDs'],5)
        self.assertEqual(coverage['source_image_aliases'],len(set(x['cross_carrier_alias'] for x in items)))
        for x in yes:self.assertRegex(x['candidate_PNG_sha256'],r'^[0-9a-f]{64}$')
        for x in items:
            if not x['cross_carrier_TW1_candidate']:self.assertNotIn('candidate_PNG_sha256',x)

    def test_source_pets_are_integer_literals_not_redeemed_rewards(self):
        pet=self.d['source_original_control_exceptions']['first_person_pet_directions']
        self.assertEqual(sorted(int(x['GetPet_literal']) for x in pet),[355,484,1479])
        self.assertEqual(len(pet),3)
        self.assertFalse(self.d['boundaries']['GetPet_original_reward_transaction_executed'])
        self.assertFalse(self.d['boundaries']['GETPET_355_484_1479_called_same_as_pets'])

    def test_original_delitem_trailing_comma_and_joint_flag_are_not_repaired(self):
        s=self.d['source_original_control_exceptions']
        self.assertEqual(len(s['long_trailing_comma_delitem']),1)
        self.assertTrue(s['long_trailing_comma_delitem'][0]['DelItem_literal'].endswith(','))
        self.assertEqual(s['long_trailing_comma_delitem'][0]['script'],'king/event69_11')
        self.assertTrue(any(x['EndSetFlg_literal']=='122,123' for x in s['raw_comma_separated_endset']))
        self.assertFalse(self.d['boundaries']['original_event_punctuation_interpreted'])

    def test_five_random_lists_keep_duplicate_positions_and_unknown_weights(self):
        records=self.d['source_original_control_exceptions']['raw_random_lists']
        self.assertEqual(len(records),5)
        nine=[x for x in records if len(x['GetRandItem_literal'].split(','))==9]
        self.assertEqual(len(nine),4)
        self.assertTrue(all(x['original_order_includes_duplicates'] for x in nine))
        self.assertFalse(self.d['boundaries']['original_random_probabilities_inferred'])
        self.assertFalse(self.d['boundaries']['original_native_game_executed'])

    def test_official_source_and_private_copyright_safety_gates(self):
        d=self.d
        self.assertEqual(d['verified_source_bundles']['NPC_total_members_SHA_CRC_verified'],2205)
        self.assertEqual(d['verified_source_bundles']['ITEM_total_members_CRC_verified'],838)
        self.assertFalse(d['verified_source_bundles']['parent_mixed25_RAR_reread'])
        self.assertEqual(d['old_index_pins'][0]['git_blob'],'52db8b4b6cd43cd2afa4a8d2e8460f214933f5e2')
        self.assertEqual(d['old_index_pins'][1]['git_blob'],'a088b61a3212f7049e7793f587123ffb29bebad7')
        self.assertTrue(d['quest_module_dedupe']['earlier_CN25_R113_story_is_media_narrative_not_original_NPC_source'])
        self.assertEqual(d['stage_A'],{'PARTIAL':7,'OPEN':2})
        self.assertEqual((d['stage_B'],d['wiki'],d['R79']),('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(d['overall_percent'])
        self.assertEqual(d['boundaries']['source_family_origin'],'UNRESOLVED')
        for k,v in d['boundaries'].items():
            if k!='source_family_origin':self.assertIs(v,False)

if __name__=='__main__':unittest.main()
