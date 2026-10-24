import hashlib
from pathlib import Path
import tempfile
import unittest

from tools.stoneage_wayi85_sixpart_acquisition import (
    STEM, check_metadata, direct_link, assemble, safe_7z_members)


class Wayi85AcquisitionTests(unittest.TestCase):
    def info(self, **extra):
        return {'filename': STEM+'.001', 'size': '12', 'hash': 'a'*64,
                'links': {'normal_download': 'https://www.mediafire.com/file/example'}, **extra}

    def test_exact_carrier_metadata(self):
        self.assertEqual(check_metadata(self.info(), 1)['service_bytes'], 12)

    def test_filename_version_and_part_confusion_rejected(self):
        for name in ('STONEAGE80.exe.001', STEM+'.002', '../'+STEM+'.001'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                check_metadata(self.info(filename=name), 1)

    def test_missing_or_rounded_integrity_fields_rejected(self):
        for extra in ({'size': 0}, {'size': str(400*1024*1024)}, {'hash': ''}, {'hash': 'b'*32}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                check_metadata(self.info(**extra), 1)

    def test_download_host_and_html_escaping(self):
        self.assertEqual(direct_link('<a id="downloadButton" href="https://download1.mediafire.com/a?x=1&amp;y=2">'),
                         'https://download1.mediafire.com/a?x=1&y=2')
        with self.assertRaises(ValueError):
            direct_link('<a id="downloadButton" href="https://unrelated.example/file">')

    def test_assembly_rehashes_parts_and_preserves_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            parts = []
            expected = b''
            for n in range(1, 7):
                content = bytes([n])*n
                expected += content
                name = f'{STEM}.{n:03d}'
                (work/name).write_bytes(content)
                parts.append({'part': n, 'filename': name, 'bytes': n, 'sha256': hashlib.sha256(content).hexdigest()})
            self.assertEqual(assemble(parts, work).read_bytes(), expected)
            with self.assertRaises(ValueError):
                assemble(parts[::-1], work)
            (work/parts[1]['filename']).write_bytes(b'changed')
            with self.assertRaises(ValueError):
                assemble(parts, work)

    def test_safe_7zip_listing(self):
        result = safe_7z_members('Path = /tmp/setup.exe\nType = Nsis\n----------\nPath = data/real_1.bin\nSize = 9\nAttributes = A\n')
        self.assertEqual(result[0]['path'], 'data/real_1.bin')

    def test_listing_traversal_links_and_aliases_rejected(self):
        for text in ('Path = ../out\nSize = 1', 'Path = a\nSize = 1\nSymbolic Link = /etc',
                     'Path = a\nSize = 1\n\nPath = A\nSize = 1'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                safe_7z_members('----------\n'+text)
