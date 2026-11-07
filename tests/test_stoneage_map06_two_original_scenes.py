import json
from pathlib import Path
import struct
import unittest
from tools import stoneage_map06_two_original_scenes as m


def dat(planes,width=2,height=2):
    return struct.pack('<II',width,height)+b''.join(struct.pack('<4H',*p) for p in planes)

class Map06(unittest.TestCase):
    def test_low_numeric_source_values_retained_without_guessing_visible_tiles(self):
        raw=dat([[1,99,100,101],[0,2,102,0],[9,8,7,6]])
        info,items=m.placements(raw)
        self.assertEqual(info['modern_draw_candidate_positions'],3)
        self.assertEqual(info['source_low_nonzero_not_rendered'],3)
        self.assertEqual(info['source_nonzero_first_two_planes'],6)
        self.assertEqual({x['image_key'] for x in items},{100,101,102})
        self.assertEqual(info['planes'][2]['nonzero_cells'],4)
    def test_original_planes_and_repeated_positions_are_not_deduplicated(self):
        raw=dat([[200]*4,[200]*4,[0]*4]);info,items=m.placements(raw)
        self.assertEqual(len(items),8)
        self.assertEqual([x['layer'] for x in items],['tile']*4+['parts']*4)
        self.assertEqual([x['xy'] for x in items[:4]],[[0,1],[1,1],[0,0],[1,0]])
    def test_reject_truncated_extra_and_zero_geometry(self):
        raw=dat([[0]*4]*3)
        for bad in [raw[:-1],raw+b'\0',b'\0'*8]:
            with self.assertRaises(ValueError):m.placements(bad)
    def test_public_receipt_keeps_sources_and_native_unknowns_separate(self):
        r=json.loads(m.REPORT.read_bytes())
        self.assertEqual(len(r['resources']),55)
        expected={'1005':(30,30,218,757),'1006':(30,40,246,1038)}
        for floor,(width,height,positions,low) in expected.items():
            a=r['maps'][floor];s=a['structure'];self.assertEqual((s['width'],s['height'],s['modern_draw_candidate_positions'],s['source_low_nonzero_not_rendered']),(width,height,positions,low))
            self.assertEqual(a['source_sha256'],m.PINS[floor+'.dat'][1])
            self.assertEqual(set(a['frames']),{'plane0','plane1','combined'})
        self.assertTrue(all(v is False for v in r['boundaries'].values()))
    def test_private_html_has_no_network_resource_or_original_game_claim(self):
        page=m.html_page({'1005-combined':b'test bytes'})
        self.assertIn('data:image/png;base64,',page)
        self.assertNotRegex(page,r'(?:src|href)=["\']https?://')
        self.assertIn('没有原客户端',page)
    def test_source_receipt_requires_complete_known_carrier_and_two_member_hashes(self):
        source=json.loads((m.REC/'STONEAGE-MAP06-ORIGINAL-DAT-SOURCE-RECEIPT-R1.json').read_bytes())
        self.assertEqual(source['bundle']['bytes'],361255180)
        self.assertEqual(source['bundle']['sha256'],'d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5')
        self.assertFalse(source['original_program_executed']);self.assertFalse(source['raw_originals_published'])
        for name,pin in m.PINS.items():
            a=source['members'][name];self.assertEqual((a['bytes'],a['sha256'],a['crc32']),pin)

if __name__=='__main__':unittest.main()
