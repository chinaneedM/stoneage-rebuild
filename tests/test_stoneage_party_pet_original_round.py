"""Exact original scheduler declarations and complete guard-round boundaries."""
import unittest
from unittest.mock import patch
from tools.stoneage_party_pet_original_round_audit import round_native,ROUND_OBSERVATIONS,EXIT_ANCHOR,definition
BODIES={'BATTLE_Battling':'static int BATTLE_Battling(int b){return BATTLE_Guard(b,0);}', 'BATTLE_Guard':'int BATTLE_Guard(int b,int a){return 0;}'}
DECL='''typedef struct {int charaindex;} BATTLE_CHARLIST;
typedef int (*FUNC)(const void*,const void*);
char szBattleString[512];
char *pszBattleTop,*pszBattleLast;
char szBadStatusString[1024];
int gWeponType;
float gDamageDiv;
int gItemCrushRate=400000;
enum {PETAI_MODE_NORMAL,PETAI_MODE_ESCAPE};
static int aBowW[50]={0};'''
EVENT='''float gBattleDamageModyfy;
int gBattleDuckModyfy;
int gBattleStausChange;
int gBattleStausTurn;
float gDuckPer;
int gCriper;
int gBattleBadStatusTbl[20];'''
BASE='''int BATTLE_ai_all(int battleindex,int side,int turn);
static int BATTLE_Battling(int b){abort();}
int main(int argc,char **argv){'''+EXIT_ANCHOR+'return 0;}'
class RoundTests(unittest.TestCase):
 def build(self,battle=DECL,base=BASE,profile='gavin'):
  with patch('tools.stoneage_party_pet_original_round_audit.ai_native',return_value=(base,False)),patch('tools.stoneage_party_pet_original_round_audit.round_originals',return_value=dict(BODIES)),patch('tools.stoneage_party_pet_original_round_audit.pp_file',return_value='int CHAR_CanCureFlg(int a,char*s){return 1;} char *strncatsafe(char*d,const char*s,const int n){return d;}'):
   return round_native(profile,'',battle,EVENT,'/tmp')[0]
 def test_complete_original_bodies_unchanged(self):
  native=self.build()
  for n,b in BODIES.items():self.assertEqual(definition(native,n),b)
  self.assertIn('typedef int (*FUNC)(const void*,const void*);',native)
 def test_scheduler_declaration_drift_rejected(self):
  with self.assertRaises(ValueError):self.build(battle=DECL.replace('BATTLE_CHARLIST','WRONG_LIST'))
 def test_original_table_drift_rejected(self):
  with self.assertRaises(ValueError):self.build(battle=DECL.replace('aBowW','WRONG_TABLE'))
 def test_previous_exit_anchor_required(self):
  with self.assertRaises(ValueError):self.build(base=BASE.replace(EXIT_ANCHOR,''))
 def test_complete_snapshot_and_true_round_oracles(self):
  for text in ('memcmp(expected_round,slots,sizeof expected_round)','memcmp(&expected_round_arena,battle,sizeof(BATTLE))','battle->turn==1','BATTLE_Loop()==1','next_wait=1','damage_executed=0'):
   self.assertIn(text,ROUND_OBSERVATIONS)
 def test_presentation_boundary_not_gameplay_stub(self):
  native=self.build()
  self.assertIn('round_sends++;return TRUE;',native)
  self.assertIn('static int BATTLE_Battling(int b){return BATTLE_Guard(b,0);}',native)
 def test_bismarck_output_preserves_macro_target_signature(self):
  native=self.build(profile='bismarck')
  self.assertIn('BOOL _BATTLE_CommandSend(int actor,char *s,char *file,int line)',native)
  self.assertNotIn('BOOL BATTLE_CommandSend(int actor,char *s)',native)
if __name__=='__main__':unittest.main()
