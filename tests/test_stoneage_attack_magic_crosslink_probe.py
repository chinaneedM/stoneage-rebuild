import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_attack_magic_crosslink_probe import analyze
from tools.stoneage_itemset_schema_probe import INDEX, SCHEMA


class AttackMagicCrosslinkProbeTests(unittest.TestCase):
    def test_synthetic_crosslink_projects_all_structural_links(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            petskill = (
                b"name,comment,PETSKILL_AttackMagic,magic=301 item=19647,"
                b"free,kind,1,1,0,0,0\n"
            )
            (root / "petskill.txt").write_bytes(petskill)

            option = "地|100|1".encode("cp950")
            magic = b",".join(
                (
                    b"name",
                    b"comment",
                    b"MAGIC_AttMagic",
                    option,
                    b"301",
                    b"1",
                    b"1",
                    b"0",
                    b"0",
                )
            ) + b"\n"
            (root / "magic.txt").write_bytes(magic)

            row = [b""] * len(SCHEMA)
            row[INDEX["id"]] = b"19647"
            row[INDEX["magicid"]] = b"301"
            row[INDEX["magicusemp"]] = b"7"
            (root / "itemset.txt").write_bytes(b",".join(row) + b"\n")

            records = [tuple([0] * 33), tuple([1] * 33)]
            payload = b"".join(
                struct.pack("<33I", *record)
                for record in records
            )
            (root / "attmagic.bin").write_bytes(payload)

            result = analyze(root)
            self.assertEqual(result["attack_skill_count"], 1)
            self.assertEqual(result["pair_count"], 1)
            self.assertEqual(result["magic_rows"], 1)
            self.assertEqual(result["func_rows"], 1)
            self.assertEqual(result["idx_valid"], 1)
            self.assertEqual(result["option_structural"], 1)
            self.assertEqual(result["attr_values"], (0,))
            self.assertEqual(result["power_values"], (100,))
            self.assertEqual(result["level_values"], (1,))
            self.assertEqual(result["item_rows"], 1)
            self.assertEqual(result["item_magic_match"], 1)
            self.assertEqual(result["item_mp_values"], (7,))
            self.assertEqual(result["att_pair_valid"], 1)
            self.assertFalse(result["complete"])


if __name__ == "__main__":
    unittest.main()
