# StoneAge 2.5 Popsoft February-2002 Carrier Boundary R1

Date: 2026-09-27  
Status: **SCAN-ONLY / OPTICAL-RESIDUAL-BOUNDED**

## Question

A contemporaneous 17173 StoneAge 2.5 upgrade guide names `《大众软件CD——大众游戏》2002年2月号` among the media through which users could obtain the StoneAge 2.5 complete package or updater. The earlier generic preservation census found one Internet Archive row for `"大众软件" AND year:2002` but did not expand it because its title failed the strict carrier filter.

This pass asks only whether the unresolved IA metadata row or the known Popsoft magazine-preservation family exposes the actual February-2002 optical carrier.

## Findings

### 1. Broad IA row is a false positive

The sole software row returned by `"大众软件" AND year:2002` is:

- identifier: `start-modem-5600d`
- title: `网际纵横 v2.3 —— 实达灵犀 5600D 随机光盘`
- creator: `福建实达网络科技有限公司`
- date: `2002-05-01`
- optical file: `START_MODEM.iso`

The ISO is a modem-driver disc. Its presence in the broad query is a metadata-description collision, not a StoneAge/Popsoft carrier. The probe now hard-rejects this object before target-optical promotion.

### 2. February 2002 Popsoft paper scans survive

IA identifier `popsoft-magazine_202403` exposes:

- `2002/大众软件-2002年02月A.pdf` — 213,906,834 bytes; MD5 `f81361daf9f1998213e191facfd110bc`; SHA-1 `95ce835b9475bfc91bded8f169828d271453cb0e`
- `2002/大众软件-2002年02月B.pdf` — 216,402,608 bytes; MD5 `2312310bf26764a76ede6f229abec66a`; SHA-1 `76915aaff249e54a0e5d090ed10172542c015072`

The item exposes 6,809 files, including 26 February-2002 A/B originals/derivatives, but **0 optical-image files** under the project's ISO/BIN/CUE/IMG/MDF/MDS/NRG/CCD/SUB classifier.

### 3. OCR corroborates editorial 2.5 presence but not disc identity

Only the small IA OCR text derivatives were read transiently:

- February A: 784,590 bytes; SHA-256 `71b56a151f692558f022c4e460ab21f1eac9b4f30579e69db8f1fff7d6043c63`; 5 StoneAge-2.5/Spirit-King proximity hits.
- February B: 870,256 bytes; SHA-256 `9614393a5280c27558f7dbc5f017964f318a251cf786ccc2413fbf70dfae3810`; 0 strong hits under the same detector.

This proves only that the February-A paper scan contains 2.5-related editorial text. It does **not** establish that A rather than B carried the target optical disc, nor that any physical `大众游戏` disc was byte-identical to an official Beijing-Waei client CD.

## Boundary

The current IA Popsoft object is a **paper-magazine preservation object, not an optical-media preservation object**. No installer filename, volume label, filesystem tree, disc checksum, mastering identity, client hash or clean-client provenance is exposed.

Do not:

- count `START_MODEM.iso` as a carrier candidate;
- treat PDF/EPUB/OCR magazine files as client-media evidence;
- infer a specific A/B cover-disc pressing from OCR editorial content;
- guess new optical filenames from the scan filenames.

Reopen this route only when a new independent token appears: exact February-2002 `大众游戏` optical identifier, disc-face photograph, ISO/BIN/CUE/file tree, checksum, torrent/archive member list, preservation uploader/collection token, or mirror URL.

## Adjacent exact visual tokens

The surviving contemporaneous 17173 2.5 product page states that the `新手报到包` had three package variants. Its new-user-package block still references exact image assets:

- `sa03.gif`
- `st25_new_02.jpg`
- `st25_new_03.jpg`

These are retained strictly as package-art / reverse-image-search tokens. They are not disc filenames or payload identifiers.

## Evidence

- Contemporary distribution page: `https://news.17173.com/z/stoneage/banben/sa25-up.htm`
- Contemporary product page: `https://news.17173.com/z/stoneage/banben/sa25-cp.htm`
- IA scan family: `popsoft-magazine_202403`
- Derived probe: `research/recovered/STONEAGE-SA25-POPSOFT-2002-RESIDUAL-R1.txt`
- Probe implementation: `tools/stoneage_sa25_popsoft_2002_residual_probe.py`
