"""Original appearance/ride tables and helpers, transient native bounded composition."""
from __future__ import annotations
import argparse
import ast
import hashlib
import itertools
import json
import operator
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_mdfyattack_source_audit import _definition
from tools.stoneage_becomepig_native_audit import _features, _assert_rows
from tools.stoneage_becomepig_preaudit import analyze_profile as source_audit
from tools import stoneage_becomepig_restore_audit as prior
from tools import stoneage_becomepig_badstatus_audit as badstatus

PIN_PATH=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-BECOMEPIG-LOOKUP-SOURCE-DOMAINS-R1.json'
FEATURES=('_NEW_RIDEPETS','_GM_METAMO_RIDE','_RIDE_CF','_ITEM_EQUITSPACE','_MO_IMAGE_EXTENSION')


def numeric_initializer(text):
    """Strictly interpret integer C initializer expressions, never evaluate code."""
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.LShift:operator.lshift,ast.BitOr:operator.or_,ast.BitAnd:operator.and_}
    def visit(node):
        if isinstance(node,ast.List):return [visit(v) for v in node.elts]
        if isinstance(node,ast.Constant) and type(node.value) is int:return node.value
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
            value=visit(node.operand)
            return -value if isinstance(node.op,ast.USub) else value
        if isinstance(node,ast.BinOp) and type(node.op) in ops:
            a,b=visit(node.left),visit(node.right)
            if type(a) is not int or type(b) is not int or (isinstance(node.op,ast.LShift) and not 0<=b<=30):
                raise ValueError('unsafe initializer arithmetic')
            return ops[type(node.op)](a,b)
        raise ValueError('noninteger source initializer')
    result=visit(ast.parse(text.replace('{','[').replace('}',']'),mode='eval').body)
    def check(value):
        if isinstance(value,list):
            for item in value:check(item)
        elif type(value) is not int or not -(1<<31)<=value<(1<<31):raise ValueError('initializer outside int32')
    check(result);return result


def array(text,name):
    match=re.search(r'\b(?:int|tagRide\w+)\s+'+re.escape(name)+r'\s*((?:\[[^\]]*\])+?)\s*=\s*\{',text)
    if not match:raise ValueError('missing selected array: '+name)
    start=match.end()-1;depth=0
    for end in range(start,len(text)):
        depth+=(text[end]=='{')-(text[end]=='}')
        if depth==0:
            declaration=text[match.start():end+1]+';'
            return declaration,numeric_initializer(text[start:end+1]),match.group(1)
    raise ValueError('unterminated source array')


