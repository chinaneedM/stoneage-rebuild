"""Cross-source evidence checks; CI intentionally has no commercial assets."""
from collections import Counter
import json
import unittest

from tools.stoneage_quest25_island_tour_source import OUTPUT, Q05, CREATES, QUEST01, CHAR01, WORLD21, load
from tools.stoneage_quest17_dino_ranch_source import sha


class FourIslandTourEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(OUTPUT.read_text()); cls.q = load(QUEST01); cls.ch = load(CHAR01)
        cls.scripts = {s['path']: s for s in cls.r['source_scripts']}

    def test_original_manifest_and_template_bindings_match_complete_old_catalogue(self):
        old = {r[0]: r for r in self.ch['source_files']}
        self.assertEqual(len(self.r['source_manifest']), 57)
        for f in self.r['source_manifest']:
            self.assertEqual((f['bytes'], f['sha256'], f['crc32']), tuple(old[f['path']][1:4]))
        source = {(r[0], r[1]): r for r in self.ch['create_rows']}
        for c in self.r['source_creates']:
            row = source[c['create_path'], c['create_ordinal']]
            self.assertEqual((c['block_sha256'], c['floor'], c['borncorner'], c['borncenter'], c['direction'], c['graphic_alias']),
                             (row[4], row[5], row[7], row[8], row[10], row[6]))
            self.assertEqual(c['script_path'], row[15][0][0]); self.assertEqual(c['functionset'], 'ExChangeMan')
        self.assertEqual(Counter(c['create_path'] for c in self.r['source_creates']), dict.fromkeys(CREATES, 27))

    def test_all_322_event_sections_are_old_exact_sections_not_new_discoveries(self):
        old = {(b['script_path'], b['script_block_ordinal']): b for b in self.q['source_event_blocks']}
        n = 0
        for s in self.r['source_scripts']:
            for e in s['events']:
                b = old[s['path'], e['ordinal']]; n += 1
                self.assertEqual(e['section_sha256'], b['source_section_decoded_cp950_normalized_UTF8_sha256'])
                self.assertEqual(e['condition_sha256'], sha(e['condition_literal'].encode()))
                self.assertEqual(e['condition_sha256'], b['condition_expression_decoded_cp950_UTF8_sha256'])
                self.assertEqual(e['event_no'], -1); self.assertTrue(e['exact_EventEnd_found'])
        self.assertEqual(n, 322); self.assertEqual(len(self.scripts), 54)
        self.assertEqual(self.r['module_review']['new_original_script_discoveries'], 0)
        self.assertEqual(self.r['module_review']['this_batch_previously_mentioned_in_these_reports'], [])

    def test_four_routes_connect_twelve_distinct_source_stations_without_crossing_proof_sets(self):
        seen = set()
        for route in self.r['routes']:
            first = 2552 if route['label'] in 'AB' else 2575
            self.assertEqual(route['initial_proof_item'], first)
            self.assertEqual(route['final_proof_item'], first + 12)
            self.assertEqual([c['number'] for c in route['checkpoints']], list(range(1, 13)))
            for n, c in enumerate(route['checkpoints']):
                self.assertEqual((c['incoming_item'], c['outgoing_item']), (first + n, first + n + 1))
                p = c['source']['script_path']; self.assertNotIn(p, seen); seen.add(p)
                e = self.scripts[p]['events'][c['event_ordinal']]
                self.assertEqual(e['commands'], {'GetItem': [str(first+n+1)], 'DelItem': [str(first+n)]})
                self.assertEqual(c['condition_literal'], e['condition_literal'])
                self.assertEqual(len(c['keyword_UTF8_sha256']), 64)
                self.assertFalse(c['keyword_raw_text_published'])
            self.assertFalse(route['source_order_is_native_reachability'])
        self.assertEqual(len(seen), 48)

    def test_branch_order_and_condition_asymmetry_are_preserved(self):
        routes = {r['label']: r for r in self.r['routes']}
        for label in 'ABC':
            self.assertEqual({c['event_ordinal'] for c in routes[label]['checkpoints']}, {0})
        self.assertEqual({c['event_ordinal'] for c in routes['D']['checkpoints']}, {1})
        self.assertTrue(all('&ENDEV=17' in c['condition_literal'] for c in routes['C']['checkpoints']))
        self.assertTrue(all('ENDEV' not in c['condition_literal'] for c in routes['D']['checkpoints']))
        self.assertEqual([c['number'] for c in routes['B']['checkpoints'] if 'ENDEV=2' in c['condition_literal']], [1])
        for c in routes['D']['checkpoints']:
            self.assertIn('ENDEV=17', self.scripts[c['source']['script_path']]['events'][0]['condition_literal'])

    def test_initial_registration_and_finish_are_separate_original_NPC_records(self):
        routes = {r['label']: r for r in self.r['routes']}
        self.assertEqual([routes[k]['registration']['floor'] for k in 'ABCD'], [3000,3000,1000,1000])
        self.assertEqual([routes[k]['finish']['floor'] for k in 'ABCD'], [4000,3000,1000,2000])
        for path, initial in [('jaruga/event/oev_0', 2552), ('sainasu/event/oev_0cd', 2575)]:
            requests = [e for e in self.scripts[path]['events'] if e['type'] == 'REQUEST']
            self.assertEqual(len(requests), 2)
            self.assertEqual([e['commands'] for e in requests], [{'GetItem': [str(initial)]}] * 2)
        a = self.scripts['jaruga/event/oev_ed1']['events']
        self.assertEqual([e['condition_literal'] for e in a[:2]], ['LV>0&ITEM=2564', 'LV>0&ITEM=2564&ENDEV=2'])
        self.assertIn('GetPet', a[0]['commands']); self.assertEqual(a[1]['commands'], {})

    def test_original_duplicate_reward_positions_and_nonexplicit_quantities_survive(self):
        b = self.scripts['jaruga/event/oev_edb']['events'][0]['commands']
        self.assertEqual(b['GetPet'], ['338,360,366,482,482,78'])
        self.assertEqual(b['GetRandItem'], ['255,352,769,1062,68,1063,58,68,2565,2566'])
        a = self.scripts['jaruga/event/oev_0']['events'][2]
        self.assertEqual(a['commands']['GetRandItem'], ['12644,12635,12635,12641,12641'])
        self.assertEqual(a['commands']['DelItem'], ['2557,2558,2559,2560,2561,2562,2563'])
        self.assertIn(',', a['condition_literal'])

    def test_pet_instance_lists_reuse_exact_WORLD21_master_relationships(self):
        old = load(WORLD21)
        for s in self.r['existing_WORLD21_pet_sources']:
            self.assertEqual(s, next(x for x in old['source_GetPet_scripts_and_event_blocks'] if x['path']==s['path']))
        ids = {i for s in self.r['existing_WORLD21_pet_sources'] for c in s['commands'] for i in c['raw_integer_tokens_in_order']}
        self.assertEqual(len(ids), 15)
        self.assertEqual(self.r['existing_WORLD21_instance_links'], [r for r in old['original_enemy_instance_to_template_lookups'] if r['getpet_integer'] in ids])

    def test_item_rows_match_both_original_tables_and_allow_shared_candidate_art(self):
        public = {r[0]: r for n in range(1,8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        self.assertEqual(len(self.r['source_items']), 48)
        for item in self.r['source_items']:
            for column, row in enumerate(item['source_rows'], 1):
                self.assertEqual(row['sha256'], public[item['item_ID']][column])
            self.assertIsNotNone(item['cross_carrier_TW1_candidate'])
        self.assertLess(len({x['cross_carrier_TW1_candidate']['alias'] for x in self.r['source_items']}), 48)

    def test_35_floor_statuses_reuse_prior_metadata_without_claiming_DAT_or_world_replay(self):
        old = {r['source_floor_id']: r for r in load(Q05)['floors']}
        floors = self.r['source_map_metadata_reused']; self.assertEqual(len(floors), 35)
        for f in floors: self.assertEqual(f, old[f['source_floor_id']])
        self.assertEqual(sum(f['map_status']=='NO_MATCHING_DAT_IN_955' for f in floors), 7)
        self.assertFalse(self.r['original_DAT_reread']); self.assertEqual(self.r['new_original_RD_decodes'], 0)

    def test_merged_physical_message_is_not_repaired_or_native_promoted(self):
        self.assertEqual(len(self.r['embedded_PetFullMsg_physical_lines']), 1)
        self.assertEqual(self.r['embedded_PetFullMsg_physical_lines'][0]['path'], 'sainasu/event/oev_edd')
        for k, v in self.r['boundaries'].items():
            self.assertEqual(v, 'UNRESOLVED' if k=='quest_origin' else False)
        self.assertEqual(self.r['stage_A'], {'PARTIAL':7,'OPEN':2})
        self.assertEqual((self.r['stage_B'],self.r['wiki'],self.r['R79']), ('GATED','GATED','PAUSED_NON_BLOCKING'))
        self.assertIsNone(self.r['overall_percent'])


if __name__ == '__main__':
    unittest.main()
