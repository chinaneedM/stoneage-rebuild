"""Strict negative controls: macro-enabled source does not imply real paired builds."""
import unittest
from tools.stoneage_pet_paired_build_matrix_audit import COMMIT,NAMES,RESOLUTION,validate_report

def valid():
    data={"pinned_commit":COMMIT,"source_blobs":"10",
          "sln_configs":"VER25_DEBUG,VER25_RELEASE",
          "script_default":"VER25_RELEASE","vs_solution_active_pet":"0",
          "server_make_default_pet":"0","server_windows_cmake_default_pet":"0",
          "paired_checked_in_default_pet":"0","client_forced_80_pet":"1",
          "server_forced_pet":"1","actual_enabled_pair_binaries":"0",
          "actual_network_packet":"0","original_early_feature_verified":"0"}
    return "\n".join([
      "SOURCE_PET_PAIR_GATE|"+"|".join(f"{k}={v}" for k,v in data.items()),
      *[f"SOURCE_PET_PAIR_PROFILE|name={name}|pet={int(name in ('client_version80_forced','server_pet_forced'))}" for name in NAMES],
      "BOUNDARY|Checked-in late-descendant solution VER25 profiles and GNU/MinGW server defaults have no PET gate; forcing both macro gates is a counterfactual preprocessor check, not a successful paired compile, link, deployed binary or historical 1999 feature",
      "CORRECTION|Prior prose identifying Debug and Release as the two solution-selected configurations was imprecise; actual solution selects VER25_DEBUG and VER25_RELEASE, while vcxproj also has standalone Debug/Release groups not selected by the solution",
      "OPEN|Any independently verified compiled PET-enabled pair; native client-server handshake, actual opcode127 packet, persistent item owner/unique-code lifecycle, early Japan/Taiwan version attribution",
      RESOLUTION])+"\n"

class PetPairedBuildMatrixTest(unittest.TestCase):
    def test_bounded_source_receipt(self):
        self.assertEqual(validate_report(valid())["paired_checked_in_default_pet"],"0")
    def test_real_binaries_network_and_early_are_not_proven(self):
        for k in ("actual_enabled_pair_binaries","actual_network_packet",
                  "original_early_feature_verified","paired_checked_in_default_pet"):
            with self.subTest(k=k),self.assertRaises(ValueError):
                validate_report(valid().replace(k+"=0",k+"=1"))
    def test_accurate_client_vs_project_and_solution_selection(self):
        for a,b in (("sln_configs=VER25_DEBUG,VER25_RELEASE","sln_configs=Debug,Release"),
                    ("script_default=VER25_RELEASE","script_default=Release"),
                    ("source_blobs=10","source_blobs=9"),
                    ("CORRECTION|Prior prose","CHANGE|Prior prose")):
            with self.subTest(a=a),self.assertRaises(ValueError):
                validate_report(valid().replace(a,b))
    def test_default_not_forced_macro_error_rejected(self):
        for k in ("vs_solution_active_pet","server_make_default_pet",
                  "server_windows_cmake_default_pet"):
            with self.subTest(k=k),self.assertRaises(ValueError):
                validate_report(valid().replace(k+"=0",k+"=1"))
        for k in ("client_forced_80_pet","server_forced_pet"):
            with self.subTest(k=k),self.assertRaises(ValueError):
                validate_report(valid().replace(k+"=1",k+"=0"))
    def test_every_named_macro_profile_required(self):
        for n in NAMES:
            with self.subTest(n=n),self.assertRaises(ValueError):
                validate_report(valid().replace("name="+n,"name=unknown"))
    def test_duplicates_and_missing_lines_rejected(self):
        data=valid()
        with self.assertRaises(ValueError):
            validate_report(data.replace("source_blobs=10","source_blobs=10|source_blobs=10"))
        ls=data.splitlines()
        for i in range(len(ls)):
            with self.subTest(i=i),self.assertRaises(ValueError):
                validate_report("\n".join(ls[:i]+ls[i+1:])+"\n")
    def test_boundary_counterfactual_and_open_required(self):
        for a,b in (("counterfactual","production"),
                    ("not a successful paired compile","paired build PASS"),
                    ("OPEN|Any independently","FACT|Any independently")):
            with self.subTest(a=a),self.assertRaises(ValueError):
                validate_report(valid().replace(a,b))
if __name__=="__main__":unittest.main()
