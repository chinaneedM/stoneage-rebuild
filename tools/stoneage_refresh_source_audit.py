"""Pinned Refresh audit with transient original callback/executor/recovery.

Original source and OPTION bytes never enter emitted reports. The native
MultiList seam is an explicit resolved-list witness, not live target selection.
"""
import argparse
import os
from pathlib import Path
import random
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _sha, _text, _compact, _function
from tools.stoneage_mdfyattack_source_audit import _definition, _strip
from tools.stoneage_weaken_source_audit import _array, _preprocess, _enum_values
from tools.stoneage_refresh_model import (
    CALLBACK_NAME, COMMAND_NAME, FEATURE_NAME, PROFILE_FACTS, BUILD_CHARSETS,
    RefreshSourceDomain, _BASELINE, parse_refresh_option,
    resolve_refresh_setup, resolve_refresh_recovery,
)


def _native(source, enums, packed_macro, profile, *, recovered_options=()):
    prefix = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BOOL int
#define TRUE 1
#define FALSE 0
#define MAGIC_EFFECT_USER 9
#define SPR_hoshi 10
#define SPR_tyusya 11
static int works[3][4096], effect, bad_events, nc_events;
static char *option;
/* This accessor seam retains the audited source's invalid-work -1 return. */
int CHAR_getWorkInt(int index,int pos){
 if(pos<CHAR_WORKBATTLEMODE||pos>=CHAR_WORKDATAINTNUM)return -1;
 return works[index][pos];
}
void CHAR_setWorkInt(int index,int pos,int value){works[index][pos]=value;}
char *PETSKILL_getChar(int array,int field){return option;}
int BATTLE_No2Index(int battle,int slot){return slot;}
void BATTLE_MultiList(int battle,int target,int *list){list[0]=1;list[1]=2;list[2]=-1;}
void BATTLE_MagicEffect(int battle,int actor,int *list,int use,int receive){effect=receive;}
void BATTLE_BadStatusString(int slot,int status){if(status!=0)abort();bad_events++;}
int getfdFromCharaIndex(int index){return index;}
int getfdFromchar_index(int index){return index;}
void lssproto_NC_send(int fd,int value){if(value!=0)abort();nc_events++;}
void GmsvServer_NC_send(int fd,int value){if(value!=0)abort();nc_events++;}
'''
    prefix = '\n'.join('#define '+key+' '+str(value) for key,value in enums.items())+'\n'+prefix
    main = r'''
