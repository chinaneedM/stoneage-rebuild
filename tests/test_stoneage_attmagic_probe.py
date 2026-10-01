import contextlib,io,struct,tempfile,unittest
from pathlib import Path

from tools.stoneage_attmagic_probe import analyze,emit,RECORD_SIZE


def rec(sprite,attack):
    vals=[0]*33
    vals[0]=sprite
    vals[1]=attack
    vals[10]=0xffffffff
    vals[14]=0xffffffff
    return struct.pack("<33I",*vals)


class AttackMagicProbeTests(unittest.TestCase):
    def test_adjacent_side_pairs_and_magic_idx_crosslink(self):
        with tempfile.TemporaryDirectory() as td:
            data=Path(td)
            a=rec(100,1)
            b=rec(200,2)
            c=rec(300,3)
            (data/"attmagic.bin").write_bytes(a+a+b+c)
            (data/"magic.txt").write_text(
                "N,C,F,O,1,1,1,0,0\n"
                "N2,C2,F2,O2,2,1,1,0,1\n",
                encoding="utf-8",
            )
            r=analyze(data)
            self.assertEqual(RECORD_SIZE,132)
            self.assertEqual(r["raw_count"],4)
            self.assertEqual(r["index_count"],2)
            self.assertEqual(r["adjacent_exact"],1)
            self.assertEqual(r["adjacent_diff"],1)
            self.assertEqual(r["valid_idx"],{0,1})
            self.assertEqual(r["invalid_idx"],set())
            self.assertEqual(r["unreferenced"],[])
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):
                emit(data)
            report=buf.getvalue()
            self.assertIn("SOURCE_MAGIC_INDEX_COUNT|2",report)
            self.assertIn("SIDE1_EVEN_RECORD_COUNT|2",report)
            self.assertIn("SIDE0_ODD_RECORD_COUNT|2",report)
            self.assertIn("ADJACENT_SIDE_PAIR_EXACT|1",report)

    def test_bad_size(self):
        with tempfile.TemporaryDirectory() as td:
            data=Path(td)
            (data/"attmagic.bin").write_bytes(b"x")
            with self.assertRaises(ValueError):
                analyze(data)


if __name__=="__main__":
    unittest.main()
