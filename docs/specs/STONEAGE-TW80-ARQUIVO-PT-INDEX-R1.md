# Independent historical index recovery for Taiwan 2005 Waei StoneAge 8.0 — Arquivo.pt R1

**Date:** 2026-10-12. **Status:** metadata-only alternative discovery channel. **No recovered original 2005 Taiwanese installer or official patch.**

## Specific blocked discovery path

The accepted 2005-05-18 period press cites a historical operator event page:

`http://www.wayi.com.tw/stoneage/actives/940329/page_3.html`

The existing bounded Wayback Machine CDX 2005–2007 request returned `TimeoutError` on both tested GitHub runners. This means **network/index request inconclusive**, NOT "the historic file disappeared" or "HTTP 404". The current live Wayi URL displays a modern corporate site and is not a 2005 original page.

## Independent public web archive metadata discovery

Arquivo.pt's maintained public API documents URL-based search with `https://arquivo.pt/textsearch?versionHistory=...` and date-bounded archival versions. References:

- https://github-wiki-see.page/m/arquivo/pwa-technologies/wiki/Arquivo.pt-API — official wiki mirror documenting `versionHistory`, dates, result `response_items` and `tstamp`.
- https://sobre.arquivo.pt/en/help/search-2/ — Portuguese Web Archive states snapshots' dates are *archival crawl dates*, not necessarily publication dates.
- https://sobre.arquivo.pt/wp-content/uploads/ProgrammingHistorian-Arquivopt.pdf — documented API search with original URL and bounded `from` and `to`.
- Prior Wayback CDX query spec remains `docs/specs/STONEAGE-TW80-MAY16-OPERATOR-SOURCE-R1.md`.

The new tool makes **one HTTPS request** solely to `https://arquivo.pt/textsearch` with *exact* historical URL, `from=2005`, `to=2007`, `maxItems=12` and `prettyPrint=false`; download/execute/extract paths are absent. It reads at most 128 KiB, timeout 9 sec and stores structured metadata in a temporary GitHub Actions artifact, never copyrighted original files.

Index parser only admits responses with well-formed `response_items` and exact matching original URL, plausible 14-digit timestamps in the bounded period, and archive-host-only references. Unsupported/malformed/foreign-region/out-of-period results are quarantined as **INDETERMINATE**, not historic original proofs. A positive `digest` is a **web archive index token**, not an EXE SHA-256. Even a valid original URL hit means **index metadata only**, NOT the historic HTML body, archived download link, client contents, or native PET runtime.

Status vocabulary: `INDEX_METADATA_FOUND_PAGE_UNVERIFIED`, `EMPTY_INDEX_NOT_PROOF_OF_ABSENCE`, `INVALID_OR_UNEXPECTED_INDEX_RESPONSE`, `NETWORK_INDETERMINATE`. The exact observed Action outcome must be read from its logs/artifact before claiming anything. Queries of archives that have limited Taiwan crawl coverage may return zero rows; zero rows cannot prove there is no 2005 Wayi source elsewhere.

## Verification and unchanged boundaries

Implementation `tools/stoneage_tw80_arquivo_pt_index_probe.py`; `tests/test_stoneage_tw80_arquivo_pt_index_probe.py` includes 17 positive/negative tests and remote read-only workflow `.github/workflows/validate-stoneage-tw80-arquivo-pt-index.yml`. Existing May16 publisher URL, Wayback CDX, prelaunch June4 physical update-disc, June8 release and 2006 DLER mirror version boundary suites run again.

Still **OPEN**: authenticated original free online Taiwanese Waei 2005 8.0 test/release installer, official upgrade/CD file trees, publisher-trustworthy file digests, PET-equipped original paired compiled client-server, opcode127 original owner/save/unique code runtime and first-era JSS1999/TW1 promotion. Pressure **2486=2465 bounded closed+18 OPEN+3 historical UB** unchanged. No engine transition.

**Highest NEXT:** if Arquivo.pt returns real 2005–2007 page-index metadata, independently authenticate archived original page before hunting explicit official installer/patch payload pointers; if network error or empty index, continue external first-party original file source discovery. Never infer "archived page exists" from a successful GitHub test workflow alone.
