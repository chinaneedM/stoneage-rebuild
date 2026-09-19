# Taiwan v1.0 Receive Dispatcher and Map-Protocol Lineage — R1

Date: 2026-09-19

## Scope

This record closes the accepted Taiwan Waei/JSS StoneAge v1.0 runtime's incoming network-to-protocol path and the first map-protocol-to-local-cache paths.

Primary evidence is the verified Taiwan retail binary. A later preserved StoneAge source tree is used only as a lineage/control corpus after its structural predictions are independently reproduced in v1.0 bytes.

## Artifact anchor

- Retail disc: Redump 104630
- Disc track SHA1: `d0f270163772eb587185a65e24a3f7e565263f2f`
- Runtime: `StoneAge/sa_3.exe`
- Runtime SHA1: `f3999d1331374abe60c1a11a70c08bc9108d6873`
- Image base: `0x400000`
- Derived report: `research/recovered/STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt`

## Incoming receive chain

The v1.0 PE has a WSOCK32 `recv` IAT entry at RVA `0x5224c`.

The exact linker thunk is `0x48472`, and the runtime has one business caller:

- `0x2ea8a -> 0x48472 -> WSOCK32 recv`

The same network path has one direct call to protocol dispatcher root `0x19730`:

- callsite `0x2eae3 -> 0x19730`

A deep direct-call graph rooted at the receive call reaches `0x19730` at depth 2.

## Dispatcher identity

`0x19730` is not identified merely because it falls near protocol code. Its own binary structure fingerprints the generated string dispatcher:

- one direct caller, `0x2eae3`;
- opening calls to `0x1b010`, `0x1b300`, and `0x1afb0`;
- exact protocol-name references in its dispatch region including `EV`, `EN`, `RS`, and `RD`;
- downstream contiguous protocol cases include the recovered login/character and map cases.

This closes:

`WSOCK32 recv -> network receive path -> v1.0 string protocol dispatcher`.

## Login/character receive branches

The six previously known mov-side name references resolve to the following receive callbacks:

| Protocol | mov-side case | Terminal callback |
| --- | ---: | ---: |
| ClientLogin | `0x1a6d5` | `0x2f200` |
| CreateNewChar | `0x1a751` | `0x31e90` |
| CharDelete | `0x1a7f6` | `0x31f90` |
| CharLogin | `0x1a89b` | `0x2f530` |
| CharList | `0x1a940` | `0x2f320` |
| CharLogout | `0x1a9e5` | `0x2f610` |

The branches share `0x1b140` and `0x1b4c0`.

Binary behavior of `0x1b140` handles a null input through common escape-work globals and otherwise follows the de-escape path. `0x1b4c0` passes three arguments into the common safe-copy helper and returns the copy address. These independently reproduce the roles later named `lssproto_demkstr_string` and `lssproto_wrapStringAddr`.

## Integer decoder

The map cases add a third receive-side helper:

- `0x1b120`

The v1.0 `MC` branch calls it exactly eight times before the string decode/copy pair.
The v1.0 `M` branch calls it exactly five times.

Those counts match the independently observed field structures:

- `MC`: `fl, x1, y1, x2, y2, tilesum, objsum, eventsum, data`
- `M`: `fl, x1, y1, x2, y2, data`

This identifies `0x1b120` as the v1.0 integer decoder equivalent.

## Map protocol dispatch

Exact v1.0 receive cases:

### MC

- protocol-name mov xref: `0x19e2e`
- 8 integer decodes via `0x1b120`
- 1 string decode via `0x1b140`
- 1 string copy/wrap via `0x1b4c0`
- terminal callback: `0x30d20`

### M

- protocol-name mov xref: `0x19f54`
- 5 integer decodes via `0x1b120`
- 1 string decode via `0x1b140`
- 1 string copy/wrap via `0x1b4c0`
- terminal callback: `0x30ef0`

## M -> writable map-cache path

Starting from v1.0 callback `0x30ef0`, the bounded call graph reaches node `0x1da40` at depth 3.

That node:

- contains exact pooled-string reference `map\\%d.dat` at `0x1da50`;
- references file modes `rb+`, `wb`, and `rb+`;
- is therefore directly proven to operate a writable/update map-cache file path.

The later control source predicts that protocol `M` parses tile/parts/event rectangles and writes them into the persistent three-plane map cache. The v1.0 binary independently reproduces the protocol parameter shape and reaches the writable `map\\%d.dat` path, so the **M -> local map update** role is established without importing later addresses as evidence.

## MC -> read/check map-cache path

Starting from callback `0x30d20`, the bounded call graph reaches node `0x1dd90` at depth 4.

That node:

- contains exact `map\\%d.dat` reference `0x1dda0`;
- references file modes `rb`, `wb`, and `rb`;
- therefore belongs to a read/check path with a create-if-missing fallback rather than the M writable-update path.

The later control source predicts that `MC` carries map checksums and invokes map-check logic. The v1.0 binary independently establishes the distinct read/check-shaped file path; the exact v1.0 symbolic function name remains unclaimed.

## Closed chain

The binary-supported map data path is now:

`WSOCK32 recv 0x2ea8a -> dispatcher 0x19730 -> M case 0x19f54 -> callback 0x30ef0 -> writable map function 0x1da40 -> map\\%d.dat`

The parallel map-control path is:

`WSOCK32 recv -> dispatcher 0x19730 -> MC case 0x19e2e -> callback 0x30d20 -> read/check map function 0x1dd90 -> map\\%d.dat`

## Evidence boundary

Established directly from v1.0 bytes:

- unique business `recv` call and dispatcher caller;
- dispatcher root and exact protocol-name fingerprints;
- receive-side branch call counts/order and callback RVAs;
- `MC` / `M` field-conversion counts;
- callback-to-map-file call-graph joins;
- writable versus read/check file-mode distinction.

Lineage-control interpretation, not independent historical naming:

- later symbolic function names for receive helpers;
- later names `writeMap` / `mapCheckSum`;
- exact later data-structure implementation details beyond what v1.0 bytes reproduce.

Still OPEN:

- roles of exact `map\\%d.dat` xrefs `0x1d846`, `0x21306`, `0x21721`, and `0x218fe`;
- exact semantic name for every intermediate callback/helper;
- server endpoint source and selection chain;
- server-side logic absent from the retail client.

## Descendant source control

Repository: `BismarckDD/stoneage`
Pinned commit: `999ffdf1d220ec6666eb65339180689c9caf1876`

Relevant files:

- `client/stoneage/proto/lssproto_cli.cpp`
- `client/stoneage/proto/lssproto_util.cpp`
- `client/stoneage/system/netmain.cpp`
- `client/stoneage/system/netproc.cpp`
- `client/stoneage/system/map.cpp`

The descendant tree is a control corpus only. Taiwan v1.0 retail bytes remain the primary evidence.
