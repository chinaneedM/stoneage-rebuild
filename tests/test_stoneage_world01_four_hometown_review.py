"""WORLD-01 finite 24-checkpoint provenance and route-claim safeguards.

All inputs are committed derived metadata; no proprietary source bundle required.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "research/recovered/STONEAGE-WORLD01-FOUR-HOMETOWN-ACCEPTANCE-R1.json"


class World01FiniteAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.source_text = {
            key: (ROOT / value).read_text(encoding="utf-8")
            for key, value in cls.audit["source_index"].items()
        }

    def test_exact_24_cells_and_unpromoted_history(self):
        x = self.audit
        self.assertEqual("BOUNDED_REVIEW_CLOSED_SOURCE_CONDITIONAL", x["package_status"])
        self.assertEqual("PARTIAL_OPEN", x["stage_a_world_family"])
        self.assertIsNone(x["aggregate_completion_percentage"])
        self.assertEqual(4, len(x["routes"]))
        self.assertEqual(24, len(x["cells"]))
        cells = {(v["route_ordinal"], v["checkpoint"]) for v in x["cells"]}
        self.assertEqual(24, len(cells))
        self.assertEqual({(r, c) for r in range(1, 5) for c in
            ("spawn", "region", "movement", "encounter", "npc", "settlement")}, cells)
        for cell in x["cells"]:
            self.assertEqual("LATER_RECOVERED", cell["version_role"])
            self.assertEqual("OPEN_TW10_JSS1999", cell["early_membership"])
            self.assertTrue(cell["evidence_paths"])
            self.assertTrue(cell["required_external_inputs"])
            self.assertTrue(cell["unresolved_gap"])
            self.assertTrue(cell["gameplay_impact"])

    def test_route_order_matches_preexisting_original_derived_report(self):
        routes = self.source_text["route"]
        expected = {
            1: ("COMBAT", 16, 0, 0, 107),
            2: ("COMBAT", 16, 0, 0, 107),
            3: ("COMBAT>SHOP>WARPMAN", 28, 1, 1, 446),
            4: ("SHOP>COMBAT>WARPMAN", 28, 1, 1, 442),
        }
        for row in self.audit["routes"]:
            ordinal = row["ordinal"]
            order, combat, shop, warpman, visited = expected[ordinal]
            self.assertEqual(order, row["milestones"])
            self.assertEqual(combat, row["combat_witnesses"])
            self.assertEqual(bool(shop), row["requires_shop"])
            self.assertEqual(bool(warpman), row["requires_warpman"])
            self.assertIn(
                f"ALL_HOMETOWN_ORDERED_ROUTE|ordinal={ordinal}|combat_witnesses={combat}|"
                f"requires_shop={shop}|requires_warpman={warpman}|ordered=1|milestones={order}|"
                f"visited_states={visited}|unresolved_map_floors=0", routes
            )

    def test_conditional_bridges_are_not_classic_warps(self):
        coords = self.source_text["coordinate"]
        bridge = self.source_text["bridge"]
        gate = self.source_text["gate"]
        shop = self.source_text["shop"]
        for o in (1, 2):
            self.assertIn(f"FRESH_START_COORDINATE_WITNESS|ordinal={o}|reachable=1|", coords)
        for o in (3, 4):
            self.assertIn(f"FRESH_START_COORDINATE_WITNESS|ordinal={o}|reachable=0|", coords)
            self.assertIn(f"FRESH_START_DIALOGUE_BRIDGE|ordinal={o}|classic_reachable=0|", bridge)
            self.assertIn(f"FRESH_START_WARPMAN_BRIDGE_GATE|ordinal={o}|", gate)
            self.assertIn(
                f"FRESH_START_BRIDGE_SHOP|ordinal={o}|ordered_shops=1|"
                f"affordable_ordered_shops=1|combined_budget_ordered_shops=1|"
                f"unresolved_map_floors=0", shop
            )
            movement = next(c for c in self.audit["cells"]
                            if c["route_ordinal"] == o and c["checkpoint"] == "movement")
            self.assertIn("WarpMan", movement["existing_model"])
            self.assertIn("FREE", movement["existing_model"])
            self.assertIn("existential", movement["unresolved_gap"])

    def test_region_plane_absence_and_original_settlement_limits(self):
        region = self.source_text["region"]
        self.assertIn("COUNT|client_dat_three_plane_floors|761", region)
        self.assertIn("COUNT|server_ls2map_two_plane_floors|65", region)
        self.assertIn("COUNT|materializable_floors|826", region)
        self.assertIn("reward semantics remain OPEN", self.source_text["settlement"])
        self.assertIn("V1_RESOURCE_COMPATIBLE -> EARLY_MEMBERSHIP_PROVEN", self.source_text["policy"])
        for c in self.audit["cells"]:
            if c["checkpoint"] == "region":
                self.assertIn("absent", c["unresolved_gap"])
            if c["checkpoint"] == "settlement":
                self.assertEqual("MODEL_NOT_ORIGINAL_END_TO_END", c["status"])


if __name__ == "__main__":
    unittest.main()
