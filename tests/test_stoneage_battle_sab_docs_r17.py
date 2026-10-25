"""R17 provenance-preserving documentation and raw Git continuity guards."""
import hashlib
import json
from pathlib import Path
import unittest
from tools.stoneage_battle_sab_crossversion_r17 import build, REPORT

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'docs/specs/STONEAGE-BATTLE-SAB-CROSSVERSION-R17.md'
OVERLAY=ROOT/'docs/continuity/BATTLE-SAB-R17-MATERIAL-20261025.md'
CLIENT_REGISTRY=ROOT/'docs/SOURCE-REGISTRY-CLIENT-RECOVERY-R1.md'
README=ROOT/'README.md'
CURRENT=ROOT/'docs/CURRENT-STATE.md'
ROADMAP=ROOT/'docs/RESTORATION-ROADMAP-R2.md'

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

class BattleSABDocsTests(unittest.TestCase):
    def test_preserved_current_entire_history(self):
        c=CURRENT.read_bytes()
        self.assertEqual(len(c),2680510)
        self.assertEqual(blob(c),'031c76a5a8e431f646853909bb2f2e11e6328cd2')
        self.assertEqual(blob(ROADMAP.read_bytes()),'c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2')
        self.assertIn(b'ORIGINAL-CHARACTER-CREATION-CONTENT-16',c[-30000:])
    def test_first_party_vs_secondary_notice_explicit(self):
        j=json.loads(REPORT.read_bytes())
        self.assertFalse(j['notice_context']['notice_is_original_2001_source_bytes'])
        self.assertFalse(j['notice_context']['same_file_proven'])
        self.assertNotEqual(j['notice_context']['attributed_download_names'],
                            j['notice_context']['actual_preserved_mixed_names'])
        text=SPEC.read_text()
        for needle in ('2015-12-21','2001-05-10','battlemap218.sab','battle218.sab',
                       '218/218','438','436','1608B','0B','原始','同构建'):
            self.assertIn(needle,text)
    def test_records_and_docs_consistency(self):
        self.assertEqual(json.loads(REPORT.read_bytes()),build())
        for p in (SPEC, OVERLAY, CLIENT_REGISTRY):
            t=p.read_text()
            for needle in ('564233902b10c60760d4f93b1ea65d4dd1469206',
                           '47157f638cce7023727035981da11f1faecc9c78',
                           'battle219.sab'):
                self.assertIn(needle,t)
        self.assertIn('BATTLE-SAB-R17-MATERIAL-20261025.md',README.read_text())
        self.assertIn('OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17',OVERLAY.read_text())
        self.assertIn('EARLY-OFFICIAL-SERVER-MASTER-DATA-SOURCE-18_OR_EXACT_DOWNLOAD_PAYLOAD_CARRIER',
                      OVERLAY.read_text())
    def test_original_sab_files_absent_from_git(self):
        # All retained domain evidence is metadata: 438 source paths and hashes,
        # not the commercial SAB payload or full copyrighted installed client.
        for row in json.loads(REPORT.read_bytes())['occurrences']:
            self.assertEqual(row['size'],804)
            self.assertFalse((ROOT/row['path']).is_file())

if __name__=='__main__':
    unittest.main()
