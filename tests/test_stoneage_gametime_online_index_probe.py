import unittest

from tools.stoneage_gametime_online_index_probe import extract_records


class GameTimeOnlineIndexProbeTests(unittest.TestCase):
    def test_extracts_stoneage_trial_record(self):
        html = """
        <td class="sfont1"> 스톤에이지 체험판 클라이언트 </td>
        <table title="정식 버전 용량은 260MB정도고 체험판은 240MB입니다.">
        <a href="download.asp?GW_IDX=76&GW_Name=Online">stone_demo.exe</a>
        </table>
        """
        rows=extract_records(html)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["idx"],"76")
        self.assertEqual(rows[0]["filename"],"stone_demo.exe")
        self.assertTrue(rows[0]["stoneage"])

    def test_extracts_manual_update_record(self):
        html = """
        <td class="sfont1"> 스톤에이지 자동 업데이트가 안된다면 이것을... </td>
        <table title="스톤 에이지 수동 업데이트 파일입니다.">
        <a href="download.asp?GW_IDX=34&GW_Name=Online">StoneAge.zip</a>
        </table>
        """
        rows=extract_records(html)
        self.assertEqual(rows[0]["idx"],"34")
        self.assertEqual(rows[0]["filename"],"StoneAge.zip")
        self.assertTrue(rows[0]["stoneage"])

    def test_non_stoneage_record_is_not_promoted(self):
        html = """
        <td class="sfont1"> unrelated online game </td>
        <table title="other client">
        <a href="download.asp?GW_IDX=9&GW_Name=Online">other.exe</a>
        </table>
        """
        rows=extract_records(html)
        self.assertEqual(rows[0]["idx"],"9")
        self.assertFalse(rows[0]["stoneage"])


if __name__=="__main__":
    unittest.main()
