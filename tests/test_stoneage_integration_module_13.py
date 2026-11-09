"""Cross-check public joins to immutable prior evidence without private assets."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

REC = Path(__file__).resolve().parents[1] / 'research/recovered'
REPORT = 'STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE-R1.json'
I11 = 'STONEAGE-INTEGRATION11-FLOOR1300-SOURCE-SCENE-R1.json'
MAP07 = 'STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json'
CHAR01 = 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'


def load(name):
    return json.loads((REC / name).read_bytes())


class Integration13Public(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = load(REPORT)
        cls.rooms = cls.report['rooms']
        cls.prior = load(I11)
        cls.char = load(CHAR01)

    def test_immutable_source_blobs(self):
        self.assertEqual(len(self.report['source_git_blobs']), 5)
        for name, expected in self.report['source_git_blobs'].items():
            raw = (REC / name).read_bytes()
            self.assertEqual(hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest(), expected)

    def test_room_sources_and_reused_canvases(self):
        old = {str(r['floor']): r for r in load(MAP07)['maps']}
        names = ['武器店', '道具店', '寵物店', '肉店', '醫院']
        self.assertEqual(set(self.rooms), set(str(f) for f in range(1301, 1306)))
        for floor, role in zip(sorted(self.rooms), names):
            room = self.rooms[floor]
            self.assertEqual(room['original_name'], f'霍特爾的{role}|0')
            self.assertEqual(room['dimensions'], [30, 30])
            self.assertEqual(room['server_map']['bytes'], 44 + 4*900)
            self.assertEqual(room['dat']['bytes'], 8 + 6*900)
            self.assertEqual(room['dat']['sha256'], old[floor]['source_dat_sha256'])
            self.assertEqual(room['dat']['sha256'], self.prior['linked_DAT'][floor]['sha256'])
            self.assertEqual(room['map07_draw_references'], old[floor]['modern_candidate_draw_positions'])
            self.assertEqual(room['map07_canvas']['size'], old[floor]['modern_candidate_canvas_size'])
        self.assertEqual(sum(r['map07_draw_references'] for r in self.rooms.values()), 828)

    def test_all_room_creates_match_original_occurrences(self):
        actual = {(r['path'], r['ordinal']): (int(f), r)
                  for f, room in self.rooms.items() for r in room['source_create']}
        expected = {(r[0], r[1]): r for r in self.char['create_rows'] if str(r[5]) in self.rooms}
        templates = {(r[0], r[1]): r for r in self.char['template_rows']}
        self.assertEqual(len(actual), 29)
        self.assertEqual(set(actual), set(expected))
        for key, (floor, row) in actual.items():
            orig = expected[key]
            self.assertEqual((row['block_sha256'], floor, row['graphic_alias'], row['xy']),
                             (orig[4], orig[5], orig[6], orig[7][:2]))
            self.assertEqual(row['enemy_template'], orig[11])
            p, n, digest = row['template']
            self.assertEqual([p, n], orig[13][0])
            self.assertEqual((digest, row['functionset'] or ''), (templates[p, n][2], templates[p, n][4]))
            self.assertEqual([(v['path'], v['sha256']) for v in row['parameters']],
                             [(p, h) for p, _, h in orig[15]])

    def test_same_point_variants_and_numeric_healer_arguments_are_preserved(self):
        same = [r for r in self.rooms['1302']['source_create'] if r['xy'] == [12, 15]]
        self.assertEqual([(r['path'], r['ordinal']) for r in same],
                         [('genout/shop_m.create', 106), ('genout/shop_m2.create', 118)])
        self.assertNotEqual(same[0]['block_sha256'], same[1]['block_sha256'])
        self.assertEqual(same[0]['parameters'], same[1]['parameters'])
        health = [r for r in self.rooms['1305']['source_create'] if r['functionset'] == 'WindowHealer']
        self.assertEqual([r['argument_literals'] for r in health], [['10', '1.3', '2.6', '2']])
        self.assertEqual(sum(r['functionset'] is None for r in self.rooms['1303']['source_create']), 6)

    def test_warp_rows_preserve_both_endpoints(self):
        old = {r['line']: r for r in self.prior['mapwarp_rows']
               if any(str(r[k][0]) in self.rooms for k in ('source', 'target'))}
        edges = self.report['warp_rows']
        self.assertEqual([r['line'] for r in edges], sorted(old))
        self.assertEqual(len(edges), 20)
        counts = Counter()
        for row in edges:
            prev = old[row['line']]
            for k in ('source', 'target', 'row_sha256'):
                self.assertEqual(row[k], prev[k])
            start, end = row['source'], row['target']
            room_first = str(start[0]) in self.rooms
            counts[(start if room_first else end)[0], room_first] += 1
            values = [prev['floor1300_tile_u16'], prev['other_floor_tile_u16']]
            self.assertEqual(row['endpoints_dat_u16'], values[::-1] if room_first else values)
            if room_first:
                out = [r for r in self.rooms[str(start[0])]['source_create']
                       if r['xy'] == start[1:] and r['target'] == end]
                self.assertEqual([r['block_sha256'] for r in out],
                                 [prev['same_tuple_create'][0]['block_sha256']])
        self.assertEqual(counts, Counter({(f, out): 2 for f in range(1301, 1306) for out in (False, True)}))

    def test_server_client_comparison_and_scope(self):
        zero = dict(changed=0, differences=[])
        for floor, room in self.rooms.items():
            self.assertEqual(room['layer_comparison'], [zero, dict(changed=60, differences=[[2, 0, 60]])]
                             if floor == '1304' else [zero, zero])
        self.assertEqual(len(self.report['original_members']), 27)
        self.assertTrue(all(not value for value in self.report['limits'].values()))
        self.assertEqual(self.report['private_package']['members'], 34)


if __name__ == '__main__':
    unittest.main()
