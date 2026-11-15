"""PET44: test community-selector candidate cohorts against raw source-derived indices."""
import json
import unittest
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"

def load(path):
    return json.loads((REC / path).read_text(encoding="utf-8"))

class TestPet44(unittest.TestCase):
    def test_source_exact_partition_and_duplicate_retention(self):
        out = load("STONEAGE-PET44-LATER-CLIENT-PETFLAG1-GAP-CANDIDATES-R1.json")
        p01 = load("STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json")
        r28 = load("tw85-spr137-r28/SOURCE-DERIVED-R28.json")
        album = load("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        reg = {v[0]: v for v in p01["graphic_registry"]}
        names = {x["graphic_number"] for x in album["records"]}
        cn = {x["spr_no"]:x for x in r28["joins"]["reference_relationships"]["CN50"]}
        tw = {x["spr_no"]:x for x in r28["joins"]["reference_relationships"]["TW10"]}
        groups = (
            out["later_source_graphics_without_TW1_index"],
            out["community_petflag1_graphics_missing_all_four_indexes"],
            out["tw1_sprite_groups_without_same_build_album_name"],
        )
        self.assertEqual([len(g) for g in groups], [412,56,6])
        self.assertEqual(len(reg), 598)
        ids = [r["graphic_number"] for g in groups for r in g]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), set(reg)-names)
        masks = Counter()
        for no,entry in reg.items():
            mask = "+".join(k for k,vals in zip(("TW1","CN50","TW85","MIXED25"),entry[2:6]) if vals) or "NONE"
            masks[mask] += 1
        self.assertEqual(dict(masks), out["carrier_masks"])
        for group in groups:
            for row in group:
                g = row["graphic_number"]
                original = reg[g]
                self.assertEqual(row["community_2016_petflag1_template_lines"], original[1])
                for key,values in zip(("TW1","CN50","TW85","MIXED25"),original[2:6]):
                    self.assertEqual(row["indexes"][key], values)
                self.assertEqual(row["tw85_exact_spr_segment_sha256_by_occurrence"],original[6])
                self.assertEqual(len(original[4]), len(original[6]))
                self.assertFalse(row["tw1_same_build_pet_album_name_verified"])
                self.assertFalse(row["official_live_release_confirmed"])
                self.assertIsNone(row["official_first_release_year"])
                self.assertFalse(row["new_original_pixel_replay"])
                if original[3]:
                    self.assertEqual(cn[g]["relation"],"SAME_ID_AND_EXACT_FULL_SPR_SEGMENT")
                    self.assertEqual(cn[g]["reference_index"],original[3][0])
                    self.assertEqual(cn[g]["tw85_index"],original[4][0])
                    self.assertTrue(row["cn50_tw85_exact_spr"])
                else:
                    self.assertFalse(row["cn50_tw85_exact_spr"])
                if original[2]:
                    self.assertEqual(tw[g]["relation"],"SAME_ID_AND_EXACT_FULL_SPR_SEGMENT")
                    self.assertEqual(tw[g]["reference_index"],original[2][0])
                    self.assertEqual(tw[g]["tw85_index"],original[4][0])
                    self.assertTrue(row["tw1_tw85_exact_spr"])
                else:
                    self.assertFalse(row["tw1_tw85_exact_spr"])
        self.assertEqual({x["graphic_number"] for x in groups[0]}, {g for g,v in reg.items() if not v[2] and v[4]})
        self.assertEqual({x["graphic_number"] for x in groups[1]}, {g for g,v in reg.items() if not any(v[2:6])})
        self.assertEqual({x["graphic_number"] for x in groups[2]}, {g for g,v in reg.items() if v[2] and g not in names})
        self.assertEqual(sorted(x["graphic_number"] for x in groups[2]), [100015,100018,100401,100432,100451,100454])
        summ = out["summary"]
        self.assertEqual(summ["later_CN50_TW85_exact_full_spr"],214)
        self.assertEqual(summ["later_TW85_physical_spr_group_occurrences"],416)
        self.assertEqual(summ["later_TW85_duplicate_numeric_keys"],[{"graphic_number":101866,"occurrences":3},{"graphic_number":101990,"occurrences":2},{"graphic_number":101991,"occurrences":2}])
        self.assertEqual(summ["official_pet_species_added"],0)
        self.assertIsNone(summ["total_historical_official_pet_species"])

    def test_source_gates_and_chronology(self):
        out=load("STONEAGE-PET44-LATER-CLIENT-PETFLAG1-GAP-CANDIDATES-R1.json")
        self.assertEqual(out["year_frontier"],2000)
        self.assertEqual(out["year_frontier_status"],"OPEN")
        self.assertTrue(all(value is False for value in out["guardrails"].values()))
        self.assertEqual(out["current_state_blob_preserved"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual((out["stage_a"],out["stage_b_wiki"],out["r79"],out["overall_percent"]),("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))
        self.assertIn("PET44 2026-11-15",(ROOT/"docs/STONEAGE-PET-CHRONOLOGICAL-RESTORATION-ORDER-R1.md").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
