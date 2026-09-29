import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_warp_destination_corpus_probe import (
    CHANGED,
    SAME_SHA_NONSTABLE,
    classify,
    emit,
    parse_outside_destinations,
)


def _dat(*values):
    width = height = 1
    tile, parts, event = values
    return (
        struct.pack("<II", width, height)
        + struct.pack("<3H", tile, parts, event)
    )


def _geometry():
    return "\n".join(
        [
            "COUNT|classic_warp_edges|3",
            "COUNT|classic_warp_destinations_stable|0",
            (
                "CLASSIC_WARP|floor=1|placement=1|source=0,0,0,0|"
                "to=100,1,1|conditional_time=0|destination_stable=0"
            ),
            (
                "CLASSIC_WARP|floor=1|placement=2|source=0,0,0,0|"
                "to=100,2,2|conditional_time=0|destination_stable=0"
            ),
            (
                "CLASSIC_WARP|floor=1|placement=3|source=0,0,0,0|"
                "to=200,3,3|conditional_time=0|destination_stable=0"
            ),
        ]
    )


def _lineage(changed_sha):
    return "\n".join(
        [
            "SOURCE_A|label=recovered25|valid_maps=2|invalid=0|compatible=1",
            "SOURCE_B|label=archived2003|valid_maps=2|invalid=0|compatible=0",
            "COUNT|shared_paths|2",
            "COUNT|same_path_same_sha256|1",
            "COUNT|same_path_changed_sha256|1",
            "COUNT|same_sha256_and_tw1_compatible_both|0",
            "COUNT|changed_sha256_and_tw1_compatible_both|0",
            "COUNT|only_recovered25|0",
            "COUNT|only_archived2003|0",
            (
                "CHANGED|path=100.dat|sha_a="
                + changed_sha
                + "|sha_b="
                + ("b" * 64)
                + "|compat_a=1|compat_b=0|size_a=1x1|size_b=1x1"
            ),
            "RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED",
        ]
    )


class WarpDestinationCorpusProbeTests(unittest.TestCase):

    def test_outside_destination_parser_preserves_edge_multiplicity(self):
        refs, total = parse_outside_destinations(_geometry())
        self.assertEqual(total, 3)
        self.assertEqual(refs, {100: 2, 200: 1})

    def test_direct_client_dat_classification_separates_change_and_compat(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            changed = root / "100.dat"
            unchanged = root / "200.DAT"
            changed.write_bytes(_dat(100, 0, 0))
            unchanged.write_bytes(_dat(101, 0, 0))

            import hashlib
            changed_sha = hashlib.sha256(changed.read_bytes()).hexdigest()
            audit = classify(
                geometry_text=_geometry(),
                lineage_text=_lineage(changed_sha),
                map_root=root,
                profile_ids={100},
            )

            self.assertEqual(len(audit.rows), 2)
            by_id = {row.floor_id: row for row in audit.rows}
            self.assertEqual(by_id[100].status, CHANGED)
            self.assertTrue(by_id[100].recovered25_tw1_asset_compatible)
            self.assertFalse(by_id[100].archived2003_tw1_asset_compatible)
            self.assertEqual(by_id[100].edge_refs, 2)

            self.assertEqual(by_id[200].status, SAME_SHA_NONSTABLE)
            self.assertFalse(by_id[200].recovered25_tw1_asset_compatible)
            self.assertFalse(by_id[200].archived2003_tw1_asset_compatible)

            self.assertEqual(audit.counts["outside_stable_edges"], 3)
            self.assertEqual(audit.counts["status:CHANGED:ids"], 1)
            self.assertEqual(
                audit.counts["status:SAME_SHA_NONSTABLE:ids"],
                1,
            )

    def test_report_emits_no_map_payload(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            changed = root / "100.dat"
            unchanged = root / "200.dat"
            changed.write_bytes(_dat(100, 0, 0))
            unchanged.write_bytes(_dat(101, 0, 0))

            import hashlib
            changed_sha = hashlib.sha256(changed.read_bytes()).hexdigest()
            audit = classify(
                geometry_text=_geometry(),
                lineage_text=_lineage(changed_sha),
                map_root=root,
                profile_ids={100},
            )
            import io
            from contextlib import redirect_stdout
            out = io.StringIO()
            with redirect_stdout(out):
                emit(audit)
            text = out.getvalue()
            self.assertIn(
                "RESOLUTION|OUTSIDE_STABLE_WARP_DESTINATIONS_CLASSIFIED",
                text,
            )
            self.assertIn("DESTINATION|floor=100|edge_refs=2", text)
            self.assertNotIn(str(changed.read_bytes()), text)


if __name__ == "__main__":
    unittest.main()
