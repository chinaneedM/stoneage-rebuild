"""Preserved ordinary enemies and a healthy solo player: original create/entry/exit.

Original source/header/master bytes remain transient. Typed network/monitor
collectors are adapters, not original transport or anti-abuse implementations.
"""
from __future__ import annotations
import argparse
import filecmp
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from tools.stoneage_battle_pool_audit import domain as pool_domain, native_source as pool_native, actor_delta, natural_birth_expectation
from tools.stoneage_enemy_entry_exit_audit import compile_probe, RowReader, entry_changes
from tools.stoneage_enemy_loader_audit import pp_file, specimen, loaded_oracle, eligible, PROFILES
from tools.stoneage_enemy_creation_audit import definition, rng_value, trap_definitions
from tools.stoneage_object_ownership_audit import BIRTH_DATA, BIRTH_WORK
from tools.stoneage_default_template_audit import digest, include_args, preprocess, expression
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _compact, _function

ROOT=Path(__file__).resolve().parents[1]
PIN_PATH=ROOT/'research/recovered/STONEAGE-PLAYER-BATTLE-SOURCE-DOMAINS-R1.json'
RESOLUTION='BOUNDED_ACTUAL_SOLO_PLAYER_CREATION_ENTRY_HEALTHY_EXIT_REUSE_PASS_ZERO_RUNTIME_PROMOTIONS'


