"""QUEST12: public evidence-only invariants, safe in GitHub Actions."""
import hashlib
import json
import unittest
from tools.stoneage_quest12_mining_competition_source import (
    ROOT, REPORT, SOURCE, parse_events, parse_operand, git_blob,
)


class MiningCompetitionSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())
        cls.s = [s['events'] for s in cls.r['scripts']]
        cls.manifest = json.loads(SOURCE.read_text())

    def test_archive_and_all_selected_files_conserved(self):
        r = self.r
        self.assertEqual(r['schema'], 'stoneage.quest12.mining_competition_original_source.r1')
        self.assertEqual(r['verified_original_NPC_members'], 2205)
        self.assertEqual(len(self.manifest['source_files']), 2205)
        self.assertEqual(git_blob(SOURCE.read_bytes()), r['prior_manifest_git_blob_sha1'])
        originals = {a[0]: a for a in self.manifest['source_files']}
        self.assertEqual(len(r['source_files']), 9)
        for f in r['source_files']:
            self.assertEqual([f['bytes'], f['sha256'], f['crc32']], originals[f['path']][1:4])

    def test_creates_are_not_confused_with_generated_messages(self):
        creates = self.r['principal_creates']
        miner = self.r['miner_create']
        generated = self.r['generated_support_creates']
        self.assertEqual((len(creates), len(miner), len(generated)), (2, 1, 21))
        self.assertEqual([(r['floor'], r['borncorner'][:2]) for r in creates],
                         [(31805, [19, 21]), (31805, [33, 23])])
        self.assertEqual((miner[0]['floor'], miner[0]['borncenter'][:2]), (31805, [26, 23]))
        original = {(a[0], a[1]): a for a in self.manifest['create_rows']}
        for row in creates + miner + generated:
            m = original[(row['path'], row['ordinal'])]
            self.assertEqual((row['block_sha256'], row['floor'], row['graphic_alias']),
                             (m[4], m[5], m[6]))
            self.assertEqual(row['parameter_references'], m[15])
        self.assertEqual(sum(x['borncorner'][:2] == [22, 4] for x in generated), 1)

    def test_two_source_scripts_and_nonexecuted_conditions(self):
        self.assertEqual([len(s) for s in self.s], [7, 6])
        self.assertEqual([s['path'] for s in self.r['scripts']],
                         ['giiru/event/giruev2_1', 'giiru/event/giruev2_2'])
        for s in self.s:
            for i, e in enumerate(s):
                self.assertEqual(e['ordinal'], i)
                self.assertEqual(len(e['source_block_sha256']), 64)
                self.assertTrue(e['source_start_byte'] < e['source_end_byte'])
                self.assertIn(e['type'], {'REQUEST', 'ACCEPT', 'MESSAGE'})
        self.assertEqual(self.s[0][1]['raw_condition'], 'ITEM=2533&ENDEV!=27')
        self.assertEqual(self.s[1][3]['raw_condition'], 'NOWEV=27&ITEM=2534')
        self.assertEqual(self.s[0][3]['raw_condition'], 'LV>29&ENDEV!=27')

    def test_mining_rights_item_handoffs_are_literal(self):
        a, b = self.s
        def ops(e):
            return [(x['key'], x['raw_operand']) for x in e['commands']]
        self.assertEqual(ops(a[0]), [('GetItem', '2527'), ('DelStone', '1000')])
        self.assertEqual(ops(a[1]), [('GetItem', '2527'), ('DelItem', '2533'), ('EndSetFlg', '27')])
        self.assertEqual(ops(b[3]), [('GetItem', '2535'), ('DelItem', '2534*1,2536')])
        self.assertEqual(ops(b[5]), [('GetItem', '2536*1')])
        self.assertEqual(ops(a[5]), [('GetItem', '2394*1'), ('DelItem', '2391*1')])
        self.assertEqual(b[3]['commands'][1]['operands'],
                         [{'item_id': 2534, 'explicit_quantity': 1},
                          {'item_id': 2536, 'explicit_quantity': None}])
        self.assertIsNone(a[1]['commands'][1]['operands'][0]['explicit_quantity'])

    def test_miners_and_gate_are_not_runtime_proof(self):
        c = self.r['other_original_controls']
        self.assertEqual({v['key']:v['raw_value'] for v in c['300/sb_bac.arg']},
                         {'entype': '2', 'item': '2535', 'steal': '1', 'enemyno': '1004', 'time': '300'})
        self.assertEqual({v['key']:v['raw_value'] for v in c['genout/wpm_31805_22_4']},
                         {'WARP': '31806,34,6', 'FREE': 'ITEM=2527', 'DelItem': '2527*1', 'MONEY': '-1'})
        self.assertFalse(self.r['boundaries']['item_2535_enemy_drops_verified'])
        self.assertFalse(self.r['boundaries']['warp_runtime_verified'])

    def test_qualified_negative_evidence_is_local_to_carrier(self):
        occ = self.r['get_item_source_occurrences_across_all_2205_files']
        self.assertEqual(set(occ), {'2391','2393','2394','2527','2533','2534','2535','2536'})
        self.assertEqual((len(occ['2533']), len(occ['2534'])), (0, 0))
        self.assertEqual([len(occ[x]) for x in ['2527','2535','2536','2393','2394']], [2,1,1,1,1])
        self.assertEqual(self.r['carrier'], 'LATER_COMMUNITY_MIXED25_NOT_OFFICIAL_DEPLOYMENT')
        self.assertFalse(self.r['boundaries']['all_version_quest_completion_verified'])

    def test_original_item_rows_and_pixel_namespaces(self):
        items = self.r['item_evidence']
        self.assertEqual([i['item_id'] for i in items], [2391,2393,2394,2527,2533,2534,2535,2536])
        self.assertEqual(sum(len(i['original_rows']) for i in items), 15)
        self.assertEqual([i['image_alias'] for i in items if i['item_id'] in [2527,2533,2535,2536]],
                         [24222]*4)
        self.assertEqual([i['image_alias'] for i in items if i['item_id']==2534], [14607])
        self.assertFalse(items[0]['tw1_original_RD_candidate_available'])
        self.assertTrue(all(i['tw1_original_RD_candidate_available'] for i in items[1:]))
        self.assertEqual(len({v['raw_line_without_newline_sha256'] for i in items for v in i['original_rows']}),8)

    def test_original_dat_positions_are_not_collision_decoding(self):
        maps = self.r['map_source_observations']
        self.assertEqual([(m['floor'],m['geometry']) for m in maps], [(31805,[50,50]),(31806,[50,50])])
        self.assertEqual([m['original_DAT_bytes'] for m in maps], [15008,15008])
        points = {(m['floor'],p['label']):p for m in maps for p in m['source_points']}
        for floor, label, xy, values in [
            (31805, 'tenim', [19,21], [4200,0,49152]),
            (31805, 'babaro',[33,23],[4301,0,49152]),
            (31805, 'miner_center',[26,23],[5068,0,49157]),
            (31805, 'permit_gate',[22,4],[4302,0,49152]),
            (31806, 'permit_dest',[34,6],[4305,0,49152]),
        ]:
            self.assertEqual((points[floor,label]['xy'],points[floor,label]['source_three_u16_values']),
                             (xy,values))
        self.assertFalse(self.r['boundaries']['character_movement_or_collision_verified'])

    def test_parser_fails_closed_and_never_invents_quantity(self):
        self.assertEqual(parse_operand('2536'), {'item_id':2536,'explicit_quantity':None})
        self.assertEqual(parse_operand('2536*1'), {'item_id':2536,'explicit_quantity':1})
        with self.assertRaises(ValueError):parse_operand('2536*?')
        original = b'EventNo:27\nTYPE:ACCEPT\nEVENT:NOWEV=27&ITEM=2534\nDelItem:2534*1,2536\nEventEnd\n'
        parsed = parse_events(original)
        self.assertEqual(parsed[0]['source_block_sha256'], hashlib.sha256(original).hexdigest())
        for bad in [original[:-9], b'TYPE:ACCEPT\nEVENT:NOWEV=27\nEventEnd\n',
                    original.replace(b'2534*1,2536',b'2534*1,2536?')]:
            with self.assertRaises(ValueError):parse_events(bad)

    def test_no_source_claim_promoted_to_native_runtime(self):
        self.assertTrue(all(value is False for value in self.r['boundaries'].values()))
        self.assertEqual(self.r['origin_class'], 'ORIGIN_UNRESOLVED')
        self.assertEqual(self.r['status']['stage_A'], '7_PARTIAL_2_OPEN')
        self.assertEqual(self.r['status']['stage_B_wiki'], 'GATED')
        self.assertEqual(self.r['status']['R79'], 'PAUSED_NON_BLOCKING')
        self.assertIsNone(self.r['status']['overall_percent'])


if __name__ == '__main__': unittest.main()
