"""Public WORLD11 joins across pinned source receipts."""

from collections import Counter
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'research' / 'recovered'
WORLD = 'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-'
SCENE13 = 'STONEAGE-SCENE13-PET-ACTION0-R1.json'


def load(name):
    return json.loads((ROOT / name).read_bytes())


class VillageAppearance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world04 = load(WORLD + '04-THREE-VILLAGE-NPC-TEXT-SOURCE-R1.json')
        cls.world10 = load(WORLD + '10-THREE-VILLAGE-MAP-OBSERVATION-R1.json')
        cls.world11 = load(WORLD + '11-NPC-STATIC-APPEARANCE-R1.json')
        cls.scene13 = load(SCENE13)

    def test_same_preserved_file_identifiers_and_namespace(self):
        self.assertEqual(self.world11['original_archive_sha256'], self.world10['original_archive_sha256'])
        sources = self.world11['original_files']
        self.assertEqual(set(sources), {'adrn_15.bin', 'real_15.bin', 'Palet_1.sap', 'spradrn_5.bin'})
        for name, source in sources.items():
            for key in ('bytes', 'sha256'):
                self.assertEqual(source[key], self.scene13['source_files'][name][key])
            if name in self.world10['image_sources']:
                self.assertEqual(source, self.world10['image_sources'][name])
        self.assertEqual(self.world11['adrn_records_scanned'] * 80, sources['adrn_15.bin']['bytes'])
        self.assertEqual(self.world11['spr_index_records_scanned'] * 12, sources['spradrn_5.bin']['bytes'])

    def test_all_29_original_records_are_bounded_and_distinct(self):
        art = self.world11['decoded_static_graphics']
        self.assertEqual(len(art), 29)
        for key in ('graphic', 'adrn_ordinal', 'rd_sha256', 'indexed_sha256'):
            self.assertEqual(len({row[key] for row in art}), 29)
        for row in art:
            self.assertEqual((row['spr_index_matches'], row['rd_flag']), (0, 1))
            self.assertEqual(row['nonzero_reserved_slots'], [])
            self.assertLess(row['adrn_ordinal'], self.world11['adrn_records_scanned'])
            self.assertGreaterEqual(row['rd_offset'], 0)
            self.assertGreater(row['rd_bytes'], 16)
            self.assertLessEqual(row['rd_offset'] + row['rd_bytes'], self.world11['original_files']['real_15.bin']['bytes'])
            for key in ('adrn_sha256', 'rd_sha256', 'indexed_sha256', 'rgba_sha256', 'png_sha256'):
                self.assertTrue(re.fullmatch(r'[0-9a-f]{64}', row[key]))
        compare = self.world11['tw1_prefix_comparison']
        source = (ROOT / compare['source_receipt']).read_text()
        self.assertIn('adrn_sha256=' + compare['actual_prefixes']['adrn_15.bin']['sha256'], source)
        self.assertIn('real_sha256=' + compare['actual_prefixes']['real_15.bin']['sha256'], source)
        self.assertIn('common_prefix_bytes=315842228', source)
        self.assertEqual(compare['actual_prefixes']['adrn_15.bin']['bytes'], 10079680)
        self.assertEqual(compare['actual_prefixes']['real_15.bin']['bytes'], 315842228)
        outside = [row['graphic'] for row in art if (row['adrn_ordinal'] + 1) * 80 > 10079680
                   or row['rd_offset'] + row['rd_bytes'] > 315842228]
        self.assertEqual(outside, [10400])
        self.assertEqual(compare['outside_either_prefix'], outside)

    def test_47_placements_preserve_original_create_and_projected_anchor(self):
        placements = self.world11['map_placements']
        self.assertEqual(len(placements), 47)
        self.assertEqual(len({p['record'] for p in placements}), 47)
        self.assertEqual(Counter(p['floor'] for p in placements), {2000: 14, 3000: 17, 4000: 16})
        self.assertEqual(Counter(p['role'] for p in placements), {'TownPeople': 35, 'SignBoard': 12})
        art = {row['graphic']: row for row in self.world11['decoded_static_graphics']}
        self.assertEqual({p['graphic'] for p in placements}, set(art))
        self.assertEqual(sum(p['graphic'] == 10400 for p in placements), 2)
        world04 = {(r['floor'], r['source_CREATE_path'], r['source_CREATE_ordinal']): r for r in self.world04['rows']}
        prior = [(floor, i, row) for floor in self.world10['floors'] for i, row in enumerate(floor['anchors'], 1)]
        for placement, (floor, i, anchor) in zip(placements, prior, strict=True):
            fid = floor['floor']
            path = anchor['create_path']
            ordinal = anchor['create_ordinal']
            self.assertEqual((placement['floor'], placement['create_path'], placement['create_ordinal']), (fid, path, ordinal))
            self.assertEqual(placement['record'], f'npc-{fid}-{i}')
            self.assertEqual(placement['coordinate'], anchor['coordinate'])
            self.assertEqual(placement['role'], anchor['role'])
            self.assertEqual(placement['graphic'], int(world04[(fid, path, ordinal)]['original_graphicname_raw']))
            self.assertTrue(re.fullmatch(r'[0-9a-f]{64}', placement['create_block_sha256']))
            x, y = anchor['coordinate']
            left, top = floor['observation_png']['canvas_origin']
            px, py = (x + y) * 32 - left, (y - x) * 24 - top
            self.assertEqual(placement['marker_px'], [px, py])
            sprite = art[placement['graphic']]
            ox, oy = sprite['signed_adrn_offset']
            self.assertEqual(placement['image_px'], [px + ox, py + oy])
            self.assertEqual(placement['dimensions'], sprite['dimensions'])
            w, h = sprite['dimensions']
            cw, ch = floor['observation_png']['dimensions']
            self.assertTrue(0 <= px + ox < px + ox + w <= cw and 0 <= py + oy < py + oy + h <= ch)

    def test_private_observer_and_historical_claim_boundary(self):
        proof = self.world11
        self.assertEqual(proof['base_world10_private_zip_sha256'], self.world10['private_observer']['sha256'])
        observer = proof['observer']
        self.assertEqual(observer['members'], 34)
        maps = observer['world10_maps_with_identical_rgba']
        self.assertEqual(len(maps), 3)
        for floor in self.world10['floors']:
            original = floor['observation_png']
            check = maps[original['file']]
            self.assertEqual(check['world10_png_sha256'], original['sha256'])
            self.assertEqual(check['identical_rgba_sha256'], original['rgba_sha256'])
            self.assertTrue(re.fullmatch(r'[0-9a-f]{64}', check['world11_png_sha256']))
        self.assertEqual(observer['unchanged_original_texts_and_anchor_links'], 47)
        self.assertEqual(observer['independent_svg_crop_pixel_matches'], 3)
        self.assertIs(observer['browser_session_executed'], False)
        self.assertTrue(re.fullmatch(r'[0-9a-f]{64}', observer['sha256']))
        self.assertEqual(len(proof['bounds']), 6)
        self.assertTrue(all(flag is False for flag in proof['bounds'].values()))
        self.assertEqual(proof['continuity']['preserved_current_blob'], 'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual((proof['stage_a'], proof['stage_b'], proof['wiki'], proof['R79']),
                         ('7_PARTIAL_2_OPEN', 'GATED', 'GATED', 'PAUSED_NON_BLOCKING'))
        self.assertIsNone(proof['overall_percent'])


if __name__ == '__main__':
    unittest.main()
