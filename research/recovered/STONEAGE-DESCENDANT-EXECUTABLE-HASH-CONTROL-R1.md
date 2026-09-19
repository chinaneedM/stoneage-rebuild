# StoneAge descendant executable hash control — R1

Retrieval date: 2026-09-19

## Scope

This record is a negative/false-positive control for clean-client recovery. It preserves public static metadata for a later StoneAge-related executable so future exact-hash/file-name hits can be rejected quickly unless independent historical provenance contradicts this classification.

## Public report

- Source: ANY.RUN public report
- Report URL: https://any.run/report/9c019d9fab9c0dc37a37a67519ca5080ae43ec2b2a84b915a24b742512a6a7ca/a36313b7-be88-42a2-a913-2a62f8edccb7
- Analysis date shown by source: 2019-10-21
- Submitted filename: `StoneAge.exe`
- PE type: PE32 GUI / Intel 80386 / Windows
- MD5: `A1A524D45C90ED3B7537A254B8757740`
- SHA1: `8C89E619399AFDF7F0F706722C3E648FA2A99654`
- SHA256: `9C019D9FAB9C0DC37A37A67519CA5080AE43EC2B2A84B915A24B742512A6A7CA`

## Version-resource / PE metadata reported by source

- PE timestamp shown: 2019-10-08 10:14:10 UTC-equivalent in the report summary
- `CompanyName`: `石器时代`
- `FileDescription`: `Stoneage`
- `FileVersion`: `1, 0, 0, 1`
- `InternalName`: `石器时代`
- `LegalCopyright`: `Copyright c 2010`
- `OriginalFileName`: `Sa.exe`
- `ProductName`: `石器时代`
- `ProductVersion`: `1, 0, 0, 1`
- Version-resource language: Chinese (Simplified)
- Reported detected languages include Chinese, English and Korean.
- Debug/output strings include a Themida Professional marker.

## Search control

Exact searches of the SHA256, SHA1 and MD5 in the GitHub global code index returned zero matches on 2026-09-19.

## Classification

**DESCENDANT / FALSE-POSITIVE CONTROL — NOT A CLEAN 2000–2001 KOREAN CLIENT CANDIDATE.**

The filename and `OriginalFileName=Sa.exe` overlap with StoneAge search traits, but the available metadata does not supply period provenance for Inium/Hananet/GameTime/CNET and instead points to a substantially later Chinese-descendant executable. PE timestamps and version resources are not immutable provenance by themselves, so this record is an exclusion/control fingerprint rather than a claim about exact lineage.

Do not use this sample to infer the original Korean executable hash, size, version, compilation date or binary identity.
