import unittest

from tools.stoneage_cnet_payload_probe import closest, id_url


class CnetPayloadProbeTests(unittest.TestCase):
    def test_closest_available(self):
        payload = {"archived_snapshots":{"closest":{
            "available":True,
            "timestamp":"20001211014100",
            "status":"200",
            "url":"http://web.archive.org/x",
        }}}
        self.assertEqual(
            closest(payload),
            {"timestamp":"20001211014100","status":"200","url":"http://web.archive.org/x"},
        )

    def test_closest_missing(self):
        self.assertIsNone(closest({"archived_snapshots":{}}))

    def test_id_url(self):
        self.assertEqual(
            id_url("20001211014100","http://korea.cnet.com/pc/games/online/stoneage.zip"),
            "https://web.archive.org/web/20001211014100id_/http://korea.cnet.com/pc/games/online/stoneage.zip",
        )


if __name__ == "__main__":
    unittest.main()
