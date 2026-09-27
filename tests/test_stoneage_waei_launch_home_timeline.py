import unittest
from tools.stoneage_waei_launch_home_timeline import semantics,target_ref

class T(unittest.TestCase):
    def test_semantics(self):
        a,b,c,d=semantics("石器時代 試玩版 274MB 下載")
        self.assertTrue(a and b and c and d)
    def test_ref(self):
        self.assertTrue(target_ref("href","http://x/download.asp?fileid=9"))

if __name__=="__main__":unittest.main()
