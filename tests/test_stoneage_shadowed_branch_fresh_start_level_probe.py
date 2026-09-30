import unittest

from tools.stoneage_shadowed_branch_fresh_start_level_probe import (
    FreshStartLevelAudit,
)


class FreshStartLevelProbeTests(unittest.TestCase):

    def test_direct_witness_requires_birth_level_joint_record(self):
        audit=FreshStartLevelAudit(
            birth_level=10,
            matching_award_records=2,
            joint_domain_records=2,
            birth_level_joint_records=1,
            gate_legal_levels=20,
        )
        self.assertTrue(audit.direct_witness)

    def test_zero_birth_level_does_not_close_direct_chain(self):
        audit=FreshStartLevelAudit(
            birth_level=0,
            matching_award_records=2,
            joint_domain_records=2,
            birth_level_joint_records=1,
            gate_legal_levels=20,
        )
        self.assertFalse(audit.direct_witness)

    def test_joint_domain_without_birth_membership_remains_open(self):
        audit=FreshStartLevelAudit(
            birth_level=1,
            matching_award_records=2,
            joint_domain_records=2,
            birth_level_joint_records=0,
            gate_legal_levels=20,
        )
        self.assertFalse(audit.direct_witness)


if __name__=="__main__":
    unittest.main()
