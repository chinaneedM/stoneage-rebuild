import copy
import json
import unittest
from tools.stoneage_scene06_evidence_guard import REPORT,validate
from tools.stoneage_private_scene_order_r6 import display_order,Native

class Scene06Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads(REPORT.read_text())
    def test_archived_source_receipt(self):self.assertTrue(validate(self.report))
    def test_promotions_and_unstated_stubs_rejected(self):
        for k in ('original_world_entered','original_client_launched','directdraw_executed',
                  'consumer_LoadBmp_stubbed_to_failure','runtime_alias_table_injected_from_unique_original_adrn'):
            with self.subTest(field=k):
                r=copy.deepcopy(self.report);r[k]=not r[k]
                with self.assertRaises(ValueError):validate(r)
    def test_wrong_order_and_unsigned_priority_rejected(self):
        for mutate in (lambda r:r['original_sorted_queue_numbers'].reverse(),
                       lambda r:r['controlled_queue'][0].update(priority=1),
                       lambda r:r['comparator_cases'][-1].__setitem__(-1,0),
                       lambda r:r['native_consumer_requested_bitmap_order'].pop(),
                       lambda r:r['unverified'].pop()):
            r=copy.deepcopy(self.report);mutate(r)
            with self.assertRaises(ValueError):validate(r)
    def test_no_private_payload(self):
        r=copy.deepcopy(self.report);r['sprites']={}
        with self.assertRaises(ValueError):validate(r)
    def test_queue_ranges_and_duplicates(self):
        for rows in ([{'queue_no':0,'priority':0}]*2,[{'queue_no':True,'priority':0}],
                     [{'queue_no':4096,'priority':0}],[{'queue_no':0,'priority':256}]):
            with self.assertRaises(ValueError):display_order(rows)
    def test_unqualified_commercial_code_rejected(self):
        with self.assertRaises(ValueError):Native(b'not original bytes')

if __name__=='__main__':unittest.main()
