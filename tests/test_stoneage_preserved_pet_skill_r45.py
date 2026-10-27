import hashlib
import unittest
from unittest.mock import patch
from tools.stoneage_preserved_pet_skill_r45 import skill_config,parse_table,derive


def row(i,name='測試技能',callback='PETSKILL_NormalAttack',cost=0):
 fields=[name.encode('cp950'),b'private comment',callback.encode(),b'2',b'',b'',
         str(i).encode(),b'1',b'2',str(cost).encode(),b'0',callback.encode()]
 return b','.join(fields)

class OriginalPetSkillParser(unittest.TestCase):
 def test_both_relative_paths_preserve_literal_prefix(self):
  d=skill_config(b'petskillfile1=./data/petskill.txt\npetskillfile2=data/petskill.txt\n')
  self.assertEqual(d['petskillfile1'],'./data/petskill.txt')
 def test_different_config_alternatives_rejected(self):
  with self.assertRaises(ValueError):skill_config(b'petskillfile1=data/petskill.txt\npetskillfile2=data/petskill1.txt\n')
 def test_duplicate_key_rejected(self):
  with self.assertRaises(ValueError):skill_config(b'petskillfile1=data/petskill.txt\npetskillfile1=data/petskill.txt\npetskillfile2=data/petskill.txt\n')
 def test_traversal_and_missing_config_rejected(self):
  for raw in (b'petskillfile1=../data/petskill.txt\npetskillfile2=data/petskill.txt',b'petskillfile1=data/petskill.txt'):
   with self.subTest(raw=raw),self.assertRaises(ValueError):skill_config(raw)
 def test_id_zero_is_preserved(self):
  self.assertEqual(parse_table(row(0))[0]['numbers']['ID'],0)
 def test_duplicate_id_rejected(self):
  with self.assertRaises(ValueError):parse_table(row(1)+b'\n'+row(1))
 def test_exact12_fields_required(self):
  with self.assertRaises(ValueError):parse_table(row(1)+b',extra')
 def test_bad_callback_and_number_rejected(self):
  with self.assertRaises(ValueError):parse_table(row(1,callback='invalid callback'))
  with self.assertRaises(ValueError):parse_table(row(1,cost='x'))
 def test_enemy_callback_in_same_table_is_not_rejected(self):
  rows=parse_table(row(500,callback='ENEMYSKILL_ReLife')+b'\n'+row(501,callback='ENEMYSKILL_ReHP'))
  self.assertEqual([r['callback'] for r in rows],['ENEMYSKILL_ReLife','ENEMYSKILL_ReHP'])
 def test_original_physical_line_offset(self):
  prefix=b'# comment\r\n\r\n';r=parse_table(prefix+row(5)+b'\r\n')[0]
  self.assertEqual((r['line'],r['offset'],r['body']),(3,len(prefix),row(5)))
 def test_complete_synthetic147_row_derivation_is_bounded(self):
  members={'setup.cf':b'petskillfile1=./data/petskill.txt\npetskillfile2=./data/petskill.txt',
           'data/petskill.txt':b'\n'.join(row(i) for i in range(147))}
  expected={k:(len(v),hashlib.sha256(v).hexdigest()) for k,v in members.items()}
  with patch('tools.stoneage_preserved_pet_skill_r45.EXPECTED',expected):d=derive(members)
  self.assertEqual([r['numeric_fields']['ID'] for r in d['selected_rows']],list(range(6)))
  self.assertEqual(len(d['selected_rows']),6)
  self.assertNotIn('private comment',str(d))
  self.assertFalse(d['cost_is_mp_or_training_price_proven'])
  self.assertFalse(d['original_callback_execution_proven'])

if __name__=='__main__':unittest.main()
