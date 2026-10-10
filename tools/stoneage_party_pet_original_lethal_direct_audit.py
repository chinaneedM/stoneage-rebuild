"""Experimental direct lethal original attack, before victory/Finish composition.

Additive bounded native witness on the accepted original physical bodies.
Must not be interpreted as full-round victory, rewards, server or historical v1.
"""
from __future__ import annotations
from tools import stoneage_party_pet_original_attack_audit as attack

LETHAL_OBSERVATIONS=r"""
{
  Char lethal_baseline[7];memcpy(lethal_baseline,slots,sizeof lethal_baseline);
  BATTLE lethal_arena=*battle;
  int lethal_rng=rng_count,lethal_mode=rng_mode;
  for(int actor=0;actor<7;actor++){
    if(!slots[actor].use||CHAR_getWorkInt(actor,CHAR_WORKBATTLEINDEX)!=battle_at)continue;
    slots[actor].workint[CHAR_WORKBATTLECOM1]=BATTLE_COM_GUARD;
    slots[actor].workint[CHAR_WORKBATTLEMODE]=BATTLE_CHARMODE_C_OK;
    slots[actor].workint[CHAR_WORKSEQUENCEPOWER]=actor*100;
    if(actor==2)slots[actor].data[CHAR_MODAI]=100;
    (void)CHAR_complianceParameter(actor);
    if(actor==2)slots[actor].workint[CHAR_WORKFIXAI]=100;
    if(actor>=4)slots[actor].workint[CHAR_WORKTACTICS]=0;
  }
""" + attack.ATTACK_SETUP.replace(
  "slots[enemy_actor].data[CHAR_HP]=500;",
  "slots[enemy_actor].data[CHAR_HP]=60;",
) + r"""
  int before_count=slots[enemy_actor].data[CHAR_DAMAGECOUNT];
  rng_mode=2;
  int attack_result=BATTLE_Attack(battle_at,0,enemy_no);
  printf("LETHAL_DELTA|mode=%d|enemy=%d|hp=%d|count=%d|result=%d|battle_mode=%d\n",
      mode,enemy_actor,slots[enemy_actor].data[CHAR_HP],
      slots[enemy_actor].data[CHAR_DAMAGECOUNT]-before_count,attack_result,battle->mode);
  fflush(stdout);
  demand(slots[enemy_actor].data[CHAR_HP]==0,"original direct lethal HP floor");
  demand(slots[enemy_actor].data[CHAR_DAMAGECOUNT]==before_count+1,"original direct lethal damage count");
  printf("REAL_HEADER_LETHAL_DIRECT|mode=%d|battle=%d|enemy_hp=0|death_damage=1|Finish_executed=0\n",mode,battle_at);
  memcpy(slots,lethal_baseline,sizeof lethal_baseline);
  *battle=lethal_arena;rng_count=lethal_rng;rng_mode=lethal_mode;
}
"""

def lethal_native(profile,source,battle,event,root):
    native,has_lua=attack.attack_native(profile,source,battle,event,root)
    old=attack.ATTACK_OBSERVATIONS.replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex",
    )
    if native.count(old)!=1:
        raise ValueError("accepted original attack observation anchor drift")
    return native.replace(old,old+LETHAL_OBSERVATIONS.replace(
        "ENTRY_FIELD","char_index" if profile=="bismarck" else "charaindex",
    ),1),has_lua

def main():
    attack.main(native_builder=lethal_native,extra_markers=("REAL_HEADER_LETHAL_DIRECT|",))
    print("BOUNDARY|direct_original_lethal_attack_only;no_original_Finish_or_positive_profit")
    print("RESOLUTION|ORIGINAL_REAL_HEADER_PARTY_PET_DIRECT_LETHAL_BOUNDED_PASS")

if __name__=="__main__":
    main()
