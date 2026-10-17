import json,hashlib,unittest
from pathlib import Path
from tools.stoneage_tw10_map_content_collision_crosswalk import audit
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered/STONEAGE-TW10-MAP-CONTENT-COLLISION-R1.json"
A=ROOT/"research/recovered/STONEAGE-TW10-MAP-CONTENT-COLLISION-ACCEPTANCE-R1.json"
class OriginalMapCollisionArchived(unittest.TestCase):
 def test_exact_source(self):
  data=R.read_bytes()
  self.assertEqual(len(data),8494)
  self.assertEqual(hashlib.sha256(data).hexdigest(),"5efa5972fe68d38d0e85aad3c7e13d6c4cd588c0f1b81a5900ba79e8a6711dd9")
  self.assertEqual(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest(),"7d4d5d2cae224c093b3e85e8ef1bfc49b54c5981")
  self.assertEqual(json.loads(A.read_text(encoding="utf-8"))["zip_sha256"],"8d48e37f0eae58b7659e7315ef83ccffe95c36d8728b6fe76d68d7d0d1dab5a4")
 def test_replay_not_world_map(self):
  self.assertEqual(R.read_bytes(),(json.dumps(audit(),ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8"))
  d=json.loads(R.read_text(encoding="utf-8"))
  self.assertEqual([x["original_tw10_collision_map_numbers"] for x in d["partition_rows"]],[4571,1271,101,3343])
  self.assertEqual(d["tw10_retail_disc_concrete_field_map_files"],0)
  self.assertFalse(d["all_early_world_regions_restored"])
  self.assertFalse(d["original_server_npc_encounter_reward_data_connected"])
if __name__=="__main__":unittest.main()
