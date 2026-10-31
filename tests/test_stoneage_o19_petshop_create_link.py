"""O19 only tests derived source contract; never reads proprietary original bytes."""
import unittest,copy,json
from tools.stoneage_o19_petshop_create_link import validate,REPORT

class TestO19Source(unittest.TestCase):
    def setUp(self):
        self.x=json.loads(REPORT.read_bytes())
    def test_exact(self):
        self.assertEqual(validate(self.x)["static_source_coordinate"],[12,13])
    def test_six_negative_source_mutations(self):
        scenarios=[("original_create","target_create_block_sha256","0"*64),
                   ("original_create","borncorner",[12,12,12,12]),
                   ("original_create","argument_relative_path","genout/ps_1003_99_99"),
                   ("client_map_source_cell","third_plane_gameplay_semantics_proven",True),
                   ("source_scope","NPC_original_runtime_instantiated",True),
                   ("source_scope","official_2003_or_tw10_same_deployment_proven",True),
                   ("source_scope","original_pet_sale_or_storage_executed",True)]
        for section,key,value in scenarios:
            with self.subTest(section=section,key=key):
                d=copy.deepcopy(self.x);d[section][key]=value
                with self.assertRaises(ValueError):validate(d)

if __name__=="__main__":
    unittest.main()
