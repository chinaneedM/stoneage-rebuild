"""PET-DETAIL15: web-text candidate skill evidence never replaces original TW1 official nulls."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECEIPT="research/pets/PET-DETAIL-EVIDENCE15-SIX-TW10-EARLY-PC-SKILL-CLAIMS-R1.json"
REPORT="docs/continuity/STONEAGE-PET-DETAIL15-SIX-EARLY-PC-SKILL-CLAIM-CROSSWALK-20261122.md"

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def gitblob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class PetDetail15EarlySkillCandidates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=read(RECEIPT)

    def test_prior_origins_are_pinned_and_historical_current_is_unchanged(self):
        data=self.data
        for item in data["prior_pinned_evidence"].values():
            self.assertEqual(gitblob(item["path"]),item["git_blob"])
        self.assertEqual(gitblob("docs/CURRENT-STATE.md"),data["guards"]["unchanged_original_current_git_blob"])
        self.assertFalse(data["source_boundary"]["original_2001_html_bytes_recovered"])
        self.assertFalse(data["source_boundary"]["tw10_original_server_skill_master_recovered"])
        self.assertFalse(data["source_boundary"]["original_TW10_W_packet_captured"])

    def test_eight_source_pages_not_synthetic_official_masters(self):
        d=self.data
        src=d["sources"]
        self.assertEqual(len(src),8)
        self.assertEqual(len({s["id"] for s in src}),8)
        for s in src:
            self.assertTrue(s["url"].startswith("https://"))
            self.assertFalse(s["original_publication_html_bytes_authenticated"])
            self.assertFalse(s["early_TW10_official_build_proven"])
        lookup={s["id"]:s for s in src}
        self.assertEqual(lookup["fto"]["byline"],"fto")
        self.assertEqual(lookup["milk"]["byline"],"俄罗斯牛奶")
        self.assertTrue(d["source_boundary"]["fto_claim_located_inside_rumor_section"])
        for k in ("p02","p03","p06"):
            self.assertIsNone(lookup[k]["display_date"])
        self.assertEqual(lookup["sina2003"]["display_date"],"2003-04-03")
        self.assertEqual(lookup["sina2004"]["display_date"],"2004-02-23")
        self.assertTrue(d["source_boundary"]["later_sina_and_undated_17173_page_can_be_dependent"])

    def test_exact_six_original_client_profiles_and_eighteen_source_claims(self):
        d=self.data
        pets=d["pet_profiles"]
        self.assertEqual(len(pets),6)
        self.assertEqual([p["pet_id"] for p in pets],
                         ["PET-000006","PET-000007","PET-000011","PET-000013","PET-000024","PET-000025"])
        self.assertEqual([p["tw10_graphic"] for p in pets],[100255,100256,100260,100262,100273,100274])
        self.assertEqual(sum(len(p["source_claims"]) for p in pets),18)
        self.assertEqual(d["counts"]["individual_page_claim_rows"],18)
        self.assertEqual(d["counts"]["pet_profiles_with_new_textual_links"],6)
        source_ids={s["id"] for s in d["sources"]}
        for p in pets:
            profile=read(p["json_path"])
            doc=(ROOT/p["md_path"]).read_text(encoding="utf-8")
            self.assertEqual(profile["profile_id"],p["pet_id"])
            self.assertEqual(profile["names"]["original_client"],p["tw10_literal"])
            self.assertEqual(profile["appearance"]["graphic_number"],p["tw10_graphic"])
            self.assertEqual(profile["version_scope"]["source_observation_id"],p["observation_id"])
            self.assertFalse(profile["actual_official_pet_identity"]["official_living_pet_release_proven"])
            self.assertEqual(profile["skills"]["status"],"OPEN_NOT_PROVEN")
            for key in ("innate_at_acquisition","skill_slots","learnable_skills","skill_ids_with_same_build_master","effects_and_formula"):
                self.assertIsNone(profile["skills"][key])
            self.assertIn("PET-DETAIL15｜",doc)
            self.assertIn("PARTIAL",doc)
            for c in p["source_claims"]:
                self.assertIn(c["source_id"],source_ids)
                self.assertFalse(c["official_innate_or_learned_confirmed"])
                self.assertIn(next(s for s in d["sources"] if s["id"]==c["source_id"])["url"],doc)

    def test_2001_turtle_innate_rumor_vs_bui_learn_and_undated_slots(self):
        d=self.data
        p={x["pet_id"]:x for x in d["pet_profiles"]}
        turtle=p["PET-000025"]["source_claims"]
        fto=next(x for x in turtle if x["source_id"]=="fto")
        self.assertEqual(fto["grade"],"INNATE_WORDING_IN_HEARSAY_SECTION")
        self.assertEqual(fto["skill_names"],["石化攻击"])
        self.assertTrue(d["source_boundary"]["fto_claim_located_inside_rumor_section"])
        bui=p["PET-000007"]["source_claims"]
        self.assertEqual(next(x for x in bui if x["source_id"]=="milk")["grade"],"HAS_SKILL_NOT_BORN")
        self.assertEqual(next(x for x in bui if x["source_id"]=="qa")["grade"],"LEARNING_ADVICE_NOT_BORN")
        self.assertEqual(next(x for x in bui if x["source_id"]=="sina2003")["grade"],"UNLISTED_NOT_PROOF_ABSENCE")
        self.assertTrue(d["source_boundary"]["undated_5_6_7_skill_capacity_not_early_original_native_limit"])
        self.assertEqual(d["unlinked_name_only"][0]["literal"],"暴龙")
        self.assertIsNone(d["unlinked_name_only"][0]["tw10_pet_profile"])

    def test_no_false_completed_species_or_skill_and_crosswalk_document(self):
        d=self.data
        counts=d["counts"]
        self.assertEqual(counts["tw10_all_profiles_partial"],124)
        self.assertEqual(counts["tw10_historically_fully_verified"],0)
        for k in ("early_official_birth_skill_names_new","original_official_skill_ids_new","official_pet_species_new"):
            self.assertEqual(counts[k],0)
        self.assertIsNone(d["guards"]["overall_percent"])
        report=(ROOT/REPORT).read_text(encoding="utf-8")
        idx=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("PET-DETAIL15",report)
        self.assertIn("PET-DETAIL15",idx)
        self.assertIn("石龟",report)
        self.assertIn("布伊",report)

if __name__=="__main__":
    unittest.main()
