import io
import struct
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_world_content_coverage_probe import (
    analyze_world_content_coverage,
    emit,
)
from tools.stoneage_world_map_library import parse_stable_later_map_manifest


_SHA_A = "a" * 64
_SHA_B = "b" * 64


def lineage_text():
    return f"""StoneAge later field-map lineage comparison — R1
COUNT|shared_paths|2
COUNT|same_path_same_sha256|2
COUNT|same_path_changed_sha256|0
COUNT|same_sha256_and_tw1_compatible_both|2
STABLE_COMPATIBLE|path=100.dat|width=2|height=2|bytes=32|sha256={_SHA_A}|required_ids=2|required_cells=4
STABLE_COMPATIBLE|path=200.dat|width=1|height=2|bytes=20|sha256={_SHA_B}|required_ids=1|required_cells=2
RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED
"""


def encount_row(floor, zorder=1):
    values = [
        1,
        floor,
        0,
        0,
        10,
        10,
        1,
        5,
        3,
        zorder,
        *([-1] * 10),
        *([-1] * 10),
        0,
        0,
        0,
    ]
    assert len(values) == 33
    return ",".join(str(value) for value in values)


class WorldContentCoverageProbeTests(unittest.TestCase):

    def test_cross_domain_coverage_stays_floor_level_and_versioned(self):
        manifest = parse_stable_later_map_manifest(lineage_text())

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc_dir = root / "npc"
            data_dir = root / "data"
            map_dir = data_dir / "map"
            npc_dir.mkdir(parents=True)
            map_dir.mkdir(parents=True)

            (npc_dir / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=WarpTemplate
functionset=Warp
}
{
templatename=TownTemplate
functionset=TownPeople
}
""",
                encoding="utf-8",
            )
            (npc_dir / "base.create").write_text(
                """NPCCREATE
{
floorid=100
borncenter=1,1
enemy=WarpTemplate|secret-argument
}
{
floorid=200
borncenter=1,1
enemy=TownTemplate|other-secret
}
{
floorid=999
borncenter=1,1
enemy=WarpTemplate|ignored-non-server-map
}
""",
                encoding="utf-8",
            )

            for floor in (100, 200):
                (map_dir / f"{floor}.map").write_bytes(
                    b"LS2MAP" + struct.pack(">H", floor)
                )

            (data_dir / "encount.txt").write_text(
                encount_row(100, 1) + "\n" + encount_row(300, 1) + "\n",
                encoding="utf-8",
            )

            coverage = analyze_world_content_coverage(
                manifest=manifest,
                npc_dir=npc_dir,
                data_dir=data_dir,
                map_dir=map_dir,
            )

        by_floor = {row.floor_id: row for row in coverage.floors}
        self.assertEqual(set(by_floor), {100, 200})
        self.assertEqual(coverage.server_map_id_count, 2)
        self.assertEqual(coverage.npc_effective_floor_count, 2)
        self.assertEqual(coverage.encounter_floor_count, 2)
        self.assertEqual(coverage.active_encounter_floor_count, 2)

        self.assertTrue(by_floor[100].server_map_present)
        self.assertEqual(by_floor[100].npc_create_count, 1)
        self.assertEqual(by_floor[100].warp_functionset_create_count, 1)
        self.assertEqual(by_floor[100].encounter_row_count, 1)

        self.assertTrue(by_floor[200].server_map_present)
        self.assertEqual(by_floor[200].npc_create_count, 1)
        self.assertEqual(by_floor[200].warp_functionset_create_count, 0)
        self.assertEqual(by_floor[200].encounter_row_count, 0)

    def test_emitted_manifest_contains_no_npc_argument_or_coordinate_payload(self):
        manifest = parse_stable_later_map_manifest(lineage_text())

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc_dir = root / "npc"
            data_dir = root / "data"
            map_dir = data_dir / "map"
            npc_dir.mkdir(parents=True)
            map_dir.mkdir(parents=True)

            (npc_dir / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=WarpTemplate
functionset=Warp
}
""",
                encoding="utf-8",
            )
            (npc_dir / "base.create").write_text(
                """NPCCREATE
{
floorid=100
borncenter=77,88
enemy=WarpTemplate|DO-NOT-LEAK
}
""",
                encoding="utf-8",
            )
            (map_dir / "100.map").write_bytes(
                b"LS2MAP" + struct.pack(">H", 100)
            )
            (data_dir / "encount.txt").write_text(
                encount_row(100, 1) + "\n",
                encoding="utf-8",
            )

            coverage = analyze_world_content_coverage(
                manifest=manifest,
                npc_dir=npc_dir,
                data_dir=data_dir,
                map_dir=map_dir,
            )
            out = io.StringIO()
            with redirect_stdout(out):
                emit(coverage, lineage_report_sha256="f" * 64)
            text = out.getvalue()

        self.assertNotIn("DO-NOT-LEAK", text)
        self.assertNotIn("77,88", text)
        self.assertNotIn("WarpTemplate", text)
        self.assertIn("COUNT|stable_floor_candidates|2", text)
        self.assertEqual(
            sum(1 for line in text.splitlines() if line.startswith("FLOOR|")),
            2,
        )
        self.assertIn(
            "RULE|recovered25 world semantics remain LATER_RECOVERED",
            text,
        )


if __name__ == "__main__":
    unittest.main()
