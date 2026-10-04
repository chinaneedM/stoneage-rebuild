"""Derived-only full Refresh family probe of the verified preservation bundle."""
import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_refresh_model import CALLBACK_NAME, parse_refresh_option, RefreshSourceDomain

EXPECTED_PETSKILL_SHA256='f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4'
EXPECTED_REFERENCED_IDS=(583,592)
EXPECTED_SLOT_REFERENCES=6
EXPECTED_TEMPLATES=6
# Full callback IDs must be observed from the verified file before pinning.
EXPECTED_CALLBACK_IDS=None


def analyze_runtime_objects(petskills, enemybase, *, expected_ids=EXPECTED_CALLBACK_IDS):
    entries=sorted((entry for entry in petskills.skills.values() if entry.function_name==CALLBACK_NAME),key=lambda e:e.skill_id)
    counts={entry.skill_id:0 for entry in entries};templates=set()
    for tempno,template in enemybase.templates.items():
        for skill_id in template.skill_slot_ids:
            if int(skill_id)>0 and int(skill_id) in counts:
                counts[int(skill_id)]+=1;templates.add(tempno)
    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes);status=None;converged=False
        try:
            converged=raw.decode('cp950','strict')==raw.decode('big5','strict')
            status=parse_refresh_option(raw,profile='iris',execution_charset='cp950')
        except (UnicodeDecodeError,RefreshSourceDomain):
            pass
        rows.append({'id':entry.skill_id,'field':entry.field,'target':entry.target,'cost':entry.cost,
                     'illegal':entry.illegal,'slot_references':counts[entry.skill_id],
                     'option_bytes':len(raw),'option_sha256':hashlib.sha256(raw).hexdigest(),
                     'cp950_big5_decode_converged':converged,'conditional_iris_cp950_status':status,
                     'conditional_option_safe':converged and status is not None})
    ids=tuple(entry.skill_id for entry in entries)
    referenced=tuple(sorted(key for key,value in counts.items() if value))
    references=(referenced==EXPECTED_REFERENCED_IDS and sum(counts.values())==EXPECTED_SLOT_REFERENCES
                and len(templates)==EXPECTED_TEMPLATES)
    return {'rows':rows,'callback_ids':ids,'referenced_ids':referenced,
            'slot_references':sum(counts.values()),'templates':len(templates),
            'references_match':references,'population_closed':expected_ids is not None and ids==expected_ids and references,
            'conditional_options_safe':bool(rows) and all(row['conditional_option_safe'] for row in rows)}


def emit(result):
    print('StoneAge recovered25 Refresh full callback probe — R1')
    print('No original names/descriptions/OPTION rows/assets stored. Original charset and ordered runtime OPEN.')
    print('Full-family enumeration includes unreferenced rows; initial observation does not pin population.')
    print(f"COUNT|refresh_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result['rows']:
        print('REFRESH_ROW|'+'|'.join(f'{key}={int(value) if isinstance(value,bool) else value}' for key,value in row.items()))
    print('RESOLUTION|RECOVERED25_REFRESH_POPULATION_'+('CLOSED' if result['population_closed'] else 'OPEN'))
    print('RESOLUTION|RECOVERED25_REFRESH_IRIS_CP950_OPTIONS_'+('SAFE' if result['conditional_options_safe'] else 'OPEN'))
    print('RESOLUTION|RECOVERED25_REFRESH_ORDERED_RUNTIME_OPEN')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-dir',type=Path,required=True)
    parser.add_argument('--setup',type=Path)
    for name in ('gavin','iris','bismarck'):parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
    enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
    digest=hashlib.sha256((args.data_dir/pets.source_file).read_bytes()).hexdigest()
    if digest!=EXPECTED_PETSKILL_SHA256:raise SystemExit('full petskill hash drift')
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    print('DATA_SHA256|file=petskill|sha256='+digest)
    if not result['references_match']:raise SystemExit('positive reference population drift')
    if not result['conditional_options_safe']:raise SystemExit('iris conditional CP950 option domain not admitted')
    if EXPECTED_CALLBACK_IDS is not None and not result['population_closed']:raise SystemExit('full callback population drift')
    from tools.stoneage_refresh_source_audit import analyze_profile
    options=tuple(pets.skills[key].option_bytes for key in result['callback_ids'])
    defined=unsafe=0
    for name in ('gavin','iris','bismarck'):
        source=analyze_profile(name,getattr(args,name+'_dir'),recovered_options=options)
        for row in source['native']:
            defined+=row['recovered_defined_cases'];unsafe+=row['recovered_unsafe_options']
            print('RECOVERED_NATIVE|profile='+name+'|'+'|'.join(f'{key}={int(value) if isinstance(value,bool) else value}' for key,value in row.items()))
    print(f'COUNT|recovered_defined_native_witnesses|{defined}')
    print(f'COUNT|recovered_unsafe_build_option_diagnostics|{unsafe}')
    print('RESOLUTION|RECOVERED25_REFRESH_ACTUAL_BYTES_CLOSED_CONDITIONAL_REFERENCE')


if __name__=='__main__':main()
