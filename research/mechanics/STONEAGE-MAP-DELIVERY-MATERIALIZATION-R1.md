# StoneAge field-map delivery and runtime materialization closure — R1

Date: 2026-09-29

## Scope

This note closes the narrow question raised by the recovered classic-warp audit: how can a classic client enter a floor when no pre-existing client field-map DAT/MAP payload is present, while a server map exists?

It separates **Taiwan-v1 direct evidence**, **fixed-descendant control evidence**, **later recovered concrete content**, and **single-player design**. The mechanism does not promote any recovered-2.5 floor into Taiwan-v1 historical membership.

## FACT — accepted Taiwan v1.0 runtime supports demand-filled field-map cache

Direct evidence already preserved in this repository establishes all of the following for the accepted Taiwan/Waei v1.0 runtime:

- the accepted retail disc contains zero ordinary field-map/cache files;
- the runtime uses the local path `map\\%d.dat` and has create/read/write/update paths for that cache;
- client-to-server protocol `M` has five integer fields representing a floor and rectangle;
- server-to-client `M` has five integers plus one string payload;
- server-to-client `MC` has eight integers plus one string, adding tile/object/event checksum/control values;
- the `M` receive path reaches the writable map-cache routine;
- the `MC` receive path reaches the read/check path, including a create-if-missing route.

The direct v1 boundary therefore supports:

`local cache absent/stale -> rectangle check/request -> map payload receive -> local cache materialization`.

Evidence:
- `research/clients/STONEAGE-TW10-RECEIVE-MAP-LINEAGE-R1.md`
- `research/recovered/STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt`
- `research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md`
- `research/clients/STONEAGE-TW10-GAMEPLAY-DATA-MATRIX-R1.md`
- `research/recovered/STONEAGE-TW10-GAMEPLAY-PROTOCOL-R1.txt`

## CONTROL — pinned descendant exposes the server half of the same semantic loop

Pinned control source: `BismarckDD/Stoneage@999ffdf1d220ec6666eb65339180689c9caf1876`.

The descendant is **not** launch-era proof. It is used here only to explain a mechanism whose client-side shape is already direct in Taiwan v1.

Observed control chain:

1. `GmsvServer_M_recv(fd, fl, x1, y1, x2, y2)` receives the five-field map rectangle request.
2. It calls `MAP_getdataFromRECT(fl, ...)`.
3. `MAP_getdataFromRECT` reads the server's authoritative map record for that floor, clips the requested rectangle, serializes the map display string plus tile, object and event planes, and returns the payload.
4. `GmsvServer_M_send` sends the clipped rectangle plus the serialized payload.
5. On the client side, `lssproto_M_recv` decodes the tile/object/event planes and calls `writeMap(fl, x1, y1, x2, y2, ...)`.
6. The descendant server's around-character path computes `MAP_getChecksumFromRECT` and sends `MC`; the descendant client compares that region with its cache. A mismatch calls client `lssproto_M_send` for the same rectangle.
7. While walking, the server can send checksum/control information for newly exposed strips, so map cache coverage is incremental rather than requiring one monolithic preinstalled client map.

The important durable boundary is therefore **server-authoritative map state + client/runtime materialization**, not the historical socket transport itself.

## FACT — four recovered warp targets are server-only on the current later corpus

The closed payload-surface audit identifies floors:

- 20002 — server LS2MAP `jyaruga/dungeon/dan_2-00-02`, 50x100;
- 20004 — server LS2MAP `jyaruga/dungeon/dan_2-00-04`, 80x80;
- 20006 — server LS2MAP `jyaruga/dungeon/dan_2-00-06`, 80x40;
- 20009 — server LS2MAP `jyaruga/dungeon/dan_2-00-09`, 100x100.

For all four:
- recovered-2.5 client DAT is absent;
- recovered-2.5 client MAP is absent;
- recovered-2.5 server LS2MAP is present;
- the archived-2003 client DAT inventory also lacks these IDs.

This does **not** mean the floors are invalid. It means their current preserved concrete payload is server-side.

Evidence:
- `research/recovered/STONEAGE-25-OUTSIDE-STABLE-WARP-DESTINATIONS-R1.txt`
- `research/recovered/STONEAGE-25-MISSING-WARP-DESTINATION-PAYLOADS-R1.txt`
- `research/recovered/STONEAGE-HISTORICAL-MAPEXE-INVENTORY-R1.txt`

## DESIGN — single-player materialization policy

The reconstruction should preserve the historical semantic boundary without carrying obsolete transport architecture into the product.

For a concrete server-only recovered floor:

1. decode the validated server-map surface into the project's engine-neutral internal world-map representation;
2. mark the concrete content `LATER_RECOVERED` with its source version and evidence reference;
3. treat the internal local world repository as the authoritative runtime map source in single-player;
4. do **not** require sockets, LSSPROTO, account services, or a separate map server;
5. do **not** create a fake historical client DAT/MAP and do not cite a derived cache as original distribution evidence;
6. if a future compatibility/emulation harness needs a legacy `map\\%d.dat` cache, generate it only as an explicitly derived transient artifact.

This policy is compatible with DD-013: local-first deployment preserves the original authoritative-state semantics while separating deterministic game logic from historical network transport.

## Boundary

This closure proves that **server-only field-map payload is architecturally compatible with the classic map-delivery model**. It does not prove that floors 20002/20004/20006/20009 existed in Taiwan v1.0, JSS 1999, or any other earlier release. Their current content role remains `LATER_RECOVERED`.

**SERVER_AUTHORITY_RUNTIME_MAP_MATERIALIZATION_R1 = CLOSED.**
