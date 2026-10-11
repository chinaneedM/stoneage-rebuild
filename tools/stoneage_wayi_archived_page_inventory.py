"""Offline inventory of archived Wayi HTML; never downloads or executes files.

Record actual replay timestamp, even when Wayback redirects to an earlier/later
snapshot. A webpage hash authenticates only the locally inspected response.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from datetime import datetime
from urllib.parse import urljoin, urlsplit

MAX_BYTES = 131072


def replay_identity(url: str) -> tuple[str, str]:
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.netloc != 'web.archive.org' or parsed.fragment:
        raise ValueError('Expected HTTPS Wayback replay')
    # Query belongs to the nested original URL, not a new archive operation.
    match = re.fullmatch(r'/web/(\d{14})id_/(https?://.+)', parsed.path)
    if not match:
        raise ValueError('Expected timestamped raw HTML replay')
    stamp, original = match.groups()
    datetime.strptime(stamp, '%Y%m%d%H%M%S')
    if parsed.query:
        original += '?' + parsed.query
    origin = urlsplit(original)
    if origin.hostname != 'www.wayi.com.tw' or origin.username or origin.password:
        raise ValueError('Expected original Taiwan Wayi page')
    if origin.port not in (None, 80 if origin.scheme == 'http' else 443):
        raise ValueError('Unexpected original port')
    return stamp, original


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.title.append(text)


def inventory_page(payload: bytes, requested_url: str, final_url: str) -> dict:
    requested_stamp, requested_origin = replay_identity(requested_url)
    actual_stamp, original = replay_identity(final_url)
    # No origin change may be silently attributed to the requested page.
    if original != requested_origin:
        raise ValueError('Replay redirected to a different original page')
    if not payload or len(payload) > MAX_BYTES:
        raise ValueError('HTML response size outside bound')
    if b'<html' not in payload[:4096].lower() or payload.startswith(b'MZ'):
        raise ValueError('Not an HTML page')
    text = payload.decode('big5', errors='strict')
    parser = PageLinks()
    parser.feed(text)
    links = []
    for href in parser.links:
        if href.startswith('#'):
            continue
        link = urljoin(original, href)
        if urlsplit(link).scheme in ('http', 'https', 'ftp') and link not in links:
            links.append(link)
    return {
        'requested_replay_timestamp': requested_stamp,
        'actual_replay_timestamp': actual_stamp,
        'replay_timestamp_changed': actual_stamp != requested_stamp,
        'original_url': original,
        'final_replay_url': final_url,
        'response_bytes': len(payload),
        'page_response_sha256': hashlib.sha256(payload).hexdigest(),
        'title': ''.join(parser.title).strip(),
        'links_not_fetched': links,
        'period_status': '2005_CAPTURE' if actual_stamp.startswith('2005') else 'OUTSIDE_2005_CAPTURE',
        'game_binary_obtained': False,
        'publisher_binary_hash_verified': False,
        'native_pet_runtime_verified': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_html', type=Path)
    parser.add_argument('--requested-url', required=True)
    parser.add_argument('--final-url', required=True)
    args = parser.parse_args()
    with args.local_html.open('rb') as stream:
        payload = stream.read(MAX_BYTES + 1)
    print(json.dumps(inventory_page(payload, args.requested_url, args.final_url), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
