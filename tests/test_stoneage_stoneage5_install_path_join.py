import unittest
from tools.stoneage_stoneage5_install_path_join import (
    safe_rel, directory_relative, same_path_comparison, msi_table, build)


class JoinTests(unittest.TestCase):
    def test_paths_reject_escaping(self):
        self.assertEqual(safe_rel("data\\battleMap\\battle00.sab"), "data/battleMap/battle00.sab")
        for s in ("../x","/x","C:/x","a//b","x/./y","x\x00y"):
            with self.subTest(value=s), self.assertRaises(ValueError):
                safe_rel(s)

    def test_directory_cycle_and_escape(self):
        self.assertEqual(directory_relative("B", {"B":("A","battleMap"),
                        "A":("INSTALLDIR","data")}),"data/battleMap")
        for folder, dirs in (("Z",{}),("A",{"A":("A","loop")}),
                             ("A",{"A":("TARGETDIR","data"),"TARGETDIR":("","SourceDir")})):
            with self.subTest(folder=folder),self.assertRaises(ValueError):
                directory_relative(folder,dirs)

    def test_comparison_distinguishes_missing_and_change(self):
        rows=[{"installed_path":"data/a","size":2,"sha256":"x"},
              {"installed_path":"data/b","size":3,"sha256":"y"},
              {"installed_path":"data/c","size":4,"sha256":"z"}]
        known={"data/a":{"size":2,"sha256":"x"},
               "data/b":{"size":3,"sha256":"different"}}
        x=same_path_comparison(rows,known)
        self.assertEqual((x["shared_path_count"],x["same_path_exact_count"],
                          x["same_path_changed_count"],x["not_present_at_same_path_count"]), (2,1,1,1))

    def test_source_table_and_live_project_pins(self):
        # The complete report is a replay of fixed, versioned source manifests.
        out=build()
        self.assertEqual(len(out["installed_files"]),413)
        self.assertEqual(out["comparisons"]["TW10"]["same_path_exact_count"],361)
        self.assertEqual(out["comparisons"]["TW85"]["same_path_exact_count"],407)
        self.assertEqual(out["comparisons"]["TW10"]["changed_path_evidence"][0]["path"],"StoneAge.exe")
        self.assertFalse(out["scope"]["original_server_content_restored"])

    def test_truncated_table_is_rejected(self):
        with self.assertRaises(ValueError):
            msi_table("MSI_EXPORT_BEGIN|table=File\n", "File")


if __name__ == "__main__":
    unittest.main()
