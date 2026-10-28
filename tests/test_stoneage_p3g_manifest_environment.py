import copy
import json
from pathlib import Path
import unittest
from tools.stoneage_p3g_manifest_environment import (
    ROOT,VARIANTS,LAYERS,manifest,inspect_manifest,paired_namespace_result,simultaneous,validate)

def fixture():
    def probe(cp,depth):
        return dict(pointer_bytes=4,original_executed=False,acp_before=cp,acp_after_console950=cp,
                    ddraw_create=0,ddraw_current_result=0,display_bpp=depth,ddraw_current=[640,480,depth])
    control=json.loads((ROOT/'research/recovered/STONEAGE-P3D-SYNTHETIC-NATIVE-R1.json').read_text())['cases'][1]
    control['palette_state'].update(display_bpp=8,windows_acp=950)
    control['palette_state']['ddraw']['primary_attach']=0
    return {'schema':'stoneage.p3g.manifest_namespace_environment.v1',
        **{k:False for k in ('original_client_downloaded','original_client_executed','original_world_entered',
           'original_process_isolation_qualified','original_server_contacted','usable_original_environment',
           'original_ANSI_GDI_text_qualified')},
        'cases':[dict(layer=layer,**{name:probe(cp,32 if layer=='DEFAULT' else 8)
                 for name,cp in zip(VARIANTS,(1252,1252,950,65001))}) for layer in LAYERS],
        'controls':[control],'namespace_effect_observed':True,
        'same_process_display_encoding_input_candidate':True,
        'status':'SYNTHETIC_CANDIDATE_ORIGINAL_ISOLATION_OPEN'}

class P3GManifestEnvironment(unittest.TestCase):
    def test_namespaces_not_just_locale_string(self):
        for good in (False,True):
            r=inspect_manifest(manifest('zh-TW',good))
            self.assertEqual(r['correct_settings_namespace'],good)
            self.assertEqual(r['active_codepage'],'zh-TW')
    def test_old_p3f_namespace_remains_evidence_of_old_input(self):
        raw=(ROOT/'tools/stoneage_p3f_zh_tw.manifest').read_text()
        import xml.etree.ElementTree as ET
        t=ET.fromstring(raw);settings=t.find('{urn:schemas-microsoft-com:asm.v3}application')[0]
        self.assertEqual(settings.tag,'{http://schemas.microsoft.com/SMI/2019/WindowsSettings}windowsSettings')
    def test_supported_os_cannot_confound_namespace_pair(self):
        raw=manifest('zh-TW').replace('</assembly>',
            '<compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1"/></assembly>')
        with self.assertRaises(ValueError):inspect_manifest(raw)
    def test_plain_and_utf8_controls_required_for_namespace_attribution(self):
        r=fixture();self.assertTrue(paired_namespace_result(r['cases']))
        for name,cp in [('wrong_namespace_zh_tw',950),('correct_utf8',1252),('correct_zh_tw',1252)]:
            q=copy.deepcopy(r);q['cases'][0][name]['acp_before']=cp
            self.assertFalse(paired_namespace_result(q['cases']))
    def test_only_same_actual_receiving_process_qualifies(self):
        r=fixture();self.assertTrue(validate(r))
        a,b=copy.deepcopy(r['controls'][0]),copy.deepcopy(r['controls'][0])
        a['palette_state']['windows_acp']=1252;b['palette_state']['display_bpp']=32
        self.assertFalse(simultaneous(a));self.assertFalse(simultaneous(b))
    def test_dispatch_or_getpixel_cannot_replace_received_input_or_capture(self):
        for edit in (lambda c:c['palette_capture'].update(frames=[]),
                     lambda c:c['after_sendinput'].update(downs=c['before_sendinput']['downs']),
                     lambda c:c['palette_state'].update(foreground_matches=False)):
            c=fixture()['controls'][0];edit(c);self.assertFalse(simultaneous(c))
    def test_original_world_isolation_and_ansi_text_not_promoted(self):
        for k in ('original_client_downloaded','original_client_executed','original_world_entered',
                  'original_process_isolation_qualified','original_server_contacted',
                  'usable_original_environment','original_ANSI_GDI_text_qualified'):
            r=fixture();r[k]=True
            with self.subTest(field=k),self.assertRaises(ValueError):validate(r)
    def test_console_950_cannot_replace_actual_process_acp(self):
        r=fixture();r['cases'][0]['correct_zh_tw']['acp_before']=1252
        with self.assertRaises(ValueError):validate(r)
    def test_missing_case_and_architecture_rejected(self):
        r=fixture();r['cases'].pop()
        with self.assertRaises(ValueError):validate(r)
        r=fixture();r['cases'][1]['correct_zh_tw']['pointer_bytes']=8
        with self.assertRaises(ValueError):validate(r)
    def test_forged_candidate_and_old_display_state_rejected(self):
        r=fixture();r['controls']=[]
        with self.assertRaises(ValueError):validate(r)

