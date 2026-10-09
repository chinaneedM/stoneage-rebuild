"""Execute pinned default-character and allocator bodies with explicit adapters.

Original C is extracted transiently, never stored here. Templates, function
lookup/callbacks and fixed positive partitions are controlled evidence domains.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_exit_lifetime_watch_audit import _definition
from tools.stoneage_becomepig_restore_audit import run_native
from tools.stoneage_becomepig_native_audit import _assert_rows

PIN_PATH = Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-CHARACTER-REUSE-SOURCE-DOMAINS-R1.json'
RESOLUTION = 'BOUNDED_DEFAULT_TEMPLATE_ALLOCATOR_REUSE_PASS_ZERO_RUNTIME_PROMOTIONS'
FIELDS = {'CHAR_WHICHTYPE':3, 'CHAR_IMAGETYPE':5, 'CHAR_INITDATA':16,
          'CHAR_WORKTICKETTIME':1, 'CHAR_WORKTICKETTIMESTART':2,
          'CHAR_WORKOBJINDEX':3, 'CHAR_WORKFD':4, 'CHAR_WORKCHATROOMNUM':5}


def source_domain(profile, root):
    head = subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    dirty = subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip()
    if head != PINNED[profile] or dirty:
        raise ValueError('pinned clean source identity drift')
    base = root/LAYOUTS[profile]
    inc = ['-I',str(base/'include')]
    if profile == 'bismarck':
        inc += ['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    def pp(path):
        raw = re.sub(r'^\s*#\s*include[^\n]*','',_text(base/path),flags=re.M)
        return subprocess.run(['cpp','-P',*inc,'-'],input='#include "version.h"\n'+raw,
                              text=True,capture_output=True,check=True).stdout
    bodies = {}
    for path,names in {'char/char_base.c':('CHAR_initCharOneArray','CHAR_constructFunctable'),
                       'char/char_data.c':('CHAR_getDefaultChar',),
                       'char/enemy.c':('ENEMY_createEnemy',)}.items():
        text = pp(path)
        for name in names:
            bodies[name] = _definition(text,name)
    creator = _compact(bodies['ENEMY_createEnemy'])
    var='new_char' if profile=='bismarck' else 'CharNew'
    if f'CHAR_getDefaultChar(&{var},31010)' not in creator or f'CHAR_initCharOneArray(&{var})' not in creator:
        raise ValueError('default/allocator enemy caller contract drift')
    if re.search(r'CHAR_WORK(?:TICKETTIME(?:START)?|OBJINDEX)\b',creator):
        raise ValueError('new direct enemy ticket/object assignment; review required')
    identity = {'source_sha':head,
        'files':{p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in
                 ('char/char_base.c','char/char_data.c','char/enemy.c','include/version.h','include/char_base.h')},
        'functions':{n:hashlib.sha256(_compact(b).encode()).hexdigest() for n,b in bodies.items()},
        'contracts':{'enemy_creator_static_only':True,'enemy_calls_default_31010_and_allocator':True,
                     'enemy_creator_has_no_direct_ticket_or_character_object_symbol':True,
                     'original_default_template_table_not_executed':True,
                     'init_callbacks_and_lookup_controlled':True,
                     'positive_partitions_only':True}}
    return bodies,identity


def vectors():
    out=[]
    for kind in (1,2,3,4):
        size=2 if kind in (1,2) else 3
        for cursor,mask,cb,payload,use,release in itertools.product(
                range(size),range(1<<size),range(4),range(3),(0,1),(0,1)):
            for lazy in ((0,1) if cursor==0 else (0,)):
                out.append((kind,cursor,mask,cb,payload,use,release,lazy))
    return out


def blank(items, value=0):
    # Logical fields of the compatible C witness, not an original ABI layout.
    return {'use':value,'data':[value]*32,'work':[value]*16,'flags':[value]*3,
        'strings':[value]*16,'workchars':[value]*16,'carried':[value]*items,
        'pool':[value]*30,'union':[value]*7,'poolpets':[value]*3,'skills':[value]*3,
        'titles':[value]*3,'address':[value]*8,'callbacks':[value]*16,
        'functions':[0]*2,'sequence':value,'opaque':value}


def template(profile, items, payload):
    if payload==2:
        ch=blank(items,37)
        ch['work'][1:4]=[901,902,903]
        ch['callbacks']=[0]*16
        ch['functions']=[0,0]
        return ch
    # Controlled table entries have nonzero work/callback/opaque fields. The
    # complete original getter intentionally copies only data/flags from them.
    base=100 if payload==0 else 200
    ch=blank(items)
    ch['use']=1
    ch['data']=[base+j if j<16 else 0 for j in range(32)]
    ch['flags']=[base+j for j in range(3)]
    for name in ('carried','pool','union','poolpets','titles'):
        ch[name]=[-1]*len(ch[name])
    ch['work'][4]=-1
    if profile!='bismarck':ch['work'][5]=-1
    return ch


ORDER=('use','data','work','flags','strings','workchars','carried','pool','union',
       'poolpets','skills','titles','address','callbacks','functions','sequence','opaque')


def flatten(ch):
    return [v for name in ORDER for v in (ch[name] if isinstance(ch[name],list) else [ch[name]])]


class Oracle:
    def __init__(self,profile,items,case):
        self.profile,self.items=profile,items
        self.kind,cursor,mask,self.cb,self.payload,self.use,self.release,self.lazy=case
        self.mode=0 if self.kind==1 else 1 if self.kind==2 else 2
        self.starts=[0,2,4];self.ends=[2,4,7];self.cursors=self.starts.copy()
        self.cursors[self.mode]+=cursor
        self.slots=[blank(items,61+i) for i in range(7)]
        for i,ch in enumerate(self.slots):
            ch['use']=1
            ch['work'][1:4]=[999,900,88]
        for j in range(self.ends[self.mode]-self.starts[self.mode]):
            self.slots[self.starts[self.mode]+j]['use']=(mask>>j)&1
        self.ch=template(profile,items,self.payload)
        self.ch['data'][3]=self.kind;self.ch['use']=self.use
        self.ch['callbacks'][0]=self.cb
        self.trace=[];self.seq=0

    def allocate(self,cb):
        start=self.cursors[self.mode];size=self.ends[self.mode]-self.starts[self.mode]
        i=next((self.starts[self.mode]+(start-self.starts[self.mode]+j)%size
                for j in range(size) if not self.slots[self.starts[self.mode]+(start-self.starts[self.mode]+j)%size]['use']),None)
        if i is None:self.trace.extend((90,self.mode));return -1
        ch=copy.deepcopy(self.ch);ch['callbacks'][0]=cb;self.slots[i]=ch
        self.trace.extend((10,cb))
        if cb:
            self.trace.extend((20,i,ch['use'],ch['work'][1],ch['work'][3],ch['sequence']))
            if cb==3:ch['work'][1:4]=[777,666,9]
            if cb==2:ch['use']=0;return -1
        ch['use']=1
        # Original construct body resolves both slots after use becomes true.
        self.trace.extend((10,cb,10,0));ch['functions']=[cb,0]
        self.cursors[self.mode]=self.starts[self.mode]+(i-self.starts[self.mode]+1)%size
        ch['sequence']=self.seq;self.seq+=1
        return i

    def run(self):
        a=self.allocate(self.cb)
        first=[*self.cursors,*(v for ch in self.slots for v in flatten(ch))]
        if a>=0 and self.release:self.slots[a]['use']=0
        b=self.allocate(0)
        return tuple([a,b,*first,*self.cursors,*(v for ch in self.slots for v in flatten(ch)),len(self.trace),*self.trace])


def native_source(profile,bodies,items):
    defines={**FIELDS,'TRUE':1,'FALSE':0,'BOOL':'int','CHAR_TYPEPLAYER':1,'CHAR_TYPEPET':2,
        'CHAR_INITFUNC':0,'CHAR_FIRSTFUNCTION':0,'CHAR_LASTFUNCTION':2,'CHAR_DATAINTNUM':32,
        'CHAR_WORKDATAINTNUM':16,'CHAR_DATACHARNUM':2,'CHAR_WORKDATACHARNUM':2,
        'CHAR_MAXITEMHAVE':items,'CHAR_MAXPOOLITEMHAVE':30,'CHAR_MAXPETSKILLHAVE':7,
        'CHAR_MAXPETHAVE':5,'CHAR_MAXPOOLPETHAVE':3,'CHAR_SKILLMAXHAVE':3,
        'CHAR_TITLEMAXHAVE':3,'ADDRESSBOOK_MAX':2}
    h='#include <stdio.h>\n#include <string.h>\n#include <stdlib.h>\n'
    h+='\n'.join(f'#define {n} {v}' for n,v in defines.items())+r'''
#define arraysizeof(a) (sizeof(a)/sizeof((a)[0]))
typedef struct { unsigned char string[8]; } String;
typedef struct {int use,data[32],workint[16],flg[3];String string[2],workchar[2];
int indexOfExistItems[CHAR_MAXITEMHAVE],indexOfExistPoolItems[30];
union {int indexOfPet[5];int indexOfPetskill[7];} unionTable;
int indexOfPoolPet[3];struct {int use;} haveSkill[3];int indexOfHaveTitle[3];
unsigned char addressBook[2][4];String charfunctable[2];void *functable[2];
unsigned int CharMakeSequenceNumber;int opaque;} Char;
static Char CHAR_chara[7],tpl[2];static int CHAR_playernum=2,CHAR_petnum=2,CHAR_charanum=7;
typedef struct {int startcnt,endcnt,cnt;} INITCHARCOUNTER;
static INITCHARCOUNTER initCharCounter[3];static int trace[128],nt;
static void event(int a,int b){if(nt+2>128)abort();trace[nt++]=a;trace[nt++]=b;}
static int init_success(int i){event(20,i);trace[nt++]=CHAR_chara[i].use;trace[nt++]=CHAR_chara[i].workint[1];trace[nt++]=CHAR_chara[i].workint[3];trace[nt++]=CHAR_chara[i].CharMakeSequenceNumber;return 1;}
static int init_failure(int i){init_success(i);return 0;}
static int init_change(int i){init_success(i);CHAR_chara[i].workint[1]=777;CHAR_chara[i].workint[2]=666;CHAR_chara[i].workint[3]=9;return 1;}
void *getFunctionPointerFromName(const unsigned char *s){event(10,s[0]);return s[0]==1?(void*)init_success:s[0]==2?(void*)init_failure:s[0]==3?(void*)init_change:NULL;}
const unsigned char *CHAR_getCharfunctable(int i,int j){return CHAR_chara[i].charfunctable[j].string;}
int CHAR_CHECKINDEX(int i){return i>=0&&i<7&&CHAR_chara[i].use;}
#define fprint(...) event(90,mode)
typedef struct {int imagenumber;Char *initchardata;int imgtype;} Default;
static Default CHAR_defaultCharacterGet[2]={{111,&tpl[0],71},{222,&tpl[1],72}};
'''
    for name in ('CHAR_getDefaultChar','CHAR_constructFunctable','CHAR_initCharOneArray'):
        body=bodies[name]
        # Replace diagnostics only; Bismarck's cpp-expanded file/line logging
        # does not affect allocator state. All functional statements unchanged.
        if name=='CHAR_initCharOneArray' and profile=='bismarck':
            body=re.sub(r'fprintf\(stderr,[^;]+;', 'event(90,mode);',body)
        h+=body+'\n'
    h+=r'''
static void fill(Char *ch,int v){memset(ch,0,sizeof(*ch));ch->use=v;for(int j=0;j<32;j++)ch->data[j]=v;for(int j=0;j<16;j++)ch->workint[j]=v;
for(int j=0;j<3;j++){ch->flg[j]=v;ch->indexOfPoolPet[j]=v;ch->haveSkill[j].use=v;ch->indexOfHaveTitle[j]=v;}
memset(ch->string,v,sizeof(ch->string));memset(ch->workchar,v,sizeof(ch->workchar));memset(ch->charfunctable,v,sizeof(ch->charfunctable));memset(ch->addressBook,v,sizeof(ch->addressBook));
for(int j=0;j<CHAR_MAXITEMHAVE;j++)ch->indexOfExistItems[j]=v;for(int j=0;j<30;j++)ch->indexOfExistPoolItems[j]=v;for(int j=0;j<7;j++)ch->unionTable.indexOfPetskill[j]=v;
ch->functable[0]=ch->functable[1]=NULL;ch->CharMakeSequenceNumber=v;ch->opaque=v;}
static void snapshot(void){for(int j=0;j<3;j++)printf(" %d",initCharCounter[j].cnt);for(int i=0;i<7;i++){Char *ch=&CHAR_chara[i];printf(" %d",ch->use);
for(int j=0;j<32;j++)printf(" %d",ch->data[j]);for(int j=0;j<16;j++)printf(" %d",ch->workint[j]);for(int j=0;j<3;j++)printf(" %d",ch->flg[j]);
for(int j=0;j<16;j++)printf(" %d",((unsigned char*)ch->string)[j]);for(int j=0;j<16;j++)printf(" %d",((unsigned char*)ch->workchar)[j]);
for(int j=0;j<CHAR_MAXITEMHAVE;j++)printf(" %d",ch->indexOfExistItems[j]);for(int j=0;j<30;j++)printf(" %d",ch->indexOfExistPoolItems[j]);for(int j=0;j<7;j++)printf(" %d",ch->unionTable.indexOfPetskill[j]);
for(int j=0;j<3;j++)printf(" %d",ch->indexOfPoolPet[j]);for(int j=0;j<3;j++)printf(" %d",ch->haveSkill[j].use);for(int j=0;j<3;j++)printf(" %d",ch->indexOfHaveTitle[j]);
for(int j=0;j<8;j++)printf(" %d",((unsigned char*)ch->addressBook)[j]);for(int j=0;j<16;j++)printf(" %d",((unsigned char*)ch->charfunctable)[j]);
for(int j=0;j<2;j++)printf(" %d",ch->functable[j]==(void*)init_success?1:ch->functable[j]==(void*)init_failure?2:ch->functable[j]==(void*)init_change?3:0);
printf(" %u %d",ch->CharMakeSequenceNumber,ch->opaque);}}
int main(void){int kind,cursor,mask,cb,payload,use,release,lazy;
/* Original static sequence advances across this entire ordered stream. */
while(scanf("%d%d%d%d%d%d%d%d",&kind,&cursor,&mask,&cb,&payload,&use,&release,&lazy)==8){
nt=0;int mode=kind==1?0:kind==2?1:2,starts[]={0,2,4},ends[]={2,4,7};
for(int i=0;i<7;i++){fill(&CHAR_chara[i],61+i);CHAR_chara[i].use=1;CHAR_chara[i].workint[1]=999;CHAR_chara[i].workint[2]=900;CHAR_chara[i].workint[3]=88;}
for(int j=0;j<3;j++){initCharCounter[j].startcnt=starts[j];initCharCounter[j].endcnt=ends[j];initCharCounter[j].cnt=starts[j];}
initCharCounter[mode].cnt+=cursor;if(lazy)initCharCounter[0].startcnt=-1;for(int j=0;j<ends[mode]-starts[mode];j++)CHAR_chara[starts[mode]+j].use=(mask>>j)&1;
Char ch;for(int i=0;i<2;i++){fill(&tpl[i],100+100*i);for(int j=0;j<32;j++)tpl[i].data[j]=100+100*i+j;for(int j=0;j<3;j++)tpl[i].flg[j]=100+100*i+j;}
if(payload==2){fill(&ch,37);ch.workint[1]=901;ch.workint[2]=902;ch.workint[3]=903;memset(ch.charfunctable,0,sizeof(ch.charfunctable));}
else {fill(&ch,55);CHAR_getDefaultChar(&ch,payload?31010:111);}
ch.data[3]=kind;ch.use=use;ch.charfunctable[0].string[0]=cb;
int a=CHAR_initCharOneArray(&ch);printf("%d",a);snapshot();
if(a>=0&&release)CHAR_chara[a].use=0;ch.charfunctable[0].string[0]=0;
int b=CHAR_initCharOneArray(&ch);printf(" %d",b);snapshot();printf(" %d",nt);for(int j=0;j<nt;j++)printf(" %d",trace[j]);printf("\n");
}return 0;}
'''
    # Static sequence is part of the original function. Reset using a new
    # process per case would be slow. Instead oracle advances it across cases.
    return h


def expected_rows(profile,items,cases):
    rows=[];sequence=0
    for case in cases:
        o=Oracle(profile,items,case);o.seq=sequence
        row=o.run();sequence=o.seq
        # Native stream prints first snapshot before the second return.
        width=3+7*len(flatten(blank(items)))
        rows.append((row[0],*row[2:2+width],row[1],*row[2+width:]))
    return rows


def audit(profile,root):
    bodies,identity=source_domain(profile,root)
    if identity!=json.loads(PIN_PATH.read_text())['profiles'][profile]:
        raise ValueError('character reuse source domain drift')
    items=54 if profile=='bismarck' else 24
    cases=vectors();expected=expected_rows(profile,items,cases)
    source=native_source(profile,bodies,items)
    payload=''.join(' '.join(map(str,c))+'\n' for c in cases)
    for opt in ('-O0','-O2'):
        _assert_rows(run_native(source,payload,opt),expected,profile+' reuse')
    mutations=[(r'memcpy\s*\(\s*&CHAR_chara\[i\]\s*,\s*ch\s*,\s*sizeof\(\s*Char\s*\)\s*\);',';'),
               (r'if\s*\(\s*initfunc\(\s*i\s*\)\s*==\s*(?:FALSE|0)\s*\)','if (initfunc(i) == 99)'),
               (r'nc->workint\[j\]\s*=\s*0;', 'nc->workint[j] = 12;')]
    witness=[(3,0,6,2,0,1,1,0),(3,0,6,0,0,1,1,0)]
    rejected=0
    for pattern,replacement in mutations:
        changed,n=re.subn(pattern,replacement,source)
        if n!=1:raise ValueError('unapplied or ambiguous mutation')
        for opt in ('-O0','-O2'):
            actual=run_native(changed,''.join(' '.join(map(str,v))+'\n' for v in witness),opt)
            try:_assert_rows(actual,expected_rows(profile,items,witness),profile+' mutation')
            except ValueError:rejected+=1
            else:raise ValueError('semantic mutation escaped oracle')
    return {'profile':profile,'source_sha':PINNED[profile],'cases_per_optimization':len(cases),
            'native_comparisons':2*len(cases),'semantic_mutations_rejected':rejected,
            'semantic_sha256':hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest()}


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for p in PINNED:
        row=audit(p,getattr(args,p+'_dir'));total+=row['native_comparisons']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|character_reuse_comparisons={total}|profiles=3')
    print('FACT|default_getter_resets_ticket_start_and_object_work_fields_with_controlled_template_table')
    print('FACT|allocator_replaces_dead_slot_from_input_template_callback_failure_leaves_unused_copied_slot_cursor_unchanged')
    print('FACT|successful_allocator_advances_partition_cursor_constructs_functions_and_assigns_sequence')
    print('BOUNDARY|original_getter_allocator_constructor_positive_fixed_partitions_controlled_templates_callbacks_direct_release')
    print('OPEN|actual_default_table_enemy_creator_helpers_natural_ticket_object_Exit_reuse_composition_zero_size_partitions_original_ABI_build_JSS_Taiwan_v1_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
