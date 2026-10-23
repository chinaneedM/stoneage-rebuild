"""Verify permanent R101 derived evidence after temporary source-artifact expiry."""
import hashlib
import json
from tools.stoneage_tw10_animation_selector_r101 import ROOT, REPORT, EXE_SHA, require

RECEIPT = ROOT / 'research/recovered/STONEAGE-TW10-ANIMATION-SELECTOR-CUSTODY-R101.json'
RECEIPT_SHA = 'fe471122dacf9bcb0fe3e28c0704c65a04cc3c5dd044ab4baf6ddc6f8d89d345'


def verify(raw=None):
    raw = RECEIPT.read_bytes() if raw is None else raw
    require(hashlib.sha256(raw).hexdigest() == RECEIPT_SHA, 'immutable custody receipt changed')
    d = json.loads(raw)
    for path, pin in d['evidence_pins'].items():
        b = (ROOT / path).read_bytes()
        require(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'evidence digest changed: ' + path)
        require(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == pin['git_blob'], 'evidence blob changed')
    runs = d['actual_content_runs']
    require(len(runs) == len({r['id'] for r in runs}) == 21, 'missing/duplicate content gates')
    require(all(r['status'] == 'completed' and r['conclusion'] == 'success' for r in runs), 'source or main gate not passed')
    source = json.loads(REPORT.read_text())
    require(source['runtime']['sha256'] == EXE_SHA and source['boundaries'] == d['boundaries'], 'original source or authority changed')
    artifacts = d['source_artifacts']
    require(len(artifacts) == len({x['artifact_id'] for x in artifacts}) == 2, 'artifact reused/missing')
    for a in artifacts:
        run = next((r for r in runs if r['id'] == a['run_id']), None)
        require(run and run['head'] == a['head'] and run['branch'] == a['branch'], 'artifact run identity mismatch')
        b = (ROOT / a['raw_report']).read_bytes()
        require(b == REPORT.read_bytes() and hashlib.sha256(b).hexdigest() == a['raw_sha256'], 'source replay bytes changed')
        report = json.loads(b)
        require(report['instrumentation']['whole_client_or_server_executed'] is False, 'bounded emulation promoted to whole-client execution')
        require(len(report['native_selector_replays']) == len(report['native_countdown_replays']) == 10, 'bounded replay set changed')
        require(all(x['native'] == x['reference'] for x in report['native_selector_replays']), 'selector replay mismatch')
        require(all(x['native_result'] == x['reference_result'] for x in report['native_countdown_replays']), 'countdown replay mismatch')
    for p in d['historical_prefixes']:
        raw = (ROOT / p['path']).read_bytes()
        require(len(raw) > p['old_bytes'] and hashlib.sha256(raw[:p['old_bytes']]).hexdigest() == p['old_sha256'], 'old history prefix altered')
    print('R101 CUSTODY PASS: original source/main reports, 21 actual gates, exact source hashes and bounded native semantics retained')
    return True


if __name__ == '__main__':
    verify()
