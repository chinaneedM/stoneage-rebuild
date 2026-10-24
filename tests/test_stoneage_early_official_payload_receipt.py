import json
from pathlib import Path
import unittest

PATH = Path("research/recovered/STONEAGE-EARLY-OFFICIAL-PAYLOAD-PROBE-R1.json")


class OriginalPayloadReceiptTest(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(PATH.read_text(encoding="utf-8"))

    def test_provenance_pin(self):
        s = self.doc["source"]
        self.assertEqual(s["run_id"], 40102349701)
        self.assertEqual(s["run_head"], "770b948a89aaaa4b3d6a122264d8c8511fc1b9ba")
        self.assertEqual(s["job_conclusion"], "success")
        self.assertFalse(s["artifact_independently_downloaded_and_rehashed"])

    def test_exact_four_real_failures(self):
        e = self.doc["raw_probe_report_from_logged_json"]["entries"]
        self.assertEqual(len(e), 4)
        self.assertEqual([i.get("error") for i in e], ["URLError","URLError","URLError","HTTP_ERROR"])
        self.assertEqual([i["http_status"] for i in e], [None,None,None,441])
        for item in e:
            self.assertEqual(item["qualification"], "NOT_RETRIEVED")
            self.assertEqual(item["sample_bytes"], 0)
            self.assertIsNone(item["sample_sha256"])
            self.assertIsNone(item["complete_original_sha256"])
            self.assertFalse(item["complete_body_downloaded"])
            self.assertFalse(item["official_clean_client_verified"])

    def test_nonpromotion(self):
        i = self.doc["interpretation"]
        self.assertEqual(i["complete_original_client_downloads"], 0)
        self.assertIsNone(i["complete_original_sha256"])
        self.assertEqual(i["pet_npc_named_original_resource_pairs"], 0)
        p = self.doc["preservation"]
        self.assertFalse(p["original_client_qualified"])
        self.assertFalse(p["copyrighted_binaries_committed"])
        self.assertIsNone(p["total_restoration_percentage"])

if __name__ == "__main__":
    unittest.main()
