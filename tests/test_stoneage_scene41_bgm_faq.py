import unittest
from tools.stoneage_scene41_bgm_faq import EXPECTED_NAMES, DESCRIPTORS, parse_page, original_names, SOURCE_URL
class Scene41SourceBoundary(unittest.TestCase):
    def test_exact_original_names(self):
        self.assertEqual(set(original_names()),set(EXPECTED_NAMES))
    def example(self, labels=DESCRIPTORS, names=EXPECTED_NAMES, date="2001-06-14", end="在北岛守桥的愿藏很烦"):
        lines=" ".join(n+" "+v for n,v in zip(names,labels))
        txt=f"<html><head><title>石器时代之全问答集</title></head><body>石器时代之全问答集 {date} 作者：未知 我可以更改石器时代的音乐吗？ {lines} {end}</body></html>"
        return (txt+" "*2100).encode("gb18030")
    def test_frozen_source_semantics(self):
        x=parse_page(self.example(),SOURCE_URL)
        self.assertEqual(x["row_count"],11)
        self.assertEqual(x["cross_reference_exact_file_name_count"],11)
        self.assertIs(x["game_sound_event_playback_observed"],False)
        self.assertIs(x["historical_published_bytes_authentic"],False)
        self.assertIs(x["original_taiwan_v1_event_selector_verified"],False)
    def test_bad_event_label_rejected(self):
        vals=list(DESCRIPTORS);vals[7]="抓到宠物"
        with self.assertRaises(AssertionError):parse_page(self.example(labels=vals),SOURCE_URL)
    def test_bad_filename_rejected(self):
        vals=list(EXPECTED_NAMES);vals[7]="sabgm_s2"
        with self.assertRaises(AssertionError):parse_page(self.example(names=vals),SOURCE_URL)
    def test_doubled_filename_rejected(self):
        names=list(EXPECTED_NAMES);names[8]="sabgm_s0"
        with self.assertRaises(AssertionError):parse_page(self.example(names=names),SOURCE_URL)
    def test_bad_date_rejected(self):
        with self.assertRaises(AssertionError):parse_page(self.example(date="2004-09-07"),SOURCE_URL)
    def test_bad_location_rejected(self):
        with self.assertRaises(AssertionError):parse_page(self.example(),"https://example.com/stoneage")
    def test_encoding_break_inside_section_rejected(self):
        b=self.example();needle="魔王战斗音乐".encode("gb18030");p=b.index(needle)
        b=b[:p]+b"\\xff"+b[p:]
        with self.assertRaises(AssertionError):parse_page(b,SOURCE_URL)
if __name__=="__main__": unittest.main()
