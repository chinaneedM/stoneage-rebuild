import unittest
from tools.stoneage_hananet_stad_file_mapping_probe import TableParser,relevant_rows

class StadMappingProbeTests(unittest.TestCase):
    def test_row_association(self):
        p=TableParser()
        p.feed('<table><tr><td>정식 버전 260 M</td><td><a href="http://x/down/sa.exe">file</a></td></tr><tr><td>체험 버전 240 M</td><td><a href="http://x/down/sa_demo.exe">file</a></td></tr></table>')
        rows=relevant_rows(p.rows)
        self.assertEqual(len(rows),2)
        self.assertIn("sa.exe", rows[0][2][0][2])
        self.assertIn("sa_demo.exe", rows[1][2][0][2])

if __name__=="__main__": unittest.main()
