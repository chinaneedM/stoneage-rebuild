import unittest
from tools.stoneage_preserved_item_shop_r44 import arg_fields, inventory_tokens, expand_inventory, parse_items
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

if __name__=='__main__':unittest.main()
