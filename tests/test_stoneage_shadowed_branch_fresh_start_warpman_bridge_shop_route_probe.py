import tempfile
import unittest
from pathlib import Path

from tools.stoneage_shadowed_branch_fresh_start_warpman_bridge_shop_route_probe import (
    _bridge_execution_profile,
    _normal_buy_shape,
    _purchase_price,
    _starter_inventory,
    _target_item_cost,
)


def _row(item_id:int,cost:int)->bytes:
    fields=[b""]*19
    fields[16]=str(item_id).encode("ascii")
    fields[18]=str(cost).encode("ascii")
    return b",".join(fields)


class FreshStartWarpManBridgeShopRouteProbeTests(unittest.TestCase):

    def test_target_item_cost_uses_recovered_itemset_id_and_cost_columns(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"itemset.txt"
            path.write_bytes(_row(10,50)+b"\n"+_row(20,125)+b"\n")
            self.assertEqual(_target_item_cost((path,),20),125)

    def test_purchase_price_matches_fixed_descendant_integer_truncation(self):
        self.assertEqual(_purchase_price(125,0.5),62)
        self.assertEqual(_purchase_price(125,1.0),125)
        self.assertIsNone(_purchase_price(125,-1.0))

    def test_starter_inventory_requires_all_15_keys_and_bounds_filled_slots(self):
        with tempfile.TemporaryDirectory() as td:
            setup=Path(td)/"setup.cf"
            setup.write_text(
                "\n".join(
                    f"ITEM{i}={101 if i==1 else -1}"
                    for i in range(1,16)
                )+"\n",
                encoding="utf-8",
            )
            self.assertEqual(_starter_inventory(setup),(15,1,14))

            setup.write_text(
                "\n".join(
                    f"ITEM{i}={101 if i==1 else ''}"
                    for i in range(1,16)
                )+"\n",
                encoding="utf-8",
            )
            self.assertEqual(_starter_inventory(setup),(15,1,14))

            setup.write_text("ITEM1=101\n",encoding="utf-8")
            self.assertEqual(_starter_inventory(setup),(1,1,0))

    def test_bridge_execution_profile_tracks_free_msg_and_action_fields(self):
        clean=_bridge_execution_profile(
            3,b"WARP:2,3,4|FREE:ITEM=10|FreeMsg:ok|PayMsg:no|MONEY:-1"
        )
        self.assertTrue(clean.free_msg_present)
        self.assertEqual(clean.event_action_fields,())

        active=_bridge_execution_profile(
            4,b"WARP:2,3,4|FREE:ITEM=10|FreeMsg:ok|DelItem:10|WARPPOINT:5,6,7"
        )
        self.assertEqual(active.event_action_fields,("DELITEM","WARPPOINT"))

    def test_normal_buy_invocation_rejects_limitshop_and_accepts_menu_or_keyword(self):
        self.assertEqual(
            _normal_buy_shape(b"ItemList:1,2|main_msg:x"),
            (True,False,False,False,False),
        )
        self.assertEqual(
            _normal_buy_shape(b"ItemList:1,2|EVENT:1|buy_msg:buy"),
            (True,False,True,False,True),
        )
        self.assertEqual(
            _normal_buy_shape(b"ItemList:1,2|LIMITSHOP:1|buy_msg:buy"),
            (False,True,False,False,True),
        )


if __name__=="__main__":
    unittest.main()
