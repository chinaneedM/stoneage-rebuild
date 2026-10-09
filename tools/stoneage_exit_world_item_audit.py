"""Bounded complete Exit with original item death, warp and map link movement.

Original bodies are extracted only from clean pinned transient trees. The
independent oracle separates actor, item, object and map-link lifetime.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_exit_destroy_ticket_audit import source_domain as prior_domain, handles as prior_handles, native_source as prior_native
from tools.stoneage_exit_lifetime_watch_audit import _definition
from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_becomepig_restore_audit import constants, run_native
from tools.stoneage_becomepig_native_audit import _assert_rows

PIN_PATH=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-EXIT-WORLD-ITEM-SOURCE-DOMAINS-R1.json'
RESOLUTION='BOUNDED_ORIGINAL_EXIT_WORLD_ITEM_PASS_ZERO_RUNTIME_PROMOTIONS'


def source_domain(profile,root):
    f,prior=prior_domain(profile,root)
    if prior!=json.loads(PIN_PATH.with_name('STONEAGE-EXIT-DESTROY-TICKET-SOURCE-DOMAINS-R1.json').read_text())['profiles'][profile]:
        raise ValueError('accepted Exit domain drift')
    base=root/LAYOUTS[profile];inc=['-I',str(base/'include')]
    if profile=='bismarck':inc+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    groups={'item/item.c':('ITEM_CHECKARRAYINDEX','_ITEM_CHECKINDEX','_ITEM_endExistItemsOne'),
            'char/char_base.c':('_CHAR_CHECKITEMINDEX','_CHAR_getItemIndex','CHAR_getPlayerMaxNum','CHAR_initCharOneArray'),
            'char/char.c':('_CHAR_warpToSpecificPoint',),
            'object.c':('OBJECT_getType','OBJECT_getFloor','OBJECT_getX','OBJECT_getY','OBJECT_setFloor','OBJECT_setX','OBJECT_setY'),
            'map/readmap.c':('_MAP_objmove',)}
    extra={}
    for path,names in groups.items():
        raw=re.sub(r'^\s*#\s*include[^\n]*','',_text(base/path),flags=re.M)
        pp=subprocess.run(['cpp','-P',*inc,'-'],input='#include "version.h"\n'+raw,text=True,capture_output=True,check=True).stdout
        for n in names:extra[n]=_definition(pp,n)
    init=_compact(extra['CHAR_initCharOneArray'])
    if not ('memset(&CHAR_chara[i],0,sizeof(Char));' in init and 'memcpy(&CHAR_chara[i],ch,sizeof(Char));' in init):
        raise ValueError('original allocator replacement contract drift')
    item=_compact(extra['_ITEM_endExistItemsOne'])
    if 'CHAR_getItemIndex(' not in item or 'hitcnt<1' not in item or 'indexOfExistPoolItems' in item:
        raise ValueError('original carried player reference scan drift')
    for n in ('OBJECT_getType','OBJECT_getFloor','OBJECT_getX','OBJECT_getY','OBJECT_setFloor','OBJECT_setX','OBJECT_setY'):
        if re.search(r'\bif\s*\(|CHECK',extra[n]):raise ValueError('unchecked object accessor contract drift')
    f.update(extra)
    return f,{'source_sha':PINNED[profile],'prior_domain':prior,
        'files':{p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in groups},
        'functions':{n:hashlib.sha256(_compact(b).encode()).hexdigest() for n,b in extra.items()},
        'contracts':{'item_scans_live_player_carried_slots_only':True,
          'object_accessors_have_no_index_or_use_guard':True,
          'map_old_floor_misplaced_link_recovery':profile=='bismarck',
          'allocator_replaces_slot_from_input_template':True,
          'allocator_body_static_inspection_only':True}}


def handles(f):
    c=prior_handles(f)
    more=constants([f['_CHAR_warpToSpecificPoint'],f['_ITEM_endExistItemsOne'],f['_CHAR_getItemIndex']])
    # Preserve all prior symbolic values; give new fields disjoint ordinals.
    for n in sorted(more):
        if n not in c and n!='BOOL':c[n]=700+len(c)
    c.pop('CHAR_CHECKITEMINDEX',None)
    c.update({'CHAR_PARTY_CLIENT':2,'CHAR_PETMAIL_NONE':0,'OBJTYPE_CHARA':1,'CHAR_DEFAULTSEESIZ':2,
              'CHAR_WORKENCOUNTPROBABILITY_MIN':850,'CHAR_WORKENCOUNTPROBABILITY_MAX':851,
              'CHAR_ENCOUNT_FIX':852,'CHAR_WORKOBJINDEX':853,'CHAR_FLOOR':854,'CHAR_X':855,'CHAR_Y':856})
    return c


def vectors():
    # Proper partitions: players 0/1, pet 2, enemy/other 3. No matched player.
    cases=set(itertools.product((2,3),(-1,0,1),(0,1),(0,1,2),range(5),(0,1),range(4),range(3)))
    out={(*v,999,17,1) for v in cases}
    for kind,side,ptr,layout,dest,ticket,per,otype in itertools.product((2,3),(-1,0,1),(0,1),range(4),range(3),(-1,0,999,1000,1001),(-1,17),(0,1)):
        out.add((kind,side,ptr,2,0,1,layout,dest,ticket,per,otype))
    return sorted(out)


class Oracle:
    def __init__(self,profile,c,limits,case):
        self.profile,self.c,self.limits=profile,c,limits
        (self.kind,self.side,self.ptr,self.pattern,self.peer,self.active,self.layout,self.dest,self.ticket,self.per,self.otype)=case
        self.actor=2 if self.kind==2 else 3;self.live=1
        self.work={'CHAR_WORKBATTLEMODE':1,'CHAR_WORKBATTLEINDEX':0,'CHAR_WORKFOXROUND':-1,
                   'CHAR_WORKTICKETTIME':self.ticket,'CHAR_WORKTICKETTIMESTART':900,
                   'CHAR_WORKENCOUNTPROBABILITY_MIN':5,'CHAR_WORKENCOUNTPROBABILITY_MAX':6,'CHAR_ENCOUNT_FIX':7,'CHAR_WORKOBJINDEX':0}
        self.coords=[7000,1,1];self.obj=[7000,1,1]
        self.cells=[[] for _ in range(32)]
        if self.layout==0:self.cells[5]=[0]
        if self.layout==2:self.cells[10]=[0]
        if self.layout==3:self.cells[5]=[1,0,2];self.cells[16+11]=[3,4]
        self.indices=[100+j for j in range(limits['items'])]+[200+j for j in range(limits['pool'])]
        self.itemuse={i:self.active for i in self.indices};self.owners={i:7 for i in self.indices};self.count=self.active*len(self.indices)
        self.entries=[[-1]*10 for _ in range(2)];self.escape=[[0]*10 for _ in range(2)]
        if self.side>=0:self.entries[self.side][9]=self.actor;self.escape[self.side][9]=7
        self.ends=self.stale_read=self.stale_write=self.cleared=0
        self.cleared=len(self.indices) if self.pattern==0 else len(self.indices)-4 if self.pattern==1 else 0
        self.trace=[];self.warp_ret=self.move_ret=-9

    def event(self,code,actor,value=0):self.trace.extend((code,actor,value))

    def read(self,key,integer=False):
        if not self.live:
            self.stale_read+=1;self.event(46 if integer else 45,self.actor,self.c[key])
            if self.profile=='bismarck':return -1
        return self.kind if key=='CHAR_WHICHTYPE' else 0 if key in ('CHAR_WORKPARTYMODE','CHAR_MAILMODE') else self.work[key]

    def write(self,key,value):
        if not self.live:self.stale_write+=1;self.event(47,self.actor,self.c[key]);return
        if key in ('CHAR_FLOOR','CHAR_X','CHAR_Y'):self.coords[('CHAR_FLOOR','CHAR_X','CHAR_Y').index(key)]=value
        else:self.work[key]=value

    def item_end(self,i):
        self.ends+=1;self.event(40,self.actor,i)
        if i<0 or not self.itemuse[i]:return
        retained=i==100 and self.peer in (1,4)
        if not retained:self.itemuse[i]=0;self.owners[i]=-1;self.count-=1

    def warp(self):
        self.read('CHAR_WORKOBJINDEX')
        if self.dest==0:self.warp_ret=0;self.event(53,self.actor,0);return
        self.event(50,0,self.obj[0])
        target=[7000 if self.dest==1 else 7001,41,6]
        for key,value in zip(('CHAR_FLOOR','CHAR_X','CHAR_Y'),target):self.write(key,value)
        old=list(self.obj);self.obj=target
        oldcell=(old[0]-7000)*16+old[2]*4+old[1]
        cell=oldcell if 0 in self.cells[oldcell] else next((j for j in range(16) if 0 in self.cells[j]),None) if self.profile=='bismarck' else None
        self.move_ret=int(cell is not None)
        if cell is not None:
            self.cells[cell].remove(0);self.cells[(target[0]-7000)*16+11].append(0)
        self.event(51,0,self.move_ret)
        for key in ('CHAR_WORKENCOUNTPROBABILITY_MIN','CHAR_WORKENCOUNTPROBABILITY_MAX'):
            if self.per!=-1:self.write(key,self.per)
        if self.profile!='bismarck':self.write('CHAR_ENCOUNT_FIX',0)
        self.read('CHAR_WHICHTYPE',True)
        # Preserve source short-circuit reads: pets read type twice and mail once.
        typ=self.read('CHAR_WHICHTYPE',True)
        if typ==2:self.read('CHAR_WHICHTYPE',True);self.read('CHAR_MAILMODE',True)
        self.event(52,0,0)
        self.read('CHAR_WHICHTYPE',True)
        if self.otype==1:self.event(54,self.actor,0)
        self.warp_ret=1;self.event(53,self.actor,1)

    def exit(self):
        if not self.live:return -101
        matched=self.side>=0 and self.entries[self.side][9]==self.actor
        if matched:
            self.entries[self.side][9]=-1;self.escape[self.side][9]=0
            self.work['CHAR_WORKBATTLEMODE']=2;self.work['CHAR_WORKBATTLEINDEX']=-1
            if self.kind==3:
                self.event(31,self.actor)
                if self.ptr:
                    for category,size in ((100,self.limits['items']),(200,self.limits['pool'])):
                        for j in range(size):self.item_end(category+j if self.pattern==2 or self.pattern==1 and j in (0,size-1) else -1)
                    self.cleared=len(self.indices);self.live=0
                self.event(41,self.actor,self.live)
        if self.profile!='bismarck' or self.live:self.read('CHAR_WORKPARTYMODE')
        if self.profile!='bismarck' or self.live:
            t=self.read('CHAR_WORKTICKETTIME')
            if 0<t<1000:
                self.event(32,self.actor,self.live)
                if self.read('CHAR_WORKTICKETTIMESTART')>0:
                    self.read('CHAR_WORKTICKETTIMESTART');self.event(32,self.actor,self.live)
                self.write('CHAR_WORKTICKETTIME',0);self.write('CHAR_WORKTICKETTIMESTART',0)
                self.event(33,self.actor,self.live);self.warp()
        return 0

    def run(self):
        a=self.exit();b=self.exit()
        fields=('CHAR_WORKBATTLEMODE','CHAR_WORKBATTLEINDEX','CHAR_WORKTICKETTIME','CHAR_WORKTICKETTIMESTART','CHAR_WORKENCOUNTPROBABILITY_MIN','CHAR_WORKENCOUNTPROBABILITY_MAX','CHAR_ENCOUNT_FIX')
        occupied=[(j//16,305 if j%16==11 else (j%16//4)*44+j%4,cell) for j,cell in enumerate(self.cells) if cell]
        return tuple([a,b,self.live,self.ends,self.cleared,self.stale_read,self.stale_write,self.count,self.warp_ret,self.move_ret,*self.coords,*self.obj,
          *(self.work[n] for n in fields),*(x for r in self.entries for x in r),*(x for r in self.escape for x in r),
          *(self.itemuse[i] for i in self.indices),*(self.owners[i] for i in self.indices),
          len(occupied),*(x for m,j,cell in occupied for x in [m,j,len(cell),*cell]),len(self.trace),*self.trace])


def native_source(profile,f,c,limits):
    h=prior_native(profile,f,c,limits).split('int main(void)')[0]
    h=h.replace('CHAR_chara[3]','CHAR_chara[4]').replace('CHAR_charanum=3','CHAR_charanum=4')
    h=h.replace('static BATTLE BattleArray[1];','static int subject,CHAR_playernum=2;\nstatic BATTLE BattleArray[1];')
    start=h.index('void ITEM_endExistItemsOne(int item)');end=h.index('void CHAR_send_N_StatusString',start)
    h=h[:start]+'void ITEM_endExistItemsOne(int item);\n'+h[end:]
    h=h.replace('void CHAR_sendCToArroundCharacter(int i){(void)i;abort();}','void CHAR_sendCToArroundCharacter(int i){event(52,i,0);}')
    start=h.index('void CHAR_warpToSpecificPoint(int i,int floor');end=h.index('static time_t clock_read',start)
    h=h[:start]+'void CHAR_warpToSpecificPoint(int i,int floor,int x,int y);\n'+h[end:]
    exitbody=f['_BATTLE_Exit'];h=h.replace(exitbody,'')
    h+=r'''
typedef struct {int use;struct {int workint[1024];} itm,item;} Item;
static Item ITEM_item[300],ITEM_gExists[300];static int ITEM_itemnum=300,ITEM_sItemNum=300,ITEM_UseItemnum,ITEM_sUseItemNum;
#define ITEM_CHECKINDEX(i) _ITEM_CHECKINDEX("w",0,i)
#define CHAR_CHECKITEMINDEX(i,j) _CHAR_CHECKITEMINDEX("w",0,i,j)
#define CHAR_getItemIndex(i,j) _CHAR_getItemIndex("w",0,i,j)
#define CheckCharMaxItem(i) CheckCharMaxItemChar(&CHAR_chara[i])
'''
    for n in ('CHAR_getPlayerMaxNum','_CHAR_CHECKITEMINDEX','_CHAR_getItemIndex','ITEM_CHECKARRAYINDEX','_ITEM_CHECKINDEX','_ITEM_endExistItemsOne'):h+=f[n]+'\n'
    h+=r'''
void ITEM_endExistItemsOne(int i){ends++;event(40,subject,i);_ITEM_endExistItemsOne(i,"w",0);}
typedef struct {int type,floor,x,y,index;} Object;
static Object obj[5];
typedef struct MAP_Objlink {int objindex;struct MAP_Objlink *next;} MAP_Objlink;
typedef MAP_Objlink *OBJECT;
typedef struct {int xsiz,ysiz;MAP_Objlink *olink[352];} Map;
static Map MAP_map[2];static MAP_Objlink links[5];static int destination,encounter,warp_ret,move_ret;
#define NEXT_OBJECT(p) ((p)->next)
#define GET_OBJINDEX(p) ((p)->objindex)
int OBJECT_getNum(void){return 5;}
int OBJECT_getIndex(int i){return obj[i].index;}
MAP_Objlink *MAP_getTopObj(int f,int x,int y){(void)f;(void)x;(void)y;abort();}
int MAP_getfloorIndex(int f){return f==7000?0:f==7001?1:-1;}
int MAP_IsValidCoordinate(int f,int x,int y){return destination!=0&&MAP_getfloorIndex(f)>=0&&x>=0&&x<44&&y>=0&&y<8;}
'''
    for n in ('OBJECT_getType','OBJECT_getFloor','OBJECT_getX','OBJECT_getY','OBJECT_setFloor','OBJECT_setX','OBJECT_setY','_MAP_objmove'):h+=f[n]+'\n'
    h+=r'''
int MAP_objmove(int i,int f,int x,int y,int nf,int nx,int ny){move_ret=_MAP_objmove("w",0,i,f,x,y,nf,nx,ny);event(51,i,move_ret);return move_ret;}
void CHAR_sendCDArroundChar_Main(int f,int x,int y,int i,int flag){(void)x;(void)y;(void)flag;event(50,i,f);}
int ENCOUNT_getEncountPercentMin(int i,int f,int x,int y){(void)i;(void)f;(void)x;(void)y;return encounter;}
int ENCOUNT_getEncountPercentMax(int i,int f,int x,int y){return ENCOUNT_getEncountPercentMin(i,f,x,y);}
void MAP_sendArroundChar(int i){event(54,i,0);}
void clearStayEncount(int fd){(void)fd;}
void CAflush(int i){(void)i;abort();}
void CHAR_sendArroundCharaData(int i){(void)i;abort();}
void CHAR_sendPMEToArroundCharacterFLXY(int i,int f,int x,int y,int a,int b,int e){(void)i;(void)f;(void)x;(void)y;(void)a;(void)b;(void)e;abort();}
void CHAR_sendLeader(int i,int v){(void)i;(void)v;abort();}
void CHAR_setWorkChar(int i,int f,const char *s){(void)i;(void)f;(void)s;abort();}
void CHAR_checkEffect(int i){(void)i;abort();}
int MAP_getMapFloorType(int f){(void)f;abort();}
void CHAR_sendAngelMark(int i,int v){(void)i;(void)v;abort();}
#define arraysizeof(a) (sizeof(a)/sizeof((a)[0]))
'''
    h+=f['_CHAR_warpToSpecificPoint']+'\n'
    h+='void CHAR_warpToSpecificPoint(int i,int floor,int x,int y){if(floor!=7001||x!=41||y!=6)abort();event(33,i,CHAR_chara[i].use);warp_ret=_CHAR_warpToSpecificPoint("w",0,i,destination==1?7000:floor,x,y);event(53,i,warp_ret);}\n'
    h+=exitbody+r'''
int main(void){int kind,side,pattern,peer,active,layout,ticket,otype;
while(scanf("%d%d%d%d%d%d%d%d%d%d%d",&kind,&side,&ptr,&pattern,&peer,&active,&layout,&destination,&ticket,&encounter,&otype)==11){
 memset(CHAR_chara,0,sizeof(CHAR_chara));memset(BattleArray,0,sizeof(BattleArray));memset(MAP_map,0,sizeof(MAP_map));memset(obj,0,sizeof(obj));memset(links,0,sizeof(links));memset(ITEM_item,0,sizeof(ITEM_item));memset(ITEM_gExists,0,sizeof(ITEM_gExists));
 nt=ends=badorder=stale_read=stale_write=cursor=0;warp_ret=move_ret=-9;subject=kind==2?2:3;
 for(int i=0;i<4;i++){CHAR_chara[i].use=1;CHAR_chara[i].data[CHAR_WHICHTYPE]=i<2?CHAR_TYPEPLAYER:i==2?CHAR_TYPEPET:CHAR_TYPEENEMY;CHAR_chara[i].workint[CHAR_WORKFOXROUND]=-1;CHAR_chara[i].data[CHAR_BECOMEPIG]=-1;
 for(int j=0;j<CHAR_MAXITEMHAVE;j++)CHAR_chara[i].indexOfExistItems[j]=-1;for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)CHAR_chara[i].indexOfExistPoolItems[j]=-1;}
 Char *ch=&CHAR_chara[subject];ch->data[CHAR_FLOOR]=7000;ch->data[CHAR_X]=ch->data[CHAR_Y]=1;
 ch->workint[CHAR_WORKBATTLEMODE]=1;ch->workint[CHAR_WORKBATTLEINDEX]=0;ch->workint[CHAR_WORKTICKETTIME]=ticket;ch->workint[CHAR_WORKTICKETTIMESTART]=900;
 ch->workint[CHAR_WORKENCOUNTPROBABILITY_MIN]=5;ch->workint[CHAR_WORKENCOUNTPROBABILITY_MAX]=6;ch->workint[CHAR_ENCOUNT_FIX]=7;
 for(int j=0;j<CHAR_MAXITEMHAVE;j++){ch->indexOfExistItems[j]=(pattern==2||(pattern==1&&(j==0||j==CHAR_MAXITEMHAVE-1)))?100+j:-1;ITEM_item[100+j].use=ITEM_gExists[100+j].use=active;ITEM_item[100+j].itm.workint[ITEM_WORKCHARAINDEX]=ITEM_gExists[100+j].item.workint[ITEM_WORKCHARAINDEX]=7;}
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++){ch->indexOfExistPoolItems[j]=(pattern==2||(pattern==1&&(j==0||j==CHAR_MAXPOOLITEMHAVE-1)))?200+j:-1;ITEM_item[200+j].use=ITEM_gExists[200+j].use=active;ITEM_item[200+j].itm.workint[ITEM_WORKCHARAINDEX]=ITEM_gExists[200+j].item.workint[ITEM_WORKCHARAINDEX]=7;}
 if(peer==1||peer==3||peer==4)CHAR_chara[0].indexOfExistItems[0]=100;
 if(peer==2)CHAR_chara[0].indexOfExistPoolItems[0]=100;
 if(peer==3)CHAR_chara[0].use=0;if(peer==4)CHAR_chara[0].indexOfExistItems[1]=100;
 ITEM_UseItemnum=ITEM_sUseItemNum=active*(CHAR_MAXITEMHAVE+CHAR_MAXPOOLITEMHAVE);
 BATTLE_battlenum=1;BattleArray[0].use=1;BattleArray[0].type=1;
 for(int s=0;s<2;s++)for(int j=0;j<10;j++){BattleArray[0].Side[s].Entry[j].charaindex=-1;BattleArray[0].Side[s].Entry[j].char_index=-1;}
 if(side>=0){BattleArray[0].Side[side].Entry[9].charaindex=subject;BattleArray[0].Side[side].Entry[9].char_index=subject;BattleArray[0].Side[side].Entry[9].escape=7;}
 obj[0].floor=7000;obj[0].x=obj[0].y=1;obj[0].type=otype;obj[0].index=subject;
 for(int i=0;i<5;i++)links[i].objindex=i;for(int i=0;i<2;i++){MAP_map[i].xsiz=44;MAP_map[i].ysiz=8;}
 if(layout==0)MAP_map[0].olink[45]=&links[0];if(layout==2)MAP_map[0].olink[90]=&links[0];
 if(layout==3){MAP_map[0].olink[45]=&links[1];links[1].next=&links[0];links[0].next=&links[2];MAP_map[1].olink[305]=&links[3];links[3].next=&links[4];}
 int a=_BATTLE_Exit("w",0,subject,0),b=_BATTLE_Exit("w",0,subject,0),cleared=0;
 for(int j=0;j<CHAR_MAXITEMHAVE;j++)cleared+=ch->indexOfExistItems[j]==-1;for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)cleared+=ch->indexOfExistPoolItems[j]==-1;
'''
    counter='ITEM_sUseItemNum' if profile=='bismarck' else 'ITEM_UseItemnum';arr='ITEM_gExists' if profile=='bismarck' else 'ITEM_item';field='item' if profile=='bismarck' else 'itm'
    h+=f'printf("%d %d %d %d %d %d %d %d %d %d",a,b,ch->use,ends,cleared,stale_read,stale_write,{counter},warp_ret,move_ret);\n'
    h+=r'''
 printf(" %d %d %d %d %d %d",ch->data[CHAR_FLOOR],ch->data[CHAR_X],ch->data[CHAR_Y],obj[0].floor,obj[0].x,obj[0].y);
 int fields[]={CHAR_WORKBATTLEMODE,CHAR_WORKBATTLEINDEX,CHAR_WORKTICKETTIME,CHAR_WORKTICKETTIMESTART,CHAR_WORKENCOUNTPROBABILITY_MIN,CHAR_WORKENCOUNTPROBABILITY_MAX,CHAR_ENCOUNT_FIX};for(int j=0;j<7;j++)printf(" %d",ch->workint[fields[j]]);
'''
    entry='char_index' if profile=='bismarck' else 'charaindex'
    h+=f'for(int s=0;s<2;s++)for(int j=0;j<10;j++)printf(" %d",BattleArray[0].Side[s].Entry[j].{entry});\n'
    h+='for(int s=0;s<2;s++)for(int j=0;j<10;j++)printf(" %d",BattleArray[0].Side[s].Entry[j].escape);\n'
    for expr in (f'{arr}[offset+j].use',f'{arr}[offset+j].{field}.workint[ITEM_WORKCHARAINDEX]'):
        h+=f'for(int group=0;group<2;group++){{int offset=group?200:100,size=group?CHAR_MAXPOOLITEMHAVE:CHAR_MAXITEMHAVE;for(int j=0;j<size;j++)printf(" %d",{expr});}}\n'
    h+=r'''
 int occupied=0;for(int m=0;m<2;m++)for(int j=0;j<352;j++)occupied+=MAP_map[m].olink[j]!=NULL;printf(" %d",occupied);
 for(int m=0;m<2;m++)for(int j=0;j<352;j++)if(MAP_map[m].olink[j]){int n=0;for(MAP_Objlink *p=MAP_map[m].olink[j];p;p=p->next){if(++n>5)abort();}printf(" %d %d %d",m,j,n);for(MAP_Objlink *p=MAP_map[m].olink[j];p;p=p->next)printf(" %d",p->objindex);}
 printf(" %d",nt);for(int j=0;j<nt;j++)printf(" %d",trace[j]);printf("\n");}return 0;}
'''
    return h


def audit(profile,root):
    f,identity=source_domain(profile,root)
    if identity!=json.loads(PIN_PATH.read_text())['profiles'][profile]:raise ValueError('world/item source domain drift')
    limits=identity['prior_domain']['prior_domain']['limits'];c=handles(f);cases=vectors()
    expected=[Oracle(profile,c,limits,v).run() for v in cases];source=native_source(profile,f,c,limits)
    payload=''.join(' '.join(map(str,v))+'\n' for v in cases)
    for opt in ('-O0','-O2'):_assert_rows(run_native(source,payload,opt),expected,profile+' world/item')
    rejected=0
    witness=(3,0,1,2,1,1,0,2,999,17,1)
    mapcase=(2,0,1,2,0,1,2,2,999,17,1)
    body=f['_ITEM_endExistItemsOne'];changed=re.sub(r'if\s*\(\s*hitcnt\s*<\s*1\s*\)','if (1)',body)
    setter=f['OBJECT_setFloor'];changedsetter=re.sub(r'obj\[index\]\.floor\s*=\s*newvalue;', '(void)newvalue;',setter)
    for old,new,case in ((body,changed,witness),(setter,changedsetter,mapcase)):
        if old==new:raise ValueError('unapplied semantic mutation')
        for opt in ('-O0','-O2'):
            rows=run_native(source.replace(old,new),' '.join(map(str,case))+'\n',opt)
            try:_assert_rows(rows,[Oracle(profile,c,limits,case).run()],profile+' mutation')
            except ValueError:rejected+=1
            else:raise ValueError('item/world mutation escaped oracle')
    return {'profile':profile,'source_sha':PINNED[profile],'cases_per_optimization':len(cases),'native_comparisons':2*len(cases),
       'semantic_mutations_rejected':rejected,'semantic_sha256':hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest()}


def main():
    p=argparse.ArgumentParser()
    for profile in PINNED:p.add_argument('--'+profile+'-dir',type=Path,required=True)
    args=p.parse_args();total=0
    for profile in PINNED:
        row=audit(profile,getattr(args,profile+'_dir'));total+=row['native_comparisons']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|exit_world_item_comparisons={total}|profiles=3')
    print('FACT|actual_item_end_retains_live_player_carried_aliases_but_ignores_pool_and_dead_player_references')
    print('FACT|gavin_iris_post_destroy_ticket_warp_can_move_retained_object_and_map_link_while_actor_coordinate_writes_fail')
    print('FACT|warp_returns_true_after_map_move_failure_object_coordinates_are_already_changed')
    print('FACT|Bismarck_map_recovers_misplaced_link_on_old_floor_ticket_guard_skips_destroyed_actor')
    print('BOUNDARY|complete_original_Exit_nonplayer_actual_item_end_warp_object_accessors_map_objmove_valid_object_indices_controlled_maps_and_hooks')
    print('OPEN|natural_enemy_ticket_object_initialization_allocator_execution_reuse_invalid_object_UB_player_cleanup_network_original_build_JSS_Taiwan_v1_runtime')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':main()
