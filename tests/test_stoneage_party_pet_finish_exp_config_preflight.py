"""EXP and profile-scoped config preflight has no payout promotion."""
import unittest
from unittest.mock import patch
from hashlib import sha256
from tools.stoneage_party_pet_finish_exp_config_preflight import (
    analyse, CONFIG_OWNER, CONFIG_PATH, NAMES,
)
from tools.stoneage_party_pet_terminal_path_preflight import PREVIOUS_FINGERPRINTS

FAKE={
  "BATTLE_Finish":"static int BATTLE_Finish(int x){return BATTLE_GetProfit(x,0,0);}",
  "BATTLE_GetProfit":"int BATTLE_GetProfit(int x,int s,int n){return BATTLE_GetExpGold(x,s,n);}",
  "BATTLE_GetExpGold":"int BATTLE_GetExpGold(int x,int s,int n){return BATTLE_GetExp(n);}",
  "BATTLE_GetExp":"int BATTLE_GetExp(int n){CHAR_AddMaxExp(n,getBattleexp());return 0;}",
}
class SourceExpTests(unittest.TestCase):
 def audited(self,profile="gavin",data=None,cfg=None):
  data=FAKE.copy() if data is None else data
  cfg=cfg if cfg is not None else "unsigned int getBattleexp(void){return "+CONFIG_OWNER[profile]+".battleexp;}"
  with patch.dict(PREVIOUS_FINGERPRINTS[profile],{
    "BATTLE_Finish":sha256(data["BATTLE_Finish"].encode()).hexdigest(),
    "BATTLE_GetProfit":sha256(data["BATTLE_GetProfit"].encode()).hexdigest(),
  }):
   return analyse(profile,data,cfg)
 def test_getter_source_profile_is_versioned(self):
  for p,owner in CONFIG_OWNER.items():
   rec=self.audited(p)
   self.assertEqual(rec["original_exp_multiplier_owner"],owner)
   self.assertTrue(rec["getexp_uses_getBattleexp"])
 def test_cross_profile_getter_not_flattened(self):
  with self.assertRaisesRegex(ValueError,"getter drift"):
   self.audited("gavin",cfg="unsigned int getBattleexp(void){return gServerConfig.battleexp;}")
 def test_negative_reward_route_fail_closed(self):
  for name,bad in (
   ("BATTLE_Finish","BATTLE_GetProfit"),
   ("BATTLE_GetProfit","BATTLE_GetExpGold"),
   ("BATTLE_GetExpGold","BATTLE_GetExp"),
   ("BATTLE_GetExp","CHAR_AddMaxExp"),
  ):
   with self.subTest(name=name):
    d=FAKE.copy()
    d[name]=d[name].replace(bad,"ABSENT")
    with self.assertRaises(ValueError):self.audited(data=d)
 def test_existing_frozen_finish_hash_is_enforced(self):
  with self.assertRaisesRegex(ValueError,"previously accepted"):
   analyse("gavin",FAKE,"unsigned int getBattleexp(void){return config.battleexp;}")
 def test_exact_pin_schema_not_invented(self):
  self.assertEqual(set(CONFIG_PATH),{"gavin","bismarck"})
  self.assertEqual(len(NAMES),4)
if __name__=="__main__":unittest.main()
