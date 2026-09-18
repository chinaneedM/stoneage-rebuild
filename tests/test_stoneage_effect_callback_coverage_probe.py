import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tools.stoneage_effect_callback_coverage_probe import (
    analyze,
    choose_active_file,
    parse_global_function_table,
    parse_named_function_table,
)


def item_row(usefunc="", attachfunc=""):
    cols = [""] * 94
    cols[0] = "name"
    cols[10] = usefunc
    cols[11] = attachfunc
    cols[16] = "1"
    return ",".join(cols)


def global_source(*names):
    body = "\n".join(f'    {{ {{"{n}"}}, (void*)1, 0 }},' for n in names)
    return (
        "static CorrespondStringAndFunctionTable "
        "correspondStringAndFunctionTable[]=\n{\n" + body + "\n};\n"
    )


def named_source(marker, *names):
    body = "\n".join(f'    {{ "{n}", (void*)1, 0 }},' for n in names)
    return f"static X {marker} = {{\n{body}\n}};\n"


class EffectCallbackCoverageProbeTests(unittest.TestCase):
    def make_args(self, root):
        data = root / "data"
        data.mkdir()
        (data / "itemset.txt").write_text(
            "\n".join([
                item_row("ITEM_A", "ITEM_ATTACH"),
                item_row("ITEM_A"),
                item_row("ITEM_B"),
                item_row("ITEM_C"),
                item_row("ITEM_D"),
            ]) + "\n",
            encoding="utf-8",
        )
        (data / "magic.txt").write_text(
            "n,d,MAGIC_A,opt,1,1,1,0\n"
            "n,d,MAGIC_B,opt,2,1,1,0\n"
            "n,d,MAGIC_C,opt,3,1,1,0\n",
            encoding="utf-8",
        )
        (data / "petskill.txt").write_text(
            "n,d,PET_A,o1,o2,o3,1,1,1,2,0,tail\n"
            "n,d,PET_B,o1,o2,o3,2,1,1,2,0,tail\n",
            encoding="utf-8",
        )
        setup = root / "setup.cf"
        setup.write_text(
            "itemset3file=data/itemset.txt\n"
            "magicfile=./data/magic.txt\n"
            "petskillfile1=./data/petskill.txt\n"
            "petskillfile2=./data/petskill.txt\n",
            encoding="utf-8",
        )

        specs = {
            "gavin": {
                "item": ("ITEM_A", "ITEM_B", "ITEM_ATTACH"),
                "magic": ("MAGIC_A", "MAGIC_B"),
                "petskill": ("PET_A",),
            },
            "iris": {
                "item": ("ITEM_A", "ITEM_ATTACH"),
                "magic": ("MAGIC_A",),
                "petskill": ("PET_A", "PET_B"),
            },
            "bismarck": {
                "item": ("ITEM_A", "ITEM_C", "ITEM_ATTACH"),
                "magic": ("MAGIC_A", "MAGIC_C"),
                "petskill": ("PET_A",),
            },
        }

        paths = {}
        for lineage, spec in specs.items():
            d = root / lineage
            d.mkdir()
            function = d / "function.c"
            magic = d / "magic.c"
            petskill = d / "pet.c"
            function.write_text(global_source(*spec["item"]), encoding="utf-8")
            magic.write_text(named_source("MAGIC_functbl[]", *spec["magic"]), encoding="utf-8")
            petskill.write_text(
                named_source("PETSKILL_functbl[]", *spec["petskill"]),
                encoding="utf-8",
            )
            paths[lineage] = (function, magic, petskill)

        return SimpleNamespace(
            data_dir=data,
            setup=setup,
            gavin_function=paths["gavin"][0],
            gavin_magic=paths["gavin"][1],
            gavin_petskill=paths["gavin"][2],
            iris_function=paths["iris"][0],
            iris_magic=paths["iris"][1],
            iris_petskill=paths["iris"][2],
            bismarck_function=paths["bismarck"][0],
            bismarck_magic=paths["bismarck"][1],
            bismarck_petskill=paths["bismarck"][2],
        )

    def test_source_table_parsers(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            g = root / "g.c"
            m = root / "m.c"
            g.write_text(global_source("A", "B"), encoding="utf-8")
            m.write_text(named_source("MAGIC_functbl[]", "M1", "M2"), encoding="utf-8")
            self.assertEqual(parse_global_function_table(g), {"A", "B"})
            self.assertEqual(parse_named_function_table(m, "MAGIC_functbl[]"), {"M1", "M2"})

    def test_active_files_follow_setup(self):
        with tempfile.TemporaryDirectory() as td:
            args = self.make_args(Path(td))
            self.assertEqual(
                choose_active_file(args.data_dir, args.setup, kind="item").name,
                "itemset.txt",
            )
            self.assertEqual(
                choose_active_file(args.data_dir, args.setup, kind="magic").name,
                "magic.txt",
            )
            self.assertEqual(
                choose_active_file(args.data_dir, args.setup, kind="petskill").name,
                "petskill.txt",
            )

    def test_item_usefunc_all_some_none_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            r = analyze(self.make_args(Path(td)))
            use = r["item_slots"]["usefunc"]
            self.assertEqual(use["unique"], 4)
            self.assertEqual(use["row_uses"], 5)
            self.assertEqual(use["classes"]["all"], 1)
            self.assertEqual(use["classes"]["some"], 2)
            self.assertEqual(use["classes"]["none"], 1)
            self.assertEqual(use["row_classes"]["all"], 2)
            self.assertEqual(use["row_classes"]["some"], 2)
            self.assertEqual(use["row_classes"]["none"], 1)

    def test_item_slot_is_classified_independently(self):
        with tempfile.TemporaryDirectory() as td:
            r = analyze(self.make_args(Path(td)))
            attach = r["item_slots"]["attachfunc"]
            self.assertEqual(attach["unique"], 1)
            self.assertEqual(attach["classes"]["all"], 1)
            self.assertEqual(attach["row_uses"], 1)

    def test_magic_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            r = analyze(self.make_args(Path(td)))
            magic = r["magic"]
            self.assertEqual(magic["unique"], 3)
            self.assertEqual(magic["classes"]["all"], 1)
            self.assertEqual(magic["classes"]["some"], 2)
            self.assertEqual(magic["classes"]["none"], 0)

    def test_petskill_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            r = analyze(self.make_args(Path(td)))
            pet = r["petskill"]
            self.assertEqual(pet["unique"], 2)
            self.assertEqual(pet["classes"]["all"], 1)
            self.assertEqual(pet["classes"]["some"], 1)
            self.assertEqual(pet["classes"]["none"], 0)
            self.assertEqual(pet["per"]["iris"]["unique_matched"], 2)
            self.assertEqual(pet["per"]["gavin"]["unique_matched"], 1)


if __name__ == "__main__":
    unittest.main()
