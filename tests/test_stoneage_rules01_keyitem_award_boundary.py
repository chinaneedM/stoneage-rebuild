"""RULES-01 alternate key-item award report: immutable source and scope guards."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-RULES01-KEYITEM-AWARD-BOUNDARY-R1.json"


class KeyItemAwardBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=json.loads(REPORT.read_text(encoding="utf-8"))

    def test_seven_exact_source_pins(self):
        self.assertEqual(7,len(self.audit["source_pins"]))
        for key,src in self.audit["source_pins"].items():
            payload=(ROOT/src["path"]).read_bytes()
            self.assertEqual(src["bytes"],len(payload),key)
            git=hashlib.sha1(
                b"blob "+str(len(payload)).encode("ascii")+bytes([0])+payload
            ).hexdigest()
            self.assertEqual(src["git_blob"],git,key)

    def test_exchange_awards_do_not_become_early_quest_or_shop_route(self):
        report=self.audit
        self.assertEqual("LATER_RECOVERED",report["evidence_role"])
        self.assertEqual("OPEN",report["early_JSS1999_TW10_membership"])
        self.assertEqual(5,len(report["tracks"]))
        by_id={x["id"]:x for x in report["tracks"]}
        self.assertEqual(len(by_id),len(report["tracks"]))
        self.assertEqual(2,by_id["EXCHANGEMAN_EVENT_AWARD"]["count_records"])
        self.assertEqual(2,by_id["BRIDGE_SHOP_TO_WARPMAN"]["count_routes"])
        text=(ROOT/report["source_pins"]["exchange"]["path"]).read_text(encoding="utf-8")
        for marker in (
            "COUNT|matching_award_records|2",
            "COUNT|records_with_delstone|2",
            "COUNT|target_deleted_records|0",
            "COUNT|target_required_by_event_records|0",
            "field_keys=ACCEPTMSG,DELSTONE,EVENT,EVENTNO,GETITEM,",
        ):
            self.assertIn(marker,text)
        self.assertIn("Do not merge with the 3/4 shop routes.",by_id["EXCHANGEMAN_EVENT_AWARD"]["boundary"])

    def test_negative_item_probe_not_claimed_universal(self):
        source=self.audit["source_pins"]
        npc=(ROOT/source["npc_refs"]["path"]).read_text(encoding="utf-8")
        nonshop=(ROOT/source["nonshop"]["path"]).read_text(encoding="utf-8")
        self.assertIn(
            "NPC_KEY_ITEM_REFERENCE|function=WarpMan|field=DelItem|create_rows=1",npc
        )
        self.assertIn("ACQUISITION_SURFACE|battle_drop=0|npc_reward=0|",nonshop)
        self.assertIn(
            "not a claim that no alternate acquisition exists",
            next(t["boundary"] for t in self.audit["tracks"]
                 if t["id"]=="NONSHOP_DROP_AND_NPC_ADD_ITEM_NEGATIVE")
        )
        self.assertTrue(any("same executed branch" in x for x in self.audit["forbidden_promotions"]))

    def test_logout_save_persistence_boundary_remains_open(self):
        self.assertTrue(self.audit["original_payloads_retained"] is False)
        save=(ROOT/self.audit["source_pins"]["save"]["path"]).read_text(encoding="utf-8")
        self.assertIn("ITEM_DROPATLOGOUT",save)
        self.assertIn("unlock",save.lower())
        self.assertIn("DROPATLOGOUT",self.audit["material_gap"]+" "+
            next(t["boundary"] for t in self.audit["tracks"]
                 if t["id"]=="DURABLE_ITEM_AND_AWARD_LIMIT"))
        self.assertIn("OPEN",self.audit["early_JSS1999_TW10_membership"])


if __name__=="__main__":
    unittest.main()
