import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_npc_world_graph_probe import (
    analyze,
    magic_kind,
)


TEMPLATE = b"""NPCTEMPLATE
{
templatename=BaseA
name=ignored
functionset=Warp
talkedfunc=CustomTalk
}
{
templatename=BaseB
functionset=SavePoint
}
"""

CREATE = b"""NPCCREATE
{
floorid=100
borncenter=5,5,1,1
enemy=BaseA|ARG=SECRET
enemy=Missing
time=1000
createnum=1
}
{
floorid=200
borncorner=1,1,2,2
movecorner=1,1,3,3
enemy=BaseB
boundary=1
}
"""


def write_ls2map(path, map_id):
    path.write_bytes(b"LS2MAP" + struct.pack(">H", map_id))


class NPCWorldGraphProbeTests(unittest.TestCase):
    def test_magic_detection_rejects_backup(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            good = root / "a.template"
            bad = root / "b.template.bak"
            good.write_bytes(TEMPLATE)
            bad.write_bytes(TEMPLATE)
            self.assertEqual(magic_kind(good), "template")
            self.assertIsNone(magic_kind(bad))

    def test_graph_resolves_templates_and_map_floors(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            maps = root / "map"
            npc.mkdir()
            maps.mkdir()
            (npc / "all.template").write_bytes(TEMPLATE)
            (npc / "world.create").write_bytes(CREATE)
            write_ls2map(maps / "100.map", 100)

            r = analyze(npc, map_dir=maps)
            c = r["counts"]
            self.assertEqual(c["template_magic_files"], 1)
            self.assertEqual(c["create_magic_files"], 1)
            self.assertEqual(c["template_blocks"], 2)
            self.assertEqual(c["create_blocks_raw"], 2)
            self.assertEqual(c["create_template_refs_total"], 3)
            self.assertEqual(c["create_template_refs_resolved"], 2)
            self.assertEqual(c["create_unresolved_template_refs"], 1)
            self.assertEqual(c["create_blocks_pre_map_valid"], 2)
            self.assertEqual(c["create_blocks_effective_map_valid"], 1)
            self.assertEqual(c["create_blocks_missing_floor"], 1)
            self.assertEqual(c["create_refs_with_argument"], 1)
            self.assertEqual(c["unique_effective_floor_candidates"], 2)

    def test_functionset_and_direct_override_are_counted_separately(self):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            (npc / "all.template").write_bytes(TEMPLATE)
            r = analyze(npc)
            self.assertEqual(r["functionsets"]["Warp"], 1)
            self.assertEqual(r["functionsets"]["SavePoint"], 1)
            self.assertEqual(r["direct_slots"]["talkedfunc"], 1)
            self.assertEqual(r["counts"]["template_with_direct_func_override"], 1)

    def test_duplicate_template_names_are_visible(self):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            (npc / "dup.template").write_bytes(
                b"""NPCTEMPLATE
{
templatename=Same
functionset=Warp
}
{
templatename=Same
functionset=Door
}
"""
            )
            (npc / "dup.create").write_bytes(
                b"NPCCREATE\n{\nfloorid=1\nborncenter=1,1,1,1\nenemy=Same\n}\n"
            )
            r = analyze(npc)
            self.assertEqual(r["counts"]["template_duplicate_name_values"], 1)
            self.assertEqual(r["counts"]["template_duplicate_extra_blocks"], 1)
            self.assertEqual(r["counts"]["template_unique_name_values"], 1)
            self.assertEqual(r["counts"]["create_refs_to_duplicate_template_name"], 1)
            self.assertEqual(r["counts"]["create_blocks_with_duplicate_template_ref"], 1)
            self.assertEqual(r["counts"]["duplicate_template_names_referenced"], 1)

    def test_create_without_born_is_not_pre_map_valid(self):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            (npc / "x.template").write_bytes(
                b"NPCTEMPLATE\n{\ntemplatename=A\nfunctionset=Warp\n}\n"
            )
            (npc / "x.create").write_bytes(
                b"NPCCREATE\n{\nfloorid=1\nenemy=A\n}\n"
            )
            r = analyze(npc)
            self.assertEqual(r["counts"]["create_blocks_pre_map_valid"], 0)

    def test_unresolved_only_create_is_not_effective(self):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            (npc / "x.template").write_bytes(
                b"NPCTEMPLATE\n{\ntemplatename=A\n}\n"
            )
            (npc / "x.create").write_bytes(
                b"NPCCREATE\n{\nfloorid=1\nborncenter=1,1,1,1\nenemy=B\n}\n"
            )
            r = analyze(npc)
            self.assertEqual(r["counts"]["create_template_refs_resolved"], 0)
            self.assertEqual(r["counts"]["create_unresolved_template_refs"], 1)
            self.assertEqual(r["counts"]["create_blocks_pre_map_valid"], 0)

    def test_more_than_eight_resolved_refs_flags_source_capacity_hazard(self):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            templates = [b"NPCTEMPLATE"]
            for i in range(9):
                templates.extend(
                    [b"{", f"templatename=T{i}".encode(), b"functionset=Warp", b"}"]
                )
            (npc / "x.template").write_bytes(b"\n".join(templates) + b"\n")
            create = [b"NPCCREATE", b"{", b"floorid=1", b"borncenter=1,1,1,1"]
            create.extend(f"enemy=T{i}".encode() for i in range(9))
            create.append(b"}")
            (npc / "x.create").write_bytes(b"\n".join(create) + b"\n")
            r = analyze(npc)
            self.assertEqual(r["counts"]["create_resolved_refs_over_8"], 1)
            self.assertEqual(r["resolved_per_block"][9], 1)

    def test_setup_limits_are_reported(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            npc.mkdir()
            setup = root / "setup.cf"
            setup.write_text(
                "npcdir=data/npc\nfilesearchnum=10000\n"
                "npctemplatenum=256\nnpccreatenum=10000\n",
                encoding="utf-8",
            )
            r = analyze(npc, setup=setup)
            self.assertEqual(r["config"]["npcdir"], "data/npc")
            self.assertEqual(r["config"]["npctemplatenum"], "256")

    def test_floor_range_uses_syntactically_effective_create_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            npc = Path(td)
            (npc / "x.template").write_bytes(
                b"NPCTEMPLATE\n{\ntemplatename=A\n}\n"
            )
            (npc / "x.create").write_bytes(
                b"""NPCCREATE
{
floorid=30
borncenter=1,1,1,1
enemy=A
}
{
floorid=10
borncenter=1,1,1,1
enemy=A
}
"""
            )
            r = analyze(npc)
            self.assertEqual(r["floor_range"], (10, 30))


if __name__ == "__main__":
    unittest.main()
