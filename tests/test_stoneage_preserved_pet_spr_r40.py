import struct
import unittest
from tools.stoneage_preserved_pet_spr_r40 import parse_pair

class SPRSourceTests(unittest.TestCase):
 def fixture(self):
  one=struct.pack('<HHII',7,12,19,2)+struct.pack('<IhhH',123,-4,7,10003)+struct.pack('<IhhH',0xffffffff,0,0,65535)
  two=struct.pack('<HHII',1,2,0,1)+struct.pack('<IhhH',456,-32768,32767,3)
  body=one+two
  index=b''.join(struct.pack('<IIHH',*v) for v in [(100250,0,1,9),(100251,len(one),1,0),(100250,0,1,9)])
  return index,body
 def test_duplicate_and_nonmonotonic_occurrences_preserved(self):
  index,body=self.fixture();m=parse_pair(index,body,[100250,100251,100252])
  self.assertEqual([g['group_index'] for g in m['selected_groups']],[0,1,2])
  self.assertEqual(m['selected_frame_occurrences'],5)
  self.assertEqual(m['selected_sentinel_occurrences'],2)
  self.assertEqual(m['selected_groups'][0]['animations'][0]['frames'][0],[123,-4,7,10003])
  self.assertEqual(m['unmatched_graphic_keys'],[100252])
  self.assertEqual(m['selected_groups'][0]['reserved'],9)
  self.assertEqual(m['selected_groups'][1]['animations'][0]['frames'][0],[456,-32768,32767,3])
 def test_truncation_and_out_of_bounds(self):
  index,body=self.fixture()
  for idx,b in [(index[:-1],body),(index,body[:-1]),(index[:4]+struct.pack('<I',99999)+index[8:],body)]:
   with self.assertRaises(ValueError):parse_pair(idx,b,[100250,100251])
 def test_no_trailing_payload_loss(self):
  index,body=self.fixture()
  with self.assertRaises(ValueError):parse_pair(index,body+b'\0',[100251])
 def test_unselected_groups_not_claimed_parsed(self):
  index,body=self.fixture();m=parse_pair(index,body,[])
  self.assertEqual(m['selected_groups'],[]);self.assertEqual(m['index_rows_count'],3)
if __name__=='__main__':unittest.main()
