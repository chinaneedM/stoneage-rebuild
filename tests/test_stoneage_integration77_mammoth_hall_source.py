"""Public derived-only conservation for the mixed25 original Mammoth Hall static source.

This deliberately cannot execute or certify private original game assets or runtime.
"""
import json
from collections import Counter
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-INTEGRATION77-MAMMOTH-HALL-ORIGINAL-SOURCE-R1.json'

class MammothHallSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DATA.read_text(encoding='utf-8'))

    def test_source_custody(self):
        d=self.d
        self.assertEqual(d['source_carrier']['zip_size_bytes'],995176)
        self.assertEqual(d['source_carrier']['zip_sha256'],'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(d['source_carrier']['zip_members'],2205)
        self.assertEqual(d['source_carrier']['zip_crc_verified'],2205)
        self.assertIn('community mixed25',d['source_carrier']['source_scope'])

    def test_creation_conservation(self):
        d=self.d;b=d['creation_blocks']
        self.assertEqual(len(b),19)
        self.assertEqual([x['n'] for x in b],list(range(1,20)))
        self.assertEqual(Counter(x['floor'] for x in b),{116:16,117:3})
        self.assertEqual({(x['floor'],x['x'],x['y']) for x in b if x['function']=='npcgen_warpman' and x['floor']==116},{(116,11,16),(116,12,16),(116,11,13),(116,12,13)})
        self.assertEqual(d['main_creation_sha256'],'d09462b9627049b9efb6cb1c05a640c841bd1a15f4e62aceda79efaec41cd40b')

    def test_all_source_argument_links_exist(self):
        d=self.d
        paths={x['path'] for x in d['file_arguments']}
        args=[x['source_argument'] for x in d['creation_blocks'] if x['source_argument']]
        self.assertEqual(len(args),15)
        self.assertEqual(len(set(args)),15)
        self.assertTrue(set(args)<=paths)
        self.assertEqual(d['source_argument_links'],{'unique':15,'resolved_in_same_zip':15,'missing':0})

    def test_fixed_source_byte_spans(self):
        x=self.d['creation_blocks'];lo=-1
        for b in x:
            start,end=b['byte_span']
            self.assertGreaterEqual(start,lo)
            self.assertGreater(end,start)
            self.assertLessEqual(end,3106)
            self.assertEqual(len(b['raw_block_sha256']),64)
            lo=end

    def test_four_performer_entry_exit_guards(self):
        d=self.d
        guards=d['floor116_staff_warp_guards']
        self.assertEqual(len(guards),4)
        self.assertEqual([x['free'] for x in guards],['LV>0&ITEM=2608']*2+['LV>0&ITEM!=2609']*2)
        self.assertEqual([x['warp'] for x in guards],['116,11,11','116,12,11','116,11,17','116,12,17'])
        self.assertTrue(all(x['del_item'] is None for x in guards))

    def test_two_unlinked_permit_source_candidates(self):
        d=self.d
        s=d['unlinked_performance_permit_script_candidates']
        self.assertEqual({(x['path'],x['conditional_token'],x['item_grant_token'],x['direct_file_reference_occurrences_in_2205']) for x in s},{('npc/extra/event/syutuen','ITEM!=2608','GetItem:2608*1',0),('npc/extra/event/karikari','ITEM!=2703','GetItem:2703*1',0)})
        self.assertEqual(d['unlinked_stage_return_parameter']['direct_file_reference_occurrences_in_2205'],0)
        self.assertEqual(d['unlinked_stage_return_parameter']['del_item'],'2702,2703')

    def test_original_number_occurrences_are_bounded(self):
        ids=self.d['all_member_literal_id_occurrences']
        self.assertEqual([len(ids[k]) for k in ['2608','2609','2703']],[3,7,3])
        self.assertEqual({x['path'] for x in ids['2608']},{'npc/extra/event/syutuen','npc/genout/wpm_116_11_16','npc/genout/wpm_116_12_16'})
        self.assertIn('npc/giiru/event/sikkoku05',{x['path'] for x in ids['2703']})

    def test_no_made_up_runtime_or_completion(self):
        q=self.d['qualification']
        self.assertTrue(all(v.startswith('OPEN') for k,v in q.items() if k!='static_create_and_argument_source'))
        self.assertIsNone(self.d['historical_stage']['overall_percent'])
        self.assertEqual([self.d['historical_stage']['stage_a_partial'],self.d['historical_stage']['stage_a_open']],[7,2])

if __name__=='__main__':unittest.main()
