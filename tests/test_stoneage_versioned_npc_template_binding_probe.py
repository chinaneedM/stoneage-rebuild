import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_versioned_npc_template_binding_probe import (
    analyze,
    emit,
)


_SHA = "a" * 64


def _lineage():
    return f"""StoneAge later field-map lineage comparison — R1
COUNT|shared_paths|1
COUNT|same_path_same_sha256|1
COUNT|same_path_changed_sha256|0
COUNT|same_sha256_and_tw1_compatible_both|1
STABLE_COMPATIBLE|path=100.dat|width=20|height=20|bytes=2408|sha256={_SHA}|required_ids=2|required_cells=2
RULE|same-path+same-sha256 across later corpora is strong later-lineage persistence, not proof of Taiwan-v1 membership
RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED
"""


def _geometry(*, classic_warp=0):
    return (
        "NPC_PLACEMENT|floor=100|placement=0|birth=5,5,5,5|"
        "move=5,5,5,5|dir=4|create_num=1|respawn_time=0|boundary=1|"
        "ignore_invincible=1|resolved_templates=1|"
        f"classic_warp_refs={classic_warp}\n"
    )


def _server_map(path: Path, floor_id=100):
    path.write_bytes(
        b"LS2MAP" + int(floor_id).to_bytes(2, "big")
    )


class AnonymousNpcTemplateBindingProbeTests(unittest.TestCase):

    def _fixture(
        self,
        template_text,
        *,
        template_ref="SecretTemplate",
        classic_warp=0,
    ):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        npc_dir = root / "npc"
        map_dir = root / "map"
        npc_dir.mkdir()
        map_dir.mkdir()
        lineage = root / "lineage.txt"
        geometry = root / "geometry.txt"
        lineage.write_text(_lineage(), encoding="utf-8")
        geometry.write_text(
            _geometry(classic_warp=classic_warp),
            encoding="utf-8",
        )
        (npc_dir / "base.template").write_text(
            "NPCTEMPLATE\n" + template_text,
            encoding="utf-8",
        )
        (npc_dir / "base.create").write_text(
            """NPCCREATE
{
floorid=100
borncenter=5,5,0,0
enemy=%s|PRIVATE-ARGUMENT
}
""" % template_ref,
            encoding="utf-8",
        )
        _server_map(map_dir / "100.map")
        return td, root, npc_dir, map_dir, lineage, geometry

    def test_unique_template_is_bound_by_anonymous_identity(self):
        td, _root, npc_dir, map_dir, lineage, geometry = self._fixture(
            """{
templatename=SecretTemplate
functionset=TownPeople
}
"""
        )
        self.addCleanup(td.cleanup)

        bindings, referenced, counts = analyze(
            lineage_report=lineage,
            geometry_report=geometry,
            npc_dir=npc_dir,
            map_dir=map_dir,
        )
        self.assertEqual(len(bindings), 1)
        binding = bindings[0]
        self.assertEqual(binding.binding_status, "UNIQUE_NAME")
        self.assertEqual(binding.functionsets, ("TownPeople",))
        self.assertEqual(binding.variant_count, 1)
        self.assertEqual(len(binding.template_key), 64)
        self.assertNotIn("SecretTemplate", binding.template_key)
        self.assertEqual(counts["stable_spawn_placements"], 1)
        self.assertEqual(counts["placements_with_duplicate_template_name"], 0)
        self.assertEqual(len(referenced), 1)

        out = io.StringIO()
        with redirect_stdout(out):
            emit(bindings, referenced, counts)
        text = out.getvalue()
        self.assertNotIn("SecretTemplate", text)
        self.assertNotIn("PRIVATE-ARGUMENT", text)
        self.assertIn("functionset_consensus=TownPeople", text)

    def test_duplicate_name_same_functionset_stays_load_order_ambiguous(self):
        td, _root, npc_dir, map_dir, lineage, geometry = self._fixture(
            """{
templatename=SecretTemplate
functionset=Warp
graphicname=1
}
{
templatename=SecretTemplate
functionset=Warp
graphicname=2
}
""",
            classic_warp=1,
        )
        self.addCleanup(td.cleanup)

        bindings, _referenced, counts = analyze(
            lineage_report=lineage,
            geometry_report=geometry,
            npc_dir=npc_dir,
            map_dir=map_dir,
        )
        binding = bindings[0]
        self.assertEqual(
            binding.binding_status,
            "DUPLICATE_NAME_SAME_FUNCTIONSET",
        )
        self.assertEqual(binding.variant_count, 2)
        self.assertEqual(binding.functionsets, ("Warp",))
        self.assertEqual(
            counts["classic_warp_duplicate_template_bindings"],
            1,
        )
        self.assertEqual(
            counts["classic_warp_with_warp_functionset_consensus"],
            1,
        )

    def test_duplicate_name_different_functionsets_marks_behavior_ambiguity(self):
        td, _root, npc_dir, map_dir, lineage, geometry = self._fixture(
            """{
templatename=SecretTemplate
functionset=Warp
}
{
templatename=SecretTemplate
functionset=Healer
}
""",
            classic_warp=1,
        )
        self.addCleanup(td.cleanup)

        bindings, _referenced, counts = analyze(
            lineage_report=lineage,
            geometry_report=geometry,
            npc_dir=npc_dir,
            map_dir=map_dir,
        )
        binding = bindings[0]
        self.assertEqual(
            binding.binding_status,
            "DUPLICATE_NAME_FUNCTIONSET_AMBIGUOUS",
        )
        self.assertEqual(binding.functionset_consensus, "<ambiguous>")
        self.assertEqual(set(binding.functionsets), {"Healer", "Warp"})
        self.assertEqual(
            counts["placements_with_functionset_ambiguity"],
            1,
        )
        self.assertEqual(
            counts["classic_warp_with_ambiguous_warp_functionset"],
            1,
        )

    def test_geometry_floor_drift_is_rejected(self):
        td, root, npc_dir, map_dir, lineage, geometry = self._fixture(
            """{
templatename=SecretTemplate
functionset=TownPeople
}
"""
        )
        self.addCleanup(td.cleanup)
        geometry.write_text(
            _geometry().replace("floor=100", "floor=101", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "floor drift"):
            analyze(
                lineage_report=lineage,
                geometry_report=geometry,
                npc_dir=npc_dir,
                map_dir=map_dir,
            )


if __name__ == "__main__":
    unittest.main()
