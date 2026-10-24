import unittest
from pathlib import Path
from tools.stoneage_cn50_original_resource_catalog import qualify_sources,DATASETS,NAMES


class CatalogPreflight(unittest.TestCase):
    def test_existing_original_cab_and_comparison_pins(self):
        root=Path(__file__).resolve().parents[1]
        report,comparison,lookup=qualify_sources(root)
        self.assertEqual(len(lookup),413)
        self.assertEqual(report["files"]["count"],413)
        self.assertEqual(comparison["families"]["bitmap_rd"]["new"]["index_count"],303197)
        self.assertEqual(comparison["families"]["animation_spr"]["new"]["index_count"],1185)
        self.assertEqual(lookup["real_31.bin"][0],1102755808)

    def test_only_metadata_outputs(self):
        self.assertEqual(len(DATASETS),5)
        self.assertTrue(all(x.endswith(".tsv.gz") for x in DATASETS))
        self.assertEqual(len(NAMES),4)
        self.assertFalse(any(x.endswith(".exe") for x in DATASETS))
