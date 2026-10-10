"""Original source ITEM_makeItem and ITEM_makeItemAndRegist in a bounded native
factory fixture. Uses the accepted allocator and original finish witnesses.
No proprietary source is stored: CI extracts pinned original bodies transiently.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from tools import stoneage_item_allocator_audit as allocator
from tools import stoneage_party_pet_original_attack_audit as attack

replace_once=allocator.replace_once
NAMES=("ITEM_makeItem","ITEM_makeItemAndRegist")
SOURCE=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-ITEM-FACTORY-SOURCE-R1.json"

def factory_originals(profile,root):
    source=attack.pp_file(profile,root,attack.LAYOUTS[profile]/"item/item.c")
    return {name:attack.definition(source,name) for name in NAMES}

CONTROL=r"""
static void factory_controls(int mode,BATTLE *arena){
 if(mode!=3)return; /* last terminal encounter: preserve the original allocator's static cursor across modes */
 ITEM_TYPE old_items[256];Char old_actors[7];BATTLE old_arena=*arena;
 memcpy(old_items,reward_items,sizeof old_items);
 memcpy(old_actors,slots,sizeof old_actors);
 TABLE_TYPE old_index[3];memcpy(old_index,allocator_table,sizeof old_index);
 int old_size=ITEM_SIZE,old_count=ITEM_COUNT,old_rng=rng_count,old_rng_mode=rng_mode;
 int old_lookups=lookup_count;
 memset(allocator_table,0,sizeof allocator_table);
 allocator_table[1].use=1;
 TABLE_PTR=allocator_table;TABLE_SIZE=3;
 ITEM_Item specimen;memset(&specimen,0,sizeof specimen);
 for(int j=0;j<DATA_FIELDS;j++)specimen.data[j]=100+4*j;
 specimen.data[ITEM_ID]=1;specimen.data[ITEM_LEAKLEVEL]=57;
 specimen.workint[ITEM_WORKCHARAINDEX]=-1;specimen.workint[ITEM_WORKOBJINDEX]=-1;
 strcpy(specimen.string[ITEM_NAME].string,"Factory");
 strcpy(specimen.string[ITEM_UNIQUECODE].string,"factory-bounded");
 FACTORY_SETUP
 FACTORY_TABLE_SNAPSHOT
 ITEM_Item table_snapshot=specimen;
 ITEM_TYPE pool_snapshot[256];memcpy(pool_snapshot,reward_items,sizeof pool_snapshot);
 Char actor_snapshot[7];memcpy(actor_snapshot,slots,sizeof actor_snapshot);
 BATTLE arena_snapshot=*arena;
 for(int run=0;run<2;run++){
  rng_mode=run;rng_count=0;
  ITEM_Item item;memset(&item,0xA5,sizeof item);
  demand(ITEM_makeItem(&item,1)==TRUE,"original valid item direct factory");
  ITEM_Item expected=specimen;
  for(int j=0;j<DATA_FIELDS;j++){
   int width=(j%5==0?0:(j%5==1?1:5));
   if(j==ITEM_ID||j==ITEM_LEAKLEVEL)width=0;
   int delta=run?(int)((double)(width+1)*1073741824.0/(RAND_MAX+1.0)):0;
   expected.data[j]=specimen.data[j]+delta;
  }
  expected.data[ITEM_LEAKLEVEL]=LEAK_EXPECTED;
  demand(!memcmp(&item,&expected,sizeof item),"original complete direct factory item bytes including strings work flags and every integer");
  demand(rng_count==DATA_FIELDS,"every integer field consumes original RAND including zero-width ranges");
  demand(!memcmp(reward_items,pool_snapshot,sizeof pool_snapshot)&&!memcmp(slots,actor_snapshot,sizeof actor_snapshot)&&!memcmp(arena,&arena_snapshot,sizeof arena_snapshot),"direct factory preserves pool actors and arena");
 }
 rng_mode=1;rng_count=0;
 ITEM_Item invalid;memset(&invalid,0x73,sizeof invalid);ITEM_Item rejected=invalid;
 demand(ITEM_makeItem(&invalid,-1)==FALSE&&!memcmp(&invalid,&rejected,sizeof invalid)&&rng_count==0,"invalid ID no write and no random consumption");
 demand(ITEM_makeItemAndRegist(-1)==-1&&rng_count==0,"invalid register no random consumption");
 demand(!memcmp(reward_items,pool_snapshot,sizeof pool_snapshot),"invalid factory and register leave whole pool unchanged");
 memset(reward_items,0,sizeof pool_snapshot);ITEM_SIZE=8;ITEM_COUNT=0;
 for(int j=0;j<256;j++)reward_items[j].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=-1;
 ITEM_TYPE expected_items[256];memcpy(expected_items,reward_items,sizeof expected_items);
 ITEM_Item registered=specimen;
 for(int j=0;j<DATA_FIELDS;j++){
  int width=(j%5==0?0:(j%5==1?1:5));
  if(j==ITEM_ID||j==ITEM_LEAKLEVEL)width=0;
  registered.data[j]=specimen.data[j]+(int)((double)(width+1)*1073741824.0/(RAND_MAX+1.0));
 }
 registered.data[ITEM_LEAKLEVEL]=LEAK_EXPECTED;
 expected_items[2].use=1;expected_items[2].ITEM_FIELD=registered;
 int id=ITEM_makeItemAndRegist(1);
 demand(id==2&&rng_count==DATA_FIELDS,"original register uses factory then next real allocator cursor two");
 demand(!memcmp(reward_items,expected_items,sizeof expected_items)&&ITEM_COUNT==1,"whole original generated and registered pool oracle");
 demand(!memcmp(slots,actor_snapshot,sizeof actor_snapshot)&&!memcmp(arena,&arena_snapshot,sizeof arena_snapshot),"registered factory keeps all seven actors and arena immutable");
 demand(!memcmp(&specimen,&table_snapshot,sizeof specimen),"factory template immutable");
 FACTORY_TABLE_ORACLE
 printf("REAL_HEADER_ITEM_FACTORY|mode=%d|table_path=TABLE_KIND|direct_trials=2|registered_index=%d|field_draws=%d|invalid_draws=0|leak_level=%d|whole_item_oracle=1|whole_actor_oracle=1|whole_arena_oracle=1|table_immutable=1\n",mode,id,DATA_FIELDS,LEAK_EXPECTED);
 /* Fixture restoration follows all complete comparisons, not a substitute for a terminal oracle. */
 memcpy(reward_items,old_items,sizeof old_items);memcpy(slots,old_actors,sizeof old_actors);
 memcpy(allocator_table,old_index,sizeof old_index);ITEM_SIZE=old_size;ITEM_COUNT=old_count;
 rng_count=old_rng;rng_mode=old_rng_mode;lookup_count=old_lookups;
}
"""

def factory_controls(profile):
    b=profile=="bismarck"
    setup=(r"""allocator_table[1].index=1;
 ITEM_gTable=factory_table;ITEM_sTableLen=2;
 memset(factory_table,0,sizeof factory_table);
 factory_table[1].item=specimen;
 for(int j=0;j<DATA_FIELDS;j++)factory_table[1].randomdata[j]=(j%5==0?0:(j%5==1?1:5));
 factory_table[1].randomdata[ITEM_ID]=factory_table[1].randomdata[ITEM_LEAKLEVEL]=0;""" if b else
 r"""allocator_table[1].itm=specimen;
 for(int j=0;j<DATA_FIELDS;j++)allocator_table[1].randomdata[j]=(j%5==0?0:(j%5==1?1:5));
 allocator_table[1].randomdata[ITEM_ID]=allocator_table[1].randomdata[ITEM_LEAKLEVEL]=0;""")
    oracle=(r"""demand(!memcmp(&factory_table[1],&expected_factory_table,sizeof expected_factory_table)&&
        ITEM_gIndex[1].index==1&&ITEM_gTable==factory_table,"indirect source table immutable and selected");""" if b else
 r"""demand(!memcmp(&allocator_table[1],&expected_factory_table,sizeof expected_factory_table),"complete direct source table immutable");""")
    text=allocator.item.substitutions(profile,CONTROL)
    subs={"TABLE_TYPE":"ITEM_Index" if b else "ITEM_table",
          "TABLE_PTR":"ITEM_gIndex" if b else "ITEM_tbl",
          "TABLE_SIZE":"ITEM_sIndexLen" if b else "ITEM_tblen",
          "FACTORY_SETUP":setup,
          "FACTORY_TABLE_SNAPSHOT":("ITEM_Table expected_factory_table=factory_table[1];" if b else "ITEM_table expected_factory_table=allocator_table[1];"),
          "FACTORY_TABLE_ORACLE":oracle,
          "TABLE_KIND":"indirect" if b else "direct",
          "DATA_FIELDS":"ITEM_DATA_ENUM_MAX" if b else "ITEM_DATAINTNUM",
          "LEAK_EXPECTED":"0" if b else "1"}
    for k,v in subs.items(): text=text.replace(k,v)
    return text

def factory_native(profile,source,battle,event,root):
    native,has_lua=allocator.allocator_native(profile,source,battle,event,root)
    bodies=factory_originals(profile,root)
    expected=json.loads(SOURCE.read_text())[profile]
    allocator.item.pet.player.validate_bodies(bodies,expected)
    for name,body in bodies.items():
        print(f"ITEM_FACTORY_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}",flush=True)
        try:previous=attack.definition(native,name)
        except ValueError:pass
        else:native=replace_once(native,previous,"")
    signatures="\n".join(b[:b.index("{")].strip()+";" for b in bodies.values())
    native=replace_once(native,"static Char slots[7];",signatures+"\nstatic Char slots[7];")
    declaration=("static ITEM_Table factory_table[2];ITEM_Table *ITEM_gTable=factory_table;static int ITEM_sTableLen=2;\n" if profile=="bismarck" else "")
    native=replace_once(native,"int main(int argc,char **argv){",
         declaration+"\n".join(bodies.values())+"\n"+factory_controls(profile)+"\nint main(int argc,char **argv){")
    field="char_index" if profile=="bismarck" else "charaindex"
    previous=allocator.item.item_observations(profile).replace("ENTRY_FIELD",field)
    with_allocator=replace_once(previous,"  reward_phase=0;",
                               "  reward_phase=0;\n  allocator_controls(mode,battle);")
    replaced=replace_once(with_allocator,"  allocator_controls(mode,battle);",
                          "  allocator_controls(mode,battle);\n  factory_controls(mode,battle);")
    native=replace_once(native,with_allocator,replaced)
    return native,has_lua

def main():
    attack.main(native_builder=factory_native,extra_markers=(
        "REAL_HEADER_FINISH_DISPATCH|","FINISH_RS_OBS|","REAL_HEADER_PLAYER_LEVEL|",
        "REAL_HEADER_PET_GROWTH|","REAL_HEADER_REWARD_ITEM|","REAL_HEADER_ITEM_ALLOCATOR|",
        "REAL_HEADER_ITEM_FACTORY|"))
    print("BOUNDARY|explicit synthetic templates and deterministic rand; original profile factories, initializer and real-header terminal control; not natural enemy loot or Taiwan-v1 original equivalence")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_ITEM_FACTORY_BOUNDED_PASS")

if __name__=="__main__":main()
