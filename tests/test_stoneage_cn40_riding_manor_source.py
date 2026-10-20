import copy
import json
import unittest
from tools.stoneage_cn40_riding_manor_source import REPORT,Cells,decode_preserving_faults,extract,replay,validate


class ManorSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())
    def rejects(self,mutate):
        r=copy.deepcopy(self.report);mutate(r)
        with self.assertRaises(ValueError):validate(r)
    def test_thirteen_source_records_and_table_references(self):
        validate(self.report);c=json.loads((REPORT.parent/'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for row in self.report['records']:
            self.assertTrue(set(c['record_contract']['required'])<=row.keys());self.assertIn(row['collection'],c['required_collections'])
        self.assertEqual(len({r['record_id'] for r in self.report['records']}),13)
    def test_invalid_bytes_are_reversible_escapes_not_silently_replaced_or_fixed(self):
        raw=b'A\xb1\nB\xb1\n';text,issues=decode_preserving_faults(raw)
        self.assertEqual(text,'A'+chr(92)+'xb1\nB'+chr(92)+'xb1\n');self.assertEqual([x['offset'] for x in issues],[1,4])
        for bad in [b'valid',b'\xff\n\xb1\n',b'\xb1\n']:
            with self.assertRaises(ValueError):decode_preserving_faults(bad)
    def test_current_and_2002_share_two_source_faults_with_different_offsets(self):
        a,b=[x['extracted'] for x in self.report['inputs']]
        self.assertEqual([x['offset'] for x in a['encoding_issues']],[35589,35628]);self.assertEqual([x['offset'] for x in b['encoding_issues']],[17740,17779])
        self.assertEqual(a['manor_rows'],b['manor_rows']);self.assertEqual(a['core_sha256'],b['core_sha256'])
        self.assertIn(chr(92)+'xb1',a['manor_rows'][0]['mount_label_escaped'])
    def test_br_columns_preserve_leading_blanks_not_strip_them(self):
        p=Cells();p.feed('<table><tr><td>A<br>B</td><td><br>C</td></tr></table>')
        self.assertEqual(p.rows,[[['A','B'],['','C']]])
        rows=self.report['inputs'][0]['extracted']['manor_rows'];self.assertIsNone(rows[0]['closed_shop_as_written']);self.assertIsNone(rows[1]['closed_shop_as_written'])
        self.assertEqual(rows[2]['closed_shop_as_written'],'落马术');self.assertEqual(rows[0]['open_shop_as_written'],'无')
    def test_nine_manors_not_twelve_and_mount_mapping_positions(self):
        rows=self.report['records'][:9];self.assertEqual([r['source_row']['manor'] for r in rows],['萨姆吉尔','玛丽娜丝','加加','卡鲁它那','伊甸','塔耳塔','尼克斯','佛烈顿','亚伊欧'])
        self.assertEqual(rows[6]['source_row']['mount_main_name'],'扬奇洛斯')
        self.assertEqual(self.report['inputs'][0]['extracted']['facts']['advertised_mount_type_cap'],12)
        self.rejects(lambda r:r['boundaries'].__setitem__('twelve_mounts_means_twelve_manors',True))
    def test_certificate_use_claim_does_not_invent_consumption_or_rebirth_scope(self):
        self.assertEqual(self.report['records'][10]['manufacturers_as_written'],['族长','长老'])
        for key in ('survives_rebirth','consumed_on_use'):self.rejects(lambda r:r['records'][10].__setitem__(key,True))
    def test_special_teacher_and_shop_are_not_original_spawn_stock_or_recipe(self):
        self.assertEqual(self.report['records'][9]['rebirth_condition_as_written'],'五转人物')
        self.rejects(lambda r:r['records'][9].__setitem__('rebirth_predicate',{'ge':5}))
        self.rejects(lambda r:r['records'][9].__setitem__('coordinates',[1,2]))
        self.rejects(lambda r:r['records'][11].__setitem__('stock_quantities',[11]))
    def test_authority_date_old_formulas_and_runtime_stay_bounded(self):
        self.rejects(lambda r:r.__setitem__('authority','WAYI_ORIGINAL_SCRIPT'))
        for key,value in [('publication_date','2002-12-01'),('broken_aliases_repaired',True),('old_cn20_compatibility_or_combat_formula_overwritten',True),('original_server_execution_verified',True)]:self.rejects(lambda r:r['boundaries'].__setitem__(key,value))
    def test_partial_or_unpinned_inputs_fail(self):
        with self.assertRaises(ValueError):replay(self.report,[b''])
        with self.assertRaises(ValueError):extract(b'valid utf8 source')

    def test_candidate_main_downloaded_replay_and_immutable_source_custody(self):
        from hashlib import sha256,sha1
        c=json.loads((REPORT.parent/'STONEAGE-CN40-RIDING-CUSTODY-R1.json').read_text())
        self.assertEqual([len(c['runs'][k]) for k in ('candidate','main')],[11,12])
        for rows in c['runs'].values():
            self.assertTrue(all(r['head_sha']==c['content_head'] and r['conclusion']=='success' for r in rows))
        for pin in c['pins']:
            b=(REPORT.parents[2]/pin['path']).read_bytes();self.assertEqual(len(b),pin['bytes']);self.assertEqual(sha256(b).hexdigest(),pin['sha256']);self.assertEqual(sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest(),pin['git_blob'])
        raw=(REPORT.parent/'STONEAGE-CN40-RIDING-CI-REPLAY-R1.json').read_bytes()
        self.assertTrue(all(a['member_sha256']==sha256(raw).hexdigest() for a in c['artifacts']))
        self.assertEqual(json.loads(raw)['extracted'],[x['extracted'] for x in self.report['inputs']])
        self.assertTrue(c['malformed_bytes_preserved']);self.assertFalse(c['original_server_or_operator_author_verified']);self.assertFalse(c['raw_sources_committed'])


if __name__=='__main__':unittest.main()
