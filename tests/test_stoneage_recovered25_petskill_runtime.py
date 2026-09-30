import tempfile
import unittest
from pathlib import Path

from tools.stoneage_recovered25_petskill_runtime import (
    load_recovered25_petskill_runtime,
)


def row(
    skill_id,
    function_name,
    option,
    *,
    field=1,
    target=3,
    cost=2,
    illegal=0,
    trailing="tail",
):
    chars = [
        "DisplayName",
        "Comment",
        function_name,
        option,
        "",
        "",
    ]
    ints = [skill_id, field, target, cost, illegal]
    return ",".join(chars + [str(value) for value in ints] + [trailing])


class Recovered25PetSkillRuntimeTests(unittest.TestCase):
    def test_loader_keeps_execution_fields_but_not_display_text(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            data = root / "data"
            data.mkdir()
            (data / "petskill.txt").write_bytes(
                (
                    row(
                        10,
                        "PETSKILL_NormalAttack",
                        "",
                    )
                    + "\n"
                    + row(
                        20,
                        "PETSKILL_ContinuationAttack",
                        "3",
                    )
                    + "\n"
                ).encode("ascii")
            )
            setup = root / "setup.cf"
            setup.write_text(
                "petskillfile1=./data/petskill.txt\n"
                "petskillfile2=./data/petskill.txt\n",
                encoding="utf-8",
            )

            runtime = load_recovered25_petskill_runtime(
                data_dir=data,
                setup=setup,
            )
            self.assertEqual(set(runtime.skills), {10, 20})
            self.assertEqual(runtime.source_file, "petskill.txt")
            attack = runtime.skills[10]
            self.assertEqual(attack.function_name, "PETSKILL_NormalAttack")
            self.assertEqual(attack.option_bytes, b"")
            self.assertTrue(attack.stable_common_callback)
            continuation = runtime.skills[20]
            self.assertEqual(continuation.ascii_option(), "3")
            self.assertEqual(continuation.target, 3)
            self.assertFalse(hasattr(continuation, "name"))
            self.assertFalse(hasattr(continuation, "comment"))

    def test_non_ascii_option_is_preserved_raw_and_ascii_decode_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            payload = (
                b"Display,Comment,PETSKILL_StatusChange,"
                b"\x81\x40,FREE,KIND,41,1,3,2,0,tail\n"
            )
            (data / "petskill.txt").write_bytes(payload)
            runtime = load_recovered25_petskill_runtime(data_dir=data)
            entry = runtime.skills[41]
            self.assertEqual(entry.option_bytes, b"\x81\x40")
            with self.assertRaisesRegex(ValueError, "not ASCII"):
                entry.ascii_option()

    def test_conflicting_compile_time_file_keys_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            data = root / "data"
            data.mkdir()
            (data / "petskill.txt").write_text(
                row(10, "PETSKILL_NormalAttack", "") + "\n",
                encoding="ascii",
            )
            (data / "petskill2.txt").write_text(
                row(20, "PETSKILL_NormalGuard", "") + "\n",
                encoding="ascii",
            )
            setup = root / "setup.cf"
            setup.write_text(
                "petskillfile1=./data/petskill.txt\n"
                "petskillfile2=./data/petskill2.txt\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "build macro is unresolved"):
                load_recovered25_petskill_runtime(
                    data_dir=data,
                    setup=setup,
                )

    def test_unresolved_skill_ids_are_reported_without_guessing(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "petskill.txt").write_text(
                row(10, "PETSKILL_NormalAttack", "") + "\n",
                encoding="ascii",
            )
            runtime = load_recovered25_petskill_runtime(data_dir=data)
            self.assertEqual(
                runtime.unresolved_skill_ids((0, 10, 20, -1, 20)),
                (20,),
            )


if __name__ == "__main__":
    unittest.main()
