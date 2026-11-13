"""Bounded replay of source-derived mixed25 dungeon01 guardian links.

Private CREATE and handler files were audited off-repo; this test protects the
published derived numerics and cannot independently execute original gameplay.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'research/recovered/STONEAGE-INTEGRATION96-DUNGEON01-SEVEN-WARPMAN-ORIGINAL-SOURCE-R1.json'
DATA = json.loads(RECEIPT.read_text(encoding='utf-8'))
EXPECTED_FREE = [
    'LV>0&ENDEV=4&ENDEV=40,LV>0&ENDEV=4&NOWEV=40',
    'LV>0',
    'LV>64&ENDEV=4',
    'LV>64&ENDEV=4&NOWEV=46&ITEM=2767&ITEM=2768',
    'LV>64&ENDEV=46&ITEM=2766',
    'LV>64&ENDEV=4',
    'LV>64&ENDEV=4',
]
EXPECTED_TARGETS = [
    (20301, 200, 41), (200, 316, 712), (21201, 61, 46),
    (21308, 20, 7), (21301, 7, 3), (30301, 23, 37), (30307, 10, 6),
]
EXPECTED_INDICES = [91, 250, 251, 252, 254, 255, 256]


class Dungeon01SourceGuardTest(unittest.TestCase):
    def test_evidence_scope_and_no_original_gameplay_claim(self):
        self.assertIn('MIXED25_COMMUNITY_PRESERVED', DATA['source_scope'])
        b = DATA['bounds']
        for key in ('FREE_expression_evaluated_in_native_server',
                    'native_warp_or_party_gate_execution_verified',
                    'same_historical_deployment_as_TW1_client_proven',
                    'same_historical_deployment_as_mainland_1_82_proven',
                    'prior_MAP04_DAT_files_re_read_in_this_work_unit',
                    'commercial_dialogue_text_published'):
            self.assertIs(b[key], False)
        self.assertIsNone(b['overall_completion_percentage'])

    def test_source_custody_full_hashes(self):
        c = DATA['source_custody']
        self.assertEqual((c['private_zip_bytes'], c['private_zip_members_crc_validated']), (995176, 2205))
        self.assertEqual(c['private_zip_sha256'], 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual((c['original_CREATE_bytes'],c['original_CREATE_sha256']),
                         (30712,'541ce646794e6c0c3e2414657567cbf6cb662d18b28049f4e3cd691071304169'))
        self.assertIs(c['parent_361MB_RAR_re_read_this_work_unit'],False)

    def test_create_type_partition_and_handler_counts(self):
        n = DATA['counts']
        self.assertEqual(n['CREATE_blocks'], n['npcgen_warp_static'] + n['npcgen_warpman'])
        self.assertEqual((n['CREATE_blocks'],n['npcgen_warp_static'],n['npcgen_warpman']), (257,250,7))
        self.assertEqual((n['exact_handler_files_re_read'],n['handler_WARP_targets'],n['handler_FREE_predicates']), (7,7,7))
        self.assertEqual(len(DATA['seven_guardians']),7)

    def test_exact_source_bytes_are_indexed_not_copied(self):
        rows=DATA['seven_guardians']
        self.assertEqual([r['create_index_0based'] for r in rows], EXPECTED_INDICES)
        self.assertEqual([r['create_byte_halfopen'] for r in rows],
                         [[10835,11010],[29544,29702],[29712,29875],[29885,30055],
                          [30182,30348],[30358,30530],[30540,30712]])
        for r in rows:
            self.assertRegex(r['create_block_sha256'], r'^[0-9a-f]{64}$')
            self.assertEqual(r['source_enemy_type'],'npcgen_warpman')
            self.assertGreater(r['create_byte_halfopen'][1], r['create_byte_halfopen'][0])

    def test_literal_free_and_warp_contracts_not_evaluated(self):
        rows=DATA['seven_guardians']
        self.assertEqual([r['handler_free_literal'] for r in rows], EXPECTED_FREE)
        self.assertEqual([tuple((t:=r['handler_target'])[x] for x in ('floor','x','y')) for r in rows], EXPECTED_TARGETS)
        for r in rows:
            self.assertEqual(r['handler_money_literal'],'-1')
            self.assertEqual(r['handler_warp_literal'],','.join(str(k) for k in
                             (r['handler_target']['floor'],r['handler_target']['x'],r['handler_target']['y'])))
            self.assertRegex(r['handler_sha256'],r'^[0-9a-f]{64}$')
            self.assertTrue(r['handler_relpath'].startswith('genout/wpm_'))
            self.assertGreater(r['handler_bytes'],0)

    def test_prior_MAP04_qualification_only(self):
        rows=DATA['seven_guardians'];n=DATA['counts']
        for key,expect in (('source',3),('handler_target',5)):
            p=[r[key] for r in rows]
            self.assertEqual(sum(x['prior_MAP04_DAT']['known'] for x in p),expect)
            for x in p:
                m=x['prior_MAP04_DAT']
                if m['known']:
                    self.assertRegex(m['sha256'],r'^[0-9a-f]{64}$')
                    self.assertTrue(m['coordinate_in_bounds'])
                    self.assertTrue(0<=x['x']<m['width'] and 0<=x['y']<m['height'])
                else:
                    self.assertEqual(set(m),{'known'})
        self.assertEqual((n['source_endpoints_with_prior_DAT'],n['target_endpoints_with_prior_DAT'],n['endpoints_missing_prior_DAT']), (3,5,6))
        self.assertEqual(n['prior_DAT_endpoint_coordinate_out_of_bounds'],0)

    def test_distinct_handlers_and_original_named_guards(self):
        rows=DATA['seven_guardians']
        self.assertEqual(len({r['handler_sha256'] for r in rows}),7)
        self.assertEqual(len({r['handler_relpath'] for r in rows}),7)
        self.assertEqual([r['graphicname'] for r in rows],[16306,16207,16203,16202,16200,16201,16208])
        self.assertEqual([r['source_dir'] for r in rows],[0,4,4,4,4,4,6])
        self.assertEqual([r['source_name_CP950'] for r in rows],
                         ['拉特拉的守門人','看門人','看門人','賢者的看門人','看門人','洞窟的守門人','洞窟的守門人'])

    def test_no_dialogue_or_original_proprietary_file_published(self):
        raw = RECEIPT.read_text(encoding='utf-8')
        for k in ('FreeMsg:', 'PayMsg:', 'PartyMsg:', 'MoneyMsg:', 'main_msg:', 'NPCCREATE\\n'):
            self.assertNotIn(k, raw)
        self.assertLess(len(raw.encode('utf-8')), 15000)
        self.assertEqual(DATA['bounds']['Stage_A'],'7 PARTIAL + 2 OPEN')
        self.assertEqual(DATA['bounds']['Stage_B'],'GATED')


if __name__ == '__main__':
    unittest.main()
