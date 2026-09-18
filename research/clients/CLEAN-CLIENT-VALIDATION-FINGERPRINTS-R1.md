# Clean Client Validation Fingerprints — R1

Date: 2026-09-18

## Purpose

Prevent a historical-looking StoneAge archive from being promoted to the bridge specimen merely because its title, folder name or one embedded string says `2.5`, `1.82`, `original` or `clean`.

## Core rule

**No single string is a version oracle.** Promotion requires agreement across provenance, bytes, runtime metadata, resource lineage and contamination checks.

## Known version/login-key control

A preserved 2010 We Love SA technical discussion labels:

- `_DEFAULT_PKEY = "ttttttttt"`
- `_RUNNING_KEY = "20041215"`

as `原始2.5版本`, and distinguishes community variants such as `12345678/12345678` and `cary/cary`.

However, a later 2015 discussion shows another source tree where the same `ttttttttt / 20041215` pair is commented as 7.5. The same thread states that different client versions also differ in login-packet format.

Therefore the key pair is useful as a **lineage/contamination fingerprint**, but not as standalone version proof.

Sources:

- https://www.lab.welovesa.com/viewthread.php?action=printable&tid=501
- https://www.shiqi.la/forum.php?extra=page%3D1&mobile=no&mod=viewthread&tid=13339
- https://www.lab.welovesa.com/redirect.php?goto=lastpost&tid=3175

## Promotion checklist for recovered bytes

1. distribution provenance and archive history;
2. archive filename, size and hashes;
3. complete file tree and timestamps;
4. PE metadata and executable naming;
5. embedded version/operator strings;
6. launcher/updater/config/network artifacts;
7. PKEY/RUNKEY and related login fingerprints;
8. packet/version behavior where safely inspectable;
9. REAL/ADRN/SPR/map/resource-format generation;
10. custom private-server domains/IPs;
11. custom launchers, DLL loaders, injectors, 外挂 components or replaced resources;
12. cross-copy comparison against another claimed copy when possible.

## Decision rule

- A candidate may become the bridge specimen only when the evidence is internally coherent and no material private-server modification is found.
- A conflicting title/version string lowers confidence; it does not get explained away.
- Community comments are clues. The recovered bytes remain the primary evidence.
