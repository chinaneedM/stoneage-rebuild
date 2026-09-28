import gzip
import hashlib
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.stoneage_symbolic_graphic_resolver_probe import (
    CONSENSUS_V1_MISSING,
    PROMOTED,
    SOURCE_CONFLICT,
    SOURCE_INCOMPLETE,
    analyze,
    emit,
    token_key,
)


def _write_gz(path: Path, rows: list[int]):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as handle:
        handle.write(
            "index\tspr_no\toffset\tanim_count\treserved\t"
            "end_offset\tnext_offset\tsegment_sha256\n"
        )
        for index, value in enumerate(rows):
            handle.write(
                f"{index}\t{value}\t0\t1\t0\t1\t1\t{'a'*64}\n"
            )


def _profile(token: str) -> str:
    key = token_key(token)
    return (
        "SEMANTIC_SOURCE_VERSION|recovered25\n"
        "EVIDENCE_ROLE|LATER_RECOVERED\n"
        "TEMPLATE_PROFILE|"
        f"template_key={'1'*64}|variant={'2'*64}|functionset=TownPeople|"
        "make_at_nobody=1|make_at_no_see=1|"
        "graphic_resolution=OPAQUE_SYMBOL|graphic_value=|"
        f"graphic_token_key={key}|"
        "type_resolution=DEFAULT_SPR_PET001|type_value=|type_token_key=|"
        "hp=0,0|mp=0,0|strength=0,0|toughness=0,0|"
        "flying=0|loop_interval=-1|direct_overrides=0\n"
        "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_RUNTIME_PROFILES_CLASSIFIED\n"
    )


def _binding() -> str:
    return (
        "SEMANTIC_SOURCE_VERSION|recovered25\n"
        "EVIDENCE_ROLE|LATER_RECOVERED\n"
        "PLACEMENT_TEMPLATE|"
        f"placement=0|floor=100|template_key={'1'*64}|variants=1|"
        "functionset_consensus=TownPeople|functionset_variants=1|"
        "status=UNIQUE_NAME|classic_warp_geometry=0\n"
        "PLACEMENT_TEMPLATE|"
        f"placement=1|floor=100|template_key={'1'*64}|variants=1|"
        "functionset_consensus=TownPeople|functionset_variants=1|"
        "status=UNIQUE_NAME|classic_warp_geometry=0\n"
        "RESOLUTION|ANONYMOUS_NPC_TEMPLATE_BINDINGS_CLASSIFIED\n"
    )


class SymbolicGraphicResolverProbeTests(unittest.TestCase):

    def _run(self, source_values, *, v1_ids):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        profile = root / "profile.txt"
        binding = root / "binding.txt"
        profile.write_text(_profile("SPR_secret"), encoding="utf-8")
        binding.write_text(_binding(), encoding="utf-8")

        source_paths = []
        for index, value in enumerate(source_values):
            path = root / f"source{index}.h"
            if value is None:
                path.write_text("#define SPR_other 999\n", encoding="utf-8")
            else:
                path.write_text(
                    f"#define SPR_secret {value}\n",
                    encoding="utf-8",
                )
            source_paths.append(path)
        spr = root / "spr.tsv.gz"
        _write_gz(spr, v1_ids)

        audits, counts = analyze(
            profile_report=profile,
            binding_report=binding,
            gavin_anim=source_paths[0],
            iriselia_anim=source_paths[1],
            bismarck_anim=source_paths[2],
            tw10_spr_groups=spr,
        )
        return audits, counts

    def test_three_source_consensus_plus_v1_resource_promotes(self):
        audits, counts = self._run((100250, 100250, 100250), v1_ids=[100250])
        self.assertEqual(len(audits), 1)
        row = audits[0]
        self.assertEqual(row.status, PROMOTED)
        self.assertEqual(row.promoted_value, 100250)
        self.assertTrue(row.v1_resource_present)
        self.assertEqual(counts["graphic_placements_total"], 2)
        self.assertEqual(counts["graphic_placements_promoted"], 2)

        out = io.StringIO()
        with redirect_stdout(out):
            emit(audits, counts)
        text = out.getvalue()
        self.assertNotIn("SPR_secret", text)
        self.assertIn(f"key={token_key('SPR_secret')}", text)
        self.assertIn("consensus=100250", text)

    def test_consensus_without_v1_resource_is_not_promoted(self):
        audits, _counts = self._run(
            (100999, 100999, 100999),
            v1_ids=[100250],
        )
        self.assertEqual(audits[0].status, CONSENSUS_V1_MISSING)
        self.assertIsNone(audits[0].promoted_value)

    def test_source_conflict_is_not_promoted(self):
        audits, _counts = self._run(
            (100250, 100250, 100251),
            v1_ids=[100250, 100251],
        )
        self.assertEqual(audits[0].status, SOURCE_CONFLICT)

    def test_source_incomplete_is_not_promoted(self):
        audits, _counts = self._run(
            (100250, 100250, None),
            v1_ids=[100250],
        )
        self.assertEqual(audits[0].status, SOURCE_INCOMPLETE)

    def test_hex_define_is_supported(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        from tools.stoneage_symbolic_graphic_resolver_probe import parse_anim_tbl

        header = root / "anim.h"
        header.write_text("#define SPR_secret 0x1879A\n", encoding="utf-8")
        mapping = parse_anim_tbl(header)
        self.assertEqual(mapping[token_key("SPR_secret")], 100250)


if __name__ == "__main__":
    unittest.main()
