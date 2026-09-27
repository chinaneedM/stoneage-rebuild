import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_versioned_world_geometry_probe import (
    analyze_world_geometry,
    emit,
)


_SHA_A = "a" * 64
_SHA_B = "b" * 64


def lineage_text():
    return f"""StoneAge later field-map lineage comparison — R1
COUNT|shared_paths|2
COUNT|same_path_same_sha256|2
COUNT|same_path_changed_sha256|0
COUNT|same_sha256_and_tw1_compatible_both|2
STABLE_COMPATIBLE|path=100.dat|width=20|height=20|bytes=2408|sha256={_SHA_A}|required_ids=2|required_cells=2
STABLE_COMPATIBLE|path=200.dat|width=10|height=10|bytes=608|sha256={_SHA_B}|required_ids=2|required_cells=2
RULE|same-path+same-sha256 across later corpora is strong later-lineage persistence, not proof of Taiwan-v1 membership
RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED
"""


def encount_row(floor, index=1, zorder=1):
    values = [
        index, floor, 1, 2, 5, 6, 10, 20, 3, zorder,
        7, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        100, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0,
    ]
    assert len(values) == 33
    return ",".join(str(value) for value in values)


class VersionedWorldGeometryProbeTests(unittest.TestCase):

    def test_extracts_numeric_geometry_without_dialogue_or_template_names(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc_dir = root / "npc"
            data_dir = root / "data"
            map_dir = data_dir / "map"
            npc_dir.mkdir()
            map_dir.mkdir(parents=True)
            lineage = root / "lineage.txt"
            lineage.write_text(lineage_text(), encoding="utf-8")

            (npc_dir / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=WarpTemplateSecret
functionset=Warp
}
{
templatename=WarpManTemplateSecret
functionset=WarpMan
}
{
templatename=TownTemplateSecret
functionset=TownPeople
}
""",
                encoding="utf-8",
            )
            (npc_dir / "base.create").write_text(
                """NPCCREATE
{
floorid=100
borncenter=5,5,0,0
dir=3
createnum=1
time=1000
boundary=1
enemy=WarpTemplateSecret|200|2|3|N
}
{
floorid=100
borncorner=1,1,2,2
movecorner=0,0,3,3
enemy=WarpManTemplateSecret|WARP=200,4,5|DO-NOT-STORE
}
{
floorid=200
borncenter=4,4,2,2
enemy=TownTemplateSecret|DIALOGUE-LIKE-ARG
}
{
floorid=999
borncenter=1,1,0,0
enemy=WarpTemplateSecret|100|1|1
}
""",
                encoding="utf-8",
            )
            for floor in (100, 200):
                (map_dir / f"{floor}.map").write_bytes(
                    b"LS2MAP" + int(floor).to_bytes(2, "big")
                )
            (data_dir / "encount.txt").write_text(
                encount_row(100) + "\n" + encount_row(999, index=2) + "\n",
                encoding="utf-8",
            )

            geometry = analyze_world_geometry(
                lineage_report=lineage,
                npc_dir=npc_dir,
                data_dir=data_dir,
                map_dir=map_dir,
            )

            self.assertEqual(len(geometry.placements), 3)
            self.assertEqual(len(geometry.classic_warps), 1)
            self.assertEqual(len(geometry.encounters), 1)

            warp = geometry.classic_warps[0]
            self.assertEqual(warp.source_floor, 100)
            self.assertEqual(warp.source_rect, (5, 5, 5, 5))
            self.assertTrue(warp.source_is_single_cell)
            self.assertEqual(
                (warp.destination_floor, warp.destination_x, warp.destination_y),
                (200, 2, 3),
            )
            self.assertTrue(warp.conditional_time)
            self.assertTrue(warp.destination_is_stable_candidate)

            by_floor = {
                row.floor_id: row for row in geometry.placements
            }
            self.assertEqual(by_floor[200].birth_rect, (3, 3, 5, 5))
            self.assertEqual(by_floor[200].move_rect, (3, 3, 5, 5))

            encounter = geometry.encounters[0]
            self.assertEqual(encounter.floor_id, 100)
            self.assertEqual(encounter.rect, (1, 2, 5, 6))
            self.assertEqual(encounter.positive_group_ref_count, 1)

            out = io.StringIO()
            with redirect_stdout(out):
                emit(geometry, lineage_report_sha256="f" * 64)
            text = out.getvalue()

            self.assertIn("NPC_PLACEMENT|", text)
            self.assertIn("CLASSIC_WARP|", text)
            self.assertIn("ENCOUNTER_AREA|", text)
            self.assertNotIn("WarpTemplateSecret", text)
            self.assertNotIn("WarpManTemplateSecret", text)
            self.assertNotIn("TownTemplateSecret", text)
            self.assertNotIn("DO-NOT-STORE", text)
            self.assertNotIn("DIALOGUE-LIKE-ARG", text)
            self.assertNotIn("WARP=200,4,5", text)

    def test_two_field_borncenter_uses_source_zero_defaults(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc_dir = root / "npc"
            data_dir = root / "data"
            map_dir = data_dir / "map"
            npc_dir.mkdir()
            map_dir.mkdir(parents=True)
            lineage = root / "lineage.txt"
            lineage.write_text(lineage_text(), encoding="utf-8")

            (npc_dir / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=PointNpc
functionset=TownPeople
}
""",
                encoding="utf-8",
            )
            (npc_dir / "base.create").write_text(
                """NPCCREATE
{
floorid=100
borncenter=7,9
enemy=PointNpc
}
""",
                encoding="utf-8",
            )
            for floor in (100, 200):
                (map_dir / f"{floor}.map").write_bytes(
                    b"LS2MAP" + int(floor).to_bytes(2, "big")
                )
            (data_dir / "encount.txt").write_text(
                encount_row(100) + "\n",
                encoding="utf-8",
            )

            geometry = analyze_world_geometry(
                lineage_report=lineage,
                npc_dir=npc_dir,
                data_dir=data_dir,
                map_dir=map_dir,
            )

        self.assertEqual(len(geometry.placements), 1)
        self.assertEqual(geometry.placements[0].birth_rect, (7, 9, 7, 9))
        self.assertEqual(geometry.placements[0].move_rect, (7, 9, 7, 9))

    def test_warpman_is_not_flattened_into_classic_warp(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc_dir = root / "npc"
            data_dir = root / "data"
            map_dir = data_dir / "map"
            npc_dir.mkdir()
            map_dir.mkdir(parents=True)
            lineage = root / "lineage.txt"
            lineage.write_text(lineage_text(), encoding="utf-8")

            (npc_dir / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=ConditionalTransport
functionset=WarpMan
}
""",
                encoding="utf-8",
            )
            (npc_dir / "base.create").write_text(
                """NPCCREATE
{
floorid=100
borncenter=5,5,0,0
enemy=ConditionalTransport|WARP=200,2,3|MONEY=999
}
""",
                encoding="utf-8",
            )
            for floor in (100, 200):
                (map_dir / f"{floor}.map").write_bytes(
                    b"LS2MAP" + int(floor).to_bytes(2, "big")
                )
            (data_dir / "encount.txt").write_text(
                encount_row(100) + "\n",
                encoding="utf-8",
            )

            geometry = analyze_world_geometry(
                lineage_report=lineage,
                npc_dir=npc_dir,
                data_dir=data_dir,
                map_dir=map_dir,
            )
            self.assertEqual(len(geometry.placements), 1)
            self.assertEqual(len(geometry.classic_warps), 0)

    def test_nonstable_floors_are_not_promoted_into_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc_dir = root / "npc"
            data_dir = root / "data"
            map_dir = data_dir / "map"
            npc_dir.mkdir()
            map_dir.mkdir(parents=True)
            lineage = root / "lineage.txt"
            lineage.write_text(lineage_text(), encoding="utf-8")

            (npc_dir / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=WarpX
functionset=Warp
}
""",
                encoding="utf-8",
            )
            (npc_dir / "base.create").write_text(
                """NPCCREATE
{
floorid=999
borncenter=1,1,0,0
enemy=WarpX|100|1|1
}
""",
                encoding="utf-8",
            )
            for floor in (100, 200):
                (map_dir / f"{floor}.map").write_bytes(
                    b"LS2MAP" + int(floor).to_bytes(2, "big")
                )
            (data_dir / "encount.txt").write_text(
                encount_row(999) + "\n",
                encoding="utf-8",
            )

            geometry = analyze_world_geometry(
                lineage_report=lineage,
                npc_dir=npc_dir,
                data_dir=data_dir,
                map_dir=map_dir,
            )
            self.assertEqual(geometry.placements, ())
            self.assertEqual(geometry.classic_warps, ())
            self.assertEqual(geometry.encounters, ())


if __name__ == "__main__":
    unittest.main()
