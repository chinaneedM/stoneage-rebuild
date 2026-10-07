import unittest

from tools.stoneage_becomepig_attack_order_audit import analyze_texts


EVENT = r"""
static int BATTLE_AttackSeq(int attackindex,int defindex,int *pDamage,int *pGuardian,int opt){
  if(BATTLE_DuckCheck(attackindex,defindex)) return 2;
  *pGuardian=BATTLE_GuardianCheck(attackindex,defindex);
  if(*pGuardian!=-1){ int GuardianIndex=BATTLE_No2Index(0,*pGuardian); defindex = GuardianIndex; }
  BATTLE_CriticalCheck(attackindex,defindex);
  return 0;
}
int BATTLE_Attack(int battleindex,int attackNo,int defNo){
  int Guardian=-1,damage=0,toindex=0,defindex=0,opt=0;
  BATTLE_AttackSeq(0,toindex,&damage,&Guardian,opt);
  if(Guardian >= 0) defindex = BATTLE_No2Index(battleindex, Guardian);
  BATTLE_DamageSub(0,defindex,&damage,0,0);
  return 1;
}
BOOL BATTLE_Counter(int battleindex,int attackNo,int defNo){
  int Guardian=-2,damage=4;
  BATTLE_CounterCheck(0,0,0);
  BATTLE_AttackSeq(0,0,&damage,&Guardian,-1);
  damage *= 0.75;
  BATTLE_DamageSub(0,0,&damage,0,0);
  return TRUE;
}
"""

BATTLE = r"""
static int BATTLE_Battling(int battleindex){
  int ContFlg=1,k=0,defNo=1,attackNo=10,myside=1;
  BATTLE_TargetAdjust(battleindex,0,myside);
  ContFlg = BATTLE_Attack(battleindex, attackNo, defNo);
  BATTLE_AddProfit(battleindex,0);
  BATTLE_TargetAdjust(battleindex,0,myside);
  for(k=0; k < 5 && ContFlg == TRUE; k++){
    ContFlg = BATTLE_Counter(battleindex,attackNo,defNo);
  }
  if(COM == BATTLE_COM_S_BECOMEPIG && BATTLE_TargetCheck(battleindex, defNo)){
    int defindex = BATTLE_No2Index(battleindex, defNo);
  }
  return 0;
}
"""


class BecomePigAttackOrderAuditTests(unittest.TestCase):
    def test_expected_order_and_counter_guardian_distinction(self):
        facts = analyze_texts(BATTLE, EVENT)
        self.assertTrue(facts["attackseq_duck_guardian_remap_critical"])
        self.assertTrue(facts["main_attackseq_guardian_remap_damage"])
        self.assertTrue(facts["counter_check_attackseq_scale_damage"])
        self.assertFalse(facts["counter_caller_guardian_remap_between_seq_damage"])
        self.assertTrue(facts["dispatch_adjust_main_profit_readjust_counter_postpig"])
        self.assertTrue(facts["postpig_rechecks_target_then_resolves_defno"])

    def test_reordered_main_guardian_is_rejected(self):
        bad = EVENT.replace(
            "if(Guardian >= 0) defindex = BATTLE_No2Index(battleindex, Guardian);\n"
            "  BATTLE_DamageSub",
            "BATTLE_DamageSub(0,defindex,&damage,0,0);\n"
            "  if(Guardian >= 0) defindex = BATTLE_No2Index(battleindex, Guardian);\n"
            "  /* BATTLE_DamageSub */",
        )
        with self.assertRaises(ValueError):
            analyze_texts(BATTLE, bad)

    def test_counter_caller_guardian_remap_is_detected_not_silently_accepted(self):
        changed = EVENT.replace(
            "damage *= 0.75;",
            "defindex = BATTLE_No2Index(battleindex, Guardian);\n  damage *= 0.75;",
        )
        facts = analyze_texts(BATTLE, changed)
        self.assertTrue(facts["counter_caller_guardian_remap_between_seq_damage"])

    def test_postpig_before_counter_is_rejected(self):
        pre = """if(COM == BATTLE_COM_S_BECOMEPIG && BATTLE_TargetCheck(battleindex, defNo)){
    int defindex = BATTLE_No2Index(battleindex, defNo);
  }
  """
        moved = BATTLE.replace(pre, "").replace(
            "for(k=0; k < 5 && ContFlg == TRUE; k++){", pre + "for(k=0; k < 5 && ContFlg == TRUE; k++){"
        )
        with self.assertRaises(ValueError):
            analyze_texts(moved, EVENT)


if __name__ == "__main__":
    unittest.main()
