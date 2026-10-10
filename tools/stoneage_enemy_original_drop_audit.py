"""Bounded actual ENEMY_createEnemy nonzero drop, using original item factory,
original allocator and the inherited real-header second-Loop/Finish witness.

Master drop pairs are explicit synthetic cases. No claim about natural master
tables, JSS 1999 or Taiwan v1 server identity is made.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from tools import stoneage_item_factory_audit as factory
from tools import stoneage_party_pet_original_attack_audit as attack

replace_once=factory.replace_once
ROOT=Path(__file__).resolve().parents[1]
PINS=ROOT/"research/recovered/STONEAGE-ENEMY-ORIGINAL-DROP-SOURCE-R1.json"

CONTROL=r"""
 /* Source-faithful nonzero probability executes inside original ENEMY_createEnemy.
    Tests are made only after all preceding complete original battle oracles. */
 int master_items[10],master_probs[10],master_style=ENEMY_enemy[0].intdata[ENEMY_STYLE];
 int *master=ENEMY_enemy[0].intdata;
 for(int i=0;i<10;i++){
  master_items[i]=master[ENEMY_ITEM1+i];
  master_probs[i]=master[ENEMY_ITEMPROB1+i];
  master[ENEMY_ITEM1+i]=0;master[ENEMY_ITEMPROB1+i]=0;
 }
 master[ENEMY_STYLE]=0;
 ITEM_TYPE before_spawn[256];memcpy(before_spawn,reward_items,sizeof before_spawn);
 Char before_actors[7];memcpy(before_actors,slots,sizeof before_actors);
 BATTLE before_arena=*arena;
 int before_item_count=ITEM_COUNT, before_item_size=ITEM_SIZE;
 int before_lookups=lookup_count;
 int old_mode=rng_mode,old_count_rng=rng_count;
 rng_mode=0;rng_count=0;
 int zero_actor=ENEMY_createEnemy(0,2);
 demand(zero_actor>=4&&zero_actor<7&&CHAR_CHECKINDEX(zero_actor),"real enemy zero-drop creation valid");
 int zero_draws=rng_count;
 demand(!memcmp(reward_items,before_spawn,sizeof before_spawn)&&ITEM_COUNT==before_item_count,
        "zero-probability master table emits no item and preserves entire original item pool");
 for(int i=0;i<10;i++)demand(slots[zero_actor].indexOfExistItems[CHAR_STARTITEMARRAY+i]==-1,
        "all ten zero probability carried slots remain empty");
 for(int i=0;i<7;i++)if(i!=zero_actor)demand(!memcmp(&before_actors[i],&slots[i],sizeof(Char)),
        "zero-drop enemy creation leaves all six other original actors intact");
 demand(!memcmp(&before_arena,arena,sizeof before_arena),
        "zero-drop enemy creation preserves complete prior arena");
 master[ENEMY_ITEM1]=1;master[ENEMY_ITEMPROB1]=1000;
 Char positive_before[7];memcpy(positive_before,slots,sizeof positive_before);
 ITEM_TYPE positive_items[256];memcpy(positive_items,reward_items,sizeof positive_items);
 rng_mode=0;rng_count=0;
 int positive_actor=ENEMY_createEnemy(0,2);
 demand(positive_actor>=4&&positive_actor<7&&positive_actor!=zero_actor&&CHAR_CHECKINDEX(positive_actor),
        "real positive-drop enemy allocates distinct live actor");
 demand(rng_count==zero_draws+1+DATA_FIELDS,
        "one native probability RAND plus every native item integer-field RAND");
 demand(slots[positive_actor].indexOfExistItems[CHAR_STARTITEMARRAY]==3,
        "real enemy carries original next static-cursor allocated item three");
 for(int i=1;i<10;i++)demand(slots[positive_actor].indexOfExistItems[CHAR_STARTITEMARRAY+i]==-1,
        "zero other original enemy item fields");
 ITEM_Item created=specimen;created.data[ITEM_LEAKLEVEL]=LEAK_EXPECTED;
 created.workint[ITEM_WORKCHARAINDEX]=positive_actor;
 created.workint[ITEM_WORKOBJINDEX]=-1;
 positive_items[3].use=1;positive_items[3].ITEM_FIELD=created;
 demand(ITEM_COUNT==before_item_count+1&&ITEM_SIZE==before_item_size,
        "original positive enemy factory increments one real item object");
 demand(!memcmp(positive_items,reward_items,sizeof positive_items),
        "whole 256 original item array matches one created, registered and carried object");
 for(int i=0;i<7;i++)if(i!=positive_actor)demand(!memcmp(&positive_before[i],&slots[i],sizeof(Char)),
        "positive-drop enemy creation preserves all other original actors including zero-drop actor");
 demand(!memcmp(&before_arena,arena,sizeof before_arena),
        "positive-drop enemy creation preserves complete previous battle arena");
 FACTORY_TABLE_ORACLE
 demand(!memcmp(&specimen,&table_snapshot,sizeof specimen),
        "original enemy drop does not mutate factory master template");
 printf("REAL_HEADER_ENEMY_POSITIVE_DROP|mode=%d|zero_prob_actor=%d|positive_actor=%d|item=3|item_id=1|positive_prob=1000|zero_draws=%d|positive_draws=%d|factory_draws=DATA_FIELDS|leak=%d|whole_item=1|whole_actor_others=1|whole_arena=1|source_table_immutable=1\n",
        mode,zero_actor,positive_actor,zero_draws,rng_count,LEAK_EXPECTED);
 /* Restore all fixture domains only after checking full original state.
    Original allocator static cursor/character sequence are never rewound. */
 memcpy(reward_items,before_spawn,sizeof before_spawn);
 memcpy(slots,before_actors,sizeof before_actors);
 for(int i=0;i<10;i++){
  master[ENEMY_ITEM1+i]=master_items[i];master[ENEMY_ITEMPROB1+i]=master_probs[i];
 }
 master[ENEMY_STYLE]=master_style;
 ITEM_SIZE=before_item_size;ITEM_COUNT=before_item_count;
 lookup_count=before_lookups;rng_mode=old_mode;rng_count=old_count_rng;
