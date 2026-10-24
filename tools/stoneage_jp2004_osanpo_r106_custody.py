"""Immutable custody for a bounded manual and its derived negative-rule reports."""
import json
from . import stoneage_jp2004_osanpo_r106 as source
ROOT = source.ROOT
RECEIPT = ROOT / 'research/recovered/STONEAGE-JP2004-OSANPO-CUSTODY-R106.json'
RECEIPT_SHA = '03dfcb37f13ae671afc0079fbff8e1acd1096296e72dd793a16711870076573b'

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
    source.require(report['source_sha256'] == source.SOURCE_SHA and report['actual_page'] == d['page']['identity'] and
                   report['rules'] == d['rules'] and report['derived_blocker_table'] == source.projection_table() and
                   report['records'] == d['records'] and report['boundaries'] == d['boundaries'] and
                   report['original_server_transactions_observed'] == 0 and report['image_probe_repeated_by_ci'] is False,
                   'Bounded source semantics changed')
    audit = json.loads((ROOT / locked['local_audit']).read_bytes())
    source.require(audit['page_identity'] == report['actual_page'] and len(audit['source_mutations']) == 10 and
                   all(x['rejected_without_raw_byte_check'] is True for x in audit['source_mutations']) and
                   audit['negative_cases_are_original_server_executions'] is False and
                   [x['normalized_sha256'] for x in audit['sections']] == [x['normalized_sha256'] for x in report['sections']],
                   'Independent local audit changed')
    source.require(len(locked['artifacts']) == 2 and {x['kind'] for x in locked['artifacts']} == {'candidate', 'main'}, 'Dual source artifacts required')
    for row in locked['artifacts']:
        source.require((ROOT / row['path']).read_bytes() == local and source.pin(local) == row['raw_identity'], 'Raw source reports differ')
    return {'source_commit': locked['source_commit'], 'evidence_pins': len(locked['evidence']),
            'actual_source_runs': len(locked['runs']), 'candidate_main_local_raw_equal': True,
            'positive_success_predicate_recovered': False, 'native_skill_ids_recovered': False}

if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
