# StoneAge 2001 xinhaonanhai contributor-lineage audit — R1

Date: 2026-09-25

## Scope

This note narrows the provenance interpretation of the active 2001-11-27 field-map target `Estoneage2.0map_1127.exe` without promoting any unrecovered package bytes.

## Evidence

### FACT — 2001-11-27 Sina full-map record

The surviving Sina download record for `《石器时代》全地图` names `xinhaonanhai` as the contributor, states size 1911K, says the package is usable with `1.X，2.0`, and exposes the exact local-download token `aid=43172` / `Estoneage2.0map_1127.exe`.

The project already records this as `SRC-CN-2001-SINA-FULLMAP-01`.

### FACT — the alias remains active inside Sina's StoneAge community in 2002

Sina's surviving StoneAge forum/award pages show the same alias participating in the StoneAge community during 2002. More importantly, November event text explicitly instructs prize winners to contact “斑竹xinhaonanhai”, identifying the alias as a forum moderator on the Sina StoneAge surface by that time.

Relevant surviving pages:

- `https://games.sina.com.cn/zhuanqu/stoneage3/zhongjiang0816.shtml`
- `https://games.sina.com.cn/zhuanqu/stoneage3/mingdan10.shtml`
- `https://games.sina.com.cn/zhuanqu/stoneage3/mingdan11.shtml`

These pages establish the role of the alias on Sina's StoneAge community surface; they do not establish a civil identity.

### FACT — 2002-11-08 Sina 4.0 full-map patch uses the same contributor alias

The surviving Sina download-center record `《石器时代4.0》最新地图补丁` is dated 2002-11-08, states size 3440K, and names `游民部落网xinhaonanhai` in the record title. Its exact local-download token is already recovered as `aid=61620` / `shiqi4updatex_02_11_08.zip`.

The description says the package makes all StoneAge maps visible locally and removes the need to read MAP data from the server during play.

The project already records this package as `SRC-CN-2002-SINA-SA40-FULL-MAP-PATCH-01`.

## Interpretation

### FACT

The string identity `xinhaonanhai` is not a one-off label attached only to the 2001 package. It appears on a sustained Sina StoneAge community surface and is explicitly associated with a later full-map package of the same functional class.

### HYPOTHESIS

The 2001 and 2002 package records likely refer to the same community contributor/account lineage. No recovered Sina account identifier or package bytes currently prove personal identity or direct file ancestry, so this must not be promoted to byte lineage.

## Provenance consequence

The 2001 `Estoneage2.0map_1127.exe` target should be treated as a **contemporaneous community-contributed field-map/cache distribution artifact carried by Sina**, not as an operator-original client component merely because Sina hosted the download.

That lowers its authority for proving what shipped on an official retail/operator client, but it does **not** lower its value for reconstructing what field-map/cache bytes were in real circulation by late 2001—especially because the source explicitly claims compatibility with both 1.X and 2.0.

If recovered, the package must be extracted and compared byte-for-byte with:

1. Taiwan Waei/JSS v1.0 map/cache evidence;
2. the 2000 `samap_1220.zip` package if it is later recovered;
3. the June-2003 historical `map.exe` corpus;
4. the mixed-2.5 corpus;
5. the 2002 `shiqi4updatex_02_11_08.zip` corpus if that package is later recovered.

## Operational consequence

Further discovery should prioritize **same-contributor and same-functional-class carriers** rather than repeating already-bounded generic Sina/Wayback scans:

- exact aliases: `xinhaonanhai`, `游民部落网友xinhaonanhai`, `游民部落网xinhaonanhai`;
- exact package names/stems: `Estoneage2.0map_1127.exe`, `Estoneage2.0map_1127`, `shiqi4updatex_02_11_08.zip`, `shiqi4updatex_02_11_08`;
- contemporaneous forum posts, mirror directories, coverdisc inventories and installed-directory backups that preserve contributor or full-map-package names.

Do not infer that the 2002 package descends byte-for-byte from the 2001 package. The shared contributor/function is a discovery key only.

## Evidence boundary

No proprietary payload is stored in this repository. This audit records public-page metadata and provenance interpretation only.
