import unittest
from pathlib import Path

from tools.stoneage_singleplayer_world import LATER_RECOVERED
from tools.stoneage_versioned_world_manifest import (
    COVERAGE_REPORT_REF,
    build_versioned_world_manifest,
)
from tools.stoneage_versioned_world_names import (
    MAP_NAMES_REPORT_REF,
    bind_versioned_world_names,
    parse_versioned_world_names,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


def _overlay():
    maps = parse_stable_later_map_manifest(
        Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
    )
    world = build_versioned_world_manifest(
        maps=maps,
        coverage_text=Path(COVERAGE_REPORT_REF).read_text(encoding="utf-8"),
    )
    return bind_versioned_world_names(
        world=world,
        names_text=Path(MAP_NAMES_REPORT_REF).read_text(encoding="utf-8"),
    )


class VersionedWorldNamesTests(unittest.TestCase):

    def test_real_name_report_binds_to_server_map_floor_set(self):
        overlay = _overlay()

        self.assertEqual(len(overlay.world.floors), 761)
        self.assertEqual(len(overlay.by_floor), 571)
        self.assertEqual(len(overlay.unresolved_by_floor), 1)
        self.assertEqual(len(overlay.no_name_evidence_floor_ids), 189)
        self.assertEqual(len(overlay.without_resolved_name_floor_ids), 190)
        self.assertEqual(set(overlay.unresolved_by_floor), {31001})

        self.assertTrue(
            all(
                row.evidence_role == LATER_RECOVERED
                for row in overlay.by_floor.values()
            )
        )
        self.assertTrue(
            all(
                row.evidence_role == LATER_RECOVERED
                for row in overlay.unresolved_by_floor.values()
            )
        )

    def test_recovered_text_preserves_uninterpreted_legacy_suffix(self):
        overlay = _overlay()

        self.assertEqual(
            overlay.recovered_text(1001),
            "薩姆吉爾的武器店|0",
        )
        self.assertEqual(
            overlay.recovered_text(10001),
            "阿布的洞窟地下１樓|0",
        )
        self.assertIsNone(overlay.recovered_text(31001))

    def test_conflicting_floor_remains_unresolved(self):
        overlay = _overlay()
        conflict = overlay.unresolved_by_floor[31001]

        self.assertEqual(
            conflict.candidate_texts,
            (
                "加特洛的洞窟１樓|0",
                "加都洛的洞窟１樓|0",
            ),
        )
        self.assertEqual(conflict.status, "SERVER_COPY_TEXT_CONFLICT")
        self.assertEqual(len(conflict.raw_sha256), 2)

    def test_truncated_name_report_is_rejected(self):
        text = Path(MAP_NAMES_REPORT_REF).read_text(encoding="utf-8")
        lines = text.splitlines()
        first_name = next(
            index for index, line in enumerate(lines)
            if line.startswith("MAP_NAME|")
        )
        truncated = "\n".join(
            lines[:first_name] + lines[first_name + 1 :]
        )

        with self.assertRaisesRegex(ValueError, "detail count"):
            parse_versioned_world_names(truncated)

    def test_unknown_floor_cannot_bind_into_world(self):
        maps = parse_stable_later_map_manifest(
            Path(LINEAGE_REPORT_REF).read_text(encoding="utf-8")
        )
        world = build_versioned_world_manifest(
            maps=maps,
            coverage_text=Path(COVERAGE_REPORT_REF).read_text(
                encoding="utf-8"
            ),
        )
        text = Path(MAP_NAMES_REPORT_REF).read_text(encoding="utf-8")
        drifted = text.replace(
            "MAP_NAME|floor=1001|",
            "MAP_NAME|floor=999999|",
            1,
        )

        with self.assertRaisesRegex(ValueError, "unknown floors"):
            bind_versioned_world_names(world=world, names_text=drifted)


if __name__ == "__main__":
    unittest.main()
