import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.stoneage_server_only_floor_gameplay_probe import (
    analyze,
)


PAYLOAD = """StoneAge missing-DAT warp destination payload audit — R1
EVIDENCE_ROLE|LATER_RECOVERED
COUNT|client_map_present:0:edges|2
COUNT|client_map_present:0:ids|2
COUNT|missing_dat_destination_ids|2
COUNT|missing_dat_edges|2
COUNT|server_map_present:1:edges|2
COUNT|server_map_present:1:ids|2
COUNT|status:SERVER_MAP_ONLY:edges|2
COUNT|status:SERVER_MAP_ONLY:ids|2
MISSING_DAT_DESTINATION|floor=20002|edge_refs=1|status=SERVER_MAP_ONLY|client_map_paths=|client_map_dimensions=|client_map_sha256=|server_map_paths=a|server_map_dimensions=50x100
MISSING_DAT_DESTINATION|floor=20004|edge_refs=1|status=SERVER_MAP_ONLY|client_map_paths=|client_map_dimensions=|client_map_sha256=|server_map_paths=b|server_map_dimensions=80x80
RESOLUTION|MISSING_DAT_WARP_DESTINATION_PAYLOADS_CLASSIFIED
"""


class ServerOnlyFloorGameplayProbeTests(unittest.TestCase):

    def test_target_floor_npc_and_classic_warp_are_derived_without_names(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            data = root / "data"
            npc.mkdir()
            data.mkdir()

            (npc / "template.txt").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=Gate\nFunctionSet=Warp\n}\n"
                b"{\nTemplateName=Other\nFunctionSet=Talk\n}\n"
            )
            (npc / "create.txt").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=20002\nBornCenter=1,1\n"
                b"Enemy=Gate|20003|7|8\n}\n"
                b"{\nFloorId=20002\nBornCenter=2,2\nEnemy=Other\n}\n"
                b"{\nFloorId=99999\nBornCenter=2,2\n"
                b"Enemy=Gate|1|2|3\n}\n"
            )

            with patch(
                "tools.stoneage_server_only_floor_gameplay_probe."
                "_encounter_floor_counts",
                return_value=(
                    "encount.txt",
                    {20002: 2, 20004: 1},
                    {20002: 1},
                ),
            ):
                audit = analyze(
                    payload_report_text=PAYLOAD,
                    npc_dir=npc,
                    data_dir=data,
                    setup=None,
                )

            by_id = {row.floor_id: row for row in audit.rows}
            self.assertEqual(by_id[20002].npc_create_count, 2)
            self.assertEqual(by_id[20002].warp_create_count, 1)
            self.assertEqual(
                by_id[20002].classic_warp_edges,
                ((20003, 7, 8),),
            )
            self.assertEqual(by_id[20002].encounter_row_count, 2)
            self.assertEqual(by_id[20002].active_encounter_row_count, 1)
            self.assertEqual(by_id[20004].npc_create_count, 0)
            self.assertEqual(audit.counts["target_floors"], 2)
            self.assertEqual(audit.counts["classic_warp_edges"], 1)

    def test_missing_born_definition_is_not_counted_as_effective_spawn(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            data = root / "data"
            npc.mkdir()
            data.mkdir()
            (npc / "template").write_bytes(
                b"NPCTEMPLATE\n"
                b"{\nTemplateName=Gate\nFunctionSet=Warp\n}\n"
            )
            (npc / "create").write_bytes(
                b"NPCCREATE\n"
                b"{\nFloorId=20002\nEnemy=Gate|20003|7|8\n}\n"
            )
            with patch(
                "tools.stoneage_server_only_floor_gameplay_probe."
                "_encounter_floor_counts",
                return_value=("encount.txt", {}, {}),
            ):
                audit = analyze(
                    payload_report_text=PAYLOAD,
                    npc_dir=npc,
                    data_dir=data,
                    setup=None,
                )
            self.assertEqual(audit.rows[0].npc_create_count, 0)
            self.assertEqual(audit.rows[0].classic_warp_edges, ())


if __name__ == "__main__":
    unittest.main()
