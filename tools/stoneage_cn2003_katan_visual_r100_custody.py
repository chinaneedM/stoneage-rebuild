"""Immutable derived-report custody; no proprietary image payloads required."""
import hashlib
import json
from pathlib import Path
from tools.stoneage_cn2003_katan_visual_r100 import ROOT, SOURCE, validate_source, require

RECEIPT = ROOT / 'research/recovered/STONEAGE-CN2003-KATAN-NPC-VISUAL-CUSTODY-R100.json'
RECEIPT_SHA = '8de28e720622ce27b78f0cdb9ac63f050859a53f8a1a307ac226d7991ac78c79'


def verify(raw=None):
    raw = RECEIPT.read_bytes() if raw is None else raw
    require(hashlib.sha256(raw).hexdigest() == RECEIPT_SHA, 'immutable custody receipt changed')
    d = json.loads(raw)
    source = validate_source(json.loads(SOURCE.read_text()))
    for path, pin in d['evidence_pins'].items():
        b = (ROOT / path).read_bytes()
        require(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'custody evidence digest mismatch: ' + path)
        require(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == pin['git_blob'], 'custody evidence blob mismatch')
    runs = d['actual_success_runs']
    require(len(runs) == len({r['id'] for r in runs}) == 22, 'missing/duplicate source gates')
    require(all(r['status'] == 'completed' and r['conclusion'] == 'success' for r in runs), 'unpassed gate')
    require(len({a['artifact_id'] for a in d['source_artifacts']}) == 3, 'artifact reused')
    payloads = []
    for a in d['source_artifacts']:
        matches = [r for r in runs if r['id'] == a['run_id']]
        require(len(matches) == 1 and matches[0]['head'] == a['head'] and matches[0]['branch'] == a['branch'], 'artifact/source run identity mismatch')
        b = (ROOT / a['raw_report']).read_bytes()
        require(len(b) == a['raw_bytes'] and hashlib.sha256(b).hexdigest() == a['raw_sha256'], 'raw report identity mismatch')
        report = json.loads(b)
        require(report['boundaries'] == source['boundaries'] and report['observations'] == source['observations'], 'image evidence authority promoted')
        require(report['html'] == {'bytes': source['source']['initial_bytes'], 'sha256': source['source']['initial_sha256'], 'equals_initial': True}, 'false HTML intake equality')
        require(report['selected_links'] == [x['url'] for x in source['images']], 'image source changed')
        for actual, expected in zip(report['images'], source['images']):
            require(all(actual[k] == expected[k] for k in ('url', 'bytes', 'sha256', 'format', 'size', 'mode', 'frames')), 'image metadata changed')
        payloads.append(b)
    require(all(p == payloads[0] for p in payloads), 'false raw report equality')
    for p in d['historical_prefixes']:
        raw = (ROOT / p['path']).read_bytes()
        require(len(raw) > p['old_bytes'] and hashlib.sha256(raw[:p['old_bytes']]).hexdigest() == p['old_sha256'], 'historical prefix altered')
    print('R100 CUSTODY PASS: 22 real source/main gates, 3 downloaded ZIP receipts, 8 pinned evidence files; original TW1.0 identity stays OPEN')
    return True


if __name__ == '__main__':
    verify()
