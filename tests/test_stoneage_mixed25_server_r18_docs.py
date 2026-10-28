"""R18 source-grade and historical-continuity document guards."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'docs/specs/STONEAGE-MIXED25-SERVER-FULL-CONSERVATION-R18.md'
OVERLAY=ROOT/'docs/continuity/MIXED25-SERVER-R18-MATERIAL-20261025.md'
SOURCE=ROOT/'docs/SOURCE-REGISTRY-CLIENT-RECOVERY-R1.md'
README=ROOT/'README.md'
CURRENT=ROOT/'docs/CURRENT-STATE.md'
ROADMAP=ROOT/'docs/RESTORATION-ROADMAP-R2.md'
REPORT=ROOT/'research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json'
def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

class R18Docs(unittest.TestCase):
    def test_preserve_entire_2680510_byte_current(self):
        c=CURRENT.read_bytes()
        self.assertGreaterEqual(len(c),2680510)
        # Preserve the full historical blob while allowing additive checkpoints.
        c=c[:2680510]
        self.assertEqual(blob(c),'031c76a5a8e431f646853909bb2f2e11e6328cd2')
        self.assertEqual(blob(ROADMAP.read_bytes()[:482245]),'c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2')
    def test_doc_source_origin_boundaries(self):
        spec=SPEC.read_text()
        for item in ('2245','2227','18','731424','10465523','2121','53','124',
                     '78e8260e89928df76513799511d45c14a9e24dfc',
                     '47157f638cce7023727035981da11f1faecc9c78',
                     'enemybase1.txt','group1.txt','ride.txt','不','同构建',
                     'OPERATOR_EVENT_QUEST','0B'):
            self.assertIn(item,spec)
    def test_additive_continuity_and_registry(self):
        self.assertIn('MIXED25-SERVER-R18-MATERIAL-20261025.md',README.read_text())
        self.assertIn('EARLY-OFFICIAL-NAMED-CONTENT-SOURCE-19',OVERLAY.read_text())
        self.assertIn('mixed25 server original-occurrence SHA correction',SOURCE.read_text())
        self.assertIn('0原件删除',README.read_text())
        r=json.loads(REPORT.read_bytes())
        self.assertEqual(len(r['all_server_occurrences']),2245)
    def test_original_scripts_not_committed(self):
        j=json.loads(REPORT.read_bytes())
        for x in j['all_server_occurrences']:
            self.assertFalse((ROOT/'gmsv/data'/x['path']).is_file())
        self.assertFalse(j['vocabulary_boundary']['source_is_clean_official_build'])

if __name__=='__main__':unittest.main()
