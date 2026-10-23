"""Immutable, derived-only custody of the accepted R104 source reports."""
import json
from . import stoneage_cn20_named_pet_visual_r104 as source
ROOT=source.ROOT
RECEIPT=ROOT/'research/recovered/STONEAGE-CN20-NAMED-PET-VISUAL-CUSTODY-R104.json'
RECEIPT_SHA='c93267433fc549db269a879eb7c6398d6041440f96e7283bdda5f3b269991615'

def validate(receipt=None):
    raw=RECEIPT.read_bytes();source.require(source.sha(raw)==RECEIPT_SHA,'Immutable receipt changed')
    locked=json.loads(raw);source.require(receipt is None or receipt==locked,'Mutated receipt object')
    for path,expected in locked['evidence'].items():source.require(source.pin((ROOT/path).read_bytes())==expected,'Evidence identity changed: '+path)
    d=source.validate(json.loads(source.SOURCE.read_text()))
    local=(ROOT/locked['local_report']).read_bytes()
    for row in locked['artifacts']:
        payload=(ROOT/row['path']).read_bytes();source.require(payload==local,'Raw source reports differ')
        report=json.loads(payload)
        source.require(report['source_sha256']==source.SOURCE_SHA and report['actual_page']==d['page']['identity'] and
                       report['selected_cells']==d['selected_cells'] and report['records']==d['records'] and
                       report['boundaries']==d['boundaries'] and report['new_species_count'] is None and
                       report['manual_review_repeated_by_ci'] is False,'Bounded source semantics changed')
        actual=report['actual_images'];source.require(len(actual)==3,'Three actual images required')
        for result,expected in zip(actual,d['images']):
            source.require(result=={k:expected[k] for k in ['ordinal','actual_url','capture','bytes','sha256','decoded']},'Image source/capture identity changed')
    return {'source_commit':locked['source_commit'],'evidence_pins':len(locked['evidence']),
            'actual_source_runs':len(locked['runs']),'candidate_main_local_raw_equal':True,
            'native_game_species_ids_recovered':False}
if __name__=='__main__':print(json.dumps(validate(),sort_keys=True))
