# StoneAge 2.5 Preserved Bundle Assessment — R1

Date: 2026-09-18

## Scope

This report assesses the publicly preserved two-part StoneAge 2.5 bundle recovered from the We Love SA thread and MediaFire. The proprietary payload is not committed; only hashes, metadata, file-tree findings and derived conclusions are stored.

## Recovery integrity

MediaFire quick keys:

- `ev7l29fw77891go`
  - filename: `石器2.5客戶端+服務端+登入器.rar.001`
  - size: 209,715,200 bytes
  - SHA-256: `7cb7acdecd56617132e6f284c468158917c91d542cad5b2e7b3c7774fb5630d5`
- `ytaa168o5jih0lx`
  - filename: `石器2.5客戶端+服務端+登入器.rar.002`
  - size: 151,539,980 bytes
  - SHA-256: `567e1ec0aeff9ea6a9ada791a339aa8f8bb8ffba83cf762e4b445fc0f1cb16bb`

The downloaded hashes exactly matched the hashes returned by MediaFire metadata.

Reassembled archive:

- size: 361,255,180 bytes
- SHA-256: `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`
- MD5: `75ca860039f24ea6d1b61a0e3f732903`
- format: RAR v4 / Win32
- extraction: successful with `unar`

Derived full inventory:
`research/recovered/STONEAGE-25-PRESERVED-BUNDLE-STATIC-INVENTORY-R1.txt`

## Bundle structure

Whole recovered bundle:

- 6,762 files in the derived inventory.

`SA2.5主程式` subtree:

- 3,709 files
- 882,509,343 bytes
- contains two materially different components:
  1. `stoneage2.5/` — the game/resource tree;
  2. `SACH-MX0.30/` — a separate scripting/helper corpus containing `脚本` and hundreds of script files.

The scripting/helper corpus is not treated as part of the clean game baseline.

## Core `stoneage2.5` resource tree

The `stoneage2.5/` subtree contains:

- 2,302 files
- 863,480,809 bytes

Top-level composition:

- `data/`: 255 files, 793,985,987 bytes
- `map/`: 2,041 files, 67,960,104 bytes
- five EXE files plus icon/uninstaller support

Major resource containers:

- `data/real_15.bin` — 763,908,374 bytes
- `data/adrn_15.bin` — 18,765,120 bytes
- `data/spr_4.bin` — 5,588,120 bytes
- `data/spradrn_5.bin` — 10,164 bytes
- `data/sound_1.bin` — 3,695,418 bytes
- `data/sound_3.bin` — 898,978 bytes
- `data/battle_2.bin` — 187,500 bytes
- 220 `battleMap/*.sab` files
- 16 palette `.sap` files
- 2,041 `.MAP` files in the core map directory

This is a high-value bridge corpus for resource/container and map-format reconstruction even though the runtime layer is contaminated.

## Runtime executables

### `StoneAge.exe`

- SHA-256: `e258bc1ba166e30962b57ff34b216d86889cb2adac12d4e27acd8c8cbb5b000c`
- PE timestamp: 2002-01-11 02:04:43
- embedded operator-era endpoints/strings include:
  - `www.waei.com.cn`
  - `www.waei.com.cn/zhuanqu/stoneage2/`
  - `www.wgs.com.cn/input.htm`
  - `www.wgs.com.cn/reg_sta.htm`
  - `www.wgs.com.cn/reg_card.htm`
  - `ftp.stoneage.com.cn`
  - `Waei Stoneage Path`

Interpretation: this is strongly consistent with a Mainland Wayi-era StoneAge launcher/startup component, but the current bundle provenance does not prove this particular copy is byte-identical to an untouched operator installer.

### `sa_2903.exe`

- SHA-256: `ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16`
- PE timestamp: 2002-04-10 10:12:40
- embedded fixed endpoint: `202.75.217.50`
- contains community-lineage strings including `[cary encounton]`, `[cary encountoff]` and `12345678`

### `sa_2903网通.exe`

- SHA-256: `79554dd8526cf30afc50575d178461338afd3c299bd959987390496f106cde50`
- same PE timestamp as `sa_2903.exe`
- embedded fixed endpoint: `202.75.208.50`
- contains the same `cary` / `12345678` lineage markers

These two runtime binaries are not acceptable as clean-version proof. Their fixed endpoints and community-lineage markers demonstrate that the preserved runtime layer has been modified or repurposed.

### Other executables

- `Startup.exe`
  - SHA-256: `67dfad6360387dd9c04c0918f8f3c16d319e190b52ae6d8e7ded787dee2ace2c`
  - PE timestamp: 2001-07-13
- `UNWISE.EXE`
  - SHA-256: `49ef36bd01b8ebf38c7b807a5fb44cbaf47c9d4efa883b01c41494c61ae4a2e2`
  - installer/uninstaller support component

## Clean-client decision

### Runtime-baseline grade: **C / MIXED-MODIFIED**

This recovered package must **not** be promoted to the project's clean bridge runtime client.

Reasons:

1. it is a community-preserved client + server + login bundle rather than an operator installer;
2. the main-program subtree includes a separate scripting/helper corpus;
3. two game executables embed fixed non-operator endpoints and community-lineage markers;
4. the bundle contains multiple executable variants rather than a single provenance-preserving runtime path.

### Resource-corpus grade: **B / HIGH-VALUE BRIDGE**

The resource corpus is still immediately useful for deterministic reverse engineering because it provides a large, coherent set of:

- REAL/ADRN graphics data;
- SPR/SPRADRN data;
- sound containers;
- palettes;
- battle-map records;
- 2,041 client map files.

The project may use this corpus to build parsers and format specifications while continuing to search for a cleaner runtime client. No claim is made that every resource file is original or strictly 2.5 until cross-version comparison is available.

## Next technical actions

1. Treat `stoneage2.5/data/real_15.bin + adrn_15.bin` as the first recovered image-resource test corpus.
2. Validate the already reconstructed ADRN/REAL record assumptions against these actual bytes.
3. Decode a small deterministic sample of `RD` blocks and compare dimensions/offsets against ADRN metadata.
4. Parse representative `.MAP` files and infer the map header/tile-layout family from real bytes.
5. Keep the runtime executables only as lineage/negative controls.
6. Continue recovery of a cleaner 2.5 client and the earlier Korean 1.74 / Japanese 1.74a candidates.
