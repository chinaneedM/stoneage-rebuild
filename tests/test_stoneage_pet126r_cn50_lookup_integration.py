import unittest
from tools.stoneage_pet16_lookup import (
    CN50_COMPILED_ALBUM, CLIENT_ALBUM, GRAPHIC_DATASETS, load_catalog, lookup, graphic_trace
)
class PET126RLookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=load_catalog()
        cls.rows=cls.c["datasets"][CN50_COMPILED_ALBUM]
    def test_full_named_source_only_catalog(self):
        self.assertEqual(len(self.rows),305)
        self.assertEqual(self.c["metrics"]["source_namespace_row_counts_NOT_species"][CN50_COMPILED_ALBUM],305)
        self.assertEqual(len({row["source_ordinal"] for row in self.rows}),305)
        self.assertTrue(all(row["name_as_written"] and row["graphic_number"] is None for row in self.rows))
        self.assertTrue(all(not row["official_live_release_confirmed"] for row in self.rows))
    def test_ordinary_lookup_preserves_original_region_and_no_graphic_id(self):
        matches=lookup(self.c,"乌力",CN50_COMPILED_ALBUM,limit=30)
        self.assertTrue(matches)
        self.assertEqual(matches[0]["source"],"CN50_THIRD_PARTY_PRESERVED_PC_5_0_CAB")
        self.assertIsNone(matches[0]["graphic_number"])
        complete=lookup(self.c,"乌力",CN50_COMPILED_ALBUM,limit=20,details=True)
        self.assertIsNone(complete[0]["graphic_number"])
        self.assertEqual(complete[0]["TW10_ordinal_based_candidate_SPR_only"],100250)
        self.assertTrue(all(not x["native_same_build_graphic_selector_proven"] for x in complete))
    def test_tw10_true_graphics_not_overwritten_or_merged(self):
        self.assertNotIn(CN50_COMPILED_ALBUM,GRAPHIC_DATASETS)
        self.assertEqual(len(self.c["datasets"][CLIENT_ALBUM]),124)
        trace=graphic_trace(self.c,100250)
        self.assertEqual(trace["tw10_same_client_album_record"]["name_as_written"],"烏力")
        self.assertIn("tw10_visual",trace["source_separated_matches"])
    def test_name_rows_not_species_or_official_proof(self):
        self.assertTrue(all(row["source_evidence"]=="CLIENT_COMPILED_NAME_ONLY_GRAPHIC_SELECTOR_UNPROVEN" for row in self.rows))
        self.assertTrue(any(row["same_carrier_candidate_SPR_present"] for row in self.rows))
if __name__=="__main__":unittest.main()
