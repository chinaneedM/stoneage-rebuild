"""Synthetic negative admission tests, never a historical program or live socket."""
import copy
import json
from pathlib import Path
import unittest
from tools import stoneage_scene34_windows_gate as m
from tools import stoneage_scene34_evidence_guard as g


def fixture():
    job=dict(created_suspended=True,assigned_before_resume=True,limit_flags=0x2008,active_process_limit=1)
    pair=dict(server_exit=0,client_exit=0,server_pid=100,client_pid=200,
        ready=dict(ready=True,bind_address='127.0.0.1',port=19200,pointer_bytes=4,pid=100),
        server=dict(connected=True,echo_exact=True,wsa_error=0,pid=100),
        client=dict(connected=True,echo_exact=True,wsa_error=0,pid=200),
        image_identity_verified=True,jobs=[job.copy(),job.copy()])
    rules=[dict(name=n,direction=d,action='Block',enabled='True',profile='Any',program='Any',protocol='Any')for n,d in zip(m.RULES,('Outbound','Inbound'))]
    return dict(scope='OWN_X86_TWO_PROCESS_TCP_IPV4_LOOPBACK_AND_ONE_EXTERNAL_CANARY',error=None,
        isolation=dict(rules=rules,profiles=[dict(Enabled=True)for _ in range(3)],watchdog=dict(registered=True,user='SYSTEM')),
        rules_before_restore=copy.deepcopy(rules),loopback_before=copy.deepcopy(pair),loopback_during=copy.deepcopy(pair),loopback_after=copy.deepcopy(pair),
        canary_before=dict(connected=True),canary_after=dict(connected=True),
        canary_blocked_before=dict(connected=False,wsa_error=10013),canary_blocked_after=dict(connected=False,wsa_error=10013),
        cleanup=dict(remaining=0),jobs_closed_before_network_restore=True,hold_cleanup_observed=True,seconds_under_rules=20,
        **{k:False for k in m.FALSE})


class FiniteGate(unittest.TestCase):
    def setUp(self):self.r=fixture()

    def test_complete_synthetic_fixture_is_finite_gate_only(self):
        self.assertTrue(m.evaluate(self.r));self.assertFalse(self.r['original_execution_admitted'])

    def test_each_original_or_universal_network_promotion_rejected(self):
        for field in m.FALSE:
            with self.subTest(field=field):
                r=fixture();r[field]=True
                with self.assertRaisesRegex(ValueError,'not original server'):m.evaluate(r)

    def test_scope_cannot_be_all_ipv6_udp_or_original_protocol(self):
        self.r['scope']='ALL_NETWORKS'
        with self.assertRaisesRegex(ValueError,'bounded experiment'):m.evaluate(self.r)

    def test_external_timeout_is_not_policy_refusal(self):
        self.r['canary_blocked_before']['wsa_error']=10060;self.assertFalse(m.evaluate(self.r))

    def test_live_external_canary_required_before_and_after(self):
        for field in ('canary_before','canary_after'):
            r=fixture();r[field]['connected']=False;self.assertFalse(m.evaluate(r))

    def test_external_path_must_still_be_blocked_after_loopback(self):
        self.r['canary_blocked_after']['connected']=True;self.assertFalse(m.evaluate(self.r))

    def test_both_rule_directions_required(self):
        self.r['isolation']['rules'].pop();self.assertFalse(m.evaluate(self.r))

    def test_exact_program_rule_cannot_be_all_programs(self):
        self.r['isolation']['rules'][0]['program']='one.exe';self.assertFalse(m.evaluate(self.r))

    def test_all_profiles_must_be_enabled(self):
        self.r['isolation']['profiles'][2]['Enabled']=False;self.assertFalse(m.evaluate(self.r))

    def test_restore_watchdog_required(self):
        self.r['isolation']['watchdog']['registered']=False;self.assertFalse(m.evaluate(self.r))

    def test_echo_bytes_cannot_be_inferred_from_bind_or_connect(self):
        self.r['loopback_during']['client']['echo_exact']=False;self.assertFalse(m.evaluate(self.r))

    def test_two_distinct_processes_required(self):
        self.r['loopback_during']['client_pid']=100;self.assertFalse(m.evaluate(self.r))

    def test_pid_from_other_observation_rejected(self):
        self.r['loopback_during']['server']['pid']=101;self.assertFalse(m.evaluate(self.r))

    def test_non_loopback_bind_rejected(self):
        self.r['loopback_during']['ready']['bind_address']='0.0.0.0';self.assertFalse(m.evaluate(self.r))

    def test_x64_does_not_qualify_x86(self):
        self.r['loopback_during']['ready']['pointer_bytes']=8;self.assertFalse(m.evaluate(self.r))

    def test_image_ownership_and_assign_before_resume_required(self):
        for mutate in [lambda r:r['loopback_during'].update(image_identity_verified=False),
                       lambda r:r['loopback_during']['jobs'][0].update(assigned_before_resume=False)]:
            r=fixture();mutate(r);self.assertFalse(m.evaluate(r))

    def test_after_restore_echo_required(self):
        self.r['loopback_after']['server_exit']=1;self.assertFalse(m.evaluate(self.r))

    def test_active_process_and_cleanup_limits_required(self):
        self.r['loopback_during']['jobs'][0]['active_process_limit']=2;self.assertFalse(m.evaluate(self.r))

    def test_cleanup_before_restore_required(self):
        self.r['jobs_closed_before_network_restore']=False;self.assertFalse(m.evaluate(self.r))

    def test_cleanup_leftovers_rejected(self):
        self.r['cleanup']['remaining']=1;self.assertFalse(m.evaluate(self.r))

    def test_failed_observation_does_not_pass(self):
        self.r['error']='actual native failure';self.assertFalse(m.evaluate(self.r))

    def test_probe_deadline_not_watchdog_duration(self):
        self.r['seconds_under_rules']=121;self.assertFalse(m.evaluate(self.r))


class ActualEvidenceJoin(unittest.TestCase):
    def setUp(self):
        self.first,self.corrected=[json.loads((g.ROOT/'research/recovered'/name).read_bytes())for name in g.PINS]

    def test_two_actual_reports_keep_original_execution_zero(self):
        self.assertEqual(g.join(self.first,self.corrected)['historical_server_runs'],0)

    def test_first_timeout_cannot_be_retrospectively_changed_to_refusal(self):
        self.first['canary_blocked_before']['wsa_error']=10013
        with self.assertRaisesRegex(ValueError,'first failed'):g.join(self.first,self.corrected)

    def test_original_execution_promotion_rejected(self):
        self.corrected['original_server_boot_attempted']=True
        with self.assertRaisesRegex(ValueError,'cannot become original'):g.join(self.first,self.corrected)

    def test_private_transfer_gap_cannot_be_erased(self):
        self.corrected['stop']='SERVER_READY'
        with self.assertRaisesRegex(ValueError,'private input prerequisite'):g.join(self.first,self.corrected)

    def test_actual_source_run_identity_required(self):
        self.corrected['source_action_run_id']='40977201848'
        with self.assertRaisesRegex(ValueError,'corrected actual source'):g.join(self.first,self.corrected)

    def test_two_jobs_cannot_be_dropped(self):
        self.corrected['loopback_during']['jobs']=[]
        with self.assertRaisesRegex(ValueError,'independent one-process'):g.join(self.first,self.corrected)

    def test_watchdog_minutes_not_measured_block_duration(self):
        self.corrected['seconds_under_rules']=90
        with self.assertRaisesRegex(ValueError,'sample duration'):g.join(self.first,self.corrected)


if __name__=='__main__':unittest.main()
