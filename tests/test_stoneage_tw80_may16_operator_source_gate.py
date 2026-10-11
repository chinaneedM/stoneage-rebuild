"""Mutation checks separating announced May 16 beta from original binary proof."""
import copy
import json
import unittest
from tools.stoneage_tw80_may16_operator_source_gate import LEDGER,validate

class May16SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(LEDGER.read_text(encoding="utf-8"))
    def reject(self,fn):
        d=copy.deepcopy(self.doc)
        fn(d)
        with self.assertRaises(ValueError):validate(d)
    def test_valid(self):
        self.assertEqual(validate(self.doc),"TW80_MAY16_OPERATOR_SOURCE_BOUNDARY_PASS")
    def test_date_not_june08(self):
        self.reject(lambda d:d["sources"][0].update(observed_date="2005-06-08"))
    def test_forum_not_official_publisher(self):
        self.reject(lambda d:d["sources"][0].update(evidence_kind="PUBLISHER_BINARY"))
    def test_mainland_press_not_taiwan_operator_site(self):
        self.reject(lambda d:d["sources"][2].update(evidence_kind="FIRST_PARTY_TAIWAN_PUBLISHER"))
    def test_no_fake_media_url(self):
        self.reject(lambda d:d.update(historical_operator_link="http://download.wayi.com.tw/STONEAGE80.exe"))
    def test_media_link_source_not_replaced(self):
        self.reject(lambda d:d["sources"][3].update(source=d["sources"][0]["source"]))
    def test_current_webpage_not_2005_original(self):
        self.reject(lambda d:d["claims"].update(web_current_operator_page_is_2005_original=True))
    def test_quoted_link_not_installer(self):
        self.reject(lambda d:d["claims"].update(quoted_wayi_url_is_downloadable_2005_installer=True))
    def test_announced_pet_reward_not_actual(self):
        self.reject(lambda d:d["claims"].update(may16_reward_announced_proves_paid_out_to_users=True))
    def test_test_server_not_client_bytes(self):
        self.reject(lambda d:d["claims"].update(original_may16_test_client_bytes_verified=True))
    def test_not_native_pet_replay(self):
        self.reject(lambda d:d["claims"].update(authenticated_test_server_native_pet_execution_verified=True))
    def test_not_packet127(self):
        self.reject(lambda d:d["claims"].update(may16_publisher_link_proves_8_0_packet127=True))
    def test_no_first_version_projection(self):
        self.reject(lambda d:d["claims"].update(prelaunch_taiwan_feature_can_be_promoted_to_jss1999_or_tw10=True))
    def test_no_fake_publisher_hash(self):
        self.reject(lambda d:d.update(sha256="0"*64))
    def test_cdx_capture_not_automatically_authenticated(self):
        self.reject(lambda d:d["claims"].update(wayback_capture_already_authenticated=True))
    def test_no_unbounded_years(self):
        self.reject(lambda d:d["archive_probe_window"].update(to=2030))
    def test_no_missing_context(self):
        self.reject(lambda d:d["sources"][1].update(content_scope="Test open"))
    def test_no_same_record_dup(self):
        self.reject(lambda d:d["sources"].__setitem__(1,copy.deepcopy(d["sources"][0])))
    def test_no_modified_pressure(self):
        self.reject(lambda d:d["pressure"].update(open=17,bounded_closed=2466))
    def test_no_extra_assertions(self):
        self.reject(lambda d:d["claims"].update(original_hash_pending=True))

if __name__=="__main__":unittest.main()
