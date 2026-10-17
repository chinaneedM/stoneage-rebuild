"""Source-qualified original login flow and avatar input crosswalk.
Semantic field labels stay EARLY_LINEAGE; original screens remain unverified.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from tools.stoneage_tw10_login_avatar_probe import ANCHORS,RUNTIME_SHA256
ROOT=Path(__file__).resolve().parents[1]
REPORT='research/recovered/STONEAGE-TW10-LOGIN-AVATAR-CATALOG-R1.json'
PINS={'research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt': '182f9df06c76996ca6983f523cbecfa4fe154852', 'research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json': 'e39a3a6020b578da017ab0bfa9369dc083e0b700', 'research/recovered/TW10-LOGIN-AVATAR-SELECTOR-WRITERS-CORRECTED-R1.json': '6bc116f35b9f0b0959b1118b933129fe814d607c', 'research/recovered/JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json': '05681ff8d6092171cce32a7ece8b29160601ac44'}

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)

def parse_protocols(text):
 out={}
 for line in text.splitlines():
  if not line.startswith('PROTOCOL|'):continue
  p=dict(x.split('=',1)for x in line.split('|')[1:])
  k=p['region'],p['name'];need(k not in out,'duplicate envelope');out[k]=p
 return out

def build_catalog():
 for f,pin in PINS.items():need(blob((ROOT/f).read_bytes())==pin,'source provenance changed: '+f)
 envelopes=parse_protocols((ROOT/'research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt').read_text())
 static=json.loads((ROOT/'research/recovered/TW10-LOGIN-AVATAR-SELECTOR-WRITERS-CORRECTED-R1.json').read_text())
 need(static['runtime_sha256']==RUNTIME_SHA256 and not static['original_program_executed'],'original specimen boundary')
 records=[]
 for name,(header,callback)in ANCHORS.items():
  direct=static['protocols'][name];need(direct['original_header_xref_rva']==header and direct['receive_callback_rva']==callback,'anchor mismatch')
  row={'protocol':name,'source_evidence':'TW10_DIRECT_COMPILED_MESSAGE_SHAPE','receive_callback_rva':callback,
       'sender_callsites':[{'site_rva':x['site_rva'],'target_rva':x['target_rva']}for x in direct['sender_callsites']],
       'historical_screen_layout':None,'proven_runtime_transition_order':None}
  for direction in ('send','recv'):
   p=envelopes[direction,name]
   row[direction]={'int_fields':int(p['int_fields']),'string_fields':int(p['string_fields']),
       'xref_rva':int(p['xref_rva'],16)}
  need(row['send']['xref_rva']==header,'compiled send shape identity')
  records.append(row)
 create=static['protocols']['CreateNewChar']['sender_callsites']
 need(len(create)==1 and len(create[0]['bounded_push_operands'])==14,'bounded create signature')
 pushes=list(reversed(create[0]['bounded_push_operands']))
 schema=json.loads((ROOT/'research/clients/STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json').read_text())['records']['character_creation']
 fields=[]
 for f,p in zip(schema['fields'],pushes[1:]):
  fields.append({'position':f['position'],'lineage_name':f['name'],'semantic_evidence':'EARLY_LINEAGE',
      'caller_push_site_rva':p['site_rva'],'static_operand_source':p['static_source'],
      'join_premise':'x86 right-to-left argument order plus retained early generated signature; static source only',
      'actual_value':None,'selected_spr_group':None,'selected_bitmap':None})
 helper=static['builder_field_helper_calls']
 need([r['helper_type']for r in helper]==['int','string']+['int']*11,'original builder field order changed')
 return {'schema':'stoneage.tw10.login_avatar.catalog.r1','source_git_blobs':PINS,
   'protocols':records,'create_payload_fields':fields,'create_builder_field_helpers':helper,
   'selector_writer_inventory':static['avatar_selector_write_candidates'],
   'jss_2001_creation_manual':json.loads((ROOT/'research/recovered/JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json').read_text())['pages']['manual01'],
   'status':'ORIGINAL_STATIC_INPUT_PROVENANCE_PARTIAL_VISUAL_IDENTITY_OPEN',
   'historical_character_names':[],'original_character_count':None,'original_character_roster_complete':False,
   'original_screen_layout_verified':False,'runtime_resource_selection_verified':False,
   'original_server_login_success_verified':False,'stage_b_started':False,
   'next':'WORLD-NPC-QUEST-SOURCE-JOIN-01; reopen avatar visual identity only with original selector values/table bounds or authenticated original screenshots'}

def validate_catalog(r):
 need(r==build_catalog(),'archived source crosswalk differs from exact semantic replay')
 need(r['original_character_count']is None and not r['original_character_roster_complete'],'no invented character census')
 for f in r['create_payload_fields']:
  need(f['actual_value']is None and f['selected_spr_group']is None and f['selected_bitmap']is None,'unproven graphical identity')
 return r
if __name__=='__main__':
 r=build_catalog();validate_catalog(r);print(json.dumps(r,ensure_ascii=False,sort_keys=True))
