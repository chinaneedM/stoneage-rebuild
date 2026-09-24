import tempfile
import unittest
from pathlib import Path
import gzip
import struct

from tools.stoneage_tw10_25_fieldmap_compat_probe import (
    analyze_map, requires_profile
)


class TaiwanV125FieldmapCompatProbeTests(unittest.TestCase):
    def test_profile_requirement_matches_client_rules(self):
        self.assertFalse(requires_profile(0))
        self.assertFalse(requires_profile(59))
        self.assertTrue(requires_profile(60))
        self.assertTrue(requires_profile(79))
        self.assertFalse(requires_profile(80))
        self.assertFalse(requires_profile(99))
        self.assertTrue(requires_profile(100))

    def test_map_compatibility_detects_missing_resource_id(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"1.dat"
            width=height=2
            tile=(0,60,100,4)
            parts=(0,0,101,0)
            event=(0,0,0,0)
            path.write_bytes(struct.pack("<II",width,height)+struct.pack("<12H",*(tile+parts+event)))
            info=analyze_map(path,{60,100})
            self.assertFalse(info["compatible"])
            self.assertEqual(info["missing_ids"],[101])

    def test_map_compatibility_accepts_resolved_ids(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"1.dat"
            path.write_bytes(struct.pack("<II",1,1)+struct.pack("<3H",100,0,0))
            info=analyze_map(path,{100})
            self.assertTrue(info["compatible"])
            self.assertEqual(info["missing_cells"],0)


if __name__=="__main__":
    unittest.main()
