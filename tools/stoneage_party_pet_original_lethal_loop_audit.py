"""Experimental full original Loop->Command->Battling lethal-hit witness.

Accepted nonterminal and direct-lethal controls are preserved. Lethal-round
post-Finish state is observed but not claimed as terminal or profit closure.
"""
from __future__ import annotations
import hashlib
import re
import subprocess
import sys
from tools import stoneage_party_pet_original_attack_audit as attack


def observed_lethal_round() -> str:
    text = attack.ATTACK_OBSERVATIONS
    patches = (
        ("slots[enemy_actor].data[CHAR_HP]=500;", "slots[enemy_actor].data[CHAR_HP]=60;"),
        ("expected_round[enemy_actor].data[CHAR_HP]=427;", "expected_round[enemy_actor].data[CHAR_HP]=0;"),
        ("REAL_HEADER_ATTACK_ROUND|", "REAL_HEADER_LETHAL_LOOP|"),
        ("attack_round=1", "lethal_round=1"),
        ("enemy_damage=73", "enemy_hp_floor=0"),
        ("damage_executed=1", "lethal_hit_executed=1"),
        # Any post-hit turn and arena state is still OPEN. Record precise
        # effects before adding independent exact oracles.
        ('demand(battle->turn==1&&battle->mode==BATTLE_MODE_BATTLE,"complete nonterminal ordinary attack round turn1");',
         'printf("LETHAL_LOOP_MODE|mode=%d|arena=%d|turn=%d|battle_mode=%d|winside=%d\\n",mode,battle_at,battle->turn,battle->mode,battle->winside);fflush(stdout);'),
        ('demand(!memcmp(expected_round,slots,sizeof expected_round),"complete all seven attack-round actor snapshots");',
         'printf("LETHAL_ACTOR_DIFF|equal=%d\\n",!memcmp(expected_round,slots,sizeof expected_round));fflush(stdout);'),
        ('demand(!memcmp(&expected_round_arena,battle,sizeof(BATTLE)),"complete exact attack-round arena delta");',
         'printf("LETHAL_ARENA_DIFF|equal=%d\\n",!memcmp(&expected_round_arena,battle,sizeof(BATTLE)));fflush(stdout);'),
        ('demand(BATTLE_CommandWait(battle_at,0)==FALSE,"next original input waits");',
         'printf("LETHAL_NEXT_WAIT|skipped=1\\n");fflush(stdout);'),
        ('demand(strstr(szAllBattleString,attack_packet)!=NULL,"original ordinary physical output target damage flags");',
         'printf("LETHAL_PACKET_OBS|present=%d\\n",strstr(szAllBattleString,attack_packet)!=NULL);fflush(stdout);'),
        ('demand(slots[actor].data[CHAR_HP]==expected_round[actor].data[CHAR_HP],"exact single enemy physical damage");',
         'if(actor==enemy_actor)demand(slots[actor].data[CHAR_HP]==0,"original full-loop lethal HP floor");'),
        ('demand(BATTLE_Loop()==1,"all ready actual original ordinary attack dispatch");',
         'int full_loop_result=BATTLE_Loop();printf("LETHAL_LOOP_RET|value=%d\\n",full_loop_result);fflush(stdout);'),
        ('demand(round_sends-round_sends_before==live,"original battle output sent to four participants");',
         'printf("LETHAL_SENDS|count=%d|live=%d\\n",round_sends-round_sends_before,live);fflush(stdout);'),
    )
    for needle, replacement in patches:
        count = text.count(needle)
        if count != 1:
            raise ValueError("exact accepted attack observation drift "+needle+": "+str(count))
        text = text.replace(needle,replacement,1)
    # Do not let a pending terminal gate assert a known-nonterminal packet or
    # wait state. HP/DAMAGECOUNT checks persist; complete deltas are printed.
    return text


LETHAL_ROUND_OBSERVATIONS = observed_lethal_round()


def lethal_round_native(profile,source,battle,event,root):
    native,has_lua=attack.attack_native(profile,source,battle,event,root)
    anchor=attack.ATTACK_OBSERVATIONS.replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex",
    )
    if native.count(anchor)!=1:
        raise ValueError("accepted attack round driver drift")
    # Lethal Loop enters original AddProfit/AddExpItem; preserve the original
    # narrow CHAR_setMaxExp function body, not a fabricated level-up stub.
    char_source=attack.pp_file(profile,root,attack.LAYOUTS[profile]/"char/char_base.c")
    original_set_max_exp=attack.definition(char_source,"CHAR_setMaxExp")
    entry="int main(int argc,char **argv){"
    if native.count(entry)!=1:
        raise ValueError("original native main entry drift")
    original_pet_die=attack.definition(battle,"Pet_Check_Die")
    original_normal_dead=attack.definition(battle,"BATTLE_NormalDeadExtra")
    native=native.replace(entry,original_set_max_exp+"\n"+original_pet_die+"\n"+original_normal_dead+"\n"+entry,1)
    return native.replace(anchor,anchor+LETHAL_ROUND_OBSERVATIONS.replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex",
    ),1),has_lua


def main():
    attack.main(
        native_builder=lethal_round_native,
        extra_markers=("REAL_HEADER_LETHAL_LOOP|",),
    )
    print("BOUNDARY|original_full_loop_lethal_HP_only;finish_profit_not_proven")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_LETHAL_LOOP_HP_PASS")


if __name__=="__main__":
    main()
