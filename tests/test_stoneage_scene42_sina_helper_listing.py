"""No server execution, release date or program feature promotions from old media links."""
import unittest
from tools.stoneage_scene42_sina_helper_listing import parse,NAMES,URL,old_version_check

def fixture(names=NAMES, extra="<p>[4月 6日] D组第3场</p>", hide=""):
    rows="".join(f"<tr><td>{n}</td><td><a href='ftp://example.test/{i}.zip'><img src='btn.gif'></a></td></tr>" for i,n in enumerate(names))
    return ("<html><body><h1>石器时代ONLINE宠物进化史相关下载</h1>"
      "<div>作者： 新浪游戏 2003-04-03 15:38</div>"
      "<div>石器时代外挂下载</div>"+hide+
      "<table><tr><td>程序名</td><td>本地下载</td></tr>"+rows+"</table>"+extra+
      "</body></html>"+" "*3400).encode("gb18030")

class Scene42(unittest.TestCase):
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
