"""Bounded keyed field reconstruction, static probe and pinned source selector.

Only synthetic data is transformed. Original client/server code is never run.
Strict model errors are not claims about malformed historical input behavior.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

from tools.stoneage_wayi_codec_profile import ALPHABET, permute
from tools.stoneage_jss_launcher_deep_probe import parse_pe_layout
from tools.stoneage_wayi_pet_sender_probe import EXPECTED_BYTES, EXPECTED_SHA256
from tools.stoneage_wayi_saupdate_route_probe import decode_window, raw_window, operand_metadata
from tools.stoneage_wayi_pet_transport_probe import summarize_window

WINDOWS = {
    'integer-pack-plus-key': (0x90080, 0x9018a),
    'integer-unpack-minus-key': (0x90190, 0x90304),
    'string-pack-minus-key': (0x90310, 0x9041c),
    'string-unpack-plus-key': (0x90420, 0x9058f),
    'integer-decode-wrapper': (0x90740, 0x9079e),
    'integer-encode-wrapper': (0x907a0, 0x90855),
    'string-decode-wrapper': (0x90860, 0x90894),
    'string-encode-wrapper': (0x908a0, 0x90949),
    'connection-full-function': (0x5f510, 0x5fa7b),
    'login-two-string-emitter': (0x93500, 0x93562),
    'login-input-transform': (0x8f150, 0x8f19e),
}
PINS = {
    'server/common/gmsv_server_send.c': '099efdea50f6dcb4c7fc3a4831d612ea7a2f1b08',
    'server/gmsv/include/version.h': 'cd68519a68a90b1123f298e16afa00d5798cd844',
    'server/gmsv/include/correct_bug.h': 'ceb8e5f8c4a5c3725d8c205f5f5a65ad39108a70',
    'server/common/common.h': '97b90d4aca6bf0a4f701356166b9d9ad4ca48621',
    'server/gmsv/autil.c': 'c1f4886c879d6d847017cc53373e9e6ead28ae28',
    'client/stoneage/proto/autil.cpp': '369f2b35a812535557d55496626ff6a2cac1c56b',
}


def demand(ok, message):
    if not ok: raise ValueError(message)


def check_key(key):
    demand(isinstance(key, bytes) and 1 <= len(key) <= 64 and 0 not in key, 'Nonempty bounded C-string key')


def keyed_pack(data, key, sign):
    check_key(key)
    demand(isinstance(data, bytes) and len(data) <= 4096 and sign in (-1,1), 'Synthetic packing domain')
    out = bytearray()
    for pos in range(0,len(data),3):
        group=data[pos:pos+3]; word=int.from_bytes(group,'little')
        for _ in range(4 if len(group)==3 else len(group)):
            out.append(ALPHABET[(word + sign*key[len(out)%len(key)])&63]);word >>= 6
        if word:
            out.append(ALPHABET[(word + sign*key[len(out)%len(key)])&63])
    return bytes(out)


def keyed_unpack(token, key, sign):
    check_key(key)
    demand(isinstance(token,bytes) and len(token)<=5462 and sign in (-1,1) and all(c in ALPHABET for c in token),'Synthetic unpacking domain')
    out=bytearray(); residual=0
    for i,c in enumerate(token):
        val=(ALPHABET.index(c)+sign*key[i%len(key)])&63
        if i%4:
            residual |= val << ((4-i%4)*2)
            out.append(residual&255);residual >>= 8
        else:residual=val
    if residual:out.append(residual&255)
    return bytes(out)


def encode_int(value,key):
    demand(type(value) is int and -(1<<31)<=value<(1<<31),'Signed int32 domain')
    return keyed_pack(bytes(c^255 for c in permute(struct.pack('<i',value),'3142')),key,1)


def decode_int(token,key):
    demand(isinstance(token,bytes) and len(token) in (5,6),'Valid encoded int domain')
    raw=keyed_unpack(token,key,-1)
    # Native helper writes its terminating NUL after decoded bytes. Exactly
    # three decoded bytes therefore supply a fourth zero to the int32 read.
    demand(len(raw) in (3,4),'Decoded int size')
    raw=raw+b'\0' if len(raw)==3 else raw
    return struct.unpack('<i',permute(bytes(c^255 for c in raw),'2413'))[0]


def encode_string(value,key):
    demand(isinstance(value,bytes) and len(value)<=4096 and 0 not in value,'Synthetic C-string domain')
    return keyed_pack(value,key,-1)


def decode_string(token,key):
    return keyed_unpack(token,key,1)


def handshake_branch(first_byte):
    demand(type(first_byte) is int and 0<=first_byte<=255,'Synthetic greeting byte')
    if first_byte==ord('E'):return 'error-message'
    if first_byte==ord('F'):return 'set-mode-0x0f000001'
    return 'version-error'


def source_selector(root):
    """Preprocess the exact bounded selector under actual pinned headers.

    This is a named header/selector profile, not a whole-program build.
    """
    root=Path(root).resolve(); raw={}
    for path,pin in PINS.items():
        b=(root/path).read_bytes()
        sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        demand(sha==pin,'Source blob drift: '+path);raw[path]=b.decode('utf-8-sig')
    source=raw['server/common/gmsv_server_send.c']
    anchor=source.index('CONNECT_getCdkey(client_fd, PersonalKey, 4096);')
    end=source.index('if (!util_SplitMessage',anchor)
    fragment=source[anchor:end]
    demand(fragment.count('#ifdef _NEW_FUNC_DECRYPT')==1 and fragment.count('#else')==1 and fragment.count('#endif')==1,'Ambiguous decoder selector')
    flags=['gcc','-E','-P','-x','c','-I'+str(root/'server/gmsv/include'),'-I'+str(root/'server/common'),'-include','version.h','-']
    results={}
    for profile,prefix in [('default',''),('controlled-undef','#undef _NEW_FUNC_DECRYPT\n')]:
        p=subprocess.run(flags,input=prefix+fragment,text=True,capture_output=True,timeout=30)
        demand(p.returncode==0,'Selector preprocessing failed: '+p.stderr[-400:])
        results[profile]={'tea_decoder_call_present':'util_DecodeMessageTea(raw, encoded)' in p.stdout,
                          'legacy_decoder_call_present':'util_DecodeMessage(raw, encoded)' in p.stdout,
                          'cdkey_then_running_suffix_present':'CONNECT_getCdkey(client_fd, PersonalKey, 4096)' in p.stdout and 'strcat(PersonalKey, "shiqi.hk")' in p.stdout}
    demand(results['default']['tea_decoder_call_present'] and not results['default']['legacy_decoder_call_present'],'Default selector drift')
    demand(results['controlled-undef']['legacy_decoder_call_present'] and not results['controlled-undef']['tea_decoder_call_present'],'Controlled selector drift')
    return {'ref':'2f736808ff4361f5429ee919b718c88fabb60346','source_blobs':PINS,
            'selector_fragment_sha256':hashlib.sha256(fragment.encode()).hexdigest(),
            'profiles':results,'scope':'exact selector fragment plus pinned version/correct_bug/common headers; not full source translation unit or deployment',
            'source_program_executed':False,'matching_operator_server':False}


def probe(payload):
    demand(len(payload)==EXPECTED_BYTES and hashlib.sha256(payload).hexdigest()==EXPECTED_SHA256,'Expected exact accepted specimen')
    layout=parse_pe_layout(payload);base=struct.unpack_from('<I',payload,layout['pe_off']+52)[0]
    windows=[];anchors={}
    for name,(a,b) in WINDOWS.items():
        ins=decode_window(raw_window(payload,layout,a,b),base+a)
        summary=summarize_window(ins,base,{})
        windows.append({'label':name,'start_rva':a,'end_rva_exclusive':b,
                        **{k:summary[k] for k in ('instruction_count','calls','branches','absolute_writes')}})
        for i in ins:
            if i.address-base in (0x90105,0x90107,0x90255,0x90263,0x90393,0x90399,0x904f3,0x904f5,0x5f7fe,0x5f809,0x5f81c,0x5f96d,0x5f99a,0x9354f):
                anchors[hex(i.address-base)]={'operation':i.mnemonic,'operands':operand_metadata(i,base)}
    return {'schema':'STONEAGE-WAYI-KEYED-FIELDS-R1','input_bytes':len(payload),
            'decompressed_input_sha256':EXPECTED_SHA256,'windows':windows,'anchors':anchors,
            'file_executed':False,'packets_captured':False,'matching_server_verified':False}


def validate(report):
    p=report['probe']
    demand(p['schema']=='STONEAGE-WAYI-KEYED-FIELDS-R1','Evidence schema')
    demand(p['input_bytes']==EXPECTED_BYTES and p['decompressed_input_sha256']==EXPECTED_SHA256,'Specimen identity')
    demand([(x['label'],x['start_rva'],x['end_rva_exclusive']) for x in p['windows']]==[(n,a,b)for n,(a,b)in WINDOWS.items()],'Bounded windows drift')
    for rva,op in ((0x90105,'add'),(0x90255,'sub'),(0x90393,'sub'),(0x904f3,'add')):
        demand(p['anchors'][hex(rva)]['operation']==op,'Directional arithmetic drift')
    for rva,val in ((0x5f7fe,69),(0x5f809,70),(0x5f81c,0x0f000001),(0x9354f,71)):
        demand(p['anchors'][hex(rva)]['operands'][-1].get('value')==val,'Handshake/login identity')
    demand(all(p[k] is False for k in ('file_executed','packets_captured','matching_server_verified')),'Native promotion')
    for row in report['integer_vectors']:
        k=bytes.fromhex(row['key_hex']);t=bytes.fromhex(row['token_hex'])
        demand(encode_int(row['value'],k)==t and decode_int(t,k)==row['value'],'Integer vector')
    for row in report['string_vectors']:
        k=bytes.fromhex(row['key_hex']);v=bytes.fromhex(row['value_hex']);t=bytes.fromhex(row['token_hex'])
        demand(encode_string(v,k)==t and decode_string(t,k)==v,'String vector')
    source=report['source_selector']
    demand(source['source_program_executed'] is False and source['matching_operator_server'] is False,'Source promotion')
    demand(source['source_blobs']==PINS,'Source pin profile')
    demand(source['profiles']['default']['tea_decoder_call_present'] and not source['profiles']['default']['legacy_decoder_call_present'],'Default decoder profile')
    demand(source['profiles']['controlled-undef']['legacy_decoder_call_present'] and not source['profiles']['controlled-undef']['tea_decoder_call_present'],'Controlled decoder profile')
    return p


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client',type=Path);parser.add_argument('--source-root',type=Path)
    args=parser.parse_args()
    if args.client:print(json.dumps(probe(args.client.read_bytes()),indent=2))
    if args.source_root:print(json.dumps(source_selector(args.source_root),indent=2))
