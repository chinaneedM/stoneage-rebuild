import copy,json,unittest
from tools.stoneage_jp2008_fukuuri_capture_source import REPORT,validate,extract,replay
class FukuuriSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(REPORT.read_text())
 def test_source_scope_and_archive_contract(self):validate(self.r)
 def test_name_count_not_complete_early_roster(self):
  self.assertEqual(self.r['facts']['reported_ordinal_pet_name'],'フクゥーリ')
  self.assertIsNone(self.r['records'][0]['original_species_master_index'])
  for k in ['original_tw10_roster_backfilled','original_jss1999_pet_number_inferred','all_200_species_names_verified','ordinal_number_is_native_species_id']:
   z=copy.deepcopy(self.r);z['boundaries'][k]=True
   with self.assertRaises(ValueError):validate(z)
 def test_capture_and_trade_must_not_be_swapped(self):
  z=copy.deepcopy(self.r);z['facts']['traded_or_other_method_counts']=True
  with self.assertRaises(ValueError):validate(z)
  z=copy.deepcopy(self.r);z['facts']['eligibility_method']='TRADED_PET'
  with self.assertRaises(ValueError):validate(z)
 def test_gash_external_prize_not_game_currency(self):
  z=copy.deepcopy(self.r);z['facts']['prize_external_platform_not_in_game']=False
  with self.assertRaises(ValueError):validate(z)
  z=copy.deepcopy(self.r);z['boundaries']['external_gash_points_are_game_currency']=True
  with self.assertRaises(ValueError):validate(z)
 def test_payout_and_source_history_not_proven(self):
  z=copy.deepcopy(self.r);z['facts']['distribution_actual_verified']=True
  with self.assertRaises(ValueError):validate(z)
  z=copy.deepcopy(self.r);z['source']['historical_original_html_sha256']='a'*64
  with self.assertRaises(ValueError):validate(z)
 def test_real_source_phrase_mutations_fail(self):
  phrases=['200種類目のペット「フクゥーリ」','捕獲以外の方法（トレード等）で入手した場合は対象外','1アカウントにつき1回']
  core=' '.join(['ガマニアデジタルエンターテインメント','デジパーク','サービス9周年目','ペットの種類が200種類を達成',
  '200種類目のペット「フクゥーリ」','2008年7月15日火曜日16時','2008年7月29日火曜日13時',
  '抽選で500名','100GASHポイント','捕獲以外の方法（トレード等）で入手した場合は対象外',
  '「GASH」ユーザーのみが対象','1アカウントにつき1回','8月5日17時頃'])
  original=('<html><body>メーカー発表文の内容をそのまま掲載しています'+core+'関連記事一覧へ</body></html>').encode()
  self.assertEqual(extract(original)['evidence_flags_checked'],13)
  for token in phrases:
   with self.subTest(token=token):
    with self.assertRaises(ValueError):extract(original.replace(token.encode(),b'REPLACED'))
  with self.assertRaises(ValueError):extract(b'<html>not a press release</html>')
  with self.assertRaises(ValueError):replay(self.r,b'<html>missing</html>')
if __name__=='__main__':unittest.main()
