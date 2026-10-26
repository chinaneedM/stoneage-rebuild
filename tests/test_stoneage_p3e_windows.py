import copy
import json
import unittest
from tools.stoneage_p3e_windows import qualify,evaluate_network
from tools.stoneage_p3e_evidence_guard import verify_report,RECOVERED

class QualificationTests(unittest.TestCase):
    def good_control(self):
        r=json.loads((RECOVERED/'STONEAGE-P3D-SYNTHETIC-NATIVE-R1.json').read_bytes())
        c=r['cases'][1];c['palette_state']['display_bpp']=8;c['palette_state']['windows_acp']=950
        c['palette_state']['ddraw']['primary_attach']=0
        return c
    def test_simultaneous_actual_prerequisites(self):
        self.assertTrue(qualify([self.good_control()]))
        for field,value in [('display_bpp',32),('windows_acp',1252),('foreground_matches',False)]:
            c=self.good_control();c['palette_state'][field]=value
            with self.subTest(field=field):self.assertFalse(qualify([c]))
    def test_capabilities_from_different_processes_cannot_be_combined(self):
        c=self.good_control();other=copy.deepcopy(c)
        c['palette_state']['windows_acp']=1252;other['palette_state']['display_bpp']=32
        self.assertFalse(qualify([c,other]))
    def test_rgb_and_received_input_still_required_for_8bit950(self):
        c=self.good_control();c['palette_capture']['frames']=[]
        self.assertFalse(qualify([c]))
        c=self.good_control();c['after_sendinput']['async_down_polls']=c['before_sendinput']['async_down_polls']
        self.assertFalse(qualify([c]))
    def network(self):
        return {'before':{'connected':True},'blocked_attempt':{'connected':False,'wsa_error':10013},
            'unblocked_copy_during_rule':{'connected':True},'after_removal':{'connected':True},
            'cleanup':{'remaining':0},'rule':{'direction':'Outbound','action':'Block','enabled':'True','profile':'Any'},
            'profiles':[{'Enabled':True}]}
    def test_firewall_requires_actual_denial_and_live_control(self):
        self.assertTrue(evaluate_network(self.network()))
        for phase in ('before','unblocked_copy_during_rule','after_removal'):
            n=self.network();n[phase]['connected']=False
            with self.subTest(phase=phase):self.assertFalse(evaluate_network(n))
        n=self.network();n['blocked_attempt']['wsa_error']=10060
        self.assertFalse(evaluate_network(n))
    def test_rule_creation_or_profile_disabled_cannot_replace_network_observation(self):
        for field,value in [('direction','Inbound'),('action','Allow'),('enabled','False'),('profile','Private')]:
            n=self.network();n['rule'][field]=value
            with self.subTest(field=field):self.assertFalse(evaluate_network(n))
        n=self.network();n['profiles'][0]['Enabled']=False;self.assertFalse(evaluate_network(n))
        n=self.network();n['blocked_attempt']['connected']=True;self.assertFalse(evaluate_network(n))

class ArchivedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.report=json.loads((RECOVERED/'STONEAGE-P3E-WINDOWS-ACTUAL-R1.json').read_bytes())
    def test_actual_report(self):verify_report(self.report)
    def test_original_claims_rejected(self):
        for k in ('original_executed','usable_original_environment','original_process_isolation_qualified'):
            r=copy.deepcopy(self.report);r[k]=True
            with self.subTest(k=k),self.assertRaises(ValueError):verify_report(r)
    def test_console_950_does_not_promote_wrong_actual_acp(self):
        self.report['display_encoding_input_candidate_found']=True
        with self.assertRaises(ValueError):verify_report(self.report)
    def test_compatibility_request_cannot_replace_actual_rgb_or_input(self):
        c=self.report['cases'][1]['controls'][1];c['assessment']['color_gate_passed']=not c['assessment']['color_gate_passed']
        with self.assertRaises(ValueError):verify_report(self.report)
    def test_firewall_scope_cannot_be_promoted(self):
        self.report['network']['original_process_isolation_qualified']=True
        with self.assertRaises(ValueError):verify_report(self.report)
    def test_one_failed_control_or_cleanup_exit_is_not_complete_source(self):
        self.report['cases'][0]['controls'][0]['process_exit_before_cleanup']=None
        with self.assertRaises(ValueError):verify_report(self.report)

if __name__=='__main__':unittest.main()
