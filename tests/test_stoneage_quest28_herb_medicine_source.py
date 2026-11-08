"""QUEST28: verify public, version-bounded derived original-content evidence.

No proprietary NPC text, DAT bytes, image pixels, or native gameplay runtime is
needed in CI. Private source-byte checks are recorded separately in the dossier.
"""
from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research' / 'recovered'
REPORT = 'STONEAGE-QUEST28-HERB-MEDICINE-FOUR-SCENES-SOURCE-R1.json'
QUEST01 = 'STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json'
CHAR01 = 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
SCRIPTS = (
    'jaruga/event/event01_1', 'jaruga/event/event01_2',
    'sainasu/event/nevent02_2', 'sainasu/event/nevent02_3',
    'sainasu/event/nevent02_4',
)


def read(name):
    return json.loads((REC / name).read_text(encoding='utf-8'))


class Quest28DerivedOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = read(REPORT)
        cls.q = read(QUEST01)
        cls.ch = read(CHAR01)

    def test_pins_are_exact_existing_public_blobs(self):
        # Do not accept stale or substituted public material as an old evidence input.
        for pin in self.r['old_evidence_inputs']:
            raw = (ROOT / pin['path']).read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            self.assertEqual((len(raw), hashlib.sha256(raw).hexdigest(), blob),
                             (pin['bytes'], pin['sha256'], pin['git_blob']))
        self.assertEqual(self.r['initial_remote']['preserved_CURRENT_blob'],
                         'c89e0e33537990aa2132b47c40fef49a985a935c')

    def test_five_scripts_and_fifteen_sections_not_new_files(self):
        old_scripts = {x['path']: x for x in self.q['source_scripts']}
        old_events = {(x['script_path'], x['script_block_ordinal']): x
                      for x in self.q['source_event_blocks']}
        self.assertEqual([x['path'] for x in self.r['source_scripts']], list(SCRIPTS))
        self.assertEqual([len(x['events']) for x in self.r['source_scripts']], [3, 4, 3, 2, 3])
        self.assertEqual((self.r['old_QUEST01_TYPE_sections'],
                          self.r['new_original_script_discoveries']), (15, 0))
        for src in self.r['source_scripts']:
            old = old_scripts[src['path']]
            self.assertEqual((src['bytes'], src['sha256'], src['crc32']),
                             (old['original_size'], old['original_sha256'], old['original_crc32']))
            for event in src['events']:
                prior = old_events[(src['path'], event['ordinal'])]
                self.assertEqual((event['event_no'], event['type'], event['section_sha256'],
                                  event['condition_sha256']),
                                 (prior['event_number'], prior['raw_type'],
                                  prior['source_section_decoded_cp950_normalized_UTF8_sha256'],
                                  prior['condition_expression_decoded_cp950_UTF8_sha256']))
                self.assertTrue(event['exact_EventEnd_found'])

    def test_original_creates_and_template_are_real_joins(self):
        rows = {(row[0], row[1]): row for row in self.ch['create_rows']}
        sources = {row[0]: row for row in self.ch['source_files']}
        templates = {(row[0], row[1]): row for row in self.ch['template_rows']}
        self.assertEqual(len(self.r['source_manifest']), 8)
        for f in self.r['source_manifest']:
            self.assertEqual((f['bytes'], f['sha256'], f['crc32']),
                             tuple(sources[f['path']][1:4]))
        self.assertEqual(len(self.r['source_creates']), 7)
        for c in self.r['source_creates']:
            row = rows[(c['create_path'], c['create_ordinal'])]
            self.assertEqual((c['block_sha256'], c['floor'], c['graphic_alias'],
                              c['borncorner'], c['direction']),
                             (row[4], row[5], row[6], row[7], row[10]))
            self.assertEqual(row[15][0][0], c['script_path'])
            self.assertEqual(row[13][0], [c['template_path'], c['template_ordinal']])
            self.assertEqual(templates[(c['template_path'], c['template_ordinal'])][4],
                             c['functionset'])
            self.assertEqual(c['functionset'], 'ExChangeMan')

    def test_six_static_relations_keep_numeric_control_and_original_order(self):
        events = {(src['path'], e['ordinal']): e
                  for src in self.r['source_scripts'] for e in src['events']}
        rel = self.r['source_relations']
        self.assertEqual(len(rel), 6)
        for r in rel:
            event = events[(r['script_path'], r['event_ordinal'])]
            self.assertEqual((r['condition_literal'], r['commands'], r['section_sha256']),
                             (event['condition_literal'], event['commands'], event['section_sha256']))
        self.assertEqual(rel[0]['commands'],
                         {'GetItem': ['2427'], 'DelItem': ['2401'], 'EndSetFlg': ['1']})
        self.assertEqual(rel[1]['commands'], {'GetItem': ['1984'], 'DelItem': ['1983*1']})
        self.assertEqual(rel[2]['condition_literal'],
                         'NOWEV=1&ITEM!=2401,NOWEV=87&ITEM!=2401,ENDEV=87&ITEM!=2401')
        self.assertEqual(rel[3]['condition_literal'], 'LV>0&ITEM=2446*10')
        self.assertEqual(rel[3]['commands'], {'GetItem': ['2449'], 'DelItem': ['2446']})
        self.assertEqual(rel[4]['commands'], {'GetItem': ['1264'], 'DelItem': ['2449*1']})
        self.assertEqual(rel[5]['commands'], {'GetItem': ['2447']})

    def test_quantity_and_version_divergence_not_silently_fixed(self):
        self.assertTrue(self.r['bone_recipe_quantity_mismatch']['omitted_DelItem_quantity_not_replaced_with_ten'])
        self.assertEqual(self.r['bone_recipe_quantity_mismatch']['commands']['DelItem'], ['2446'])
        self.assertFalse(self.r['powder_branch']['item1982_deleted_by_this_source_section'])
        self.assertFalse(self.r['herb_grant']['all_conditions_flattened_to_event1'])
        self.assertTrue(self.r['harp_keyword']['missing_nevent02_1_in_source_NPC_subtree'])
        self.assertFalse(self.r['harp_keyword']['harp_trigger_or_bone_drop_recovered'])
        self.assertFalse(self.r['harp_keyword']['answer_original_text_published'])

    def test_nine_items_preserve_two_original_rows_and_image_gaps(self):
        public = {row[0]: row
                  for i in range(1, 8)
                  for row in read(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{i:02d}-R1.json')['rows']}
        self.assertEqual([x['item_ID'] for x in self.r['source_items']],
                         [1264, 1982, 1983, 1984, 2401, 2427, 2446, 2447, 2449])
        self.assertEqual(len(self.r['source_item_control_columns']), 18)
        for x in self.r['source_items']:
            self.assertEqual([v['sha256'] for v in x['source_rows']],
                             public[x['item_ID']][1:3])
            for v in x['source_rows']:
                self.assertEqual(v['image_alias'], x['cross_carrier_candidate_alias'])
                self.assertRegex(v['sha256'], '^[a-f0-9]{64}$')
        missing = [x['item_ID'] for x in self.r['source_items'] if not x['candidate_PNG_sha256']]
        self.assertEqual(missing, [1982, 1984])
        self.assertEqual(len({x['cross_carrier_candidate_alias'] for x in self.r['source_items']
                              if x['candidate_PNG_sha256']}), 7)
        self.assertTrue(all(x['names_from_existing_descendant94_schema'] and
                            x['actual_item_effect_executed'] is False
                            for x in self.r['source_item_control_columns']))

    def test_four_original_maps_and_six_coordinates_are_source_bounded(self):
        scenes = self.r['original_scene_observations']
        self.assertEqual([(s['floor'], s['geometry']) for s in scenes],
                         [(3110, [30, 30]), (20105, [50, 70]),
                          (3305, [30, 30]), (3105, [30, 30])])
        self.assertEqual(sum(len(s['source_points']) for s in scenes), 6)
        self.assertEqual(self.r['distinct_replayed_tile_PNGs'], 439)
        for s in scenes:
            self.assertEqual(s['original_DAT_bytes'], 8 + 6 * s['geometry'][0] * s['geometry'][1])
            self.assertRegex(s['original_DAT_sha256'], '^[a-f0-9]{64}$')
            self.assertTrue(all(len(p['raw_three_u16']) == 3 and not p['original_NPC_sprite_drawn']
                                for p in s['source_points']))
        self.assertEqual(self.r['source_floor3200_map_metadata']['map_status'],
                         'MAP10_GT99_RD_SOURCE_BOUND_LOW_VALUES_OPEN')
        self.assertEqual(self.r['new_original_RD_decodes'], 0)

    def test_no_native_early_official_or_ownership_overclaims(self):
        self.assertEqual(self.r['source_scope'],
                         'MIXED25_COMMUNITY_PRESERVED_NOT_AUTHENTICATED_OFFICIAL_EARLY_BUILD')
        for k, v in self.r['boundaries'].items():
            self.assertEqual(v, 'UNRESOLVED' if k == 'quest_origin' else False)
        self.assertEqual(self.r['stage_A'], {'PARTIAL': 7, 'OPEN': 2})
        self.assertEqual((self.r['stage_B'], self.r['wiki'], self.r['R79']),
                         ('GATED', 'GATED', 'PAUSED_NON_BLOCKING'))
        self.assertIsNone(self.r['overall_percent'])
        self.assertEqual(self.r['next'], 'QUEST29_MODULE_SOURCE_REVIEW_AFTER_MEDICINE_BATCH_STOP')


if __name__ == '__main__':
    unittest.main()
