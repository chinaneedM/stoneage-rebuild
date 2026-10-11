# StoneAge 8.0 PET Equipment: Contemporary Release Evidence and Binary Provenance Gate R1

Date: 2026-10-11. Scope: Taiwanese operator's later 8.0 version, **not** JSS 1999 or Taiwan 1.0. Historical study only, not a modern game feature decision.

## A. A stronger, separate historical claim

**FACT — contemporaneous published release announcement:** 巴哈姆特 GNN, by 小賢, published 2005-06-08 23:04:46, *《石器時代 8.0》新版上線 推出「寵物裝備」*, https://gnn.gamer.com.tw/detail.php?sn=20167 . This first-hand contemporary press report says the Taiwan 8.0: Lost World update launched on 2005-06-08; its coverage attributes statements to operator 華義 and describes the PET equipment system as part of that update. Independently mirrored by Sina on 2005-06-09 at https://games.sina.com.cn/o/n/2005-06-09/1552109910.shtml (derivative republication **not** an independent second primary witness).

**Scope of FACT:** This is strong historical evidence of an announced/launched official Taiwan 8.0 PET equipment **game feature**. It is **not** evidence that BismarckDD/Stoneage commit 999ffdf1 is the actual deployed source, that its `_PET_ITEM` macro was set in an operator build, that binary opcode 127 occurred, or that any item-index or unique-code lifecycle was executed in a surviving original executable. Operator press claim and exact binary implementation are distinct evidentiary layers.

**Corroborating but lower weight:** 巴哈姆特's 8.0 game overview describes seven equipment categories and attributes, https://acg.gamer.com.tw/acgDetail.php?s=5326 ; date/version context is consistent but does not bind a particular codebase.

## B. Binary acquisition leads, NOT accepted deploy proofs

1. **2008-12-30 community thread, claimed operator-hosted filename:** https://www.iopq.net/forum.php?mod=viewthread&tid=16508364 cites `http://cdl.wayi.com.cn/sa8_8016.rar` for an 8.0 client. The URL is a historical **lead**, not authenticated source bytes: the current retrieval attempt did not yield a verified download, no hash/manifest/embedded version has been inspected, and the same post explicitly asks readers to install private-server/client/pet/map patches. Never regard the *patched package* as a clean client or pair with an arbitrary server.
2. **2009-07-08 community launcher:** https://www.lab.welovesa.com/viewthread.php?tid=2 gives `sa_8002a` as a bundled launcher with Assa8.0 third-party tooling. This is evidence of a named *community-distributed* executable lead, not a clean operator baseline; contaminated bundling risk is explicit.
3. **2010-02-13 thread, edited 2010-07-22:** https://www.lab.welovesa.com/viewthread.php?tid=575 describes Yang SA8.0 server for `sa_8002a`, with a publicly described Windows MediaFire distribution and forum-gated Linux attachment. Author explicitly says they implemented the functions. This establishes a custom community server lineage, **not** original 2005 official deployment or pinned Bismarck code identity. A listed *riding equipment* feature must not be silently equated to original PET inventory equipment.
4. **2012-08-03 discussion:** https://www.lab.welovesa.com/viewthread.php?tid=1978 includes a later forum comment claiming 8.0 login client UI included PET equipment and could be removed by reverse engineering. This is **HYPOTHESIS / later recollection**, not executable provenance.

Sources are metadata/links only. No external binary, original source, patched client, launcher, third-party scripts or proprietary assets were copied into this repository.

## C. Acceptance matrix

| Question | This gate |
| --- | --- |
| Did contemporary reporting describe official Taiwan 8.0 PET equipment on launch? | FACT (2005-06-08 press record) |
| Is the checked-in pinned later Bismarck default PET feature enabled? | NO in the previously accepted default source/profile gate |
| Are the 2008/2009/2010 digital download URLs presently byte-verified? | OPEN; none fetched/hashed/authenticated here |
| Is there an original compatible enabled client/server binary pair with version identifiers and checked configuration? | OPEN |
| Was opcode 127 observed from an original game client to an original server? | OPEN |
| Are native PET item owner/unique code/save-load transitions reproducible without synthetic aliases? | OPEN |
| Does any result establish 1999 JSS or Taiwan 1.0 PET equipment? | NO |

## D. Next retrieval and executable audit gate

Identify an independently retrievable **operator-distributed** 8.0 client archive or original versioned binary. Record carrier URL, timestamp, chain of custody, exact SHA256, file list, executable PE/version metadata and clean/patched ambiguity. Pair with a separately authenticated server only if matching version/configuration is evidenced. Then check PET UI behavior and packet 127 with permission and within isolated local offline analysis; test native item owner, save/load and unique-code lifecycle only after genuine route admission. Community-built/modified executables stay separate and can prove only their *own* behavior. If no clean verifiable binaries are available, retain the runtime OPEN.

This supplements, and does not replace, the accepted `STONEAGE-PET-PAIRED-BUILD-MATRIX-R1.md` source-only negative default-build result. Pressure remains 2486 = 2465 bounded closed + 18 OPEN + 3 historical UB; zero early-provenance promotions.
