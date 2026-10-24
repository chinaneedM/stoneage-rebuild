#!/usr/bin/env python3
"""Bounded negative-claim guard for R107 metadata. Not a historical HTML replay."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/recovered/STONEAGE-CN2003-TOURNAMENT-REWARD-R107.json"

def verify(document):
    assert document["schema"] == "stoneage.cn2003.tournament_reward.r107"
    assert document["task"].endswith("-107")
    source = document["source"]
    assert source["url"] == "https://games.sina.com.cn/zhuanqu/sa/gonggao.shtml"
    assert source["provenance_level"] == "PUBLIC_WEB_TEXT_RENDER_ONLY_NO_BYTE_REPLAY"
    assert source["actual_raw_html_sha256"] is None
    assert source["actual_raw_html_bytes"] is None
    assert source["exact_historical_capture"] is None
    assert len(document["records"]) == 4
    items = {r["record_id"].rsplit(":", 1)[-1]: r for r in document["records"]}
    assert set(items) == {"golden-pet-npc","golden-pet-reward","golden-pet-claim","semifinal-selection"}
    for r in document["records"]:
        for k in ("record_id","entity_type","collection","version_profile",
                  "source_refs","verification_status","rights_status","record_revision"):
            assert k in r, (r.get("record_id"), k)
        assert r["game_ids"] is None
        assert r["version_profile"].startswith("LATER_OFFICIAL:CN_WAYI_TOURNAMENT_2003")
        assert r["verification_status"] == "TOURNAMENT_ORGANIZER_CLAIM_IN_MEDIA_PAGE_NOT_RUNTIME"
    npc, reward, claim, semi = (items[x] for x in (
        "golden-pet-npc", "golden-pet-reward", "golden-pet-claim", "semifinal-selection"))
    assert npc["collection"] == "npcs" and npc["name_as_written"] == "华义大财神"
    assert npc["npc_original_id"] is None and npc["coordinates"] is None
    assert reward["collection"] == "pets" and reward["name_as_written"] == "金暴"
    assert reward["reported_reward_quantity"] == 1
    assert reward["pet_species_id"] is None and reward["actual_delivery_verified"] is False
    assert claim["npc_ref"] == npc["record_id"]
    assert claim["reward_ref"] == reward["record_id"]
    assert claim["announced_claim_start"] == "2003-04-11"
    assert claim["real_transaction_observed"] is False and claim["quest_storyline"] is False
    assert claim["eligibility_predicate"] is None
    assert semi["choice_options_as_written"] == ["白虎","魔法兽"]
    assert semi["deadline_conflict"] == "UNRESOLVED_SAME_PAGE_TWO_DIFFERENT_DEADLINES"
    assert {x["parsed_date"] for x in semi["site_deadline_claims"]} == {"2003-04-21","2003-04-22"}
    assert semi["site_deadline_claims"][0]["time_as_written"] == "09:00"
    assert semi["site_deadline_claims"][1]["time_as_written"] is None
    assert semi["qualified_reward_unconditional"] is False
    assert semi["actual_reward_delivery"] is None
    assert document["continuation"]["overall_restoration_percent"] is None
    assert document["continuation"]["savedata_r79"] == "PAUSED_NON_BLOCKING"
    return True

def main():
    verify(json.loads(PATH.read_text(encoding="utf-8")))
    print("R107 bounded tournament metadata: PASS (not raw-source/runtime replay)")

if __name__ == "__main__":
    main()
