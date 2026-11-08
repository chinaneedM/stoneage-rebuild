"""Public derived evidence checks, without access to original commercial assets."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from tools.stoneage_quest21_liuli_source import (
    CORE_ITEMS, CREATE, FILES, GUIDE, MAP04, MAP_CREATE, QUEST01, CHAR01,
    SCRIPTS, OUTPUT, REC, shared_warp_tiles,
)


def load(n):
    return json.loads((REC / n).read_text('utf-8'))


class LiuliOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(OUTPUT.read_text('utf-8'))
        cls.q, cls.ch, cls.m, cls.g = [load(n) for n in [QUEST01, CHAR01, MAP04, GUIDE]]

    def test_01_original_2205_member_manifest_and_previous_input_pins(self):
        files = {x[0]: x for x in self.ch['source_files']}
        self.assertEqual([x['path'] for x in self.r['source_manifest']], FILES)
        for row in self.r['source_manifest']:
            old = files[row['path']]
            self.assertEqual((row['bytes'], row['sha256'], row['crc32']), tuple(old[1:4]))
        for p in self.r['previous_inputs']:
            raw = (REC.parents[1] / p['path']).read_bytes()
            self.assertEqual(len(raw), p['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), p['sha256'])
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(), p['git_blob'])
        self.assertEqual(self.r['private_archive_verification']['NPC_members_CRC_and_full_source_hashes'], 2205)

    def test_02_six_source_creates_are_old_quest01_records(self):
        refs = [x for x in self.q['source_creation_references'] if x['create_source_path'] == CREATE]
        self.assertEqual(len(refs), 6)
        for c, old in zip(self.r['source_creates'], refs, strict=True):
            self.assertEqual((c['ordinal'], c['floor'], c['graphic_alias'], c['script_ref']),
                             (old['create_brace_ordinal'], old['floorid'], old['graphic_alias_numeric'], old['original_script_path']))
        self.assertEqual([c['script_ref'] for c in self.r['source_creates']], SCRIPTS)
        self.assertEqual([c['borncorner'][:2] for c in self.r['source_creates']],
                         [[10, 8], [16, 18], [158, 1005], [13, 9], [13, 8], [13, 10]])

    def test_03_all_22_old_events_and_literal_item_commands(self):
        oldblocks = {(x['script_path'], x['script_block_ordinal']): x for x in self.q['source_event_blocks']}
        count = Counter()
        for script in self.r['source_scripts']:
            for e in script['events']:
                old = oldblocks[(script['path'], e['ordinal'])]
                self.assertEqual((e['event_no'], e['type'], e['condition_sha256'], e['section_sha256']),
                                 (old['event_number'], old['raw_type'], old['condition_expression_decoded_cp950_UTF8_sha256'], old['source_section_decoded_cp950_normalized_UTF8_sha256']))
                count[e['type']] += 1
        self.assertEqual(dict(count), {'ACCEPT': 6, 'MESSAGE': 15, 'REQUEST': 1})
        self.assertEqual(sum(count.values()), self.r['source_event_count'])
        self.assertEqual(self.r['old_QUEST01_event_count'], 22)
        self.assertEqual(self.r['newly_discovered_original_scripts'], 0)
        reward = self.r['source_scripts'][0]['events'][0]
        self.assertEqual(reward['commands'], {'GetItem': ['2701'], 'DelItem': ['2698,2699'], 'EndSetFlg': ['39'], 'Charm': ['1']})
        self.assertEqual(self.r['source_scripts'][1]['events'][1]['condition_literal'], 'LV>0&ENDEV=4')

    def test_04_nine_source_positions_preserve_repeat_and_eight_guide_positions(self):
        row = self.r['son_relocation']
        positions = row['source_target_occurrences']
        self.assertEqual(len(positions), 9)
        self.assertEqual(len(set(map(tuple, positions))), 8)
        self.assertEqual(Counter(map(tuple, positions))[(200, 115, 1011)], 2)
        text = ','.join('.'.join(map(str, p)) for p in positions)
        self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), row['raw_NpcWarp_argument_sha256'])
        g = next(x for x in self.g['extraction']['npc_occurrences'] if x['role'] == 'lost_son_diary_handoff')
        self.assertEqual(set(tuple(p[1:]) for p in positions), set(map(tuple, g['reported_search_positions'])))
        self.assertIsNone(row['actual_random_weighting'])
        self.assertEqual(self.r['source_unreferenced_alternate']['exact_CREATE_or_backup_references'], [])
        self.assertNotEqual(self.r['source_unreferenced_alternate']['sha256'], self.r['source_scripts'][2]['sha256'])
        self.assertNotIn('NpcWarp', self.r['source_unreferenced_alternate']['events'][1]['commands'])

    def test_05_two_original_pools_keep_all_170_positions(self):
        pools = self.r['original_random_pools']
        self.assertEqual([(x['positions'], x['distinct_IDs'], x['duplicate_extra_positions']) for x in pools],
                         [(85, 67, 18), (85, 57, 28)])
        for pool, script in zip(pools, self.r['source_scripts'][4:6], strict=True):
            literal = ','.join(map(str, pool['literal_item_IDs']))
            self.assertEqual(script['events'][0]['commands']['GetRandItem'], [literal])
            self.assertEqual(hashlib.sha256(literal.encode()).hexdigest(), pool['original_argument_sha256'])
            self.assertEqual(script['events'][0]['commands']['DelItem'], ['2700'])
            self.assertEqual(script['events'][0]['bare_Break_lines'], 1)
            self.assertIsNone(pool['probability_or_number_of_rewards'])
            # Sorting/deduplicating would destroy the source argument identity.
            changed = ','.join(map(str, sorted(set(pool['literal_item_IDs']))))
            self.assertNotEqual(hashlib.sha256(changed.encode()).hexdigest(), pool['original_argument_sha256'])

    def test_06_map_graph_matches_old_63_create_configurations(self):
        rows = self.r['original_map_create']['creates']
        old = [x for x in self.ch['create_rows'] if x[0] == MAP_CREATE]
        self.assertEqual(len(rows), 63)
        self.assertEqual(len(old), 63)
        for row, src in zip(rows, old, strict=True):
            self.assertEqual((row['ordinal'], row['floor'], row['borncorner'], row['template']),
                             (src[1], src[5], src[7], src[11]))
        self.assertEqual(sum(x['target'] is not None for x in rows), 57)
        self.assertEqual(rows[5]['target'], [21004, 28, 4])
        self.assertEqual(rows[6]['target'], [21003, 34, 14])
        self.assertEqual(rows[5]['borncorner'][:2], [34, 6])
        self.assertEqual(rows[21]['borncorner'][:2], [5, 32])
        self.assertEqual(rows[21]['target'], [21012, 13, 21])

    def test_07_duplicate_source_tiles_cannot_choose_a_silent_winner(self):
        graph = self.r['original_map_create']
        groups = shared_warp_tiles(graph['creates'])
        self.assertEqual(groups, graph['shared_source_tiles'])
        self.assertEqual([g['source'] for g in groups], [[200, 229, 988], [21016, 13, 21]])
        self.assertEqual([len(g['targets']) for g in groups], [2, 6])
        self.assertEqual([len(set(map(tuple, g['targets']))) for g in groups], [2, 6])
        self.assertFalse(self.r['boundaries']['shared_coordinate_CREATE_selection_priority_verified'])

    def test_08_MAP04_sha_geometry_and_unavailable_floor200_stay_separate(self):
        old = {int(Path(x[0]).stem): x for x in self.m['per_floor_source_rows']}
        joins = {x['floor']: x for x in self.r['map_qualification']}
        self.assertEqual(set(joins), {200, 3413, *range(21001, 21017)})
        self.assertIsNone(joins[200]['geometry'])
        self.assertIsNone(joins[200]['source_DAT_sha256'])
        for floor, row in joins.items():
            self.assertEqual(row['original_DAT_bytes_reread_this_round'], 0)
            if floor in old:
                self.assertEqual((row['source_DAT_sha256'], row['geometry']), (old[floor][2], old[floor][3:5]))
        for row in self.r['source_creates'] + self.r['original_map_create']['creates']:
            if row['floor'] == 200:
                continue
            w, h = joins[row['floor']]['geometry']
            x, y = row['borncorner'][:2]
            self.assertTrue(0 <= x < w and 0 <= y < h)

    def test_09_six_core_items_have_two_old_source_rows_each(self):
        old = {r[0]: r for n in range(1, 8) for r in load(f'item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json')['rows']}
        rows = self.r['core_item_rows']
        self.assertEqual([x['item_ID'] for x in rows], CORE_ITEMS)
        for x in rows:
            self.assertEqual([r['sha256'] for r in x['source_rows']], old[x['item_ID']][1:3])
            self.assertEqual([r['columns'] for r in x['source_rows']], [94, 94])
            self.assertEqual([r['image_alias'] for r in x['source_rows']], [x['source_image_alias']] * 2)
        self.assertEqual(len(self.r['cross_carrier_candidate_images']), 6)

    def test_10_source_limits_do_not_promote_guide_or_drop_claims(self):
        r = self.r
        c = r['existing_2003_guide_comparison']
        self.assertEqual((c['documentary_judgment_floor'], c['source_conditional_CREATE_floor']), (4, 21003))
        self.assertFalse(c['source_floor_ID_equals_documentary_ordinal_verified'])
        self.assertFalse(c['same_game_version_or_deployment_verified'])
        self.assertEqual(r['conditional_warp']['source_values'],
                         {'WARP': '21003,34,7', 'FREE': 'LV>0&ITEM=2700,LV>0&NOWEV=39,LV>0&ENDEV=39', 'MONEY': '-1'})
        self.assertEqual(r['feather_2700']['source_GetItem_literal_files_in_full_2205_NPC_corpus'], [])
        self.assertTrue(all(v is False for k, v in r['boundaries'].items() if isinstance(v, bool)))
        self.assertEqual(r['boundaries']['original_permanent_versus_operated_event_origin'], 'UNRESOLVED')
        self.assertEqual(r['stage_A'], {'PARTIAL': 7, 'OPEN': 2})
        self.assertEqual((r['stage_B'], r['wiki'], r['R79']), ('GATED', 'GATED', 'PAUSED_NON_BLOCKING'))
        self.assertIsNone(r['overall_percent'])
        # Existing documentary provenance is immutable; source numeric IDs do not backfill it.
        self.assertTrue(all(x['item_id'] is None for x in self.g['extraction']['delivery_and_reward_items']))


if __name__ == '__main__':
    unittest.main()
