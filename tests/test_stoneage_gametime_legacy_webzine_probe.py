import unittest

from tools.stoneage_gametime_legacy_webzine_probe import plain, row_content_links


class GameTimeLegacyWebzineProbeTests(unittest.TestCase):
    def test_plain_strips_markup(self):
        self.assertEqual(plain("<b>StoneAge</b>   download"), "StoneAge download")

    def test_row_content_link_binds_title_and_num(self):
        html = """
        <tr>
          <td>7</td>
          <td onclick="JavaScript:Go('content.asp?name=&num=9&ref=37&page=4')">
            스톤 에이지 베타 버젼용 클라이언트
          </td>
          <td>7898</td><td>2000-10-11</td>
        </tr>
        """
        rows=row_content_links(
            html,
            "http://www.gametime.co.kr/webzine/online/down/bbs.asp?name=&page=4",
        )
        self.assertEqual(len(rows),1)
        self.assertIn("num=9",rows[0][0])
        self.assertIn("스톤 에이지 베타 버젼용 클라이언트",rows[0][1])


if __name__=="__main__":
    unittest.main()
