# StoneAge `sa-arena` optical negative control — R1

Date: 2026-09-25

## Purpose

This note classifies Internet Archive item `sa-arena`, which was surfaced by the project's generic StoneAge archive-candidate scan because its current metadata title contains `疯狂原始人 Stoneage Arena Online CD-ROM 2002` and names 北京华义. The item was investigated only because it could have been mistaken for an early Mainland StoneAge carrier.

The result is a **negative control for StoneAge client recovery**: the preserved optical object is a Beijing-Waei/WGS-era `疯狂原始人` product disc, not a StoneAge 2.5 client disc.

## Preserved-object FACTS

The current Internet Archive file metadata exposes an original BIN/CUE pair:

- `CD [SA_ARENA].bin`
  - 721,431,312 bytes
  - MD5 `f4e7b6ec2b27282d67f6b3982310cc2e`
  - SHA-1 `f21da5f459db55cc5e09fccadc09f00a7b115177`
  - CRC32 `bcf893b0`
- `CD [SA_ARENA].cue`
  - 299 bytes
  - MD5 `3b6ddb5cf3de1760273d5bd75cc6d7e4`
  - SHA-1 `5928bffc95d34be28fcce802cced0b2769f625b4`
  - CRC32 `2d33121f`

The CUE has one `MODE1/2352` track. Bounded HTTP Range reads recover the ISO9660 filesystem without downloading the full image:

- volume label: `SA_ARENA`
- logical volume size: 306,731 × 2,048 = 628,185,088 bytes
- root files/directories:
  - `AUTORUN.INF`, 48 bytes
  - `DIRECTX8/`
  - `README.TXT`, 22,009 bytes
  - `SAARENA.EXE`, 599,802,752 bytes
  - `SA_ARENA.ICO`, 2,238 bytes

`AUTORUN.INF` SHA-256 is `5249a555ab91845294983c384da2d204527922eddbf86880b0a5e8b1d7c8ac7f` and launches `SaArena.exe`.

`README.TXT` SHA-256 is `b4a7145830418692f73030e8b6f6561458bbe272252f23178ec538e107cdd3ab`; it decodes as GB18030/GBK-family Simplified Chinese.

## Product-identity FACTS from the preserved README

The README identifies the product itself as `疯狂原始人`, including:

- product registration instructions explicitly headed `注册《疯狂原始人》`;
- a statement that the product contains **10 days and 10 nights of free game time**;
- Beijing-Waei/WGS account and charging instructions using `http://www.waei.com.cn` and `http://www.wgs.com.cn`;
- default installation directory `C:\Program Files\Waei\疯狂原始人\`;
- Beijing Waei contact identity `北京华义联合软件开发有限公司` and `tiki@waei.com.cn`.

Most importantly for StoneAge classification, the README states that WGS points can be used for **`《石器时代》、《大法师》、《疯狂原始人》`** and other WGS-supported games. The text therefore treats `石器时代` and `疯狂原始人` as separate products in the same WGS ecosystem.

This byte-derived distinction independently agrees with the project's later SMZDM collector control, whose surviving-disc list separately names `2.5 / 3.0 / 4.0 / 5.0 / 疯狂原始人`.

## Installer prefix

Only the first 524,288 bytes of `SAARENA.EXE` were read. The prefix:

- SHA-256: `1144fe338a01f785520fca6fed4003d9f1767f22f9ec552e209bb79268ec638e`
- contains a valid PE header;
- exposes Wise Installation Wizard strings.

The PE timestamp field is preserved in the derived report but is **not interpreted as a release date**.

No deeper installer read is justified for the StoneAge 2.5 recovery objective because the README already resolves the product identity.

## Evidence boundary

**FACT:** the archived BIN/CUE object is a complete optical distribution object with the hashes, volume label and filesystem structure recorded above.

**FACT:** preserved README bytes identify the product as `疯狂原始人` and explicitly distinguish it from `石器时代` within the WGS ecosystem.

**OPEN:** the current Internet Archive title/date/creator fields are uploader/catalog metadata and are not independently promoted to contemporaneous publication facts by this probe.

**NOT SUPPORTED:** any claim that this BIN/CUE is a StoneAge 2.5 client, a 2.5 pressing, or byte-equivalent to any recovered StoneAge client.

## Operational consequence

- Remove `sa-arena` from the StoneAge 2.5 candidate queue.
- Retain it as a **same-operator / same-WGS-era negative control** for identifying filenames, packaging vocabulary, WGS documentation and optical-disc layout.
- Do not spend primary recovery effort extracting the 599 MB installer unless a future cross-product technical question specifically requires it.
- This result does **not** move the StoneAge 2.5 field-map provenance anchor earlier than June 2003.

Canonical derived report: `research/recovered/STONEAGE-SA-ARENA-IA-OPTICAL-R1.txt`.
