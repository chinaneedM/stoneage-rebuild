"""Mutation-backed negative tests for the Taiwan 8.0 documentary scope gate."""
import unittest
from pathlib import Path
from tools.stoneage_pet_80_release_evidence_gate import (
    ROOT, SPEC, OTHER, validate, ORIGINAL_ANNOUNCEMENT,
)

class Pet80ContemporaryGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = [(ROOT / p).read_text(encoding="utf-8") for p in (SPEC, *OTHER)]

    def test_accepted_evidence_scope(self):
        validate(*self.content)

    def test_unverified_original_binary_cannot_be_promoted(self):
        data = self.content.copy()
        data[0] = data[0].replace(
            "| Is there an original compatible enabled client/server binary pair with version identifiers and checked configuration? | OPEN |",
            "| Is there an original compatible enabled client/server binary pair with version identifiers and checked configuration? | VERIFIED |",
        )
        self.assertNotEqual(data[0], self.content[0])
        with self.assertRaisesRegex(ValueError, "Evidence matrix drift"):
            validate(*data)

    def test_pinned_bismarck_is_not_operator_binary(self):
        data = self.content.copy()
        data[0] = data[0].replace(
            "| Is the checked-in pinned later Bismarck default PET feature enabled? | NO in the previously accepted default source/profile gate |",
            "| Is the checked-in pinned later Bismarck default PET feature enabled? | YES in deployed release |",
        )
        self.assertNotEqual(data[0], self.content[0])
        with self.assertRaisesRegex(ValueError, "Evidence matrix drift"):
            validate(*data)

    def test_no_first_version_promotion(self):
        data = self.content.copy()
        data[0] = data[0].replace(
            "| Does any result establish 1999 JSS or Taiwan 1.0 PET equipment? | NO |",
            "| Does any result establish 1999 JSS or Taiwan 1.0 PET equipment? | YES |",
        )
        self.assertNotEqual(data[0], self.content[0])
        with self.assertRaisesRegex(ValueError, "Evidence matrix drift"):
            validate(*data)

    def test_primary_press_source_must_remain_registered(self):
        data = self.content.copy()
        data[2] = data[2].replace(ORIGINAL_ANNOUNCEMENT, "URL_REMOVED")
        self.assertNotEqual(data[2], self.content[2])
        with self.assertRaisesRegex(ValueError, "press citation missing"):
            validate(*data)

    def test_continuity_receipt_required(self):
        data = self.content.copy()
        data[3] = data[3].replace(
            "PET 8.0 contemporary launch evidence and clean-binary retrieval leads",
            "UNTRACKED_AND_REPLACED",
        )
        with self.assertRaisesRegex(ValueError, "Continuity receipt missing"):
            validate(*data)

if __name__ == "__main__":
    unittest.main()
