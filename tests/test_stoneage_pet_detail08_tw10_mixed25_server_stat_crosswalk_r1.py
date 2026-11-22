"""PET-DETAIL08 source-grade test: full 124 TW1 x 297 MIXED25 candidate template replay."""
import hashlib
import json
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = "research/pets/PET-DETAIL-EVIDENCE08-TW10-MIXED25-124-GRAPHIC-NUMERIC-SERVER-TEMPLATE-REFERENCE-R1.json"
DOC = "docs/pets/TW10-124-MIXED25-SERVER-TEMPLATE-STATS-REFERENCE.md"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def git_blob(path):
    raw = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + bytes([0]) + raw).hexdigest()

class PetDetail08SourceOnlyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load(DATA)
        s = cls.d["source"]
        cls.reg = load(s["tw10_registry_path"])
        cls.mixed = load(s["mixed25_988_template_source_path"])
        cls.p13 = load(s["mixed25_PET13_independent_same_archive_name_source"])

    def test_current_blob_preserved_and_source_gits_pinned(self):
        s = self.d["source"]
        self.assertEqual(git_blob(s["tw10_registry_path"]), s["tw10_registry_git_blob_sha"])
        self.assertEqual(git_blob(s["mixed25_988_template_source_path"]),
                         s["mixed25_988_template_source_git_blob_sha"])
        self.assertEqual(git_blob(s["mixed25_PET13_independent_same_archive_name_source"]),
                         s["mixed25_PET13_git_blob_sha"])
        self.assertEqual(s["mixed25_RAR_sha256"],self.mixed["preserved_original_rar"]["sha256"])
        self.assertEqual(s["mixed25_original_enemybase_sha256"],
                         self.mixed["verified_original_archive_members"]["enemybase.txt"]["sha256"])
        self.assertEqual(s["mixed25_original_petskill_sha256"],
                         self.mixed["verified_original_archive_members"]["petskill.txt"]["sha256"])
        self.assertEqual(git_blob("docs/CURRENT-STATE.md"),
                         self.d["limits"]["original_CURRENT_state_blob_unmodified"])

    def test_all_tw10_graphics_join_to_each_raw_988_row_unmodified(self):
        raw = defaultdict(list)
        for row in self.mixed["source_rows"]["enemybase.txt"]:
            self.assertEqual(len(row), 17)
            raw[row[2]].append(row)
        self.assertEqual(sum(len(v) for v in raw.values()), 988)
        self.assertEqual(len(self.d["pet_dossiers"]), 124)
        self.assertEqual(len(self.reg["catalog_entries"]), 124)
        observed_pairs = set()
        for e,origin in zip(self.d["pet_dossiers"], self.reg["catalog_entries"]):
            self.assertEqual(e["pet_id"],origin["catalog_pet_id"])
            self.assertEqual(e["tw10_name"],origin["original_client_name"])
            self.assertEqual(e["tw10_graphic_number"],int(origin["legacy_dossier_key"].split("-G")[1]))
            self.assertEqual(e["tw10_dossier_md"],origin["visible_dossier_path"])
            self.assertTrue((ROOT / e["tw10_dossier_md"]).is_file())
            self.assertEqual(e["tw10_obs_ids"],origin["observations"])
            self.assertEqual(e["source_relation"],
                             "IDENTICAL_NUMERIC_GRAPHIC_ID_DIFFERENT_ARCHIVE_NOT_SAME_SPECIES")
            self.assertIsNone(e["verified_TW1_birth_stats"])
            self.assertIsNone(e["verified_TW1_same_server_pet_id"])
            orig_rows = raw[e["tw10_graphic_number"]]
            self.assertEqual(len(e["candidates"]),len(orig_rows))
            self.assertGreater(len(orig_rows),0)
            self.assertEqual(e["counts"]["flag1"], sum(x[3]==1 for x in orig_rows))
            self.assertEqual(e["counts"]["flag0"], sum(x[3]==0 for x in orig_rows))
            self.assertEqual(e["counts"]["distinct_base_vectors"],
                             len({tuple(x[6:10]) for x in orig_rows}))
            for src,joined in zip(orig_rows,e["candidates"]):
                self.assertEqual(joined["source_line_1based"],src[0])
                self.assertEqual(joined["source_template_id"],src[1])
                self.assertEqual(joined["graphic_number"],src[2])
                self.assertEqual(joined["PETFLG_literal"],src[3])
                self.assertEqual(joined["INITNUM_literal"],src[4])
                self.assertEqual(joined["LVUP_literal"],src[5])
                self.assertEqual(list(joined["base_components_raw"].values()),src[6:10])
                self.assertEqual(list(joined["element_components_raw"].values()),src[10:14])
                self.assertEqual(joined["skill_capacity_literal"],src[14])
                self.assertEqual(joined["seven_skill_slot_ids_raw"],src[15])
                self.assertEqual(joined["cp950_comma_normalized_56column_sha256"],src[16])
                self.assertFalse(joined["official_TW1_species_and_stats_verified"])
                self.assertFalse(joined["original_same_deployment_verified"])
                self.assertEqual(len(joined["skill_definition_links"]),7)
                observed_pairs.add((joined["source_line_1based"],joined["source_template_id"]))
        self.assertEqual(len(observed_pairs),297)
        self.assertEqual(len(raw),self.mixed["table_summaries"]["enemybase.txt"]["distinct_graphic_ids_all_flags"])

    def test_same_archive_skill_and_named_subset_links(self):
        definitions = {v[1]:(v[0],v[2]) for v in self.mixed["source_rows"]["petskill.txt"]}
        shortnames = {v["skill_id"]:v["source_short_name"] for v in
                      self.p13["same_source_original_petskill_short_labels_private_verified"]}
        source_names = {v["original_template_numeric_ID"]:v for v in self.p13["templates"]}
        got_names = []
        all_skills = []
        for e in self.d["pet_dossiers"]:
            for row in e["candidates"]:
                r = source_names.get(row["source_template_id"])
                recovered = row["source_original_template_name_recovered_via_PET13"]
                qualifies = (r is not None and r["original_graphic_numeric_ID"]==row["graphic_number"]
                            and r["original_56_column_normalized_sha256"]==
                            row["cp950_comma_normalized_56column_sha256"])
                if qualifies:
                    self.assertEqual(recovered["name"],r["mixed25_configured_original_name"])
                    self.assertEqual(recovered["row_sha256"],
                                     r["original_physical_line_including_newline_sha256"])
                    got_names.append((e["pet_id"],r["mixed25_configured_original_name"]))
                else:
                    self.assertIsNone(recovered)
                for value,link in zip(row["seven_skill_slot_ids_raw"],row["skill_definition_links"]):
                    if value is None or value<=0:
                        self.assertIsNone(link)
                        continue
                    all_skills.append(value)
                    self.assertEqual(link["skill_id"],value)
                    self.assertEqual(link["definition"]["line"],definitions[value][0])
                    self.assertEqual(link["definition"]["sha"],definitions[value][1])
                    self.assertEqual(link["short_label"],shortnames.get(value))
        self.assertCountEqual(got_names,[("PET-000064","卡特利奴"),("PET-000086","巨大瑪恩摩")])
        self.assertEqual(len(all_skills),708)
        self.assertEqual(len(set(all_skills)),37)
        self.assertTrue(all(x in definitions for x in all_skills))
        self.assertEqual(self.d["counts"]["undefined_skill_ids"],[])

    def test_counts_and_limits_prevent_false_birth_stat_promotion(self):
        c = self.d["counts"]
        for k,value in {"original_tw10_named_dossiers":124,"graphic_number_matches":124,
                        "templates_in_all_matches":297,"multi_template_graphics":88,
                        "single_template_graphics":36,"petflag1":182,"petflag0":115,
                        "positive_skill_slots":708,"distinct_positive_skill_ids":37,
                        "verified_distinct_same_archive_original_template_names":2,
                        "new_official_original_initial_attribute_records":0,
                        "new_official_original_pet_ids":0,"new_original_binary_bytes":0,
                        "fully_verified_dossiers":0}.items():
            self.assertEqual(c[k],value,k)
        self.assertIsNone(c["global_official_PC_pet_count"])
        self.assertIsNone(c["overall_percent"])
        for key,value in self.d["limits"].items():
            if key=="original_CURRENT_state_blob_unmodified":
                continue
            self.assertTrue(value,key)
        self.assertIn("cross-build",self.d["next"].lower())

    def test_human_reference_and_master_index_are_navigable(self):
        text = (ROOT / DOC).read_text(encoding="utf-8")
        index = (ROOT / "docs/pets/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("TW10-124-MIXED25-SERVER-TEMPLATE-STATS-REFERENCE.md",index)
        self.assertEqual(text.count("\n### PET-"),124)
        for e in self.d["pet_dossiers"]:
            self.assertIn("### "+e["pet_id"],text)
            self.assertIn(e["tw10_name"],text)
            self.assertIn(e["tw10_dossier_md"].replace("docs/pets/",""),text)
        self.assertIn("卡特利奴",text)
        self.assertIn("巨大瑪恩摩",text)
        self.assertIn("不是",text)

if __name__=="__main__":
    unittest.main()