def source_domain(name,root):
    base=root/LAYOUTS[name];includes=['-I',str(base/'include')]
    if name=='bismarck':includes+=['-I',str(root/'server/common'),'-I',str(root/'shared/lua51')]
    strip=lambda s:re.sub(r'^\s*#\s*include[^\n]*','',s,flags=re.M)
    # Default feature source, real animation macros, and real ride flag/MAXNOINDEX
    # defines. Other char_base declarations are unused transient CPP context.
    prefix='#include "version.h"\n#include "anim_tbl.h"\n'+strip(_text(base/'include/char_base.h'))+'\n'
    def pp(text):
        result=subprocess.run(['cpp','-P',*includes,'-'],input=prefix+strip(text),text=True,capture_output=True)
        if result.returncode:raise ValueError('lookup default preprocessing failed: '+result.stderr[-1500:])
        return result.stdout
    active=_features(name,root)
    data=pp(_text(base/'char/char_data.c'));ride=pp(_text(base/'char/char_base.c'))
    declarations={};tables={};bounds={}
    names=['CHAR_eqimagetbl','ridePetTable']
    if '_NEW_RIDEPETS' in active:names+=['RideCodeMode','RideNoList','RPlistMode']
    for key in names:
        declaration,rows,dims=array(data if key=='CHAR_eqimagetbl' else ride,key)
        declarations[key]=declaration;tables[key]=rows;bounds[key]=dims
    if bounds['CHAR_eqimagetbl']!='[][5]' or not all(len(row)==5 for row in tables['CHAR_eqimagetbl']):
        raise ValueError('equipment row width drift')
    bound=int(re.fullmatch(r'\[(\d+)\]',bounds['ridePetTable']).group(1))
    if len(tables['ridePetTable'])>bound or not all(len(row)==4 for row in tables['ridePetTable']):
        raise ValueError('static ride declaration overflow/shape drift')
    initialized=len(tables['ridePetTable'])
    tables['ridePetTable']+=[[0,0,0,0] for _ in range(bound-initialized)]
    functions={'CHAR_getNewImagenumberFromEquip':_definition(data,'CHAR_getNewImagenumberFromEquip')}
    maxno=0
    if '_NEW_RIDEPETS' in active:
        for fn in ('RIDEPET_getNOindex','RIDEPET_getPETindex','RIDEPET_getRIDEno'):functions[fn]=_definition(ride,fn)
        maxno=numeric_initializer(pp('int lookup_maxno = MAXNOINDEX;').split('int lookup_maxno =')[-1].strip().removesuffix(';'))
        if not all(len(row)==2 and len(row[0])==maxno for row in tables['RideNoList']):raise ValueError('dynamic ride row width drift')
        if not all(len(row)==2 for row in tables['RideCodeMode']) or not all(len(row)==3 for row in tables['RPlistMode']):raise ValueError('dynamic map shape drift')
    item=pp(_text(base/'include/item.h'))
    enum=re.search(r'typedef\s+enum\s*\{([^{}]*)\}\s*ITEM_CATEGORY\b',item,re.S)
    if not enum or not re.fullmatch(r'ITEM_FIST\s*=\s*0',enum.group(1).strip().split(',')[0].strip()):raise ValueError('original ITEM_FIST zero ordinal drift')
    files=('char/char_data.c','char/char_base.c','include/char_base.h','include/anim_tbl.h','include/item.h','include/version.h')
    identity={'source_sha':PINNED[name],'files':{p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in files},
              'functions':{fn:hashlib.sha256(_compact(body).encode()).hexdigest() for fn,body in functions.items()},
              'tables':{key:{'sha256':hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),
                             'declared_dimensions':bounds[key],'rows':len(rows)} for key,rows in tables.items()},
              'static_initialized_rows':initialized,'static_zero_filled_rows':bound-initialized,
              'maxnoindex':maxno,'item_fist':0,'equipment_index_argument':name=='bismarck','features':{f:f in active for f in FEATURES}}
    return {'functions':functions,'declarations':declarations,'tables':tables,'identity':identity}


def equipment(domain,index,base,category,belt,current):
    if domain['identity']['equipment_index_argument'] and domain['identity']['features']['_ITEM_EQUITSPACE'] and index!=-1 and belt:return current
    if category<0 or category>5:return -1
    for row in domain['tables']['CHAR_eqimagetbl']:
        if row[0]==base:
            if category==5:raise ValueError('excluded original matching-row category5 undefined access')
            return row[category]
    return -1


def pet_index(domain,pet,learn):
    return next((i for i,row in enumerate(domain['tables']['RideCodeMode']) if row[0]==pet and row[1]&learn),-1)


def player_index(domain,base):
    return next((row[1] for row in domain['tables']['RPlistMode'] if row[0]==base),-1)


def ride_number(domain,index,ti):
    rows=domain['tables']['RideNoList'];width=domain['identity']['maxnoindex']
    return rows[index][0][ti] if 0<=index<len(rows) and 0<=ti<width else -1


def handles(functions,body,status_tables,status_features,domain):
    c=badstatus.handles(functions,body,status_tables,status_features)
    for field in ('CHAR_EQBELT','CHAR_LOWRIDEPETS'):
        if field not in c:c[field]=450+('CHAR_EQBELT','CHAR_LOWRIDEPETS').index(field)
    c['ITEM_FIST']=domain['identity']['item_fist'];return c


