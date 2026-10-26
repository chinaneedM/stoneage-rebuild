import struct
import unittest
import copy
import json
from tools import stoneage_village_interiors_r34 as r
from tools import stoneage_village_interiors_archive_r34 as archive

def dat(w,h,planes):
    return struct.pack('<II',w,h)+b''.join(struct.pack('<'+'H'*len(p),*p) for p in planes)

class Rooms(unittest.TestCase):
    def test_order_and_transition_multiplicity(self):
        a=dat(2,2,[[1]*4,[3,3,5,0],[0x4000]*4])
        b=dat(2,2,[[1]*4,[4,4,5,0],[0xc000]*4])
        x=r.compare_pair(a,b)
        self.assertEqual([p['changed_cells'] for p in x['planes']],[0,2,4])
        self.assertEqual(x['planes'][1]['transitions'],[{'june_u16':3,'dec_u16':4,'xor_mask':7,'cells':2}])
        self.assertEqual(x['planes'][2]['xor_counts'],[[0x8000,4]])

    def test_unsigned_and_noop_control(self):
        raw=dat(1,1,[[65535],[0],[32768]])
        self.assertEqual([p['changed_cells'] for p in r.compare_pair(raw,raw)['planes']],[0]*3)

    def test_short_extra_odd_and_zero_fail(self):
        raw=dat(1,1,[[1],[2],[3]])
        for bad in (raw[:7],raw[:-1],raw+b'\0',struct.pack('<II',0,2),struct.pack('<II',1000001,1)):
            with self.subTest(bad=bad[:8]), self.assertRaises(ValueError):r.parse(bad)

    def test_geometry_not_just_cell_count(self):
        with self.assertRaises(ValueError):r.compare_pair(dat(1,2,[[1,2]]*3),dat(2,1,[[1,2]]*3))

    def test_source_rows_must_be_unique(self):
        with self.assertRaises(ValueError):r.fields('A|id=1|v=x\nA|id=1|v=y','A|id=1|')

    def test_source_qualified_names_remain_later(self):
        rows=r.annotations()
        self.assertEqual(len(rows),4)
        self.assertTrue(all(x['name_scope'].startswith('LATER_RECOVERED') for x in rows.values()))
        self.assertTrue(rows[1003]['recovered25_name_escaped'].endswith('%7C0'))

class ArchiveBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=r.ROOT/archive.RAW
        if not path.exists():raise unittest.SkipTest('source-only commit before archival report')
        cls.source=json.loads(path.read_bytes())

    def test_actual_source_acceptance(self):
        archive.validate_source(self.source)

    def test_forged_bit_meaning_name_or_game_execution(self):
        for key in ('original_game_executed','same_build_name_or_npc_binding_proven','rendered_scene_proven','plane3_event_or_walkability_semantics_proven','room_name_from_dat'):
            d=copy.deepcopy(self.source);d['boundaries'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):archive.validate_source(d)

    def test_transition_direction_and_unsigned_value(self):
        for key,value in [('june_u16',49152),('dec_u16',-16384),('cells',79),('xor_mask',16384)]:
            d=copy.deepcopy(self.source);d['rooms'][0]['planes'][2]['transitions'][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):archive.validate_source(d)

    def test_repeated_room_or_invented_name(self):
        d=copy.deepcopy(self.source);d['rooms'][1]=copy.deepcopy(d['rooms'][0])
        with self.assertRaises(ValueError):archive.validate_source(d)
        d=copy.deepcopy(self.source);d['rooms'][0]['name_reference']['name_scope']='AUTHENTICATED_TW10'
        with self.assertRaises(ValueError):archive.validate_source(d)

if __name__=='__main__':unittest.main()
