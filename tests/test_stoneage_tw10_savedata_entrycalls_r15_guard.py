"""R15 independently pinned original derived report rejects tampering."""
import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_entrycalls_r15_guard import validate
P=Path("research/recovered/STONEAGE-TW10-SAVEDATA-ENTRYCALLS-R15-ORIGINAL.json")
class TestR15Guard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content=P.read_text()
        cls.data=json.loads(cls.content)
    def broken(self,mutate):
        a=copy.deepcopy(self.data);mutate(a)
        with self.assertRaises(ValueError):validate(json.dumps(a))
    def test_identity(self):
        x=validate(self.content)
        self.assertEqual(x["upstream_input_count"],4)
        self.assertFalse(x["native_io_executed"])
    def test_native_io_not_promoted(self):
        self.broken(lambda a:a.update(native_io_executed=True))
    def test_known_value_not_promoted(self):
        self.broken(lambda a:a["upstream_inputs"][0].update(fully_known_value=True))
    def test_entry_not_proven(self):
        self.broken(lambda a:a.update(bounded_graph_entry_not_proven=False))
    def test_call_target_not_assumed(self):
        self.broken(lambda a:a["call_surfaces"][0].update(direct_target_rva=0))
    def test_call_effect_not_known(self):
        self.broken(lambda a:a["call_surfaces"][2].update(callee_effect_summary_admitted=True))
    def test_provenance_register_not_wrong(self):
        self.broken(lambda a:a["upstream_inputs"][0].update(register="ebx"))
    def test_memory_input_address_mutation(self):
        self.broken(lambda a:a["upstream_inputs"][0]["origins"][0]["semantic"]["memory_input"]["displacement_region"].update(displacement_rva=0))
    def test_frame_owner_not_promoted(self):
        self.broken(lambda a:a.update(frame_setup_ownership_proven=True))
    def test_undocumented_key(self):
        self.broken(lambda a:a.update(native_file_format_proven=True))
    def test_duplicate_json_key(self):
        with self.assertRaises(ValueError):validate('{"schema":"a","schema":"b"}')
    def test_size_cap(self):
        with self.assertRaises(ValueError):validate(" "*40001)
if __name__=="__main__":
    unittest.main()
