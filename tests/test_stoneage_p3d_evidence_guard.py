import copy
import json
import unittest
from tools import stoneage_p3d_evidence_guard as g


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.wine=json.loads((g.RECOVERED/'STONEAGE-P3D-SYNTHETIC-WINE8-R1.json').read_text())
        self.native=json.loads((g.RECOVERED/'STONEAGE-P3D-SYNTHETIC-NATIVE-R1.json').read_text())

    def test_actual_reports_replay(self):
        for suffix in ('WINE8','WINE24','NATIVE'):
            g.verify_report(json.loads((g.RECOVERED/('STONEAGE-P3D-SYNTHETIC-'+suffix+'-R1.json')).read_text()))

    def test_failed_real_rgb_cannot_be_promoted_by_successful_calls(self):
        self.wine['cases'][0]['assessment']['color_gate_passed']=True
        with self.assertRaises(ValueError):g.verify_report(self.wine)

    def test_sendinput_success_without_receiver_counters_is_rejected(self):
        c=self.native['cases'][0]
        c['after_sendinput']['downs']=c['before_sendinput']['downs']
        with self.assertRaises(ValueError):g.verify_report(self.native)

    def test_native_32bpp_and_wrong_acp_are_not_original_preflight(self):
        self.native['original_rerun_prerequisite_synthetic_8bit_passed']=True
        with self.assertRaises(ValueError):g.verify_report(self.native)

    def test_cleanup_is_not_program_exit(self):
        self.native['cases'][0]['process_exit_before_cleanup']=None
        with self.assertRaises(ValueError):g.verify_report(self.native)

    def test_original_execution_claims_are_rejected(self):
        for key in ('original_client_downloaded','original_client_executed','original_game_world_entered'):
            d=copy.deepcopy(self.native);d[key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):g.verify_report(d)

    def test_wine_host_namespace_or_external_interface_cannot_be_accepted(self):
        d=copy.deepcopy(self.wine);d['network']['child_net_namespace']=d['network']['host_net_namespace']
        with self.assertRaises(ValueError):g.verify_report(d)
        self.wine['network']['interfaces'].append('eth0')
        with self.assertRaises(ValueError):g.verify_report(self.wine)

    def test_native_network_isolation_must_not_be_invented(self):
        self.native['network_scope']='isolated native OS'
        with self.assertRaises(ValueError):g.verify_report(self.native)

    def test_actual_server_absence_accepts_nonzero_kill_but_not_living_server(self):
        d=json.loads((g.RECOVERED/'STONEAGE-P3D-SYNTHETIC-PRIVATE-COLORMAP-R1.json').read_text())
        self.assertEqual(d['wine_restart_observation']['kill_returncode'],1)
        g.verify_report(d)
        d['wine_restart_observation']['living_server_pids_after_wait']=[42]
        with self.assertRaises(ValueError):g.verify_report(d)

    def test_private_colormap_registry_success_cannot_replace_readback_and_restart(self):
        d=json.loads((g.RECOVERED/'STONEAGE-P3D-SYNTHETIC-PRIVATE-COLORMAP-R1.json').read_text())
        d['wine_x11_configuration']['registry_write_and_readback_passed']=False
        with self.assertRaises(ValueError):g.verify_report(d)


if __name__=='__main__':unittest.main()
