# StoneAge 2.5 preserved bridge — installation-residue boundary R1

## Scope

This note classifies the filesystem shape of the recovered mixed StoneAge 2.5 client/server/login bundle. It does **not** promote the bundle to an original 2002 installer or clean client.

Canonical derived inventory:

- `research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt`

Original recovered payload bytes remain outside the repository.

## Observed client-root layout

The recovered `SA2.5主程式/stoneage2.5/` root contains:

- `sa_2903.exe`
- `sa_2903网通.exe`
- `Startup.exe`
- `StoneAge.exe`
- `Stoneage2.ico`
- `UNWISE.EXE`
- `data/`
- `map/`

The derived full inventory contains **no client-root**:

- `INSTALL.LOG`
- `SETUP.EXE`
- `SETUP.INI`
- `AUTORUN.INF`
- `*.CAB`
- `*.MSI`
- `*.HDR`
- `*.INX`
- `*.ISS`
- other obvious Wise/InstallShield source-media payload files.

The only installer-family residue at the client root is `UNWISE.EXE` (149,504 bytes; SHA-256 `49ef36bd01b8ebf38c7b807a5fb44cbaf47c9d4efa883b01c41494c61ae4a2e2`).

## Embedded executable timestamps

The static inventory's PE metadata records:

- `Startup.exe`: **2001-07-13 14:48:02**
- `StoneAge.exe`: **2002-01-11 02:04:43**
- `sa_2903.exe`: **2002-04-10 10:12:40**
- `UNWISE.EXE`: **1999-06-25 14:55:29**

These are PE header timestamps, not authenticated release dates. They may reflect toolchain/build metadata and can be altered. They are therefore used only as lineage constraints, not as release-date proof.

The important practical point is that the runtime set is **not temporally homogeneous**. In particular, the preserved `sa_2903.exe` carries a timestamp later than the January/February 2002 StoneAge 2.5 rollout window and already has independently documented community/private-server contamination strings/endpoints.

## Classification

**FACT:** the recovered object is a directory tree containing runtime/resource files and uninstall-program residue, not a preserved original installer-media layout.

**HYPOTHESIS — high confidence:** the `stoneage2.5` subtree is closer to an **installed/deployed client directory copied and later repackaged** than to an untouched January-2002 retail/download installer extraction.

Reasons:

1. runtime/resource tree is already fully expanded;
2. `UNWISE.EXE` survives without the normal surrounding install-media payload;
3. no setup package, cabinet/MSI or autorun layer is present;
4. runtime components are heterogeneous in embedded build time and contamination status;
5. the parent archive itself is a later mixed client/server/login engineering bundle.

## Archaeology consequence

Do **not** use this bridge tree to infer:

- the original 575/580 MB full-package filename;
- the original 8.25 MB updater filename;
- original disc volume label;
- original setup executable name;
- original Wise/InstallShield package structure;
- January-2002 launch-state runtime identity.

The bridge remains valuable for:

- resource/container format reconstruction;
- map-cache lineage comparison;
- operator-looking `StoneAge.exe` lineage analysis;
- later 2.5-family runtime/resource differential work.

If a real 2002 disc/download package is recovered, compare it against this tree at file/hash level and classify each matching component independently.

## Status

**BOUNDED FOR INSTALLER-FILENAME INFERENCE / RETAIN AS RESOURCE BRIDGE.**
