"""Bounded original second Loop -> BATTLE_Finish dispatch candidate.

Preserves preceding full original lethal Loop, original FinishSet and all
source-profile-specific win conditions. No gameplay stubs or fabricated rewards.
"""
from __future__ import annotations
from tools import stoneage_party_pet_original_lethal_loop_audit as lethal
from tools import stoneage_party_pet_original_attack_audit as attack

FINISH_OBSERVATION = r"""
  int final_arena=BattleArray[battle_at].use;
  int final_total=Total_BattleNum;
  int final_mode=BattleArray[battle_at].mode;
  int final_winner=BattleArray[battle_at].winside;
  demand(final_arena&&final_mode==BATTLE_MODE_FINISH,"original lethal finish state before next Loop");
  demand(final_winner==EXPECTED_WIN_SIDE,"original pre-Finish winning side");
  int finish_loop_ret=BATTLE_Loop();
  printf("ORIGINAL_FINISH_NEXT_LOOP|arena=%d|ret=%d|use=%d|mode=%d|total_before=%d|total_after=%d|winner_before=%d|actor0_mode=%d|actor1_mode=%d\n",
    battle_at,finish_loop_ret,BattleArray[battle_at].use,BattleArray[battle_at].mode,
    final_total,Total_BattleNum,final_winner,
    slots[0].workint[CHAR_WORKBATTLEMODE],slots[1].workint[CHAR_WORKBATTLEMODE]);
  fflush(stdout);
  demand(BattleArray[battle_at].use==0,"original terminal arena released");
  demand(BattleArray[battle_at].mode==BATTLE_MODE_NONE,"original terminal arena mode NONE");
  demand(Total_BattleNum==final_total-1,"original terminal arena counter decremented");
  printf("REAL_HEADER_FINISH_DISPATCH|mode=%d|battle=%d|original_finish_loop=1|released=1\n",mode,battle_at);
  /* Only test-fixture normalization; no gameplay code is modified. The
     inherited accepted Exit control then performs its own teardown. */
  Total_BattleNum=final_total;
"""

def finish_observations(profile):
    script=lethal.LETHAL_ROUND_OBSERVATIONS
    anchor="memcpy(slots,round_baseline,sizeof round_baseline);*battle=round_arena;rng_count=round_rng;rng_mode=round_rng_mode;"
    if script.count(anchor)!=1:raise ValueError("accepted lethal round restoration anchor drift")
    sentinel="-1" if profile=="bismarck" else "0"
    return script.replace(anchor,FINISH_OBSERVATION+anchor,1).replace("EXPECTED_WIN_SIDE",sentinel)

def finish_native(profile,source,battle,event,root):
    native,has_lua=lethal.lethal_round_native(profile,source,battle,event,root)
    previous=lethal.LETHAL_ROUND_OBSERVATIONS.replace(
        "EXPECTED_WIN_SIDE","-1" if profile=="bismarck" else "0",
    ).replace("ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex")
    if native.count(previous)!=1:
        raise ValueError("accepted original lethal round body drift")
    native=native.replace(previous,finish_observations(profile).replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex"),1)
    bodies={}
    for n in ("BATTLE_Finish","BATTLE_GetProfit","BATTLE_GetExpGold"):
        bodies[n]=attack.definition(battle,n)
    anchor="int main(int argc,char **argv){"
    for n,body in bodies.items():
        try:prior=attack.definition(native,n)
        except ValueError:pass
        else:native=native.replace(prior,"",1)
        # Add exact original signature declaration for potentially earlier use.
        native=native.replace(anchor,body[:body.index("{")].strip()+";\n"+anchor,1)
    # Original BATTLE_Loop is defined before our source-body insert at main;
    # preserve the original static linkage by declaring Finish before its use.
    loop=attack.definition(native,"BATTLE_Loop")
    if native.count(loop)!=1:raise ValueError("original Loop body declaration anchor drift")
    signature=bodies["BATTLE_Finish"][:bodies["BATTLE_Finish"].index("{")].strip()+";"
    native=native.replace(loop,signature+"\n"+loop,1)
    native=native.replace(anchor,"\n".join(bodies.values())+"\n"+anchor,1)
    return native,has_lua

def main():
    attack.main(native_builder=finish_native,extra_markers=(
        "REAL_HEADER_LETHAL_LOOP|","LETHAL_LOOP_MODE|","ORIGINAL_FINISH_NEXT_LOOP|",
        "REAL_HEADER_FINISH_DISPATCH|",
    ))
    print("BOUNDARY|second_original_Finish_executed;positive_rewards_not_yet_verified")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_FINISH_DISPATCH_BOUNDED_PASS")

if __name__=="__main__":main()
