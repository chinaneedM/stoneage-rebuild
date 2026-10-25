"""Evidence-grade documentation and source custody acceptance for creation R16."""
import copy
import json
from pathlib import Path
import unittest
from tools.stoneage_tw10_character_creation_r16_acceptance import verify, PATH

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/'research/recovered/STONEAGE-TW10-CREATION-BODY-SOURCE-CUSTODY-R16.json'
SPEC=ROOT/'docs/specs/STONEAGE-TW10-CHARACTER-CREATION-BODY-SOURCE-R16.md'
OVERLAY=ROOT/'docs/continuity/CHARACTER-CREATION-R16-MATERIAL-20261025.md'
REGISTRY=ROOT/'docs/SOURCE-REGISTRY-CLIENT-RECOVERY-R1.md'
README=ROOT/'README.md'

def require(x, message):
    if not x:raise ValueError(message)

def check(doc):
    require(doc['schema']=='stoneage.tw10.character_creation.body_source_publication.r16','receipt schema drift')
    b=doc['start_remote']
    require(b['head']=='fa97b026893e8285f619ee907af60c55aaaff85a' and b['tree']=='eb3170e2481533e9c525c8ff46c1e7069ff5a26d','fresh source head drift')
    require(b['current_bytes']==2680510 and b['current_blob']=='031c76a5a8e431f646853909bb2f2e11e6328cd2','historical CURRENT original corrupted')
    d=doc['derived']
    require(d['source_run']==40195712866 and d['source_job']==121175972333 and d['source_status']=='completed/success','original source Action not genuine')
    require(d['artifact_id']==12600325678 and d['zip_bytes']==1670 and d['zip_sha256']=='368a7b3ed200f5164835e1ac68ca50c3e67eb32ac712fa0438c4f4faadfa5e6c','original ZIP provenance drift')
    require(d['source_json_bytes']==12876 and d['source_json_sha256']=='03be7a2c14f71c96c8114156c7189d836d99b805895510edf453ae9f706d7a59','raw derived report identity drift')
    require(d['archived_git_blob']=='4e0d8bddf6ee9e9de372b0b484d3489796007726','permanent derived Git source changed')
    require(d['archive_status']=='completed/success' and d['archive_run']==40196456122 and d['archive_commit']=='5ee3a6d213ce8ca47237bc4160f80b92782c7719','archive act not completed')
    require(doc['check']['source_join_run']==40196161564 and doc['check']['candidate_acceptance_run']==40196651280,'candidate CI receipts drift')
    require(doc['discoveries']['sourced_candidate_group_ids']==list(range(100000,100240,20)),'original SPR key sequence drift')
    require(doc['discoveries']['next_dword']==198,'raw numeric boundary drift')
    require(doc['discoveries']['number_of_selectable_characters'] is None and doc['discoveries']['original_roster_verified'] is False,'unproven character population promoted')
    require(doc['policies']['raw_exe_committed'] is False and doc['policies']['raw_visuals_committed'] is False and doc['policies']['full_current_untouched'] is True,'copyright or history safety drift')
    require(doc['policies']['percent'] is None and doc['policies']['stage_b']=='GATED','false historical completion')
    require(doc['next']=='OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17','next exceeded finite original content package')
    return doc

class DocumentationReceiptTests(unittest.TestCase):
    def test_all_primary_source_hashes_replay(self):
        self.assertEqual(verify()['matching_consecutive_spr_group_keys'],12)
    def test_custody_schema(self):
        check(json.loads(RECEIPT.read_bytes()))
    def test_reject_fake_historical_character_count(self):
        x=json.loads(RECEIPT.read_bytes())
        x['discoveries']['number_of_selectable_characters']=12
        with self.assertRaises(ValueError):check(x)
    def test_reject_unsafe_original_binary_commit(self):
        x=json.loads(RECEIPT.read_bytes())
        x['policies']['raw_exe_committed']=True
        with self.assertRaises(ValueError):check(x)
    def test_docs_have_boundaries_and_main_safe_overlay(self):
        spec=SPEC.read_text()
        overlay=OVERLAY.read_text()
        registry=REGISTRY.read_text()
        readme=README.read_text()
        for text in (spec,overlay,registry):
            self.assertIn('100220',text)
            self.assertIn('198',text)
            self.assertIn('03be7a2c14f71c96c8114156c7189d836d99b805895510edf453ae9f706d7a59',text)
            self.assertIn('4e0d8bddf6ee9e9de372b0b484d3489796007726',text)
        self.assertIn('CURRENT-STATE.md',overlay)
        self.assertIn('Stage A',spec)
        self.assertIn('DD-028',registry)
        self.assertIn('docs/continuity/CHARACTER-CREATION-R16-MATERIAL-20261025.md',readme)
        self.assertIn('original_character_count',PATH.read_text())
    def test_no_historical_current_replacement(self):
        current=(ROOT/'docs/CURRENT-STATE.md').read_bytes()
        self.assertGreaterEqual(len(current),2680510)
        self.assertIn(b'ORIGINAL-CHARACTER-CREATION-CONTENT-16',current[-30000:])

if __name__=='__main__':unittest.main()
