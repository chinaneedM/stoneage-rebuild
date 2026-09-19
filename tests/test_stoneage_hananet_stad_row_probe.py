import unittest
from tools.stoneage_hananet_stad_row_probe import RowParser, select_rows

class HananetStadRowProbeTests(unittest.TestCase):
    def test_select(self):
        p=RowParser()
        p.feed('<table><tr><td>1</td></tr><tr><td><a href="?k2=8119:1">온라인게임 스톤에이지 정식 버전</a></td><td>2001</td></tr></table>')
        rows=select_rows(p.rows)
        self.assertEqual(len(rows),1)
        self.assertIn("2001",rows[0][0])

if __name__=="__main__":unittest.main()
