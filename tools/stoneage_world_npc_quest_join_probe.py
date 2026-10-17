"""Finite named-NPC/world/event/item join for the shell-delivery guide witnesses.

Only derived identities, geometry, typed numeric fields and query matches leave
CI. No original NPC rows, dialogue, scripts, map payload or binaries are emitted.
Recovered25 is a later preservation source, never original TW1.0 server proof.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from tools.stoneage_npc_world_graph_probe import iter_blocks,magic_kind,collect_server_map_ids
from tools.stoneage_quest_npc_item_binding_probe import argument_bytes,fields,BUNDLE_SHA256
from tools.stoneage_itemset_schema_probe import SCHEMA,INDEX,setup_itemsets
from tools.stoneage_quest_item_identity_probe import EXPECTED
QUERIES={'YAYOI':('弥生','彌生'),'HIMIKO':('日美子',)}
CODECS=('utf-8','big5','gb18030')
NAME_KEYS={b'name',b'charname',b'npcname'}
MAX_PLACEMENTS=50
MAX_EVENTS=150

def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def exact_name(raw):
 out=[]
 for codec in CODECS:
  try:s=raw.decode(codec,'strict')
  except UnicodeError:continue
  for role,terms in QUERIES.items():
   if s in terms:out.append({'query_role':role,'codec':codec,'exact_name_match':True})
 return out

def mentions(raw):
 found=set()
 for role,terms in QUERIES.items():
  for term in terms:
   for codec in CODECS:
    try:token=term.encode(codec,'strict')
    except UnicodeError:continue
    if token in raw:found.add(role)
 return sorted(found)

def numeric_items(value):
 out=[]
 if not value:return out
 for t in value.split(b','):
  m=re.fullmatch(rb'\s*([0-9]+)(?:\*([1-9][0-9]*))?\s*',t)
  if not m:return None
  out.append({'id':int(m[1]),'quantity':int(m[2]or b'1')})
 return out

def typed_events(arg):
 out=[]
 for i,record in enumerate(arg.split(b'EventEnd')):
  selected=[];predicates=[]
  for key,value in fields(record):
   if key in (b'getitem',b'delitem'):
    items=numeric_items(value)
    if items is not None:selected.append({'role':'GIVE_ITEM_CONFIG' if key==b'getitem' else 'REMOVE_ITEM_CONFIG','items':items})
   if key==b'event':
    for clause in value.split(b','):
     for atom in clause.split(b'&'):
      m=re.fullmatch(rb'\s*ITEM\s*(=|!=)\s*([0-9]+)(?:\*([1-9][0-9]*))?\s*',atom,re.I)
      if m:predicates.append({'kind':'ITEM','comparison':m[1].decode(),'id':int(m[2]),'quantity':int(m[3]or b'1')})
  if selected or predicates:
   out.append({'record_ordinal':i,'event_record_sha256':sha(record),'actions':selected,'item_predicates':predicates,
       'execution_verified':False,'condition_satisfiable_verified':False})
 return out

def scalar(fields,key):
 values=[v for k,v in fields if k==key]
 return int(values[0]) if len(values)==1 and re.fullmatch(rb'[+-]?[0-9]+',values[0]) else None

def geometry(entries):
 out=[]
 for key,v in entries:
  if key not in (b'borncenter',b'borncorner'):continue
  try:nums=[int(x.strip())for x in v.split(b',')]
  except ValueError:continue
  if len(nums)==4:out.append({'kind':key.decode(),'values':nums,'actual_spawn_or_fixed_tile_verified':False})
 return out

def lookup_items(server,ids):
 selected=setup_itemsets(server/'setup.cf');tables={}
 for filename,pin in EXPECTED.items():
  p=server/'data'/filename;b=p.read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'item source '+filename)
  rows=[];count=0
  for line_no,raw in enumerate(b.splitlines(),1):
   line=raw.strip()
   if not line or line.startswith(b'#'):continue
   cells=[x.strip()for x in line.replace(b'\t',b' ').split(b',')]
   need(len(cells)==len(SCHEMA)==94,'item schema');count+=1
   item_id=int(cells[INDEX['id']])
   if item_id not in ids:continue
   labels=[]
   for col in ('name','secretname'):
    for codec in CODECS:
     try:name=cells[INDEX[col]].decode(codec,'strict')
     except UnicodeError:continue
     # Exact finite terms only; unrelated item names are not dumped.
     if name in ('贝壳','貝殼','仙尼亚的花','仙尼亞的花','仙人掌花','花'):
      labels.append({'field':col,'codec':codec,'query_label':name})
   vals={k:int(cells[INDEX[k]])if cells[INDEX[k]] else None for k in ('id','imagenumber','cost','dropatlogout','vanishatdrop')}
   rows.append({'physical_line':line_no,'row_sha256':sha(raw),'name_sha256':sha(cells[INDEX['name']]),
      'matched_public_item_terms':labels,'numeric_fields':vals})
  need(count==pin['rows'],'item row census')
  tables[filename]={'bytes':len(b),'sha256':sha(b),'row_count':count,
    'selected_by_setup':filename in {Path(v.replace('\\','/')).name.lower()for v in selected.values()},'joined_rows':rows}
 return {'setup_itemsets':selected,'tables':tables}

def analyze(server):
 npc=server/'data/npc';paths=sorted((p for p in npc.rglob('*')if p.is_file()),key=lambda p:str(p).lower())
 templates=defaultdict(list)
 for path in paths:
  if magic_kind(path)!='template':continue
  for entries in iter_blocks(path):
   d=dict(entries);name=d.get(b'templatename')
   if name:templates[name.strip()].append((entries,d))
 map_ids,map_files=collect_server_map_ids(server/'data/map');counts=Counter();output=[];all_item_ids=set()
 for path in paths:
  if magic_kind(path)!='create':continue
  for ordinal,entries in enumerate(iter_blocks(path)):
   for ei,(key,value)in enumerate(entries):
    if key!=b'enemy':continue
    counts['all_enemy_references']+=1
    name,sep,raw=value.partition(b'|');definitions=templates.get(name.strip(),[])
    if len(definitions)!=1:
     counts['unresolved_or_ambiguous_templates']+=1;continue
    te,template=definitions[0];arg,transport=argument_bytes(npc,raw if sep else b'')
    if arg is None:counts['argument_'+transport]+=1;continue
    exact=[]
    for origin,items in [('template',te),('create',entries),('parameter',list(fields(arg)))]:
     for k,v in items:
      if k in NAME_KEYS:
       for match in exact_name(v):exact.append({'origin':origin,'field':k.decode(),**match})
    mentioned=mentions(arg)
    if not exact and not mentioned:continue
    f=template.get(b'functionset',b'').decode('ascii','replace').strip()
    events=typed_events(arg)if f.lower()=='exchangeman'else[]
    for e in events:
     for action in e['actions']:
      all_item_ids.update(x['id']for x in action['items'])
     all_item_ids.update(x['id']for x in e['item_predicates'])
    floor=scalar(entries,b'floorid')
    ident=str(path.relative_to(npc)).replace('\\','/')+'|'+str(ordinal)+'|'+str(ei)
    output.append({'placement_key':sha(ident.encode()),'create_file_sha256':sha(path.read_bytes()),
       'create_block_ordinal':ordinal,'template_name_sha256':sha(name.strip()),
       'parameter_sha256':sha(arg),'transport':transport,'functionset':f,
       'identity_evidence':'EXACT_NAME_FIELD'if exact else 'PARAMETER_MENTION_ONLY',
       'exact_name_matches':exact,'mentioned_query_roles':mentioned,'floor_id':floor,
       'map_header_exists':floor in map_ids if floor is not None else False,
       'spawn_geometry':geometry(entries),'event_records':events,
       'historical_guide_same_npc_proven':False,'original_tw10_membership_proven':False})
 need(len(output)<=MAX_PLACEMENTS and sum(len(x['event_records'])for x in output)<=MAX_EVENTS,'bounded named selection exceeded')
 return {'schema':'stoneage.world_npc_quest.source_join.r1','source_profile':'LATER_RECOVERED25',
   'source_bundle_sha256':BUNDLE_SHA256,'query_roles':QUERIES,'counts':dict(counts),
   'server_map_files':map_files,'server_map_ids':len(map_ids),'selected_placements':output,
   'selected_item_ids':sorted(all_item_ids),'item_master_joins':lookup_items(server,all_item_ids),
   'original_server_executed':False,'complete_delivery_quest_verified':False,'original_tw10_world_restored':False,
   'same_name_proves_same_npc':False,'event_presence_proves_execution':False,
   'original_dialogue_or_raw_rows_exported':False,'stage_b_started':False}

def main():
 p=argparse.ArgumentParser();p.add_argument('--server',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 r=analyze(a.server);a.output.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')
 print(json.dumps({'selected_placements':len(r['selected_placements']),'item_ids':r['selected_item_ids'],'counts':r['counts']},sort_keys=True))
if __name__=='__main__':main()
