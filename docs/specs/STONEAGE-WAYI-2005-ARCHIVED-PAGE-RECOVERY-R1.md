# Wayi 2005 official page recovery and download-chain evidence R1

Date: 2026-10-12 (Asia/Shanghai). Source bodies inspected outside Git; only response hashes, URLs, byte counts, link metadata and derived observations retained. Original software not retrieved or certified.

## Retrieved pages and actual replay dates

| Original operator page | Actual capture | What it establishes |
| --- | --- | --- |
| `/stoneage/` | 2005-06-15 02:38:34 | Official home reports all star systems updated to 8.0; advertises deluxe update package containing two discs; supplies client download page link. |
| `/stoneage/actives/940329/page_3.html` | 2005-06-05 00:26:08 | Previously press-linked official five-year event HTML is now actually readable. Its image-sliced content is not interpreted as original PET execution. |
| `/service/download_list1.asp?id=1` | **2005-04-05 18:56:35** | A June/August replay request redirects backward. Page labels full client **7.5**, dated 2004-12-29; separate StoneAge2.exe launcher entry dated 2004-11-26. |
| `/stoneage/producer/producer01.asp` | 2005-06-12 01:14:06 | Operator's own index links March3 PET preview idno109 and May31 8.0 preview idno121. |
| `/stoneage/producer/producer02.asp?idno=109` | **2005-11-30 00:29:44** | Publisher describes seven planned equipment families, species eligibility and proposed quest/synthesis acquisition. June index supplies March3 entry date; November body is not assumed byte-identical to March. |
| `/stoneage/producer/producer02.asp?idno=121` | **2010-07-11 06:02:06** | Out-of-period redirect; cannot establish recovered May31 2005 page body. Retained only as a quarantined lead. |

Exact replay URLs and SHA256 of locally received HTML responses: `research/recovered/STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json`. A response hash is **not** a publisher installer hash. Requested timestamp, actual capture, displayed entry date and software build date remain distinct.

## New concrete official file pointers

The April download page explicitly links `ftp://download.wayi.com.tw/stoneageinstall.exe` for the **7.5** full client and `/download/download.asp?fileid=329` for the separate StoneAge2.exe launcher. This gives a first-party file-chain lead, stronger than a third-party basename. No bytes for either file have been recovered. The FTP CDX lookup returned HTTP503; not a publisher-server 404 or proof of absence. The launcher endpoint CDX returned four **302** records (2004, 2005, 2006, 2009), not executable content. A date-filtered download-page CDX lookup timed out despite a successful raw replay. Earlier May16/CDX timeouts and Arquivo.pt empty results remain valid observations of those earlier requests; they did not prove global absence and are superseded only as to present page accessibility.

## Reproducible offline inspection

`tools/stoneage_wayi_archived_page_inventory.py` reads bounded local Big5 HTML, records the **final** replay timestamp, checks original Wayi Taiwan identity, inventories links without following them and hashes only the page response. It performs no network request, installer download, script execution or extraction. Nine functional controls cover backward/forward snapshot redirects, nested query identity, FTP/relative links, injected script text, malformed replay dates/origins, binary and oversized input. All six real page responses were inspected with this tool.

## Remaining goal

Continue original authenticated **Taiwan 2005 8.0** installer/disc/update identity and exact byte hash recovery. The official 7.5 pointer may be investigated separately as a dated bridge. Neither original 8.0 compiled PET pair, opcode127, owner/save/unique-code lifecycle nor JSS1999/Taiwan1.0 membership is established. `2486 = 2465 bounded closed + 18 OPEN + 3 historical UB` unchanged. No production-engine transition.


### Same-round byte-level follow-through: official updater redirect recovered

Followed the archived November15 2005 fileid329 **302** without reading its body; Location identifies `http://www.wayi.com.tw/download/file/onlineGame/StoneAge2.exe`. Bounded raw replay recovered **113664 bytes**, actual final capture **2006-09-08 11:16:12**, SHA256 `a72a2fa646766f9c3a9a04f4340a3c7a1d76029d0c464bc7613f604a1900820f`. Static file/objdump inspection: PE32 i386 GUI, UPX0/UPX1/.rsrc sections; embedded ProductName SaUpdate, OriginalFilename SaUpdate.EXE, file/product version **1, 0, 0, 5**; COFF header timestamp May18 2005 11:26:56 UTC. No execution or unpacking. This is a real **operator-linked archived updater specimen**, not a recovered full 8.0 client. Archive capture is 2006, PE timestamp/resources are mutable and neither prove first-release version/date nor publisher-original checksum. No PET native execution or pressure change; updater bytes remain outside Git. Earlier same-round statements about unreceived launcher bytes are superseded by this bounded acquisition; original 8.0 installer remains OPEN. Metadata in `STONEAGE-WAYI-2005-ARCHIVED-PAGES-R1.json`.
