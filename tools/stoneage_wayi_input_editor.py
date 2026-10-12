"""Bounded static input-editor/settings projection; synthetic byte data only.

Never runs original code, supplies credentials, reads actual saved files or
connects to servers. Model invariants are not inferred native safety guards.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_jss_saupdate_xref_probe import parse_imports
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_saupdate_route_probe import decode_window,raw_window,operand_metadata
from tools.stoneage_wayi_pet_transport_probe import summarize_window
from tools.stoneage_wayi_codec_profile import read_literal
from tools.stoneage_enemy_creation_audit import definition

SOURCE_REF='2f736808ff4361f5429ee919b718c88fabb60346'
PINS={
 'client/stoneage/system/chat.cpp':'9930f252869ccab2bf432f71f2adbba38277aa0a',
 'client/stoneage/systeminc/chat.h':'d961e1b896d46bbb2d09ecc4d3ddc3a8782a0c73',
 'client/stoneage/game/main.cpp':'65b5d8501f6770aefe35d38c5d4c1c4c902259bd',
 'client/sdk/caryime.h':'414ade24d4407b8464f7d362833669ab2b9372d2',
 'client/stoneage/system/login.cpp':'987e60c4ef581cd2336ff0956400a1da47aeff20',
 'client/stoneage/system/savedata.cpp':'6809dd415e89e87ad00f7813cb35209db034aa53',
 'client/stoneage/systeminc/savedata.h':'59bcd35bc9cf95cf28e6a1c2fe6681d30513acf9',
}
WINDOWS={
 'single-byte-editor':(0x113d0,0x114dd),
 'two-byte-editor':(0x114e0,0x1156c),
 'string-callback':(0x10620,0x10678),
 'focus-pointer':(0x11940,0x1194a),
 'main-character-call':(0x3ff50,0x3ff65),
 'alternate-wm-char-gate':(0x8dacb,0x8daed),
 'startup-callback-binding':(0x1e5a6,0x1e5be),
 'callback-initializer':(0x94ef0,0x950bd),
 'callback-two-byte-result':(0x9524a,0x95285),
 'callback-string-result':(0x95528,0x95561),
 'login-submit-body':(0x20c80,0x20ebf),
 'settings-write-body':(0x806ba,0x80752),
 'settings-create-body':(0x808c0,0x809bb),
}


def demand(ok,message):
 if not ok:raise ValueError(message)


def state_check(backing,count,cursor,limit):
 demand(isinstance(backing,bytes) and len(backing)==260,'Synthetic fixed backing')
 demand(all(type(x)is int for x in (count,cursor,limit))and 1<=limit<=255 and 0<=cursor<=count<=limit,'Well-formed synthetic state')
 demand(backing[count]==0 and 0 not in backing[:count],'Explicit existing terminator invariant')


def login_char_allowed(value):
 demand(type(value)is int and 0<=value<=255,'Byte domain')
 return 48<=value<=57 or 65<=value<=90 or 97<=value<=122


def insert_byte(backing,count,cursor,value,limit=12,login=True):
 state_check(backing,count,cursor,limit)
 demand(type(value)is int and 0<=value<=255 and type(login)is bool,'Synthetic insertion arguments')
 if value<=31 or count>=limit or(login and not login_char_allowed(value)):
  return backing,count,cursor,False
 out=bytearray(backing)
 # Preserve the old terminator with exactly the observed backwards copy.
 for pos in range(count,cursor-1,-1):out[pos+1]=out[pos]
 out[cursor]=value
 return bytes(out),count+1,cursor+1,True


def insert_pair(backing,count,cursor,pair,limit=12,login=True):
 state_check(backing,count,cursor,limit)
 demand(isinstance(pair,bytes) and len(pair)==2 and 0 not in pair and type(login)is bool,'Synthetic complete pair')
 if count>=limit-1 or login:return backing,count,cursor,False
 out=bytearray(backing)
 for pos in range(count,cursor-1,-1):out[pos+2]=out[pos]
 out[cursor:cursor+2]=pair
 return bytes(out),count+2,cursor+2,True


def callback_plan(units,budget=86):
 """Complete synthetic one/two-byte units. Locale classification supplied.

    Do not infer the original ACP, reject dangling pairs in original code, or
    silently turn the loop budget into a complete-character boundary check.
 """
 demand(type(budget)is int and 1<=budget<=86,'Source loop budget')
 demand(all(isinstance(u,bytes)and len(u)in(1,2)and 0 not in u for u in units),'Synthetic complete units')
 total=sum(len(u)for u in units);cap=min(total,budget);pos=0;rows=[]
 for u in units:
  if pos>=cap:break
  rows.append({'start':pos,'helper_width':len(u),'past_loop_budget':pos+len(u)>cap})
  pos+=len(u)
 return rows


def click_submit_condition(first,second):
 """Bounded click branch only, not authentication or keyboard-return rule."""
 demand(isinstance(first,bytes)and isinstance(second,bytes),'Synthetic strings')
 first=first.split(b'\0',1)[0]
 return bool(first)


def settings_factory(stereo,se_volume,bgm_volume,pitch):
 demand(all(type(x)is int and 0<=x<=255 for x in(stereo,se_volume,bgm_volume))and isinstance(pitch,bytes)and len(pitch)==16,'Synthetic settings')
 out=bytearray(127);out[:2]=struct.pack('<H',6)
 out[36:39]=bytes((stereo,se_volume,bgm_volume));out[39:55]=pitch
 out[56]=10;out[57]=3
 return bytes(out)


def source_profile(root):
 raw={}
 for path,pin in PINS.items():
  data=(Path(root)/path).read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  demand(actual==pin,'Source drift: '+path);raw[path]=data.decode('utf-8-sig')
 chat=raw['client/stoneage/system/chat.cpp']
 single=definition(chat,'StockStrBufferChar')
 # Only lexical/source facts; not whole-source preprocessing/build identity.
 stripped=re.sub(r'/\*.*?\*/','',single,flags=re.S)
 relaxed=re.search(r'if\s*\(pNowStrBuffer == &idKey \|\| pNowStrBuffer == &passwd\)\s*\{\s*\}',stripped)is not None
 pair=definition(chat,'StockStrBufferDBChar')
 login=raw['client/stoneage/system/login.cpp'];submit=definition(login,'inputIdPassword')
 saved=raw['client/stoneage/system/savedata.cpp']
 report={'source_ref':SOURCE_REF,'source_blobs':PINS,
  'current_single_byte_login_filter_commented_out':relaxed,
  'current_double_byte_login_fields_rejected':'pNowStrBuffer == &idKey || pNowStrBuffer == &passwd' in pair and 'GbkToUtf8' in pair,
  'current_window_wm_char_uses_utf8_bridge':'StockStrBufferWmChar(wParam)'in raw['client/stoneage/game/main.cpp'],
  'current_submit_checks_both_nonempty':'strlen(idKey.buffer) > 0 && strlen(passwd.buffer) > 0'in submit,
  'current_login_initializer_parameter':18,
  'settings_cdkey_and_password_named_tokens_only_in_enums':len(re.findall(r'\bCDKEY\b',saved))==2 and len(re.findall(r'\bPASSWORD\b',saved))==2,
  'settings_no_szuser_szpassword_access':not re.search(r'\b(szUser|szPassword)\b',saved),
  'source_program_executed':False,'matching_original_operator_server':False}
 demand(relaxed and report['current_double_byte_login_fields_rejected']and report['current_submit_checks_both_nonempty'],'Expected source divergence')
 demand('idKey, usernameBoxX, usernameBoxY, 18,'in login,'Current input profile')
 return report


def probe(payload):
 demand(len(payload)==EXPECTED_BYTES and hashlib.sha256(payload).hexdigest()==EXPECTED_SHA256,'Exact accepted specimen')
 layout=parse_pe_layout(payload);base=struct.unpack_from('<I',payload,layout['pe_off']+52)[0];imports=parse_imports(payload,layout,base)
 windows=[];anchors={}
 targets={0x113d5,0x113fd,0x11464,0x11469,0x1146e,0x11473,0x11478,0x1147d,
          0x114fb,0x1153d,0x10635,0x1064f,0x20cc3,0x20cc9,
          0x94ff5,0x95273,0x9554f,0x8dacb,0x806e6,0x80933,0x8093a}
 for name,(a,b)in WINDOWS.items():
  ins=decode_window(raw_window(payload,layout,a,b),base+a);summary=summarize_window(ins,base,imports)
  windows.append({'label':name,'start_rva':a,'end_rva_exclusive':b,
                  **{k:summary[k]for k in('instruction_count','calls','branches','absolute_writes')}})
  for i in ins:
   if i.address-base in targets:anchors[hex(i.address-base)]={'operation':i.mnemonic,'operands':operand_metadata(i,base)}
 return {'schema':'STONEAGE-WAYI-INPUT-EDITOR-R1','input_bytes':len(payload),'decompressed_input_sha256':EXPECTED_SHA256,
 'windows':windows,'anchors':anchors,'focus_pointer_rva':0x150d64,'callback_pointer_rva':0x4bb46d0,
 'dbcs_classifier_import':list(imports[base+0xa018c]),'settings_path_literal':read_literal(payload,layout,0xd6058),
 'settings_backing_rva':0x4319d28,'file_executed':False,'real_savedata_opened':False,'native_login_verified':False}


def validate(r):
 p=r['probe'];demand(p['schema']=='STONEAGE-WAYI-INPUT-EDITOR-R1'and p['input_bytes']==EXPECTED_BYTES and p['decompressed_input_sha256']==EXPECTED_SHA256,'Identity')
 demand([(x['label'],x['start_rva'],x['end_rva_exclusive'])for x in p['windows']]==[(n,a,b)for n,(a,b)in WINDOWS.items()],'Windows')
 demand(p['dbcs_classifier_import']==['KERNEL32.DLL','IsDBCSLeadByte'],'Locale-classifier identity')
 for rva,value in((0x11464,48),(0x11469,57),(0x1146e,65),(0x11473,90),(0x11478,97),(0x1147d,122),(0x10635,86),(0x806e6,127),(0x80933,127)):
  demand(p['anchors'][hex(rva)]['operands'][-1].get('value')==value,'Guard or save length')
 demand(p['settings_path_literal']=='data\\savedata.dat'and p['settings_backing_rva']==0x4319d28,'Settings profile')
 demand(all(p[k]is False for k in('file_executed','real_savedata_opened','native_login_verified')),'Native promotion')
 s=r['source_profile'];demand(s['source_ref']==SOURCE_REF and s['source_blobs']==PINS,'Source identity')
 demand(s['current_single_byte_login_filter_commented_out']and s['current_submit_checks_both_nonempty']and s['current_login_initializer_parameter']==18,'Source/compiled distinction')
 demand(s['source_program_executed']is False and s['matching_original_operator_server']is False,'Source promotion')
 for row in r['synthetic_insertions']:
  before=bytes.fromhex(row['before_hex']);actual=insert_byte(before,row['count'],row['cursor'],row['byte'],row['limit'])
  demand(actual[0].hex()==row['after_hex']and actual[1:]==(row['after_count'],row['after_cursor'],row['accepted']),'Synthetic insertion')
 return p


if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--client',type=Path);parser.add_argument('--source-root',type=Path);a=parser.parse_args()
 if a.client:print(json.dumps(probe(a.client.read_bytes()),indent=2))
 if a.source_root:print(json.dumps(source_profile(a.source_root),indent=2))
