# Taiwan WAYI StoneAge 8.5 installer: source chain, not authenticated bytes (R1)

2026-10-11. This is a **later 8.5 candidate** and cannot establish official Taiwan 2005 8.0 PET runtime.

## Evidence

1. A 2006-08-13 private-server forum guide (https://bbs.comefromchina.com/threads/449920/) cites the operator-domain `http://download.wayi.com.tw/download/STONEAGE20060616.exe` and calls it Taiwan 8.5.
2. An independent 2008-02-16 guide (https://www.nakuz.com/thread-3245861-1-1.html) cites **the same exact** operator-domain URL and labels it StoneAge 8.5. Subsequent private-server login/patch instructions in both guides are contamination, not part of the clean-client source.
3. A 2012-04-14 community preservation post (https://www.lab.welovesa.com/viewthread.php?action=printable&tid=1654) distributes six MediaFire pieces with matching basename `STONEAGE20060616.exe.001` through `.006`. All six individual **landing pages** show correct filenames, five rounded 200MB size labels and one 92.4MB label, and their 2012-04-14 upload display times. This is **page metadata**, not verified downloaded payload or exact byte size.
4. A 2024-02-20 forum reply claims installing the package displays version 8.5; this is a later recollection, **not** a version-resource inspection by this project.

The filename component `20060616` is **not an independently verified release date**. Original WAYI publisher bytes have not been retrieved; six community mirror links sharing a basename do not establish identical hashes. The sixth part shows a *chronologically earlier hosted upload time* than the first five; concatenate by numeric part suffix, not upload date.

Complete hosted IDs, timestamps, label sizes and source-claim boundaries live in `research/recovered/STONEAGE-WAYI-85-SIXPART-METADATA-R1.json`. The labels are rounded UI sizes: no exact total size may be claimed.

## Reproducible no-promotion gate

`tools/stoneage_wayi_85_archive_chain.py` validates exact six-part metadata, forbids all false authentication flags, and (only with `--local-dir`) computes read-only streaming local SHA256 of all six **locally supplied** pieces and the concatenated sequence. It **never downloads, extracts or executes** an original binary. A local digest alone remains `LOCAL_HASH_ONLY_NOT_ORIGINAL_AUTHENTICATION`. CI includes mutation tests and empty/missing-file rejection.

## OPEN and next steps

- Retrieve unmodified clean Taiwan **8.0** original installer/patch bytes for the active historical PET feature gate; the 8.5 mirror is an optional later comparison bridge.
- If six 8.5 parts become retrievable, calculate each exact SHA256 and joined hash, inspect version and installer metadata offline, then compare independently authenticated original publisher hashes. Until that comparison, community mirror authenticity remains OPEN.
- No enabled original paired server, live PET packet127, natural item owner/unique-code, or JSS1999/Taiwan1.0 feature membership was established.
- Mainland `http://cdl.wayi.com.cn/sa8_8016.rar` is a **separate** artifact lineage and MUST NOT be conflated with Taiwan WAYI 8.5.
- No copyrighted executable/assets imported. Historical pressure remains 2486 = 2465 bounded closed + 18 OPEN + 3 historical UB; no production-engine promotion.
