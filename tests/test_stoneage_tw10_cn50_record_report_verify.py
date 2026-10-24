import copy
import unittest
from pathlib import Path
import json
from tools.stoneage_tw10_cn50_record_report_verify import verify, source_tw10_files


class DerivedReportGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[1]
        # Source creates the report asynchronously. The unit suite on the first
        # source-only commit may run before that immutable file is present.
        cls.ready=(cls.root/"research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json").is_file()

    def test_tw10_manifest_semantics(self):
        text=(self.root/"research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt").read_text(encoding="utf8")
        rows=source_tw10_files(text)
        self.assertEqual(len(rows),383)
        self.assertIn("StoneAge/data/adrn_1.bin",rows)

    @unittest.skipUnless(Path(__file__).resolve().parents[1].joinpath(
        "research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json").is_file(),
        "await original-byte CI derived report before replay tests")
    def test_semantic_guard_and_mutants(self):
        root=self.root
        j=json.loads((root/"research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json").read_text(encoding="utf8"))
        c=json.loads((root/"research/recovered/STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json").read_text(encoding="utf8"))
        t=(root/"research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt").read_text(encoding="utf8")
        a=verify(j,c,t)
        self.assertEqual(a["bitmap_rd"]["old_records"],125996)
        self.assertEqual(a["animation_spr"]["old_records"],464)
        self.assertEqual(a["bitmap_rd"]["new_records"],303197)
        self.assertEqual(a["animation_spr"]["new_records"],1185)
        self.assertEqual(a["bitmap_rd"]["new_unique_ids"],177201)
        self.assertEqual(a["animation_spr"]["new_unique_ids"],721)
        mutations=[
            ("cn50_hash",lambda z:z["source_claims"]["CN50"].update(cab_sha256="bad")),
            ("early_sha",lambda z:z["source_claims"]["TW10"]["files"]["adrn"].update(sha256="bad")),
            ("server_fiction",lambda z:z["evidence_boundaries"].update(original_server_npc_quest_growth_master_recovered=True)),
            ("false_equal",lambda z:z["families"]["bitmap_rd"]["comparison"].update(exact_payload_or_segment_count=-1)),
            ("false_new",lambda z:z["families"]["animation_spr"]["comparison"].update(new_unique_ids_absent_in_old_count=999999999)),
        ]
        for name,change in mutations:
            with self.subTest(name=name):
                changed=copy.deepcopy(j)
                change(changed)
                with self.assertRaises(ValueError):
                    verify(changed,c,t)
