"""Replay two actual own-program observations without promoting a server boot."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_scene34_windows_gate import evaluate,pair_ok,FALSE

ROOT=Path(__file__).resolve().parents[1]
PINS={
 'STONEAGE-SCENE34-FIRST-OWN-WINDOWS-ACTUAL-R1.json':(4549,'f9e12d411d1c6d66c1fd2b5738bb2c1662e778b210c645a2acba825d85224c60'),
 'STONEAGE-SCENE34-CORRECTED-OWN-WINDOWS-ACTUAL-R1.json':(6051,'f01c0c1508fc66fe3bc1f3d4f6a441629110cdf0497a8d68df379a1af3801638'),
}

def need(ok,message):
    if not ok:raise ValueError(message)

def join(first,corrected):
    for r in (first,corrected):
        need(all(r[k]is False for k in FALSE),'own-program observation cannot become original execution')
        need(r['runner_image']=='20261021.278.1','actual Windows image')
    need(first['execution_HEAD']=='1e1976a425d3921c1b63cabd19684f1508197f8f' and first['source_action_run_id']=='41002704873','first actual source identity')
    need(corrected['execution_HEAD']=='bff50fef46d3effeb57c5626876b30cd8e62dda0' and corrected['source_action_run_id']=='41002914495','corrected actual source identity')
    need(first['finite_tcp_ipv4_gate_passed']is False and first['canary_blocked_before']['wsa_error']==10060 and first['stop']=='ISOLATION_QUALIFICATION_FAILED','retain first failed classification')
    need(pair_ok(first['loopback_before']) and pair_ok(first['loopback_after']),'first finite unblocked loopback facts retained')
    need(evaluate(corrected)is True and corrected['finite_tcp_ipv4_gate_passed']is True,'actual finite TCP gate')
    need(corrected['stop']=='PRIVATE_SOURCE_TO_WINDOWS_CHANNEL_UNAVAILABLE','private input prerequisite remains blocked')
    for key in ('loopback_before','loopback_during','loopback_after'):
        need(len(corrected[key]['jobs'])==2,'two independent one-process jobs')
    need(corrected['seconds_under_rules']==1.75,'sample duration is not watchdog duration')
    need(first['source_sha256']['tools/stoneage_scene34_windows_gate.py']==corrected['source_sha256']['tools/stoneage_scene34_windows_gate.py'] and
        first['source_sha256']['tools/stoneage_p3h_native.py']==corrected['source_sha256']['tools/stoneage_p3h_native.py'],'same observation and Job code across correction')
    need(first['source_sha256']['tools/stoneage_scene34_loopback.c']!=corrected['source_sha256']['tools/stoneage_scene34_loopback.c'],'actual connect readiness correction retained')
    return dict(actual_own_windows_runs=2,finite_tcp_ipv4_gate_passed=True,historical_server_runs=0,original_world_entered=False,
        stop='PRIVATE_SOURCE_TO_WINDOWS_CHANNEL_UNAVAILABLE')

def main():
    reports=[]
    for name,(size,digest)in PINS.items():
        # Git bytes avoid Windows checkout CRLF normalization of original reports.
        import subprocess
        path='research/recovered/'+name
        raw=subprocess.check_output(['git','show','HEAD:'+path])
        need(len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,'exact actual report bytes '+name)
        reports.append(json.loads(raw))
    result=join(*reports)
    from tools.stoneage_scene33_source_pair import validate,REPORT
    validate(json.loads(REPORT.read_text()))
    print(json.dumps(result))

if __name__=='__main__':main()
