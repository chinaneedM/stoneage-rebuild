import unittest
from tools.stoneage_sa25_21cn_downit20165_probe import ID, NoRedirect, candidate_refs

class T(unittest.TestCase):
    def test_id(self):
        self.assertEqual(ID,"20165")
    def test_refs(self):
        s='<meta content="0;URL=http://download.21cn.com/file1/game/maoxian/sa25up.zip"><script>window.location="http://202.104.32.168/file/game/maoxian/sa25up.zip"</script>'
        r=candidate_refs(s)
        self.assertTrue(any("file1/game/maoxian/sa25up.zip" in x for x in r))
        self.assertTrue(any("202.104.32.168/file/game/maoxian/sa25up.zip" in x for x in r))
    def test_no_redirect(self):
        h=NoRedirect()
        self.assertIsNone(h.redirect_request(None,None,302,"Found",{},"http://example.com/"))
if __name__=="__main__":
    unittest.main()
