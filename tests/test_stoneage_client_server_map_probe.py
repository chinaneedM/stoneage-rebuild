import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_client_server_map_probe import analyze


def make_server(map_id, width, height, tile, obj, name=b"test"):
    header=b"LS2MAP"+struct.pack(">H",map_id)+name.ljust(32,b"\0")[:32]+struct.pack(">HH",width,height)
    return header+struct.pack(f">{len(tile)}H",*tile)+struct.pack(f">{len(obj)}H",*obj)


class ClientServerMapProbeTests(unittest.TestCase):
    def test_client_map_can_match_server_layer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            client=root/"client"
            server=root/"server"
            client.mkdir(); server.mkdir()
            width,height=3,2
            tile=(1,2,3,4,5,6)
            obj=(9,8,7,6,5,4)
            (client/"100.MAP").write_bytes(struct.pack("<II",width,height)+struct.pack("<6H",*tile))
            (server/"map100").write_bytes(make_server(100,width,height,tile,obj))
            r=analyze(client,server)
            self.assertEqual(r["counts"]["matched_id_count"],1)
            self.assertEqual(r["counts"]["matched_id_and_dimensions"],1)
            self.assertEqual(r["counts"]["ids_with_any_tile_match"],1)
            self.assertEqual(r["counts"]["ids_with_any_obj_match"],0)


if __name__=="__main__":
    unittest.main()
