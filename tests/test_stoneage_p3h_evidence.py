"""Adversarial provenance and observation boundaries for the original TW1 run."""
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from tools.stoneage_p3h_evidence_guard import ROOT,receiver,job,rule,verify_report,verify_visual
from tools.stoneage_p3h_windows_original import certificate_identity,surface

ACTUAL=ROOT/'research/recovered/STONEAGE-P3H-WINDOWS-ACTUAL-R1.json'

class PreflightEvidence(unittest.TestCase):
    def sample(self):
        return json.loads((ROOT/'research/recovered/STONEAGE-P3H-INVENTORY-FAILURE-ACTUAL-R1.json').read_bytes())['preflight']
    def test_actual_unchanged_sidecar_preflight_not_original_execution(self):
        p=self.sample();self.assertFalse(p['original_executed']);self.assertTrue(p['unchanged_PE_pair'])
        self.assertEqual(p['plain']['acp_before'],1252);self.assertEqual(p['external_manifest']['acp_before'],950)
        self.assertTrue(receiver(p['receiver']));job(p['job_smoke'])
    def test_dispatch_cannot_replace_real_receiver_or_screen_rgb(self):
        for edit in (lambda c:c['after_sendinput'].update(downs=c['before_sendinput']['downs']),
                     lambda c:c['palette_capture'].update(frames=[]),
                     lambda c:c['palette_state'].update(windows_acp=1252),
                     lambda c:c['palette_state'].update(foreground_matches=False)):
            c=self.sample()['receiver'];edit(c)
            with self.assertRaises(ValueError):receiver(c)
    def test_job_must_be_assigned_while_suspended_and_one_process_only(self):
        for edit in (lambda j:j.update(created_suspended=False),lambda j:j.update(assigned_before_resume=False),
                     lambda j:j.update(active_process_limit=2),lambda j:j.update(limit_flags=8)):
            j=self.sample()['job_smoke'];edit(j)
            with self.assertRaises(ValueError):job(j)
    def test_certificate_line_endings_do_not_relax_identity(self):
        b=(ROOT/'research/recovered/STONEAGE-P3H-TRANSFER-CERT.pem').read_bytes().replace(b'\r\n',b'\n')
        with TemporaryDirectory() as d:
            p=Path(d)/'cert.pem'
            for raw in (b,b.replace(b'\n',b'\r\n')):
                p.write_bytes(raw);certificate_identity(p)
            p.write_bytes(b.replace(b'MI',b'NI',1))
            with self.assertRaises(ValueError):certificate_identity(p)
    def test_missing_or_wrong_owned_surface_cannot_receive_input(self):
        exe=Path('/private/run/sa_3.exe');w=dict(klass='ＳｔｏｎｅＡｇｅ',client_size=[640,480],image=str(exe))
        self.assertEqual(surface([w],exe),w)
        for windows in ([],[w,w],[dict(w,klass='#32770')],[dict(w,image='/wrong/sa_3.exe')],[dict(w,client_size=[320,200])]):
            with self.assertRaises(ValueError):surface(windows,exe)
    def test_failure_keeps_download_and_execution_distinct(self):
        r=json.loads((ROOT/'research/recovered/STONEAGE-P3H-INVENTORY-FAILURE-ACTUAL-R1.json').read_bytes())
        self.assertTrue(r['original_downloaded']);self.assertFalse(r['original_client_executed'])
        self.assertEqual(r['error'],'original inventory changed')
        with self.assertRaises(ValueError):verify_report(r)

class ActualOriginalEvidence(unittest.TestCase):
    def sample(self):return json.loads(ACTUAL.read_bytes())
    def test_actual_source_replay(self):
        self.assertIn(verify_report(self.sample()),('ORIGINAL_WINDOW_KNOWN_EXIT_POINT_RESPONSE','ORIGINAL_WINDOW_EXIT_RESPONSE_OPEN'))
    def test_original_source_or_server_claim_mutation_rejected(self):
        for edit in (lambda r:r.update(original_world_entered=True),lambda r:r.update(original_server_contacted=True),
                     lambda r:r.update(original_client_executed=False),lambda r:r['runtime'].update(original_GetACP_directly_measured=True),
                     lambda r:r['runtime']['original_executable'].update(sha256='0'*64),
                     lambda r:r['extraction'].update(files=374)):
            r=self.sample();edit(r)
            with self.assertRaises(ValueError):verify_report(r)
    def test_denial_during_original_and_restoration_both_required(self):
        for edit in (lambda t:t['network_before'].update(connected=False),lambda t:t['network_blocked_before'].update(wsa_error=10060),
                     lambda t:t['network_blocked_after'].update(connected=True),lambda t:t['network_after_restore'].update(connected=False),
                     lambda t:t['isolation']['profiles'][0].update(Enabled=False),lambda t:t['rule_after_original'].update(program='one.exe'),
                     lambda t:t.update(job_closed_before_network_restore=False)):
            r=self.sample();edit(r['runtime'])
            with self.assertRaises(ValueError):verify_report(r)
    def test_wrong_pid_or_capture_cannot_replace_actual_original_pixels(self):
        for edit in (lambda t:t.update(pid=-1),lambda t:t.update(actual_process_image='other.exe'),
                     lambda t:[o.pop('frame',None) for o in t['observations']]):
            r=self.sample();edit(r['runtime'])
            with self.assertRaises(ValueError):verify_report(r)
    def test_forced_cleanup_cannot_be_credited_as_quit(self):
        r=self.sample();t=r['runtime'];t.update(quit_exit_before_cleanup=True,exit_before_cleanup=None)
        with self.assertRaises(ValueError):verify_report(r)
    def test_nonuniform_ime_pixels_are_not_a_verified_game_picture(self):
        r=self.sample();v=json.loads((ROOT/'research/recovered/STONEAGE-P3H-VISUAL-REVIEW-R1.json').read_bytes())
        self.assertEqual(verify_visual(r,v),'ORIGINAL_PROCESS_EXIT_COORDINATE_OBSERVED_VISUAL_DISPLAY_OPEN')
        self.assertTrue(r['runtime']['observations'][0]['frame']['nonuniform_pixels'])
        for key in ('visible_game_picture_verified','original_palette_correct_verified','original_ANSI_GDI_text_qualified',
                    'original_GetACP_directly_measured','original_world_entered','authenticated_login'):
            q=copy.deepcopy(v);q[key]=True
            with self.subTest(field=key),self.assertRaises(ValueError):verify_visual(r,q)
    def test_frame_count_or_source_hash_mismatch_cannot_be_reviewed_as_same_capture(self):
        r=self.sample();v=json.loads((ROOT/'research/recovered/STONEAGE-P3H-VISUAL-REVIEW-R1.json').read_bytes())
        for edit in (lambda q:q['frames'][0].update(nonblack_pixels=100000),
                     lambda q:q['frames'][0].update(png_sha256='0'*64),
                     lambda q:q.update(third_frame_identical_to_directly_viewed_first=False)):
            q=copy.deepcopy(v);edit(q)
            with self.assertRaises(ValueError):verify_visual(r,q)

if __name__=='__main__':unittest.main()
