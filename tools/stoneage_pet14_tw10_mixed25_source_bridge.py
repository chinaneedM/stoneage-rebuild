"""PET14 public source-derived crosswalk. Original commercial files are not needed in CI."""
from collections import defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PET07 = ROOT / "research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json"
PET10 = ROOT / "research/recovered/STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"
REPORT = ROOT / "research/recovered/STONEAGE-PET-MODULE-14-TW10-MIXED25-SOURCE-SEPARATED-NUMERIC-BRIDGE-R1.json"

def derive():
    a = json.loads(PET07.read_text(encoding="utf-8"))
    b = json.loads(PET10.read_text(encoding="utf-8"))
    groups = a["source_groups"]
    if len(groups) != 130 or len(set(g[0] for g in groups)) != 130:
        raise ValueError("original TW1 graphics sample changed")
    keys = set(g[0] for g in groups)
    tables = ("enemybase.txt", "enemybase2.txt")
    indices = {}
    for t in tables:
        rows = b["source_rows"][t]
        if len(rows) != (988 if t == tables[0] else 640):
            raise ValueError("original mixed25 source row conservation")
        d = defaultdict(list)
        for r in rows:
            if len(r) != 17 or r[3] not in (0, 1):
                raise ValueError("original PET10 row/flag layout")
            d[r[2]].append(r)
        indices[t] = d

    def stats(t):
        selected = [r for k in keys for r in indices[t][k]]
        positive = [r for r in selected if r[3] == 1]
        return {
            "source_table_total_rows":len(b["source_rows"][t]),
            "graphic_groups_with_any_source_rows":sum(bool(indices[t][k]) for k in keys),
            "graphic_groups_with_PETFLG_1":len(set(r[2] for r in positive)),
            "PETFLG_1_rows_at_TW10_graphic_keys":len(positive),
            "PETFLG_0_rows_at_TW10_graphic_keys":len(selected)-len(positive),
            "all_source_rows_at_TW10_graphic_keys":len(selected),
            "PETFLG_1_rows_outside_this_TW10_sample":sum(r[3]==1 for r in b["source_rows"][t])-len(positive),
        }
    out = []
    for g in groups:
        entry = {
            "original_TW10_spr_numeric_graphic":g[0],
            "original_TW10_SPR_group_sha256":g[2],
            "TW10_original_pixel_preview":"PREEXISTING_PET07_SOURCE_PIXEL_SAMPLED_SEQUENCES_NOT_NATIVE_GAMEPLAY",
        }
        for table,label in ((tables[0],"mixed25_main"),(tables[1],"mixed25_alternative")):
            rs = indices[table][g[0]]
            entry[label] = {
                "source_template_rows":len(rs),
                "PETFLG_1_rows":sum(r[3]==1 for r in rs),
                "PETFLG_0_rows":sum(r[3]==0 for r in rs),
            }
        out.append(entry)
    report = {
        "schema":"stoneage.pet14_original_tw10_pixel_gallery_mixed25_two_source_table_numeric_crosswalk.r1",
        "date":"2026-11-06",
        "source_git_blobs":{"PET07":"0b5f81b41a642025ab53a12884638fdee887470e","PET10":"25a37aeb134fb180e322e7dc335029b7374452d8"},
        "private_replayed_source_sha256":{
            "PET07_original_pixel_gallery":"58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76",
            "PET10_original_mixed25_CP950_catalog":"640506addf01417390a7078f70aece167c99feecf4beeca8cb769f32972ff5d3",
        },
        "source_scope":{
            "TW10":"ORIGINAL_RETAIL_SPR_ADRN_REAL_PET07_PREEXISTING_PRIVATE_PIXEL_OBSERVATIONS",
            "MIXED25":"LATER_COMMUNITY_PRESERVED_RAR_TWO_DISTINCT_ORIGINAL_PET_TEMPLATE_TABLES_NOT_PROVEN_ACTIVE_TOGETHER",
            "mixed25_archive_sha256":b["preserved_original_rar"]["sha256"],
            "private_media_in_public_git":False,
        },
        "summary":{
            "TW10_source_graphic_groups_in_PET07_sample":len(groups),
            "mixed25_main":stats(tables[0]),"mixed25_alternative":stats(tables[1]),
            "TW10_graphics_without_any_mixed25_alternative_rows":sorted(keys-set(indices[tables[1]])),
            "TW10_graphics_without_mixed25_alternative_PETFLG_1_rows":sorted(k for k in keys if not any(r[3]==1 for r in indices[tables[1]][k])),
            "original_specimens_newly_downloaded":0,"original_pixel_blocks_newly_decoded":0,
        },
        "graphics":out,
        "evidence_boundary":{
            "same_number_proves_same_pet_species":False,
            "same_deployment_or_official_mixed25_proven":False,
            "original_TW10_server_names_stats_or_skills_proven":False,
            "original_capture_success_replayed":False,
            "original_pet_skill_or_growth_runtime_proven":False,
            "PET07_original_pixels_observed_in_earlier_work_not_new_this_run":True,
            "private_CP950_names_present_in_public_report":False,
            "stage_a":"7_PARTIAL_2_OPEN",
            "stage_b_wiki":"GATED","r79":"PAUSED_NON_BLOCKING","overall_percent":None,
        }
    }
    if (report["summary"]["mixed25_main"]["PETFLG_1_rows_at_TW10_graphic_keys"],
        report["summary"]["mixed25_alternative"]["PETFLG_1_rows_at_TW10_graphic_keys"]) != (188,142):
        raise ValueError("original source join changed")
    return report

if __name__ == "__main__":
    print(json.dumps(derive(),ensure_ascii=False,sort_keys=True))
