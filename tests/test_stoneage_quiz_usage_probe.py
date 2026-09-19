import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_quiz_usage_probe import analyze, emit

TPL = b"""NPCTEMPLATE
{
templatename=Q
functionset=Quiz
}
"""
CREATE = b"""NPCCREATE
{
enemy=Q|file:q.arg
}
"""
DUP_TPL = b"""NPCTEMPLATE
{
templatename=Q
functionset=Quiz
}
"""
MIXED_TPL = b"""NPCTEMPLATE
{
templatename=Q
functionset=TownPeople
}
"""
ARG = b"""StartMsg:x
Quiznum:5
EntryItem:100*2,200
EntryStone:50
NoEntryMsg:y
ItemFullMsg:z
GetItem:4,300.301,2,302
Border:4,high,2,low
Warp:4,1.2.3,2,4.5.6
Party:p
Type:1
Answer:2
Level:4
"""
QUESTIONS = b"""# ignored
1,1,2,1,1,secret-question-payload,a,b,c
2,2,4,2,2,other-question-payload,d,e,f
"""


class QuizUsageProbeTests(unittest.TestCase):
    def build(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "t").write_bytes(TPL)
        (root / "c").write_bytes(CREATE)
        (root / "q.arg").write_bytes(ARG)
        (root / "question.txt").write_bytes(QUESTIONS)
        return td, root

    def test_shapes(self):
        td, root = self.build()
        try:
            result = analyze(root, root / "question.txt")
            self.assertEqual(result["counts"]["refs"], 1)
            self.assertEqual(result["counts"]["resolved_files"], 1)
            self.assertEqual(result["counts"]["stable_quiz_template_names"], 1)
            self.assertEqual(result["item_shapes"][("tokens", 2)], 1)
            self.assertEqual(result["quantities"][2], 1)
            self.assertEqual(result["pair_shapes"][("GetItem", 2, 0)], 1)
            self.assertEqual(result["reward_candidate_arity"][2], 1)
            self.assertEqual(result["warp_destination_arity"][3], 2)
            self.assertEqual(result["questions"]["source_rows"], 2)
            self.assertEqual(result["questions"]["loaded_rows"], 2)
            self.assertEqual(result["questions"]["arity"][9], 2)
            self.assertEqual(result["scalar_values"][("Quiznum", 5)], 1)
            self.assertEqual(result["scalar_values"][("EntryStone", 50)], 1)
            self.assertEqual(result["threshold_values"][("Warp", 4)], 1)
        finally:
            td.cleanup()

    def test_duplicate_same_functionset_remains_stable_quiz(self):
        td, root = self.build()
        try:
            (root / "t2").write_bytes(DUP_TPL)
            result = analyze(root, root / "question.txt")
            self.assertEqual(result["counts"]["refs"], 1)
            self.assertEqual(result["counts"]["duplicate_stable_quiz_template_names"], 1)
            self.assertEqual(result["counts"]["ambiguous_mixed_quiz_template_names"], 0)
        finally:
            td.cleanup()

    def test_mixed_duplicate_is_reported_as_load_order_ambiguity(self):
        td, root = self.build()
        try:
            (root / "t2").write_bytes(MIXED_TPL)
            result = analyze(root, root / "question.txt")
            self.assertEqual(result["counts"]["refs"], 0)
            self.assertEqual(result["counts"]["ambiguous_mixed_quiz_template_names"], 1)
            self.assertEqual(result["counts"]["ambiguous_mixed_template_refs"], 1)
        finally:
            td.cleanup()

    def test_output_drops_payload(self):
        td, root = self.build()
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root, root / "question.txt"))
            text = out.getvalue()
            for secret in ("100*2", "300.301", "1.2.3", "secret-question-payload", "other-question-payload", "q.arg"):
                self.assertNotIn(secret, text)
            self.assertIn("PAIR_SHAPE|Warp|pairs=2|remainder=0|blocks=1", text)
            self.assertIn(
                "QUESTION_FILE|present=1|source_rows=2|loaded_rows=2", text
            )
        finally:
            td.cleanup()

    def test_question_loader_shape_matches_fixed_parser(self):
        td, root = self.build()
        try:
            with (root / "question.txt").open("ab") as f:
                f.write(b"3,1,1,2,1,too-short,a,b\n")
            result = analyze(root, root / "question.txt")
            self.assertEqual(result["questions"]["source_rows"], 3)
            self.assertEqual(result["questions"]["loaded_rows"], 2)
            self.assertEqual(
                result["questions"]["invalid_shape"]["fewer_than_9_fields"], 1
            )
        finally:
            td.cleanup()

    def test_missing_secondary_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "t").write_bytes(TPL)
            (root / "c").write_bytes(b"NPCCREATE\n{\nenemy=Q|file:no.arg\n}\n")
            result = analyze(root, None)
            self.assertEqual(result["counts"]["missing_files"], 1)
            self.assertFalse(result["questions"]["present"])


if __name__ == "__main__":
    unittest.main()
