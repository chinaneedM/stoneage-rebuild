import unittest

from tools.stoneage_sa25_baidu_share_metadata_probe import (
    SIZE_RE,
    classify,
    extract_ints,
    extract_names,
)


class BaiduShareProbeTests(unittest.TestCase):
    def test_extract_names_and_sizes(self):
        text = r'''
        {"server_filename":"StoneAge2.5.rar","size":"553320338","fs_id":"123"}
        {"path":"\/apps\/SA2.5","size":42}
        '''
        self.assertEqual(
            extract_names(text),
            ("StoneAge2.5.rar", "/apps/SA2.5"),
        )
        self.assertEqual(extract_ints(SIZE_RE, text), (553320338, 42))

    def test_needs_code_without_names(self):
        self.assertEqual(classify("请输入提取码", ()), "NEEDS_CODE")

    def test_metadata_beats_code_phrase_when_names_present(self):
        text = '请输入提取码 {"server_filename":"SA25.rar"}'
        names = extract_names(text)
        self.assertEqual(names, ("SA25.rar",))
        self.assertEqual(classify(text, names), "PUBLIC_METADATA_EXPOSED")

    def test_missing_share(self):
        self.assertEqual(classify("啊哦，你来晚了，分享的文件已经被取消", ()), "MISSING")

    def test_link_not_found(self):
        self.assertEqual(classify("百度网盘-链接不存在", ()), "MISSING")

    def test_expired_precedes_code_noise(self):
        self.assertEqual(classify("分享链接已过期 提取码", ()), "EXPIRED")


if __name__ == "__main__":
    unittest.main()
