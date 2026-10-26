import copy
import unittest
from tools.stoneage_p3d_bench import evaluate_case,input_delta


class BenchAssessmentTests(unittest.TestCase):
    def good(self):
        return {'mode':'gdi','palette_state':{'phase':1,'palette_created':True,'getpixel_valid':True,'red_getpixel':[222,0,0],'green_getpixel':[0,200,80],
                                'foreground_matches':True,'active_matches':True,'focus_matches':True},
                'palette_capture':{'frames':[{'synthetic_control_red_pixels':19200,'synthetic_control_green_pixels':19200}]},
                'sendinput_command':{'returncode':0,'report':{'sendinput_down':1,'sendinput_up':1}},
                'before_sendinput':{'downs':1,'ups':1,'async_down_polls':12},
                'after_sendinput':{'downs':2,'ups':2,'async_down_polls':24}}

    def test_actual_rgb_and_received_input_are_accepted_only_as_synthetic(self):
        r=evaluate_case(self.good());self.assertTrue(r['color_gate_passed']);self.assertTrue(r['sendinput_gate_passed'])
        self.assertFalse(r['original_client_executed']);self.assertFalse(r['original_game_input_or_color_proven'])

    def test_successful_dispatch_without_receiver_messages_or_async_is_not_input(self):
        for key in ('downs','ups','async_down_polls'):
            c=self.good();c['after_sendinput'][key]=c['before_sendinput'][key]
            with self.subTest(key=key):self.assertFalse(evaluate_case(c)['sendinput_gate_passed'])

    def test_getpixel_or_nonuniform_capture_cannot_replace_external_known_rgb(self):
        c=self.good();c['palette_capture']['frames'][0]['synthetic_control_green_pixels']=0
        self.assertFalse(evaluate_case(c)['color_gate_passed'])
        c=self.good();c['palette_state']['red_getpixel']=[128,0,0]
        self.assertFalse(evaluate_case(c)['color_gate_passed'])

    def test_capture_failure_and_sendinput_zero_are_not_success(self):
        c=self.good();c['palette_capture']={'frames':[],'capture_error_type':'OSError'}
        self.assertFalse(evaluate_case(c)['color_gate_passed'])
        c=self.good();c['sendinput_command']['report']['sendinput_down']=0
        self.assertFalse(evaluate_case(c)['sendinput_gate_passed'])

    def test_foreground_active_and_focus_are_independent(self):
        for key in ('foreground_matches','active_matches','focus_matches'):
            c=self.good();c['palette_state'][key]=False
            with self.subTest(key=key):self.assertFalse(evaluate_case(c)['foreground_gate_passed'])

    def test_failed_directdraw_blt_cannot_be_promoted_by_leftover_colored_pixels(self):
        c=self.good();c['mode']='ddraw';c['palette_state'].update(display_bpp=8,
            ddraw=dict(create=0,cooperative=0,primary=0,offscreen_8bit=0,palette=0,offscreen_attach=0,primary_attach=0,blt=-1))
        self.assertTrue(evaluate_case(c)['known_rgb_external_capture'])
        self.assertFalse(evaluate_case(c)['color_gate_passed'])


if __name__=='__main__':unittest.main()
