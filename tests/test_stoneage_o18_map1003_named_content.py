"""O18 original content/version separation negative tests with no original bytes."""
import copy
import json
import unittest
from tools.stoneage_o18_map1003_named_content import REPORT,validate

class O18NamedMapContractTests(unittest.TestCase):
    def setUp(self):
        self.report=json.loads(REPORT.read_bytes())
    def test_source_receipt(self):
        self.assertEqual(validate(self.report)["matching_original_source_cells"],1800)
    def test_12_negative_claims(self):
        cases=[
            ("original_server_map","original_CP950_location_label","UNKNOWN"),
            ("original_server_map","difference_count_by_plane",[0,1]),
            ("original_client_map","sha256","0"*64),
            ("original_aux_map","semantics_known",True),
            ("bounds","name_proven_for_2003_or_official_TW10",True),
            ("bounds","client_server_same_deployed_release_proven",True),
            ("bounds","original_NPC_runtime_spawns_proven",True),
            ("bounds","original_shop_transaction_executed",True),
            ("bounds","original_pet_skill_training_executed",True),
            ("bounds","original_game_world_entered",True),
            ("private_source_package","committed_to_public_Git",True)]
        for name,field,value in cases:
            with self.subTest(section=name,field=field):
                d=copy.deepcopy(self.report)
                d[name][field]=value
                with self.assertRaises(ValueError): validate(d)
        d=copy.deepcopy(self.report)
        d["original_NPC_message_members"]["msg_1003_16_13"]["actual_NPC_create_pointer_proven"]=True
        with self.assertRaises(ValueError): validate(d)

if __name__=="__main__":
    unittest.main()
