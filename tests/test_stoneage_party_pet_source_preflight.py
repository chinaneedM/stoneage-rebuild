"""Structural guard regression tests; actual originals run in the CI source gate."""
import unittest

from tools.stoneage_party_pet_source_preflight import FUNCTIONS, classify, require


PET = """int BATTLE_PetDefaultEntry(int c,int b,int s) {
 int pno=CHAR_getInt(c,CHAR_DEFAULTPET),pindex,ret=0;
 if(pno==-1)return 0;
 pindex=CHAR_getCharPet(c,pno);
 if(CHAR_CHECKINDEX(pindex)&&!CHAR_getFlg(pindex,CHAR_ISDIE)&&CHAR_getInt(pindex,CHAR_HP)>0){
    if(BATTLE_NewEntry(pindex,b,s)){}else{ret=0;}
 }else{CHAR_setInt(c,CHAR_DEFAULTPET,-1);}
 return ret;
}"""
PARTY = """int BATTLE_PartyNewEntry(int c,int b,int s){
 int i,iRet,work;
 iRet=BATTLE_NewEntry(c,b,s);if(iRet)return iRet;
 CAflush(c);CDflush(c);iRet=BATTLE_PetDefaultEntry(c,b,s);
 if(iRet)return iRet;BATTLE_ClearGetExp(c);
 for(i=1;i<CHAR_PARTYMAX;i++){
   work=CHAR_getWorkInt(c,i+CHAR_WORKPARTYINDEX1);
   if(CHAR_getWorkInt(work,CHAR_WORKBATTLEMODE)!=0)continue;
   iRet=BATTLE_NewEntry(work,b,s);CAflush(work);CDflush(work);
   iRet=BATTLE_PetDefaultEntry(work,b,s);BATTLE_ClearGetExp(work);
 }
 return iRet;
}"""
EXP = """int BATTLE_ClearGetExp(int c){
 int i,pindex;
 if(CHAR_CHECKINDEX(c)==0)return 1;
 CHAR_setWorkInt(c,CHAR_WORKGETEXP,0);
 for(i=0;i<CHAR_MAXPETHAVE;i++){
  pindex=CHAR_getCharPet(c,i);
  if(CHAR_CHECKINDEX(pindex)==0)continue;
  CHAR_setWorkInt(pindex,CHAR_WORKGETEXP,0);
 }
 return 0;
}"""


def fixtures():
    return dict(zip(FUNCTIONS, (PET, PARTY, EXP)))


class SourcePreflightTests(unittest.TestCase):
    def test_gavin_fixed_loop(self):
        r = classify("gavin", fixtures())
        self.assertEqual(r["party_capacity_source"], "CHAR_PARTYMAX")
        self.assertEqual(r["runtime_party_pet_admission"], "OPEN")

    def test_bismarck_dynamic_final_guard(self):
        f = fixtures()
        f["BATTLE_PartyNewEntry"] = PARTY.replace(
            "i<CHAR_PARTYMAX", "i<getPartyNum(c)"
        ).replace(
            "!=0)continue", "!=BATTLE_CHARMODE_NONE&&CHAR_getWorkInt(work,CHAR_WORKBATTLEMODE)!=BATTLE_CHARMODE_FINAL)continue"
        )
        r = classify("bismarck", f)
        self.assertEqual(r["party_capacity_source"], "getPartyNum")

    def test_reject_no_owned_pet_clear(self):
        f = fixtures()
        f["BATTLE_ClearGetExp"] = EXP.replace(
            "CHAR_setWorkInt(pindex,CHAR_WORKGETEXP,0);", "/* not cleared */"
        )
        with self.assertRaises(ValueError):
            classify("gavin", f)

    def test_reject_no_default_pet(self):
        f = fixtures()
        f["BATTLE_PetDefaultEntry"] = PET.replace("CHAR_DEFAULTPET", "CHAR_UNUSED")
        with self.assertRaises(ValueError):
            classify("gavin", f)

    def test_reject_missing_party_index(self):
        f = fixtures()
        f["BATTLE_PartyNewEntry"] = PARTY.replace("i+CHAR_WORKPARTYINDEX1", "i")
        with self.assertRaises(ValueError):
            classify("gavin", f)

    def test_reject_wrong_profile(self):
        with self.assertRaises(ValueError):
            classify("iris", fixtures())

    def test_require_detects_missing_token(self):
        with self.assertRaises(ValueError):
            require("x", "abc", ("missing",))


if __name__ == "__main__":
    unittest.main()
