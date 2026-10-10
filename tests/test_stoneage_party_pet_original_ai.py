"""Original decision-body composition and fail-closed declaration drift."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_original_ai_audit import ai_native,AI_NAMES,AI_OBSERVATIONS,definition,EXIT_ANCHOR
AI='''struct B_AI_RESULT {int command;int target;};
static int BATTLE_ai_normal(int,int,BATTLE_ENTRY*,struct B_AI_RESULT*);
static int (*functbl[])(int,int,BATTLE_ENTRY*,struct B_AI_RESULT*)={0,BATTLE_ai_normal,};
int BATTLE_ai_all(int b,int s,int t){return BATTLE_ai_normal(t,b,0,0);}
enum {AI_ATT_EARTHAT=1,AI_ATT_WATERAT};
int GetSubdueAttribute(int i){return 1;}
typedef enum {B_AI_ATTACKMODE=1,B_AI_WAZAMODE0} B_AI_MODE;
static int BATTLE_ai_normal(int t,int c,BATTLE_ENTRY* e,struct B_AI_RESULT* r){return 1;}'''
BASE='''int BATTLE_ai_all(int b,int s,int t){abort();/* UNREACHED_ORIGINAL */}
int main(int argc,char **argv){'''+EXIT_ANCHOR+'return 0;}'
CHAR='''int CHAR_CHECKCHARWORKDATAINDEX(int i){return 1;}
char *_CHAR_getWorkChar(char*f,int l,int i,int e){return 0;}'''
BATTLE='int BATTLE_CanMoveCheck(int i){return 1;}'
UTIL='char *NPC_Util_GetStrFromStrWithDelim(char*s,char*q,char*b,int n){return b;}'
class OriginalAiTests(unittest.TestCase):
 def build(self,ai=AI,base=BASE,profile='gavin'):
  def pp(p,r,path):
   name=str(path)
   return ai if name.endswith('battle_ai.c') else CHAR if name.endswith('char_base.c') else UTIL
  with patch('tools.stoneage_party_pet_original_ai_audit.input_native',return_value=(base,False)),patch('tools.stoneage_party_pet_original_ai_audit.pp_file',side_effect=pp):
   return ai_native(profile,'',BATTLE,'','/tmp')[0]
 def test_original_bodies_and_declarations_preserved(self):
  native=self.build()
  for n in AI_NAMES:self.assertEqual(definition(native,n),definition(AI,n))
  self.assertEqual(definition(native,'BATTLE_CanMoveCheck'),definition(BATTLE,'BATTLE_CanMoveCheck'))
  self.assertIn('static int (*functbl[])(int,int,BATTLE_ENTRY*,struct B_AI_RESULT*)={0,BATTLE_ai_normal,};',native)
 def test_declaration_drift_rejected(self):
  with self.assertRaises(ValueError):self.build(ai=AI.replace('B_AI_MODE;','WRONG_MODE;'))
 def test_previous_ai_stub_required(self):
  with self.assertRaises(ValueError):self.build(base=BASE.replace('UNREACHED_ORIGINAL','CHANGED'))
 def test_exit_anchor_required(self):
  with self.assertRaises(ValueError):self.build(base=BASE.replace(EXIT_ANCHOR,''))
 def test_profiles_use_original_entry_field(self):
  self.assertIn('Entry[i].charaindex',self.build())
  self.assertIn('Entry[i].char_index',self.build(profile='bismarck'))
 def test_complete_oracles_and_no_round(self):
  for marker in ('scenario<8','memcmp(ai_expected,slots,sizeof ai_expected)','memcmp(&prepared_ai_arena,battle,sizeof(BATTLE))','rng_count==expected_rng','round_executed=0'):
   self.assertIn(marker,AI_OBSERVATIONS)
  self.assertNotIn('BATTLE_Loop(',AI_OBSERVATIONS)
  self.assertNotIn('BATTLE_Battling(',AI_OBSERVATIONS)
if __name__=='__main__':unittest.main()
