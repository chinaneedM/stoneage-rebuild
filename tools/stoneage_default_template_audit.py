"""Execute actual pinned defaultPlayer/table/getter with original headers.

Source stays transient. Derived enums, hashes and host-layout observations are
receipts, not original executable ABI or natural enemy-creation evidence.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_character_reuse_audit import source_domain as reuse_domain

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT/'research/recovered/STONEAGE-DEFAULT-TEMPLATE-SOURCE-DOMAINS-R1.json'
RESOLUTION = 'BOUNDED_ACTUAL_DEFAULT_TEMPLATE_HEADERS_PASS_ZERO_RUNTIME_PROMOTIONS'
SYMBOLS = ('CHAR_DATAINTNUM','CHAR_INITDATA','CHAR_IMAGETYPE','CHAR_WHICHTYPE',
           'CHAR_WORKDATAINTNUM','CHAR_WORKOBJINDEX','CHAR_WORKTICKETTIME',
           'CHAR_WORKTICKETTIMESTART','CHAR_WORKFD','CHAR_WORKCHATROOMNUM',
           'CHAR_BECOMEPIG','CHAR_BECOMEPIG_BBI')


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value,str) else value).hexdigest()


def expression(value, symbols):
    """Restricted integer C-expression subset; reject unsupported syntax."""
    node=ast.parse(value.strip(),mode='eval').body
    def walk(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,int):return n.value
        if isinstance(n,ast.Name):return symbols[n.id]
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
            return -walk(n.operand) if isinstance(n.op,ast.USub) else walk(n.operand)
        if isinstance(n,ast.BinOp):
            a,b=walk(n.left),walk(n.right)
            ops={ast.Add:lambda:a+b,ast.Sub:lambda:a-b,ast.Mult:lambda:a*b,
                 ast.LShift:lambda:a<<b,ast.RShift:lambda:a>>b,
                 ast.BitOr:lambda:a|b,ast.BitAnd:lambda:a&b}
            if type(n.op) in ops:return ops[type(n.op)]()
        raise ValueError('unsupported integer initializer expression')
    return walk(node)


def enums(text):
    values={}
    for match in re.finditer(r'typedef\s+enum(?:\s+\w+)?\s*\{([^{}]+)\}\s*\w+\s*;',text):
        previous=-1
        for entry in match[1].split(','):
            entry=entry.strip()
            if not entry:continue
            pair=entry.split('=',1);name=pair[0].strip()
            if not re.fullmatch(r'\w+',name):raise ValueError('enum syntax drift')
            previous=expression(pair[1],values) if len(pair)==2 else previous+1
            values[name]=previous
    return values


def block(text,marker):
    start=text.index(marker);brace=text.index('{',start);depth=0
    for i in range(brace,len(text)):
        if text[i]=='{':depth+=1
        if text[i]=='}':
            depth-=1
            if not depth:return text[start:i+1]+';'
    raise ValueError('unterminated initializer')


def top_entries(text):
    """Split a brace initializer at top-level commas, preserving nested arrays."""
    body=text[text.index('{')+1:text.rindex('}')];entries=[];start=depth=0
    for i,c in enumerate(body):
        if c in '{(':depth+=1
        elif c in '})':depth-=1
        elif c==',' and depth==0:
            if body[start:i].strip():entries.append(body[start:i].strip())
            start=i+1
    if body[start:].strip():entries.append(body[start:].strip())
    return entries


def include_args(profile,root):
    base=root/LAYOUTS[profile]
    args=['-I'+str(base/'include'),'-I'+str(base/'char')]
    if profile=='bismarck':args+=['-I'+str(root/'server/common'),'-I'+str(root/'shared/lua51')]
    return args


PREFIX = '#include <stdio.h>\n#include <string.h>\n#include <stddef.h>\n#include "version.h"\n#include "char.h"\n#include "anim_tbl.h"\n#include "defaultPlayer.h"\n'


def preprocess(profile,root,source):
    return subprocess.run(['cc','-E','-P',*include_args(profile,root),'-x','c','-'],
        input=source,text=True,capture_output=True,check=True).stdout


def source_domain(profile,root):
    bodies,prior=reuse_domain(profile,root)
    base=root/LAYOUTS[profile]
    raw=re.sub(r'^\s*#\s*include[^\n]*','',_text(base/'char/char_data.c'),flags=re.M)
    pp=preprocess(profile,root,'#include "version.h"\n'+raw)
    table=block(pp,'static defaultCharacterGet CHAR_defaultCharacterGet')
    type_start=pp.index('typedef struct tagdefaultCharcterGet')
    declaration=pp[type_start:pp.index('static defaultCharacterGet CHAR_defaultCharacterGet')]+table
    source=PREFIX+declaration+'\n'+bodies['CHAR_getDefaultChar']+'\n'
    expanded=preprocess(profile,root,source)
    ev=enums(expanded)
    player=block(expanded,'static Char player')
    entries=top_entries(player)
    if len(entries)!=4:raise ValueError('player initializer shape changed')
    if expression(entries[0],ev)!=0:raise ValueError('default use drift')
    data=[expression(v,ev) for v in top_entries(entries[1])]
    flags=[expression(v,ev) for v in top_entries(entries[3])]
    for v in top_entries(entries[2]):
        if re.sub(r'\s+','',v)!='{""}':raise ValueError('nonempty default string requires review')
    rows=top_entries(block(expanded,'static defaultCharacterGet CHAR_defaultCharacterGet'))
    table_rows=[]
    for row in rows:
        image,ptr,level,imgtype=top_entries(row)
        if ptr!='&player' or level!='&lvplayer00':raise ValueError('new template/level pointer; review required')
        table_rows.append([expression(image,ev),expression(imgtype,ev)])
    dependencies=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],
        input=source,text=True,capture_output=True,check=True).stdout
    files={}
    for name in dependencies.replace('\\\n',' ').split()[1:]:
        path=Path(name)
        if path.is_file():
            relative=path.relative_to(root).as_posix();files[relative]=digest(path.read_bytes())
    files[(LAYOUTS[profile]/'char/char_data.c').as_posix()]=digest((base/'char/char_data.c').read_bytes())
    defines=subprocess.run(['cc','-dM','-E',*include_args(profile,root),'-x','c','-'],
        input=PREFIX,text=True,capture_output=True,check=True).stdout
    source_macro_names=set()
    for path in files:
        source_macro_names.update(re.findall(r'^\s*#\s*define\s+(_[A-Z]\w*)',_text(root/path),flags=re.M))
    features=sorted(line for line in defines.splitlines()
                    if len(line.split())>1 and line.split()[1] in source_macro_names)
    identity={'source_sha':PINNED[profile],'files':dict(sorted(files.items())),
        'getter_sha256':prior['functions']['CHAR_getDefaultChar'],
        'preprocessed_player_sha256':digest(_compact(player)),
        'preprocessed_table_sha256':digest(_compact(block(expanded,'static defaultCharacterGet CHAR_defaultCharacterGet'))),
        'feature_definitions_sha256':digest('\n'.join(features)),
        'feature_definition_count':len(features),'enum_values':{k:ev[k] for k in SYMBOLS if k in ev},
        'template_initializer_ints':len(data),'excess_initializer_ints':max(0,len(data)-ev['CHAR_DATAINTNUM']),
        'table_rows':table_rows,'all_rows_share_player':True,
        'template_pig_value':data[ev['CHAR_BECOMEPIG']],
        'template_pig_image':data[ev['CHAR_BECOMEPIG_BBI']],
        'logical_data_sha256':digest(json.dumps(data[:ev['CHAR_DATAINTNUM']],separators=(',',':'))),
        'actual_headers_table_and_defaultPlayer':True,'original_build_and_ABI_not_claimed':True}
    return source,identity,data,flags


def vectors(table):
    images=list(dict.fromkeys([*(row[0] for row in table),31010,-1,0,2147483647]))
    return list(itertools.product(images,(0,0x5a,0xa5,0xff)))


def expected_data(identity,data):
    enum=identity['enum_values'];cut=enum['CHAR_INITDATA'];size=enum['CHAR_DATAINTNUM']
    return data[:cut]+[0]*(size-cut)


def native_source(profile,source,identity,data,flags):
    expected=expected_data(identity,data)
    work=[0]*identity['enum_values']['CHAR_WORKDATAINTNUM']
    work[identity['enum_values']['CHAR_WORKFD']]=-1
    if profile!='bismarck':work[identity['enum_values']['CHAR_WORKCHATROOMNUM']]=-1
    source+='static const int expected_data[]={'+','.join(map(str,expected))+'};\n'
    source+='static const int expected_work[]={'+','.join(map(str,work))+'};\n'
    source+='static const unsigned char expected_flags[]={'+','.join(map(str,flags))+'};\n'
    source+=r'''
static void expected(Char *ch){
 memset(ch,0,sizeof(*ch));ch->use=1;
 memcpy(ch->data,expected_data,sizeof(expected_data));
 memcpy(ch->workint,expected_work,sizeof(expected_work));
 memcpy(ch->flg,expected_flags,sizeof(expected_flags));
 for(int j=0;j<CHAR_MAXITEMHAVE;j++)ch->indexOfExistItems[j]=-1;
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)ch->indexOfExistPoolItems[j]=-1;
 for(int j=0;j<CHAR_MAXPETSKILLHAVE;j++)ch->unionTable.indexOfPetskill[j]=-1;
 for(int j=0;j<CHAR_MAXPOOLPETHAVE;j++)ch->indexOfPoolPet[j]=-1;
 for(int j=0;j<CHAR_TITLEMAXHAVE;j++)ch->indexOfHaveTitle[j]=-1;
'''
    if profile=='bismarck':source+=' for(int j=0;j<CHAR_MAXPETHAVE;j++)ch->unionTable.indexOfPet[j]=-1;\n'
    source+=r'''}
int main(void){
 if(sizeof(void*)!=8 || sizeof(int)!=4)return 9;
 printf("LAYOUT %zu %zu %zu %zu %zu %zu %zu %zu\n",sizeof(Char),offsetof(Char,data),offsetof(Char,string),offsetof(Char,flg),offsetof(Char,charfunctable),offsetof(Char,workint),offsetof(Char,CharMakeSequenceNumber),sizeof(((Char*)0)->flg));
 printf("TEMPLATE %d %d %d\n",player.data[CHAR_IMAGETYPE],player.data[CHAR_BECOMEPIG],player.data[CHAR_BECOMEPIG_BBI]);
 int image,fill;
 while(scanf("%d%d",&image,&fill)==2){
  Char actual,want;expected(&want);memset(&actual,fill,sizeof(actual));
  for(int call=0;call<2;call++){
   int result=CHAR_getDefaultChar(&actual,image);
   printf("CASE %d %d %d %d %d",image,fill,call,result,memcmp(&actual,&want,sizeof(actual))==0);
   for(int j=0;j<CHAR_DATAINTNUM;j++)printf(" %d",actual.data[j]);
   for(int j=0;j<CHAR_WORKDATAINTNUM;j++)printf(" %d",actual.workint[j]);
   for(size_t j=0;j<sizeof(actual.flg);j++)printf(" %u",(unsigned char)actual.flg[j]);
   printf("\n");
  }
 }return 0;
}
'''
    return source


def execute(profile,root,source,payload,opt):
    with tempfile.TemporaryDirectory(prefix='stoneage-template-') as tmp:
        exe=Path(tmp)/'probe'
        result=subprocess.run(['cc','-std=gnu99',opt,'-fsanitize=undefined','-fno-sanitize-recover=all',
            *include_args(profile,root),'-x','c','-','-o',str(exe)],input=source,text=True,capture_output=True)
        if result.returncode:raise ValueError(result.stderr[-4000:])
        # Retain warning counts; do not suppress known positional initializer diagnostics.
        excess=result.stderr.count('warning: excess elements in array initializer')
        output=subprocess.run([str(exe)],input=payload,text=True,capture_output=True,check=True)
        if output.stderr:raise ValueError('unexpected native stderr')
        return output.stdout,excess


def validate_output(profile,identity,data,flags,cases,output):
    lines=output.splitlines()
    if not lines[0].startswith('LAYOUT '):raise ValueError('missing native layout')
    tpl=list(map(int,lines[1].split()[1:]));ev=identity['enum_values']
    if tpl!=[data[ev['CHAR_IMAGETYPE']],identity['template_pig_value'],identity['template_pig_image']]:
        raise ValueError('positional default initializer differs from independent parsing')
    work=[0]*ev['CHAR_WORKDATAINTNUM'];work[ev['CHAR_WORKFD']]=-1
    if profile!='bismarck':work[ev['CHAR_WORKCHATROOMNUM']]=-1
    flgsize=int(lines[0].split()[-1]);expected_flags=flags+[0]*(flgsize-len(flags))
    expected_tail=expected_data(identity,data)+work+expected_flags
    if len(lines)!=2+2*len(cases):raise ValueError('native row cardinality mismatch')
    for line,(image,fill,call) in zip(lines[2:],((i,f,c) for i,f in cases for c in (0,1))):
        if line.split()[0]!='CASE':raise ValueError('bad row')
        if list(map(int,line.split()[1:]))!=[image,fill,call,1,1,*expected_tail]:
            raise ValueError(f'{profile}: complete actual template state mismatch {image}/{fill}/{call}')
    return lines[0]


def audit(profile,root,require_pin=True):
    source,identity,data,flags=source_domain(profile,root)
    if require_pin and identity!=json.loads(PIN_PATH.read_text())['profiles'][profile]:
        raise ValueError('default template source domain drift')
    cases=vectors(identity['table_rows']);payload=''.join(f'{i} {f}\n' for i,f in cases)
    native=native_source(profile,source,identity,data,flags);reference=None;layout=None
    for opt in ('-O0','-O2'):
        output,excess=execute(profile,root,native,payload,opt)
        layout=validate_output(profile,identity,data,flags,cases,output)
        if excess!=identity['excess_initializer_ints']:raise ValueError('initializer warning count drift')
        if reference is not None and output!=reference:raise ValueError('optimization-dependent output')
        reference=output
    mutations=[(r'memset\(\s*nc,\s*0,\s*sizeof\(Char\)\s*\);',';'),
               (r'nc->workint\[j\]\s*=\s*0;', 'nc->workint[j]=12;'),
               (r'nc->indexOfExistItems\[j\]\s*=\s*-1;', 'nc->indexOfExistItems[j]=0;'),
               (r'nc->data\[j\]\s*=\s*defaultchar->data\[j\];','nc->data[j]=0;')]
    witness=[(31010,0xa5)];rejected=0
    for pattern,replacement in mutations:
        changed,n=re.subn(pattern,replacement,native)
        if n!=1:raise ValueError('ambiguous native mutation')
        for opt in ('-O0','-O2'):
            out,_=execute(profile,root,changed,'31010 165\n',opt)
            try:validate_output(profile,identity,data,flags,witness,out)
            except ValueError:rejected+=1
            else:raise ValueError('native semantic mutation escaped')
    return {'profile':profile,'source_sha':PINNED[profile],
        'table_rows':len(identity['table_rows']),'cases_per_optimization':len(cases),
        'native_getter_calls':4*len(cases),'semantic_mutations_rejected':rejected,
        'excess_initializer_warnings':identity['excess_initializer_ints'],
        'host_layout':layout,'semantic_sha256':digest(reference)},identity


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for p in PINNED:
        row,_=audit(p,getattr(args,p+'_dir'));total+=row['native_getter_calls']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|actual_default_template_getter_calls={total}|profiles=3')
    print('FACT|all_actual_table_entries_share_player_template_image_type_write_is_overwritten_by_data_prefix_copy')
    print('FACT|actual_header_getter_zeros_ticket_start_object_and_callback_fields_even_from_dirty_destination')
    print('FACT|default_template_tail_pig_values_are_not_copied_past_CHAR_INITDATA')
    print('BOUNDARY|original_headers_defaultPlayer_table_getter_current_version_h_GNU99_LP64_host_diagnostics_retained')
    print('OPEN|full_enemy_creator_init_helpers_natural_ticket_object_Exit_reuse_original_build_ABI_other_compile_profiles_JSS_Taiwan_v1_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
