# StoneAge 2.5 2009→2011 descendant distribution lineage — R1

Research date: 2026-09-25

## Scope

This record separates a historically useful **community descendant distribution lineage** from original/operator StoneAge 2.5 provenance. It records source relationships and exact recovery tokens without assuming byte identity between packages.

## 2009 source distribution

Source thread:
- https://www.iopq.net/thread-16615099-1-1.html
- Author: `love198959`
- Posted: 2009-12-17 20:34:26
- Title: `[亲测]石器时代2.5精灵王的传说`
- Reported client size: about **420M**
- Exact client URL: `http://download1.92ysa.com/YSA2.5.8.rar`

The post describes the client download separately from an additional RayFile package containing single-player login tooling, login-tool construction tooling and the server; an外挂 package is also linked separately.

The post's installation text refers to `石器时代WIN版2.5.exe`, a matching single-player patch containing `cax.ini`, and a `D:/csa/gmsv` deployment context. The publicly indexed text does **not** expose `SACH-MX0.30` or `sa_2903.exe`.

The exact `YSA2.5.8.rar` public-preservation path was previously probed and remains bounded:
- Wayback exact HTTP/HTTPS: 0 captures;
- Wayback Availability: 0 snapshot;
- Internet Archive exact filename: 0;
- DiscMaster exact filename: 0.
Canonical report: `research/recovered/STONEAGE-YSA25-ARCHIVE-PROBE-R1.txt`.

## 2011 one-click derivative

Source thread:
- https://www.iopq.net/thread-16731619-1-1.html
- Author: `5615918`
- Posted: 2011-07-21 08:55:58
- Edited: 2011-08-04 10:21
- Title begins: `(原创)石器时代2.5精灵王的传说...`

The author explicitly thanks `love198959` for the earlier post, then states that this is a newly assembled one-click installation. This establishes a **public source/derivation relationship at the post level**, but not byte continuity.

The 2011 installation instructions explicitly introduce:
- `石器时代WIN版服务端管理器.exe`;
- `SACH-MX0.30/STW0.30.exe`;
- client launch path `D:/csa/gmsv/stoneage2.5/sa_2903.exe`;
- bundled single-player server behavior.

A contemporary reply states that the downloaded `GMSV` directory lacked `GMSV.EXE` and that the user copied a 2.5 Windows server executable from another site before running the package. This is direct evidence that the one-click corpus could be incomplete/mixed and must not be treated as a clean baseline.

Exact public 115.com recovery token:
- first URL: `http://u.115.com/file/clnrsbsc`;
- later URL: `http://115.com/file/clnrsbsc#`;
- token: `clnrsbsc`;
- filename: `石器时代2.5精灵王的传说一键.zip`.

The source later asks users to contact the poster if the resource expires. A current mirror/repost at `https://www.7chaowan.com/52247.html` preserves the same 115 token and instructions, but does not supply an independent payload hash or new file host.

## Preservation probe

Canonical report:
`research/recovered/STONEAGE-SA25-115-LINEAGE-PROBE-R1.txt`

Workflow run:
- GitHub Actions run `36092086106`
- conclusion: success

Results:
- Wayback successful exact/prefix surfaces: **0 HTTP-200 rows**;
- Arquivo.pt successful exact surfaces: **0 rows**;
- Internet Archive exact token/filename searches: **0 documents**;
- two Wayback variants timed out and remain inconclusive;
- no archive bytes, file tree, checksum or mirror payload was recovered.

## Evidence classification

FACT:
- the 2009 post exposes `YSA2.5.8.rar` as a client download and separates server/login tooling into another package;
- the 2011 post explicitly credits the earlier author, describes a newly assembled one-click package, exposes `SACH-MX0.30`, `sa_2903.exe`, and exact 115 token `clnrsbsc`;
- the 2011 one-click source has direct mixed/incomplete-server evidence from its own replies.

SUPPORTED LINEAGE INTERPRETATION:
- a StoneAge 2.5 private/single-player engineering ecosystem was publicly circulating by 2009 and was being reassembled/reposted by 2011;
- the 2011 package belongs to the same broad descendant engineering ecosystem as later SACH/`sa_2903.exe` bundles.

NOT ESTABLISHED:
- byte identity between `YSA2.5.8.rar` and `石器时代2.5精灵王的传说一键.zip`;
- byte identity between either package and the recovered 2012 MediaFire mixed bundle;
- original Beijing-Waei retail-disc provenance;
- clean runtime provenance;
- any pre-2003 field-map provenance.

## Operational consequence

Treat `clnrsbsc`, `石器时代2.5精灵王的传说一键.zip`, and the two thread IDs as descendant-lineage search keys only. Do not spend primary recovery effort on this route unless a public payload, hash or file tree appears. If bytes ever become publicly recoverable, compare them against the existing MediaFire bridge and 99ds descendant corpus before making any lineage claim.
