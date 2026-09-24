import hashlib, unittest
from tools.stoneage_sa25_old_disc_torrent_probe import bdecode,root_info_span,torrent_paths,interesting,relevant_paths

class TorrentProbeTests(unittest.TestCase):
    def test_bdecode_and_info_span(self):
        raw=b"d4:infod4:name12:2001C226.isoee"
        obj,end=bdecode(raw)
        self.assertEqual(end,len(raw))
        s,e=root_info_span(raw)
        self.assertEqual(hashlib.sha1(raw[s:e]).hexdigest(),hashlib.sha1(b"d4:name12:2001C226.isoe").hexdigest())

    def test_strong_path(self):
        meta={b"info":{b"name":"2001 NEW GAME 093".encode()}}
        strong,weak=interesting(torrent_paths(meta),b"")
        self.assertIn("2001 NEW GAME 093",strong)

    def test_generic_issue_280_is_not_target(self):
        meta={b"info":{b"name":"读者 2002年第11期（总第280期）".encode()}}
        strong,weak=interesting(torrent_paths(meta),b"")
        self.assertFalse(strong)

    def test_relevant_paths_excludes_unrelated_issue_280(self):
        paths=(
            "读者30年/2002年第11期（总第280期）.epub.jpg",
            "藏经阁/2001 NEW GAME 093（总第280期）2CD/disc.iso",
        )
        strong,weak=interesting(paths,b"")
        selected=relevant_paths(paths,strong,weak)
        self.assertEqual(selected,(paths[1],))

    def test_contextual_issue_280_requires_catalog_token(self):
        meta={b"info":{b"files":[
            {b"path":["藏经阁".encode(),"2001 NEW GAME 093（总第280期）2CD".encode()]}
        ]}}
        strong,weak=interesting(torrent_paths(meta),b"")
        self.assertTrue(any("总第280期" in x for x in strong))

if __name__=="__main__":
    unittest.main()
