"""PET88: source-bounded first pass on 2012 original PC pets, not annual closure."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"


def read(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


class PET88Year2012(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("STONEAGE-PET88-YEAR2012-CN-85-25-ORIGINAL-CLIENT-AND-NAMED-PETS-FIRST-PASS-R1.json")
        cls.q = read("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")

    def test_2012_partial_frontier_and_forward_receipts(self):
        a, q = self.a, self.q
        y = q["yearly_work_queue"][2012 - 1999]
        self.assertEqual((a["year"], a["year_frontier_before"], a["year_frontier_after"]), (2012, 2012, 2012))
        self.assertGreaterEqual(q["current_frontier"]["year"], 2012)
        self.assertIn(y["research_gate"], ("NOT_YEAR_AUDITED", "SOURCE_BOUNDED_REVIEWED"))
        self.assertFalse(a["historically_complete"])
        self.assertEqual(a["year_review_status"], "NOT_YEAR_AUDITED")
        self.assertIsNone(a["global_species_population_2012"])
        self.assertIsNone(a["first_release_species_count_2012"])
        receipts = [x["id"] for x in q["root_source_census_receipts"]]
        self.assertEqual(receipts.count(a["id"]), 1)
        self.assertEqual(len(receipts), len(set(receipts)))
        self.assertEqual(sum(x["id"] == a["id"] for x in y["partial_source_review_receipts"]), 1)

    def test_client_publish_listing_is_not_original_bytes(self):
        a = self.a
        c = a["client_2012_CN"]
        self.assertEqual(c["update_date"], "2012-10-09")
        self.assertEqual(c["page_header_2010_not_download_version_date"], True)
        self.assertEqual((c["version"], c["file_size_on_page"]), ("V1.200.012", "1.34GB"))
        self.assertEqual(c["published_md5"], "2a1743e07e4f97f1b2e337048918da6a")
        self.assertEqual(c["observed_mirror_result"], "HTTP_502")
        self.assertFalse(c["md5_recalculated"])
        self.assertEqual(c["actual_original_bytes_acquired"], 0)
        self.assertFalse(c["same_build_85_vs_25_attribution_verified"])
        self.assertEqual((a["new_authenticated_original_client_bytes"], a["new_native_pet_ids"],
                          a["new_original_2012_sprites"], a["new_actual_original_server_pet_grants"]),
                         (0, 0, 0, 0))

    def test_cn_pet_claims_not_species_and_per_version(self):
        a = self.a
        self.assertEqual(len(a["sources"]), 13)
        self.assertEqual(len(a["named_pet_source_mentions"]), 11)
        self.assertEqual(set(a["cn_source_boundary"]["two_new_year_godbeast_names"]), {"麒麟", "貔貅"})
        self.assertEqual(a["cn_source_boundary"]["cn85_circus_named_reward"], "怀肯沃")
        self.assertEqual(a["cn_source_boundary"]["cn25_circus_named_reward"], "塔斯夫")
        self.assertEqual(a["cn_source_boundary"]["jan16_chase_reward_cn85"], "PET_EQUIPMENT")
        self.assertEqual(a["cn_source_boundary"]["jan16_chase_reward_cn25"], "YEAR_BEAST_EXCHANGE_VOUCHER")
        self.assertTrue(a["cn_source_boundary"]["麒麟的牙骨_貔貅的牙骨_are_items_not_pets"])
        self.assertTrue(a["cn_source_boundary"]["二代玛蕾菲雅_is_pet_rebirth_stage_not_sequel_game"])
        self.assertTrue(a["cn_source_boundary"]["MM_repeated_two_articles_not_two_species"])
        mm = [x for x in a["named_pet_source_mentions"] if x["name"] == "玛蕾菲雅"]
        self.assertEqual(len(mm), 2)
        self.assertEqual({x["source_id"] for x in mm}, {"CN2012FEB17", "CN2012MAY15"})
        self.assertTrue(all(x["native_pet_id"] is None and not x["first_release_in_2012_proven"]
                            for x in a["named_pet_source_mentions"]))

    def test_taiwan_honglong_korea_japan_separation(self):
        a = self.a
        self.assertEqual(set(a["region_gaps"]), {"CN", "TW", "HK_MO", "KR", "JP", "OTHER"})
        self.assertTrue(all(a["source_evidence_gates"].values()))
        klass = {x["id"]: x["source_class"] for x in a["sources"]}
        self.assertTrue(klass["TW2012LATE"].startswith("LATER_PLAYER"))
        self.assertTrue(klass["HKMO2012LATE"].startswith("LATER_PLAYER"))
        self.assertTrue(klass["KR2012LATE"].startswith("LATER_FAN"))
        self.assertEqual(klass["CN2012OCT09"], "SOURCE_PAGE_CLIENT_METADATA_ONLY")
        self.assertEqual(klass["JP2012BOUND"], "EARLIER_SERVICE_HISTORY_ONLY")
        self.assertTrue(all(x["original_native_pet_ids_confirmed"] == 0 and
                            not x["real_reward_execution_verified"] for x in a["sources"]))

    def test_native_state_blob_untouched_and_stage(self):
        a = self.a
        raw = (ROOT / "docs" / "CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(raw), a["startup"]["current_bytes"])
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
        self.assertEqual(sha, a["startup"]["current_git_blob"])
        self.assertTrue(a["historical_CURRENT_untouched"])
        self.assertEqual((a["stage_A"], a["stage_B_wiki"], a["r79"], a["overall_percent"]),
                         ("7_PARTIAL_2_OPEN", "GATED", "PAUSED_NON_BLOCKING", None))


if __name__ == "__main__":
    unittest.main()
