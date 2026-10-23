"""Verify immutable, derived-only R103 CI reports and their source custody."""
import json
from pathlib import Path
from . import stoneage_sachmx_version_visual_r103 as source

ROOT=source.ROOT
RECEIPT=ROOT/'research/recovered/STONEAGE-SACHMX-VERSION-VISUAL-CUSTODY-R103.json'
RECEIPT_SHA='341b295ee04206a0336fa50e534ce4355520a500ca70baf35845f64fb9fad31a'

def validate(receipt=None):
    raw=RECEIPT.read_bytes()
    source.require(source.digest(raw)==RECEIPT_SHA, 'Immutable receipt changed')
    locked=json.loads(raw)
    source.require(receipt is None or receipt==locked, 'Mutated receipt object')
    for path,expected in locked['evidence'].items():
        source.require(source.pin((ROOT/path).read_bytes())==expected, 'Evidence identity changed: '+path)
    d=source.validate_source(json.loads(source.SOURCE.read_text()))
    local=(ROOT/locked['local_report']).read_bytes()
    for row in locked['artifacts']:
        payload=(ROOT/row['path']).read_bytes()
        source.require(payload==local, 'Raw CI report differs from accepted local bytes')
        report=json.loads(payload)
        source.require(report['contract_sha256']==source.SOURCE_SHA and
                       report['records']==d['records'] and report['comparison']==d['comparison'] and
                       report['boundaries']==d['boundaries'] and
                       report['visual_observations']==d['visual_observations'], 'Replay semantics changed')
        expected={'index':d['index']}
        for article in d['articles']:
            key=article['edition'];expected[key+'_html']=article;expected[key+'_image']=article['image']
        source.require(set(report['actual_inputs'])==set(expected), 'Five actual input identities required')
        for key,actual in report['actual_inputs'].items():
            initial=expected[key]
            source.require(type(actual['equals_initial']) is bool and actual['equals_initial'] is True and
                           (actual['bytes'],actual['sha256'])==(initial['bytes'],initial['sha256']),
                           'Actual CI input identity/equality changed')
    return {'source_commit':locked['source_commit'],'evidence_pins':len(locked['evidence']),
            'actual_source_runs':len(locked['runs']),'raw_candidate_main_local_equal':True,
            'original_software_executed':False}

if __name__=='__main__':
    print(json.dumps(validate(),sort_keys=True))