int main(void){
 char hex[2048],bytes[1024];int before,array,value;
 while(scanf("%2047s%d%d",hex,&before,&array)==3){
  memset(works,0,sizeof(works));effect=bad_events=nc_events=0;
  for(int who=0;who<3;who++)for(int j=1;j<BATTLE_ST_END;j++){
   if(scanf("%d",&value)!=1)abort();works[who][StatusTbl[j]]=value;
  }
  if(strcmp(hex,"NULL")==0)option=NULL;
  else{size_t n=strlen(hex)/2;if(strcmp(hex,"EMPTY")==0)n=0;
   for(size_t i=0;i<n;i++){unsigned v;sscanf(hex+2*i,"%2x",&v);bytes[i]=(char)v;}
   bytes[n]=0;option=bytes;
  }
  works[0][CHAR_WORKBATTLECOM3]=before;
  int ok=PETSKILL_Refresh(0,1,array,NULL);
  int ret=BATTLE_S_Refresh(0,0,1,array);
  printf("%d %d %d %d %d %d %d %d %d",ok,works[0][CHAR_WORKBATTLECOM1],
   works[0][CHAR_WORKBATTLECOM2],works[0][CHAR_WORKBATTLEMODE],
   works[0][CHAR_WORKBATTLECOM3],ret,effect,bad_events,nc_events);
  for(int who=1;who<3;who++)for(int j=1;j<BATTLE_ST_END;j++)printf(" %d",works[who][StatusTbl[j]]);
  printf("\n");
 }
 return 0;
}
'''
    end = enums['BATTLE_ST_END']
    zero = (0,)*end
    rng = random.Random(575)
    vectors = [(zero,zero,zero)]
    for status in range(1,end):
        one = list(zero); one[status] = 3
        multi = list(one); multi[1] = 4
        silence = list(zero); silence[10] = 2
        vectors += [(zero,tuple(one),tuple(multi)),(tuple(one),tuple(silence),zero)]
    for _ in range(32):
        vectors.append(tuple((0,)+tuple(rng.choice((-1,0,0,0,2,4)) for _ in range(1,end)) for _ in range(3)))
    rows = []
    for charset in BUILD_CHARSETS[profile]:
        options = [b'',*tuple(x.encode(charset) for x in _BASELINE[profile])]
        if charset == 'utf-8':options += ['眼'.encode()]
        if profile == 'bismarck':options += [b'plain', b'x'+ '沉默'.encode(charset)]
        cases = [(raw,v) for raw in options for v in vectors]
        actual_defined = []; unsafe = []
        for raw in recovered_options:
            try:
                status=parse_refresh_option(raw,profile=profile,execution_charset=charset)
            except RefreshSourceDomain:
                unsafe.append(raw)
            else:
                key=status if status else end-1
                selection=[vectors[0],*vectors[1+2*(key-1):3+2*(key-1)],
                           *vectors[19:21],*vectors[-4:]]
                actual_defined += [(raw,v) for v in selection]
        cases += actual_defined
        inputs = []; expected = []
        for n,(raw,(actor,target1,target2)) in enumerate(cases):
            before = (0x1234abcd,-65535,0)[n%3]; array = (23,65536,-1)[n%3]
            setup = resolve_refresh_setup(target_slot=1,skill_array=array,packed_com3_before=before)
            status = parse_refresh_option(raw,profile=profile,execution_charset=charset)
            out = resolve_refresh_recovery(status,profile=profile,actor_counters=actor,target_counters=(target1,target2))
            inputs.append(' '.join(map(str,(raw.hex() or 'EMPTY',before,array,*actor[1:],*target1[1:],*target2[1:]))))
            effect = 0 if out.receive_effect_name is None else 11 if out.source_return_value else 10
            values = (1,enums[COMMAND_NAME],1,enums['BATTLE_CHARMODE_C_OK'],setup.packed_com3,
                      int(out.source_return_value),effect,sum(x is not None for x in out.cleared_statuses),
                      len(out.silence_clear_targets),*out.target_counters[0][1:],*out.target_counters[1][1:])
            expected.append(' '.join(map(str,values)))
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory); src=p/'oracle.c';exe=p/'oracle'
            src.write_text(prefix+'\n'+packed_macro+'\n'+source+'\n'+main)
            result=subprocess.run(['cc','-std=c11','-w','-fexec-charset='+charset,
                '-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-pie','-no-pie',
                str(src),'-o',str(exe)],capture_output=True,text=True)
            if result.returncode:raise ValueError('native compilation failed: '+result.stderr[-2000:])
            env=dict(os.environ,ASAN_OPTIONS='detect_leaks=0')
            run=subprocess.run([str(exe)],input='\n'.join(inputs)+'\n',capture_output=True,text=True,env=env)
            if run.returncode:raise ValueError(f'{profile}/{charset} native failed: '+run.stderr[-2000:])
            if run.stdout.splitlines()!=expected:
                observed=run.stdout.splitlines()
                first=next((n for n,(a,b) in enumerate(zip(observed,expected)) if a!=b),min(len(observed),len(expected)))
                raise ValueError(f'{profile}/{charset} native mismatch at {first}: {observed[first:first+1]} vs {expected[first:first+1]}')
            # Preserve genuine source diagnostics without pretending these
            # unsafe recovered build interpretations are runnable mechanics.
            for raw in (None,*unsafe,*( (b'x',) if profile!='bismarck' else ())):
                line=' '.join(map(str,('NULL' if raw is None else raw.hex(),0,23,*zero[1:],*zero[1:],*zero[1:])))+'\n'
                bad=subprocess.run([str(exe)],input=line,capture_output=True,text=True,env=env)
                if bad.returncode==0 or not any(x in bad.stderr for x in ('null pointer','out of bounds','global-buffer-overflow')):
                    raise ValueError(f'{profile}/{charset} expected source scan diagnostic absent')
        rows.append({'execution_charset':charset,'defined_cases':len(cases),
                     'recovered_defined_cases':len(actual_defined),'recovered_unsafe_options':len(unsafe),
                     'expected_null_diagnostics':1,'expected_short_table_diagnostics':len(unsafe)+int(profile!='bismarck'),
                     'sanitizers_pass':True})
    return rows


def analyze_profile(profile, root, *, recovered_options=()):
    root=Path(root).resolve()
    head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if head!=PINNED[profile] or subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip():
        raise ValueError('clean pinned source identity drift')
    base=root/LAYOUTS[profile]; includes=['-I',str(base/'include')]
    if profile=='bismarck':includes+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    paths={key:base/value for key,value in {
        'pet':'battle/pet_skill.c','event':'battle/battle_event.c','magic':'battle/battle_magic.c',
        'battle':'battle/battle.c','getter':'char/char_base.c','bh':'include/battle.h',
        'char':'include/char_base.h','ph':'include/pet_skillinfo.h','version':'include/version.h',
    }.items()}
    data={key:_text(path) for key,path in paths.items()}
    macros=subprocess.check_output(['cpp','-dM',*includes,str(paths['version'])],text=True)
    active=set(re.findall(r'^#define\s+(\w+)',macros,re.M))
    functions=[_definition(data['pet'],CALLBACK_NAME),_definition(data['event'],'BATTLE_S_Refresh'),
               _function(data['magic'],'void BATTLE_MultiStatusRecovery')]
    source=_preprocess('\n'.join([_array(data['event'],key) for key in ('aszStatus','StatusTbl')]+functions),includes,paths['version'])
    names=set(re.findall(r'\b(?:CHAR_[A-Z_0-9]+|BATTLE_ST_END|BATTLE_COM_S_REFRESH|BATTLE_CHARMODE_C_OK|PETSKILL_OPTION)\b',source))
    names.discard('CHAR_SETWORKINT_LOW')
    names.update(('CHAR_WORKDATAINTNUM','CHAR_WORKCONFUSION','PETSKILL_REFRESH','SIDE_OFFSET'))
    enums=_enum_values(sorted(names),includes)
    labels=len(re.findall(r'"[^"]*"',_array(source,'aszStatus')))
    work_count=1+len(re.findall(r'CHAR_WORK[A-Z_0-9]+',_array(source,'StatusTbl')))
    callback=_compact(_strip(functions[0])).replace('char_index','charaindex')
    executor=_compact(_strip(functions[1])).replace('char_index','charaindex')
    recovery=_compact(_strip(functions[2]))
    dispatch=_compact(_strip(data['battle'])).replace('char_index','charaindex')
    dispatch=dispatch[dispatch.index('case'+COMMAND_NAME+':'):].split('break;',1)[0]
    getter=_compact(_strip(data['getter']))
    gates={
        'skill_and_silence_features_active':FEATURE_NAME in active and '_MAGIC_NOCAST' in active,
        'callback_command_target_mode_low':all(x in callback for x in (COMMAND_NAME,'CHAR_WORKBATTLECOM2,toindex','BATTLE_CHARMODE_C_OK','CHAR_SETWORKINT_LOW')),
        'callback_ignores_option_and_actor_kind':'PETSKILL_getChar' not in callback and 'CHAR_getInt' not in callback,
        'dispatch_direct_target_and_low_array':all(x in dispatch for x in ('CHAR_WORKBATTLECOM2','CHAR_GETWORKINT_LOW','BATTLE_S_Refresh')) and 'BATTLE_TargetAdjust' not in dispatch,
        'scan_two_bytes_over_status_end':'strncmp(pszP,aszStatus[i],2)' in executor and 'i<BATTLE_ST_END' in executor,
        'actor_counter_controls_return_effect':all(x in executor for x in ('CHAR_getWorkInt(charaindex,StatusTbl[status])>0','iRet=TRUE','SPR_tyusya','SPR_hoshi','returniRet')),
        'invalid_work_getter_returns_minus_one':bool(re.search(r'if\(CHAR_WORKBATTLEMODE>element\|\|element>=CHAR_WORKDATAINTNUM\)\{[^{}]*return-1;',getter)),
        'recovery_keeps_highest_positive_status':all(x in recovery for x in ('j=1;j<BATTLE_ST_END;j++','CHAR_getWorkInt(toindex,StatusTbl[j])>0','tostatus=j')),
        'wildcard_uses_work_enum_bound':'status==0&&tostatus!=0&&tostatus<=CHAR_WORKCONFUSION' in recovery,
        'specific_requires_highest_status':'status==tostatus' in recovery,
        'clear_only_one_and_notify_silence':all(x in recovery for x in ('CHAR_setWorkInt(toindex,StatusTbl[tostatus],0)','StatusTbl[tostatus]==CHAR_WORKNOCAST','BATTLE_BadStatusString(ToList[i],0)')),
        'effect_before_target_recovery':recovery.index('BATTLE_MagicEffect(')<recovery.index('for(i=0;'),
        'no_executor_recovery_random_draw':all('RAND(' not in x and 'rand(' not in x for x in (executor,recovery)),
        'complete_status_work_table':work_count==enums['BATTLE_ST_END'],
        'profile_facts_match':(enums['BATTLE_ST_END'],labels,enums['CHAR_WORKCONFUSION'])==PROFILE_FACTS[profile],
        'wildcard_bound_admits_all_active_indices':enums['BATTLE_ST_END']-1<=enums['CHAR_WORKCONFUSION'],
    }
    if not all(gates.values()):raise ValueError(f'{profile} source gates failed: '+repr({k:v for k,v in gates.items() if not v}))
    packed=re.search(r'^\s*#define\s+CHAR_SETWORKINT_LOW(?:[^\n]*\\\n)*[^\n]*',data['bh'],re.M)
    if not packed:raise ValueError('actual LOW macro absent')
    return {'profile':profile,'commit':head,'enums':enums,'label_count':labels,
            'status_work_count':work_count,'attack_magic_active':'__ATTACK_MAGIC' in active,
            'gates':gates,'hashes':{str(path.relative_to(root)):_sha(path) for path in paths.values()},
            'native':_native(source,enums,packed.group(),profile,recovered_options=recovered_options)}


def emit(results):
    print('StoneAge pinned descendant Refresh source audit — R1')
    print('Derived facts only. Resolved MultiList witness; target selection and ordered runtime OPEN.')
    print('Build charsets are conditional; original recovered binary build is OPEN.')
    for row in results:
        print(f"PROFILE|name={row['profile']}|sha={row['commit']}|labels={row['label_count']}|work_table={row['status_work_count']}|attack_magic_active={int(row['attack_magic_active'])}")
        for key in ('BATTLE_COM_S_REFRESH','PETSKILL_REFRESH','BATTLE_ST_END','CHAR_WORKCONFUSION','CHAR_WORKNOCAST'):
            print(f"ENUM|profile={row['profile']}|name={key}|value={row['enums'][key]}")
        for key,value in row['gates'].items():
            print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for native in row['native']:
            print('NATIVE|profile='+row['profile']+'|'+'|'.join(f'{k}={int(v) if isinstance(v,bool) else v}' for k,v in native.items()))
        for path,digest in row['hashes'].items():
            print(f"SOURCE_HASH|profile={row['profile']}|path={path}|sha256={digest}")
    print('RESOLUTION|REFRESH_FIXED_SOURCE_CLOSED_BOUNDED_CONDITIONAL_REFERENCE')


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args()
    emit([analyze_profile(name,getattr(args,name+'_dir')) for name in PINNED])


if __name__=='__main__':main()
