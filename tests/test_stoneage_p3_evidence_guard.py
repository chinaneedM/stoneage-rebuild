"""Semantic corruptions must fail even after a new report digest is computed."""
import copy
import json
import unittest
from tools import stoneage_p3_evidence_guard as g


class P3EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.native = json.loads((g.RECOVERED / 'STONEAGE-TW10-ORIGINAL-BOOT-P3-DEPTH8-ORIGINAL-R1.json').read_text())
        self.control = json.loads((g.RECOVERED / 'STONEAGE-TW10-ORIGINAL-BOOT-P3-DEPTH8-DISPLAY-R1.json').read_text())

    def test_actual_native_baseline_and_synthetic_depth_are_distinct(self):
        g.native(self.native, modal=False)
        g.synthetic(self.control, 8)
        with self.assertRaises(ValueError):
            g.synthetic(self.native, 8)

    def test_window_title_without_original_image_ownership_is_rejected(self):
        for obs in self.native['observations']:
            for w in obs['windows']['windows']:
                w['image_path'] = 'Z:\\synthetic.exe'
        with self.assertRaises(ValueError):
            g.native(self.native, modal=False)

    def test_world_visual_and_network_promotions_are_rejected(self):
        for key in ('game_world_entered', 'authentic_game_display_visually_verified', 'assistant_viewed_original'):
            r = copy.deepcopy(self.native)
            r[key] = True
            with self.subTest(key=key), self.assertRaises(ValueError):
                g.native(r, modal=False)
        self.native['network']['interfaces'].append('eth0')
        with self.assertRaises(ValueError):
            g.native(self.native, modal=False)

    def test_external_endpoint_or_changed_original_is_rejected(self):
        r = copy.deepcopy(self.native)
        r['original_launch_args'][-1] = 'IP:0:192.0.2.1:9'
        with self.assertRaises(ValueError):
            g.native(r, modal=False)
        self.native['source_executable']['sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            g.native(self.native, modal=False)

    def test_offscreen_8bit_success_does_not_replace_actual_display_mode(self):
        self.control['synthetic_control']['current_display_bpp'] = 32
        with self.assertRaises(ValueError):
            g.synthetic(self.control, 8)


if __name__ == '__main__':
    unittest.main()
