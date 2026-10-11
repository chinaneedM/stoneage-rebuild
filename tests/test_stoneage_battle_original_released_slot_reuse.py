"""Negative and complete-matrix checks for bounded original released-slot reuse."""
import unittest
from tools.stoneage_battle_original_released_slot_reuse_audit import validate_reuse_rows


def row(profile, alias):
    blocked = alias == 0
    fields = {
        "alias": alias, "victim": 8, "old_id": 1,
        "created": -1 if blocked else 8, "new_id": 1 if blocked else 2,
        "old_owner": 6 if blocked else -1, "new_owner": 6 if blocked else -1,
        "released": 0 if blocked else 1, "guard_warnings": int(blocked),
        "factory_diagnostics": int(blocked),
        "release_calls": int(not blocked), "assignment_draws": 6,
        "factory_draws": 66, "blockers": 244, "count_delta": int(not blocked),
        "pet_ref": 8 if alias == 2 else -1, "player_ref": 8 if blocked else -1,
    }
    fields.update({k: 1 for k in (
        "others_unchanged", "whole_actors", "whole_arena", "whole_connections",
        "tables_immutable", "no_cursor_rewind", "original_creation",
        "original_assignment", "original_factory", "synthetic_alias",
        "synthetic_blockers")})
    return "|".join(["ACTUAL", profile, "REAL_HEADER_RELEASED_SLOT_REUSE"] +
                    [f"{k}={v}" for k, v in fields.items()])


def fixture():
    return [row(p, a) for p in ("gavin", "bismarck") for a in (-1, 2, 0)]


class ReleasedSlotReuseEvidence(unittest.TestCase):
    def test_exact_complete_matrix(self):
        self.assertEqual(len(validate_reuse_rows(fixture())), 6)

    def test_every_row_required(self):
        lines = fixture()
        for i in range(len(lines)):
            with self.subTest(i=i), self.assertRaises(ValueError):
                validate_reuse_rows(lines[:i] + lines[i+1:])

    def test_alias_protection_vs_pet_dangling(self):
        lines = fixture()
        for old, new in (("created=8", "created=-1"),
                         ("new_id=2", "new_id=1"),
                         ("pet_ref=8", "pet_ref=-1"),
                         ("player_ref=8", "player_ref=-1"),
                         ("guard_warnings=1", "guard_warnings=0"),
                         ("factory_diagnostics=1", "factory_diagnostics=0"),
                         ("released=1", "released=0")):
            target = next(x for x in lines if old in x)
            with self.subTest(old=old), self.assertRaises(ValueError):
                validate_reuse_rows([x.replace(old, new) if x == target else x for x in lines])

    def test_mutation_oracle_required(self):
        lines = fixture()
        for key in ("others_unchanged", "whole_actors", "whole_arena",
                    "whole_connections", "tables_immutable", "no_cursor_rewind",
                    "original_creation", "original_assignment", "original_factory"):
            with self.subTest(field=key), self.assertRaises(ValueError):
                validate_reuse_rows([x.replace(key + "=1", key + "=0", 1) if i == 0
                                    else x for i, x in enumerate(lines)])

    def test_duplicate_and_unknown_field(self):
        lines = fixture()
        with self.assertRaises(ValueError):
            validate_reuse_rows(lines + [lines[0]])
        with self.assertRaises(ValueError):
            validate_reuse_rows([lines[0] + "|extra=1"] + lines[1:])
        with self.assertRaises(ValueError):
            validate_reuse_rows([lines[0] + "|victim=8"] + lines[1:])

    def test_negative_invalid_identity_and_count(self):
        lines = fixture()
        for old, new in (("ACTUAL|gavin|", "ACTUAL|unknown|"),
                         ("alias=-1", "alias=1"), ("blockers=244", "blockers=0"),
                         ("factory_draws=66", "factory_draws=0"),
                         ("count_delta=1", "count_delta=2"),
                         ("old_owner=-1", "old_owner=6")):
            target = next(x for x in lines if old in x)
            with self.subTest(old=old), self.assertRaises(ValueError):
                validate_reuse_rows([x.replace(old, new) if x == target else x for x in lines])

    def test_non_actual_rows_cannot_substitute_evidence(self):
        with self.assertRaises(ValueError):
            validate_reuse_rows(["PREDICTED" + x[6:] for x in fixture()])


if __name__ == "__main__":
    unittest.main()
