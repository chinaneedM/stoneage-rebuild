"""Independent replay of the exact R77 registered retained-evidence census."""
import json
import hashlib
import subprocess
from pathlib import Path

def number(v):
 if type(v)is int:return v
 if isinstance(v,str):
  try:return int(v,0)
  except ValueError:return None

def scan(value,addresses,roots,operands,targets):
 out={n:{'decoded':[],'roots':[],'references':[]}for n in targets}
 pending=[('$',value)]
 while pending:
  path,x=pending.pop()
  if isinstance(x,dict):
   for n in targets:
    values=(n,n+4194304)
    if any(number(x.get(k))in values for k in addresses)and isinstance(x.get('mnemonic'),str)and x['mnemonic']and any(isinstance(x.get(k),list)for k in operands):out[n]['decoded'].append((path,x['mnemonic']))
    if any(number(x.get(k))in values for k in roots):out[n]['roots'].append(path)
   pending.extend((path+'.'+k,v)for k,v in x.items())
  elif isinstance(x,list):pending.extend((path+'['+str(i)+']',v)for i,v in enumerate(x))
  else:
   for n in targets:
    if number(x)in(n,n+4194304):out[n]['references'].append(path)
 return out

def validate(path):
 d=json.loads(Path(path).read_bytes());targets=[t['rva']for t in d['targets']]
 assert d['report_count']==len(d['registered_reports'])==156
 assert d['source_head']=='b49c0d81ad17dc8c5f691e505a9ca817df2a625d'
 assert targets==[321787,313683]
 assert d['entry_address_keys']==['site_rva','rva','instruction_rva','address','va','instruction_address']
 assert d['operand_array_keys']==['operands','ops','operand_shapes']
 manifest=d['registered_reports'];names=[r['path']for r in manifest]
 actual=subprocess.check_output(['git','ls-tree','-r','--name-only',d['source_head'],'research/recovered'],text=True).splitlines()
 assert names==[p for p in actual if Path(p).name.startswith('STONEAGE-TW10-SAVEDATA-')and p.endswith('.json')]
 results={n:{'decoded':[],'roots':[],'references':[]}for n in targets}
 for r in manifest:
  raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==r['git_blob']
  found=scan(json.loads(raw),d['entry_address_keys'],d['root_address_keys'],d['operand_array_keys'],targets)
  for n in targets:
   for k,vs in found[n].items():results[n][k].extend((r['path'],v)for v in vs)
 for t in d['targets']:
  result=results[t['rva']]
  assert sorted(result['decoded'])==sorted((h['file'],(h['object_path'],h['mnemonic']))for h in t['decoded_entry_hits'])
  assert sorted(result['roots'])==sorted((h['file'],h['object_path'])for h in t['root_bearing_objects'])
  assert sorted(result['references'])==sorted((h['file'],h['value_path'])for h in t['numeric_reference_hits'])
  assert not result['decoded']
 assert d['absence_bounded_to_registered_representations']is True and d['numeric_reference_is_not_decoded_callee_graph']is True and d['actual_handle_value_or_callee_preservation_or_persistence_proven']is False
 return {'registered_reports':156,'target_decoded_entries':[0,0],'root_objects':[len(results[n]['roots'])for n in targets],'numeric_references':[len(results[n]['references'])for n in targets]}

if __name__=='__main__':print(json.dumps(validate('research/recovered/STONEAGE-TW10-SAVEDATA-R77-REFRESH-PREFLIGHT.json'),sort_keys=True))
