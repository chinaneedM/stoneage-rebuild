import errno
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import stoneage_p3_boot as p


class P3BootTests(unittest.TestCase):
    def test_source_backed_resource_flags_and_only_isolated_loopback_endpoint(self):
        self.assertIn('updated',p.LAUNCH_ARGS)
        for name in ('realbin','adrnbin','sprbin','spradrnbin','soundbin','battlebin'):
            self.assertIn(name+':1',p.LAUNCH_ARGS)
        self.assertIn('windowmode',p.LAUNCH_ARGS)
        self.assertEqual([x for x in p.LAUNCH_ARGS if x.startswith('IP:')],['IP:0:127.0.0.1:9'])
    def test_original_inventory_is_complete_without_installers(self):
        rows=p.inventory();self.assertEqual(len(rows),375)
        self.assertEqual(sum(int(r['size']) for r in rows),372529095)
        self.assertEqual({r['category'] for r in rows}&{'installer_support'},set())
        exe=next(r for r in rows if r['path']=='StoneAge/sa_3.exe')
        self.assertEqual(exe['sha256'],'cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a')

    def test_no_unqualified_host_namespace_execution(self):
        with patch.dict(p.os.environ,{},clear=True),self.assertRaises(ValueError):p.network_gate()
        with patch.dict(p.os.environ,{'P3_HOST_NET_NAMESPACE':'same'}),patch.object(p.os,'readlink',return_value='same'),self.assertRaises(ValueError):p.network_gate()

    def test_namespace_network_controls_fail_closed(self):
        cases=[([{'ifname':'lo'},{'ifname':'eth0'}],'','',errno.ENETUNREACH),
               ([{'ifname':'lo'}],'default via 1.2.3.4','',errno.ENETUNREACH),
               ([{'ifname':'lo'}],'','default via fe80::1',errno.ENETUNREACH),
               ([{'ifname':'lo'}],'','',0)]
        for links,route,route6,code in cases:
            with self.subTest(links=links,route=route,route6=route6,code=code),\
                 patch.dict(p.os.environ,{'P3_HOST_NET_NAMESPACE':'host'}),\
                 patch.object(p.os,'readlink',return_value='child'),\
                 patch.object(p.subprocess,'check_output',side_effect=[json.dumps(links),route,route6]),\
                 patch.object(p.socket,'socket') as sock:
                sock.return_value.connect_ex.return_value=code
                with self.assertRaises(ValueError):p.network_gate()

    def test_only_loopback_no_route_and_actual_negative_connect_is_admitted(self):
        with patch.dict(p.os.environ,{'P3_HOST_NET_NAMESPACE':'host'}),\
             patch.object(p.os,'readlink',return_value='child'),\
             patch.object(p.subprocess,'check_output',side_effect=['[{"ifname":"lo"}]','','']),\
             patch.object(p.socket,'socket') as sock:
            sock.return_value.connect_ex.return_value=errno.ENETUNREACH
            d=p.network_gate();self.assertTrue(d['outbound_namespace_isolation_verified'])
            sock.return_value.connect_ex.assert_called_once_with(('192.0.2.1',9))

    def test_proprietary_extraction_rejects_public_repository_and_overwrite(self):
        for path in [p.ROOT,p.ROOT/'research/forbidden-original']:
            with self.subTest(path=path),self.assertRaises(ValueError):p.extract(Path('/missing-disc.bin'),path)
        with tempfile.TemporaryDirectory() as d,self.assertRaises(ValueError):p.extract(Path('/missing-disc.bin'),Path(d))

    def test_frame_inspection_does_not_claim_original_visual_confirmation(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'synthetic.png'
            image=Image.new('RGB',(20,10),(222,0,0))
            image.paste((0,200,80),(10,0,20,10));image.save(path)
            result=p.frame(path)
            self.assertEqual(result['synthetic_control_red_pixels'],100)
            self.assertEqual(result['synthetic_control_green_pixels'],100)
            self.assertTrue(result['nonuniform_pixels'])
            self.assertFalse(result['assistant_viewed_original']);self.assertFalse(result['image_published'])


if __name__=='__main__':unittest.main()
