"""Static qualification of one preserved client/SAAC/GMSV candidate.

Never executes a historical program. Private source mode invokes only a supplied
UnRAR extractor and emits bounded derived facts; credentials/text/binaries stay
outside Git. Public CI checks the frozen source-derived report and negative gates.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
import struct
import subprocess
import zlib

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-SCENE33-SOURCE-PAIR-R1.json'
AUDIT=ROOT/'research/recovered/STONEAGE-SCENE33-ACTUAL-PRIVATE-STATIC-AUDIT-R1.json'
AUDIT_SHA='9e5cac819ee808332d772f40c177fdecf3f84571f1748ce057bfe760fa169bf8'
ARCHIVE_SHA='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
PINS={
 'gmsv/gmsv.exe':(1897867,'d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00'),
 'saac/saac.exe':(178353,'299910efe3d04ccf83a224a6f670c9fabe379440df36d6e0bf6514d76c834615'),
 'gmsv/setup.cf':(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d'),
 'saac/acserv.cf':(807,'95d3414597dfb2617ea3fc6fd8bcf134652908661d55b03e04c4fe3e76979045'),
 'SA2.5服務端/readme.txt':(1345,'c1140aebf9d08a90f1eec62fd27c766b8a4efa4355a6673179b59782ff657b8f'),
 'stoneage2.5/sa_2903.exe':(561152,'ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16'),
 'gmsv/cygwin1.dll':(1295582,'c0e27ae6a7b7106da5db889980a17fe55ea515ebfb3d4c03ce1e26d51bf9c73e'),
 'saac/cygwin1.dll':(1295582,'c0e27ae6a7b7106da5db889980a17fe55ea515ebfb3d4c03ce1e26d51bf9c73e'),
}
FALSE=('historical_programs_executed','SAAC_GMSV_handshake_observed','server_ports_bound_observed',
 'client_loopback_endpoint_control_verified','client_server_protocol_compatibility_verified',
 'original_world_entered','same_deployed_build_authenticated','official_TW10_pair_authenticated',
 'clean_25_runtime_authenticated','database_requirement_resolved','historical_credentials_published',
 'original_binaries_or_config_text_published')
FROZEN_SHA='d584790cda271b41c736bc932b8386d39a53f18ec422ebec5a61e1b58a597657'

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(r):return json.dumps(r,sort_keys=True,separators=(',',':')).encode()

def config_rows(raw):
    text=raw.decode('cp950');need(text.encode('cp950')==raw,'CP950 config roundtrip')
    rows=[];opaque=[]
    for number,line in enumerate(text.splitlines(),1):
        s=line.strip()
        if not s or s.startswith('#'):continue
        parts=s.split('=',1)if '='in s else s.split(None,1)
        key=parts[0].strip();value=parts[1].strip()if len(parts)>1 else ''
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',key):opaque.append(number);continue
        rows.append(dict(line=number,key=key,value=value))
    return rows,opaque

def one(rows,key):
    values=[r['value']for r in rows if r['key']==key]
    need(len(values)==1,'unique original config key: '+key)
    return values[0]

def config_pair(gmsv,saac):
    g,go=config_rows(gmsv);a,ao=config_rows(saac)
    return dict(gmsv_active_key_occurrences=len(g),saac_active_key_occurrences=len(a),
        gmsv_opaque_line_numbers=go,saac_opaque_line_numbers=ao,
        acserv_host=one(g,'acserv'),gmsv_acserv_port=int(one(g,'acservport')),
        saac_listen_port=int(one(a,'port')),gmsv_player_port=int(one(g,'port')),
        static_auth_token_bytes_equal=one(g,'acpasswd').encode('cp950')==one(a,'pass').encode('cp950'),
        auth_values_published=False,mapdir=one(g,'mapdir'),npcdir=one(g,'npcdir'),
        blank_startup_values=[r['key']for r in g if r['key']in ('apport','looptime','enableservice')and r['value']==''],
        saac_USEMSSQL_value=one(a,'USEMSSQL'),saac_AUTOREG_value=one(a,'AUTOREG'),
        config_switch_is_not_runtime_database_proof=True)

def pe_imports(raw):
    need(len(raw)>128 and raw[:2]==b'MZ','PE MZ header')
    pe=struct.unpack_from('<I',raw,60)[0];need(pe+24<=len(raw)and raw[pe:pe+4]==b'PE\0\0','PE signature')
    machine,n,stamp,_,_,optional_size,flags=struct.unpack_from('<HHIIIHH',raw,pe+4)
    op=pe+24;need(op+optional_size+n*40<=len(raw)and optional_size>=112,'PE header extent')
    magic=struct.unpack_from('<H',raw,op)[0];need(magic==0x10b,'bounded PE32 reader')
    sections=[]
    for i in range(n):
        p=op+optional_size+i*40;vs,va,size,offset=struct.unpack_from('<IIII',raw,p+8)
        need(offset+size<=len(raw),'PE section raw range');sections.append((va,vs,size,offset))
    def off(rva,length=1):
        for va,vs,size,offset in sections:
            if va<=rva<va+max(vs,size):
                d=rva-va;need(d+length<=size,'PE virtual-only or truncated range');return offset+d
        raise ValueError('PE unmapped RVA')
    def cstring(rva):
        start=off(rva)
        limit=next(offset+size for va,vs,size,offset in sections if va<=rva<va+max(vs,size))
        end=raw.find(b'\0',start,min(limit,start+256));need(end>=start,'PE string extent')
        return raw[start:end].decode('ascii')
    import_rva=struct.unpack_from('<I',raw,op+104)[0];descriptors=[]
    if import_rva:
        for i in range(64):
            p=off(import_rva+i*20,20);lookup,ts,forward,name,iat=struct.unpack_from('<IIIII',raw,p)
            if not any((lookup,ts,forward,name,iat)):break
            symbols=[]
            for j in range(4096):
                value=struct.unpack_from('<I',raw,off((lookup or iat)+4*j,4))[0]
                if not value:break
                symbols.append('#'+str(value&0xffff)if value&0x80000000 else cstring(value+2))
            else:raise ValueError('PE import symbol bound')
            descriptors.append(dict(descriptor_index=i,dll=cstring(name),import_symbol_count=len(symbols),
                dynamic_library_loader_imported=any(x in symbols for x in ('LoadLibraryA','LoadLibraryW','dlopen')),
                sql_named_import_symbols=sum(bool(re.match(r'(?i)(mysql|SQL|odbc)',x))for x in symbols)))
        else:raise ValueError('PE import descriptor bound')
    return dict(machine=machine,optional_magic=magic,subsystem=struct.unpack_from('<H',raw,op+68)[0],
        is_DLL=bool(flags&0x2000),COFF_timestamp_raw=stamp,timestamp_is_not_release_authentication=True,
        import_descriptors=descriptors,import_DLL_occurrences=[d['dll']for d in descriptors],
        dynamic_loads_and_transitive_runtime_dependencies_fully_resolved=False)

def rar_receipt(raw,members):
    need(len(raw)==361255180 and sha(raw)==ARCHIVE_SHA,'complete original archive')
    need(raw[:7]==b'Rar!\x1a\x07\x00','RAR4 magic');pos=7;count=0;selected=[]
    while pos<len(raw):
        need(pos+7<=len(raw),'RAR header extent');crc,kind,flags,size=struct.unpack_from('<HBHH',raw,pos)
        need(size>=7 and pos+size<=len(raw),'RAR header size');h=raw[pos:pos+size]
        need(zlib.crc32(h[2:])&0xffff==crc,'RAR header CRC');extra=struct.unpack_from('<I',h,7)[0]if flags&0x8000 else 0
        if kind==0x74:
            count+=1;need(len(h)>=32 and not flags&0x100,'bounded RAR4 member')
            packed,unpacked,host,file_crc,mtime,ver,method,nlen,attr=struct.unpack_from('<IIBIIBBHI',h,7)
            legacy=h[32:32+nlen].split(b'\0',1)[0].replace(b'\\',b'/');extra=packed
            for key,data in members.items():
                suffix=b'/readme.txt'if key.startswith('SA2.5')else b'/'+key.encode('ascii')
                if not legacy.endswith(suffix)or unpacked!=len(data)or zlib.crc32(data)&0xffffffff!=file_crc:continue
                need(not flags&(1|2|4|16),'split/encrypted/solid member excluded')
                selected.append(dict(target=key,header_offset=pos,header_bytes=size,packed_bytes=packed,
                    unpacked_bytes=unpacked,header_sha256=sha(h),packed_sha256=sha(raw[pos+size:pos+size+packed]),
                    member_crc32=file_crc,member_sha256=sha(data)))
        need(pos+size+extra<=len(raw),'RAR packed range');pos+=size+extra
    need(pos==len(raw)and count==7952,'complete original header inventory')
    need(len(selected)==8 and Counter(r['target']for r in selected)==Counter(members.keys()),'eight unique original member headers')
    return dict(all_file_headers_scanned=count,all_header_CRCs_verified=True,selected_member_CRCs_verified=True,
        header_parser_is_not_second_decompressor=True,members=selected)

def source_probe(archive,unrar,out):
    out=out.resolve();need(out!=ROOT and ROOT not in out.parents and not out.exists(),'new private folder outside Git')
    raw=archive.read_bytes();need((len(raw),sha(raw))==(361255180,ARCHIVE_SHA),'original parent SHA')
    listed=subprocess.run([str(unrar),'lb','-p-',str(archive)],capture_output=True,check=True,timeout=30).stdout.decode('utf-8').splitlines()
    normalized=[s.replace('\\','/').rstrip('/')for s in listed];out.mkdir(mode=0o700,parents=True);members={};inputs=[]
    for key,pin in PINS.items():
        matches=[s for s in normalized if s.endswith('/'+key)];need(len(matches)==1,'unique selected original archive member '+key)
        data=subprocess.run([str(unrar),'p','-inul','-p-',str(archive),matches[0]],capture_output=True,check=True,timeout=30).stdout
        need((len(data),sha(data))==pin,'actual member size/SHA '+key);members[key]=data
        target=out/key;target.parent.mkdir(mode=0o700,parents=True,exist_ok=True);target.write_bytes(data)
        inputs.append(dict(path=key,bytes=len(data),sha256=sha(data)))
    config=config_pair(members['gmsv/setup.cf'],members['saac/acserv.cf'])
    base=next(s.rsplit('/',1)[0]for s in normalized if s.endswith('/gmsv/gmsv.exe'))
    g,_=config_rows(members['gmsv/setup.cf']);references=[]
    path_keys=['LOCKIP','USEREXP','maptilefile','battlemapfile','itemset6file','itemset5file','itemset4file','itemset3file',
        'invinciblefile','appearpositionfile','titlenamefile','titleconfigfile','encountfile','enemyfile','enemybasefile','groupfile',
        'magicfile','attmagicfile','petskillfile2','petskillfile1','itematomfile','effectfile','quizfile','gmsetfile']
    folded=Counter(s.casefold()for s in normalized)
    for key in path_keys:
        value=one(g,key);resolved=posixpath.normpath(base+'/'+value)
        references.append(dict(config_key=key,relative_path=value,archive_occurrences=folded[resolved.casefold()],
            required_at_startup_proven=False))
    readme=members['SA2.5服務端/readme.txt'].decode('cp950');config_text=members['gmsv/setup.cf'].decode('cp950')
    r=dict(schema='stoneage.scene33.static_source_pair.r1',source_scope='MIXED_MODIFIED_COMMUNITY_PRESERVATION_NOT_OFFICIAL_TW1',
        parent_archive=dict(bytes=len(raw),sha256=sha(raw)),source_inputs=inputs,original_RAR_witness=rar_receipt(raw,members),
        config_pair=config,binaries={key:pe_imports(data)for key,data in members.items()if key.endswith(('.exe','.dll'))},
        startup_file_references=references,source_readme_says_saac_before_gmsv=('1。開啟 saac'in readme and '2。開啟 gmsv'in readme),
        readme_document_date_token_2009_01_20_present='2009.01.20'in readme,
        startup_config_comment_8_0_present='8.0'in config_text,
        client_literal_IP_colon_marker_occurrences=members['stoneage2.5/sa_2903.exe'].count(b'IP:'),
        static_candidate_status='STATIC_SERVER_CONFIG_AND_X86_DEPENDENCIES_QUALIFIED_RUNTIME_PAIR_OPEN',
        extraction_witness=dict(successful_decompressor='RARLab official-source local UnRAR 7.30 beta 2',
            successful_second_decompressor_for_all_eight=False,
            prior_system_libarchive_failure='Parsing filters is unsupported (cygwin1.dll)',
            header_CRC_is_not_second_decompression=True),
        original_world_entry_minimum_next='ISOLATED_SAAC_GMSV_LOOPBACK_BOOT_BEFORE_ANY_CLIENT_OR_REAL_ACCOUNT',
        source_action_run_id=None,overall_percent=None,**{k:False for k in FALSE})
    (out/'source-derived-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    return r

def validate(r):
    need(r['schema']=='stoneage.scene33.static_source_pair.r1','schema')
    need(r['source_scope']=='MIXED_MODIFIED_COMMUNITY_PRESERVATION_NOT_OFFICIAL_TW1','source/version boundary')
    need(r['parent_archive']==dict(bytes=361255180,sha256=ARCHIVE_SHA),'parent archive identity')
    need({x['path']:(x['bytes'],x['sha256'])for x in r['source_inputs']}==PINS and len(r['source_inputs'])==8,'eight exact source identities')
    need(all(r[k]is False for k in FALSE),'static is not runtime/official/correctness proof')
    need(r['source_action_run_id']is None and r['overall_percent']is None,'source/percent not invented')
    c=r['config_pair'];need((c['acserv_host'],c['gmsv_acserv_port'],c['saac_listen_port'],c['gmsv_player_port'])==('localhost',9200,9200,9065),'original static host/port join')
    need(c['static_auth_token_bytes_equal']is True and c['auth_values_published']is False,'credential equality only')
    need(c['blank_startup_values']==['apport','looptime','enableservice'],'original blank fields retained')
    need(len(r['binaries'])==5,'five original PE occurrences including both DLL copies')
    for key,b in r['binaries'].items():
        need(b['machine']==0x14c and b['optional_magic']==0x10b,'original x86 PE32')
        need(b['dynamic_loads_and_transitive_runtime_dependencies_fully_resolved']is False,'finite import coverage')
    need(r['binaries']['gmsv/gmsv.exe']['import_DLL_occurrences']==['cygwin1.dll','cygwin1.dll','cygwin1.dll','KERNEL32.dll','cygwin1.dll','cygwin1.dll'],'preserve duplicate import descriptor positions')
    need(r['readme_document_date_token_2009_01_20_present']and r['startup_config_comment_8_0_present'],'modified lineage markers')
    refs=r['startup_file_references']
    need(len(refs)==24 and [x['config_key']for x in refs if x['archive_occurrences']==0]==['LOCKIP'],'bounded original reference coverage')
    need(all(x['required_at_startup_proven']is False for x in refs),'path presence is not startup validity')
    need(r['extraction_witness']['successful_second_decompressor_for_all_eight']is False,'one successful decompressor only')
    need(r['static_candidate_status']=='STATIC_SERVER_CONFIG_AND_X86_DEPENDENCIES_QUALIFIED_RUNTIME_PAIR_OPEN','bounded candidate status')
    need(sha(canonical(r))==FROZEN_SHA,'frozen actual original static source receipt')
    return dict(source_members=8,static_server_config_ports_match=True,all_runtime_pairing_and_world_claims_remain_open=True)

def validate_audit(a,r):
    need(a['source_report_sha256']==sha(REPORT.read_bytes()) and a['canonical_source_report_sha256']==sha(canonical(r)),'actual audit/report binding')
    need(a['actual_source_members']==8 and a['actual_source_member_bytes']==sum(p[0]for p in PINS.values()),'actual audit member coverage')
    checks=a['five_actual_PE_import_comparisons']
    need(len(checks)==5 and {x['path']for x in checks}==set(r['binaries']),'actual audit PE occurrence coverage')
    for x in checks:
        need(x['sha256']==PINS[x['path']][1] and x['ordered_import_DLL_descriptors_match']is True and x['descriptor_occurrences']==len(r['binaries'][x['path']]['import_DLL_occurrences']),'independent actual import comparison')
    need(a['historical_programs_executed']is False and a['original_world_entered']is False and a['source_action_run_id']is None,'actual static audit is not execution')
    need(sha(canonical(a))==AUDIT_SHA,'frozen actual independent static audit')
    return True

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--archive',type=Path);ap.add_argument('--unrar',type=Path);ap.add_argument('--private-output',type=Path);args=ap.parse_args()
    if args.archive:
        need(args.unrar is not None and args.private_output is not None,'explicit extractor and private output required')
        r=source_probe(args.archive,args.unrar,args.private_output);print(json.dumps({'static_report_SHA256':sha(canonical(r)),'source_members':8,'historical_programs_executed':False}))
    else:
        r=json.loads(REPORT.read_text());result=validate(r);validate_audit(json.loads(AUDIT.read_text()),r)
        print(json.dumps(result))

if __name__=='__main__':main()
