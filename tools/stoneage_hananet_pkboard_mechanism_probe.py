#!/usr/bin/env python3
"""Recover sparse Hananet pkboard/STAD board-mechanism metadata.

The preserved STAD list page is fetched transiently, along with referenced script
assets when replayable. Only relevant script/form/link snippets are emitted.
"""

from __future__ import annotations

import hashlib
import html.parser
import re
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0"
TS = "20010814230641"
PAGE = "http://www.hananet.net/cgi-bin/pkboard.cgi?k1=GAM2:STAD"

INTEREST = re.compile(
    r"(?i)(pkboard|download|attach|attachment|file|save|down|cgi-bin|"
    r"8119|8120|GAM2:STAD|k1=|k2=|첨부|파일|다운)"
)
URL_RE = re.compile(r"(?i)(?:https?|ftp)://[^\s\"'<>]+")
CGI_RE = re.compile(r"(?i)[a-z0-9_./-]+\.cgi(?:\?[^\s\"'<>]*)?")
FUNC_RE = re.compile(r"(?is)(?:function\s+[a-zA-Z0-9_$]+\s*\([^)]*\)\s*\{.{0,1600}?\})")


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs = []
        self.scripts = []
        self._in_script = False
        self._script_parts = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        amap = dict(attrs)
        for name, value in attrs:
            if value and name.lower() in ("href", "src", "action", "onclick", "onload", "value"):
                self.attrs.append((tag, name.lower(), value))
        if tag == "script":
            if amap.get("src"):
                self.scripts.append(("external", amap["src"]))
            self._in_script = True
            self._script_parts = []

    def handle_data(self, data):
        if self._in_script:
            self._script_parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self._in_script:
            body = "".join(self._script_parts).strip()
            if body:
                self.scripts.append(("inline", body))
            self._in_script = False
            self._script_parts = []


def request(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), str(getattr(r, "url", url)), str(getattr(r, "status", ""))


def replay(ts, url):
    return f"https://web.archive.org/web/{ts}id_/{url}"


def decode(data):
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", "replace")


def safe(v, limit=900):
    v = " ".join(str(v).split())
    return "".join(ch for ch in v if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def relevant_snippets(text):
    out = set()
    for line in text.splitlines():
        line = safe(line, 500)
        if line and INTEREST.search(line):
            out.add(line)
    for m in FUNC_RE.finditer(text):
        value = safe(m.group(0), 900)
        if INTEREST.search(value):
            out.add(value)
    for m in CGI_RE.finditer(text):
        out.add(safe(m.group(0), 700))
    for m in URL_RE.finditer(text):
        value = safe(m.group(0), 700)
        if INTEREST.search(value):
            out.add(value)
    return sorted(out)


def main():
    print("StoneAge Hananet pkboard mechanism probe — R1")
    print("SCOPE|transient-html-and-script-assets|sparse-mechanism-metadata-only|no-client-binary-download")

    body, resolved, status = request(replay(TS, PAGE))
    text = decode(body)
    p = Parser()
    p.feed(text)

    print(
        f"PAGE|timestamp={TS}|status={safe(status)}|bytes={len(body)}|"
        f"sha256={hashlib.sha256(body).hexdigest()}|resolved={safe(resolved)}"
    )

    attrs = set()
    for tag, attr, value in p.attrs:
        absolute = urllib.parse.urljoin(PAGE, value) if not value.lower().startswith("javascript:") else value
        if INTEREST.search(value) or attr in ("action", "onclick"):
            attrs.add((tag, attr, absolute))

    print(f"COUNT|relevant_page_attrs|{len(attrs)}")
    for tag, attr, value in sorted(attrs):
        print(f"ATTR|tag={safe(tag)}|attr={safe(attr)}|value={safe(value,900)}")

    snippets = relevant_snippets(text)
    print(f"COUNT|page_snippets|{len(snippets)}")
    for value in snippets:
        print(f"SNIPPET|source=page|value={safe(value,900)}")

    external = []
    seen = set()
    for kind, value in p.scripts:
        if kind != "external":
            continue
        url = urllib.parse.urljoin(PAGE, value)
        if url in seen:
            continue
        seen.add(url)
        external.append(url)

    print(f"COUNT|external_scripts|{len(external)}")
    fetched = 0
    for url in external:
        try:
            data, script_resolved, script_status = request(replay(TS, url))
        except Exception as exc:
            print(f"SCRIPT_ERROR|url={safe(url)}|kind={type(exc).__name__}|message={safe(exc)}")
            continue
        fetched += 1
        script_text = decode(data)
        print(
            f"SCRIPT|url={safe(url)}|status={safe(script_status)}|bytes={len(data)}|"
            f"sha256={hashlib.sha256(data).hexdigest()}|resolved={safe(script_resolved)}"
        )
        for value in relevant_snippets(script_text):
            print(f"SNIPPET|source={safe(url)}|value={safe(value,900)}")

    print(f"COUNT|external_scripts_fetched|{fetched}")


if __name__ == "__main__":
    main()
