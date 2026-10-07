import copy
import hashlib
from pathlib import Path
from types import SimpleNamespace as S
import unittest

from tools.stoneage_recovered25_becomepig_probe import analyze_runtime_objects, emit


def fixture():
    pets = S(skills={
        i: S(skill_id=i, field=1, target=1, cost=2, illegal=0,
             function_name="PETSKILL_BecomePig", option_bytes=b"40 60 100250")
        for i in (631, 635)
    })
    enemies = S(templates={
        100: S(graphic_id=1001, base_vital=10, base_strength=20, base_toughness=30,
               base_dexterity=40, ai=50, skill_slot_ids=(631, 0, 0, 0, 0, 0, 0)),
        101: S(graphic_id=1002, base_vital=11, base_strength=21, base_toughness=31,
               base_dexterity=41, ai=51, skill_slot_ids=(0, 635, 0, 0, 0, 0, 0)),
    })
    return pets, enemies


def pins():
    option = b"40 60 100250"
    rows = tuple((i, 1, 1, 2, 0, 1, len(option), hashlib.sha256(option).hexdigest(), False, True, True) for i in (631, 635))
    templates = (
        (100, 1001, 10, 20, 30, 40, 50, (1,), (631,)),
        (101, 1002, 11, 21, 31, 41, 51, (2,), (635,)),
    )
    return dict(expected_callback_ids=(631, 635), expected_exact_rows=rows, expected_template_rows=templates)


class BecomePigDiscoveryTests(unittest.TestCase):
    def test_discovery_cannot_accept_unpinned_population_or_placements(self):
        r = analyze_runtime_objects(*fixture())
        self.assertTrue(r["positive_references_closed"])
        for key in ("population", "exact_rows", "exact_templates"):
            self.assertFalse(r[key+"_closed"])

    def test_unreferenced_family_row_is_reported_and_breaks_population_pin(self):
        pets, enemies = fixture()
        pets.skills[700] = copy.copy(pets.skills[631])
        pets.skills[700].skill_id = 700
        r = analyze_runtime_objects(pets, enemies, **pins())
        self.assertEqual(r["callback_ids"], (631, 635, 700))
        self.assertEqual(r["rows"][-1]["slot_references"], 0)
        self.assertTrue(r["positive_references_closed"])
        self.assertFalse(r["population_closed"])

    def test_neighbor_callback_cannot_close_known_family(self):
        pets, enemies = fixture()
        pets.skills[631].function_name = "PETSKILL_BecomeFox"
        self.assertFalse(analyze_runtime_objects(pets, enemies)["positive_references_closed"])

    def test_duplicate_use_does_not_hide_missing_referenced_id(self):
        pets, enemies = fixture()
        enemies.templates[101].skill_slot_ids = (0, 631, 0, 0, 0, 0, 0)
        r = analyze_runtime_objects(pets, enemies)
        self.assertEqual(r["slot_references"], 2)
        self.assertFalse(r["positive_references_closed"])

    def test_same_use_count_on_one_template_is_rejected(self):
        pets, enemies = fixture()
        enemies.templates[100].skill_slot_ids = (631, 635, 0, 0, 0, 0, 0)
        enemies.templates[101].skill_slot_ids = (0,) * 7
        self.assertFalse(analyze_runtime_objects(pets, enemies)["positive_references_closed"])

    def test_option_digest_and_metadata_are_independent_from_slot_census(self):
        for field, value in (("option_bytes", b"41 60 100250"), ("target", 3), ("illegal", 3000)):
            with self.subTest(field=field):
                pets, enemies = fixture()
                setattr(pets.skills[631], field, value)
                r = analyze_runtime_objects(pets, enemies, **pins())
                self.assertTrue(r["positive_references_closed"])
                self.assertTrue(r["population_closed"])
                self.assertFalse(r["exact_rows_closed"])
                self.assertTrue(r["exact_templates_closed"])

    def test_slot_and_base_stat_changes_break_placement_pins(self):
        for field, value in (("skill_slot_ids", (0, 631, 0, 0, 0, 0, 0)), ("base_strength", 21), ("ai", 51)):
            with self.subTest(field=field):
                pets, enemies = fixture()
                setattr(enemies.templates[100], field, value)
                r = analyze_runtime_objects(pets, enemies, **pins())
                self.assertTrue(r["positive_references_closed"])
                self.assertFalse(r["exact_templates_closed"])

    def test_report_does_not_disclose_raw_option_or_display_text(self):
        import contextlib
        import io
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            emit(analyze_runtime_objects(*fixture()))
        self.assertNotIn("40 60 100250", stream.getvalue())
        self.assertIn("option_sha256=", stream.getvalue())
        self.assertIn("EXACT_ROWS_OPEN", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
