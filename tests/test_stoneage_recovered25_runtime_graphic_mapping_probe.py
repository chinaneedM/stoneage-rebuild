import gzip
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_recovered25_runtime_graphic_mapping_probe import (
    RECOVERED25_ABSENT,
    RECOVERED25_CONFLICT,
    RECOVERED25_V1_MISSING,
    RECOVERED25_V1_RESOURCE,
    analyze,
    parse_runtime_ls2data,
)
from tools.stoneage_symbolic_graphic_resolver_probe import token_key


_TEMPLATE_KEY = "1" * 64
_VARIANT = "2" * 64


def _profile(token: str) -> str:
    return (
        "SEMANTIC_SOURCE_VERSION|recovered25\n"
        "EVIDENCE_ROLE|LATER_RECOVERED\n"
        "TEMPLATE_PROFILE|"
        f"template_key={_TEMPLATE_KEY}|variant={_VARIANT}|functionset=TownPeople|"
        "make_at_nobody=1|make_at_no_see=1|"
        "graphic_resolution=OPAQUE_SYMBOL|graphic_value=|"
        f"graphic_token_key={token_key(token)}|"
        "type_resolution=DEFAULT_SPR_PET001|type_value=|type_token_key=|"
        "hp=0,0|mp=0,0|strength=0,0|toughness=0,0|"
        "flying=0|loop_interval=-1|direct_overrides=0\n"
        "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_RUNTIME_PROFILES_CLASSIFIED\n"
    )


def _bindings() -> str:
    return (
        "SEMANTIC_SOURCE_VERSION|recovered25\n"
        "EVIDENCE_ROLE|LATER_RECOVERED\n"
        "PLACEMENT_TEMPLATE|"
        f"placement=0|floor=100|template_key={_TEMPLATE_KEY}|variants=1|"
        "functionset_consensus=TownPeople|functionset_variants=1|"
        "status=UNIQUE_NAME|classic_warp_geometry=0\n"
        "PLACEMENT_TEMPLATE|"
        f"placement=1|floor=100|template_key={_TEMPLATE_KEY}|variants=1|"
        "functionset_consensus=TownPeople|functionset_variants=1|"
        "status=UNIQUE_NAME|classic_warp_geometry=0\n"
        "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_BINDINGS_CLASSIFIED\n"
    )


def _spr_groups(path: Path, ids):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as out:
        out.write(
            "index\tspr_no\toffset\tanim_count\treserved\t"
            "end_offset\tnext_offset\tsegment_sha256\n"
        )
        for index, value in enumerate(ids):
            out.write(
                f"{index}\t{value}\t0\t1\t0\t1\t1\t{'a'*64}\n"
            )


class RecoveredRuntimeGraphicMappingProbeTests(unittest.TestCase):

    def _fixture(self, *, token="SecretGraphic", v1_ids=(100250,)):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        recovered = root / "recovered"
        recovered.mkdir()
        profile = root / "profile.txt"
        binding = root / "binding.txt"
        spr = root / "spr.tsv.gz"
        profile.write_text(_profile(token), encoding="utf-8")
        binding.write_text(_bindings(), encoding="utf-8")
        _spr_groups(spr, v1_ids)
        return root, recovered, profile, binding, spr

    def test_count_plus_name_value_runtime_file_resolves_anonymous_token(self):
        root, recovered, profile, binding, spr = self._fixture()
        runtime = recovered / "ls2data.dat"
        runtime.write_text(
            "2\nSecretGraphic 100250\nOtherGraphic 100251\n",
            encoding="ascii",
        )

        parsed = parse_runtime_ls2data(runtime)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.declared_count, 2)
        self.assertEqual(
            parsed.mapping[token_key("SecretGraphic")],
            100250,
        )

        files, audits, counts = analyze(
            profile_report=profile,
            binding_report=binding,
            recovered_root=recovered,
            tw10_spr_groups=spr,
        )
        self.assertEqual(len(files), 1)
        self.assertEqual(len(audits), 1)
        row = audits[0]
        self.assertEqual(row.status, RECOVERED25_V1_RESOURCE)
        self.assertEqual(row.runtime_resolved_value, 100250)
        self.assertTrue(row.v1_resource_present)
        self.assertEqual(counts["graphic_placements_total"], 2)
        self.assertEqual(counts["graphic_placements_runtime_resolved"], 2)
        self.assertEqual(
            counts["graphic_placements_v1_resource_compatible"],
            2,
        )

    def test_runtime_mapping_can_resolve_later_even_when_v1_resource_missing(self):
        _root, recovered, profile, binding, spr = self._fixture(
            v1_ids=(100251,)
        )
        (recovered / "ls2data.dat").write_text(
            "1\nSecretGraphic 100250\n",
            encoding="ascii",
        )
        _files, audits, counts = analyze(
            profile_report=profile,
            binding_report=binding,
            recovered_root=recovered,
            tw10_spr_groups=spr,
        )
        self.assertEqual(audits[0].status, RECOVERED25_V1_MISSING)
        self.assertEqual(audits[0].runtime_resolved_value, 100250)
        self.assertEqual(counts["graphic_placements_runtime_resolved"], 2)
        self.assertEqual(
            counts["graphic_placements_v1_resource_compatible"],
            0,
        )

    def test_conflicting_runtime_files_are_not_silently_selected(self):
        _root, recovered, profile, binding, spr = self._fixture(
            v1_ids=(100250, 100251)
        )
        a = recovered / "a"
        b = recovered / "b"
        a.mkdir()
        b.mkdir()
        (a / "ls2data.dat").write_text(
            "1\nSecretGraphic 100250\n",
            encoding="ascii",
        )
        (b / "ls2data.dat").write_text(
            "1\nSecretGraphic 100251\n",
            encoding="ascii",
        )
        files, audits, _counts = analyze(
            profile_report=profile,
            binding_report=binding,
            recovered_root=recovered,
            tw10_spr_groups=spr,
        )
        self.assertEqual(len(files), 2)
        self.assertEqual(audits[0].status, RECOVERED25_CONFLICT)
        self.assertEqual(audits[0].recovered_values, (100250, 100251))
        self.assertIsNone(audits[0].runtime_resolved_value)

    def test_header_stub_named_ls2data_dat_is_ignored(self):
        _root, recovered, profile, binding, spr = self._fixture()
        (recovered / "ls2data.dat").write_text(
            "#ifndef LS2DATA_DAT\n#define LS2DATA_DAT\n",
            encoding="ascii",
        )
        files, audits, counts = analyze(
            profile_report=profile,
            binding_report=binding,
            recovered_root=recovered,
            tw10_spr_groups=spr,
        )
        self.assertEqual(files, ())
        self.assertEqual(audits[0].status, RECOVERED25_ABSENT)
        self.assertEqual(counts["runtime_mapping_files"], 0)

    def test_declared_rows_must_be_parseable(self):
        root, _recovered, _profile, _binding, _spr = self._fixture()
        path = root / "bad.dat"
        path.write_text("2\nOne 100\nBROKEN\n", encoding="ascii")
        self.assertIsNone(parse_runtime_ls2data(path))


if __name__ == "__main__":
    unittest.main()
