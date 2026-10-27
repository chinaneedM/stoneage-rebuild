import unittest
import hashlib
from unittest.mock import patch
from tools.stoneage_preserved_item_shop_r44 import arg_fields, inventory_tokens, expand_inventory, parse_items, derive
from tools.stoneage_itemset_schema_probe import INDEX


def item(i):
 fields=[b'']*94;fields[0]=b'name';fields[INDEX['id']]=str(i).encode()
 return b','.join(fields)


class BoundedOriginalShop(unittest.TestCase):
 def test_arg_duplicate_case_is_rejected(self):
  with self.assertRaises(ValueError):arg_fields(b'ItemList:1\nitemlist:2\n')

 def test_prose_values_are_not_emitted_by_field_parser_as_numbers(self):
  fields=arg_fields(b'# comment\nMessage:do not emit me\nItemList:1,3-4\n')
  self.assertEqual(fields['itemlist'],b'1,3-4')

 def test_unsupported_arg_grammar_rejected(self):
  with self.assertRaises(ValueError):arg_fields(b'not an assignment\n')

 def test_range_order_and_occurrences_retained(self):
  tokens=inventory_tokens(b' 3 - 5, 3, 8 ')
  p=expand_inventory(tokens,{3,5,8})
  self.assertEqual([r['item_id'] for r in p['listed_defined_occurrences']],[3,5,3,8])

 def test_undefined_ids_skipped_without_filling(self):
  p=expand_inventory(inventory_tokens(b'1-4'),{2,4})
  self.assertEqual([r['item_id'] for r in p['listed_defined_occurrences']],[2,4])

 def test_original_runtime_is_not_claimed(self):
  p=expand_inventory([[1,50]],set(range(1,51)))
  self.assertEqual(len(p['descendant_model_visible_occurrences']),33)
  self.assertEqual(len(p['descendant_model_truncated_occurrences']),17)
  self.assertFalse(p['model_is_original_runtime'])

 def test_reversed_and_polluted_tokens_rejected(self):
  for raw in (b'5-3',b'1x',b'1,,2',b'-1',b'1-1000001'):
   with self.subTest(raw=raw),self.assertRaises(ValueError):inventory_tokens(raw)

 def test_duplicate_master_id_rejected(self):
  with self.assertRaises(ValueError):parse_items(item(1)+b'\n'+item(1)+b'\n')

 def test_94_columns_required(self):
  with self.assertRaises(ValueError):parse_items(b'one,two,3\n')

 def test_physical_line_and_byte_offset_preserved(self):
  prefix=b'# header\r\n\r\n';raw=prefix+item(7)+b'\r\n'
  rows,count=parse_items(raw)
  self.assertEqual(count,1);self.assertEqual(rows[7][:2],(3,len(prefix)))
  self.assertEqual(rows[7][2],item(7))

class FullSyntheticDerivation(unittest.TestCase):
 def test_exact_preserved_relative_config_path_and_first_six_names(self):
  # Synthetic source explicitly bypasses only the full-source SHA constants.
  # It exercises the complete13252-row decoder and the path that failed in CI.
  rows=[]
  for i in range(1,13253):
   fields=[b'0']*94
   fields[0]=fields[1]='測試石'.encode('cp950')
   fields[INDEX['id']]=str(i).encode()
   rows.append(b','.join(fields))
  members={'setup.cf':b'\n'.join(k+b'=data/itemset.txt' for k in
     (b'itemset3file',b'itemset4file',b'itemset5file',b'itemset6file')),
   'data/itemset.txt':b'\n'.join(rows),
   'data/npc/my/shop/ACCESSORY1.arg':b'ItemList:1-8\nbuy_rate:2.5\n'}
  pins={k:(len(v),hashlib.sha256(v).hexdigest()) for k,v in members.items()}
  with patch('tools.stoneage_preserved_item_shop_r44.EXPECTED',pins):
   result=derive(members)
  self.assertEqual([r['item_id'] for r in result['selected_items']],[1,2,3,4,5,6])
  self.assertEqual(result['rate_fields']['buy_rate']['raw_decimal'],'2.5')
  self.assertIsNone(result['computed_runtime_prices'])
  self.assertEqual(result['configured_itemset_keys']['itemset3file'],'data/itemset.txt')

if __name__=='__main__':unittest.main()
