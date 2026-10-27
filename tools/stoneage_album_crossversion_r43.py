"""Retrospective album-name projection onto three separate resource specimens.

The mixed25 names do not authenticate TW10 species identities. No original
pixels, server tables, program execution or runtime selection are inferred.
"""
import argparse
import csv
import gzip
import hashlib
import json
import lzma
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'research/recovered/'
PINS = {
 BASE+'STONEAGE-NATIVE-ALBUM-MATERIAL-R36.json': '1a79802705c88d94fb755903ddee3a3da5985e302f822e9ba0064af8034595e0',
 BASE+'logical-alias-catalog-r1/REFERENCES-R1.tsv.gz': '3092102e3ee83524ccbf27414ce0cf5bc5579d9a5c8638bfa073f9e62a4db1ea',
 BASE+'logical-alias-catalog-r1/CONTENTS-R1.tsv.gz': '2e4ac01f97d2e481ca1517c50a5ae6df96097dab72f4453273a761e938c35b89',
}
REPORT = BASE+'STONEAGE-ALBUM-CROSSVERSION-MATERIAL-R43.json.xz'
PROFILES = ('TW10', 'CN50', 'PATCH129')


def need(ok, message):
 if not ok:
  raise ValueError(message)


def project(rows, refs, contents):
 """Keep every candidate in its original profile; never choose last-wins."""
 bykey = defaultdict(list)
 for ref in refs:
  need(ref['profile'] in PROFILES, 'unexpected profile')
  cid = ref['content_id']
  need(cid in contents, 'missing RD content definition')
  content = contents[cid]
  need(int(ref['adrn_size']) == int(content['bytes']), 'RD size mismatch')
  bykey[(ref['profile'], int(ref['logical_alias']))].append(ref)
 result = []
 holes = []
 for row in rows:
  if row['album_slot'] == -1:
   need(row['table_face_value'] == 0 and row['name_gbk'] == '无', 'invalid placeholder')
   holes.append(row['table_index'])
   continue
  need(row['album_slot'] >= 0 and row['table_face_value'] > 0, 'invalid album namespace')
  matches = {}
  for profile in PROFILES:
   candidates = []
   for ref in bykey[(profile, row['table_face_value'])]:
    content = contents[ref['content_id']]
    candidates.append({**ref, 'rd_sha256': content['rd_sha256'],
                       'rd_bytes': int(content['bytes'])})
   identities = {(c['rd_bytes'], c['rd_sha256']) for c in candidates}
   matches[profile] = {'status': 'MISSING_IN_FIXED_CATALOG' if not candidates else
                       ('ONE_CONTENT' if len(identities) == 1 else 'MULTIPLE_CONTENTS'),
                       'content_count': len(identities), 'references': candidates}
  result.append({'album_row': row, 'profiles': matches})
 return result, holes


def build():
 pins = {}
 for path, expected in PINS.items():
  raw = (ROOT/path).read_bytes()
  need(hashlib.sha256(raw).hexdigest() == expected, 'input SHA mismatch: '+path)
  pins[path] = {'bytes': len(raw), 'sha256': expected,
               'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
 album = json.loads((ROOT/next(iter(PINS))).read_text())
 # Reuse the existing exact row and source-chain verification; no source reacquisition.
 from tools.stoneage_native_album_material_r36 import replay
 replay(album)
 with gzip.open(ROOT/(BASE+'logical-alias-catalog-r1/REFERENCES-R1.tsv.gz'), 'rt') as f:
  refs = list(csv.DictReader(f, delimiter='\t'))
 with gzip.open(ROOT/(BASE+'logical-alias-catalog-r1/CONTENTS-R1.tsv.gz'), 'rt') as f:
  contents = {r['content_id']: r for r in csv.DictReader(f, delimiter='\t')}
 rows, holes = project(album['table']['rows'], refs, contents)
 counts = {}
 for profile in PROFILES:
  states = Counter(r['profiles'][profile]['status'] for r in rows)
  counts[profile] = {'slots_with_reference': sum(s != 'MISSING_IN_FIXED_CATALOG' for r in rows for s in [r['profiles'][profile]['status']]),
                     'reference_occurrences': sum(len(r['profiles'][profile]['references']) for r in rows),
                     'statuses': dict(sorted(states.items()))}
 comparisons = {}
 for left, right in [('TW10','CN50'), ('TW10','PATCH129'), ('CN50','PATCH129')]:
  c = Counter()
  for row in rows:
   a = {(x['rd_bytes'],x['rd_sha256']) for x in row['profiles'][left]['references']}
   b = {(x['rd_bytes'],x['rd_sha256']) for x in row['profiles'][right]['references']}
   c['MISSING_ONE_OR_BOTH' if not a or not b else 'EQUAL_CONTENT_SETS' if a == b else 'DIFFERENT_CONTENT_SETS'] += 1
  comparisons[left+'__'+right] = dict(sorted(c.items()))
 return {'schema': 'stoneage.album_crossversion_material.r43', 'source_pins': pins,
         'name_scope': album['source_scope'], 'join_kind': 'RETROSPECTIVE_LOGICAL_ALIAS_COMPATIBILITY_NOT_SAME_BUILD_IDENTITY',
         'input_catalog_references': len(refs), 'compiled_rows': len(album['table']['rows']),
         'named_slots': len(rows), 'placeholder_table_indices': holes,
         'profile_counts': counts, 'profile_content_set_comparisons': comparisons,
         'rows': rows,
         'boundaries': {'official_tw10_names_authenticated': 0, 'same_deployment_proven': False,
                        'runtime_alias_winner_proven': False, 'pixels_read_or_rendered': False,
                        'new_original_downloads': 0, 'original_program_executed': False,
                        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED',
                        'r79': 'PAUSED_NON_BLOCKING', 'overall_restoration_percent': None}}


def main():
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--write', action='store_true')
 args = parser.parse_args()
 result = build()
 raw = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+'\n'
 if args.write:
  (ROOT/REPORT).write_bytes(lzma.compress(raw.encode(), preset=9))
 else:
  need(lzma.decompress((ROOT/REPORT).read_bytes()).decode() == raw, 'stored material differs from complete replay')
 print(json.dumps({k:result[k] for k in ['named_slots','profile_counts','profile_content_set_comparisons']}, ensure_ascii=False))

if __name__ == '__main__':
 main()
