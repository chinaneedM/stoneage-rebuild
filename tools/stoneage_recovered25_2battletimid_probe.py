"""Derived-only complete 2BattleTimid population and exact placement probe."""
import argparse
import hashlib
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime

CALLBACK_NAME = 'PETSKILL_2BattleTimid'
EXPECTED_PETSKILL_SHA256 = 'f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4'
EXPECTED_REFERENCED_IDS = (636,)
EXPECTED_CALLBACK_IDS = (636,)
EXPECTED_EXACT_ROWS = ((636,1,7,2,10000,2,17,'8e6b5dd952bf3bc81e522f1df382db48473b1aeec13f9ff08c7bb76d2c06f9e5',False,False,True),)
EXPECTED_TEMPLATE_ROWS = ((178,101872,(3,),(636,)),(179,101873,(3,),(636,)))


def analyze_runtime_objects(petskills, enemybase, *, expected_callback_ids=EXPECTED_CALLBACK_IDS,
                            expected_exact_rows=EXPECTED_EXACT_ROWS,
                            expected_template_rows=EXPECTED_TEMPLATE_ROWS):
    entries = sorted((e for e in petskills.skills.values() if e.function_name == CALLBACK_NAME), key=lambda e:e.skill_id)
    counts = {e.skill_id:0 for e in entries}
    templates = []
    for tempno, template in sorted(enemybase.templates.items()):
        slots = tuple(i for i, skill in enumerate(template.skill_slot_ids,1) if skill in counts)
        if not slots:
            continue
        for i in slots:
            counts[template.skill_slot_ids[i-1]] += 1
        templates.append({'tempno':tempno,'graphic_id':template.graphic_id,'skill_slots':slots,
                          'skill_ids':tuple(template.skill_slot_ids[i-1] for i in slots)})
    rows = []
    for entry in entries:
        raw = bytes(entry.option_bytes)
        try:
            cp950, big5 = raw.decode('cp950','strict'), raw.decode('big5','strict')
            codec_agrees = cp950 == big5
        except UnicodeError:
            codec_agrees = False
        rows.append({'id':entry.skill_id,'field':entry.field,'target':entry.target,'cost':entry.cost,
                     'illegal':entry.illegal,'slot_references':counts[entry.skill_id],
                     'option_bytes':len(raw),'option_sha256':hashlib.sha256(raw).hexdigest(),
                     'option_contains_nul':b'\0' in raw,'option_ascii':raw.isascii(),
                     'cp950_big5_agrees':codec_agrees})
    ids = tuple(row['id'] for row in rows)
    refs = tuple(sorted(skill for skill,count in counts.items() if count))
    uses = sum(counts.values())
    exact_rows = tuple(tuple(row[k] for k in ('id','field','target','cost','illegal','slot_references',
                       'option_bytes','option_sha256','option_contains_nul','option_ascii','cp950_big5_agrees')) for row in rows)
    exact_templates = tuple((r['tempno'],r['graphic_id'],r['skill_slots'],r['skill_ids']) for r in templates)
    return {'rows':tuple(rows),'templates':tuple(templates),'callback_ids':ids,'referenced_ids':refs,
            'slot_references':uses,'positive_references_closed':refs==EXPECTED_REFERENCED_IDS and uses==2 and len(templates)==2,
            'population_closed':expected_callback_ids is not None and ids==expected_callback_ids,
            'exact_rows_closed':expected_exact_rows is not None and exact_rows==expected_exact_rows,
            'exact_templates_closed':expected_template_rows is not None and exact_templates==expected_template_rows}


def emit(result):
    print('StoneAge recovered25 2BattleTimid probe — R1')
    print('Derived facts only; no names/descriptions/raw OPTION bytes/assets stored.')
    print('COUNT|callback_rows|'+str(len(result['rows'])))
    print('COUNT|enemybase_slot_references|'+str(result['slot_references']))
    print('COUNT|enemybase_templates|'+str(len(result['templates'])))
    for row in result['rows']:
        print('TWOBATTLETIMID_ROW|'+'|'.join(f'{k}={int(v) if isinstance(v,bool) else v}' for k,v in row.items()))
    for row in result['templates']:
        print('TWOBATTLETIMID_TEMPLATE|'+'|'.join(f'{k}={",".join(map(str,v)) if isinstance(v,tuple) else v}' for k,v in row.items()))
    for name in ('positive_references','population','exact_rows','exact_templates'):
        print('RESOLUTION|RECOVERED25_2BATTLETIMID_'+name.upper()+'_'+('CLOSED' if result[name+'_closed'] else 'OPEN'))


def main():
    p=argparse.ArgumentParser();p.add_argument('--data-dir',type=Path,required=True);p.add_argument('--setup',type=Path);p.add_argument('--discover',action='store_true')
    args=p.parse_args()
    pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
    enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
    digest=hashlib.sha256((args.data_dir/pets.source_file).read_bytes()).hexdigest()
    if digest != EXPECTED_PETSKILL_SHA256:raise SystemExit('full petskill hash drift')
    result=analyze_runtime_objects(pets,enemies);emit(result)
    print('DATA_SHA256|file=petskill|sha256='+digest)
    if not result['positive_references_closed']:raise SystemExit('2BattleTimid positive references drift')
    if args.discover:
        print('BOUNDARY|discovery_only_exact_population_and_identity_not_accepted');return
    if not all(result[k+'_closed'] for k in ('population','exact_rows','exact_templates')):
        raise SystemExit('2BattleTimid exact population/row/template identity drift')


if __name__=='__main__':main()