def replace_once(source,old,new):
    if source.count(old)!=1:raise ValueError('independent harness adapter drift: '+old[:70])
    return source.replace(old,new)


def original_helpers(domain,name):
    code='typedef int ITEM_CATEGORY;\n'+domain['declarations']['CHAR_eqimagetbl']+'\n'
    if name=='bismarck':
        code+='int _CHAR_getItemIndex(char *file,int line,int index,int field){(void)file;(void)line;return CHAR_getItemIndex(index,field);}\n'
        code+='int _CHAR_getInt(char *file,int line,int index,int field){(void)file;(void)line;return CHAR_getInt(index,field);}\n'
    for fn,body in domain['functions'].items():
        code+='#define '+fn+' original_'+fn+'\n'+body+'\n#undef '+fn+'\n'
    args='int index,int base,int category' if name=='bismarck' else 'int base,int category'
    call='index,base,category' if name=='bismarck' else 'base,category'
    actor='index' if name=='bismarck' else 'mappingactor'
    code+='int CHAR_getNewImagenumberFromEquip('+args+'){event(4,'+actor+',category);return original_CHAR_getNewImagenumberFromEquip('+call+');}\n'
    if domain['identity']['features']['_NEW_RIDEPETS']:
        for fn,args,call,event in (('RIDEPET_getPETindex','int n,int code','n,code',5),('RIDEPET_getNOindex','int n','n',6),('RIDEPET_getRIDEno','int n,int ti','n,ti',7)):
            code+='int '+fn+'('+args+'){event('+str(event)+',0,0);return original_'+fn+'('+call+');}\n'
    return code


def ride_tables_c(domain):
    code='typedef struct {int rideNo,charNo,petNo,petId;} tagRidePetTable;\n'
    code+=domain['declarations']['ridePetTable']+'\n'
    if domain['identity']['features']['_NEW_RIDEPETS']:
        code+='#define MAXNOINDEX '+str(domain['identity']['maxnoindex'])+'\n'
        code+='typedef struct {int petNo,learnCode;} tagRideCodeMode;\ntypedef struct {int RideNo[MAXNOINDEX];int flg;} tagRideNoList;\ntypedef struct {int charNo,Noindex,sex;} tagRidePetList;\n'
        code+='\n'.join(domain['declarations'][key] for key in ('RideCodeMode','RideNoList','RPlistMode'))+'\n'
    return code


