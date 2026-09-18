import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_transport_usage_probe import analyze,emit

TPL=b"""NPCTEMPLATE
{
templatename=B
functionset=Bus
}
{
templatename=A
functionset=Airplane
}
"""
CREATE=b"""NPCCREATE
{
enemy=B|file:bus.arg
}
{
enemy=A|file:air.arg
}
"""
BUS=b"""routenum:2
routeto1:1,2;3,4
routeto2:5,6;7,8;9,10
waittime:30
reverse:1
allowitem:100,100
pickupitem:1
needstone:50
"""
AIR=b"""routenum:1
routeto1:1,2,3;2,4,5
oneway:1
needlevel:10
WAVE:88
delitem:9
maxlevel:80
"""

class ProbeTests(unittest.TestCase):
    def build(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        (root/"x.template").write_bytes(TPL)
        (root/"x.create").write_bytes(CREATE)
        (root/"bus.arg").write_bytes(BUS)
        (root/"air.arg").write_bytes(AIR)
        return td,root

    def test_counts_and_shapes(self):
        td,root=self.build()
        try:
            result=analyze(root)
            self.assertEqual(result["counts"][("Bus","refs")],1)
            self.assertEqual(result["counts"][("Airplane","refs")],1)
            self.assertEqual(
                result["counts"][("Airplane","routes_with_floor_change")],1
            )
            self.assertEqual(result["route_lengths"][("Bus",2)],1)
            self.assertEqual(result["route_lengths"][("Bus",3)],1)
            self.assertEqual(result["point_arities"][("Airplane",3)],2)
        finally:
            td.cleanup()

    def test_scalar_and_item_aggregates(self):
        td,root=self.build()
        try:
            result=analyze(root)
            self.assertEqual(result["scalars"][("Bus","needstone",50)],1)
            self.assertEqual(result["scalars"][("Airplane","maxlevel",80)],1)
            self.assertEqual(result["item_lengths"][("Bus","allowitem",2)],1)
            self.assertEqual(result["counts"][("Bus","allowitem_duplicates")],1)
        finally:
            td.cleanup()

    def test_output_drops_route_and_item_payloads(self):
        td,root=self.build()
        try:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                emit(analyze(root))
            text=out.getvalue()
            self.assertNotIn("1,2;3,4",text)
            self.assertNotIn("100,100",text)
            self.assertNotIn("bus.arg",text)
            self.assertIn(
                "SCALAR|Bus|needstone|value=50|blocks=1",text
            )
        finally:
            td.cleanup()

    def test_missing_file_counted(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"x.template").write_bytes(TPL)
            (root/"x.create").write_bytes(
                b"NPCCREATE\n{\nenemy=B|file:no.arg\n}\n"
            )
            result=analyze(root)
            self.assertEqual(result["counts"][("Bus","missing_files")],1)

if __name__=="__main__":
    unittest.main()
