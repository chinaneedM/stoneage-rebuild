import unittest
from tools.stoneage_hananet_pds_topology_probe import Parser, normalize

class HananetPdsTopologyProbeTests(unittest.TestCase):
    def test_parser(self):
        p=Parser(); p.feed('<frameset><frame src="left.html"><form action="/search.cgi"><input name="q" value="x"></form>')
        self.assertIn(("frame","src","left.html"),p.refs)
        self.assertIn(("form","action","/search.cgi"),p.refs)
        self.assertEqual(p.inputs[0][1],"q")
    def test_normalize(self):
        self.assertEqual(normalize("http://pds.hananet.net/index2.html","left.html"),"http://pds.hananet.net/left.html")

if __name__=="__main__":unittest.main()
