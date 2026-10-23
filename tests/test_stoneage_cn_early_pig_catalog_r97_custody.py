"""R97 durable acceptance receipt, source-boundary and no-fabricated-artifact guards."""
import copy
import json
import unittest
from tools.stoneage_cn_early_pig_catalog_r97 import ROOT,blob_sha,verify,P

RECEIPT=ROOT/"research/recovered/STONEAGE-CN-EARLY-PIG-CATALOG-ACCEPTANCE-R97.json"
PIN="ff054974e7ea94b163e4951bfe3d1f5000ef586b"

def validate(d):
    raw=RECEIPT.read_bytes()
    assert blob_sha(raw)==PIN, "receipt changed"
    assert d==json.loads(raw.decode("utf-8")), "receipt fields changed"
    assert d["task"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-97"
    assert d["docs_main_commit"]=="6b2b1a89fb3600c33f896d91fcd958e821450317"
    assert d["docs_tree"]=="66ec7bea645c986817981031ee2cedbd3315d046"
    assert d["content_commit"]=="9198b803507e78d05d1f494578b9d4dfb5ce4a5a"
    assert d["candidate_source_ci"]["initial_failed_run"]==39964383907
    assert d["candidate_source_ci"]["initial_failed_job"]==120450316527
    assert d["candidate_source_ci"]["initial_failure_preserved"] is True
    assert d["candidate_source_ci"]["corrected_run"]==39964485685
    assert d["candidate_source_ci"]["corrected_job"]==120450670263
    assert d["candidate_source_ci"]["corrected_test_methods"]==14
    assert d["candidate_source_ci"]["corrected_conclusion"]=="success"
    cand=d["candidate_docs_ci"]["run_ids"];main=d["main_docs_ci"]["run_ids"]
    assert len(cand)==len(set(cand))==9 and len(main)==len(set(main))==11
    assert cand==sorted(cand) and main==sorted(main)
    assert set(cand).isdisjoint(set(main))
    assert d["candidate_docs_ci"]["all_success"] is True and d["main_docs_ci"]["all_success"] is True
    assert d["main_docs_ci"]["dedicated_run"]==39965302676
    assert d["main_docs_ci"]["dedicated_job"]==120453484392
    assert d["source"]["git_blob_sha1"]==blob_sha(P.read_bytes())
    assert d["source"]["original_historical_html_authenticated"] is False
    assert d["source"]["original_sprite_mapping_verified"] is False
    for path,blob in d["source_parent_blobs"].items():
        assert blob_sha((ROOT/path).read_bytes())==blob
    old=[
      ("docs/CURRENT-STATE.md","7394357dbaf17c0fb2ee624bd1bb2022a1bdc738","6a0a1558304a764fff2ea2b9266f81e4525a6ea3"),
      ("docs/HISTORICAL-TIMELINE.md","c981494f0d1bacacfa72a363963946c0085eb19f","81dc3f1778c6e1dc7e86bb298105e0de4bf0808d"),
      ("docs/SOURCE-REGISTRY.md","f55c057b9b78a1badf8b17e78260d110b10502ea","a7b073ae7c730805118e9358d4a2e83646f0a6d8"),
      ("docs/RESTORATION-ROADMAP-R2.md","3a225fce3e86ec4d0402018355b32b97a10ade11","87f9040c84e4a4055e04d806c73eae390aec02a1")
    ]
    for rec,expected in zip(d["historical_prefix"],old):
        assert (rec["path"],rec["prior_blob"],rec["new_blob"])==expected
        assert rec["prefix_verified"] is True
        assert rec["new_chars"]>=rec["prior_chars"]
    assert d["compare"]=={"ahead_by":3,"behind_by":0,"changed_files":9,"deletions":0,"nonforce_fast_forward_main":True}
    a=d["github_actions_artifacts"]
    assert a["candidate_source_corrected_artifact_count"]==0
    assert a["main_source_artifact_count"]==0
    assert all(a[x] is None for x in ("raw_source_zip_sha256","original_historical_html_sha256","original_gif_sha256"))
    q=d["limits"]
    assert q["source_is_web_catalog_not_original_pet_master"] is True
    assert q["named_entries"]==8 and q["unique_detail_names"]==7
    assert q["rows_007_008_name_mismatches"] and q["thumb_links_007_008_swapped"]
    assert q["stage_a_complete"] is False and q["stage_b_started"] is False
    assert q["overall_restoration_percent"] is None
    assert q["next"]=="OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-98"
    assert verify(json.loads(P.read_text(encoding="utf-8")))
    return True

class R97Custody(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=json.loads(RECEIPT.read_text(encoding="utf-8"))
    def test_receipt_and_source_pins(self):
        self.assertTrue(validate(self.base))
    def refuse(self,change):
        d=copy.deepcopy(self.base)
        change(d)
        with self.assertRaises(AssertionError):
            validate(d)
    def test_false_ci_success_and_loss_of_failure(self):
        self.refuse(lambda d:d["candidate_source_ci"].update(initial_failure_preserved=False))
        self.refuse(lambda d:d["candidate_source_ci"].update(corrected_run=39964383907))
    def test_duplicate_and_missing_ci(self):
        self.refuse(lambda d:d["candidate_docs_ci"]["run_ids"].pop())
        self.refuse(lambda d:d["main_docs_ci"]["run_ids"].__setitem__(0,d["main_docs_ci"]["run_ids"][1]))
    def test_wrong_main_and_receipt(self):
        self.refuse(lambda d:d.update(docs_main_commit=d["content_commit"]))
        self.refuse(lambda d:d["compare"].update(nonforce_fast_forward_main=False))
    def test_old_history_not_rewritten(self):
        self.refuse(lambda d:d["historical_prefix"][0].update(prefix_verified=False))
    def test_no_fictitious_original_archive(self):
        self.refuse(lambda d:d["github_actions_artifacts"].update(candidate_source_corrected_artifact_count=1))
        self.refuse(lambda d:d["github_actions_artifacts"].update(original_gif_sha256="deadbeef"))
    def test_no_pet_master_promotion(self):
        self.refuse(lambda d:d["source"].update(original_sprite_mapping_verified=True))
        self.refuse(lambda d:d["limits"].update(stage_a_complete=True))
