"""Transient original bad-status body/tables composed with complete restoration callers."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_mdfyattack_source_audit import _definition
from tools.stoneage_becomepig_native_audit import _features, _assert_rows
from tools.stoneage_becomepig_preaudit import analyze_profile as source_audit
from tools import stoneage_becomepig_restore_audit as prior

PIN_PATH = Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BECOMEPIG-BADSTATUS-SOURCE-DOMAINS-R1.json'
FEATURES = ('_OTHER_MAGICSTAUTS','_MAGICSTAUTS_RESIST','_IMPRECATE_ITEM',
            '_PETSKILL_SETDUCK','_MAGICPET_SKILL','_BATTLE_PROPERTY',
            '_PROFESSION_SKILL','_PETSKILL_BECOMEPIG','_STRENGTH_PETSKILL',
            '_LOSTLOST_PETSKILL','_PETSKILL_NEW_PASSIVE')


def source_domain(name, root):
    base=root/LAYOUTS[name]
    includes=['-I',str(base/'include')]
    if name=='bismarck':includes+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    def pp(text):
        text=re.sub(r'^\s*#\s*include[^\n]*','',text,flags=re.M)
        return subprocess.run(['cpp','-P',*includes,'-'],
                              input='#include "version.h"\n'+text,
                              text=True,capture_output=True,check=True).stdout
    body=_definition(pp(_definition(_text(base/'battle/battle.c'),
                                   'BATTLE_BadStatusAllClr',raw_window=True)),
                     'BATTLE_BadStatusAllClr')
    event=pp(_text(base/'battle/battle_event.c'))
    tables={}
    for key in ('StatusTbl','MagicTbl'):
        matches=re.findall(r'\bint\s+'+key+r'\s*\[\s*\]\s*=\s*\{([^{}]*)\}\s*;',event,re.S)
        if len(matches)!=1:raise ValueError('ambiguous selected status table: '+key)
        fields=[s.strip() for s in matches[0].split(',') if s.strip()]
        if fields[0]!='-1' or not all(re.fullmatch(r'CHAR_[A-Z0-9_]+',s) for s in fields[1:]):
            raise ValueError('status table shape drift')
        tables[key]=fields
    header=pp(_text(base/'include/battle_event.h'))
    enum=re.search(r'\benum\s*\{\s*BATTLE_ST_NONE\b(.*?)\}',header,re.S)
    if not enum:raise ValueError('missing actual status enum')
    names=['BATTLE_ST_NONE']+[s.strip() for s in enum.group(1).strip(', \n').split(',')]
    if names[-1]!='BATTLE_ST_END' or not all(re.fullmatch(r'BATTLE_ST_[A-Z0-9_]+',s) for s in names):
        raise ValueError('status enum shape drift')
    limits=subprocess.run(['cpp','-dM',*includes,'-'],
        input='#include "version.h"\n'+re.sub(r'^\s*#\s*include[^\n]*','',_text(base/'include/battle_event.h'),flags=re.M),
        text=True,capture_output=True,check=True).stdout
    magic=int(re.search(r'^#define MAXSTATUSTYPE (\d+)$',limits,re.M).group(1))
    if len(names)-1!=len(tables['StatusTbl']) or magic!=len(tables['MagicTbl']):
        raise ValueError('actual table and original loop-limit mismatch')
    active=_features(name,root)
    identity={'source_sha':PINNED[name],
              'files':{p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in
                       ('battle/battle.c','battle/battle_event.c','include/battle_event.h','include/version.h')},
              'default_function_sha256':hashlib.sha256(_compact(body).encode()).hexdigest(),
              'selected_table_sha256':{k:hashlib.sha256(','.join(v).encode()).hexdigest() for k,v in tables.items()},
              'status_count':len(tables['StatusTbl']),'magic_count':magic,
              'features':{f:f in active for f in FEATURES}}
    return body,tables,identity


def clear_fields(tables, features):
    early=list(tables['StatusTbl'][1:])
    if features['_OTHER_MAGICSTAUTS']:
        for field in tables['MagicTbl'][1:]:early.extend((field,'CHAR_OTHERSTATUSNUMS'))
    if features['_IMPRECATE_ITEM']:early.extend('CHAR_WORKIMPRECATENUM'+str(i) for i in (1,2,3))
    if features['_PETSKILL_SETDUCK']:
        early.extend(('CHAR_MYSKILLDUCK','CHAR_MYSKILLDUCKPOWER'))
        if features['_MAGICPET_SKILL']:
            early.extend('CHAR_'+key for key in ('MYSKILLSTR','MYSKILLSTRPOWER','MYSKILLTGH','MYSKILLTGHPOWER','MYSKILLDEX','MYSKILLDEXPOWER','MAGICPETMP'))
    for feature,fields in (('_STRENGTH_PETSKILL',('CHAR_WORK_STRENGTH',)),
                           ('_LOSTLOST_PETSKILL',('CHAR_WORK_LOSTLOST',)),
                           ('_PETSKILL_NEW_PASSIVE',tuple('CHAR_WORKPASSIVE_'+s for s in ('DUCK','ACURATE','CRITICAL','COUNTER','MULTIPLE')))):
        if features[feature]:early.extend(fields)
    late=[]
    if features['_PROFESSION_SKILL']:
        late=['CHAR_MYSKILLHIT','CHAR_WORK_P_DUCK','CHAR_WORKMOD_P_DUCK','CHAR_WORK_WEAPON',
              'CHAR_WORK_F_RESIST','CHAR_WORK_I_RESIST','CHAR_WORK_T_RESIST']
    return early,late


def handles(functions,body,tables,features):
    early,late=clear_fields(tables,features)
    c=prior.constants(functions+[body,' '.join(early+late)+' CHAR_WORKOBLIVION'])
    c['CHAR_SKILLMAXHAVE']=26 if features['_PROFESSION_SKILL'] else 5
    # Arithmetic field families retain adjacency without selecting original ABI ordinals.
    for offset,keys in ((400,('CHAR_WORKIMPRECATENUM1','CHAR_WORKIMPRECATENUM2','CHAR_WORKIMPRECATENUM3')),
                        (410,('CHAR_WORK_F_RESIST','CHAR_WORK_I_RESIST','CHAR_WORK_T_RESIST'))):
        for i,key in enumerate(keys):c[key]=offset+i
    c['BATTLE_ST_END']=len(tables['StatusTbl']);c['MAXSTATUSTYPE']=len(tables['MagicTbl'])
    return c


class Witness(prior.Witness):
    def __init__(self,name,c,v,tables,features):
        super().__init__(name,c,v[:15])
        self.v=v;self.features=features;self.early,self.late=clear_fields(tables,features)
        self.petpig,self.pointermask,self.owned,self.seed=v[15:]
        self.properties=[ord('x'),ord('x')]
        self.ints[1]['CHAR_BECOMEPIG']=self.petpig
        for actor in (0,1):
            for key in set(self.early+self.late):self.works[actor][key]=self.seed
            # Oblivion's separate Exit ownership hook is excluded in this milestone.
            self.works[actor]['CHAR_WORKOBLIVION']=0

    def event(self,code,actor,value=0):
        super().event(code,actor,value)
        if code==25:self.clear(actor)

    def clear(self,actor):
        for key in self.early:
            self.works[actor][key]=0;super().event(35,actor,self.c[key])
        self.flags[actor]['CHAR_ISDIE']=0;super().event(37,actor,0)
        if self.features['_BATTLE_PROPERTY']:
            if not self.pointermask&(1<<actor):return
            self.properties[actor]=0;super().event(34,actor,0)
        for key in self.late:
            self.works[actor][key]=0;super().event(35,actor,self.c[key])
        if self.features['_PETSKILL_BECOMEPIG'] and self.ints[actor]['CHAR_WHICHTYPE']==1 and actor==0 and self.owned:
            self.ints[1]['CHAR_BECOMEPIG']=-1;super().event(36,1,-1)

    def execute(self):
        if self.v[0]>=2:
            self.event(25,self.v[0]-2);return 0
        action,validchar,validbattle,use,side,pos,*_=self.v
        if action==0:return self.compliance(0)
        if not validchar:return -101
        if not validbattle:return -102
        if self.i['CHAR_BASEIMAGENUMBER']==101749 or self.w['CHAR_WORKFOXROUND']!=-1:
            self.setint(0,'CHAR_BASEIMAGENUMBER',100000);self.w['CHAR_WORKFOXROUND']=-1
        if self.i['CHAR_BECOMEPIG']>-1:
            self.setint(0,'CHAR_BASEIMAGENUMBER',100388);self.compliance(0);self.event(20,0);self.event(21,0,self.c['CHAR_P_STRING_BASEBASEIMAGENUMBER'])
        self.event(28,0)
        if self.name=='bismarck':self.w['CHAR_WORKNOCAST']=0
        if not use:return -103
        if side>=0:
            self.entries[side][pos]=-1;self.escapes[side][pos]=0
            self.w['CHAR_WORKBATTLEMODE']=2;self.w['CHAR_WORKBATTLEINDEX']=-1
            lost=bool(self.f['CHAR_ISDIE'] or (self.name!='bismarck' and self.i['CHAR_HP']==1));self.event(27,0,10 if lost else 0)
            if lost:self.f['CHAR_ISDIE']=0;self.i['CHAR_HP']=1
            self.entries[side][pos+5]=-1;self.works[1]['CHAR_WORKBATTLEMODE']=0;self.works[1]['CHAR_WORKBATTLEINDEX']=-1
            self.event(25,0);self.compliance(0);self.event(24,0)
            if self.w['CHAR_WORKPETFALL']:
                self.w['CHAR_WORKPETFALL']=0;self.setint(0,'CHAR_RIDEPET',-2)
            status=0
            for key in ('HP','EXP','MP','DUELPOINT','CHARM','EARTH','WATER','FIRE','WIND','RIDEPET'):status|=self.c['CHAR_P_STRING_'+key]
            self.event(21,0,status)
            if self.i['CHAR_RIDEPET']==-2:self.setint(0,'CHAR_RIDEPET',-1)
            if self.owned:
                self.works[1]['CHAR_WORKBATTLEMODE']=0
                if self.ints[1]['CHAR_BASEIMAGENUMBER']!=100800:self.setint(1,'CHAR_BASEIMAGENUMBER',100800);self.event(23,0,ord('K'))
                self.event(25,1);self.compliance(1);self.event(22,0,0)
            self.event(29,0)
        self.event(26,0)
        return 0

    def row(self,ret):
        row=super().row(ret)
        extra=[]
        for actor in (0,1):
            extra.extend(self.works[actor].get(key,0) for key in sorted(set(self.early+self.late)))
            extra.append(self.properties[actor])
        return row[:72]+tuple(extra)+row[72:]


def vectors():
    for v in prior.vectors():
        for pointermask in (0,3):yield v+(180,pointermask,1,73)
    # Direct helper covers subject kind, ownership, counters, both pointer states,
    # and positive/negative/zero status seeds, independently of Exit eligibility.
    for action,kind,pig,petpig,mask,owned,seed in itertools.product((2,3),(1,2,3),(-1,180),(-2,-1,0,180),range(4),(0,1),(-7,0,73)):
        yield (action,1,1,1,-1,0,pig,100250,-1,0,0,kind,1,-1,0)+(petpig,mask,owned,seed)
    # Exit with no live ownership still has a valid battle-side pet. Half-valid
    # property pointers and unselected/unused/invalid battle paths are explicit.
    for mask,owned,petpig,seed,meta,ride,state in itertools.product(range(4),(0,1),(-2,-1,0,180),(-7,0,73),range(4),range(4),
                ((0,1,1,0,0),(1,0,1,0,0),(1,1,0,0,0),(1,1,1,-1,0),(1,1,1,0,0),(1,1,1,1,4))):
        if not owned and ride:continue  # An invalid rider remains outside this native domain.
        vc,vb,use,side,pos=state
        yield (1,vc,vb,use,side,pos,180,100250,100015,meta,ride,1,0,2,1)+(petpig,mask,owned,seed)


def native_source(name,functions,body,tables,features,c):
    source=prior.native_source(name,functions,c)
    source=source.replace('[2][160]','[2][512]').replace('trace[256]','trace[2048]').replace('nt+3>256','nt+3>2048')
    source=source.replace('static int checked(', 'static int clearing,petpig,pointermask,owned,seed;\nstatic int checked(')
    source=source.replace('ints[i][f]=v;if(f==CHAR_BASEIMAGENUMBER)',
                          'ints[i][f]=v;if(clearing&&f==CHAR_BECOMEPIG)event(36,i,v);if(f==CHAR_BASEIMAGENUMBER)')
    source=source.replace('works[checked(i)][f]=v;', 'i=checked(i);works[i][f]=v;if(clearing)event(35,i,f);')
    source=source.replace('flags[checked(i)][f]=v;', 'i=checked(i);flags[i][f]=v;if(clearing&&f==CHAR_ISDIE)event(37,i,v);')
    source=source.replace('return i==0&&slot==0?1:-1;', 'return owned&&i==0&&slot==0?1:-1;')
    helpers=r'''
typedef struct {struct {char string[16];} charfunctable[512];} Char;
static Char chars[2];
Char *CHAR_getCharPointer(int i){return pointermask&(1<<i)?&chars[i]:NULL;}
void strcpysafe(char *s,int n,const char *v){(void)n;(void)v;s[0]=0;}
void strncpysafe(char *s,int n,const char *v){strcpysafe(s,n,v);}
void CHAR_constructFunctable(int i){event(34,i,0);}
'''
    helpers+='\n'.join('static int '+key+'[]={'+','.join(fields)+'};' for key,fields in tables.items())+'\n'
    # Original function body stays unchanged: alias only its declaration/name,
    # then observe the call around it. Other caller bodies are untouched.
    helpers+='#define BATTLE_BadStatusAllClr original_badstatus\n'+body+'\n#undef BATTLE_BadStatusAllClr\n'
    helpers+='void BATTLE_BadStatusAllClr(int i){event(25,i,0);clearing=1;original_badstatus(i);clearing=0;}\n'
    source=source.replace('void BATTLE_BadStatusAllClr(int i){event(25,i,0);}',helpers)
    source=source.replace('&kind,&dead,&fox,&fall)==15)', '&kind,&dead,&fox,&fall,&petpig,&pointermask,&owned,&seed)==19)')
    source=source.replace('%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d"', '%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d"')
    fields=sorted(set(sum(clear_fields(tables,features),[])))
    init='clearing=0;memset(chars,0,sizeof(chars));for(int i=0;i<2;i++){chars[i].charfunctable[CHAR_BATTLEPROPERTY].string[0]=\'x\';'
    init+=''.join('works[i]['+key+']=seed;' for key in fields)
    init+='works[i][CHAR_WORKOBLIVION]=0;}ints[1][CHAR_BECOMEPIG]=petpig;\n'
    source=source.replace('ridePetTable[0].charNo=',init+'ridePetTable[0].charNo=')
    source=source.replace('int result=action?', 'int result;if(action>=2){BATTLE_BadStatusAllClr(action-2);result=0;}else result=action?')
    extra='for(int i=0;i<2;i++){'+''.join('printf(" %d",works[i]['+key+']);' for key in fields)+'printf(" %d",chars[i].charfunctable[CHAR_BATTLEPROPERTY].string[0]);}\n'
    source=source.replace(' printf(" %d",nt);',extra+' printf(" %d",nt);')
    return source


def audit(name,root):
    source_audit(name,root)
    body,tables,identity=source_domain(name,root)
    if identity!=json.loads(PIN_PATH.read_text())['profiles'][name]:raise ValueError('bad-status source/default-table identity drift')
    functions,caller_identity=prior.original_functions(name,root)
    pins=json.loads((PIN_PATH.parent/'STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json').read_text())['profiles'][name]
    if caller_identity!=pins['functions']:raise ValueError('complete caller identity drift')
    c=handles(functions,body,tables,identity['features']);vs=list(vectors())
    payload=''.join(' '.join(map(str,v))+'\n' for v in vs)
    expected=[]
    for v in vs:
        w=Witness(name,c,v,tables,identity['features']);expected.append(w.row(w.execute()))
    source=native_source(name,functions,body,tables,identity['features'],c)
    for opt in ('-O0','-O2'):_assert_rows(prior.run_native(source,payload,opt),expected,name+' complete original badstatus composition')
    return {'profile':name,'cases_per_optimization':len(vs),'direct_clear_cases':sum(v[0]>=2 for v in vs),
            'composed_cases':sum(v[0]<2 for v in vs),'optimizations':2,'identity':identity}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for name in PINNED:
        r=audit(name,getattr(args,name+'_dir').resolve());total+=r['cases_per_optimization']*2
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in r.items() if k!='identity'))
        print('SOURCE|profile='+name+'|domain_sha256='+hashlib.sha256(json.dumps(r['identity'],sort_keys=True,separators=(',',':')).encode()).hexdigest())
    print(f'TOTAL|original_badstatus_composition_comparisons={total}')
    print('BOUNDARY|complete_default_badstatus_body_actual_selected_status_magic_tables_complete_compliance_exit_callers_symbolic_ABI')
    print('BOUNDARY|controlled_property_storage_empty_copy_constructFunctable_stats_equipment_ride_network_hooks_valid_battle_side_pet_owned_slot0_or_none')
    print('OPEN|actual_equipment_ride_tables_equipment_category5_matching_row_UB_attack_order_timers_broader_ownership_and_runtime')
    print('RESOLUTION|BECOMEPIG_BOUNDED_ORIGINAL_BADSTATUS_COMPOSITION_PASS_ZERO_RUNTIME_PROMOTIONS')


if __name__=='__main__':main()
