"""PET09: native 2016 C pet-generator semantics, 124 graphic source-only reference.

The remote code was inspected at the pinned GitHub commit. This CI independently
replays only the already accepted numeric source indices, not a 1999/2000 server.
"""
import hashlib
import json
import unittest
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
DATA = "research/pets/PET-DETAIL-EVIDENCE09-2016-PC-BIRTH-GROWTH-124-LV1-REFERENCE-R1.json"
DOC = "docs/pets/TW10-124-2016-PC-SOURCE-PET-BIRTH-GROWTH-REFERENCE.md"

def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

def blob(p):
    b=(ROOT/p).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()

def index(rows, column):
    d=defaultdict(list)
    for x in rows:
        d[x[column]].append(x)
    return d

def rank(s):
    return 0 if s>=100 else 1 if s>=95 else 2 if s>=90 else 3 if s>=85 else 4 if s>=80 else 5

def finger16(x):
    return [x[3],x[4],*x[5:14],*x[14]]

def finger25(x):
    return [int(x[4]),float(x[5]),*[int(t) for t in x[6:15]],*x[15]]

class SourceGradeEarlyPetBirthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load(DATA)
        src=cls.d["source"]["pinned_local_indexes"]
        cls.prior=[load(x["path"]) for x in src]
        cls.registry=cls.prior[2]

    def test_git_source_and_unmodified_historical_current(self):
        for ref in self.d["source"]["pinned_local_indexes"]:
            self.assertEqual(blob(ref["path"]),ref["git_blob"])
        self.assertEqual(blob("docs/CURRENT-STATE.md"),
                         self.d["restrictions"]["current_original_blob"])
        original=self.d["source"]
        self.assertEqual(original["commit"],"57b14e2bb373ba851c14db28a239273e4a8831bb")
        self.assertEqual(original["original_C_files"][0]["sha"],
                         "72e43f44a76db4baa23dfcea568f16d54d3bf620")
        self.assertEqual(original["original_C_files"][1]["sha"],
                         "f12bee31be5ad9b7bd6754201631b441d1e4107e")
        self.assertEqual(original["original_C_files"][2]["sha"],
                         "a86dd72c1d71cef41ce0f1ad228b7cc1832daa90")
        self.assertEqual(self.d["source"]["pinned_local_indexes"][0]["original_2016_enemybase1_blob"],
                         "a19a508975e3a982fada323861b35b2edab79349")

    def test_124_dossiers_replay_195_source_rows_and_theoretical_lv1_bounds(self):
        y,m,reg,_=self.prior
        source=index(y["petflag1_template_tuples"],2)
        instances=index(y["enemy_instances"],2)
        bands=[[450,500],[470,520],[490,540],[510,560],[530,580],[550,600]]
        self.assertEqual(len(self.d["dossiers"]),124)
        self.assertEqual(len(reg["catalog_entries"]),124)
        seen=set()
        lv1_count=0
        for new,origin in zip(self.d["dossiers"],reg["catalog_entries"]):
            self.assertEqual(new["pet_id"],origin["catalog_pet_id"])
            self.assertEqual(new["tw10_name"],origin["original_client_name"])
            g=int(origin["legacy_dossier_key"].split("-G")[1])
            self.assertEqual(new["tw10_graphic"],g)
            self.assertEqual(new["tw10_dossier_md"],origin["visible_dossier_path"])
            self.assertTrue((ROOT/new["tw10_dossier_md"]).is_file())
            self.assertIsNone(new["tw10_verified_official_birth_stats"])
            self.assertEqual(len(new["server2016_candidates"]),len(source[g]))
            self.assertTrue(new["has_Lv1_server2016_instance"])
            for row,p in zip(source[g],new["server2016_candidates"]):
                self.assertEqual(p["source_template_line"],row[0])
                self.assertEqual(p["source_template_id"],row[1])
                self.assertEqual(p["graphic_id"],g)
                self.assertEqual(p["initnum"],row[3])
                self.assertEqual(p["lvup_point"],row[4])
                self.assertEqual(list(p["four_base_values"].values()),row[5:9])
                self.assertEqual(list(p["source_elements"].values()),row[9:13])
                self.assertEqual(p["skill_capacity"],row[13])
                self.assertEqual(p["seven_skill_slots"],row[14])
                base=row[5:9]
                x=sum(base)
                self.assertEqual(p["rank_source_unmodified_sum"],x)
                self.assertEqual(p["rank_from_unmodified_template"],rank(x))
                self.assertEqual(p["rank_levelup_random_band"],bands[rank(x)])
                self.assertEqual(p["level1_precompliance_raw_internal_ability_bounds"], {
                    key:{"min":(base[i]-2)*row[3],"max":(base[i]+12)*row[3]}
                    for i,key in enumerate(("vital","strength","toughness","dexterity"))})
                eligible=[z for z in instances[row[1]]
                          if z[5]==1 and z[3]<=1<=z[4]]
                self.assertEqual(p["static_level1_eligible_enemy_instance_line_numbers"],
                                 [z[0] for z in eligible])
                self.assertEqual(p["static_level1_eligible_enemy_instance_ids"],
                                 [z[1] for z in eligible])
                self.assertTrue(p["early_original_TW10_same_build_verified"] is False)
                lv1_count+=len(eligible)
                seen.add((row[0],row[1]))
        self.assertEqual(len(seen),195)
        self.assertEqual(lv1_count,370)

    def test_crossarchive_exact_matching_preserves_3_exceptions(self):
        y,m,reg,_=self.prior
        byGraphic=index(m["source_rows"]["enemybase.txt"],2)
        exactly=0
        allModels=0
        exceptions=[]
        for d in self.d["dossiers"]:
            mrows=[r for r in byGraphic[d["tw10_graphic"]] if r[3]==1]
            anymatched=False
            for s in d["server2016_candidates"]:
                raw=finger16(next(r for r in y["petflag1_template_tuples"]
                                  if r[0]==s["source_template_line"] and
                                  r[1]==s["source_template_id"]))
                same=[r for r in mrows if finger25(r)==raw]
                self.assertEqual(s["crossarchive_mixed25_exact_numeric_matches"],
                                 [{"row":r[0],"template_id":r[1],
                                   "original_row_sha256":r[16]} for r in same])
                if same:
                    exactly+=1
                    anymatched=True
                allModels+=1
            self.assertEqual(d["has_mixed25_exact_numeric_match"],anymatched)
            if not anymatched:
                exceptions.append(d["pet_id"])
        self.assertEqual(allModels,195)
        self.assertEqual(exactly,152)
        self.assertEqual(exceptions,["PET-000025","PET-000096","PET-000097"])
        self.assertEqual([x["pet_id"] for x in self.d["exceptions_no_strict_crossarchive_match"]],
                         exceptions)

    def test_counts_historic_limits_and_doc_are_consistent(self):
        c=self.d["counts"]
        expected={
            "tw10_source_dossiers":124,
            "server2016_templates_for_tw10_graphics":195,
            "server2016_template_ids_unique":195,
            "server2016_level1_instance_config_rows":370,
            "server2016_templates_with_level1_instance":176,
            "tw10_dossiers_with_server2016_level1_instance":124,
            "server2016_rows_matching_mixed25_numeric_fields":152,
            "tw10_dossiers_with_mixed25_numeric_correspondence":121,
            "tw10_dossiers_without_mixed25_numeric_correspondence":3,
            "official_early_PC_birth_stats_verified":0,
            "new_original_binary_bytes":0,
            "new_official_species":0}
        for k,v in expected.items():
            self.assertEqual(c[k],v,k)
        self.assertIsNone(c["global_official_PC_pet_total"])
        self.assertIsNone(c["overall_percent"])
        self.assertTrue(self.d["restrictions"]["original_tw10_official_fields_stay_null"])
        self.assertTrue(self.d["code_evidence"]["static_2016_source_does_not_confirm_TW10_or_CN182_same_build"])
        self.assertFalse(self.d["code_evidence"]["full_player_visible_HP_ATK_DEF_SPEED_exact_values_derived"])
        doc=(ROOT/DOC).read_text(encoding="utf-8")
        self.assertEqual(doc.count("\n### PET-"),124)
        self.assertIn("2016与混合2.5",doc)
        for p in self.d["dossiers"]:
            self.assertIn("### "+p["pet_id"],doc)
            self.assertIn(p["tw10_name"],doc)
        self.assertIn("TW10-124-2016-PC-SOURCE-PET-BIRTH-GROWTH-REFERENCE.md",
                      (ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
