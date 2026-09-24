import unittest

from tools.stoneage_discmaster_target_probe import TARGETS, query_url, walk_candidate_dicts


class DiscMasterTargetProbeTests(unittest.TestCase):
    def test_exact_filename_and_package_identifiers_are_pinned(self):
        targets={label:(field,query,extra) for label,field,query,extra in TARGETS}
        self.assertEqual(targets["sa174hg-exact-name"][0],"name")
        self.assertEqual(targets["sa174hg-exact-name"][1],'"sa174hg.exe"')
        self.assertEqual(targets["package-model-content"][1],'"WR-04156"')
        self.assertEqual(targets["package-jan-content"][1],'"4988609011565"')

    def test_query_uses_recovered_schema(self):
        url=query_url("name",'"sa174hg.exe"',{"tsMin":"2003","tsMax":"2004"})
        self.assertIn("qfields=name",url)
        self.assertIn("mode=deep",url)
        self.assertIn("outputAs=json",url)
        self.assertIn("tsMin=2003",url)
        self.assertIn("tsMax=2004",url)

    def test_candidate_walker_finds_nested_file_rows(self):
        sample={"hits":{"hits":[{"_source":{"itemid":12,"name":"sa174hg.exe","size":123}}]}}
        rows=walk_candidate_dicts(sample)
        self.assertTrue(any(row.get("name")=="sa174hg.exe" for row in rows))


if __name__=="__main__":
    unittest.main()
