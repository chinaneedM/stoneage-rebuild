"""Audit bounded original-client named-entity provenance; no proprietary bytes."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/recovered/STONEAGE-CLIENT-NAMED-ENTITY-PRIMARY-SOURCE-GAP-R1.json"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0".replace(b"\\0", b"\x00") + data).hexdigest()

def verify(obj=None):
    d = json.loads(REPORT.read_text(encoding="utf-8")) if obj is None else obj
    assert d["schema"] == "stoneage.client_named_entity_primary_source_gap.r1"
    assert d["task"] == "CLIENT-ARTIFACT-NAMED-ENTITY-PROVENANCE-01"
    assert len(d["source_pins"]) == 8
    pinned = {}
    for s in d["source_pins"]:
        name = s["path"]
        assert name not in pinned and name.startswith(("research/", "docs/"))
        data = (ROOT/name).read_bytes()
        assert git_blob_sha(data) == s["git_blob_sha"], name
        pinned[name] = data
    def report(p):
        return json.loads(pinned[p].decode("utf-8"))
    direct = report("research/recovered/STONEAGE-TW10-CN50-DIRECT-STATIC-VISUAL-P2B-R1.json")
    native = report("research/recovered/STONEAGE-TW10-WRITER-SOURCE-CLOSURE-P2B-R1.json")
    publication = report("research/recovered/STONEAGE-TW10-WRITER-SOURCE-PUBLICATION-P2B-R1.json")
    screenshot = report("research/recovered/STONEAGE-JSS2001-INTRO-SCREENSHOT-SOURCES-R1.json")
    facts = d["result"]
    recs = direct["records"]
    assert len(recs) == facts["tw10_cn50_same_original_physical_bitmap_candidates"] == 101
    assert direct["counts"]["direct_original_id_matches"] == 101
    for field, key in [
        ("original_npc_name", "tw10_same_build_authenticated_npc_names"),
        ("original_npc_id", "tw10_same_build_authenticated_npc_ids"),
        ("original_pet_species_id", "tw10_same_build_authenticated_pet_species_ids")]:
        assert sum(x[field] is not None for x in recs) == facts[key] == 0
    assert native["counts"]["candidate_native_writes"] == facts["tw10_writer_candidate_sites"] == 10
    assert facts["tw10_writer_source_classes"] == {
        "stack": native["counts"]["stack_sources"],
        "memory": native["counts"]["other_memory_sources"],
        "arithmetic": native["counts"]["arithmetic_sources"],
    } == {"stack": 7, "memory": 2, "arithmetic": 1}
    assert facts["native_packet_to_selector_object_proven"] is publication["result"]["packet_to_original_object_proven"] is False
    assert facts["jss2001_archive_qualified_intro_screenshots"] == screenshot["qualified_screenshot_count"] == 10
    assert facts["jss2001_or_tw10_same_build_proven"] is screenshot["boundaries"]["jss1999_or_tw10_same_build_proven"] is False
    assert "http://stoneage.hananet.net/down/sa.exe" in pinned["research/clients/STONEAGE-KOREA-2000-PUBLIC-DISTRIBUTION-RECOVERY-R1.md"].decode("utf-8")
    assert "sha256=6795d9349168f77aa025d7c4ea05d005c5bbfe33dd4b227eb7731802fa7eb82b" in pinned["research/recovered/STONEAGE-JSS-LAUNCHER-DEEP-PROBE-R1.txt"].decode("utf-8")
    assert "unique_available_snapshots|0" in pinned["research/recovered/STONEAGE-CNET-KOREA-PAYLOAD-PROBE-R1.txt"].decode("utf-8")
    assert facts["confirmed_original_named_entity_to_bitmap_or_animation_id_pairs"] == 0
    assert facts["new_official_installers_acquired_in_this_audit"] == 0
    assert facts["korea_2000_complete_installer_acquired_by_evidence_sources"] is False
    assert facts["historical_original_client_bytes_committed"] is False
    assert facts["overall_restoration_percent"] is None
    assert d["domain_disposition"] == "SOURCE_GAP_RECORDED_STOP_P2B_NATIVE_WRITER_EXPANSION"
    assert d["next"] == "EARLY-OFFICIAL-CLIENT-ORIGINAL-PAYLOAD-QUALIFICATION-02"
    assert len(d["exact_missing_evidence"]) == 3
    assert len(d["named_original_client_acquisition_leads"]) == 4
    assert all(x["downloaded_and_hashed"] is False for x in d["named_original_client_acquisition_leads"])
    assert len(d["rejected_joins"]) == 6
    assert d["project_boundaries"]["stage_a"] == "7 PARTIAL + 2 OPEN"
    assert d["project_boundaries"]["stage_b"] == "GATED"
    return True

if __name__ == "__main__":
    verify()
    print("PRIMARY SOURCE GAP R1 PASS: 101 physical IDs, 0 named-original joins; package bytes OPEN.")
