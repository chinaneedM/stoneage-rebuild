"""Rights-safe source evidence replay: later mixed25 Munde settlement, no native gameplay claim."""
import collections
import copy
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION110-MUNDE-TRIBE-ORIGINAL-NPC-STATIC-ROUTE-R1.json'
CHAR01 = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
COVERAGE = ROOT / 'research/recovered/STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt'


class OriginalMundeEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.parent = json.loads(CHAR01.read_text(encoding='utf-8'))
        cls.lines = COVERAGE.read_text(encoding='utf-8').splitlines()
        cls.rows = cls.doc['source_rows']

    def assert_row_against_parent(self, r):
        source = r['source_file'].removeprefix('npc/')
        candidates = [x for x in self.parent['create_rows'] if x[0] == source and x[1] == r['ordinal_zero_based']]
        self.assertEqual(len(candidates), 1)
        p = candidates[0]
        self.assertEqual([p[2], p[3]], r['byte_span_inclusive_exclusive'])
        self.assertEqual(p[4], r['original_block_sha256'])
        self.assertEqual(p[5], r['source_floor'])
        self.assertEqual(p[6], r['source_graphicname'])
        self.assertEqual(p[7][:2], r['source_xy'])
        self.assertEqual(p[11], r['source_function'])
        if r['original_handler_ref'] is not None:
            self.assertIn([r['original_handler_ref'], 'EXACT_SAME_NPC_SUBTREE_PATH', r['original_handler_sha256']],p[15])

    def test_source_carrier_and_unmodified_historical_boundary(self):
        v = self.doc
        self.assertEqual(v['private_original_source']['npc_zip_sha256'],'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(v['private_original_source']['zip_members_crc_pass'], 2205)
        self.assertEqual(v['baseline']['current_original_git_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(v['baseline']['current_original_bytes'],2709173)
        self.assertIn('NOT_TW1_OR_NATIVE_RUNTIME',v['evidence_scope'])

    def test_all_nine_original_file_sha_size_crc_are_from_prior_full_index(self):
        reference = {x[0]: x for x in self.parent['source_files']}
        files = self.doc['private_original_source']['individual_files']
        self.assertEqual(len(files),9)
        for k,v in files.items():
            self.assertIn(k, reference)
            self.assertEqual((v['bytes'],v['sha256'],v['crc32']), (reference[k][1],reference[k][2],reference[k][3]))
            self.assertRegex(v['sha256'],r'^[a-f0-9]{64}$')
        self.assertEqual(files['genout/11100npc.create']['bytes'],1481)
        self.assertEqual(files['genout/11101d.create']['bytes'],1737)

    def test_each_22_original_byte_span_and_function_matches_char01(self):
        self.assertEqual(len(self.rows),22)
        self.assertEqual(collections.Counter(r['source_file'] for r in self.rows),{'genout/11100npc.create':8,'genout/11101d.create':14})
        self.assertEqual(collections.Counter(r['source_function'] for r in self.rows),{'npcgen_warp':14,'npcgen_man':5,'npcgen_dengon':1,'npcgen_warpman':1,'npcgen_signboard':1})
        for r in self.rows:
            self.assert_row_against_parent(r)
        self.assertEqual([r['ordinal_zero_based'] for r in self.rows[:8]],list(range(8)))
        self.assertEqual([r['ordinal_zero_based'] for r in self.rows[8:]],list(range(14)))

    def test_negative_source_mutations_are_caught_by_byte_span_and_sha(self):
        r=copy.deepcopy(self.rows[0]);r['original_block_sha256']='0'*64
        with self.assertRaises(AssertionError):self.assert_row_against_parent(r)
        r=copy.deepcopy(self.rows[1]);r['byte_span_inclusive_exclusive'][1]+=1
        with self.assertRaises(AssertionError):self.assert_row_against_parent(r)
        r=copy.deepcopy(self.rows[2]);r['source_floor']=100
        with self.assertRaises(AssertionError):self.assert_row_against_parent(r)

    def test_prior_dat_metadata_has_exact_dimensions_sha_and_bounds(self):
        meta=self.doc['source_qualified_prior_DAT_metadata']
        self.assertEqual(meta['reference_file'], 'research/recovered/STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt')
        self.assertEqual(len(meta['floors']),7)
        indexed={}
        for s in self.lines:
            m=re.match(r'^FLOOR\|id=(\d+)\|path=([^|]+)\|width=(\d+)\|height=(\d+)\|map_sha256=([a-f0-9]{64})',s)
            if m:indexed[int(m.group(1))]=(int(m.group(3)),int(m.group(4)),m.group(5))
        self.assertEqual(sorted(x['floor'] for x in meta['floors']),list(range(11101,11108)))
        for x in meta['floors']:
            self.assertEqual(indexed[x['floor']],(x['width'],x['height'],x['sha256']))
        for r in self.rows:
            fm=indexed.get(r['source_floor'])
            if fm:
                self.assertTrue(0<=r['source_xy'][0]<fm[0] and 0<=r['source_xy'][1]<fm[1])
                self.assertEqual(r['source_DAT_qualification'],'IN_BOUNDS_PRIOR_COVERAGE_METADATA')
            else:self.assertEqual(r['source_DAT_qualification'],'NO_QUALIFIED_DAT_IN_SELECTED_PRIOR_COVERAGE')

    def test_14_static_routes_reciprocal_12_and_two_to_unqualified_100(self):
        warps=self.rows[8:]
        self.assertTrue(all(x['source_function']=='npcgen_warp' for x in warps))
        q={(r['source_floor'],*r['source_xy'],*r['literal_target_floor_xy']) for r in warps}
        self.assertEqual(len(q),14)
        reverse=[p for p in q if (*p[3:],*p[:3]) in q]
        self.assertEqual(len(reverse),12)
        no_reverse=[p for p in q if (*p[3:],*p[:3]) not in q]
        self.assertEqual(sorted(x[0] for x in no_reverse),[11101,11107])
        self.assertEqual({p[3] for p in no_reverse},{100})
        self.assertEqual(sum(r['target_DAT_qualification']=='NO_QUALIFIED_DAT_IN_SELECTED_PRIOR_COVERAGE' for r in warps),2)

    def test_original_entry_offset_not_exact_reverse(self):
        w=self.doc['source_warpman_100_443_127']
        self.assertEqual(w['source_floor_xy'],[100,443,127])
        self.assertEqual(w['literal_WARP_target'],[11101,33,29])
        self.assertEqual(w['static_return_at_11101_33_28'],[100,442,127])
        self.assertFalse(w['exact_reverse_coordinate_match'])
        self.assertNotEqual(w['source_floor_xy'][1:],[442,127])
        self.assertEqual(w['source_handler_sha256'],self.doc['private_original_source']['individual_files']['genout/wpm_100_443_127']['sha256'])

    def test_counts_and_negative_copyright_runtime_qualifications(self):
        c=self.doc['derived_counts']
        self.assertEqual((c['source_create_blocks'],c['source_static_warps'],c['source_npc_and_sign_configuration_blocks'],c['original_handler_files']),(22,14,8,7))
        self.assertEqual((c['create_source_points_qualified'],c['create_source_points_unqualified_in_selected_index']),(20,2))
        self.assertEqual((c['warp_targets_qualified'],c['warp_targets_unqualified_in_selected_index']),(12,2))
        self.assertFalse(any(self.doc['copyright_and_execution_limits'].values()))
        self.assertTrue(all(not isinstance(r.get('original_dialogue_full_text'),str) for r in self.rows))

if __name__=='__main__': unittest.main()