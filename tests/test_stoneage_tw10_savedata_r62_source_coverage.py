"""Distinguish concrete decoded operands from mere integer site mentions."""
import copy
import json
import unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_r62_source_coverage import (
  collect, analyze_sources, load_directory, SITES, CONTROL,
)
BASE=Path(__file__).resolve().parents[1]/"research/recovered"

class Coverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=load_directory(BASE)
    def test_report_set_and_source_fingerprints(self):
        out=analyze_sources(self.files)
        self.assertEqual(out["report_count"],32)
        self.assertEqual(len(out["reports"]),32)
        for n,sha in CONTROL.items():
            row=next(x for x in out["reports"] if x["report"]=="R"+str(n))
            self.assertEqual(row["git_blob"],sha)
        self.assertFalse(out["actual_native_return_count_or_callee_abi_proven"])
        self.assertFalse(out["actual_savedata_write_flush_close_or_persistence_proven"])
    def test_site_mention_is_not_operand(self):
        m,f=collect({"x":[{"site_rva":SITES[0],"syntax_class":"unknown_call"},
                          {"site_rva":SITES[1],"mnemonic":"jne"},
                          {"site_rva":SITES[0],"operands":[]}]})
        self.assertEqual(len(m[str(SITES[0])]),2)
        self.assertEqual(f[str(SITES[0])],[])
        self.assertEqual(f[str(SITES[1])],[])
    def test_true_synthetic_operand_is_identified_without_claiming_execution(self):
        m,f=collect({"instructions":[{"site_rva":SITES[0],"mnemonic":"test",
                                       "operands":[{"register":"eax"}]}]})
        self.assertEqual(len(f[str(SITES[0])]),1)
        self.assertEqual(f[str(SITES[0])][0]["mnemonic"],"test")
    def test_unrelated_addresses_ignored(self):
        m,f=collect([{"site_rva":0x4C68C,"mnemonic":"call","operands":[]}])
        self.assertTrue(all(not a for a in m.values()))
        self.assertTrue(all(not a for a in f.values()))
    def test_invalid_report_set_fails_closed(self):
        rows=dict(self.files)
        rows.pop(next(k for k in rows if "R33-ORIGINAL" in k))
        with self.assertRaises(ValueError):analyze_sources(rows)
    def test_mutated_pinned_report_fails_closed(self):
        rows=dict(self.files)
        f=next(k for k in rows if "R44-ORIGINAL" in k)
        buf=bytearray(rows[f]);buf[21]^=1;rows[f]=bytes(buf)
        with self.assertRaises(ValueError):analyze_sources(rows)
    def test_unregistered_fake_report_fails_closed(self):
        rows=dict(self.files);rows["STONEAGE-TW10-SAVEDATA-NATIVE-IO-R100-ORIGINAL.json"]=b"{}"
        with self.assertRaises(ValueError):analyze_sources(rows)

if __name__=="__main__":
    unittest.main()
