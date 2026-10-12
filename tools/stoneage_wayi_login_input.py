"""Hash-pinned DES-table/input-flow recovery and synthetic 32-bit DES model.

Reads original bytes/source as data, never executes original programs/source.
All evaluated blocks and keys are supplied synthetic data. No credential input.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_saupdate_route_probe import raw_window,decode_window,operand_metadata
from tools.stoneage_wayi_pet_transport_probe import summarize_window
from tools.stoneage_wayi_codec_profile import read_literal

SOURCE_REF='2f736808ff4361f5429ee919b718c88fabb60346'
PINS={
 'client/stoneage/wgs/descrypt.cpp':'ad1e9a3508ecc5fbce1436ddfd5dd009372d4dbf',
 'client/stoneage/wgs/descrypt.h':'e9c5f9d13a69d90c3939dd08106b5f176eae429b',
 'server/gmsv/descrypt.c':'2d7290371bc1907f2217242ec4745d0c49125c86',
 'server/gmsv/include/descrypt.h':'5b9ca1326037cfd4748d2bd3fd11ff0692b678ef',
 'client/stoneage/system/login.cpp':'987e60c4ef581cd2336ff0956400a1da47aeff20',
 'client/stoneage/system/netproc.cpp':'0dc677d3cd367ab89ca8d5becbb383bcbbccb3a8',
}
TABLES={
 'nshifts':(0xda094,16,1),'pc1':(0xda0a4,56,1),
 'pc2_c':(0xda0dc,24,1),'pc2_d':(0xda0f4,24,1),
 'Psboxes':(0xda10c,512,4),'Ip_l':(0xda90c,256,4),
 'Ip_r':(0xdad0c,256,4),'Ip_inv_l':(0xdb10c,256,4),
 'Ip_inv_r':(0xdb50c,256,4),
}
TABLE_HASHES={
 'nshifts':'844b8205d28c096e00fefc11c0b874e040a0a14ffa6c3e395c39e457483f1707',
 'pc1':'4b2b89f8dd2b405f225218a592fa4d248afb7aa3bc19c1c681c648d2c7c8dc76',
 'pc2_c':'c045ed4b230ede4635da41b945f1285d8d0fdd965291c8bd0c21405a3bf48777',
 'pc2_d':'f20de024fb4b106efd85a6a22f807d8e10acfc4d43c9580cc08e9ce60fd0a776',
 'Psboxes':'668bb69e184e0c32dc3bc488001c506c87ee5a95c7e7b6b87d24c3a6dc779956',
 'Ip_l':'1ad702a1ced972e43d5d389b7e39bcf7b37f4ecaf1f0f49666b00d03a700c3cc',
 'Ip_r':'d286736c26b793d619b589ca8406bdc6609df1c32c55bf849d076c9004bf855f',
 'Ip_inv_l':'f2da95fedc5363ea65ff8f39d33d9660c44b9d8855d15f12913348edc73a39ce',
 'Ip_inv_r':'d001670c647ee992a03016a6e342750ab7f1e39de912b1e1c2c28062328067dd',
}
WINDOWS={
 'key-schedule':(0x8ebe0,0x8ed80),'block-rounds':(0x8ed80,0x8f14a),
 'ecb-wrapper':(0x8f150,0x8f19e),'ui-prologue':(0x206b0,0x206bf),
 'restore-two-32-byte-inputs':(0x2074c,0x20794),
 'save-two-32-byte-inputs':(0x2097d,0x209c3),
 'clear-two-input-descriptors':(0x209c3,0x209f7),
 'initial-input-descriptors':(0x20ba0,0x20c37),
 'descriptor-setter':(0x211c0,0x211f7),
 'login-two-16-byte-decode':(0x5f8d8,0x5f950),
}


def demand(ok,message):
 if not ok:raise ValueError(message)


def parse_array(source,name):
 """Parse numeric initializers and literal C/D+integer sums; never eval code."""
 pattern=r'\b'+re.escape(name)+r'\s*(?:\[[^\]]*\])+\s*=\s*\{'
 starts=list(re.finditer(pattern,source))
 demand(len(starts)==1,'Missing/ambiguous numeric array')
 start=starts[0].end();end=source.find('};',start)
 demand(end>=start,'Unterminated numeric array')
 body=source[start:end].replace('{','').replace('}','')
 out=[]
 for token in body.split(','):
  token=token.strip()
  if not token:continue
  terms=token.split('+');value=0
  for term in terms:
   term=term.strip()
   if term in ('C','D'):value+=28 if term=='C'else 0
   else:
    demand(re.fullmatch(r'(?:0x[0-9a-fA-F]+|0|[1-9][0-9]*)',term) is not None,'Unsupported initializer')
    value+=int(term,0)
  out.append(value)
 demand(out and len(out)<=2048,'Array cardinality')
 return out


def table_bytes(values,width):
 demand(width in (1,4) and all(type(x)is int and 0<=x<(1<<(width*8))for x in values),'Table element width')
 return b''.join(x.to_bytes(width,'little')for x in values)


def load_source(root):
 raw={}
 for path,pin in PINS.items():
  b=(Path(root)/path).read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  demand(sha==pin,'Pinned source drift: '+path);raw[path]=b.decode('utf-8-sig')
 tables={}
 for name,(_,count,width)in TABLES.items():
  a=parse_array(raw['client/stoneage/wgs/descrypt.cpp'],name)
  b=parse_array(raw['server/gmsv/descrypt.c'],name)
  demand(a==b and len(a)==count,'Client/server numeric profile disagreement')
  demand(hashlib.sha256(table_bytes(a,width)).hexdigest()==TABLE_HASHES[name],'Numeric table hash')
  tables[name]=a
 return raw,tables


def rotate(value,count,bits):
 demand(type(bits)is int and bits in (28,32) and type(count)is int and 0<=count<bits,'Rotate domain')
 mask=(1<<bits)-1;value &=mask
 return ((value<<count)|(value>>(bits-count)))&mask


def key_schedule(key,tables):
 demand(isinstance(key,bytes) and len(key)==8,'Synthetic eight-byte key')
 left=right=0;index=0
 for value in key:
  for bit in range(7):
   pos=tables['pc1'][index];index+=1
   if value&(128>>bit):
    if pos>=28:left |=1<<(pos-28)
    else:right |=1<<pos
 keys=[]
 for count in tables['nshifts']:
  left=rotate(left,count,28);right=rotate(right,count,28);groups=[]
  for half,name in ((left,'pc2_c'),(right,'pc2_d')):
   for start in range(0,24,6):
    value=0
    for pos in tables[name][start:start+6]:value=(value<<1)|((half>>pos)&1)
    groups.append(value)
  keys.append((int.from_bytes(bytes(groups[::2]),'big'),int.from_bytes(bytes(groups[1::2]),'big')))
 return keys


def merge(table,values):
 value=0
 for byte in values:value=(value>>1)|table[byte]
 return value


def des_block(key,block,tables,decrypt=False):
 demand(isinstance(block,bytes) and len(block)==8 and type(decrypt)is bool,'Synthetic block domain')
 left=merge(tables['Ip_l'],block);right=merge(tables['Ip_r'],block)
 keys=key_schedule(key,tables)
 for even_key,odd_key in keys[::-1]if decrypt else keys:
  rotated=rotate(right,1,32);even=rotate(rotated,28,32)^even_key;odd=rotated^odd_key
  new=left
  for box in range(8):
   index=((even if box%2==0 else odd)>>((3-box//2)*8))&63
   new ^=tables['Psboxes'][box*64+index]
  left,right=right,new&0xffffffff
 order=[byte for i in range(4)for byte in ((right>>(i*8))&255,(left>>(i*8))&255)]
 return merge(tables['Ip_inv_l'],order).to_bytes(4,'big')+merge(tables['Ip_inv_r'],order).to_bytes(4,'big')


def rounded_length(length):
 demand(type(length)is int and 0<=length<=4096,'Synthetic length domain')
 return(length+7)&~7


def transform(key,backing,length,mode,tables):
 """Require explicit backing bytes; historical wrapper supplies no padding."""
 demand(isinstance(backing,bytes) and len(backing)<=4096 and type(mode)is int and 0<=mode<=3,'Synthetic wrapper inputs')
 end=rounded_length(length);demand(len(backing)>=end,'No invented padding')
 return b''.join(des_block(key,backing[i:i+8],tables,bool(mode&1))for i in range(0,end,8))+backing[end:]


def wrapper_return(mode):
 demand(type(mode)is int and 0<=mode<=3,'Synthetic mode')
 return 0 if mode&2 else 1


def source_crosscheck(root):
 import Crypto
 from Crypto.Cipher import DES
 from Crypto.SelfTest.Cipher import test_DES
 demand(Crypto.__version__=='3.23.0','Independent oracle version drift')
 raw,tables=load_source(root)
 passed=0
 for row in test_DES.test_data:
  plain,cipher,key=map(bytes.fromhex,row[:3])
  demand(des_block(key,plain,tables)==cipher,'Published DES forward vector')
  demand(des_block(key,cipher,tables,True)==plain,'Published DES inverse vector')
  demand(DES.new(key,DES.MODE_ECB).encrypt(plain)==cipher,'Independent oracle disagreement')
  passed+=1
 # Synthetic storage/first-half login projection. No real account values.
 key=b'R1-key!!';first=b'R1-first-input'.ljust(16,b'\0');second=b'R1-second-half!!'
 demand(len(first)==16 and len(second)==16,'Synthetic block shape')
 full=first+second;stored=transform(key,full,32,0,tables)
 recovered=transform(key,stored,32,1,tables);login=transform(key,stored[:16],16,1,tables)
 demand(recovered==full and login==first,'32 vs16 byte flow')
 demand(DES.new(key,DES.MODE_ECB).encrypt(full)==stored,'Independent synthetic flow oracle')
 fixture=Path(test_DES.__file__).read_bytes()
 return {'source_ref':SOURCE_REF,'source_blobs':PINS,'table_hashes':TABLE_HASHES,
         'independent_oracle':'pycryptodome3.23.0','published_fixture_sha256':hashlib.sha256(fixture).hexdigest(),
         'published_forward_inverse_vectors_passed':passed,
         'synthetic_32byte_storage_16byte_projection':{'key_hex':key.hex(),'plain_hex':full.hex(),'stored_hex':stored.hex(),'login_plain_hex':login.hex()},
         'word_width_bits':32,'original_program_executed':False,'native_login_verified':False}


def raw_data(payload,layout,rva,count):
 for section in layout['sections']:
  offset=rva-section['vaddr']
  if 0<=offset and offset+count<=section['raw_size']:
   start=section['raw_ptr']+offset;return payload[start:start+count]
 raise ValueError('Data outside bounded raw section')


def probe(payload):
 demand(len(payload)==EXPECTED_BYTES and hashlib.sha256(payload).hexdigest()==EXPECTED_SHA256,'Exact accepted specimen required')
 layout=parse_pe_layout(payload);base=struct.unpack_from('<I',payload,layout['pe_off']+52)[0];windows=[];anchors={}
 for name,(a,b)in WINDOWS.items():
  ins=decode_window(raw_window(payload,layout,a,b),base+a);summary=summarize_window(ins,base,{})
  windows.append({'label':name,'start_rva':a,'end_rva_exclusive':b,
                  **{k:summary[k]for k in ('instruction_count','calls','branches','absolute_writes')}})
  for i in ins:
   if i.address-base in (0x206b7,0x2074c,0x2074e,0x2075d,0x2097d,0x2097e,0x2098d,0x20baa,0x20bdb,0x211e0,0x8f16a,0x8f177,0x8f192):
    anchors[hex(i.address-base)]={'operation':i.mnemonic,'operands':operand_metadata(i,base)}
 hashes={name:hashlib.sha256(raw_data(payload,layout,rva,count*width)).hexdigest()for name,(rva,count,width)in TABLES.items()}
 demand(hashes==TABLE_HASHES,'Compiled table profile drift')
 return {'schema':'STONEAGE-WAYI-LOGIN-INPUT-R1','input_bytes':len(payload),'decompressed_input_sha256':EXPECTED_SHA256,
         'windows':windows,'anchors':anchors,'tables':[{ 'name':n,'rva':r,'entries':c,'width_bytes':w,'sha256':hashes[n]}for n,(r,c,w)in TABLES.items()],
         'key_literal':read_literal(payload,layout,0xa248c),'file_executed':False,'packets_captured':False,'native_login_verified':False}


def validate(report):
 p=report['probe'];demand(p['schema']=='STONEAGE-WAYI-LOGIN-INPUT-R1'and p['input_bytes']==EXPECTED_BYTES and p['decompressed_input_sha256']==EXPECTED_SHA256,'Specimen')
 demand([(r['label'],r['start_rva'],r['end_rva_exclusive'])for r in p['windows']]==[(n,a,b)for n,(a,b)in WINDOWS.items()],'Window coverage')
 demand(p['tables']==[{'name':n,'rva':r,'entries':c,'width_bytes':w,'sha256':TABLE_HASHES[n]}for n,(r,c,w)in TABLES.items()],'Tables')
 demand(p['key_literal']=='f;encor1c','Compiled key literal')
 for rva,value in ((0x2074e,8),(0x2075d,32),(0x2097e,8),(0x2098d,32),(0x20baa,12),(0x20bdb,12)):
  demand(p['anchors'][hex(rva)]['operands'][-1].get('value')==value,'UI size/profile')
 demand(all(p[k]is False for k in ('file_executed','packets_captured','native_login_verified')),'Native promotion')
 s=report['crosscheck'];demand(s['source_ref']==SOURCE_REF and s['source_blobs']==PINS and s['table_hashes']==TABLE_HASHES,'Source identity')
 demand(s['published_forward_inverse_vectors_passed']==121 and s['word_width_bits']==32 and s['independent_oracle']=='pycryptodome3.23.0','Oracle scope')
 demand(s['original_program_executed']is False and s['native_login_verified']is False,'Oracle/native conflation')
 return p


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--client',type=Path);p.add_argument('--source-root',type=Path);a=p.parse_args()
 if a.client:print(json.dumps(probe(a.client.read_bytes()),indent=2))
 if a.source_root:print(json.dumps(source_crosscheck(a.source_root),indent=2))
