"""Independent R14 derived-only provenance guard mutation checks."""
import copy
import json
import unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_reachdefs_r14_guard import validate
P=Path("research/recovered/STONEAGE-TW10-SAVEDATA-REACHDEFS-R14-ORIGINAL.json")

class TestR14Guard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=P.read_text()
        cls.record=json.loads(cls.raw)

    def corrupted(self,change):
        obj=copy.deepcopy(self.record)
        change(obj)
        with self.assertRaises(ValueError):
            validate(json.dumps(obj))

    def test_pinned_original_accepts(self):
        x=validate(self.raw)
        self.assertEqual(x["query_count"],5)
        self.assertFalse(x["native_io_executed"])

    def test_false_runtime_promotion(self):
        self.corrupted(lambda v:v.update(native_io_executed=True))

    def test_frame_entry_promotion(self):
        self.corrupted(lambda v:v["regions"][0].update(anchor_is_verified_function_entry=True))

    def test_unknown_call_promotion(self):
        self.corrupted(lambda v:v["regions"][1]["inputs"][1]["reaching_sources"][0].update(origin="definition"))

    def test_wrong_site(self):
        self.corrupted(lambda v:v["regions"][1]["inputs"][3].update(site_rva=0))

    def test_wrong_call(self):
        self.corrupted(lambda v:v["regions"][1]["call_barrier_sites"].pop())

    def test_register_known_promotion(self):
        self.corrupted(lambda v:v["regions"][0]["inputs"][0].update(register_value_known=True))

    def test_out_of_window_gap_dropped(self):
        self.corrupted(lambda v:v["regions"][0].update(frontier=[]))

    def test_extra_key(self):
        self.corrupted(lambda v:v.update(save_format_proven=True))

    def test_duplicate_field(self):
        with self.assertRaises(ValueError):
            validate('{"schema":"a","schema":"b"}')

    def test_size_cap(self):
        with self.assertRaises(ValueError):
            validate(" "*12001)

if __name__=="__main__":
    unittest.main()