class Witness(badstatus.Witness):
    def __init__(self,name,c,v,status_tables,status_features,domain):
        super().__init__(name,c,v[:19],status_tables,status_features)
        self.v=v;self.domain=domain
        base,pbase,petold,self.category,self.learn,self.belt=v[19:]
        self.i['CHAR_BASEBASEIMAGENUMBER']=base
        self.ints[1]['CHAR_BASEBASEIMAGENUMBER']=pbase;self.ints[1]['CHAR_BASEIMAGENUMBER']=petold
        self.i['CHAR_LOWRIDEPETS']=self.learn

    def compliance(self,actor):
        i,w,f=self.ints[actor],self.works[actor],self.flags[actor]
        if actor==0 and not self.valid:return 0
        self.event(1,actor);self.event(2,actor)
        w.update({'CHAR_WORKATTACKPOWER':15,'CHAR_WORKDEFENCEPOWER':26,'CHAR_WORKQUICK':30,'CHAR_WORKARRANGEPOWER':40,'CHAR_WORKSEQUENCEPOWER':50})
        self.event(3,actor);i['CHAR_HP']=min(i['CHAR_HP'],100);i['CHAR_MP']=min(i['CHAR_MP'],80)
        if f['CHAR_ISDIE']:return 1
        old=i['CHAR_BASEIMAGENUMBER'];base=i['CHAR_BASEBASEIMAGENUMBER']
        category=self.category if self.eq>=0 else self.c['ITEM_FIST'];self.event(4,actor,category)
        new=equipment(self.domain,actor,base,category,self.belt,old)
        item=w['CHAR_WORKITEMMETAMO']>1000;npc=w['CHAR_WORKNPCMETAMO']>0
        if item or npc or i['CHAR_BECOMEPIG']>-1:new=old
        if old==100259 or (self.name=='bismarck' and old==100362):new=old
        if i['CHAR_WHICHTYPE']==2 and w['CHAR_WORKBATTLEMODE']!=0 and old==101428:new=old
        if i['CHAR_WHICHTYPE']==3:return 0
        if self.name!='bismarck' or i['CHAR_RIDEPET']==-1:self.setint(actor,'CHAR_BASEIMAGENUMBER',base if new==-1 else new)
        if not self.domain['identity']['features']['_NEW_RIDEPETS']:return 1
        if item or npc:return 0
        if i['CHAR_RIDEPET']!=-1:
            if actor!=0 or not self.owned:raise ValueError('invalid original rider excluded')
            found=False;petbase=self.ints[1]['CHAR_BASEBASEIMAGENUMBER']
            for ride,char,pet,_ in self.domain['tables']['ridePetTable']:
                if (char==i['CHAR_BASEIMAGENUMBER'] or char==base) and pet==petbase:
                    self.setint(actor,'CHAR_BASEIMAGENUMBER',ride);found=True;break
            self.event(5,0);ti=pet_index(self.domain,petbase,self.learn)
            if ti>=0:
                self.event(6,0);no=player_index(self.domain,base)
                if no>=0:
                    self.event(7,0);image=ride_number(self.domain,no,ti)
                    if image>=0:self.setint(actor,'CHAR_BASEIMAGENUMBER',image);found=True
            if not found:
                self.setint(actor,'CHAR_RIDEPET',-1);self.setint(actor,'CHAR_BASEIMAGENUMBER',base);self.event(20,actor);self.event(21,actor,self.c['CHAR_P_STRING_RIDEPET'])
        return 1

    def execute(self):
        action,validchar,validbattle,use,side,pos,*_=self.v
        if action==0:return self.compliance(0)
        if not validchar:return -101
        if not validbattle:return -102
        base=self.i['CHAR_BASEBASEIMAGENUMBER'];petbase=self.ints[1]['CHAR_BASEBASEIMAGENUMBER']
        if self.i['CHAR_BASEIMAGENUMBER']==101749 or self.w['CHAR_WORKFOXROUND']!=-1:
            self.setint(0,'CHAR_BASEIMAGENUMBER',base);self.w['CHAR_WORKFOXROUND']=-1
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
                if self.ints[1]['CHAR_BASEIMAGENUMBER']!=petbase:self.setint(1,'CHAR_BASEIMAGENUMBER',petbase);self.event(23,0,ord('K'))
                self.event(25,1);self.compliance(1);self.event(22,0,0)
            self.event(29,0)
        self.event(26,0);return 0


NAMES=('action','validchar','validbattle','use','side','pos','pig','old','eq','meta','ride','kind','dead','fox','fall',
       'petpig','pointermask','owned','seed','base','pbase','petold','category','learn','belt')


def fixture(**changes):
    v=dict(zip(NAMES,(0,1,1,1,0,0,180,100250,0,0,0,1,0,-1,0,180,3,1,73,100000,100800,100250,0,0,0)))
    v.update(changes)
    if v['action'] and v['kind']!=1:raise ValueError('nonplayer Exit excluded')
    if v['ride'] and (not v['owned'] or v['kind']!=1):raise ValueError('invalid rider excluded')
    return tuple(v[k] for k in NAMES)


