"""CHAR01 public receipt: bounded original-source counts; no commercial text bundled."""
import copy,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-MIXED25-SOURCE-RECEIPT-R1.json'
def check(d):
 assert d['schema']=='stoneage.character_npc_module_01_mixed25_full_original_npc_subtree_audit_receipt.r1'
 assert d['source_original_rar']['sha256']=='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
 assert d['source_original_rar']['original_entry_headers_scanned']==7952
 assert d['source_original_rar']['bytes']==361255180
 assert sum(d['file_types'].values())==d['metrics']['source_files']==d['full_derived_private_source']['all_npc_subtree_original_files']==2205
 assert d['full_derived_private_source']['all_npc_original_bytes']==1930332
 assert d['file_types']['create']==d['metrics']['original_create_source_files']==189
 assert d['file_types']['template']==d['metrics']['original_template_source_files']==46
 assert d['file_types']['arg']==d['metrics']['original_parameter_arg_files']==309
 assert d['file_types']['(no extension)']==1585
 assert d['metrics']['original_create_blocks']==4985
 assert d['metrics']['original_template_blocks']==119
 assert d['metrics']['nonempty_name_fields']==2451
 assert d['metrics']['source_create_blocks_with_numeric_graphicname']==2482
 assert d['metrics']['distinct_numeric_graphicname']==254
 assert d['metrics']['distinct_numeric_floorid']==633
 assert sum(d['metrics']['source_template_exact_token_links'].values())==4985
 assert d['metrics']['source_template_exact_token_links']=={'same_directory_unique':4131,'elsewhere_in_same_archive_unique':853,'ambiguous_across_archive':1,'unmatched':0}
 assert d['metrics']['original_source_file_references']=={'total':1803,'exact_target_file_present':1788,'exact_target_absent_in_same_npc_subtree':15}
 assert len(set(d['missing_exact_source_file_reference_paths']))==15
 assert d['ambiguous_template']['source_exact_token']=='npc_transmigration'
 assert len(d['ambiguous_template']['same_archive_candidates'])==2
 assert d['full_derived_private_source']['private_original_files_zip']['stored_user_private_Library'] is True
 assert d['full_derived_private_source']['rights_safe_complete_source_derived_row_index']['stored_local_artifact_not_in_public_Git_commit'] is True
 assert d['qualification']['restoration_percent'] is None
 assert all(v is False for k,v in d['qualification'].items() if k!='restoration_percent')
 assert d['prior_different_source_evidence']['TW1_image_and_MIXED25_server_names_are_same_deployed_build'] is False
 assert d['next'].startswith('CHARACTER_NPC_MODULE_02_')
class CHAR01(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=json.loads(P.read_text(encoding='utf8'))
 def test_source_bounded_counts(self):check(self.d)
 def test_no_false_npc_population(self):
  x=copy.deepcopy(self.d);x['qualification']['blocks_are_distinct_people']=True
  with self.assertRaises(AssertionError):check(x)
 def test_no_fake_runtime(self):
  x=copy.deepcopy(self.d);x['qualification']['blocks_are_authorized_runtime_active']=True
  with self.assertRaises(AssertionError):check(x)
 def test_no_fake_complete_dialogue_source(self):
  x=copy.deepcopy(self.d);x['metrics']['original_source_file_references']['exact_target_file_present']=1803
  with self.assertRaises(AssertionError):check(x)
 def test_no_fake_all_early_official(self):
  x=copy.deepcopy(self.d);x['qualification']['archive_is_official_TW1_or_JSS_1999']=True
  with self.assertRaises(AssertionError):check(x)
if __name__=='__main__':unittest.main()
