import struct
import unittest
from tools import stoneage_village_interiors_r34 as r

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

if __name__=='__main__':unittest.main()
