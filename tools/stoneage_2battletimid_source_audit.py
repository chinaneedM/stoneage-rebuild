"""Pinned 2BattleTimid source audit and conditional native byte witnesses."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_guard_break2_source_audit import PINNED,LAYOUTS,_text,_sha,_compact
from tools.stoneage_mdfyattack_source_audit import _definition,_strip
from tools.stoneage_battletimid_source_audit import _case_block
from tools.stoneage_weaken_source_audit import _enum_values
from tools.stoneage_2battletimid_reference_model import (
    CALLBACK_NAME,COMMAND_NAME,FEATURE_NAME,PROFILE_UTF8,PROFILE_BIG5,
    resolve_2battletimid_setup,resolve_2battletimid_post_damage,parse_2battletimid_chance,
)


def native_oracle(data,actual_options=()):
    prefix=r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TRUE 1
#define FALSE 0
#define CHAR_TYPEPLAYER 0
#define CHAR_TYPEPET 1
#define CHAR_WHICHTYPE 0
#define CHAR_DEFAULTPET 1
#define CHAR_BASEIMAGENUMBER 2
#define CHAR_BASEBASEIMAGENUMBER 3
#define CHAR_WORKBATTLECOM1 0
#define CHAR_WORKBATTLECOM2 1
#define CHAR_WORKBATTLEMODE 2
#define CHAR_WORKBATTLECOM3 3
#define CHAR_WORKATTACKPOWER 4
#define CHAR_WORKDEFENCEPOWER 5
#define CHAR_WORKQUICK 6
#define CHAR_WORKFIXSTR 7
#define CHAR_WORKFIXTOUGH 8
#define CHAR_WORKFIXDEX 9
#define CHAR_WORKBATTLEFLG 10
#define CHAR_WORKPLAYERINDEX 11
#define CHAR_WORKFOXROUND 12
#define CHAR_BATTLEFLG_NORETURN 1
#define BATTLE_COM_S_2TIMID 77
#define BATTLE_CHARMODE_C_OK 3
#define PETSKILL_OPTION 0
#define _FIXWOLF
#define _PETSKILL_BECOMEFOX
static int works[3][13],valid_actor,pet_type,default_pet,draw_value,draws;
static int exits,notifications,bs,be,bh,ks_value,status_value,owner_slot;
static char option_buffer[8192],*option;
#define CHAR_CHECKINDEX(i) (valid_actor)
int CHAR_getWorkInt(int i,int k){return works[i][k];}
void CHAR_setWorkInt(int i,int k,int v){works[i][k]=v;}
int CHAR_getInt(int i,int k){
 if(k==CHAR_WHICHTYPE)return i==2?pet_type:CHAR_TYPEPLAYER;
 if(k==CHAR_DEFAULTPET)return default_pet;
 if(k==CHAR_WORKFOXROUND)return -1;
 return 123;
}
void CHAR_setInt(int i,int k,int v){if(k==CHAR_DEFAULTPET)default_pet=v;}
char *PETSKILL_getChar(int i,int k){return option;}
int BATTLE_No2Index(int b,int slot){owner_slot=slot;return 1;}
int CHAR_getCharPet(int i,int slot){return 2;}
void BATTLE_PetDefaultExit(int owner,int battle){exits++;}
void CHAR_sendStatusString(int owner,char *s){notifications++;sscanf(s,"K%d",&status_value);}
int getfdFromCharaIndex(int i){return 3;}
int getfdFromchar_index(int i){return 3;}
void lssproto_KS_send(int fd,int slot,int flag){notifications++;ks_value=slot;}
void GmsvServer_KS_send(int fd,int slot,int flag){lssproto_KS_send(fd,slot,flag);}
void record_frame(char *s){if(!strncmp(s,"BS|",3))bs++;if(!strncmp(s,"BE|",3))be++;if(!strncmp(s,"BH|",3))bh++;}
#define BATTLESTR_ADD(s) record_frame(s)
int oracle_rand(void){draws++;return draw_value;}
#define rand oracle_rand
'''
    macro=re.search(r'^\s*#define\s+CHAR_SETWORKINT_LOW(?:[^\n]*\\\n)*[^\n]*',data['battle_h'],re.M)
    if not macro:raise ValueError('packed-work macro missing')
    callback=_definition(data['pet'],CALLBACK_NAME)
    recall=_definition(data['event'],'BATTLE_PetIn')
    at=data['event'].find('case '+COMMAND_NAME+':')
    event_case=_case_block(data['event'][at:],'case '+COMMAND_NAME+':')
    effect='\nvoid effect(int damage,int defNo){int battleindex=0,attackNo=10,defindex=2,skill=0,flg=0,petdamage=0;char *pszP=NULL;char szCommand[1024];switch(77){'+event_case+'}}\n'
    main=r'''
int main(int argc,char **argv){
 if(argc!=3)return 2;
 size_t n=strlen(argv[1]);if(n%2||n/2>=sizeof(option_buffer))return 3;
 for(size_t i=0;i<n/2;i++){unsigned int v;sscanf(argv[1]+i*2,"%2x",&v);option_buffer[i]=(char)v;}
 option_buffer[n/2]=0;option=option_buffer;
 int mode=atoi(argv[2]);
 if(mode==0){int target,array,packed,a,d,q,wa,wd,wq;
  while(scanf("%d%d%d%d%d%d%d%d%d%d",&valid_actor,&target,&array,&packed,&a,&d,&q,&wa,&wd,&wq)==10){
   memset(works,0,sizeof(works));works[0][3]=packed;works[0][4]=wa;works[0][5]=wd;works[0][6]=wq;
   works[0][7]=a;works[0][8]=d;works[0][9]=q;draws=0;
   int ok=PETSKILL_2BattleTimid(0,target,array,NULL);
   printf("%d %d %d %d %d %d %d %d %d\n",ok,works[0][0],works[0][1],works[0][2],works[0][3],works[0][4],works[0][5],works[0][6],draws);
  }
 }else{int damage,blocked,react,slot,before;
  while(scanf("%d%d%d%d%d%d%d",&draw_value,&damage,&pet_type,&blocked,&react,&slot,&before)==7){
   memset(works,0,sizeof(works));works[2][10]=blocked;works[2][11]=1;works[2][12]=-1;
   default_pet=before;draws=exits=notifications=bs=be=bh=0;ks_value=status_value=owner_slot=-100;
   if(damage>0&&!react)effect(damage,slot);
   printf("%d %d %d %d %d %d %d %d %d %d\n",draws,exits,default_pet,notifications,bs,be,bh,ks_value,status_value,owner_slot);
  }
 }
 return 0;
}
'''
    options=[b'',b'ASCII',*[text.encode(codec) for codec in ('big5','utf-8') for text in (
        '-攻%70|-防%40|-敏%80|命%15','-攻%70|+攻%20|命%100',
        '-攻%70|-防%bad|-敏%bad|命%bad','+防%20|+敏%30|命%-1')]]
    options.extend(raw for raw in actual_options if raw not in options)
    counts=[]
    with tempfile.TemporaryDirectory(prefix='sa2timid-native-') as directory:
        source=Path(directory)/'oracle.c';source.write_text(prefix+'\n'+macro.group(0)+'\n'+callback+'\n'+recall+effect+main,encoding='utf-8')
        for profile,encoding in ((PROFILE_UTF8,'UTF-8'),(PROFILE_BIG5,'BIG5')):
            exe=Path(directory)/profile
            result=subprocess.run(['cc','-std=c99','-O0','-finput-charset=UTF-8','-fexec-charset='+encoding,str(source),'-o',str(exe)],text=True,capture_output=True)
            if result.returncode:raise ValueError('native harness compile failure: '+result.stderr)
            setup_count=post_count=0
            for raw in options:
                setup_vectors=[];setup_expected=[]
                for valid in (0,1):
                    for fixed in ((101,99,77),(300,200,100),(0,0,0),(16777217,100,100)):
                        vector=(valid,5,23,0x12340000,*fixed,900,800,700)
                        r=resolve_2battletimid_setup(raw,profile=profile,target_slot=5,skill_array=23,
                            packed_com3_before=0x12340000,fixed_powers=fixed,powers_before=(900,800,700),valid_actor=bool(valid))
                        setup_vectors.append(vector);setup_expected.append((int(r.accepted),77 if valid else 0,5 if valid else 0,
                            3 if valid else 0,r.packed_com3,*r.powers,0))
                payload=''.join(' '.join(map(str,v))+'\n' for v in setup_vectors)
                actual=[tuple(map(int,line.split())) for line in subprocess.check_output([str(exe),raw.hex(),'0'],input=payload,text=True).splitlines()]
                if actual!=setup_expected:raise ValueError(f'{profile} native callback mismatch')
                setup_count+=len(actual)
                vectors=[];expected=[]
                for draw in range(100):
                    for damage in (1,2):
                        for pet in (0,1):
                            for blocked in (0,1):vectors.append((draw,damage,pet,blocked,0,5,2))
                vectors.extend((0,damage,1,0,react,slot,2) for damage,react in ((0,0),(2,1),(2,0)) for slot in (5,15))
                for draw,damage,pet,blocked,react,slot,before in vectors:
                    r=resolve_2battletimid_post_damage(raw,profile=profile,damage=damage,
                        draw=None if react or damage==0 else draw,target_is_pet=bool(pet),
                        pet_noreturn=bool(blocked),active_original_reaction=bool(react),source_target_slot=slot,default_pet_slot=before)
                    expected.append((r.rng_draws,int(r.pet_withdrawn),r.owner_default_pet_after,r.status_notifications,
                        r.bs_frames,0,int(damage>0 and not react),r.owner_default_pet_after if r.pet_recall_requested else -100,
                        before if r.pet_recall_requested else -100,r.owner_slot if r.pet_recall_requested else -100))
                payload=''.join(' '.join(map(str,v))+'\n' for v in vectors)
                actual=[tuple(map(int,line.split())) for line in subprocess.check_output([str(exe),raw.hex(),'1'],input=payload,text=True).splitlines()]
                if actual!=expected:
                    index=next(i for i,pair in enumerate(zip(actual,expected)) if pair[0]!=pair[1])
                    raise ValueError(f'{profile} native post/recall mismatch at {vectors[index]}: {actual[index]} != {expected[index]}')
                post_count+=len(actual)
            counts.append((profile,setup_count,post_count,len(actual_options)))
    return counts


def analyze_profile(name,root,actual_options=()):
    root=Path(root).resolve()
    sha=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    dirty=subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True).strip()
    if sha!=PINNED[name] or dirty:raise ValueError('pinned source commit/tree drift')
    base=root/LAYOUTS[name]
    paths={'pet':base/'battle/pet_skill.c','battle':base/'battle/battle.c','event':base/'battle/battle_event.c',
           'battle_h':base/'include/battle.h','version':base/'include/version.h','petskill_h':base/'include/pet_skillinfo.h',
           'target_h':base/'include/pet_skill.h'}
    data={key:_text(path) for key,path in paths.items()}
    includes=['-I',str(base/'include')]
    if name=='bismarck':includes+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    macros=subprocess.check_output(['cpp','-dM',*includes,str(paths['version'])],text=True)
    active=set(re.findall(r'^#define\s+(\w+)',macros,re.M))
    enums=_enum_values([COMMAND_NAME,'BATTLE_CHARMODE_C_OK','PETSKILL_TARGET_WITHOUTMYSELFANDPET'],includes)
    callback=_compact(_strip(_definition(data['pet'],CALLBACK_NAME))).replace('char_index','charaindex')
    damage=_compact(_strip(_definition(data['event'],'BATTLE_S_AttackDamage'))).replace('char_index','charaindex')
    event_case=_compact(_strip(_case_block(data['event'][data['event'].find('case '+COMMAND_NAME+':'):],'case '+COMMAND_NAME+':')))
    recall=_compact(_strip(_definition(data['event'],'BATTLE_PetIn'))).replace('char_index','charaindex')
    start=data['battle'].find('case '+COMMAND_NAME+':');dispatch=_compact(data['battle'][start:].split('#endif',1)[0])
    target=_compact(_strip(_definition(data['battle'],'BATTLE_TargetListSet')))
    guards={
        'target7_symbol_verified':enums['PETSKILL_TARGET_WITHOUTMYSELFANDPET']==7,
        'feature_active':FEATURE_NAME in active,
        'callback_registered':bool(re.search(r'"'+CALLBACK_NAME+r'"\s*,\s*'+CALLBACK_NAME,data['pet'])),
        'callback_actor_check_without_player_rejection':'CHAR_CHECKINDEX' in callback and 'CHAR_TYPEPLAYER' not in callback,
        'callback_command_target_mode_before_option':callback.find('CHAR_WORKBATTLEMODE')<callback.find('PETSKILL_getChar'),
        'callback_six_ordered_independent_power_markers':all(x in callback for x in ('-攻%','+攻%','-防%','+防%','-敏%','+敏%')) and callback.count('sscanf(pszP+4')==6,
        'callback_packed_skill_after_option':'CHAR_SETWORKINT_LOW' in callback and 'rand(' not in callback and 'RAND(' not in callback,
        'dispatch_targetadjust_before_attackdamage':dispatch.find('BATTLE_TargetAdjust(')>=0 and dispatch.find('BATTLE_TargetAdjust(')<dispatch.find('BATTLE_S_AttackDamage('),
        'dispatch_symbolic_type_and_low_skill':COMMAND_NAME in dispatch and 'CHAR_GETWORKINT_LOW' in dispatch,
        'reaction_demotes_before_attackseq':'skill_type=-1' in damage and damage.find('skill_type=-1')<damage.find('BATTLE_AttackSeq('),
        'zero_damage_demotes_before_post_switch':'if(damage<=0)' in damage and damage.find('if(damage<=0)')<damage.find('case'+COMMAND_NAME+':'),
        'post_chance_marker_fixed_byte_offset':'sscanf(timidc+3,"%d",&timid)' in event_case,
        'post_rand_left_operand_before_damage_and_pet_gate':'if(rand()%100<timid&&damage>1)' in event_case and event_case.find('rand()%100')<event_case.find('CHAR_TYPEPET'),
        'post_only_pet_recall_not_player_exit':'BATTLE_PetIn(battleindex,defNo-5)' in event_case and 'BATTLE_Exit(' not in event_case and 'CHAR_DischargeParty' not in event_case,
        'post_old_exit_code_commented_out':'BATTLE_NoAction' not in event_case and 'BATTLE_PetDefaultExit' not in event_case,
        'post_status_before_recall_ks_after':event_case.find('CHAR_sendStatusString')<event_case.find('BATTLE_PetIn')<event_case.find('KS_send'),
        'recall_noreturn_guard_before_default_exit':recall.find('CHAR_BATTLEFLG_NORETURN')<recall.find('BATTLE_PetDefaultExit'),
        'recall_clears_default_and_bs_frame':'CHAR_DEFAULTPET,-1' in recall and 'BS|s%X|f0|' in recall,
        '2timid_not_in_legacy_same_side_list':COMMAND_NAME not in target,
    }
    if not all(guards.values()):raise ValueError(f'{name} source gates failed: {[k for k,v in guards.items() if not v]}')
    return {'profile':name,'sha':sha,'enums':enums,'gates':guards,'hashes':{k:_sha(v) for k,v in paths.items()},
            'native':native_oracle(data,actual_options),'wolf_active':'_FIXWOLF' in active,'fox_active':'_PETSKILL_BECOMEFOX' in active}


def emit(rows,actual_options=()):
    print('StoneAge 2BattleTimid pinned source/native conditional reference — R1')
    print('Derived facts only; original source and actual OPTION remain transient.')
    for row in rows:
        print(f"PROFILE|name={row['profile']}|sha={row['sha']}|command_value={row['enums'][COMMAND_NAME]}|mode_value={row['enums']['BATTLE_CHARMODE_C_OK']}|wolf_active={int(row['wolf_active'])}|fox_active={int(row['fox_active'])}")
        for key,value in row['gates'].items():print(f"GATE|profile={row['profile']}|name={key}|pass={int(value)}")
        for key,value in row['hashes'].items():print(f"SOURCE_SHA256|profile={row['profile']}|file={key}|sha256={value}")
        for encoding,setup,post,actual in row['native']:
            print(f"NATIVE|profile={row['profile']}|charset={encoding}|callback_cases={setup}|post_recall_cases={post}|actual_data_options={actual}")
    for index,raw in enumerate(actual_options):
        for profile in (PROFILE_UTF8,PROFILE_BIG5):
            r=resolve_2battletimid_setup(raw,profile=profile,target_slot=5,skill_array=23,packed_com3_before=0,
                fixed_powers=(1000,1000,1000),powers_before=(900,800,700))
            print(f'ACTUAL_OPTION_SEMANTICS|index={index}|charset={profile}|attack_at_fixed1000={r.powers[0]}|defence_at_fixed1000={r.powers[1]}|quick_at_fixed1000={r.powers[2]}|chance={parse_2battletimid_chance(raw,profile=profile)}')
    print('FACT|secondary_pet_recall_only_no_player_exit_or_party_discharge')
    print('FACT|post_draw_owned_only_after_positive_damage_and_no_reaction_demotion')
    print('FACT|recall_noreturn_blocks_default_exit_but_not_outer_status_and_ks')
    print('BOUNDARY|literal_encoding_utf8_and_big5_are_explicit_conditional_profiles_no_original_build_selected')
    print('BOUNDARY|normal_nontransformed_pet_with_owner_aligned_slot_only_wolf_fox_compositions_open')
    print('BOUNDARY|gavin_iris_null_guard_bismarck_literal_pointer_guard_nonnull_only')
    print('RESOLUTION|2BATTLETIMID_FIXED_SOURCE_CLOSED_CONDITIONAL_REFERENCE')


def main():
    p=argparse.ArgumentParser()
    for name in PINNED:p.add_argument('--'+name+'-dir',type=Path,required=True)
    p.add_argument('--data-dir',type=Path);p.add_argument('--setup',type=Path);args=p.parse_args()
    options=()
    if args.data_dir:
        from tools.stoneage_recovered25_2battletimid_probe import analyze_runtime_objects,EXPECTED_PETSKILL_SHA256
        from tools.stoneage_recovered25_petskill_runtime import load_recovered25_petskill_runtime
        from tools.stoneage_recovered25_enemybase_runtime import load_recovered25_enemybase_runtime
        import hashlib
        pets=load_recovered25_petskill_runtime(data_dir=args.data_dir,setup=args.setup)
        enemies=load_recovered25_enemybase_runtime(data_dir=args.data_dir,setup=args.setup)
        result=analyze_runtime_objects(pets,enemies)
        if hashlib.sha256((args.data_dir/pets.source_file).read_bytes()).hexdigest()!=EXPECTED_PETSKILL_SHA256 or not all(result[k+'_closed'] for k in ('population','exact_rows','exact_templates')):
            raise ValueError('actual OPTION identity must be accepted before native comparison')
        options=tuple(pets.skills[skill].option_bytes for skill in result['callback_ids'])
    rows=[analyze_profile(name,getattr(args,name+'_dir'),options) for name in PINNED]
    emit(rows,options)


if __name__=='__main__':main()
