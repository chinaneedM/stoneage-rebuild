"""Public checks for the derived floor 1300 join and its evidence limits."""
from collections import Counter
import json
import unittest

from tools.stoneage_integration11_floor1300 import REPORT, parse_warps, sources


class Floor1300Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.sources = sources()

    def test_create_provenance_and_colocation(self):
        creates = self.report['creates']
        old = self.sources['i06']['floor1300_source_create_records']
        self.assertEqual([(r['path'], r['ordinal'], r['parameter_sha256']) for r in creates],
                         [(r['create_path'], r['create_block_ordinal'], r['parameter_sha256']) for r in old])
        overlap = {tuple(r['xy']): [b['enemy_token'] for b in r['separate_create_blocks']]
                   for r in self.report['colocated_create_blocks']}
        self.assertEqual(overlap, {(37, 26): ['npcgen_timeman']*2, (70, 51): ['changeevent', 'npcgen_man']})
        self.assertEqual(len({tuple(r['xy']) for r in creates}), 5)
        self.assertEqual(creates[4]['source_tile_u16'], [406, 0, 49152])

    def test_two_warp_sources_and_directionality(self):
        rows = self.report['mapwarp_rows']
        edges = {(tuple(r['source']), tuple(r['target'])) for r in rows}
        self.assertEqual(len(edges), 46)
        self.assertEqual(len({r['line'] for r in rows}), 46)
        self.assertEqual(self.report['direct_CREATE_only'], [])
        self.assertTrue(all(len(r['same_tuple_create']) == 1 for r in rows))
        counts = Counter((r['source'][0], r['target'][0]) for r in rows)
        self.assertEqual(counts[100, 1300], 8)
        self.assertEqual(counts[1300, 100], 8)
        self.assertEqual(sum(r['exact_reverse'] for r in rows), 30)
        for r in rows:
            self.assertEqual(r['exact_reverse'], (tuple(r['target']), tuple(r['source'])) in edges)
        self.assertIn(((100, 622, 190), (1300, 24, 59)), edges)
        self.assertIn(((1300, 23, 59), (100, 621, 190)), edges)

    def test_every_endpoint_has_pinned_dat(self):
        linked = self.report['linked_DAT']
        self.assertEqual(set(map(int, linked)), {100, 1301, 1302, 1303, 1304, 1305, 1306, 1310})
        pins = {r[5]: r[3] for r in self.sources['map']['original_decoded_source_rows']
                if r[0] == 0 and r[1].lower().endswith('.dat')}
        pins.update({r['floor']: r['sha256'] for r in self.sources['i10']['recovered_DAT']})
        self.assertEqual(self.report['original_DAT']['sha256'], pins[1300])
        for k, v in linked.items():
            self.assertEqual(v['sha256'], pins[int(k)])
        for r in self.report['mapwarp_rows']:
            for endpoint in (r['source'], r['target']):
                f, x, y = endpoint
                geo = linked.get(str(f), dict(width=100, height=100))
                self.assertTrue(0 <= x < geo['width'] and 0 <= y < geo['height'])
            self.assertEqual(len(r['floor1300_tile_u16']), 3)
            self.assertEqual(len(r['other_floor_tile_u16']), 3)

    def test_tw1_coverage_and_claim_limits(self):
        c = self.report['candidate']
        old = self.sources['i06']['original_MAP_rows'][0]
        self.assertEqual(self.report['original_MAP']['sha256'], old['original_sha256'])
        self.assertEqual(self.report['original_MAP']['equal_u16_cells_by_DAT_plane'], [0, 0, 0])
        self.assertEqual(c['distinct_aliases'], 384+20)
        self.assertEqual(c['draw_references'], 6149+43)
        self.assertEqual(len(self.report['new_aliases']), 20)
        self.assertEqual(sum(r['references'] for r in self.report['new_aliases'].values()), 43)
        self.assertEqual(c['uncovered_references'], 0)
        self.assertTrue(c['independent_canvas_match'])
        self.assertTrue(all(v is False for v in self.report['limits'].values()))

    def test_warp_parser_keeps_order_and_rejects_partial_coordinate(self):
        rows = parse_warps(b'# header\nNONE:NULL:1300,1,2:100,3,4:NULL\nNONE:NULL:100,3,4:1300,1,2:NULL')
        self.assertEqual([r[:3] for r in rows], [(2, (1300, 1, 2), (100, 3, 4)), (3, (100, 3, 4), (1300, 1, 2))])
        with self.assertRaises(ValueError):
            parse_warps(b'NONE:NULL:1300,1:100,3,4:NULL')


if __name__ == '__main__':
    unittest.main()