class P3GArchivedEvidence(unittest.TestCase):
    def test_independent_source_replay(self):
        from tools.stoneage_p3g_evidence_guard import FILES,verify_report
        results=[verify_report(json.loads((ROOT/'research/recovered'/p).read_bytes())) for p in FILES]
        self.assertEqual(results,[False,True])
    def test_archived_namespace_or_identity_drift_rejected(self):
        from tools.stoneage_p3g_evidence_guard import verify_report
        r=json.loads((ROOT/'research/recovered/STONEAGE-P3G-WINDOWS2025-ACTUAL-R1.json').read_bytes())
        for edit in (lambda x:x['embedded_manifest_readback']['correct_zh_tw'].update(correct_settings_namespace=False),
                     lambda x:x.update(original_process_isolation_qualified=True),
                     lambda x:x['source_sha256'].update({'tools/stoneage_p3d_control.c':'0'*64})):
            q=copy.deepcopy(r);edit(q)
            with self.assertRaises(ValueError):verify_report(q)

class P3GBoundedIsolation(unittest.TestCase):
    def sample(self):
        rule=dict(action='Block',direction='Outbound',profile='Any',enabled='True',protocol='Any',
                  program='Any',remote_address=['Any'],local_address=['Any'])
        return dict(before={'connected':True},alternate_before={'connected':True},
            blocked={'connected':False,'wsa_error':10013},alternate_blocked={'connected':False,'wsa_error':10013},
            after_controls_blocked={'connected':False,'wsa_error':10013},after_restore={'connected':True},
            cleanup={'remaining':0},profiles=[dict(Name=p,Enabled=True) for p in ('Domain','Private','Public')],
            rule=rule,after_controls_rule=copy.deepcopy(rule),watchdog={'registered':True,'user':'SYSTEM'},
            probe_during_block={'acp_before':950,'display_bpp':8},controls_during_block=fixture()['controls'])
    def test_bounded_qualified_metadata(self):
        from tools.stoneage_p3g_isolation import qualifies
        self.assertTrue(qualifies(self.sample()))
    def test_timeout_dead_endpoint_or_early_restore_cannot_pass(self):
        from tools.stoneage_p3g_isolation import qualifies
        for edit in (lambda r:r['before'].update(connected=False),
                     lambda r:r['blocked'].update(wsa_error=10060),
                     lambda r:r['after_controls_blocked'].update(connected=True),
                     lambda r:r['after_restore'].update(connected=False),
                     lambda r:r['cleanup'].update(remaining=1)):
            r=self.sample();edit(r);self.assertFalse(qualifies(r))
    def test_both_program_paths_and_all_profiles_required(self):
        from tools.stoneage_p3g_isolation import qualifies
        for edit in (lambda r:r['alternate_blocked'].update(connected=True),
                     lambda r:r.update(profiles=[]),lambda r:r['profiles'][0].update(Enabled=False),
                     lambda r:r['rule'].update(program='one.exe'),lambda r:r['after_controls_rule'].update(protocol='TCP')):
            r=self.sample();edit(r);self.assertFalse(qualifies(r))
    def test_display_while_blocked_cannot_come_from_other_process(self):
        from tools.stoneage_p3g_isolation import qualifies
        r=self.sample();r['controls_during_block'][0]['palette_state']['windows_acp']=1252
        self.assertFalse(qualifies(r))
    def test_actual_archived_isolation_and_no_scope_promotion(self):
        from tools.stoneage_p3g_evidence_guard import verify_isolation
        r=json.loads((ROOT/'research/recovered/STONEAGE-P3G-ISOLATION-ACTUAL-R1.json').read_bytes())
        self.assertTrue(verify_isolation(r))
        for k in ('original_world_entered','original_process_isolation_qualified','IPv6_and_UDP_empirically_tested','loopback_server_qualified'):
            q=copy.deepcopy(r);q[k]=True
            with self.assertRaises(ValueError):verify_isolation(q)
        r=fixture();r['cases'][1]['correct_zh_tw']['ddraw_current'][2]=32
        with self.assertRaises(ValueError):validate(r)

if __name__=='__main__':unittest.main()
