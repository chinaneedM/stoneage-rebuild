"""Derived-only AttackCrazed population/OPTION gate for verified bundle data."""
import argparse
import hashlib
from pathlib import Path
from tools.stoneage_attack_crazed_model import CALLBACK_NAME, parse_attack_crazed_option
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime

EXPECTED_IDS = (613,)
EXPECTED_SLOT_REFERENCES = 9
EXPECTED_TEMPLATES = 9


def analyze_runtime_objects(petskills, enemybase):
    entries=sorted((e for e in petskills.skills.values() if e.function_name==CALLBACK_NAME),key=lambda e:e.skill_id)
    ids={e.skill_id for e in entries}; references=0; templates=set()
    for tempno, template in enemybase.templates.items():
        uses=sum(int(i) in ids for i in template.skill_slot_ids if int(i)>0)
        references+=uses
        if uses:templates.add(tempno)
    rows=[]
    for e in entries:
        raw=bytes(e.option_bytes); count=None
        try:count=parse_attack_crazed_option(raw)
        except ValueError:pass
        rows.append({'id':e.skill_id,'field':e.field,'target':e.target,'cost':e.cost,'illegal':e.illegal,
                     'option_bytes':len(raw),'option_sha256':hashlib.sha256(raw).hexdigest(),
                     'attack_count':count,'safe_count':count is not None,'option_nul_free':b'\0' not in raw})
    population=tuple(r['id'] for r in rows)==EXPECTED_IDS and references==EXPECTED_SLOT_REFERENCES and len(templates)==EXPECTED_TEMPLATES
    return {'rows':tuple(rows),'slot_references':references,'templates':len(templates),'population_closed':population,
            'option_domain_closed':population and all(r['safe_count'] for r in rows)}


def emit(r):
    print('StoneAge recovered25 AttackCrazed domain probe — R1')
    print('No original names, descriptions, raw OPTION text or source rows are stored.')
    print(f"COUNT|attackcrazed_skill_rows|{len(r['rows'])}")
    print(f"COUNT|enemybase_slot_references|{r['slot_references']}")
    print(f"COUNT|enemybase_templates|{r['templates']}")
    for row in r['rows']:print('ATTACKCRAZED_ROW|'+'|'.join(f'{k}={int(v) if isinstance(v,bool) else v}' for k,v in row.items()))
    for key,tag in [('population_closed','POPULATION'),('option_domain_closed','OPTION_DOMAIN')]:
        print('RESOLUTION|RECOVERED25_ATTACKCRAZED_'+tag+'_'+('CLOSED' if r[key] else 'OPEN'))


def main():
    p=argparse.ArgumentParser();p.add_argument('--data-dir',type=Path,required=True);p.add_argument('--setup',type=Path)
    a=p.parse_args();r=analyze_runtime_objects(load_recovered25_petskill_runtime(data_dir=a.data_dir,setup=a.setup),
                                             load_recovered25_enemybase_runtime(data_dir=a.data_dir,setup=a.setup))
    emit(r)
    if not r['option_domain_closed']:raise SystemExit('AttackCrazed data gate remains open')
if __name__=='__main__':main()
