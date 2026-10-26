import copy
import json
import unittest
from tools import stoneage_p3c_evidence_guard as g


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.display=json.loads((g.RECOVERED/'STONEAGE-TW10-ORIGINAL-LOGIN-P3C-DISPLAY-R1.json').read_text())
        self.original=json.loads((g.RECOVERED/'STONEAGE-TW10-ORIGINAL-LOGIN-P3C-ORIGINAL-R1.json').read_text())

    def test_real_reports_preserve_calibration_and_input_boundaries(self):
        g.calibration(self.display);g.fullscreen_failure(self.original)

    def test_known_rgb_cannot_be_replaced_with_merely_nonuniform_pixels(self):
        self.display['x11_known_rgb_control']['windows'][0]['map']['synthetic_control_green_pixels']=0
        with self.assertRaises(ValueError):g.calibration(self.display)

    def test_wrong_colormap_negative_control_and_wine_claim_cannot_be_dropped(self):
        r=copy.deepcopy(self.display)
        r['x11_known_rgb_control']['windows'][0]['same_indices_different_colormap_rgb']=False
        with self.assertRaises(ValueError):g.calibration(r)
        self.display['wine_known_rgb_preserved']=not self.display['wine_known_rgb_preserved']
        with self.assertRaises(ValueError):g.calibration(self.display)

    def test_private_frame_and_finite_input_scope_cannot_be_promoted(self):
        r=copy.deepcopy(self.original)
        r['original_window_colormaps']['windows'][0]['sealed_private_frame']['plaintext_sha256']='0'*64
        with self.assertRaises(ValueError):g.fullscreen_failure(r)
        self.original['input_observation']['account_or_password_entered']=True
        with self.assertRaises(ValueError):g.fullscreen_failure(self.original)

    def test_cleanup_or_input_dispatch_failure_is_not_an_observed_quit(self):
        r=copy.deepcopy(self.original)
        r['input_observation']['click_returncode']=1
        with self.assertRaises(ValueError):g.fullscreen_failure(r)
        i=self.original['input_observation'];i['launcher_returncode_after']=None
        i['exit_observed_before_cleanup']=True
        with self.assertRaises(ValueError):g.fullscreen_failure(self.original)

    def test_crash_debugger_history_cannot_be_deleted_to_promote_fullscreen(self):
        for o in self.original['observations']:
            o['windows']['windows']=[w for w in o['windows']['windows'] if not w['image_path'].lower().endswith('winedbg.exe')]
        with self.assertRaises(ValueError):g.fullscreen_failure(self.original)


if __name__=='__main__':unittest.main()
