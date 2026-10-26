import copy
import json
import lzma
import struct
import unittest
from tools import stoneage_map_resource_content_r21 as m

class ParserTests(unittest.TestCase):
    def test_three_planes_and_all_cells_preserved(self):
        b=struct.pack('<II6H',2,1,9,9,0,42,0xf001,0xf002)
        r=m.parse(b)
        self.assertEqual(r['planes'][0]['histogram'],[[9,2]])
        self.assertEqual(r['planes'][1]['histogram'],[[0,1],[42,1]])
        self.assertEqual(r['planes'][2]['histogram'],[[61441,1],[61442,1]])
    def test_bad_extent_and_dimensions_rejected(self):
        for b in (b'',struct.pack('<II',0,3),struct.pack('<II',1000001,1),struct.pack('<II3H',1,1,1,2,3)+b'x'):
            with self.subTest(b=b),self.assertRaises(ValueError):m.parse(b)
    def test_zero_is_not_a_default_graphic_and_missing_is_not_dropped(self):
        r=m.join_histogram([[0,4],[42,2]],'TW10',{('TW10',0):[{'content_sha256':'a'}]})
        self.assertEqual(r['unresolved_values'],[42]);self.assertEqual(r['unresolved_cells'],2)
        self.assertEqual(r['rows'][0]['candidates'],[])
    def test_all_duplicate_occurrences_and_contents_are_retained(self):
        idx={('TW10',42):[{'content_sha256':'a'},{'content_sha256':'a'},{'content_sha256':'b'}]}
        r=m.join_histogram([[42,9]],'TW10',idx)
        self.assertEqual(r['rows'][0]['candidate_count'],3);self.assertEqual(r['rows'][0]['distinct_content_count'],2)
        self.assertEqual(r['multiple_occurrence_values'],[42]);self.assertEqual(r['multiple_content_values'],[42])
    def test_profiles_and_identifier_namespaces_cannot_be_merged(self):
        idx={('CN50',42):[{'content_sha256':'a'}]}
        self.assertEqual(m.join_histogram([[42,1]],'TW10',idx)['unresolved_values'],[42])

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(lzma.decompress((m.ROOT/'research/recovered/STONEAGE-FOUR-MAP-RESOURCE-CONTENT-R21.json.xz').read_bytes()))
    def test_actual_metadata_replays(self):m.replay(self.r)
    def test_wrong_same_build_name_or_runtime_claim_rejected(self):
        for k in ('same_build_render_selection_proven','map_names_or_npcs_inferred','original_client_executed'):
            r=copy.deepcopy(self.r);r[k]=True
            with self.subTest(k=k),self.assertRaises(ValueError):m.replay(r)
    def test_missing_duplicate_candidate_rejected(self):
        for mp in self.r['maps']:
            for p in mp['planes'][:2]:
                for profile in m.PROFILES:
                    for row in p['resource_value_comparisons'][profile]['rows']:
                        if row['candidate_count']>1:
                            row['candidates'].pop()
                            with self.assertRaises(ValueError):m.replay(self.r)
                            return
        self.fail('real report lacks any resource candidate')
    def test_false_resource_resolution_rejected(self):
        p=self.r['maps'][0]['planes'][0]['resource_value_comparisons']['TW10'];p['unresolved_cells']+=1
        with self.assertRaises(ValueError):m.replay(self.r)
    def test_map_histogram_cell_loss_rejected(self):
        self.r['maps'][0]['planes'][0]['histogram'][0][1]-=1
        with self.assertRaises(ValueError):m.replay(self.r)
    def test_third_plane_is_not_graphic_or_entity_data(self):
        p=self.r['maps'][0]['planes'][2];p['resource_value_comparisons']={}
        with self.assertRaises(ValueError):m.replay(self.r)

if __name__=='__main__':unittest.main()
