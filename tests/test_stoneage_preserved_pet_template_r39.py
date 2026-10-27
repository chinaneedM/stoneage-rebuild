import unittest
from tools.stoneage_preserved_pet_template_r39 import derive, lines

class TemplateEvidenceTests(unittest.TestCase):
 def specimen(self):
  rows=[]
  for i in range(988):
   fields=[b'']*56;fields[0]=('烏力' if i in (0,1) else '其他').encode('cp950')
   fields[6]=str(i+1).encode();fields[36]=str(100000+i).encode();fields[37]=b'1'
   rows.append(b','.join(fields))
  return b'\r\n'.join(rows)+b'\r\n',b'# config\r\nenemybasefile = ./data/enemybase.txt\r\n'
 def test_offsets_and_duplicate_names_preserved(self):
  raw,setup=self.specimen();report=derive(raw,setup)
  self.assertEqual([r['template_number_column_7'] for r in report['selected_rows']],[1,2])
  for row in report['selected_rows']:
   self.assertTrue(raw[row['byte_offset']:].startswith('烏力'.encode('cp950')))
  self.assertEqual(report['selected_rows'][1]['graphic_field_column_37'],100001)
  self.assertEqual(report['unmatched_name_queries'],['烏力烏力','烏力斯坦'])
  self.assertFalse(report['same_client_server_build_proven'])
 def test_wrong_config_and_duplicate_config_rejected(self):
  raw,setup=self.specimen()
  for bad in (setup.replace(b'enemybase.txt',b'enemybase2.txt'),setup+setup):
   with self.assertRaises(ValueError):derive(raw,bad)
 def test_wrong_extent_rejected(self):
  raw,setup=self.specimen()
  for bad in (raw+b',',raw.split(b'\r\n',1)[1]):
   with self.assertRaises(ValueError):derive(bad,setup)
 def test_not_atoi_coercion(self):
  raw,setup=self.specimen()
  with self.assertRaises(ValueError):derive(raw.replace(b'100000',b'100000garbage',1),setup)
 def test_line_offset_includes_comments_and_newlines(self):
  self.assertEqual(list(lines(b'#a\r\n\r\nx\r\n')) ,[(3,6,b'x')])
if __name__=='__main__':unittest.main()
