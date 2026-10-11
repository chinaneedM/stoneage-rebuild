# Taiwan StoneAge 8.0: 2005 physical discs and 2006 DLER mirror, R1

**Date:** 2026-10-11. **Evidence status:** source-only, provenance-sensitive. No authenticated publisher-owned Taiwan 2005 8.0 installer, disc image, SHA, completed update tree or compiled original PET-equipped client/server has been retrieved.

## 1. Prior-to-release 2005 distribution lead

The **2005-06-03 contemporaneous GNN press index** (https://acg.gamer.com.tw/search.php?c1=976&c2=3&machine=1%2C0&s=2&type=1) includes “《石器時代》捷運淡水站歡樂大拍賣” with a reported Waei plan to **give away 8.0 revision/update discs at the June 4 Tamsui MRT station event**. The searchable news excerpt, not the original official event disc or complete press article, is the evidentiary surface. It establishes an announced physical distribution opportunity; it does not establish actual handover, the disc's content or whether it was a full installer.

The contemporaneous GNN **2005-06-08 release article** (https://gnn.gamer.com.tw/detail.php?sn=20167) separately reports official Waei Taiwan version 8.0 PET equipment launch and boxed-pack update discs. The announced June 4 event carrier and June 8 product-package carriers remain distinct until authentic media images, exact file trees and cryptographic checksums establish relationship. The later recollection of June 6 VIP discs also does not by itself identify June 4/8 physical media contents.

## 2. New 2006 Taiwan-hosted third-party mirror path, NOT verified original

A Hong Kong **2006-08-01** player discussion (https://www.nakuz.com/thread-2493728-1-1.html) quotes a fully specified main-program path:

`http://tcrc.dl.dler.org/Yesterday/v/wayi/Stoneage80.exe`

The original text is explicitly a private-server usage guide: it discusses selecting executable `sa_7505`, use of `sa_7507` login tool and replacing or renaming resource files. A later response in the same thread disputes that all servers require those binaries and mentions `sa_8001`. These details rule out treating the HOWTO as a successfully verified 8.0 historical PET execution trace. They **do not** prove that the uninspected main installer itself was modified—its bytes were never obtained. Likewise the hostname and path component `/wayi/` do not prove the host was an official Waei publication endpoint.

Public DLER's later site (https://dler.com/index.php?o=display%3Bid%3D7143) does have a different 2018 StoneAge listing with modern size and MD5; it is unrelated to the 2006 filename and must not transfer checksum, release version or custody. The 2006 mirror address was not accessible via the current web document reader; that observation is **not an HTTP 404 from the origin** and not evidence it has disappeared everywhere.

## 3. Acquisition and safety protocol

**New lead priority:** seek independently preserved copies of the *exact* `Stoneage80.exe` on the specified DLER path, preserving metadata and SHA256 before any extraction, but keep its tentative 2006 mirror provenance separate from the 2005 Taiwanese release disc family. Check archive captures and authenticated original Wayi installation manifests if obtainable. Do **not** equate a filename containing “80” to on-disk executable version 8.0. Never upgrade an unverified third-party copy solely because private-server tutorials recommend it.

Source-only JSON: `research/recovered/STONEAGE-TW80-DISC-MIRROR-IDENTITY-R1.json`. Gate: `tools/stoneage_tw80_disc_mirror_identity_gate.py`. Tests: `tests/test_stoneage_tw80_disc_mirror_identity_gate.py` (19 control/mutation checks); workflow `validate-stoneage-tw80-disc-mirror-identity.yml` reruns chronology, regional candidate quarantine and installed-state snapshot tests.

No original files or proprietary assets enter GitHub. Existing pressure `2486 = 2465 bounded closed +18 OPEN +3 historical UB`, JSS1999/Taiwan1.0 evidence and the original PET packet127/persistent owner-identity verification remain unchanged. New-engine stage is not activated.

**Highest NEXT:** digitally recover source-authenticated 2005 **Taiwan official 8.0** original installer/disc/patch and exact hashes or a contemporaneous original-file manifest/checksum; optionally investigate 2006 DLER mirror as a version-quarantined candidate. Verify publisher custody separately from network-host identity and binary identity.
