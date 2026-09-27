#!/usr/bin/env python3
"""Bounded metadata-only crawler for the public old-disc Directory Lister.

Goal: resolve the current StoneAge 2.5 physical-carrier lead around
《中学生电脑》2002年攻略特刊 without downloading optical/game payload bodies.

The crawler reads only directory-listing HTML pages under top-level paths whose
names contain 老光盘群. It records matching directory/file names and hrefs.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import html.parser
import time
import urllib.parse
import urllib.request

BASE = "https://oddownload.nuduseng.com/"
UA = "stoneage-rebuild-archaeology/1.0"
MAX_PAGES = 5000
MAX_LINKS = 300000
MAX_BODY = 2_000_000
TIMEOUT = 15
RETRIES = 1
WORKERS = 16
BATCH = 96

TOKENS = (
    "中学生电脑",
    "课堂内外",
    "攻略特刊",
    "石器时代2.5",
    "石器時代2.5",
    "精灵王传说",
    "精靈王傳說",
    "stoneage2.5",
    "stone age 2.5",
)

OPTICAL_EXTS = (
    ".iso", ".bin", ".cue", ".img", ".mdf", ".mds", ".nrg", ".ccd", ".sub",
)
ARCHIVE_EXTS = (".rar", ".zip", ".7z", ".tar", ".gz", ".exe")
DOC_EXTS = (".pdf", ".txt", ".doc", ".docx", ".chm", ".rtf")


def clean(value, limit=5000):
    text = " ".join(str(value or "").split())
    return text.replace("|", "%7C")[:limit]


def norm(value):
    return "".join(str(value or "").lower().split())


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if href is not None:
            self._href = href
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, "".join(self._text).strip()))
            self._href = None
            self._text = []


def parse_links(body):
    p = LinkParser()
    p.feed(body.decode("utf-8", errors="replace"))
    return tuple(p.links)


def dir_from_href(href):
    parsed = urllib.parse.urlparse(urllib.parse.urljoin(BASE, href))
    query = urllib.parse.parse_qs(parsed.query)
    values = query.get("dir")
    if not values:
        return None
    return values[0].strip("/")


def is_old_disc_root(path):
    return "老光盘群" in urllib.parse.unquote_plus(path or "")


def file_class(name):
    low = str(name or "").lower()
    if low.endswith(OPTICAL_EXTS):
        return "optical"
    if low.endswith(ARCHIVE_EXTS):
        return "archive"
    if low.endswith(DOC_EXTS):
        return "document"
    return "other"


def token_hits(text):
    low = norm(urllib.parse.unquote_plus(text or ""))
    hits = []
    for token in TOKENS:
        if norm(token) in low:
            hits.append(token)
    return tuple(dict.fromkeys(hits))


def page_url(path):
    return BASE if not path else BASE + "?dir=" + urllib.parse.quote(path, safe="/()")


def fetch_page(path):
    url = page_url(path)
    last = None
    for attempt in range(RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                body = response.read(MAX_BODY + 1)
                if len(body) > MAX_BODY:
                    raise ValueError("directory-html-too-large")
                return (
                    path,
                    int(getattr(response, "status", response.getcode())),
                    response.geturl(),
                    body,
                )
        except Exception as exc:
            last = exc
            if attempt < RETRIES:
                time.sleep(0.25 * (attempt + 1))
    raise last


def under_root(candidate, root):
    c = candidate.strip("/")
    r = root.strip("/")
    return c == r or c.startswith(r + "/")


def stoneage_hit(hits):
    return any("石器" in h or "stone" in h.lower() or "精灵" in h or "精靈" in h for h in hits)


def main():
    print("StoneAge 2.5 old-disc Directory Lister carrier-name crawl — R2")
    print("SCOPE|public-directory-html-only|old-disc-roots|metadata-only|no-file-bodies")
    print(
        f"LIMITS|max_pages={MAX_PAGES}|max_links={MAX_LINKS}|max_html_bytes={MAX_BODY}|"
        f"workers={WORKERS}|batch={BATCH}"
    )

    errors = []
    visited = set()
    roots = []

    try:
        _, status, final, body = fetch_page("")
        print(
            f"ROOT|status={status}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|"
            f"final={clean(final)}"
        )
        for href, _text in parse_links(body):
            path = dir_from_href(href)
            if path and is_old_disc_root(path):
                roots.append(path)
        roots = sorted(set(roots))
        print(f"COUNT|old_disc_roots|{len(roots)}")
        for root in roots:
            print(f"ROOT_DIR|value={clean(root)}")
    except Exception as exc:
        print(f"ERROR|scope=root|kind={type(exc).__name__}|message={clean(exc)}")
        print("RESOLUTION|ROOT_FETCH_FAILED|retry directory metadata only")
        return

    frontier = {(root, root) for root in roots}
    pages = 0
    links_seen = 0
    file_links = 0
    dir_links = 0
    matches = []
    exact_middle_school = []
    stoneage_matches = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        while frontier and pages < MAX_PAGES and links_seen < MAX_LINKS:
            available = MAX_PAGES - pages
            batch_rows = sorted(frontier)[: min(BATCH, available)]
            for row in batch_rows:
                frontier.discard(row)

            futures = {pool.submit(fetch_page, path): (path, root) for path, root in batch_rows}
            pages += len(batch_rows)

            for future in concurrent.futures.as_completed(futures):
                path, root = futures[future]
                if path in visited:
                    continue
                visited.add(path)
                try:
                    _path, status, final, body = future.result()
                    if status != 200:
                        errors.append((path, "HTTPStatus", str(status)))
                        continue
                    links = parse_links(body)
                    links_seen += len(links)

                    hits = token_hits(path)
                    if hits:
                        row = ("directory", path, page_url(path), hits, "directory")
                        matches.append(row)
                        if "中学生电脑" in hits:
                            exact_middle_school.append(row)
                        if stoneage_hit(hits):
                            stoneage_matches.append(row)

                    for href, text in links:
                        child = dir_from_href(href)
                        if child:
                            dir_links += 1
                            if child in {"", path} or child in visited:
                                continue
                            if under_root(child, root):
                                frontier.add((child, root))
                            continue

                        absolute = urllib.parse.urljoin(final, href)
                        parsed = urllib.parse.urlparse(absolute)
                        if parsed.scheme not in {"http", "https"}:
                            continue
                        if parsed.netloc != urllib.parse.urlparse(BASE).netloc:
                            continue
                        name = urllib.parse.unquote(parsed.path.rsplit("/", 1)[-1]) or text
                        file_links += 1
                        blob = path + "/" + name
                        hits = token_hits(blob)
                        if not hits:
                            continue
                        row = ("file", blob, absolute, hits, file_class(name))
                        matches.append(row)
                        if "中学生电脑" in hits:
                            exact_middle_school.append(row)
                        if stoneage_hit(hits):
                            stoneage_matches.append(row)
                except Exception as exc:
                    errors.append((path, type(exc).__name__, str(exc)))

            if links_seen >= MAX_LINKS:
                break

    print(f"COUNT|pages_visited|{pages}")
    print(f"COUNT|links_seen|{links_seen}")
    print(f"COUNT|directory_links|{dir_links}")
    print(f"COUNT|file_links|{file_links}")
    print(f"COUNT|matches|{len(matches)}")
    print(f"COUNT|middle_school_computer_matches|{len(exact_middle_school)}")
    print(f"COUNT|stoneage_name_matches|{len(stoneage_matches)}")
    print(f"COUNT|errors|{len(errors)}")
    print(f"COUNT|frontier_remaining|{len(frontier)}")

    for kind, path, target, hits, cls in sorted(matches)[:1500]:
        print(
            f"MATCH|kind={kind}|class={cls}|hits={clean(','.join(hits))}|"
            f"path={clean(path)}|target={clean(target)}"
        )

    for path, kind, message in errors[:250]:
        print(f"ERROR|scope={clean(path)}|kind={clean(kind)}|message={clean(message)}")

    if frontier:
        print("RESOLUTION|CRAWL_LIMIT_REACHED|increase only if new metadata justifies a wider pass")
    elif exact_middle_school:
        optical = [row for row in exact_middle_school if row[4] == "optical"]
        if optical:
            print("RESOLUTION|MIDDLE_SCHOOL_COMPUTER_OPTICAL_NAME_FOUND|inspect exact carrier identity before any payload access")
        else:
            print("RESOLUTION|MIDDLE_SCHOOL_COMPUTER_METADATA_FOUND|no matched optical filename on traversed public listing")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_TARGET_NAME|retry failed directory metadata only")
    else:
        print("RESOLUTION|NO_TARGET_NAME_ON_CURRENT_DIRECTORY_TREE|current public listing has no indexed middle-school-computer carrier name")

    print(
        "EVIDENCE_BOUNDARY|directory/file names identify only public preservation leads; "
        "they do not prove 2002 issue identity, disc contents, clean-client status or byte provenance."
    )


if __name__ == "__main__":
    main()
