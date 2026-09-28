import gzip
import hashlib
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_versioned_npc_symbol_resolver_probe import (
    analyze,
    emit,
)


def _sha(value: str) -> str:
    return hashlib.sha256(value.lower().encode()).hexdigest()


def _write_spr_groups(path: Path, ids):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as out:
        out.write("index\tspr_no\toffset\n")
        for index, value in enumerate(ids):
            out.write(f"{index}\t{value}\t0\n")


class AnonymousNpcSymbolResolverProbeTests(unittest.TestCase):

    def _fixture(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        npc = root / "npc"
        npc.mkdir()

        template_key = _sha("SecretTemplate")
        binding = root / "bindings.txt"
        binding.write_text(
            "SEMANTIC_SOURCE_VERSION|recovered25\n"
            "EVIDENCE_ROLE|LATER_RECOVERED\n"
            f"TEMPLATE_IDENTITY|key={template_key}|variants=1|"
            "variant_fingerprints=1|functionset_consensus=TownPeople|"
            "functionset_variants=1|stable_placements=1\n"
            "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_BINDINGS_CLASSIFIED\n",
            encoding="utf-8",
        )

        graphic_key = _sha("SPR_SECRET_GRAPHIC")
        type_key = _sha("SPR_SECRET_TYPE")
        profile = root / "profiles.txt"
        profile.write_text(
            "SEMANTIC_SOURCE_VERSION|recovered25\n"
            "EVIDENCE_ROLE|LATER_RECOVERED\n"
            f"TEMPLATE_PROFILE|template_key={template_key}|variant={'a'*64}|"
            "functionset=TownPeople|make_at_nobody=1|make_at_no_see=1|"
            "graphic_resolution=OPAQUE_SYMBOL|graphic_value=|"
            f"graphic_token_key={graphic_key}|"
            "type_resolution=OPAQUE_SYMBOL|type_value=|"
            f"type_token_key={type_key}|hp=0,0|mp=0,0|strength=0,0|"
            "toughness=0,0|flying=0|loop_interval=-1|direct_overrides=0\n"
            "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_RUNTIME_PROFILES_CLASSIFIED\n",
            encoding="utf-8",
        )

        (npc / "base.template").write_text(
            """NPCTEMPLATE
{
templatename=SecretTemplate
graphicname=SPR_SECRET_GRAPHIC
type=SPR_SECRET_TYPE
functionset=TownPeople
}
""",
            encoding="utf-8",
        )

        paths = {}
        for name in ("gavin", "iris", "bismarck"):
            path = root / f"{name}.h"
            path.write_text(
                "#define SPR_SECRET_GRAPHIC 1001\n"
                "#define SPR_SECRET_TYPE 1002\n"
                "#define SPR_pet001 100250\n",
                encoding="utf-8",
            )
            paths[name] = path
        spr = root / "spr.tsv.gz"
        _write_spr_groups(spr, (1001, 1002, 100250))
        return td, root, npc, binding, profile, paths, spr

    def test_three_way_consensus_plus_v1_membership_is_bridge_eligible(self):
        td, _root, npc, binding, profile, paths, spr = self._fixture()
        self.addCleanup(td.cleanup)

        rows, counts = analyze(
            binding_report=binding,
            profile_report=profile,
            npc_dir=npc,
            gavin_anim=paths["gavin"],
            iris_anim=paths["iris"],
            bismarck_anim=paths["bismarck"],
            tw1_spr_groups=spr,
        )

        self.assertEqual(len(rows), 3)
        self.assertEqual(counts["opaque_graphic_tokens"], 1)
        self.assertEqual(counts["opaque_type_tokens"], 1)
        self.assertEqual(counts["default_type_tokens"], 1)
        self.assertEqual(counts["tokens_with_tw1_resource_bridge"], 3)
        self.assertTrue(all(row["bridge_eligible"] for row in rows))
        self.assertTrue(
            all(
                row["classification"] == "FIXED_THREE_WAY_CONSENSUS"
                for row in rows
            )
        )

        out = io.StringIO()
        with redirect_stdout(out):
            emit(rows, counts)
        text = out.getvalue()
        self.assertNotIn("SPR_SECRET_GRAPHIC", text)
        self.assertNotIn("SPR_SECRET_TYPE", text)
        self.assertNotIn("SPR_pet001", text)
        self.assertIn(f"key={_sha('SPR_SECRET_GRAPHIC')}", text)

    def test_divergent_fixed_mapping_is_not_promoted(self):
        td, root, npc, binding, profile, paths, spr = self._fixture()
        self.addCleanup(td.cleanup)
        paths["bismarck"].write_text(
            "#define SPR_SECRET_GRAPHIC 9999\n"
            "#define SPR_SECRET_TYPE 1002\n"
            "#define SPR_pet001 100250\n",
            encoding="utf-8",
        )

        rows, _counts = analyze(
            binding_report=binding,
            profile_report=profile,
            npc_dir=npc,
            gavin_anim=paths["gavin"],
            iris_anim=paths["iris"],
            bismarck_anim=paths["bismarck"],
            tw1_spr_groups=spr,
        )
        graphic = next(
            row for row in rows
            if "graphic" in row["roles"]
        )
        self.assertEqual(
            graphic["classification"],
            "UNRESOLVED_OR_DIVERGENT",
        )
        self.assertIsNone(graphic["bridge_value"])
        self.assertFalse(graphic["bridge_eligible"])

    def test_recovered_direct_mapping_has_priority_but_still_requires_v1_resource(self):
        td, root, npc, binding, profile, paths, spr = self._fixture()
        self.addCleanup(td.cleanup)
        recovered = root / "recovered.h"
        recovered.write_text(
            "#define SPR_SECRET_GRAPHIC 1234\n"
            "#define SPR_SECRET_TYPE 1002\n"
            "#define SPR_pet001 100250\n",
            encoding="utf-8",
        )

        rows, _counts = analyze(
            binding_report=binding,
            profile_report=profile,
            npc_dir=npc,
            gavin_anim=paths["gavin"],
            iris_anim=paths["iris"],
            bismarck_anim=paths["bismarck"],
            tw1_spr_groups=spr,
            recovered_anim=recovered,
        )
        graphic = next(
            row for row in rows
            if "graphic" in row["roles"]
        )
        self.assertEqual(graphic["classification"], "RECOVERED25_DIRECT")
        self.assertEqual(graphic["bridge_value"], 1234)
        self.assertFalse(graphic["tw1_spr_present"])
        self.assertFalse(graphic["bridge_eligible"])

    def test_profile_hash_mismatch_is_rejected(self):
        td, _root, npc, binding, profile, paths, spr = self._fixture()
        self.addCleanup(td.cleanup)
        text = profile.read_text(encoding="utf-8").replace(
            _sha("SPR_SECRET_GRAPHIC"),
            "f" * 64,
            1,
        )
        profile.write_text(text, encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "graphic symbol tokens"):
            analyze(
                binding_report=binding,
                profile_report=profile,
                npc_dir=npc,
                gavin_anim=paths["gavin"],
                iris_anim=paths["iris"],
                bismarck_anim=paths["bismarck"],
                tw1_spr_groups=spr,
            )


if __name__ == "__main__":
    unittest.main()
