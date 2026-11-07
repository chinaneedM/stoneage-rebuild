import unittest
from pathlib import Path
import importlib.util

P=Path(__file__).resolve().parents[1]/'tools/stoneage_item07_patch129_item_alias_crosswalk.py'
s=importlib.util.spec_from_file_location('item07',P)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

class Item07(unittest.TestCase):
    def setUp(self):
        self.item={'schema':'stoneage.item06.mixed25_item_alias_pixels.r1','counts':{'strict':415,'absent':416},'aliases':[]}
        for a in range(416):self.item['aliases'].append({'alias':10000+a,'status':'absent'})
        for a in range(415):self.item['aliases'].append({'alias':20000+a,'status':'strict','rd_sha256':f'{a:064x}'})
        self.cols={'aa':{'rd_sha256':'f'*64,'bytes':'12'},'bb':{'rd_sha256':'0'*64,'bytes':'13'}, 'cc':{'rd_sha256':'1'*64,'bytes':'17'}}
    def row(self,alias,idx,cid):
        return {'profile':'PATCH129','logical_alias':str(alias),'source_index':str(idx),'physical_bitmapno':str(idx),'content_id':cid,'width':'40','height':'20','source_rd_status':'OK','catalog_rd_qualification':'SOURCE','record_sha256':'a'*64}
    def run_crosswalk(self, rows):
        rows += [{'profile':'OTHER'}]* (m.EXPECTED_REF_ROWS - len(rows)-20229+len([r for r in rows if r.get('profile')=='PATCH129']))
        n=sum(r.get('profile')=='PATCH129' for r in rows)
        rows += [self.row(99999,900000+i,'aa') for i in range(20229-n)]
        return m.crosswalk(self.item,rows,self.cols)
    def test_source_narrow_and_rd_identity(self):
        d=self.run_crosswalk([self.row(10000,4,'aa'),self.row(10000,5,'bb'),self.row(20000,6,'bb'),self.row(20001,7,'cc')])
        mapp={x['mixed25_item_image_alias']:x for x in d['aliases']}
        self.assertEqual(mapp[10000]['result'],'PATCH_MULTIPLE_RD_CANDIDATES')
        self.assertEqual(mapp[10001]['result'],'PATCH_NOT_IN_ALIAS_CATALOG')
        self.assertEqual(mapp[20000]['result'],'PATCH_SAME_RD_AS_MIXED25')
        self.assertEqual(mapp[20001]['result'],'PATCH_ONE_RD_CANDIDATE')
        self.assertEqual(len(d['aliases']),831)
    def test_reject_wrong_count(self):
        with self.assertRaises(AssertionError):m.crosswalk(self.item,[],self.cols,expected_rows=43632)
    def test_no_source_item_identity_promotion(self):
        d=self.run_crosswalk([])
        self.assertEqual(d['summary']['patch129_matched_aliases'],0)
        self.assertNotIn('item_name',d['aliases'][0])

if __name__=='__main__':unittest.main()
