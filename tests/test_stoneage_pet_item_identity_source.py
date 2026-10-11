"""Reject missing/overstated source-only PET-item and identity receipts."""
import unittest
from tools.stoneage_pet_item_identity_source_audit import (
    PROFILES, FUNCTIONS, REQUIRED, validate_report,
)


def fixture():
    rows = []
    for name, spec in PROFILES.items():
        data = {
            "profile": name,
            "base_blob": spec["files"]["base"],
            "char_blob": spec["files"]["char"],
            "item_blob": spec["files"]["item"],
            "pet_gate": spec["pet_gate"],
            "pet_slot_limit": spec["item_slots"],
            **{k: 1 for k in REQUIRED},
            "natural_reachability_proven": 0,
            "production_macro_configuration_verified": 0,
            "first_release_membership_proven": 0,
        }
        rows.append("SOURCE_ONLY_PET_ITEM_IDENTITY|" +
                    "|".join(f"{k}={v}" for k, v in data.items()))
        for group in FUNCTIONS.values():
            for item in group:
                rows.append(f"SOURCE_ONLY_PET_ITEM_FUNCTION|profile={name}|name={item}|sha256={'a'*64}")
    rows.append("RESOLUTION|PET_ITEM_IDENTITY_SOURCE_ONLY_ORIENTATION_PASS")
    return rows


class PetItemIdentitySourceEvidence(unittest.TestCase):
    def setUp(self):
        self.lines = fixture()

    def expect_reject(self, new):
        with self.assertRaises(ValueError):
            validate_report("\n".join(new))

    def test_complete_matrix(self):
        profiles, functions = validate_report("\n".join(self.lines))
        self.assertEqual(len(profiles), 2)
        self.assertEqual(len(functions), 22)

    def test_each_profile_and_function_required(self):
        for i, item in enumerate(self.lines[:-1]):
            with self.subTest(i=i, text=item[:44]):
                self.expect_reject(self.lines[:i] + self.lines[i+1:])

    def test_no_natural_reachability_or_early_identity_promotion(self):
        for field in ("natural_reachability_proven",
                      "production_macro_configuration_verified",
                      "first_release_membership_proven"):
            changed = [x.replace(field + "=0", field + "=1")
                       if x.startswith("SOURCE_ONLY_PET_ITEM_IDENTITY|") else x
                       for x in self.lines]
            self.expect_reject(changed)

    def test_profile_gate_must_not_be_flattened(self):
        for old, new in (("pet_gate=NOT_SIMPLIFY_ITEMSTRING", "pet_gate=PET_ITEM"),
                         ("pet_gate=PET_ITEM", "pet_gate=NOT_SIMPLIFY_ITEMSTRING"),
                         ("pet_slot_limit=CHAR_MAXITEMHAVE",
                          "pet_slot_limit=CHAR_MAXPETITEMHAVE")):
            self.expect_reject([x.replace(old,new) for x in self.lines])

    def test_each_positive_source_path_flag_required(self):
        for field in REQUIRED:
            with self.subTest(flag=field):
                modified = list(self.lines)
                modified[0] = modified[0].replace(field + "=1", field + "=0")
                self.expect_reject(modified)

    def test_raw_blob_provenance_and_fingerprint_format(self):
        changed = list(self.lines)
        changed[0] = changed[0].replace("base_blob=" + PROFILES["gavin"]["files"]["base"],
                                        "base_blob=" + "0"*40)
        self.expect_reject(changed)
        changed = list(self.lines)
        pos = next(i for i, x in enumerate(changed) if x.startswith("SOURCE_ONLY_PET_ITEM_FUNCTION|"))
        changed[pos] = changed[pos].replace("sha256=" + "a"*64, "sha256=nonhex")
        self.expect_reject(changed)

    def test_duplicate_and_extra_data_rejected(self):
        self.expect_reject(self.lines + [self.lines[0]])
        changed = list(self.lines); changed[0] += "|extra=1"; self.expect_reject(changed)
        changed = list(self.lines); changed[0] += "|profile=gavin"; self.expect_reject(changed)
        changed = list(self.lines); changed[0] = changed[0].replace("profile=gavin", "profile=unknown")
        self.expect_reject(changed)

    def test_resolution_required(self):
        self.expect_reject(self.lines[:-1])

    def test_fake_synthetic_witness_is_not_actual_source_result(self):
        self.expect_reject([x.replace("SOURCE_ONLY_PET_ITEM_", "FAKE_PET_ITEM_")
                            for x in self.lines])


if __name__ == "__main__":
    unittest.main()
