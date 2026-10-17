"""Archived TW1 original executable audio callsite JSON: replay/custody negative gates."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"research/recovered/STONEAGE-TW10-AUDIO-EVENT-GATE-R1.json"
ACCEPTANCE=ROOT/"research/recovered/STONEAGE-TW10-AUDIO-EVENT-GATE-ACCEPTANCE-R1.json"
BLOB="67cc3707d45b6f079432b1db29b043851571b518"
RAW="ce1cd5738dac1a571999eea9ea6ee5ead86341f30bff4f0c4e4610a80f917047"
class OriginalAudioArchive(unittest.TestCase):
 def test_source_byte_identity(self):
  b=RESULT.read_bytes()
  self.assertEqual(len(b),11013)
  self.assertEqual(hashlib.sha256(b).hexdigest(),RAW)
  self.assertEqual(hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest(),BLOB)
  receipt=json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
  self.assertEqual(receipt["artifact"]["zip_sha256"],"b5a36f3fa0c42c01dc60fd6cff9f2d3dd21443606e546f6f4da38dbb5a180d4c")
  self.assertEqual(receipt["artifact"]["raw_report_git_blob"],BLOB)
  self.assertTrue(receipt["artifact"]["independently_downloaded_zip_and_raw_verified"])
 def test_actual_original_witness_and_no_scene_claims(self):
  d=json.loads(RESULT.read_text(encoding="utf-8"))
  z=d["compiled_audio_api_callsite_audit"]
  self.assertEqual(z["original_runtime_sha256"],"cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a")
  self.assertEqual(len(z["compiled_imported_audio_apis"]),7)
  self.assertEqual(z["native_import_use_site_count"],9)
  self.assertEqual(z["direct_callers_of_audio_import_thunks_total"],1)
  types={(x["import_dll"],x["import_function"]) for x in z["native_import_use_sites"]}
  self.assertIn(("DSOUND.dll","#1"),types)
  self.assertIn(("WINMM.dll","mmioOpenA"),types)
  self.assertFalse(d["original_audio_event_to_track_binding_certified"])
  self.assertFalse(d["gameplay_trigger_to_sound_file_or_bgm_selector_certified"])
  self.assertFalse(d["specific_original_village_music_attributed"])
  self.assertFalse(d["any_pet_sound_species_identity_certified"])
  self.assertFalse(d["original_audio_bytes_added_to_repo"])
  self.assertEqual(d["next"],"PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-03")
if __name__=="__main__":unittest.main()