def composition_vectors(domain):
    tables=domain['tables']
    bases=[row[0] for row in tables['CHAR_eqimagetbl']]+[-1,0,2000000]
    for base,category,belt,pig,kind,dead in itertools.product(bases,range(5),(0,1),(-1,180),(1,2,3),(0,1)):
        yield fixture(base=base,category=category,belt=belt,pig=pig,kind=kind,dead=dead)
        if kind==1:yield fixture(action=1,base=base,category=category,belt=belt,pig=pig,dead=dead)
    # Every physical static row, including declared zero-fill, is represented;
    # the inactive Bismarck caller remains inactive, never promoted via this set.
    for ride,base,pet,_ in tables['ridePetTable']:
        for pig,action in itertools.product((-1,180),(0,1)):
            yield fixture(action=action,base=base,pbase=pet,ride=1,pig=pig,category=1)
        yield fixture(base=2000000,pbase=pet,old=base,ride=1,pig=180)
    if domain['identity']['features']['_NEW_RIDEPETS']:
        allcode=(1<<domain['identity']['maxnoindex'])-1
        for base,_,_ in tables['RPlistMode']:
            for pet,code in tables['RideCodeMode']:
                for learn,action,pig in itertools.product((0,code,allcode,code^allcode,-1),(0,1),(-1,180)):
                    yield fixture(action=action,base=base,pbase=pet,learn=learn,ride=1,pig=pig,category=2)
    # Crossing timer/appearance/property/Exit guards with selected first/last/missing
    # rider pairs, without the invalid-rider domain or category5 matching rows.
    pairs=[(tables['ridePetTable'][0][1],tables['ridePetTable'][0][2]),
           (tables['ridePetTable'][-1][1],tables['ridePetTable'][-1][2]),(2000000,2000001)]
    if 'RideCodeMode' in tables:pairs.append((tables['RPlistMode'][0][0],tables['RideCodeMode'][0][0]))
    states=((0,1,1,1,0,0),(1,0,1,1,0,0),(1,1,0,1,0,0),(1,1,1,0,0,0),(1,1,1,1,-1,0),(1,1,1,1,0,0),(1,1,1,1,1,4))
    for (base,pet),meta,mask,dead,belt,(action,vc,vb,use,side,pos) in itertools.product(pairs,range(4),range(4),(0,1),(0,1),states):
        yield fixture(action=action,validchar=vc,validbattle=vb,use=use,side=side,pos=pos,
                      base=base,pbase=pet,learn=-1,ride=1,meta=meta,pointermask=mask,dead=dead,belt=belt,fox=2,fall=1)
    for base,old in itertools.product((bases[0],2000000),(100259,100362,101428,101749)):
        for kind,eq,owned in itertools.product((1,2,3),(-1,0),(0,1)):
            yield fixture(base=base,old=old,kind=kind,eq=eq,owned=owned,pig=-1,category=4)


def native_composition(name,functions,body,status_tables,status_features,c,domain):
    source=badstatus.native_source(name,functions,body,status_tables,status_features,c)
    source=replace_once(source,'static int clearing,petpig,pointermask,owned,seed;','static int clearing,petpig,pointermask,owned,seed,base,pbase,petold,category,learn,belt,mappingactor;')
    source=replace_once(source,'static struct {int charNo,petNo,rideNo;} ridePetTable[1];',ride_tables_c(domain))
    source=replace_once(source,'void CHAR_initcharWorkInt(int i){event(1,i,0);','void CHAR_initcharWorkInt(int i){mappingactor=i;event(1,i,0);')
    source=replace_once(source,'int CHAR_getItemIndex(int i,int f){(void)i;(void)f;return eqresult<0?-1:0;}',
                        'int CHAR_getItemIndex(int i,int f){(void)i;if(f==CHAR_EQBELT)return belt?0:-1;return eqresult<0?-1:0;}')
    source=replace_once(source,'int ITEM_getInt(int i,int f){(void)i;(void)f;return 7;}','int ITEM_getInt(int i,int f){(void)i;(void)f;return category;}')
    for stub in ('int RIDEPET_getPETindex(int n,int low){(void)n;(void)low;event(5,0,0);return ridekind==2?0:-1;}',
                 'int RIDEPET_getNOindex(int n){(void)n;event(6,0,0);return 0;}',
                 'int RIDEPET_getRIDEno(int n,int p){(void)n;(void)p;event(7,0,0);return 300002;}'):
        source=replace_once(source,stub,'')
    mapping='int CHAR_getNewImagenumberFromEquip('+('int index,' if name=='bismarck' else '')+'int base,int category){event(4,'+('index' if name=='bismarck' else '(base==100800?1:0)')+',category);return base==100800?base:eqresult;}\n'
    source=replace_once(source,mapping,original_helpers(domain,name))
    source=replace_once(source,'%d'*19+'"','%d'*25+'"')
    source=replace_once(source,'&petpig,&pointermask,&owned,&seed)==19)', '&petpig,&pointermask,&owned,&seed,&base,&pbase,&petold,&category,&learn,&belt)==25)')
    source=replace_once(source,'ridePetTable[0].charNo=ride==1?100000:-99;ridePetTable[0].petNo=100800;ridePetTable[0].rideNo=300001;',
                        'ints[0][CHAR_BASEBASEIMAGENUMBER]=base;ints[1][CHAR_BASEBASEIMAGENUMBER]=pbase;ints[1][CHAR_BASEIMAGENUMBER]=petold;ints[0][CHAR_LOWRIDEPETS]=learn;')
    return source


