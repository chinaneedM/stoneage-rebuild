import unittest
from tools.stoneage_sa40_arquivo_probe import items,field
class ArquivoTests(unittest.TestCase):
    def test_generic_items(self):
        o={"response_items":[{"originalURL":"http://x","tstamp":"2003"}]}
        self.assertEqual(len(items(o)),1)
        self.assertEqual(field(items(o)[0],"originalURL"),"http://x")
if __name__=="__main__":unittest.main()
