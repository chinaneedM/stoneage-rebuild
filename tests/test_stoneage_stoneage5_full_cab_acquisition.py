"""Synthetic tests; a green unit suite is not a real cabinet download."""
import tempfile
import unittest
from pathlib import Path
from tools.stoneage_stoneage5_full_cab_acquisition import (
    safe_name, verify_range, extracted_inventory, exact_matches)


class FullCabSafetyTests(unittest.TestCase):
    def test_safe_paths(self):
        self.assertEqual(safe_name("data\\test.bin"),"data/test.bin")
        for item in ("../x","/root/a","C:/a","a/../b","a//b","a\x00b","a/./b"):
            with self.subTest(item=item),self.assertRaises(ValueError):
                safe_name(item)

    def test_exact_byte_range(self):
        verify_range("bytes 100-199/1000",100,199,1000)
        for value in ("","bytes 101-199/1000","bytes 100-200/1000","bytes 100-199/999"):
            with self.subTest(value=value),self.assertRaises(ValueError):
                verify_range(value,100,199,1000)

    def test_file_size_and_sha_join(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            (p/"one.bin").write_bytes(b"abcd")
            files=[{"name":"one.bin","size":4,"index":0,"i_folder":0}]
            rows=extracted_inventory(p,files)
            self.assertEqual(len(rows),1)
            key=(rows[0]["size"],rows[0]["sha256"])
            self.assertEqual(len(exact_matches(rows,{key:["TW10/one.bin"]})),1)
            self.assertEqual(exact_matches(rows,{}),[])
            files[0]["size"]=3
            with self.assertRaises(ValueError):
                extracted_inventory(p,files)

    def test_missing_and_unexpected_files(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            expected=[{"name":"one.bin","size":4,"index":0,"i_folder":0}]
            with self.assertRaises(ValueError):
                extracted_inventory(p,expected)
            (p/"one.bin").write_bytes(b"abcd")
            (p/"extra.bin").write_bytes(b"x")
            with self.assertRaises(ValueError):
                extracted_inventory(p,expected)
            (p/"extra.bin").unlink()
            (p/"link").symlink_to(p/"one.bin")
            with self.assertRaises(ValueError):
                extracted_inventory(p,expected)


if __name__=="__main__":
    unittest.main()