def domain(profile,root):
    source,prior,data,flags,exps,ride=pool_domain(profile,root)
    accepted=json.loads((PIN_PATH.parent/'STONEAGE-BATTLE-POOL-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]['identity']
    if prior!=accepted:raise ValueError('accepted pool identity drift')
    paths={k:LAYOUTS[profile]/v for k,v in {'battle':'battle/battle.c','char':'char/char.c','base':'char/char_base.c','party':'char/char_party.c'}.items()}
    if profile=='bismarck':paths['lua']=LAYOUTS[profile]/'mylua/function.c'
    texts={k:pp_file(profile,root,v) for k,v in paths.items()}
    groups={'battle':['BATTLE_PetDefaultEntry','BATTLE_ClearGetExp','BATTLE_PartyNewEntry'],'char':['CHAR_sendBattleEffect']}
    if profile=='gavin':groups['base']=['CHAR_CHECKSKILLINDEX','_CHAR_getIntPSkill']
    else:
        groups['party']=['getPartyNum']
        groups['lua']=['FindLua','EquipEffectFunction']
    bodies={n:(_function(texts[k],'lua_State *FindLua') if n=='FindLua' else definition(texts[k],n)) for k,names in groups.items() for n in names}
    # Replace only an explicitly inherited adapter; original bodies stay intact.
    fd=definition(source,'getfdFromCharaIndex')
    source=source.replace(fd,fd.replace('return -1;','return 7;'),1)
    watch=definition(source,'CHAR_sendWatchEvent')
    source=source.replace(watch,r'''
static int effect_count,effect_payload[3];
void CHAR_sendWatchEvent(int index,int act,int *opt,int len,int mine){
 if(act==CHAR_ACTSTAND){if(index<0||index>=2||opt||len||mine!=1)abort();watch_count++;return;}
 if(index!=0||act!=CHAR_ACTBATTLE||!opt||len!=3||mine!=1)abort();
 effect_count++;memcpy(effect_payload,opt,sizeof(effect_payload));
}
''',1)
    if profile=='bismarck':
        item=definition(source,'ITEM_equipEffect')
        lua='#include "mylua/mylua.h"\nMY_Lua MYLua;\n'+bodies['FindLua']+'\n'+bodies['EquipEffectFunction']+'\n'
        source=source.replace(item,lua+item,1)
    # The original compliance body occurs earlier in the inherited composition.
    for n in groups.get('base',[]):source=source.replace(definition(source,'_CHAR_complianceParameter'),bodies[n]+'\n'+definition(source,'_CHAR_complianceParameter'),1)
    source+='\n#define time audit_time\n'
    for k in ('party','battle','char'):
        for n in groups.get(k,[]):source+=bodies[n]+'\n'
    source+='#undef time\n'
    prefix='lssproto_' if profile=='gavin' else 'GmsvServer_'
    callbacks={
        'CAflush':'if(ACTOR!=0)abort();ca_count++;',
        'CDflush':'if(ACTOR!=0)abort();cd_count++;',
        'CheckDefBTime':'if(ACTOR!=0||fd!=7||lowTime!=1000||battletime!=2||addTime!=0)abort();monitor_count++;return 1;',
        'CONNECT_checkfd':'if(fd!=7)abort();checkfd_count++;return 1;',
        'CONNECT_SetBattleRecvTime':'if(fd!=7||!a||a->tv_sec!=1000||a->tv_usec!=0)abort();recv_count++;',
        'CHAR_Skillupsend':'if(ACTOR!=0)abort();skill_count++;return 1;',
        'CHAR_send_P_StatusString':'if(ACTOR!=0)abort();status_count++;status_mask=indextable;return 1;',
        prefix+'EN_send':'en_count++;en_fd=fd;en_result=result;en_field=field;',
        prefix+'NC_send':'nc_count++;nc_fd=fd;nc_flg=flg;',
        prefix+'XYD_send':'xyd_count++;xyd_fd=fd;xyd_x=x;xyd_y=y;xyd_dir=dir;',
    }
    source+='\nstatic int ca_count,cd_count,monitor_count,checkfd_count,recv_count,skill_count,status_count;\nstatic unsigned int status_mask;\nstatic int en_count,en_fd,en_result,en_field,nc_count,nc_fd,nc_flg,xyd_count,xyd_fd,xyd_x,xyd_y,xyd_dir;\n'
    signatures={}
    for n,body in callbacks.items():
        signature=trap_definitions(profile,root,source,[n]).split('{',1)[0].strip()
        signatures[n]=digest(_compact(signature))
        source+=signature+'{'+body.replace('ACTOR','charaindex' if profile=='gavin' else 'char_index')+'}\n'
    constants=('CHAR_PARTYMAX','BATTLE_S_TYPE_PLAYER','BATTLE_S_TYPE_ENEMY','BATTLE_TYPE_P_vs_E','CHAR_P_STRING_HP','CHAR_P_STRING_EXP','CHAR_P_STRING_MP','CHAR_P_STRING_DUELPOINT','CHAR_P_STRING_CHARM','CHAR_P_STRING_EARTH','CHAR_P_STRING_WATER','CHAR_P_STRING_FIRE','CHAR_P_STRING_WIND','CHAR_P_STRING_RIDEPET')
    ev=prior['accepted_entry_identity']['enum_values']|prior['battle_mode_enum_values']
    pp=preprocess(profile,root,source+'\n'+''.join('int observed_'+n+'='+n+';\n' for n in constants))
    for body in re.findall(r'\benum(?:\s+\w+)?\s*\{([^{}]+)\}',pp):
        if 'BATTLE_TYPE_P_vs_E' not in body:continue
        value=-1
        for item in body.split(','):
            if not item.strip():continue
            pair=item.strip().split('=',1);name=pair[0].strip()
            value=expression(pair[1],ev) if len(pair)==2 else value+1;ev[name]=value
    values={n:expression(re.search(r'int observed_'+n+r'\s*=\s*([^;]+);',pp)[1],ev) for n in constants}
    deps=subprocess.run(['cc','-MM',*include_args(profile,root),'-x','c','-'],input=source,text=True,capture_output=True,check=True).stdout
    closure={}
    for n in deps.replace('\\\n',' ').split()[1:]:
        p=Path(n)
        if p.is_file():closure[p.relative_to(root).as_posix()]=digest(p.read_bytes())
    normalized_lua={};lua_declarations=[]
    if profile=='bismarck':
        # Lua 5.1 parenthesizes its declarator names; normalize declarations only
        # so the inherited typed unreachable-trap extractor can consume them.
        for match in re.finditer(r'(?m)^extern ([^;{}\n]+?)\((lua_\w+|luaL_\w+)\)(\s*\([^;{}]+\)\s*;)',pp):
            declaration=match[1]+match[2]+match[3]
            normalized_lua[match[2]]=digest(_compact(declaration));lua_declarations.append(declaration)
        source=source.replace('#include "mylua/mylua.h"\n','#include "mylua/mylua.h"\n'+'\n'.join(lua_declarations)+'\n',1)
    identity={'source_sha':PINNED[profile],'accepted_pool_identity':prior,
              'files':{str(p):digest((root/p).read_bytes()) for p in paths.values()},
              'functions':{n:digest(_compact(b)) for n,b in bodies.items()},
              'collector_signature_sha256':signatures,'normalized_original_Lua_declaration_sha256':normalized_lua,'constants':values,
              'header_dependency_closure':dict(sorted(closure.items())),
              'scope':'healthy solo unequipped player0, no pets/party/profession/ride/ticket, mode0 ordinary enemies1..3',
              'adapters':['descriptor7','typed packet/status/skill/flush collectors','CheckDefBTime monitor collector/CONNECT_checkfd1','receive-time collector',
                          'battle effect watcher payload collector','inherited encounter/field/RNG/clock/walk/world/detached-node collectors'],
              'controlled_player_preparation':'original world constructor; explicit guards/base stats/empty pet/party/skill arrays; original compliance then captured baseline; restored per case',
              'player_all_fields_independent_oracle':False,
              'Bismarck_Lua_scope':'original FindLua and EquipEffectFunction with controlled empty MYLua list; Lua invocation aborts' if profile=='bismarck' else 'not applicable'}
    return source,identity,data,flags,exps,ride


def pinned_identity(identity):
    """Link accepted evidence by canonical identity hash rather than duplicating it."""
    prior=identity['accepted_pool_identity']
    return {**{k:v for k,v in identity.items() if k!='accepted_pool_identity'},
            'accepted_pool_pin_path':'research/recovered/STONEAGE-BATTLE-POOL-SOURCE-DOMAINS-R1.json',
            'accepted_pool_identity_sha256':digest(json.dumps(prior,sort_keys=True,separators=(',',':')))}


def native_source(profile,source):
    # Reuse the independently authored observational helpers, not a C facsimile.
    old=pool_native(profile,source);prefix=old[:old.index('int main(int argc')]
    prefix=prefix.replace('Side[1].Entry[i];','Side[1].Entry[i+5];')
    original=definition(prefix,'world_same')
    replacement=original.replace('memcmp(worlds,slots,2*sizeof(Char))','memcmp(&worlds[1],&slots[1],sizeof(Char))')
    prefix=prefix.replace(original,replacement,1)
    setup='if(!configmem(64,262144))return 11;' if profile=='gavin' else 'sUnitSize=64;sUnitNumTotal=262144;'
    jump='static int controlled_jump[2]={-1,0};MAP_idjumptbl=controlled_jump;' if profile=='gavin' else 'MAP_idjumptbl[0]=-1;MAP_idjumptbl[1]=0;'
    special='slots[0].workint[CHAR_WORKSTREETVENDOR]=-1;slots[0].workint[CHAR_WORKANGELMODE]=0;slots[0].data[PROFESSION_CLASS]=PROFESSION_CLASS_NONE;' if profile=='gavin' else 'slots[0].workint[CHAR_WORKNOCAST]=777;slots[0].workint[CHAR_WORK_SHOWBATTLETIME]=0;'
    field='char_index' if profile=='bismarck' else 'charaindex'
    return (prefix+r'''
static Char player_before;
static int player_retained(Char *ch){
 Char retained=*ch;memcpy(retained.workint,player_before.workint,sizeof(retained.workint));memcpy(retained.flg,player_before.flg,sizeof(retained.flg));
 return !memcmp(&retained,&player_before,sizeof(retained));
}
static void player_state(void){
 Char *ch=&slots[0];BATTLE_ENTRY *e=&BattleArray[battle_at].Side[0].Entry[0];
 printf(" %d %d %d %d %d %d %d %d",ch->use,e->ENTRY_FIELD,e->bid,e->escape,searchObjectFromCharaIndex(0),
  !memcmp(ch->data,player_before.data,sizeof(ch->data)),player_retained(ch),ch->CharMakeSequenceNumber);
 sparse(ch->workint,player_before.workint);for(int j=0;j<sizeof(ch->flg);j++)printf(" %u",(unsigned char)ch->flg[j]);
}
static void packets(void){
 printf(" %d %d %d %d %d %d %d %d %d %d %d %d %d %u %d %d %d %d %d %d %d %d %d %d %d %d %d",
 ca_count,cd_count,recv_count,en_count,en_fd,en_result,en_field,effect_count,effect_payload[0],effect_payload[1],effect_payload[2],monitor_count,status_count,status_mask,checkfd_count,skill_count,nc_count,nc_fd,nc_flg,xyd_count,xyd_fd,xyd_x,xyd_y,xyd_dir,encounter_count,field_count,fd_count);
}
static void stage(void){
 printf(" %d %d %d %d %d %d %d %d %d %d %d",battle_at,Battle_getTotalBattleNum(),BATTLE_searchCnt,
  BattleArray[battle_at].use,BattleArray[battle_at].mode,world_same(),clock_count,slots[4].use+slots[5].use+slots[6].use,
  initCharCounter[2].cnt,walk_count,reclaim_count);
 BATTLE *b=&BattleArray[battle_at];
 printf(" %d %d %d %d %d %d %d %d %d %d",b->Side[0].type,b->Side[1].type,b->leaderindex,b->type,b->createindex,b->field_no,b->dpbattle,b->Side[0].flg,b->CreateTime,b->flgTime);
 // Observe every entry including empty swapped front/back positions.
 for(int s=0;s<2;s++)for(int j=0;j<BATTLE_ENTRY_MAX;j++){
  BATTLE_ENTRY *e=&b->Side[s].Entry[j];printf(" %d %d %d",e->ENTRY_FIELD,e->bid,e->escape);
  for(int k=0;k<GETITEM_MAX;k++)printf(" %d",e->getitem[k]);
 }
 player_state();actors();packets();
}
int main(int argc,char **argv){
 if(argc!=3||sizeof(void*)!=8||sizeof(int)!=4)return 10;
'''+setup+r'''
 if(!memInit())return 12;
 if(!ENEMYTEMP_initEnemy(argv[1])||!ENEMY_initEnemy(argv[2])||!BATTLE_initBattleArray(3))return 13;
 MAP_map=controlled_map;MAP_idtblsize=1;
'''+jump+r'''
 controlled_map[0].id=1;controlled_map[0].xsiz=controlled_map[0].ysiz=2;controlled_map[0].olink=controlled_links;
 initCharCounter[0]=(INITCHARCOUNTER){0,0,2};initCharCounter[1]=(INITCHARCOUNTER){2,2,4};initCharCounter[2]=(INITCHARCOUNTER){4,4,7};
 if(!initObjectArray(2))return 14;
 for(int i=0;i<2;i++){int c,o;if(!CHAR_createCharacter(CHAR_TYPEPLAYER,1,1,1,0,&c,&o,1)||c!=i||o!=i)return 15;}
 slots[0].data[CHAR_VITAL]=10000;slots[0].data[CHAR_STR]=10000;slots[0].data[CHAR_TOUGH]=10000;slots[0].data[CHAR_DEX]=10000;
 slots[0].data[CHAR_HP]=20;slots[0].data[CHAR_BECOMEPIG]=-1;slots[0].data[CHAR_DEFAULTPET]=-1;slots[0].data[CHAR_RIDEPET]=-1;
 slots[0].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_NONE;slots[0].workint[CHAR_WORKBATTLEINDEX]=-1;
 slots[0].workint[CHAR_WORKPETFOLLOW]=-1;slots[0].workint[CHAR_WORKPETFALL]=0;slots[0].workint[CHAR_WORKACTION]=-1;
 slots[0].workint[CHAR_WORKPARTYMODE]=CHAR_PARTY_NONE;slots[0].workint[CHAR_WORKGETEXP]=777;slots[0].workint[CHAR_WORKFD]=7;
 slots[0].workint[CHAR_WORKTICKETTIME]=slots[0].workint[CHAR_WORKTICKETTIMESTART]=0;
 for(int i=0;i<CHAR_PARTYMAX;i++)slots[0].workint[CHAR_WORKPARTYINDEX1+i]=-1;
 for(int i=0;i<CHAR_MAXPETHAVE;i++)slots[0].unionTable.indexOfPet[i]=-1;
 memset(slots[0].haveSkill,0,sizeof(slots[0].haveSkill));
'''+special+r'''
 if(!CHAR_complianceParameter(0)||slots[0].data[CHAR_HP]!=20)return 16;
 player_before=slots[0];memcpy(worlds,slots,2*sizeof(Char));
 printf("P");sparse(player_before.workint,NULL);for(int j=0;j<sizeof(player_before.flg);j++)printf(" %u",(unsigned char)player_before.flg[j]);printf("\n");
 int array,mode,count;
 while(scanf("%d%d%d",&array,&mode,&count)==3){
  slots[0]=player_before;born=0;rng_mode=mode;clock_count=netwatch_count=0;encounter_count=field_count=fd_count=0;
  ca_count=cd_count=recv_count=en_count=effect_count=monitor_count=status_count=checkfd_count=skill_count=nc_count=xyd_count=0;
  status_mask=0;en_fd=en_result=en_field=nc_fd=nc_flg=xyd_fd=xyd_x=xyd_y=xyd_dir=0;memset(effect_payload,0,sizeof(effect_payload));
  for(int j=0;j<count;j++)encounter_table[j]=array;encounter_table[count]=-1;
  battle_at=BATTLE_searchCnt%3;printf("C %d %d %d",array,mode,count);
  int ret=BATTLE_CreateVsEnemy(0,0,-1);printf(" %d",ret);stage();
  ret=BATTLE_Exit(0,battle_at);printf(" %d",ret);stage();
  BATTLE_ExitAll(battle_at);printf(" %d",BATTLE_DeleteBattle(battle_at));stage();printf("\n");
 }
 endObjectOne(0);endObjectOne(1);memEnd();return 0;
}
''').replace('ENTRY_FIELD',field)


def cases_for(selected):
    return [(i,m,1+n%3) for n,(i,m) in enumerate((i,m) for i in selected for m in range(4))]


def player_delta(profile,identity,before,battle,exited):
    pool=identity['accepted_pool_identity'];entry=pool['accepted_entry_identity'];ev=entry['enum_values']
    after=before.copy();after.update(entry_changes(profile,entry,before,0,exited))
    after[ev['CHAR_WORKBATTLEINDEX']]=-1 if exited else battle;after[ev['CHAR_WORKGETEXP']]=0
    if profile=='bismarck':
        after[ev['CHAR_WORK_SHOWBATTLETIME']]=1002
        if exited:after[ev['CHAR_WORKNOCAST']]=0
    return {k:v for k,v in sorted(after.items()) if v!=before.get(k,0)}


def expected_packets(profile,identity,battle,exited):
    const=identity['constants'];mask=0
    if exited:
        for n,v in const.items():
            if n.startswith('CHAR_P_STRING_'):mask|=v
    return [1,1,int(profile=='gavin'),1,7,const['BATTLE_TYPE_P_vs_E'],0,1,battle,0,0,int(exited),int(exited),mask,
            int(exited and profile=='bismarck'),int(exited),int(exited),7 if exited else 0,0,int(exited),7 if exited else 0,
            1 if exited else 0,1 if exited else 0,0,1,1,(2 if profile=='gavin' else 1)+(3 if exited else 0)]


def verify_line(profile,identity,data,flags,exps,temps,enemies,case,line,number,sequence,player_base,player_flags):
    rd=RowReader(line);index,mode,count=case;pool=identity['accepted_pool_identity'];entry=pool['accepted_entry_identity'];ev=entry['enum_values'];lim=entry['limits'];const=identity['constants']
    if rd.take(3)!=list(case):raise ValueError('player battle case order')
    battle=number%3;loader=entry['accepted_ownership_identity']['accepted_loader_identity'];e=enemies[index];ce=loader['accepted_creator_identity']['enum_values']
    level=rng_value(mode,e[1][ce['ENEMY_LV_MIN']],e[1][ce['ENEMY_LV_MAX']])
    d,w=natural_birth_expectation(loader,data,exps,temps[e[0]],e,level,mode);births=[]
    slots=[4+(sequence-2+j)%3 for j in range(count)]
    for j in range(count):
        if rd.take(3)!=[slots[j],15,sequence+j]:raise ValueError('player battle birth slot/RNG/sequence')
        if rd.take(len(BIRTH_DATA)+len(BIRTH_WORK))!=[d[n] for n in BIRTH_DATA]+[w[n] for n in BIRTH_WORK]:raise ValueError('player battle named birth')
        before=rd.sparse(ev['CHAR_WORKDATAINTNUM']);f=rd.take(lim['flag_bytes'])
        if f!=flags+[0]*(lim['flag_bytes']-len(flags)):raise ValueError('player battle birth flags')
        for n,v in w.items():
            if before.get(ev[n],0)!=v:raise ValueError('player battle captured birth consistency')
        if births and births[0]!=(before,f):raise ValueError('player battle simultaneous birth baseline')
        births.append((before,f))
    for stage in range(3):
        exited=stage>0;deleted=stage==2
        if rd.take(1)!=[0]:raise ValueError('player battle create/Exit/Delete return')
        clock=1+int(profile=='bismarck')+int(exited)+(count if deleted and profile=='gavin' else 0)
        wanted=[battle,int(not deleted),battle+1,int(not deleted),pool['battle_mode_enum_values']['BATTLE_MODE_NONE' if deleted else 'BATTLE_MODE_INIT'],1,clock,
                0 if deleted else count,4+(sequence-2+count)%3,2,0]
        got=rd.take(11)
        if got!=wanted:raise ValueError('player battle arena/cursor/world/lifetime '+str((stage,got,wanted)))
        if rd.take(10)!=[const['BATTLE_S_TYPE_PLAYER'],const['BATTLE_S_TYPE_ENEMY'],0,const['BATTLE_TYPE_P_vs_E'],-1,0,0,0,1000,200]:raise ValueError('player battle arena metadata')
        for side in range(2):
            for pos in range(lim['entry_max']):
                actor=-1;bid=-1
                if not deleted:
                    if side==0 and pos==0:actor=-1 if exited else 0;bid=0
                    if side==1:
                        bid=10+pos
                        if pos>=5 and pos<5+count and not deleted:actor=slots[pos-5]
                if side==1 and deleted:actor=-1
                if rd.take(3+lim['item_max'])!=[actor,bid,0]+[-1]*lim['item_max']:raise ValueError('player battle full swapped entries')
        if rd.take(8)!=[1,-1 if exited else 0,-1 if deleted else 0,0,0,1,1,0]:raise ValueError('player battle player lifetime/data/string/object')
        got=rd.sparse(ev['CHAR_WORKDATAINTNUM']);wanted=player_delta(profile,identity,player_base,battle,exited)
        if got!=wanted:raise ValueError('player battle complete player work delta '+str((stage,got,wanted)))
        pf=player_flags.copy();pf[ev['CHAR_ISATTACKED']//8]|=1<<(ev['CHAR_ISATTACKED']%8);pf[ev['CHAR_ISDIE']//8]&=255^(1<<(ev['CHAR_ISDIE']%8))
        if rd.take(lim['flag_bytes'])!=pf:raise ValueError('player battle player flags')
        for j,(before,f) in enumerate(births):
            enemy_exited=deleted
            if rd.take(4+lim['item_max'])!=[slots[j],-1 if enemy_exited else slots[j],-1 if deleted else 15+j,0]+[-1]*lim['item_max']:raise ValueError('player battle enemy entry')
            if rd.take(5)!=[int(not enemy_exited),1,-1,1,1]:raise ValueError('player battle enemy lifetime/data/string/item/object')
            abio=100466<=d['CHAR_BASEBASEIMAGENUMBER']<=100471
            if rd.sparse(ev['CHAR_WORKDATAINTNUM'])!=actor_delta(profile,pool,before,battle,enemy_exited,abio):raise ValueError('player battle complete enemy work')
            ef=f.copy();ef[ev['CHAR_ISATTACKED']//8]|=1<<(ev['CHAR_ISATTACKED']%8);ef[ev['CHAR_ISDIE']//8]&=255^(1<<(ev['CHAR_ISDIE']%8))
            if rd.take(lim['flag_bytes'])!=ef:raise ValueError('player battle enemy flags')
        got=rd.take(27);wanted=expected_packets(profile,identity,battle,exited)
        if got!=wanted:raise ValueError('player battle exact network/monitor/effect collectors '+str((stage,got,wanted)))
    rd.done();return sequence+count


def verify_output(profile,identity,data,flags,exps,temps,enemies,cases,path):
    entry=identity['accepted_pool_identity']['accepted_entry_identity'];ev=entry['enum_values'];sequence=2
    with path.open() as stream:
        line=stream.readline()
        if not line.startswith('P '):raise ValueError('player battle baseline')
        rd=RowReader('C '+line[2:]);base=rd.sparse(ev['CHAR_WORKDATAINTNUM']);pf=rd.take(entry['limits']['flag_bytes']);rd.done()
        for n,v in {'CHAR_WORKOBJINDEX':0,'CHAR_WORKBATTLEMODE':0,'CHAR_WORKBATTLEINDEX':-1,'CHAR_WORKGETEXP':777,'CHAR_WORKFD':7,'CHAR_WORKPARTYMODE':0,'CHAR_WORKPETFOLLOW':-1}.items():
            if base.get(ev[n],0)!=v:raise ValueError('controlled player baseline '+n)
        for n,c in enumerate(cases):sequence=verify_line(profile,identity,data,flags,exps,temps,enemies,c,stream.readline(),n,sequence,base,pf)
        if stream.readline():raise ValueError('player battle extra rows')


def mutation_trials(source):
    def one(name,pattern,replacement,label):
        body=definition(source,name);changed,n=re.subn(pattern,replacement,body)
        if n!=1:raise ValueError('player battle mutation anchor '+label+' '+str(n))
        return label,source.replace(body,changed,1)
    yield one('BATTLE_ClearGetExp',r'CHAR_setWorkInt\(\s*(?:charaindex|char_index)\s*,\s*CHAR_WORKGETEXP\s*,\s*0\s*\)\s*;', '(void)0;', 'clear-player-exp')
    yield one('BATTLE_CreateVsEnemy',r'pEntry\[i\s*\+\s*5\]\.bid\s*=\s*i\s*\+\s*5\s*\+\s*SIDE_OFFSET\s*;', 'pEntry[i+5].bid=i+SIDE_OFFSET;', 'swapped-bid')
    yield one('BATTLE_CreateVsEnemy',r'CHAR_sendBattleEffect\(\s*(?:charaindex|char_index)\s*,\s*1\s*\)\s*;', '(void)0;', 'battle-effect')
    yield one('_BATTLE_Exit',r'CHAR_Skillupsend\(\s*(?:charaindex|char_index)\s*\)\s*;', '(void)0;', 'player-Exit-skill')
    yield one('_BATTLE_Exit',r'CHAR_setWorkInt\(\s*(?:charaindex|char_index)\s*,\s*CHAR_WORKBATTLEMODE\s*,\s*BATTLE_CHARMODE_FINAL\s*\)\s*;', 'CHAR_setWorkInt(char_index,CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_NONE);' if 'int char_index' in definition(source,'_BATTLE_Exit') else 'CHAR_setWorkInt(charaindex,CHAR_WORKBATTLEMODE,BATTLE_CHARMODE_NONE);', 'player-Exit-mode')


def execute(profile,root,source,paths,cases,opt,traps,tmp):
    exe=tmp/('probe'+opt);compile_probe(profile,root,native_source(profile,source),exe,opt,traps)
    out=tmp/('output'+opt+'.txt')
    with out.open('w') as stream:
        r=subprocess.run([str(exe),*map(str,paths)],input=''.join(' '.join(map(str,c))+'\n' for c in cases),text=True,stdout=stream,stderr=subprocess.PIPE)
    if r.returncode or r.stderr:raise ValueError('unsafe solo player probe '+r.stderr+' rc='+str(r.returncode))
    return out


def audit(profile,root,paths):
    pins=json.loads(PIN_PATH.read_text())['profiles'][profile];source,identity,data,flags,exps,ride=domain(profile,root)
    if pinned_identity(identity)!=pins['identity']:raise ValueError('player battle source drift')
    loader=identity['accepted_pool_identity']['accepted_entry_identity']['accepted_ownership_identity']['accepted_loader_identity']
    temps,enemies=loaded_oracle(profile,loader,*[p.read_bytes() for p in paths],32,32)
    selected=eligible(loader,temps,enemies,ride);cases=cases_for(selected)
    with tempfile.TemporaryDirectory(prefix='stoneage-player-battle-') as directory:
        tmp=Path(directory);outputs=[]
        for opt in ('-O0','-O2'):
            out=execute(profile,root,source,paths,cases,opt,pins['unreachable_traps'],tmp)
            verify_output(profile,identity,data,flags,exps,temps,enemies,cases,out);outputs.append(out)
        if not filecmp.cmp(*outputs,shallow=False):raise ValueError('player battle optimization divergence')
        sha=hashlib.sha256(outputs[0].read_bytes()).hexdigest();rejected=0
        for name,mutant in mutation_trials(source):
            case=[(selected[0],1,3)]
            out=execute(profile,root,mutant,paths,case,'-O0',pins['unreachable_traps'],tmp)
            try:verify_output(profile,identity,data,flags,exps,temps,enemies,case,out)
            except ValueError:rejected+=1
            else:raise ValueError('undetected player battle mutation '+name)
    return {'profile':profile,'source_sha':PINNED[profile],'successful_solo_cycles':len(cases)*2,
            'preserved_enemy_births':sum(c[2] for c in cases)*2,'complete_player_work_stages':len(cases)*6,
            'complete_enemy_work_stages':sum(c[2] for c in cases)*6,'mutations_rejected':rejected,'semantic_sha256':sha}


def main():
    parser=argparse.ArgumentParser()
    for p in PINNED:parser.add_argument('--'+p+'-dir',type=Path,required=True)
    args=parser.parse_args();roots={p:getattr(args,p+'_dir') for p in PINNED}
    for p,r in roots.items():
        if subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip()!=PINNED[p] or subprocess.check_output(['git','-C',str(r),'status','--porcelain'],text=True):raise ValueError('source pin/cleanliness '+p)
    paths,receipt=specimen(roots['gavin']);pins=json.loads(PIN_PATH.read_text())
    if receipt!=pins['preserved_specimen']:raise ValueError('player battle input drift')
    totals={k:0 for k in ('successful_solo_cycles','preserved_enemy_births','complete_player_work_stages','complete_enemy_work_stages')}
    for p in PROFILES:
        row=audit(p,roots[p],paths)
        for k in totals:totals[k]+=row[k]
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print('TOTAL|'+'|'.join(f'{k}={v}' for k,v in totals.items())+'|executed_profiles=2')
    print('MUTATIONS|semantic_mutations_rejected=10|clear_player_exp_swapped_bid_effect_player_Exit_skill_FINAL|additional_cycles=10')
    print('FACT|complete_original_CreateVsEnemy_PartyNewEntry_solo_PetDefaultEntry_empty_ClearGetExp_BattleEffect_player_Exit_compliance_enemy_ExitAll_Delete_reuse_execute')
    print('FACT|player_remains_live_object_owner_enemy_partition_recycles_actual_round_robin_slots_and_battle_cursor')
    print('BOUNDARY|healthy_solo_player_preparation_descriptor7_typed_network_monitor_collectors_no_party_pet_profit_full_server_original_reclaimer')
    print('OPEN|party_pet_CreateVsEnemy_Init_TaskLoop_player_pet_profit_watcher_nonempty_items_callbacks_original_ABI_JSS_Taiwan_v1_Iris_encoding')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
