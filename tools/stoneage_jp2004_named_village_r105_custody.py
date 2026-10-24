"""Verify immutable R105 source/CI report custody without inventing runtime."""
import json
from . import stoneage_jp2004_named_village_r105 as source
ROOT = source.ROOT
RECEIPT = ROOT / 'research/recovered/STONEAGE-JP2004-NAMED-VILLAGE-CUSTODY-R105.json'
RECEIPT_SHA = '5624df1c0ffd001ca051d42d14d9b15a20d5efbfc6193bac51f694c6e37fef0f'

def validate(receipt=None):
    raw = RECEIPT.read_bytes()
    source.require(source.pin(raw)['sha256'] == RECEIPT_SHA, 'Immutable receipt changed')
    locked = json.loads(raw)
    source.require(receipt is None or receipt == locked, 'Mutated receipt object')
    for path, identity in locked['evidence'].items():
        source.require(source.pin((ROOT / path).read_bytes()) == identity, 'Evidence identity changed: ' + path)
    d = source.validate(json.loads(source.SOURCE.read_bytes()))
    local = (ROOT / locked['local_report']).read_bytes()
    report = json.loads(local)
    source.require(report['source_sha256'] == source.SOURCE_SHA and report['records'] == d['records'] and
                   report['operator_rows'] == d['operator_rows'] and report['boundaries'] == d['boundaries'] and
                   report['gaps'] == d['gaps'] and report['original_server_transactions_observed'] == 0 and
                   report['contest']['planned_is_executed'] is False and
                   report['press']['authority'] == 'CONTEMPORARY_PRESS_NOT_OPERATOR_PATCH_BODY_OR_RUNTIME', 'Source semantics changed')
    source.require(len(locked['artifacts']) == 2 and {r['kind'] for r in locked['artifacts']} == {'candidate', 'main'}, 'Dual source artifacts required')
    for row in locked['artifacts']:
        source.require((ROOT / row['path']).read_bytes() == local, 'Raw source reports differ')
        source.require(source.pin(local) == row['raw_identity'], 'Raw source report identity changed')
    return {'source_commit': locked['source_commit'], 'evidence_pins': len(locked['evidence']),
            'actual_source_runs': len(locked['runs']), 'candidate_main_local_raw_equal': True,
            'original_server_transactions_observed': 0, 'operator_patch_bodies_recovered': False}

if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
