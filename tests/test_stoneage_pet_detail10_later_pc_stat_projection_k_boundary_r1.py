"""PET-DETAIL10: source-pinned 2016 baseline projections and original TW10 K contract.

This tests derived source models only. It does not execute old clients/servers and
never promotes the later PC server's stats to early official TW10 attributes.
"""
import hashlib
import json
import itertools
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH="research/pets/PET-DETAIL-EVIDENCE10-LATER2016-124-HP-ATK-DEF-QUICK-AND-TW10-K-BOUNDARY-R1.json"
DOC="docs/pets/TW10-124-2016-BASE-UI-STATS-AND-K-PROTOCOL-CROSSWALK.md"
METRICS={"max_hp":([4,1,1,1],100),
         "attack":([2,20,2,1],2000),
         "defense":([2,2,20,1],2000),
         "quick":([0,0,0,1],100)}
AXES=("vital","strength","toughness","dexterity")

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def gitblob(path):
    raw=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+bytes([0])+raw).hexdigest()

def bounds(v,init,weights,div):
    subtotal=sum(a*b for a,b in zip(v,weights))
    total=sum(weights)
    return (init*(subtotal-2*total+10*min(weights)),
            init*(subtotal+2*total+10*max(weights)))

class PetDetail10CrossSourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read(PATH)
        cls.prev=read(cls.d["sources"]["previous_pet09"]["path"])
        cls.early=read(cls.d["sources"]["original_TW10_client_K_parser"]["path"])
        cls.petreg=read(cls.d["sources"]["pet_registry"]["path"])

    def test_git_pins_and_untouched_historic_blob(self):
        for key in ("previous_pet09","original_TW10_client_K_parser","pet_registry"):
            spec=self.d["sources"][key]
            self.assertEqual(gitblob(spec["path"]),spec["git_blob"])
        self.assertEqual(gitblob("docs/CURRENT-STATE.md"),
                         self.d["limits"]["original_current_state_blob"])
        self.assertEqual(self.d["sources"]["later2016_exact_commit"],
                         "57b14e2bb373ba851c14db28a239273e4a8831bb")
        self.assertEqual(self.d["sources"]["later2016_file_git_blob"],
                         "5a044dc68bb76758b2a757a8e83c10b93578be31")
        self.assertEqual(self.d["sources"]["original_TW10_client_K_parser"]["early_exe_sha256"],
                         self.early["original_source"]["exe_sha256"])

    def test_replay_all_124_x_195_from_pinned_2016_model(self):
        d=self.d
        self.assertEqual(len(d["pet_source_views"]),124)
        total=0
        for idx,(p,old,reg) in enumerate(zip(d["pet_source_views"],self.prev["dossiers"],self.petreg["catalog_entries"])):
            self.assertEqual(p["pet_id"],old["pet_id"])
            self.assertEqual(p["pet_id"],reg["catalog_pet_id"])
            self.assertEqual(p["tw10_original_album_name"],old["tw10_name"])
            self.assertEqual(p["tw10_original_graphic"],old["tw10_graphic"])
            self.assertEqual(p["tw10_dossier_md"],reg["visible_dossier_path"])
            self.assertIsNone(p["original_early_TW10_HP_ATK_DEF_QUICK_birth_range"])
            self.assertEqual(len(p["candidates"]),len(old["server2016_candidates"]))
            for r,src in zip(p["candidates"],old["server2016_candidates"]):
                self.assertEqual(r["source_2016_template_id"],src["source_template_id"])
                self.assertEqual(r["source_2016_physical_line"],src["source_template_line"])
                self.assertEqual(r["source_INITNUM"],src["initnum"])
                self.assertEqual(r["source_BASE"],src["four_base_values"])
                self.assertFalse(r["verified_early_TW10_official_UI_birth_stats"])
                base=[r["source_BASE"][key] for key in AXES]
                for stat,(weights,div) in METRICS.items():
                    z=r["baseline_stat_envelopes"][stat]
                    lo,hi=bounds(base,r["source_INITNUM"],weights,div)
                    self.assertEqual(z["source_min_numerator"],lo)
                    self.assertEqual(z["source_max_numerator"],hi)
                    self.assertEqual(z["denominator"],div)
                    self.assertEqual(z["nominal_min"],lo//div)
                    self.assertEqual(z["nominal_max"],hi//div)
                    self.assertLessEqual(z["nominal_min"],z["nominal_max"])
                total+=1
        self.assertEqual(total,195)
        self.assertEqual(d["counts"]["source_only_projection_sets"],4*total)

    def test_exhaustive_urli_first_pet_bonus_and_offset_endpoints(self):
        # Verify each mathematical envelope for a representative first source
        # using all combinations of 10 shared allocated points (286), and
        # 2^4 extreme independent initial offsets (16). No Monte Carlo.
        sample=self.d["pet_source_views"][0]["candidates"][0]
        self.assertEqual(sample["source_2016_template_id"],1)
        self.assertEqual(sample["source_INITNUM"],10)
        base=[sample["source_BASE"][key] for key in AXES]
        allocs=[(a,b,c,10-a-b-c)
                for a in range(11) for b in range(11-a)
                for c in range(11-a-b)]
        self.assertEqual(len(allocs),286)
        for name,(w,div) in METRICS.items():
            vals=[]
            for delta in itertools.product((-2,2),repeat=4):
                for bonus in allocs:
                    components=[sample["source_INITNUM"]*(base[i]+delta[i]+bonus[i])
                                for i in range(4)]
                    vals.append(sum(w[i]*components[i] for i in range(4))//div)
            z=sample["baseline_stat_envelopes"][name]
            self.assertEqual(min(vals),z["nominal_min"],name)
            self.assertEqual(max(vals),z["nominal_max"],name)
        self.assertEqual(sample["baseline_stat_envelopes"]["max_hp"]["nominal_min"],12)
        self.assertEqual(sample["baseline_stat_envelopes"]["max_hp"]["nominal_max"],18)

    def test_early_original_K_receiver_and_later_K_sender_not_falsely_merged(self):
        evidence=self.d["k_packet_source_alignment"]
        items=evidence["fields"]
        self.assertEqual(len(items),20)
        orig=self.early["k_parser"]["field_map"]
        self.assertEqual([x["token"] for x in items],[x["token"] for x in orig])
        self.assertEqual([x["tw10_early_field"] for x in items],
                         [x["name_from_early_lineage"] for x in orig])
        self.assertEqual([x["tw10_source_struct_offset"] for x in items],
                         [x["struct_offset"] for x in orig])
        self.assertEqual([x["token"] for x in items if x["semantic_match"]],
                         list(range(2,20)))
        self.assertEqual(evidence["first_schema_difference_at_token"],20)
        self.assertEqual(evidence["expected_tw10_tokens20_21"],["name","free_name"])
        self.assertEqual(evidence["later2016_without_showfusion_tokens20_22"],
                         ["transmigration","name","free_name"])
        self.assertEqual(evidence["later2016_with_showfusion_tokens20_23"],
                         ["transmigration","fusion_rebirth","name","free_name"])
        self.assertTrue(evidence["cannot_declare_later2016_full_K_compatible_with_TW10"])

    def test_document_nav_and_negative_official_claims(self):
        d=self.d
        self.assertEqual(d["counts"]["tw10_client_named_dossiers"],124)
        self.assertEqual(d["counts"]["later2016_source_template_candidates"],195)
        self.assertEqual(d["counts"]["source_only_projection_sets"],780)
        self.assertEqual(d["counts"]["matching_early_later_K_numeric_fields"],18)
        self.assertEqual(d["counts"]["earliest_TW10_official_birth_stat_profiles_confirmed"],0)
        self.assertEqual(d["counts"]["new_original_server_pet_masters"],0)
        self.assertEqual(d["counts"]["new_official_species_confirmed"],0)
        self.assertIsNone(d["counts"]["overall_percent"])
        self.assertFalse(d["later2016_baseline_math"]["original_early_official_birth_projection_verified"])
        self.assertTrue(d["limits"]["all_early_official_attribute_fields_untouched"])
        doc=(ROOT/DOC).read_text(encoding="utf-8")
        self.assertEqual(doc.count("\n### PET-"),124)
        for p in d["pet_source_views"]:
            self.assertIn("### "+p["pet_id"],doc)
            self.assertIn(p["tw10_original_album_name"],doc)
        idx=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("TW10-124-2016-BASE-UI-STATS-AND-K-PROTOCOL-CROSSWALK.md",idx)

if __name__=="__main__":
    unittest.main()
