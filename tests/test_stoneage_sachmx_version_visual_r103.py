import copy
import hashlib
import io
import json
import unittest
from tools import stoneage_sachmx_version_visual_r103 as m

D=json.loads(m.SOURCE.read_text())

def fixture(edition):
    source=copy.deepcopy(next(s for s in D['articles'] if s['edition']==edition))
    source['review_sha256']=m.digest(b'SYNTHETIC_REVIEW_ONLY')
    values=dict(source['metadata'])
    abuse=m.COMMON_ABUSE if edition=='free' else [('unrestricted_level_claim','不限等')]+m.COMMON_ABUSE
    helps=m.COMMON_HELP if edition=='free' else m.COMMON_HELP+[('delivery_currency_script','自动送货赚石币脚本')]
    values['作弊功能']=''.join(str(i)+'.'+text for i,(_,text) in enumerate(abuse,1))
    values['辅助功能']=''.join(str(i)+'.'+text for i,(_,text) in enumerate(helps,1))
    if edition=='free':values['辅助功能']+='等等的辅助功能与收费的SACH-MX会员版里的功能大致相同'
    values['测试评价']='SYNTHETIC_REVIEW_ONLY'
    source['table_sha256']=m.digest(m.canonical({k:m.compact(v) for k,v in values.items()}))
    image=source['image']
    html='<h1>'+source['title']+'</h1><table><tr><td>作者：'+source['author']+'</td><td>'+source['display_date']+'</td><td>submission</td></tr></table><table>'
    for i,k in enumerate(m.LABELS):
        if i==0:
            row='<td><a href="'+image['original_href']+'"><img src="'+image['thumbnail']+'"></a></td><td>【'+k+'】</td><td>'+values[k]+'</td>'
        elif i<7:row='<td>【'+k+'】</td><td>'+values[k]+'</td>'
        else:row='<td>【'+k+'】'+values[k]+'</td>'
        html+='<tr>'+row+'</tr>'
    return html+'</table>',source

class SACHMXSource(unittest.TestCase):
    def test_valid_contract_and_versioned_research_records(self):
        m.validate_source(D)
        records=D['records']
        self.assertEqual(len(records),len({r['record_id'] for r in records}))
        self.assertEqual(len(records),22)
        self.assertEqual(sum(r['entity_type']=='helper_capability' for r in records),18)
        for r in records:
            self.assertTrue({'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}<=r.keys())
            self.assertIn(r['collection'],['helper_programs','helper_capabilities','screens'])
            self.assertIsNone(r['game_ids'])
            self.assertFalse(r['implemented_in_rebuild'])
            self.assertFalse(r['adoption_decided'])

    def test_independent_synthetic_tables_both_editions(self):
        for edition,n in [('member',10),('free',8)]:
            html,source=fixture(edition)
            result=m.parse_article(html.encode('gb18030'),source)
            self.assertEqual(sum(len(result[k]) for k in ['explicit_abuse_categories','explicit_assistance_categories']),n)
            self.assertFalse(result['edition_feature_list_complete'])
            self.assertFalse(result['review_is_benchmark'])

    def test_free_qualified_similarity_not_full_equivalence(self):
        html,source=fixture('free')
        html=html.replace('大致相同','完全相同')
        with self.assertRaisesRegex(ValueError,'meaning/order'):
            m.parse_article(html.encode('gb18030'),source,enforce_fingerprint=False)

    def test_missing_member_feature_not_repaired_outside_table_or_hidden(self):
        html,source=fixture('member')
        for repair in ['<p>1.不限等</p>','<script>1.不限等</script>','<span hidden>1.不限等</span>','<span style="display:none">1.不限等</span>']:
            altered=html.replace('1.不限等','')+repair
            with self.subTest(repair=repair), self.assertRaises(ValueError):
                m.parse_article(altered.encode('gb18030'),source,enforce_fingerprint=False)

    def test_feature_negation_and_versions_are_not_substring_matches(self):
        html,source=fixture('member')
        for old,new in [('自动登入','不能自动登入'),('任务脚本','不支持任务脚本'),('5.00B9会员版','6.00B9会员版'),('￥50/年','￥50/月'),('服务器端】</td><td>有','服务器端】</td><td>无')]:
            with self.subTest(old=old), self.assertRaises(ValueError):
                m.parse_article(html.replace(old,new).encode('gb18030'),source,enforce_fingerprint=False)

    def test_free_cannot_receive_member_unlisted_capabilities(self):
        html,source=fixture('free')
        html=html.replace('【辅助功能】','【辅助功能】5.自动送货赚石币脚本')
        with self.assertRaises(ValueError):m.parse_article(html.encode('gb18030'),source,enforce_fingerprint=False)

    def test_author_date_and_image_associations_are_bound(self):
        html,source=fixture('member')
        for old,new in [('作者：SACH-MX(万宇在线)','作者：新浪游戏'),('15:28','15:32'),(source['image']['original_href'],source['image']['thumbnail']),('sachmx5.00b9.JPG','sachmx6.00freeb1.JPG')]:
            with self.subTest(old=old), self.assertRaises(ValueError):
                m.parse_article(html.replace(old,new).encode('gb18030'),source,enforce_fingerprint=False)

    def test_duplicate_product_tables_are_ambiguous(self):
        html,source=fixture('member')
        table=html[html.rfind('<table>'):]
        with self.assertRaisesRegex(ValueError,'ambiguous'):
            m.parse_article((html+table).encode('gb18030'),source)

    def test_unrelated_page_wrapping_does_not_change_table_semantics(self):
        html,source=fixture('free')
        before=m.parse_article(html.encode('gb18030'),source)
        after=m.parse_article((html+'<script>advertisement</script><p>extra navigation</p>').encode('gb18030'),source)
        self.assertEqual(before,after)

    def test_index_links_policy_and_hidden_repair(self):
        links=''.join('<a href="'+s['original_url']+'">'+s['index_label']+'</a>' for s in D['articles'])
        policy='不提供外挂下载并且在截图资料中隐去了外挂网址'
        good=(policy+links).encode('gb18030')
        self.assertFalse(m.parse_index(good,D)['developer_homepage_obtained'])
        for bad in ['<script>'+policy+'</script>'+links, policy+links.replace('13364.shtml','99999.shtml'),policy+links+links]:
            with self.assertRaises(ValueError):m.parse_index(bad.encode('gb18030'),D)

    def test_image_integrity_and_full_decode_are_separate(self):
        from PIL import Image
        b=io.BytesIO();Image.new('RGB',(3,2)).save(b,format='JPEG');raw=b.getvalue()
        expected={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'format':'JPEG','mode':'RGB','size':[3,2],'frames':1}
        self.assertEqual(m.decode_image(raw,expected)['size'],[3,2])
        with self.assertRaisesRegex(ValueError,'bytes'):m.decode_image(raw+b'x',expected)
        expected['size']=[2,3]
        with self.assertRaisesRegex(ValueError,'decode'):m.decode_image(raw,expected)

    def test_runtime_or_completeness_promotion_rejected(self):
        for key in ['developer_release_or_author_identity_authenticated','software_or_scripts_executed','free_omissions_prove_feature_absence','complete_helper_genealogy_or_features_recovered','new_game_adoption_decided']:
            changed=copy.deepcopy(D);changed['boundaries'][key]=True
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,'contract'):m.validate_source(changed)

if __name__=='__main__':unittest.main()
