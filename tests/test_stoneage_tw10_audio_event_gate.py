"""Guard original TW1 audio resource metadata against invented scene/music attribution."""
import unittest
from tools.stoneage_tw10_audio_event_gate import audio_catalog, TARGET_DLLS
class OriginalAudioEventGate(unittest.TestCase):
 def test_fixed_audio_catalog_and_wrapper_differences(self):
  r=audio_catalog()
  self.assertEqual(r["indexed_sfx"],114)
  self.assertEqual(r["loose_sfx"],116)
  self.assertEqual(r["loose_bgm"],11)
  self.assertEqual(r["original_container_bytes"],3695418)
  self.assertEqual((r["identical_full_wave_pairs"],r["same_pcm_different_wrapper"],r["different_pcm_pairs"]),(107,1,6))
  self.assertEqual(len(r["metadata_variants"]),7)
  self.assertEqual(r["unindexed_sfx"],2)
 def test_import_report_is_source_only(self):
  q=audio_catalog()["old_preexisting_audio_imports"]
  self.assertEqual(len(q),7)
  self.assertEqual({x["dll"] for x in q},set(TARGET_DLLS))
  self.assertIn({"dll":"DSOUND.dll","name":"#1"},q)
if __name__=="__main__":unittest.main()
