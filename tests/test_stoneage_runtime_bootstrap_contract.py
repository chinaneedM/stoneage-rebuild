import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTRACT_PATH=ROOT/"game"/"RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"


def _read(path):
    return (ROOT/path).read_text(encoding="utf-8")


def _route_rows(text):
    out={}
    for raw in text.splitlines():
        if not raw.startswith("ALL_HOMETOWN_ORDERED_ROUTE|"):
            continue
        fields={}
        for token in raw.split("|")[1:]:
            key,value=token.split("=",1)
            fields[key]=value
        out[int(fields["ordinal"])]=fields
    return out


class RuntimeBootstrapContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.all_hometown=_read("research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-ALL-HOMETOWN-PROGRESSION-R1.txt")
        cls.shop=_read("research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-WARPMAN-BRIDGE-SHOP-ROUTE-R1.txt")
        cls.gate=_read("research/recovered/STONEAGE-25-SHADOWED-BRANCH-FRESH-START-WARPMAN-BRIDGE-GATE-R1.txt")
        cls.world=_read("research/recovered/STONEAGE-25-STATE-GATED-RUNTIME-WORLD-REACHABILITY-R1.txt")
        cls.fresh_world=_read("research/recovered/STONEAGE-25-FRESH-START-STATE-GATED-RUNTIME-WORLD-REACHABILITY-R1.txt")

    def test_version_and_provenance_are_not_conflated(self):
        c=self.contract
        self.assertEqual(c["historical_foundation"]["profile"],"taiwan-v1.0")
        self.assertEqual(c["runtime_world_profile"]["profile"],"recovered25")
        self.assertEqual(c["runtime_world_profile"]["evidence_role"],"LATER_RECOVERED")
        self.assertEqual(c["runtime_world_profile"]["historical_membership_in_taiwan_v1"],"UNPROVEN")
        self.assertFalse(c["runtime_world_profile"]["may_be_relabelled_as_taiwan_v1_content"])

    def test_local_first_runtime_boundary(self):
        d=self.contract["deployment"]
        self.assertEqual(d["mode"],"LOCAL_FIRST_SINGLE_PLAYER")
        self.assertEqual(d["authoritative_state"],"LOCAL_WORLD_MODEL")
        self.assertFalse(d["legacy_network_transport_required"])
        self.assertFalse(d["account_service_required"])
        self.assertEqual(d["engine_binding"],"NONE")

    def test_world_counts_match_closed_reports(self):
        w=self.contract["world"]
        self.assertEqual(w["materializable_floor_count"],826)
        self.assertEqual(w["fresh_start_state_gated_reachable_floor_count"],826)
        self.assertEqual(w["remaining_unreachable_floor_count"],0)
        self.assertIn("COUNT|materializable_floor_ids|826",self.fresh_world)
        self.assertIn("COUNT|fresh_start_state_gated_reachable_floor_ids|826",self.fresh_world)
        self.assertIn("COUNT|fresh_start_remaining_unreachable_floor_ids|0",self.fresh_world)
        self.assertIn("COUNT|remaining_unreachable_floor_ids|0",self.world)

    def test_all_hometown_routes_match_final_ordered_report(self):
        report_rows=_route_rows(self.all_hometown)
        routes={row["ordinal"]:row for row in self.contract["fresh_start"]["routes"]}
        self.assertEqual(set(report_rows),{1,2,3,4})
        self.assertEqual(set(routes),{1,2,3,4})
        for ordinal in (1,2,3,4):
            self.assertEqual(report_rows[ordinal]["ordered"],"1")
            self.assertTrue(routes[ordinal]["ordered"])
            reported=[] if report_rows[ordinal]["milestones"]=="NONE" else report_rows[ordinal]["milestones"].split(">")
            self.assertEqual(routes[ordinal]["milestones"],reported)
        self.assertIn("FRESH_START_ALL_HOMETOWNS_ORDERED_PROGRESSION|witness=1",self.all_hometown)
        self.assertIn("ALL_HOMETOWNS_FULL_WORLD|closed=1",self.all_hometown)

    def test_starter_inventory_and_shop_prerequisites_match_report(self):
        inv=self.contract["fresh_start"]["inventory"]
        self.assertEqual(inv,{"capacity":15,"configured_positive_starter_items":13,"guaranteed_empty_slots":2})
        self.assertIn("STARTER_INVENTORY|config_keys_present=15|positive_item_configs=13|guaranteed_empty_slots=2|item_ids_withheld=1",self.shop)
        self.assertIn("FRESH_START_ALL_FAILED_HOMETOWNS_STARTING_STONE_COVERS_SHOP_AND_AWARD|witness=1",self.shop)
        self.assertIn("FRESH_START_ALL_FAILED_HOMETOWNS_WARPMAN_EXECUTION_PREREQUISITES|witness=1",self.shop)

    def test_hometown_warpman_bridges_remain_conditional(self):
        transitions={x["id"]:x for x in self.contract["state_gated_transitions"]}
        for ordinal in (3,4):
            row=transitions[f"fresh_start_hometown_{ordinal}_bridge"]
            self.assertFalse(row["unconditional"])
            self.assertEqual(row["predicates"],["ITEM_EQ"])
            self.assertEqual(row["money_gate"],"DISABLED_NEGATIVE")
            self.assertEqual(row["schedule_gate"],"ABSENT")
            self.assertEqual(row["party_gate"],"ABSENT")
            self.assertTrue(row["free_msg_required_and_present"])
            self.assertEqual(row["event_action_side_effect_fields"],0)
        self.assertIn("COUNT|free_kind:ITEM:edges|2",self.gate)
        self.assertIn("COUNT|money_class:NEGATIVE_DISABLED|2",self.gate)
        self.assertIn("COUNT|newtime_present:0|2",self.gate)
        self.assertIn("COUNT|checkparty_present:0|2",self.gate)

    def test_shadowed_branch_ingress_remains_state_gated(self):
        row=next(x for x in self.contract["state_gated_transitions"] if x["id"]=="shadowed_branch_ingress")
        self.assertFalse(row["unconditional"])
        self.assertEqual((row["source_floor"],row["destination_floor"]),(811,820))
        self.assertIn("GATED_TRANSPORT|source_floor=811|destination_floor=820|progression_witness=1",self.world)


if __name__=="__main__":
    unittest.main()
