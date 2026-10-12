"""Strict guard uses pinned derived JSON as fixture, then tests tampering."""
import copy, json, unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_mutations_r13_guard import validate
PATH = Path("research/recovered/STONEAGE-TW10-SAVEDATA-MUTATIONS-R13-ORIGINAL.json")

class TestGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = PATH.read_text()
        cls.fixture = json.loads(cls.original)

    def changed(self, mutate):
        row=copy.deepcopy(self.fixture)
        mutate(row)
        with self.assertRaises(ValueError):
            validate(json.dumps(row))

    def test_pinned_original_valid(self):
        result=validate(self.original)
        self.assertEqual(result["global_write_candidates"],4)
        self.assertFalse(result["native_io_executed"])

    def test_prohibition_promotion(self):
        self.changed(lambda r:r.update(native_io_executed=True))

    def test_frame_offset_tamper(self):
        self.changed(lambda r:r["store_candidates"][0].update(destination_relative_field_offset=0))

    def test_wrong_global(self):
        self.changed(lambda r:r["store_candidates"][2].update(expected_global_rva=0))

    def test_source_register_tamper(self):
        self.changed(lambda r:r["store_candidates"][4]["source_operand"].update(register="eax"))

    def test_missing_jump_context(self):
        self.changed(lambda r:r["linear_windows"][0].update(jump_sites=[]))

    def test_bad_effect_scope(self):
        self.changed(lambda r:r["store_candidates"][1].update(named_caller_effect_admitted=True))

    def test_duplicate_json_field(self):
        with self.assertRaises(ValueError):
            validate('{"schema":"a","schema":"b"}')

    def test_extra_field(self):
        self.changed(lambda r:r.update(native_save_format_proven=True))

    def test_oversized_payload(self):
        with self.assertRaises(ValueError):
            validate(" "*16001)

if __name__=="__main__":
    unittest.main()