def helper_vectors(domain):
    tables=domain['tables'];bases=[row[0] for row in tables['CHAR_eqimagetbl']]+[-1,0,2000000]
    for index,base,category,belt in itertools.product((-1,0,1),bases,(-2,-1,0,1,2,3,4,5,6),(0,1)):
        try:value=equipment(domain,index,base,category,belt,100250)
        except ValueError:continue
        yield (0,index,base,category,belt,100250),value
    for key,action in (('ridePetTable',4),('CHAR_eqimagetbl',5)):
        for i,row in enumerate(tables[key]):
            for j,value in enumerate(row):yield (action,i,0,j,0,0),value
    if not domain['identity']['features']['_NEW_RIDEPETS']:return
    width=domain['identity']['maxnoindex'];pets=[row[0] for row in tables['RideCodeMode']]+[-1,0,2000000]
    for pet,learn in itertools.product(pets,list(range(1<<width))+[-1,-2]):
        yield (1,0,pet,learn,0,0),pet_index(domain,pet,learn)
    for base in [row[0] for row in tables['RPlistMode']]+[-1,0,2000000]:
        yield (2,0,base,0,0,0),player_index(domain,base)
    for index,ti in itertools.product(range(-2,len(tables['RideNoList'])+2),range(-2,width+2)):
        yield (3,index,0,ti,0,0),ride_number(domain,index,ti)
    for key,action in (('RideCodeMode',6),('RideNoList',7),('RPlistMode',8)):
        for i,row in enumerate(tables[key]):
            values=row[0]+[row[1]] if key=='RideNoList' else row
            for j,value in enumerate(values):yield (action,i,0,j,0,0),value


def native_helpers(domain,name):
    source='''#include <stdio.h>
#define arraysizeof(a) (sizeof(a)/sizeof((a)[0]))
#define CHAR_EQBELT 1
#define CHAR_BASEIMAGENUMBER 2
static int belt,current,mappingactor;
int CHAR_getItemIndex(int i,int f){(void)i;(void)f;return belt?0:-1;}
int CHAR_getInt(int i,int f){(void)i;(void)f;return current;}
void event(int a,int b,int c){(void)a;(void)b;(void)c;}
'''+ride_tables_c(domain)+original_helpers(domain,name)
    source+='int main(void){int action,index,base,category;while(scanf("%d%d%d%d%d%d",&action,&index,&base,&category,&belt,&current)==6){int out=-999;switch(action){\n'
    source+='case 0:out=CHAR_getNewImagenumberFromEquip('+('index,' if name=='bismarck' else '')+'base,category);break;\n'
    source+='case 4:{int row[]={ridePetTable[index].rideNo,ridePetTable[index].charNo,ridePetTable[index].petNo,ridePetTable[index].petId};out=row[category];break;}\ncase 5:out=CHAR_eqimagetbl[index][category];break;\n'
    if domain['identity']['features']['_NEW_RIDEPETS']:
        source+='case 1:out=RIDEPET_getPETindex(base,category);break;case 2:out=RIDEPET_getNOindex(base);break;case 3:out=RIDEPET_getRIDEno(index,category);break;\n'
        source+='case 6:out=category?RideCodeMode[index].learnCode:RideCodeMode[index].petNo;break;case 7:out=category==MAXNOINDEX?RideNoList[index].flg:RideNoList[index].RideNo[category];break;case 8:{int row[]={RPlistMode[index].charNo,RPlistMode[index].Noindex,RPlistMode[index].sex};out=row[category];break;}\n'
    return source+'}printf("%d\\n",out);}return 0;}\n'


