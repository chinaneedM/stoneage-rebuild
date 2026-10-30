import json
import unittest
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-SCENE40-SINA-AXE-PLAYER-REPLAY-R1.json'
CUST=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-SCENE40-SOURCE-CUSTODY-R1.json'

class Scene40PinnedSource(unittest.TestCase):
    def setUp(self):
        self.source=json.loads(SRC.read_text(encoding='utf-8'))
        self.custody=json.loads(CUST.read_text(encoding='utf-8'))

    def test_exact_current_source_identity(self):
        s=self.source
        self.assertEqual((s['raw_bytes'],s['raw_sha256'],s['invalid_decoding_original_bytes']),
                         (36312,'d1fbdacdb50b9b31c0068e270d7026550ea6764f577cc9df3641d20df3432bfb',10))
        self.assertEqual(s['url_final'],s['url_requested'])
        self.assertEqual(s['raw_decoding'],'gb18030_surrogateescape_lossless')

    def test_three_player_guide_rows_not_original_item_master(self):
        s=self.source
        self.assertEqual([(x['preserved_mixed25_item_id_for_comparison'],x['player_guide_price']) for x in s['source_rows']],[(0,65),(4,105),(10,260)])
        self.assertEqual(s['source_row_count'],3)
        self.assertTrue(all(x['commercial_trade_executed'] is False and x['original_client_same_build_proven'] is False for x in s['source_rows']))

    def test_no_official_or_old_capture_fabrication(self):
        s=self.source
        self.assertEqual(s['genre'],'USER_CONTRIBUTED_GAME_GUIDE')
        self.assertIsNone(s['verified_original_publication_date'])
        self.assertIsNone(s['historical_exact_build_id'])
        self.assertEqual(s['new_official_rules'],0)
        self.assertIs(s['native_game_executed'],False)
        self.assertIs(s['original_html_in_public_git'],False)

    def test_failure_and_source_custody_remain_separate(self):
        a=self.custody
        self.assertEqual(a['first_source_attempt']['conclusion'],'failure')
        self.assertEqual(a['corrected_source_attempt']['conclusion'],'success')
        self.assertEqual(a['corrected_source_attempt']['source_html_sha256'],self.source['raw_sha256'])
        self.assertEqual(a['corrected_source_attempt']['artifact_zip_bytes'],922)
        self.assertFalse(a['parsed_player_contribution']['same_build_identity'])

if __name__=='__main__':
    unittest.main()
