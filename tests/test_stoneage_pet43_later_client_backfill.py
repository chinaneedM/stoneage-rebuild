"""PET43: recompute exact sprite carryover while keeping historic official issuance open."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
def load(name):
    return json.loads((REC/name).read_text(encoding="utf-8"))
class TestPet43(unittest.TestCase):
    def test_cross_carrier_names_and_exact_spr(self):
        report=load("STONEAGE-PET43-LATER-CLIENT-SPR-BACKFILL-R1.json")
        album=load("STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        p01=load("STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json")
        r28=load("tw85-spr137-r28/SOURCE-DERIVED-R28.json")
        named={x["graphic_number"]:x for x in album["records"]}
        index={x[0]:x for x in p01["graphic_registry"]}
        tw={x["spr_no"]:x for x in r28["joins"]["reference_relationships"]["TW10"]}
        cn={x["spr_no"]:x for x in r28["joins"]["reference_relationships"]["CN50"]}
        rows={x["tw1_graphic"]:x for x in report["records"]}
        self.assertEqual((len(named),len(rows)),(124,124))
        self.assertEqual(set(rows),set(named))
        for num,row in rows.items():
            native=named[num]; source=index[num]; i=row["spr_group_indexes"]
            self.assertEqual(row["tw1_original_name"],native["name_as_written"])
            self.assertEqual(row["tw1_name_row_sha256"],native["source_row_sha256"])
            self.assertEqual(row["tw1_full_spr_sha256"],native["spr_original_segment_sha256"])
            self.assertEqual(row["tw1_full_spr_sha256"],source[6][0])
            for key,index_pos in (("TW1",2),("CN50",3),("TW85",4),("MIXED25",5)):
                self.assertEqual(source[index_pos],[i[key]])
            self.assertEqual(tw[num]["reference_index"],i["TW1"])
            self.assertEqual(cn[num]["reference_index"],i["CN50"])
            self.assertEqual(tw[num]["tw85_index"],i["TW85"])
            self.assertEqual(cn[num]["tw85_index"],i["TW85"])
            self.assertEqual(tw[num]["relation"],"SAME_ID_AND_EXACT_FULL_SPR_SEGMENT")
            self.assertEqual(cn[num]["relation"],"SAME_ID_AND_EXACT_FULL_SPR_SEGMENT")
            self.assertFalse(row["official_live_release_confirmed"])
            self.assertFalse(row["later_build_official_certified"])
    def test_no_backdating_of_official_release_or_2000_year(self):
        j=load("STONEAGE-PET43-LATER-CLIENT-SPR-BACKFILL-R1.json")
        for k in ("early_named_graphic_cohort","found_same_numeric_group_in_CN50","found_same_numeric_group_in_TW85","found_same_numeric_group_in_MIXED25","TW1_TW85_exact_full_SPR_group","CN50_TW85_exact_full_SPR_group"):
            self.assertEqual(j["observations"][k],124)
        self.assertEqual(j["observations"]["new_qualified_official_live_pet_releases"],0)
        self.assertIsNone(j["observations"]["historical_pet_species_count"])
        self.assertFalse(j["guardrails"]["all_later_versions_contain_every_older_pet"])
        self.assertFalse(j["guardrails"]["same_animation_implies_official_pet_issuance"])
        self.assertFalse(j["guardrails"]["early_year_closure"])
        self.assertFalse(j["guardrails"]["new_commercial_client_bytes_recovered"])
        self.assertEqual(j["current_state_blob_preserved"],"c89e0e33537990aa2132b47c40fef49a985a935c")
        year=load("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
        self.assertEqual(year["current_frontier"]["year"],2000)
        self.assertIn("PET43-LATER-CLIENT-REVERSE-BACKFILL-20261115",[r["id"] for r in year["root_source_census_receipts"]])
        self.assertIn("## 24. Source-bounded later-client reverse backfill",(ROOT/"docs/PROJECT-CONTINUITY-PROTOCOL-R1.md").read_text(encoding="utf-8"))
if __name__=="__main__":
    unittest.main()