def audit(name,root):
    source_audit(name,root);domain=source_domain(name,root)
    if domain['identity']!=json.loads(PIN_PATH.read_text())['profiles'][name]:raise ValueError('actual lookup source/default table identity drift')
    body,status_tables,status_identity=badstatus.source_domain(name,root)
    if status_identity!=json.loads(badstatus.PIN_PATH.read_text())['profiles'][name]:raise ValueError('original bad-status identity drift')
    functions,caller_identity=prior.original_functions(name,root)
    if caller_identity!=json.loads((PIN_PATH.parent/'STONEAGE-BECOMEPIG-RESTORATION-SOURCE-DOMAINS-R1.json').read_text())['profiles'][name]['functions']:
        raise ValueError('complete caller identity drift')
    c=handles(functions,body,status_tables,status_identity['features'],domain)
    hvs=list(helper_vectors(domain));payload=''.join(' '.join(map(str,v))+'\n' for v,_ in hvs);expected=[(value,) for _,value in hvs]
    for opt in ('-O0','-O2'):_assert_rows(prior.run_native(native_helpers(domain,name),payload,opt),expected,name+' actual lookup helpers/table census')
    vs=list(composition_vectors(domain));payload=''.join(' '.join(map(str,v))+'\n' for v in vs);expected=[]
    for v in vs:
        w=Witness(name,c,v,status_tables,status_identity['features'],domain);expected.append(w.row(w.execute()))
    source=native_composition(name,functions,body,status_tables,status_identity['features'],c,domain)
    for opt in ('-O0','-O2'):_assert_rows(prior.run_native(source,payload,opt),expected,name+' original lookup/badstatus/full caller composition')
    return {'profile':name,'lookup_and_table_cases_per_optimization':len(hvs),'composed_cases_per_optimization':len(vs),
            'optimizations':2,'identity':domain['identity']}


def main():
    parser=argparse.ArgumentParser()
    for name in PINNED:parser.add_argument('--'+name+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0;helper=0;composed=0
    for name in PINNED:
        r=audit(name,getattr(args,name+'_dir').resolve());helper+=2*r['lookup_and_table_cases_per_optimization'];composed+=2*r['composed_cases_per_optimization']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in r.items() if k!='identity'))
        print('SOURCE|profile='+name+'|domain_sha256='+hashlib.sha256(json.dumps(r['identity'],sort_keys=True,separators=(',',':')).encode()).hexdigest())
    total=helper+composed
    print(f'TOTAL|original_lookup_and_table_comparisons={helper}|complete_composition_comparisons={composed}|comparisons={total}')
    print('BOUNDARY|actual_default_equipment_static_ride_tables_active_dynamic_maps_and_helpers_complete_compliance_exit_badstatus_actual_status_maps')
    print('BOUNDARY|symbolic_ABI_controlled_item_presence_category_belt_stats_property_construct_network_ownership_PvE_slots0_or4')
    print('OPEN|category5_matching_lookup_row_UB_inactive_Bismarck_dynamic_ride_attack_order_timer_composition_broader_ownership_and_runtime')
    print('RESOLUTION|BECOMEPIG_BOUNDED_ORIGINAL_LOOKUP_AND_FULL_CALLER_COMPOSITION_PASS_ZERO_RUNTIME_PROMOTIONS')


if __name__=='__main__':main()
