"""Preserve the exact archive report and 22-domain source-layer constraints."""
import hashlib
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
class SnapshotPortfolioTest(unittest.TestCase):
    def test_verified_source_archive_raw_digest(self):
        p=ROOT/"research/recovered/STONEAGE-EARLY-MEDIA-ARCHIVE-SNAPSHOT-BOUNDARY-R1.json"
        raw=p.read_bytes()
        self.assertEqual(len(raw),3520)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),"e50cf9406ba4f057915adf84536dbb6d268d8bdd3303779a7da7b783cb9d6c57")
        x=json.loads(raw)
        self.assertEqual(x["counts"],{"qualified_early_link_pages":0,"requested_targets":3})
        self.assertEqual([a["actual_capture"] for a in x["targets"]],
                         ["20060115044722","20060115044722","20040204024948"])
        self.assertTrue(all(a["status"]=="OUT_OF_WINDOW_NOT_EARLY_EVIDENCE" for a in x["targets"]))
        self.assertTrue(all(a["availability_closest"] is None for a in x["targets"]))
        self.assertTrue(all("503" in a["availability_error"] for a in x["targets"]))
        self.assertFalse(x["source_1999_2002_globally_absent"])
        self.assertFalse(x["tw10_original_pet_species_verified"])
    def test_22_domain_statuses_preserved(self):
        m=read("research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json")
        x=read("research/recovered/STONEAGE-22-DOMAIN-EVIDENCE-COVERAGE-CHECKPOINT-R1.json")
        self.assertEqual(len(x["reviewed_domains"]),22)
        self.assertEqual(x["reviewed_domains_count"],22)
        self.assertEqual([(z["domain_id"],z["baseline_evidence_status"]) for z in x["reviewed_domains"]],
                         [(z["id"],z["status"]) for z in m["domains"]])
        self.assertTrue(all(z["bounded_source_connections"] for z in x["reviewed_domains"]))
        self.assertTrue(all(z["historical_fact_auto_promoted_from_2001_article_or_2004_2006_replay"] is False
                            for z in x["reviewed_domains"]))
        self.assertFalse(x["all_origins_fully_recovered"])
        self.assertTrue(x["remaining_historical_server_content_unproven"])
    def test_provenance_pins_and_no_invented_species(self):
        x=read("research/recovered/STONEAGE-22-DOMAIN-EVIDENCE-COVERAGE-CHECKPOINT-R1.json")
        self.assertEqual(x["early_media_bridge"]["player_pet_name_candidates"],20)
        self.assertEqual(x["jss_navigation"]["qualified_pages"],6)
        self.assertEqual(x["jss_navigation"]["link_records"],85)
        self.assertEqual(x["archive_boundary"]["qualified_1999_2002_media_pages"],0)
        self.assertFalse(x["stage_b_implementation_started"])
        self.assertFalse(x["public_wiki_deployment_started"])
        self.assertIn("SAME-BUILD",x["next_priority"])
    def test_archive_custody_receipt(self):
        r=read("research/recovered/STONEAGE-EARLY-MEDIA-ARCHIVE-SNAPSHOT-ACCEPTANCE-R1.json")
        self.assertEqual(r["raw_report_sha256"],
                         hashlib.sha256((ROOT/"research/recovered/STONEAGE-EARLY-MEDIA-ARCHIVE-SNAPSHOT-BOUNDARY-R1.json").read_bytes()).hexdigest())
        self.assertEqual(r["raw_report_git_blob"],"0d5ff5dcb8532626ff40891ff76e92cff378ec26")
        self.assertEqual(r["artifact_zip_bytes"],1094)
        self.assertEqual(r["artifact_id"],12102473238)
        self.assertFalse(r["global_media_source_absence_asserted"])
if __name__=="__main__":
    unittest.main()
