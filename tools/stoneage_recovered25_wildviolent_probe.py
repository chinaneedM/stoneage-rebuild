"""Derived-only full callback population and conditional OPTION domain probe."""
import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
from tools.stoneage_wildviolent_model import CALLBACK_NAME, parse_wildviolent_option
from tools.stoneage_enemy_ai_wildviolent_bridge import validate_recovered25_wildviolent_population

EXPECTED_REFERENCED_IDS = (541,)
EXPECTED_CALLBACK_IDS = (541,652)  # Observed by verified run 37192280455.
EXPECTED_SLOT_REFERENCES = 7
EXPECTED_TEMPLATES = 7
EXPECTED_PETSKILL_SHA256 = 'f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4'


def analyze_runtime_objects(petskills, enemybase):
    entries=sorted((e for e in petskills.skills.values() if e.function_name==CALLBACK_NAME),
                   key=lambda e:e.skill_id)
    ids={e.skill_id for e in entries}
    counts={i:0 for i in ids};templates=set()
    for tempno,template in enemybase.templates.items():
        used=False
        for skill_id in template.skill_slot_ids:
            if int(skill_id)>0 and int(skill_id) in ids:
                counts[int(skill_id)]+=1;used=True
        if used:templates.add(tempno)
    rows=[]
    for entry in entries:
        raw=bytes(entry.option_bytes)
        parsed=None;converged=False;unsafe_reason='UNPARSED'
        try:
            if raw.decode('cp950','strict')!=raw.decode('big5','strict'):
                raise ValueError('encoding disagreement')
            cp=parse_wildviolent_option(raw,execution_charset='cp950')
            big=parse_wildviolent_option(raw,execution_charset='big5')
            if cp!=big:raise ValueError('execution charset disagreement')
            parsed=cp;converged=True
            unsafe_reason=('SIGNED_HIGH_SHIFT_UNDEFINED' if not 0<=cp.additive_dodge_percent_points<=32767
                           else 'NONE')
        except ValueError:
            pass
        try:
            utf8=parse_wildviolent_option(raw,execution_charset='utf-8')
        except ValueError:
            utf8=None
        rows.append({'id':entry.skill_id,'field':entry.field,'target':entry.target,
                     'cost':entry.cost,'illegal':entry.illegal,'slot_references':counts[entry.skill_id],
                     'option_bytes':len(raw),'option_sha256':hashlib.sha256(raw).hexdigest(),
                     'cp950_big5_converged':converged,
                     'attack_delta_fraction':parsed.attack_delta_fraction if parsed else None,
                     'defense_delta_fraction':parsed.defense_delta_fraction if parsed else None,
                     'additive_dodge_percent_points':parsed.additive_dodge_percent_points if parsed else None,
                     'defined_high_shift':parsed is not None and unsafe_reason=='NONE',
                     'unsafe_reason':unsafe_reason,
                     'utf8_execution_matches_conditional_cp950':parsed is not None and parsed==utf8})
    referenced=tuple(sorted(i for i,n in counts.items() if n))
    population=(tuple(e.skill_id for e in entries)==EXPECTED_CALLBACK_IDS
                and referenced==EXPECTED_REFERENCED_IDS and sum(counts.values())==EXPECTED_SLOT_REFERENCES
                and len(templates)==EXPECTED_TEMPLATES)
    return {'rows':tuple(rows),'referenced_ids':referenced,'slot_references':sum(counts.values()),
            'templates':len(templates),'population_closed':population,
            'conditional_option_domain_closed':population and all(r['defined_high_shift'] for r in rows)}


def emit(result):
    print('StoneAge recovered25 WildViolentAttack full callback probe — R1')
    print('No original names, descriptions, raw OPTION rows or assets are stored.')
    print('Complete callback population includes unreferenced ID 652, verified by initial run 37192280455.')
    print('CP950/Big5 build interpretation is conditional; original execution charset and ordered runtime OPEN.')
    print(f"COUNT|wildviolent_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result['rows']:
        print('WILDVIOLENT_ROW|'+'|'.join(f'{k}={int(v) if isinstance(v,bool) else v}' for k,v in row.items()))
    for key,tag in (('population_closed','POPULATION'),('conditional_option_domain_closed','CONDITIONAL_OPTION_DOMAIN')):
        print('RESOLUTION|RECOVERED25_WILDVIOLENT_'+tag+'_'+('CLOSED' if result[key] else 'OPEN'))
    print('RESOLUTION|RECOVERED25_WILDVIOLENT_RUNTIME_OPEN')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-dir',type=Path,required=True)
    parser.add_argument('--setup',type=Path)
    for name in ('gavin','iris','bismarck'):
        parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
    enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
    result=analyze_runtime_objects(pets,enemies)
    emit(result)
    path=args.data_dir/pets.source_file
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    print('DATA_SHA256|file=petskill|sha256='+digest)
    if digest!=EXPECTED_PETSKILL_SHA256:
        raise SystemExit('verified full petskill file hash drift')
    if not result['population_closed']:
        raise SystemExit('referenced population drift')
    validate_recovered25_wildviolent_population(pets)
    print('RESOLUTION|RECOVERED25_WILDVIOLENT_TYPED_ADMISSION_CLOSED_CONDITIONAL_CP950')
    if result['conditional_option_domain_closed']:
        from tools.stoneage_wildviolent_source_audit import analyze_profile
        options=tuple(pets.skills[i].option_bytes for i in EXPECTED_CALLBACK_IDS)
        witnesses=0
        for name in ('gavin','iris','bismarck'):
            source=analyze_profile(name,getattr(args,name+'_dir'),recovered_options=options)
            for row in source['native']:
                n=row['recovered_callback_cases'];witnesses+=n
                print(f'RECOVERED_NATIVE|profile={name}|execution_charset={row["execution_charset"]}|callback_cases={n}|UBSan=PASS')
        print(f'COUNT|recovered_native_callback_witnesses|{witnesses}')
        print('RESOLUTION|RECOVERED25_WILDVIOLENT_ACTUAL_CALLBACK_CLOSED_CONDITIONAL_CHARSET_REFERENCE')
    # An observed native-undefined OPTION is a research result to preserve,
    # not a failed build to hide or silently replace with x86 behaviour.


if __name__=='__main__':main()
