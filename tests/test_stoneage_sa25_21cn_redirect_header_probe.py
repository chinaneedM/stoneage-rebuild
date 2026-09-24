import unittest
from tools.stoneage_sa25_21cn_redirect_header_probe import CASES,body_targets,replay_urls

class SA2521CNRedirectHeaderTests(unittest.TestCase):
    def test_cases_pin_record(self):
        self.assertTrue(all("id=20165" in url for _,_,url in CASES))
        self.assertTrue(any("num=0" in url for _,_,url in CASES))
    def test_replay_raw_first(self):
        urls=replay_urls("20030318074019","http://download.21cn.com/downit.php?id=20165&num=0")
        self.assertIn("20030318074019id_",urls[0])
    def test_body_target_extract(self):
        vals=body_targets('<script>location="http://dg.download.21cn.com/file1/game/maoxian/sa25up.zip"</script>')
        self.assertEqual(vals,("http://dg.download.21cn.com/file1/game/maoxian/sa25up.zip",))
if __name__=="__main__": unittest.main()
