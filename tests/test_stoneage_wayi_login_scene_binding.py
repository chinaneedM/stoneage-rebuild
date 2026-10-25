import copy
import unittest
from tools import stoneage_wayi_login_scene_binding as m


def fixture(physical=376059,index=376059):
    row={'index':str(index),'bitmapno':str(physical),'adder':'100','size':'200',
         'xoff':'-320','yoff':'-240','width':'640','height':'480','map_number':'26301',
         'record_sha256':str(physical).zfill(64),'attr_sha256':'a'*64}
    native={k:v for k,v in row.items() if k!='map_number'}
    native.update(rd_status='HEADER_MATCH',rd_sha256='b'*64,rd_width='640',rd_height='480',rd_size='200')
    pair={'patch_index':str(index),'bitmapno':str(physical),'patch_record_sha256':row['record_sha256'],
          'native_exact_indices':str(index),'rd_status':'HEADER_MATCH','rd_sha256':'b'*64,
          'qualification':'EXACT_NATIVE_RECORD_AND_RD_STRUCTURE'}
    return row,native,pair


class LoginSceneBinding(unittest.TestCase):
    def test_alias_uses_attribute_and_preserves_physical_id(self):
        r,n,p=fixture();selected=m.select_aliases([r]);result=m.join(selected,[n],[p])
        self.assertEqual(result[0]['candidates'][0]['bitmapno'],376059)
        self.assertEqual(result[0]['candidates'][0]['static_draw_origin'],[0,0])
        self.assertFalse(result[0]['candidates'][0]['same_deployed_executable_build_proven'])

    def test_same_number_physical_row_is_not_a_logical_alias(self):
        r,_,_=fixture(26301);r['map_number']='0'
        self.assertEqual(m.select_aliases([r])[26301],[])

    def test_no_member_means_unresolved(self):
        result=m.join(m.select_aliases([]),[],[])
        self.assertTrue(all(r['candidate_count']==0 for r in result))
        self.assertTrue(all(r['selection']=='UNRESOLVED_PRESERVE_ALL_OCCURRENCES' for r in result))

    def test_duplicate_alias_candidates_are_not_last_wins(self):
        a,na,pa=fixture();b,nb,pb=fixture(376062,376062)
        result=m.join(m.select_aliases([a,b]),[na,nb],[pa,pb])
        self.assertEqual([r['bitmapno'] for r in result[0]['candidates']],[376059,376062])
        self.assertEqual(result[0]['selection'],'UNRESOLVED_PRESERVE_ALL_OCCURRENCES')

    def test_wrong_native_record_hash(self):
        r,n,p=fixture();n['record_sha256']='c'*64
        with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n],[p])

    def test_wrong_patch_occurrence(self):
        r,n,p=fixture();p['patch_index']='1'
        with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n],[p])

    def test_native_header_changes(self):
        for field in ('adder','size','xoff','yoff','width','height'):
            with self.subTest(field=field):
                r,n,p=fixture();n[field]=str(int(n[field])+1)
                with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n],[p])

    def test_rd_metadata_changes(self):
        for field,value in [('rd_status','HEADER_MISMATCH'),('rd_sha256','c'*64),
                            ('rd_width','639'),('rd_height','479'),('rd_size','199'),('attr_sha256','c'*64)]:
            with self.subTest(field=field):
                r,n,p=fixture();n[field]=value
                with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n],[p])

    def test_paired_real_hash_changes(self):
        r,n,p=fixture();p['rd_sha256']='d'*64
        with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n],[p])

    def test_unqualified_link(self):
        r,n,p=fixture();p['qualification']='SAME_NAME_ONLY'
        with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n],[p])

    def test_ambiguous_native_occurrences(self):
        r,n,p=fixture();n2=copy.deepcopy(n);n2['index']='376062'
        with self.assertRaises(ValueError):m.join(m.select_aliases([r]),[n,n2],[p])

    def test_fake_binary_not_admitted(self):
        with self.assertRaises(ValueError):m.build(b'MZ synthetic only')


if __name__=='__main__':unittest.main()
