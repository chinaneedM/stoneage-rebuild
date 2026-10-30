"""No server execution, release date or program feature promotions from old media links."""
import unittest
import json
from pathlib import Path
from tools.stoneage_scene42_sina_helper_listing import parse,NAMES,URL,old_version_check

def fixture(names=NAMES, extra="<p>[4月 6日] D组第3场</p>", hide=""):
    rows="".join(f"<tr><td>{n}</td><td><a href='ftp://example.test/{i}.zip'><img src='btn.gif'></a></td></tr>" for i,n in enumerate(names))
    return ("<html><body><h1>石器时代ONLINE宠物进化史相关下载</h1>"
      "<div>作者： 新浪游戏 2003-04-03 15:38</div>"
      "<div>石器时代外挂下载</div>"+hide+
      "<table><tr><td>程序名</td><td>本地下载</td></tr>"+rows+"</table>"+extra+
      "</body></html>"+" "*3400).encode("gb18030")

class Scene42(unittest.TestCase):
    def test_frozen_source_and_8_exact_original_hrefs(self):
        from tools.stoneage_scene42_sina_helper_listing import FROZEN
        a=json.loads(FROZEN.read_text(encoding="utf-8"))
        self.assertEqual((a["page_bytes"],a["page_sha256"],a["page_encoding"]),
            (69464,"812b32be4c9e9df45b956826c5a2a566d644ee8ef9acff5cfb69ab962a1b6a1d","gb18030"))
        self.assertEqual([r["archive_listing_label"] for r in a["entries"]],list(NAMES))
        self.assertEqual(sum(len(r["download_links_in_same_table_row"]) for r in a["entries"]),8)
        self.assertEqual(a["entries"][0]["download_links_in_same_table_row"][0],
                         "ftp://211.90.133.5/dowload/sa/sachxp%2B%2B5042.exe")
    def test_frozen_rejects_exact_date_and_binary_upgrades(self):
        from tools.stoneage_scene42_sina_helper_listing import FROZEN
        a=json.loads(FROZEN.read_text(encoding="utf-8"))
        for k in ("sachmx_b8_and_june_b9_are_same_binary_verified",
                  "blue_pet_quiz_tool_task_answers_verified",
                  "original_game_started","source_html_or_program_files_committed"):
            self.assertIs(a[k],False)
        self.assertIs(a["date_label_does_not_establish_exact_contemporary_page_snapshot"],True)
        for r in a["entries"]:
            self.assertIs(r["downloaded_program_build_identity_verified"],False)
            self.assertIs(r["first_release_or_first_seen_date_verified"],False)
    def test_two_historical_mirrors_not_new_sources(self):
        from tools.stoneage_scene42_sina_helper_listing import FROZEN
        a=json.loads(FROZEN.read_text(encoding="utf-8"))
        self.assertIs(a["source_url_previously_in_repo"],True)
        self.assertEqual(a["entry_count"],4)
        self.assertEqual(a["preexisting_source_register_name"],"SRC-CN-2003-SINA-SA-DOWNLOAD-HUB-01")

    def test_old_original_version(self):
        self.assertEqual(old_version_check()["member"],"SACH-MX5.00B9")
    def test_current_illustrative_same_row_labels(self):
        d=parse(fixture())
        self.assertEqual(d["entry_count"],4)
        self.assertEqual(len(d["entries"][0]["download_links_in_same_table_row"]),1)
        self.assertIs(d["sachmx_b8_and_june_b9_are_same_binary_verified"],False)
    def test_order_mismatch(self):
        l=list(NAMES);l[0],l[1]=l[1],l[0]
        with self.assertRaises(ValueError):parse(fixture(names=l))
    def test_missing_tool(self):
        with self.assertRaises(ValueError):parse(fixture(names=NAMES[:3]))
    def test_duplicate_does_not_prove_four_distinct_items(self):
        with self.assertRaises(ValueError):parse(fixture(names=[*NAMES,NAMES[1]]))
    def test_no_april6_does_not_pin_date(self):
        with self.assertRaises(ValueError):parse(fixture(extra=""))
    def test_redirect_rejected(self):
        with self.assertRaises(ValueError):parse(fixture(),URL.replace("games.sina","other.sina"))
    def test_invisible_items_not_in_real_cells(self):
        with self.assertRaises(ValueError):parse(fixture(names=NAMES[:3],hide="<script>小明蓝暴自动猜谜器</script>"))
    def test_empty_source(self):
        with self.assertRaises(ValueError):parse(b"<html/>")
