import unittest
from pathlib import Path

from tools.stoneage_singleplayer_world import (
    DESIGN_RECONSTRUCTED,
    EARLY_MEMBERSHIP_PROVEN,
    LATER_ONLY_RESOURCE_DEPENDENCY,
    LATER_RECOVERED,
    RESOURCE_RELATION_UNKNOWN,
    STABLE_LATER_MAP_CANDIDATE,
    V1_RESOURCE_COMPATIBLE,
    HistoricalMapDefinition,
    HistoricalWorldTopology,
    WorldMapProvenance,
)
from tools.stoneage_world_map_library import (
    LINEAGE_REPORT_REF,
    parse_stable_later_map_manifest,
)


_SHA_A = "a" * 64
_SHA_B = "b" * 64
_SHA_C = "c" * 64


def small_manifest():
    return f"""StoneAge later field-map lineage comparison — R1
SCOPE|later-corpus-byte-identity+tw1-resource-compatibility|does-not-prove-v1-membership|no-payload-retained
COUNT|shared_paths|3
COUNT|same_path_same_sha256|2
COUNT|same_path_changed_sha256|1
COUNT|same_sha256_and_tw1_compatible_both|2
STABLE_COMPATIBLE|path=100.dat|width=2|height=3|bytes=44|sha256={_SHA_A}|required_ids=4|required_cells=5
STABLE_COMPATIBLE|path=200.dat|width=1|height=1|bytes=14|sha256={_SHA_B}|required_ids=2|required_cells=1
CHANGED|path=300.dat|sha_a={_SHA_A}|sha_b={_SHA_C}|compat_a=1|compat_b=1|size_a=4x5|size_b=4x5
RULE|same-path+same-sha256 across later corpora is strong later-lineage persistence, not proof of Taiwan-v1 membership
RESOLUTION|LATER_FIELDMAP_LINEAGE_CLASSIFIED
"""


class WorldMapProvenanceTests(unittest.TestCase):

    def test_stable_later_candidate_cannot_claim_early_membership(self):
        provenance = WorldMapProvenance(
            content_role=LATER_RECOVERED,
            resource_role=V1_RESOURCE_COMPATIBLE,
            source_versions=("recovered25", "archived2003"),
            evidence_refs=(LINEAGE_REPORT_REF,),
            payload_sha256=_SHA_A,
            qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
        )
        self.assertFalse(provenance.claims_early_membership)

        with self.assertRaisesRegex(ValueError, "must remain LATER_RECOVERED"):
            WorldMapProvenance(
                content_role=EARLY_MEMBERSHIP_PROVEN,
                resource_role=V1_RESOURCE_COMPATIBLE,
                source_versions=("taiwan-v1", "archived2003"),
                evidence_refs=(LINEAGE_REPORT_REF,),
                payload_sha256=_SHA_A,
                qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
            )

    def test_stable_later_candidate_requires_compatible_resources_and_two_versions(self):
        with self.assertRaisesRegex(ValueError, "must be V1_RESOURCE_COMPATIBLE"):
            WorldMapProvenance(
                content_role=LATER_RECOVERED,
                resource_role=LATER_ONLY_RESOURCE_DEPENDENCY,
                source_versions=("recovered25", "archived2003"),
                evidence_refs=(LINEAGE_REPORT_REF,),
                payload_sha256=_SHA_A,
                qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
            )

        with self.assertRaisesRegex(ValueError, "at least two source versions"):
            WorldMapProvenance(
                content_role=LATER_RECOVERED,
                resource_role=V1_RESOURCE_COMPATIBLE,
                source_versions=("recovered25",),
                evidence_refs=(LINEAGE_REPORT_REF,),
                payload_sha256=_SHA_A,
                qualifiers=(STABLE_LATER_MAP_CANDIDATE,),
            )

    def test_design_map_does_not_need_historical_source_version(self):
        provenance = WorldMapProvenance(
            content_role=DESIGN_RECONSTRUCTED,
            resource_role=RESOURCE_RELATION_UNKNOWN,
            evidence_refs=("docs/DESIGN-DECISIONS.md#future-map",),
        )
        self.assertEqual(provenance.source_versions, ())
        self.assertFalse(provenance.claims_early_membership)

    def test_strict_topology_rejects_ambiguous_free_text_only_map(self):
        map_definition = HistoricalMapDefinition(
            floor_id=100,
            width=20,
            height=20,
            evidence="looks old",
        )
        with self.assertRaisesRegex(ValueError, "lacks structured"):
            HistoricalWorldTopology.from_provenance_maps({
                100: map_definition,
            })


class WorldMapLibraryManifestTests(unittest.TestCase):

    def test_parser_builds_strict_later_recovered_topology(self):
        manifest = parse_stable_later_map_manifest(small_manifest())
        self.assertEqual(len(manifest.candidates), 2)
        self.assertEqual(len(manifest.changed), 1)

        topology = manifest.to_topology()
        self.assertTrue(topology.require_structured_provenance)
        self.assertEqual(set(topology.maps), {100, 200})

        provenance = topology.provenance_for_floor(100)
        self.assertIsNotNone(provenance)
        self.assertEqual(provenance.content_role, LATER_RECOVERED)
        self.assertEqual(provenance.resource_role, V1_RESOURCE_COMPATIBLE)
        self.assertEqual(
            provenance.qualifiers,
            (STABLE_LATER_MAP_CANDIDATE,),
        )
        self.assertFalse(provenance.claims_early_membership)

    def test_sample_limited_report_is_rejected(self):
        report = small_manifest().replace(
            f"STABLE_COMPATIBLE|path=200.dat|width=1|height=1|bytes=14|sha256={_SHA_B}|required_ids=2|required_cells=1\n",
            "",
        )
        with self.assertRaisesRegex(ValueError, "detail count"):
            parse_stable_later_map_manifest(report)

    def test_invalid_three_plane_byte_length_is_rejected(self):
        report = small_manifest().replace(
            "path=100.dat|width=2|height=3|bytes=44",
            "path=100.dat|width=2|height=3|bytes=43",
        )
        with self.assertRaisesRegex(ValueError, "three-plane DAT"):
            parse_stable_later_map_manifest(report)

    def test_repository_manifest_is_complete_and_never_promoted_to_v1(self):
        path = Path(LINEAGE_REPORT_REF)
        self.assertTrue(path.is_file())
        manifest = parse_stable_later_map_manifest(
            path.read_text(encoding="utf-8")
        )

        self.assertEqual(manifest.shared_path_count, 995)
        self.assertEqual(manifest.same_sha_count, 980)
        self.assertEqual(manifest.declared_stable_count, 761)
        self.assertEqual(manifest.declared_changed_count, 15)
        self.assertEqual(len(manifest.candidates), 761)
        self.assertEqual(len(manifest.changed), 15)

        topology = manifest.to_topology()
        self.assertEqual(len(topology.maps), 761)
        self.assertTrue(topology.require_structured_provenance)
        self.assertTrue(
            all(
                definition.provenance is not None
                and definition.provenance.content_role == LATER_RECOVERED
                and definition.provenance.resource_role == V1_RESOURCE_COMPATIBLE
                and STABLE_LATER_MAP_CANDIDATE
                    in definition.provenance.qualifiers
                and not definition.provenance.claims_early_membership
                for definition in topology.maps.values()
            )
        )


if __name__ == "__main__":
    unittest.main()
