from types import SimpleNamespace
import unittest

from tools.stoneage_recovered25_lighttakeed_probe import analyze_runtime_objects


def skill(skill_id, option):
    return SimpleNamespace(
        skill_id=skill_id,
        function_name="PETSKILL_Lighttakeed",
        field=1,
        target=1,
        cost=2,
        illegal=0,
        option_bytes=option,
    )


def enemy(graphic_id, slots):
    return SimpleNamespace(
        graphic_id=graphic_id,
        skill_slot_ids=tuple(slots),
    )


class LighttakeedProbeTests(unittest.TestCase):
    def test_population_markers_and_templates(self):
        pets = SimpleNamespace(skills={
            610: skill(610, b"VANISH"),
            611: skill(611, b"ABSROB"),
        })
        enemies = SimpleNamespace(templates={
            10: enemy(100010, (610, 0, 611, 0, 0, 0, 0)),
            20: enemy(100020, (0, 610, 0, 0, 0, 0, 0)),
        })
        result = analyze_runtime_objects(pets, enemies)
        self.assertTrue(result["population_closed"])
        self.assertEqual(result["slot_references"], 3)
        self.assertEqual(len(result["templates"]), 2)
        rows = {row["id"]: row for row in result["rows"]}
        self.assertTrue(rows[610]["marker_vanish"])
        self.assertFalse(rows[610]["marker_absrob"])
        self.assertTrue(rows[611]["marker_absrob"])
        self.assertFalse(rows[611]["marker_reflec"])
        self.assertEqual(
            tuple(row["skill_ids"] for row in result["templates"]),
            ((610, 611), (610,)),
        )

    def test_population_rejects_extra_reference_count(self):
        pets = SimpleNamespace(skills={
            610: skill(610, b"VANISH"),
            611: skill(611, b"REFLEC"),
        })
        enemies = SimpleNamespace(templates={
            10: enemy(100010, (610, 611, 610, 611, 0, 0, 0)),
            20: enemy(100020, (0, 0, 0, 0, 0, 0, 0)),
        })
        result = analyze_runtime_objects(pets, enemies)
        self.assertFalse(result["population_closed"])
        self.assertEqual(result["slot_references"], 4)


if __name__ == "__main__":
    unittest.main()
