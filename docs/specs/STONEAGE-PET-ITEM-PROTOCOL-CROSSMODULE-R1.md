# Bismarck optional PET equipment protocol — three-stage source-only gate R1

Status: **SOURCE_ONLY_OPTIONAL_PET_PROTOCOL_CHAIN_ACCEPTED**.
Tested pinned Bismarck late descendant `999ffdf1d220ec6666eb65339180689c9caf1876`
under Actions38143205543/job114481110061 SUCCESS (24 Python tests).
Derived native-source report 1710 bytes SHA256
`24c2723a3b268f3c0dd9b401edf03d5ead128ec61464b03afabd38a9fea1327e`,
Git blob `2a9316528c30460f8a314862dcf22f57d198190e`.
Downloaded ZIP1053 bytes SHA256
`de7cc961a2d5164d0d2c9b0dfce18349bbf60ea2b9886ebbd74aff8837776c73`,
both verified independently. Current report also checked against committed
bytes by Actions. Original source code and proprietary assets never committed.

## Correction of previous search boundary

The accepted preceding PET compile audit scanned `server/gmsv` recursively:
it correctly found Bismarck's `CHAR_movePetItem` definition and **zero direct
call sites *within that subtree***. It never established that the complete
server tree had no callers. This new gate scans the complete pinned `server/`
C source tree including the separately built `server/common` library.

It finds a complete **conditional source chain**:

1. `common/gmsv_server_send.c:1388`: opcode
   `LSSPROTO_PET_ITEM_RECV` branch calls
   `GmsvServer_PETITEM_recv`, under `#ifdef _PET_ITEM`.
2. `common/gmsv_server_recv.c:985`: original
   `GmsvServer_PETITEM_recv` definition, under `#ifdef _PET_ITEM`.
   Its line1010 calls `CHAR_movePetItem` following game/trade-state guards.
3. `gmsv/char/char_item.c:2655`: `CHAR_movePetItem` definition
   also under `#ifdef _PET_ITEM`, using a PET/player physical-global-item-index
   exchange.

In the checked-in default make/header compile configuration, native GCC
preprocessing excludes all three branches; the ordinary
`GmsvServer_MI_recv` -> `CHAR_moveEquipItem` path still exists.
Controlled `-D_PET_ITEM` on the **same pinned sources** reveals all three
optional parts. This establishes **source capability and compiler gate**;
it does not verify any deployed server option or any client sending the
optional opcode.

## Exact evidence rules

- Pin original `server/common/makefile`, `gmsv_server_send.c`,
  `gmsv_server_recv.c` and `server/gmsv/char/char_item.c` to their Git
  blobs and verify the known original commit. Common makefile must include
  both protocol C files and the GMSV include path.
- Require default-vs-forced GCC preprocessor results for opcode decoder,
  handler and equipment body; forbid natural runtime or first-release
  promotion in receipt rows.
- Include complete, ordered `server/`-wide C call-site inventory, no raw
  source code. Negative tests reject tampering, omissions, duplicate
  records, wrong counts and false production/early claims.
- Preserve the preceding narrower report and clearly supersede **only**
  the mistaken broad inference; no silent historical evidence rewrite.

## OPEN and DESIGN boundary

Neither a genuine game client packet nor deployed compile flags are in
this proof. It is possible the code remained disabled in the checked-in
default and could have been enabled in other builds, but no such build is
verified. In-game PET inventory ownership/release, natural stale alias,
unique-code generation timing, and JSS1999/Taiwan1.0 equivalence remain
OPEN. No modern single-player item architecture decision is made.

Pressure remains 2486 = 2465 bounded closed + 18 OPEN + 3 historical UB.
Next: connect a proven enabled source/binary configuration with authentic
client protocol/opcode emission before attempting non-synthetic native
owner/unique-code lifecycle experiments.
