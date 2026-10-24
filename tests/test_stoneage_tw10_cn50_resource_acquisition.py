import tempfile
from pathlib import Path
import unittest
from tools.stoneage_tw10_cn50_resource_acquisition import expected_source, validate_pinned_target


class RealAcquisitionContractTest(unittest.TestCase):
    def test_existing_source_pins_replay(self):
        report, cn, tw = expected_source(Path(__file__).resolve().parents[1])
        self.assertEqual(len(cn),413)
        self.assertEqual(len(tw),383)
        self.assertEqual(cn["adrn_31.bin"][0],24255760)
        self.assertEqual(cn["real_31.bin"][0],1102755808)
        self.assertEqual(report["source"]["cab_sha256"],
                         "cb414ad1ef4cc7925ec429ec088d0146892834c72667d1af82c8075d09f1683b")

    def test_no_size_or_digest_swap(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"data"
            p.write_bytes(b"data")
            import hashlib
            sha=hashlib.sha256(b"data").hexdigest()
            self.assertEqual(validate_pinned_target(p,"data",{"data":(4,sha)})["bytes"],4)
            with self.assertRaises(ValueError):
                validate_pinned_target(p,"data",{"data":(3,sha)})
            with self.assertRaises(ValueError):
                validate_pinned_target(p,"data",{"data":(4,"0"*64)})
            with self.assertRaises(ValueError):
                validate_pinned_target(p,"renamed",{"data":(4,sha)})
