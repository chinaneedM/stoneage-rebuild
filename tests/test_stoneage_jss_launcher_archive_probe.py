import struct, unittest
from tools.stoneage_jss_launcher_archive_probe import ORIGINAL, hashes, pe_sections, replay_url, snapshots

class JssLauncherArchiveProbeTests(unittest.TestCase):
    def test_original(self):
        self.assertEqual(ORIGINAL,"http://www.titan.co.jp/stoneage/stoneage.exe")
    def test_snapshot_dedup(self):
        c=[{"timestamp":"20010501010101","original":ORIGINAL,"statuscode":"200","digest":"ABC"}]
        a=[{"timestamp":"20010501010101","status":"200","url":"x"}]
        rows=snapshots(c,a)
        self.assertEqual(len(rows),1); self.assertEqual(rows[0]["source"],"cdx")
    def test_replay_identity(self):
        u=replay_url({"timestamp":"20010501010101","original":ORIGINAL})
        self.assertIn("20010501010101id_",u); self.assertIn("titan.co.jp/stoneage/stoneage.exe",u)
    def test_hashes(self):
        self.assertEqual(hashes(b"abc")[2],"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    def test_minimal_pe(self):
        data=bytearray(512); data[:2]=b"MZ"; struct.pack_into("<I",data,0x3C,0x80)
        data[0x80:0x84]=b"PE\0\0"; struct.pack_into("<HHI",data,0x84,0x14c,0,946684800); struct.pack_into("<H",data,0x94,0)
        self.assertEqual(pe_sections(bytes(data))["machine"],0x14c)

if __name__=="__main__": unittest.main()