"""

def source_bodies(profile,root):
    enemy=attack.pp_file(profile,root,attack.LAYOUTS[profile]/"char/enemy.c")
    return {"ENEMY_createEnemy":attack.definition(enemy,"ENEMY_createEnemy")}

def extra_controls(profile):
    s=factory.allocator.item.substitutions(profile,CONTROL)
    expected=(r"""demand(!memcmp(&factory_table[1],&expected_factory_table,sizeof expected_factory_table)&&
        ITEM_gIndex[1].index==1&&ITEM_gTable==factory_table,"indirect source table immutable and selected");""" if profile=="bismarck"
        else r"""demand(!memcmp(&allocator_table[1],&expected_factory_table,sizeof expected_factory_table),"complete direct source table immutable");""")
    for key,value in (
        ("FACTORY_TABLE_ORACLE",expected),
        ("DATA_FIELDS","ITEM_DATA_ENUM_MAX" if profile=="bismarck" else "ITEM_DATAINTNUM"),
        ("LEAK_EXPECTED","0" if profile=="bismarck" else "1"),
    ):
        s=s.replace(key,value)
    return s

def positive_drop_native(profile,source,battle,event,root):
    native,has_lua=factory.factory_native(profile,source,battle,event,root)
    actual=source_bodies(profile,root)
    pins=json.loads(PINS.read_text())["source_functions_sha256"][profile]
    factory.allocator.item.pet.player.validate_bodies(actual,pins)
    for name,body in actual.items():
        native_body=attack.definition(native,name)
        import re
        # Raw inherited function preserves RAND(...) whereas the separate
        # pinned original source view macro-expands RAND. Verify ordered
        # probability/creation/ownership symbols without conflating text forms.
        symbols=("ENEMY_ITEMPROB1","ENEMY_ITEM1","ITEM_makeItemAndRegist",
                 "CHAR_setItemIndex","ITEM_setWorkInt","ITEM_WORKCHARAINDEX",
                 "ITEM_WORKOBJINDEX")
        pattern=r"\\b(?:"+"|".join(symbols)+r")\\b"
        original_calls=re.findall(pattern,body)
        inherited_calls=re.findall(pattern,native_body)
        if original_calls!=inherited_calls or len(original_calls)<10:
            raise ValueError("enemy original drop branch structure drift "+profile+" "+str((original_calls,inherited_calls)))
        digest=hashlib.sha256(native_body.encode()).hexdigest()
        expected_inherited=json.loads(PINS.read_text()).get("inherited_native_sha256",{}).get(profile)
        if expected_inherited and digest!=expected_inherited:
            raise ValueError("inherited original enemy raw-body drift "+profile)
        print("ENEMY_ORIGINAL_DROP_SOURCE|"+profile+"|"+name+
              "|preprocessed_sha256="+hashlib.sha256(body.encode()).hexdigest()+
              "|inherited_raw_sha256="+digest+"|ordered_drop_symbols="+str(len(inherited_calls)),flush=True)
    anchor='  demand(!memcmp(&specimen,&table_snapshot,sizeof specimen),"factory template immutable");'
    native=replace_once(native,anchor,anchor+"\n"+extra_controls(profile))
    return native,has_lua

def main():
    attack.main(native_builder=positive_drop_native,extra_markers=(
        "REAL_HEADER_FINISH_DISPATCH|","FINISH_RS_OBS|","REAL_HEADER_PLAYER_LEVEL|",
        "REAL_HEADER_PET_GROWTH|","REAL_HEADER_REWARD_ITEM|","REAL_HEADER_ITEM_ALLOCATOR|",
        "REAL_HEADER_ITEM_FACTORY|","REAL_HEADER_ENEMY_POSITIVE_DROP|"))
    print("BOUNDARY|synthetic source-shaped 10-pair item master; original enemy creation and item factory with zero versus guaranteed-drop RNG, not verified natural drop data, no original JSS/Taiwan server identification")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_ENEMY_POSITIVE_DROP_BOUNDED_PASS")

if __name__=="__main__":main()
