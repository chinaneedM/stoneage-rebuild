import hashlib
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_versioned_npc_template_profile_probe import (
    analyze,
    emit,
)


def _key(name: str) -> str:
    return hashlib.sha256(name.lower().encode()).hexdigest()


def _binding_report(name: str, variants: int = 1) -> str:
    return (
        "SEMANTIC_SOURCE_VERSION|recovered25\n"
        "EVIDENCE_ROLE|LATER_RECOVERED\n"
        f"TEMPLATE_IDENTITY|key={_key(name)}|variants={variants}|"
        f"variant_fingerprints={variants}|functionset_consensus=TownPeople|"
        f"functionset_variants=1|stable_placements=1\n"
        "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_BINDINGS_CLASSIFIED\n"
    )


class AnonymousNpcTemplateRuntimeProfileProbeTests(unittest.TestCase):

    def test_extracts_nontext_runtime_structure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            npc.mkdir()
            binding = root / "binding.txt"
            binding.write_text(
                _binding_report("SecretTemplate"),
                encoding="utf-8",
            )
            (npc / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=SecretTemplate
name=PRIVATE-DISPLAY-NAME
makeatnobody=1
makeatnosee=0
graphicname=12345
type=SPR_SECRET_TYPE
hp=10,15
mp=7
str=4,2
fly=1
functionset=TownPeople
loopfunc=PRIVATE_CALLBACK
loopfunctime=900
}
""",
                encoding="utf-8",
            )

            profiles, counts = analyze(
                binding_report=binding,
                npc_dir=npc,
            )
            self.assertEqual(len(profiles), 1)
            profile = profiles[0]
            self.assertEqual(profile.template_key, _key("SecretTemplate"))
            self.assertEqual(profile.functionset, "TownPeople")
            self.assertEqual(profile.make_at_nobody, 1)
            self.assertEqual(profile.make_at_no_see, 0)
            self.assertEqual(profile.graphic_resolution, "NUMERIC")
            self.assertEqual(profile.graphic_value, 12345)
            self.assertIsNone(profile.graphic_token_key)
            self.assertEqual(profile.type_resolution, "OPAQUE_SYMBOL")
            self.assertIsNone(profile.type_value)
            self.assertEqual(len(profile.type_token_key), 64)
            self.assertEqual((profile.hp_min, profile.hp_max), (10, 15))
            self.assertEqual((profile.mp_min, profile.mp_max), (7, 7))
            self.assertEqual(
                (profile.strength_min, profile.strength_max),
                (2, 4),
            )
            self.assertEqual(
                (profile.toughness_min, profile.toughness_max),
                (0, 0),
            )
            self.assertEqual(profile.flying, 1)
            self.assertEqual(profile.loop_interval, 900)
            self.assertEqual(profile.direct_override_count, 1)
            self.assertEqual(counts["runtime_profile_variants"], 1)
            self.assertEqual(counts["graphic_resolution:NUMERIC"], 1)
            self.assertEqual(counts["type_resolution:OPAQUE_SYMBOL"], 1)

            out = io.StringIO()
            with redirect_stdout(out):
                emit(profiles, counts)
            text = out.getvalue()
            self.assertNotIn("SecretTemplate", text)
            self.assertNotIn("PRIVATE-DISPLAY-NAME", text)
            self.assertNotIn("PRIVATE_CALLBACK", text)
            self.assertNotIn("SPR_SECRET_TYPE", text)
            self.assertIn("graphic_value=12345", text)
            self.assertIn("type_resolution=OPAQUE_SYMBOL", text)

    def test_missing_graphic_and_type_use_source_defaults(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            npc.mkdir()
            binding = root / "binding.txt"
            binding.write_text(
                _binding_report("SecretTemplate"),
                encoding="utf-8",
            )
            (npc / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=SecretTemplate
functionset=TownPeople
}
""",
                encoding="utf-8",
            )

            profiles, _counts = analyze(
                binding_report=binding,
                npc_dir=npc,
            )
            profile = profiles[0]
            self.assertEqual(profile.graphic_resolution, "DEFAULT_ZERO")
            self.assertIsNone(profile.graphic_value)
            self.assertEqual(
                profile.type_resolution,
                "DEFAULT_SPR_PET001",
            )
            self.assertIsNone(profile.type_value)
            self.assertEqual(profile.loop_interval, -1)

    def test_variant_count_must_match_binding_report(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            npc = root / "npc"
            npc.mkdir()
            binding = root / "binding.txt"
            binding.write_text(
                _binding_report("SecretTemplate", variants=2),
                encoding="utf-8",
            )
            (npc / "base.template").write_text(
                """NPCTEMPLATE
{
templatename=SecretTemplate
functionset=TownPeople
}
""",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "variant-count drift"):
                analyze(
                    binding_report=binding,
                    npc_dir=npc,
                )


if __name__ == "__main__":
    unittest.main()
