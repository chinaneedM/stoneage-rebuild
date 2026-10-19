import copy
import json
import unittest

from tools.stoneage_pirate_relic_guide import REPORT, extract, replay, validate


class PirateGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())

    @staticmethod
    def sample():
        # Synthetic clause fixture; not the original article or its core hash.
        parts=['2003-05-21 22:27 华义官方授权新浪石器',
          '海贼王遗迹任务(可一转做一次)', '推荐等级：LV100；',
          '1，不可思议的贝壳。2，解完海贼秘宝任务。',
          '鱼鳃草-使用后可在水底呼吸一小时”', '耐久力大概每分钟会减你总耐久力的1/30',
          '上述的时间为现实中的时间；一次总共可以在水底遨游两个小时',
          '在(181 322)遇到一只LV130的大白鲨', '从(54 17)进入，贝克(7 12)',
          '奇喀喀村(44 56)找到杰克森', '需要3只等级不能超过80的人龙(扬奇洛斯，邦奇诺，利则诺顿)',
          '需要30万石币的报酬或者是一瓶改点酒(必须是伏特加)',
          '两个海贼王宝箱的钥匙；杰克森会随机收走你身上的人龙',
          '拿着钥匙，再次来到海底，并打败守门的鲨鱼，就可以见到贝克，与其对话，展开战斗',
          '胜利后再次对话就会被传到下层开启宝箱了~。']
        return ''.join('<p>'+s+'</p>' for s in parts).encode('gb18030')

    def rejects(self,mutate):
        r=copy.deepcopy(self.report);mutate(r)
        with self.assertRaises(ValueError):validate(r)

    def test_eight_archive_records_and_five_stage_flow(self):
        validate(self.report)
        c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for r in self.report['records']:
            self.assertTrue(set(c['record_contract']['required'])<=r.keys())
            self.assertIn(r['collection'],c['required_collections'])
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),8)
        self.assertEqual(len(self.report['records'][0]['facts']['flow']),5)

    def test_parser_extracts_semantics_from_synthetic_clauses(self):
        got=extract(self.sample())
        self.assertEqual(got['facts'],self.report['inputs'][0]['extracted']['facts'])
        self.assertNotEqual(got['core_sha256'],self.report['inputs'][0]['extracted']['core_sha256'])

    def test_recommended_level_is_not_minimum_and_rebirth_not_reset_code(self):
        self.assertFalse(extract(self.sample())['facts']['recommendation_is_requirement'])
        self.rejects(lambda r:r['records'][0].__setitem__('minimum_character_level',100))
        self.rejects(lambda r:r['records'][0].__setitem__('reset_implementation','REBIRTH_FLAG'))

    def test_payment_is_pets_and_either_money_or_vodka(self):
        f=extract(self.sample())['facts']
        self.assertEqual(f['payment_alternatives'],[{'currency':'石币','amount':300000},{'item':'伏特加','quantity_as_written':'一瓶'}])
        self.rejects(lambda r:r['records'][4].__setitem__('payment_logic','PETS_AND_MONEY_AND_VODKA'))
        with self.assertRaises(ValueError):extract(self.sample().replace('或者是'.encode('gb18030'),'还需要'.encode('gb18030')))

    def test_pet_threshold_and_random_inventory_warning_both_retained(self):
        f=extract(self.sample())['facts'];self.assertEqual((f['pet_total'],f['pet_level_max_inclusive']),(3,80));self.assertTrue(f['random_pet_removal_warning'])
        self.rejects(lambda r:r['records'][4].__setitem__('quantity_per_pet_name',1))
        self.rejects(lambda r:r['records'][4].__setitem__('random_selection_filter','ONLY_MATCHING_LEVEL80_OR_LESS'))

    def test_timing_is_reported_approximation_not_original_timer(self):
        f=extract(self.sample())['facts'];self.assertEqual(f['breathing_duration_as_written'],'一小时');self.assertEqual(f['no_grass_hp_loss_per_real_minute_approx_fraction'],'1/30')
        self.assertIn('USE_ONE_THEN_REQUEST_ANOTHER',f['two_hour_explanation'])
        with self.assertRaises(ValueError):extract(self.sample().replace('上述的时间为现实中的时间'.encode('gb18030'),b'unknown'))

    def test_missing_referral_battle_and_handin_warning_rejected(self):
        for phrase in ['杰克森会随机收走你身上的人龙','并打败守门的鲨鱼','两个海贼王宝箱的钥匙']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):extract(self.sample().replace(phrase.encode('gb18030'),b'unknown'))

    def test_no_author_build_coordinate_or_reward_promotion(self):
        self.rejects(lambda r:r.__setitem__('authority','OFFICIAL_OPERATOR_SCRIPT'))
        for key,value in [('exact_region','CN'),('exact_client_build','6.0'),('portal_authorization_is_article_authorship',True),('source_coords_are_original_map_ids',True),('tw10_or_jss1999_backfill',True)]:
            self.rejects(lambda r:r['boundaries'].__setitem__(key,value))
        self.rejects(lambda r:r['records'][0].__setitem__('chest_contents',['金虎']))

    def test_snapshot_is_exact_bytes_and_not_second_witness(self):
        h=self.report['inputs'][1];self.assertEqual(h['capture_timestamp'],'20031204053709');self.assertEqual(h['http']['bytes'],29939)
        self.assertTrue(h['same_release_not_independent_witness'])
        with self.assertRaises(ValueError):replay(self.report,[self.sample(),self.sample()])
        with self.assertRaises(ValueError):replay(self.report,[self.sample()])

    def test_old_author_slot_and_new_submission_link_not_conflated(self):
        self.assertFalse(self.report['inputs'][1]['current_submission_link_present'])
        self.assertTrue(self.report['inputs'][0]['current_submission_link_present'])
        self.assertEqual(self.report['inputs'][0]['extracted'],self.report['inputs'][1]['extracted'])

    def test_permanent_replay_exact_hashes_and_head_scoped_custody(self):
        import hashlib
        receipt=json.loads((REPORT.parent/'STONEAGE-PIRATE-RELIC-CUSTODY-R1.json').read_text())
        saved=json.loads((REPORT.parent/'STONEAGE-PIRATE-RELIC-CI-REPLAY-R1.json').read_text())
        for pin in receipt['permanent_derived_files']:
            b=(REPORT.parents[2]/pin['path']).read_bytes()
            self.assertEqual((len(b),hashlib.sha256(b).hexdigest()),(pin['bytes'],pin['sha256']))
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin['git_blob'])
        self.assertEqual(saved['guide'],self.report['inputs'][0]['extracted'])
        self.assertFalse(saved['raw_html_or_images_in_output'])
        self.assertFalse(saved['original_server_execution_verified'])
        for group,count in [('candidate',10),('main',11)]:
            rows=receipt['validation'][group];self.assertEqual(len(rows),count)
            self.assertTrue(all(r['conclusion']=='success' and r['head']==receipt['content_commit']['sha'] for r in rows))


if __name__=='__main__':unittest.main()
