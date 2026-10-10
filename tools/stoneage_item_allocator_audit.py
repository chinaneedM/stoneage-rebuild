"""Pinned original item initializer, cursor/reuse and empty callback registries.

Controls run after the independently checked original terminal reward matrix.
Original gameplay bodies stay unchanged; templates/pools are explicit fixtures.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from tools import stoneage_party_pet_original_reward_item_audit as item
from tools import stoneage_party_pet_original_attack_audit as attack
replace_once=item.replace_once
NAMES=('_ITEM_initExistItemsOne','ITEM_CHECKITEMTABLE','ITEM_constructFunctable')

def original_parts(profile,root):
    text=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'item/item.c')
    names=NAMES+(('ITEM_setLUAFunction',) if profile=='bismarck' else ())
    return {n:attack.definition(text,n) for n in names}

CONTROLS=r'''
static void allocator_controls(int mode,BATTLE *arena){
 ITEM_TYPE saved_items[256],expected[256];Char saved_actors[7],expected_actors[7];BATTLE saved_arena=*arena;
 memcpy(saved_items,reward_items,sizeof saved_items);memcpy(saved_actors,slots,sizeof saved_actors);
 int saved_size=ITEM_SIZE,saved_count=ITEM_COUNT;
 TABLE_TYPE saved_table[3];memcpy(saved_table,allocator_table,sizeof saved_table);
 memset(allocator_table,0,sizeof allocator_table);allocator_table[1].use=1;
 TABLE_PTR=allocator_table;TABLE_SIZE=3;
 TABLE_TYPE table_oracle[3];memcpy(table_oracle,allocator_table,sizeof table_oracle);
 for(int a=0;a<2;a++){
  for(int j=0;j<CHAR_MAXITEMHAVE;j++)slots[a].indexOfExistItems[j]=-1;
  for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)slots[a].indexOfExistPoolItems[j]=-1;
 }
 memcpy(expected_actors,slots,sizeof expected_actors);
 memset(reward_items,0,sizeof reward_items);ITEM_SIZE=8;ITEM_COUNT=0;
 for(int j=0;j<256;j++)reward_items[j].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
 for(int j=1;j<8;j++)if(j!=2)reward_items[j].use=1;ITEM_COUNT=6;
 ITEM_Item template;memset(&template,0,sizeof template);template.data[ITEM_ID]=1;
 template.workint[ITEM_WORKCHARAINDEX]=-1;template.workint[ITEM_WORKOBJINDEX]=-1;
 strcpy(template.string[ITEM_NAME].string,"Allocator");strcpy(template.string[ITEM_UNIQUECODE].string,"bounded");
 for(int j=0;j<ITEM_LASTFUNCTION-ITEM_FIRSTFUNCTION;j++)template.functable[j]=(void*)allocator_controls;
 LUA_TEMPLATE
 ITEM_Item initialized=template;
 for(int j=0;j<ITEM_LASTFUNCTION-ITEM_FIRSTFUNCTION;j++)initialized.functable[j]=NULL;
 LUA_ORACLE
 memcpy(expected,reward_items,sizeof expected);
 int lookups=lookup_count,created=0,releases=0;
 demand(ITEM_CHECKITEMTABLE(-1)==0&&ITEM_CHECKITEMTABLE(0)==0&&ITEM_CHECKITEMTABLE(1)==1&&ITEM_CHECKITEMTABLE(2)==0&&ITEM_CHECKITEMTABLE(3)==0,"original table bounds and inactive ID controls");
 for(int j=0;j<3;j++){
  int ids[]={-1,3,2};template.data[ITEM_ID]=ids[j];ITEM_Item rejected=template;
  demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==-1,"original invalid template ID rejected");
  demand(!memcmp(&template,&rejected,sizeof template)&&!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==6&&lookup_count==lookups,"invalid ID preserves entire pool/template/count/lookup");
 }
 template.data[ITEM_ID]=1;ITEM_Item template_oracle=template;
 expected[2].use=1;expected[2].ITEM_FIELD=initialized;
 demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==2,"literal initial cursor allocation two");created++;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==7,"whole initial allocation pool oracle");
 _ITEM_endExistItemsOne(2,"allocator-fixture",1);releases++;expected[2].use=0;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==6,"whole released item retained bytes oracle");
 expected[2].use=1;
 demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==2,"original cursor wraps and reuses released two");created++;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==7,"whole reused pool oracle");
 for(int j=1;j<8;j++)reward_items[j].use=1;ITEM_COUNT=7;
 memcpy(expected,reward_items,sizeof expected);
 demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==-1,"original full pool rejected");
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==7,"full pool preserves whole pool and count");
 reward_items[4].use=reward_items[5].use=0;ITEM_COUNT=5;
 reward_items[4].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=1;
 reward_items[5].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=1;
 slots[1].indexOfExistItems[CHAR_STARTITEMARRAY]=4;slots[1].indexOfExistPoolItems[0]=5;
 memcpy(expected_actors,slots,sizeof expected_actors);memcpy(expected,reward_items,sizeof expected);
 expected[4].use=1;expected[5].use=1;expected[5].ITEM_FIELD=initialized;
 demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==5,"carried stale slot protected and pool-only stale slot reused");created++;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==6,"stale protection changes use without incrementing live counter");
 demand(!memcmp(expected_actors,slots,sizeof slots),"allocator preserves carried and pool references");
 _ITEM_endExistItemsOne(5,"allocator-fixture",1);releases++;expected[5].use=0;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==5&&slots[1].indexOfExistPoolItems[0]==5,"original release ignores warehouse reference");
 reward_items[6].use=0;ITEM_COUNT=4;memcpy(expected,reward_items,sizeof expected);
 expected[6].use=1;expected[6].ITEM_FIELD=initialized;
 demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==6,"original cursor continues after released five");created++;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==5,"whole continuing allocation oracle");
 for(int j=1;j<8;j++)reward_items[j].use=1;reward_items[1].use=0;ITEM_COUNT=6;
 memcpy(expected,reward_items,sizeof expected);expected[1].use=1;expected[1].ITEM_FIELD=initialized;
 demand(_ITEM_initExistItemsOne("allocator-fixture",1,&template)==1,"original cursor wraps past seven to one");created++;
 demand(!memcmp(expected,reward_items,sizeof expected)&&ITEM_COUNT==7,"whole final allocation oracle including reserved zero");
 int before_invalid_construct=lookup_count;ITEM_constructFunctable(-1);ITEM_constructFunctable(8);
 LUA_INVALID
 demand(lookup_count==before_invalid_construct,"invalid function table leaves registry lookup unchanged");
 demand(lookup_count-lookups==5*(1+ITEM_LASTFUNCTION-ITEM_FIRSTFUNCTION),"exact empty original native registry lookup count");
 demand(!memcmp(&template,&template_oracle,sizeof template)&&!memcmp(table_oracle,allocator_table,sizeof table_oracle),"entire original template and ID table immutable");
 demand(!memcmp(expected,reward_items,sizeof expected)&&!memcmp(expected_actors,slots,sizeof slots)&&!memcmp(&saved_arena,arena,sizeof saved_arena),"whole pool seven actors and arena allocator oracle");
 LUA_SENTINEL
 printf("REAL_HEADER_ITEM_ALLOCATOR|mode=%d|cursor_results=2,2,-1,5,6,1|invalid_ids=3|allocations=%d|releases=%d|lookup_delta=%d|function_slots=%d|empty_lua_fallback=LUA_ACTIVE|carried_protected=1|warehouse_reused=1|reserved_zero_preserved=1|whole_pool_oracle=1|whole_actor_oracle=1|whole_arena_oracle=1|template_immutable=1|table_immutable=1\n",mode,created,releases,lookup_count-lookups,ITEM_LASTFUNCTION-ITEM_FIRSTFUNCTION);
 /* Restore fixture domains only after all independent comparisons. Original
    function-static cursor is untouched and has naturally returned to one. */
 memcpy(reward_items,saved_items,sizeof saved_items);memcpy(slots,saved_actors,sizeof saved_actors);
 memcpy(allocator_table,saved_table,sizeof saved_table);ITEM_SIZE=saved_size;ITEM_COUNT=saved_count;
}
'''

def controls(profile):
    text=item.substitutions(profile,CONTROLS)
    b=profile=='bismarck'
    replacements={
      'TABLE_TYPE':'ITEM_Index' if b else 'ITEM_table',
      'TABLE_PTR':'ITEM_gIndex' if b else 'ITEM_tbl',
      'TABLE_SIZE':'ITEM_sIndexLen' if b else 'ITEM_tblen',
      'LUA_TEMPLATE':('for(int j=0;j<ITEM_LASTFUNCTION-ITEM_FIRSTFUNCTION;j++){template.lua[j]=(lua_State*)&ITEM_luaFunc;template.luafunctable[j]=(char*)&ITEM_luaFunc;}' if b else ''),
      'LUA_ORACLE':('for(int j=0;j<ITEM_LASTFUNCTION-ITEM_FIRSTFUNCTION;j++){initialized.lua[j]=NULL;initialized.luafunctable[j]=NULL;}' if b else ''),
      'LUA_INVALID':('demand(ITEM_setLUAFunction(-1,ITEM_FIRSTFUNCTION,"")==0&&ITEM_setLUAFunction(1,ITEM_FIRSTFUNCTION-1,"")==0&&ITEM_setLUAFunction(1,ITEM_LASTFUNCTION,"")==0,"original Lua invalid index and function bounds");' if b else ''),
      'LUA_SENTINEL':('ITEM_LuaFunc empty_lua;memset(&empty_lua,0,sizeof empty_lua);demand(!memcmp(&empty_lua,&ITEM_luaFunc,sizeof empty_lua),"whole complete empty Lua sentinel immutable");' if b else ''),
      'LUA_ACTIVE':'1' if b else '0',
    }
    for a,v in replacements.items():text=text.replace(a,v)
    return text

def allocator_native(profile,source,battle,event,root):
    native,has_lua=item.item_native(profile,source,battle,event,root)
    bodies=original_parts(profile,root)
    frozen=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-ITEM-ALLOCATOR-SOURCE-R1.json'
    item.pet.player.validate_bodies(bodies,json.loads(frozen.read_text())[profile])
    for n,b in bodies.items():
        print(f'ITEM_ALLOCATOR_SOURCE|{profile}|{n}|sha256={hashlib.sha256(b.encode()).hexdigest()}',flush=True)
        try:previous=attack.definition(native,n)
        except ValueError:pass
        else:native=replace_once(native,previous,'')
    decl=('static ITEM_Index allocator_table[3];ITEM_Index *ITEM_gIndex=allocator_table;static int ITEM_sIndexLen=3;ITEM_LuaFunc ITEM_luaFunc;\n' if profile=='bismarck' else 'static ITEM_table allocator_table[3];static ITEM_table *ITEM_tbl=allocator_table;static int ITEM_tblen=3;\n')
    signatures='\n'.join(b[:b.index('{')].strip()+';' for b in bodies.values())
    native=replace_once(native,'static Char slots[7];',signatures+'\nstatic void allocator_controls(int,BATTLE*);\nstatic Char slots[7];')
    native=replace_once(native,'int main(int argc,char **argv){',decl+'\n'+'\n'.join(bodies.values())+'\n'+controls(profile)+'\nint main(int argc,char **argv){')
    field='char_index' if profile=='bismarck' else 'charaindex'
    old=item.item_observations(profile).replace('ENTRY_FIELD',field)
    observed=replace_once(old,'  reward_phase=0;','  reward_phase=0;\n  allocator_controls(mode,battle);')
    native=replace_once(native,old,observed)
    return native,has_lua

def main():
    attack.main(native_builder=allocator_native,extra_markers=('REAL_HEADER_FINISH_DISPATCH|','FINISH_RS_OBS|','REAL_HEADER_PLAYER_LEVEL|','REAL_HEADER_PET_GROWTH|','REAL_HEADER_REWARD_ITEM|','REAL_HEADER_ITEM_ALLOCATOR|'))
    print('BOUNDARY|explicit_template_ID1_and_eight_slot_pool;unchanged_static_cursor;empty_native_and_Lua_registries;no_natural_reward_allocator_or_historical_promotion')
    print('RESOLUTION|ORIGINAL_REAL_HEADER_ITEM_ALLOCATOR_BOUNDED_PASS')
if __name__=='__main__':main()
