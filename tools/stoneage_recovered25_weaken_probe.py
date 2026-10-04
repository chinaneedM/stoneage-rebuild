"""Derived-only Weaken population/OPTION gate for verified bundle data."""
import argparse
import hashlib
from pathlib import Path

from tools.stoneage_weaken_model import CALLBACK_NAME, parse_weaken_option
from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime

EXPECTED_IDS = (575, 576)
EXPECTED_SLOT_REFERENCES = 7
EXPECTED_TEMPLATES = 6


def analyze_runtime_objects(petskills, enemybase):
    entries = sorted((e for e in petskills.skills.values() if e.function_name == CALLBACK_NAME),
                     key=lambda e: e.skill_id)
    ids = {e.skill_id for e in entries}
    references = 0
    templates = set()
    for tempno, template in enemybase.templates.items():
        uses = sum(int(i) in ids for i in template.skill_slot_ids if int(i) > 0)
        references += uses
        if uses:
            templates.add(tempno)
    rows = []
    for e in entries:
        raw = bytes(e.option_bytes)
        option = None
        try:
            cp = parse_weaken_option(raw, encoding='cp950')
            big = parse_weaken_option(raw, encoding='big5')
            if cp != big or raw.decode('cp950') != raw.decode('big5'):
                raise ValueError('encoding disagreement')
            option = cp
        except ValueError:
            pass
        rows.append({
            'id': e.skill_id, 'field': e.field, 'target': e.target,
            'cost': e.cost, 'illegal': e.illegal, 'option_bytes': len(raw),
            'option_sha256': hashlib.sha256(raw).hexdigest(),
            'status_index': option.status_index if option else None,
            'turn': option.turn if option else None,
            'success_offset': option.success_offset if option else None,
            'safe_option': option is not None and option.turn > 0 and option.success_offset > 0,
            'option_nul_free': b'\0' not in raw,
        })
    population = (tuple(r['id'] for r in rows) == EXPECTED_IDS
                  and references == EXPECTED_SLOT_REFERENCES
                  and len(templates) == EXPECTED_TEMPLATES)
    return {'rows': tuple(rows), 'slot_references': references,
            'templates': len(templates), 'population_closed': population,
            'option_domain_closed': population and all(r['safe_option'] for r in rows)}


def emit(result):
    print('StoneAge recovered25 Weaken domain probe — R1')
    print('No original names, descriptions, raw OPTION text or source rows are stored.')
    print('Reference/data closure does not imply ordered-runtime acceptance.')
    print(f"COUNT|weaken_skill_rows|{len(result['rows'])}")
    print(f"COUNT|enemybase_slot_references|{result['slot_references']}")
    print(f"COUNT|enemybase_templates|{result['templates']}")
    for row in result['rows']:
        print('WEAKEN_ROW|' + '|'.join(
            f'{k}={int(v) if isinstance(v, bool) else v}' for k, v in row.items()))
    for key, tag in [('population_closed', 'POPULATION'), ('option_domain_closed', 'OPTION_DOMAIN')]:
        print('RESOLUTION|RECOVERED25_WEAKEN_' + tag + '_' +
              ('CLOSED' if result[key] else 'OPEN'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--setup', type=Path)
    args = parser.parse_args()
    petskills=load_recovered25_petskill_runtime(data_dir=args.data_dir, setup=args.setup)
    enemybase=load_recovered25_enemybase_runtime(data_dir=args.data_dir, setup=args.setup)
    result = analyze_runtime_objects(petskills,enemybase)
    emit(result)
    if not result['option_domain_closed']:
        raise SystemExit('Weaken data gate remains open')
    # The real preservation bundle exercises production admission, including
    # complete metadata, both encoding parses and the immutable OPTION hash.
    from types import SimpleNamespace
    from tools.stoneage_enemy_ai_weaken_bridge import resolve_enemy_ai_weaken_submission
    admitted=0
    for template in enemybase.templates.values():
        slots=tuple(int(i) for i in template.skill_slot_ids)
        for slot,skill_id in enumerate(slots):
            if skill_id not in EXPECTED_IDS:
                continue
            submission=resolve_enemy_ai_weaken_submission(
                SimpleNamespace(template=template,participant=SimpleNamespace(
                    participant_id="probe",kind="enemy",side="enemy")),
                skill_slot=slot,target_slot=0,petskill_runtime=petskills)
            if submission.skill_id!=skill_id:
                raise SystemExit("Weaken selected seven-slot identity drift")
            admitted+=1
    if admitted!=EXPECTED_SLOT_REFERENCES:
        raise SystemExit("Weaken typed admission population drift")
    print(f"COUNT|weaken_typed_admitted_slot_references|{admitted}")
    print("RESOLUTION|RECOVERED25_WEAKEN_TYPED_ADMISSION_CLOSED")


if __name__ == '__main__':
    main()
