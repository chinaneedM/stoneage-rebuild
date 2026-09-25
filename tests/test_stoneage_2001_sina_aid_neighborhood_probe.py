import unittest
from tools.stoneage_2001_sina_aid_neighborhood_probe import rank_neighbors,extract_direct_binary_links

class Sina2001AidNeighborhoodTests(unittest.TestCase):
    def test_rank_neighbors(self):
        rows=[
            {"original":"http://x/download.pl?col=map&aid=43170&filename=a.zip","timestamp":"1"},
            {"original":"http://x/download.pl?col=demo&aid=42000&filename=b.exe","timestamp":"2"},
            {"original":"http://x/download.pl?col=map&filename=noaid.zip","timestamp":"3"},
        ]
        r=rank_neighbors(rows,43172,10)
        self.assertEqual(r[0][1],43170)

    def test_extract_direct_binary(self):
        b=b'<a href="http://202.0.0.1/down/x.zip">x</a><a href="/page.htm">p</a>'
        self.assertEqual(extract_direct_binary_links(b,"http://host/"),("http://202.0.0.1/down/x.zip",))

if __name__=="__main__":
    unittest.main()
