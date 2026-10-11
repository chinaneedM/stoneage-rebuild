# Wayi official 8.0 download chain and executable specimens R1

FACT: Raw operator download HTML recovered from actual **2006-02-21** capture, requested May2006. It retains an explicit July1 **2005** `石器時代8.0完整主程式` entry linking `ftp://download.wayi.com.tw/Stoneage80.exe`. This supersedes an inference that only the April2005 7.5 installer pointer exists. The new page is a 2006 capture of dated entries, not recovered July2005 HTML. It does not prove equality to a later third-party file named Stoneage80.exe.

| Displayed date | Official pointer | Bounded meaning |
|---|---|---|
| 2005-07-06 | fileid335 → sa.exe | Official 8.0 replacement game executable listing |
| 2005-07-01 | FTP Stoneage80.exe | Full-client pointer; bytes still OPEN |
| 2005-05-18 | fileid333 → adrn_129.rar | Listed 7.5 black-screen image-index repair |
| 2005-05-17 | fileid329 → StoneAge2.exe | Official 8.0 launcher/updater listing |

November27 **2005** archived original fileid335 redirect links `/download/file/onlineGame/sa.exe`. Its distinct archive response, captured September15 **2006**, is369152 bytes, SHA256 `4b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38`. Static PE32/i386/UPX headers have July6 2005 12:05:11UTC timestamp. Embedded strings: Waei SaDeb / SaDeb.exe /1.0.0.1. These old resource values do not contradict or override the operator's commercial8.0 listing: resource version is not the commercial release version. Timestamps/resources are mutable and not a publisher-original checksum.

Previous operator-linked StoneAge2.exe response113664 bytes/2006-09-08/SHA256a72a2fa646766f9c3a9a04f4340a3c7a1d76029d0c464bc7613f604a1900820f is now explicitly linked to the retained May17 8.0 entry. Static decompression only used official UPX4.2.4 tool. No original program ran. Output hashes are separate from archive-response hashes:

| Specimen | Decompressed bytes | Decompressed SHA256 |
|---|---:|---|
| sa.exe | 921600 | 4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63 |
| StoneAge2.exe | 253952 | d0d9c33acc7eb47c2f625b827d5e30daccd29cb9782ff6c302b730e0a5406b2f |

HYPOTHESIS supported by static observations: sa.exe serves game-client role (ClientLogin, CharLogin,511 extracted data-path strings); StoneAge2 serves updater role (SaUpdate1.0.0.5,23 data-path strings, update host `stoneage.wayi.com.tw`, `/saupdate/sa70a/newest7x.txt`, `/saupdate/newest6.txt`). Literal paths do not establish actual selected branch, available manifest, runtime behavior or PET protocol.

FACT: May24 **2005** fileid333 redirect links adrn_129.rar. Actual September11 **2006** response3983427 bytes has RAR magic and SHA256b077dcc7f1e944c33c6df4fe629d5e37abce9cb4d40f5b8d800cc69d59416e25. No extraction/member identity; advertised bin contents remain unverified. Directory CDX `length` describes archive records, not raw file length. patch007.exe and EnumDriver.exe are unrelated-name directory hits, not StoneAge files absent a source chain.

OPEN: Full installer replay HTTP/FTP404 and HTTP CDX `[]` are bounded archive lookup results, not proof of historical absence. FTP CDX503 is indeterminate. Both embedded manifest path replay requests returned archive404; no manifest bytes recovered. Original2005 file response or independent publisher digest is still missing. Native PET pair/owner/save/unique-code/opcode127 remains OPEN; pressure2486=2465+18+3 unchanged, no early-era promotions or modern-engine transition.

## Reproduction

`python tools/stoneage_wayi_pe_static_inventory.py /path/to/local-specimen.exe` inspects at most8MiB offline. It checks DOS/PE32/i386 headers, bounded section table/raw ranges, hashes the exact input, records markers with file offsets and structurally bounded candidate VERSION strings (not certified resource-directory membership). No fetching, executing or unpacking in the tool/CI. Ten synthetic controls cover truncation, count/ranges, formats, marker encodings, candidate block parsing and immutable evidence flags. CI runs47 checks including the three adjacent archive suites. Original HTML, compressed/decompressed programs, RAR and UPX tool are excluded from Git; only derived metadata is committed.
