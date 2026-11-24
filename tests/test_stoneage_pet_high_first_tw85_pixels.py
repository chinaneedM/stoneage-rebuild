"""Use archived hashes to guard scope and catalogue links without original art."""
import gzip
import json
import unittest

from tools import stoneage_pet_high_first_tw85_lookup as lookup
from tools import stoneage_pet_high_first_tw85_pixels as pixels


class TestTw85Pixels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = pixels.build_plan()
        with gzip.open(pixels.TARGET, 'rt', encoding='utf-8') as stream:
            cls.receipt = json.load(stream)

    def test_receipt_and_patch_gaps(self):
        summary = pixels.verify(self.receipt, self.plan)
        self.assertEqual(summary['portrait_aliases_with_records'], 207)
        self.assertEqual(summary['portrait_aliases_outside_patch_with_records'], 25)
        self.assertEqual(summary['portrait_records_decoded'], 207)
        self.assertEqual(summary['sampled_groups_fully_decoded'], 498)

    def test_raidisiluo_portrait_and_prior_eight_frames(self):
        archived = pixels.ROOT / 'research/recovered/tw85-rd-private-r30/SOURCE-R30.json'
        frames = json.loads(archived.read_bytes())['frames']
        self.assertEqual(len(frames), 8)
        for old in frames:
            index = self.receipt['frame_bitmap_to_adrn_index'][str(old['bitmapno'])]
            self.assertEqual(self.receipt['observed_blocks'][str(index)]['index_pixels_sha256'],
                             old['source_palette_index_sha256'])
        row, = lookup.attach_visual_routes(lookup.query(lookup.load(), name='雷帝斯洛', program='sa.exe'))
        visual = row['original_visual_candidates']
        portrait, = visual['portrait_blocks']
        self.assertEqual((portrait['bitmap'], portrait['width'], portrait['height']), (303372, 96, 104))
        self.assertFalse(row['official_live_pet_id_verified'])

    def test_preserve_executable_specific_routes(self):
        source = lookup.load()
        variants = lookup.attach_visual_routes(lookup.query(source, name='普德多基'))
        row, = variants
        self.assertEqual(row['source_program'], 'sa.exe')
        group, = row['original_visual_candidates']['sprite_groups']
        self.assertEqual(group['spr'], 102016)
        portrait, = row['original_visual_candidates']['portrait_blocks']
        self.assertEqual(portrait['status'], 'DUAL_DECODED_INDEX_PIXELS')

    def test_combined_pet12_pet13_sample_coverage(self):
        rows = lookup.attach_visual_routes(lookup.query(lookup.load(), limit=2000))
        groups = {}
        for row in rows:
            self.assertFalse(row['official_live_pet_id_verified'])
            for g in row.get('original_visual_candidates', {}).get('sprite_groups', []):
                key = g['source_group_index']
                value = g['has_complete_index_pixel_sample']
                if key in groups:
                    self.assertEqual(groups[key], value)
                groups[key] = value
        self.assertEqual(len(groups), 518)
        self.assertEqual(sum(groups.values()), 510)
        self.assertEqual({i for i,v in groups.items() if not v},
                         {1329,1369,1465,1479,1482,1495,1541,1586})
