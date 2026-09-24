import hashlib, unittest
from tools.stoneage_sa25_old_disc_torrent_probe import bdecode,root_info_span,torrent_paths,interesting

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
        self.assertIn("NEW GAME 093",strong)

    def test_weak_only(self):
        meta={b"info":{b"name":b"collection 280"}}
        strong,weak=interesting(torrent_paths(meta),b"")
        self.assertFalse(strong)
        self.assertIn("280",weak)

if __name__=="__main__":
    unittest.main()
