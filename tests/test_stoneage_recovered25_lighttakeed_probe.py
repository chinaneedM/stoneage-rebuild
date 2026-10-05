from types import SimpleNamespace
import hashlib
import unittest

from tools.stoneage_recovered25_lighttakeed_probe import analyze_runtime_objects


def skill(skill_id, option, *, field=1, target=7, cost=2, illegal=5000):
    return SimpleNamespace(
        skill_id=skill_id,
        function_name="PETSKILL_Lighttakeed",
        field=field,
        target=target,
        cost=cost,
        illegal=illegal,
        option_bytes=option,
    )


def enemy(graphic_id, slots):
    return SimpleNamespace(
        graphic_id=graphic_id,
        skill_slot_ids=tuple(slots),
    )


def exact_row(skill_id, option, refs):
    return (
        skill_id, 1, 7, 2, 5000, refs, len(option),
        hashlib.sha256(option).hexdigest(), False,
        b"VANISH" in option, b"ABSROB" in option, b"REFLEC" in option,
    )


class LighttakeedProbeTests(unittest.TestCase):
    def test_population_markers_and_templates(self):
        opt609 = b"ABSROB"
        opt610 = b"REFLEC"
        opt611 = b"VANISH"
        pets = SimpleNamespace(skills={
            609: skill(609, opt609),
            610: skill(610, opt610),
            611: skill(611, opt611),
        })
        enemies = SimpleNamespace(templates={
            10: enemy(100010, (610, 0, 611, 0, 0, 0, 0)),
            20: enemy(100020, (0, 610, 0, 0, 0, 0, 0)),
        })
        expected_rows = (
            exact_row(609, opt609, 0),
            exact_row(610, opt610, 2),
            exact_row(611, opt611, 1),
        )
        expected_templates = (
            (10, 100010, (1, 3), (610, 611)),
            (20, 100020, (2,), (610,)),
        )
        result = analyze_runtime_objects(
            pets,
            enemies,
            expected_exact_rows=expected_rows,
            expected_template_rows=expected_templates,
        )
        self.assertTrue(result["population_closed"])
        self.assertTrue(result["exact_rows_closed"])
        self.assertTrue(result["exact_templates_closed"])
        self.assertEqual(result["slot_references"], 3)
        rows = {row["id"]: row for row in result["rows"]}
        self.assertTrue(rows[609]["marker_absrob"])
        self.assertTrue(rows[610]["marker_reflec"])
        self.assertTrue(rows[611]["marker_vanish"])

    def test_population_rejects_extra_reference_count(self):
        pets = SimpleNamespace(skills={
            609: skill(609, b"ABSROB"),
            610: skill(610, b"REFLEC"),
            611: skill(611, b"VANISH"),
        })
        enemies = SimpleNamespace(templates={
            10: enemy(100010, (610, 611, 610, 611, 0, 0, 0)),
            20: enemy(100020, (0, 0, 0, 0, 0, 0, 0)),
        })
        result = analyze_runtime_objects(
            pets,
            enemies,
            expected_exact_rows=(),
            expected_template_rows=(),
        )
        self.assertFalse(result["population_closed"])
        self.assertEqual(result["slot_references"], 4)


if __name__ == "__main__":
    unittest.main()
