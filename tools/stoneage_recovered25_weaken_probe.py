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
    result = analyze_runtime_objects(
        load_recovered25_petskill_runtime(data_dir=args.data_dir, setup=args.setup),
        load_recovered25_enemybase_runtime(data_dir=args.data_dir, setup=args.setup))
    emit(result)
    if not result['option_domain_closed']:
        raise SystemExit('Weaken data gate remains open')


if __name__ == '__main__':
    main()
