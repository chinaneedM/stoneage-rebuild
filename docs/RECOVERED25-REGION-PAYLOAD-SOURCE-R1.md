# Recovered25 Region Payload Source R1

## Purpose

This layer supplies actual recovered map planes behind the engine-neutral world-profile interface.

It preserves format boundaries instead of inventing one historical file format.

## Source split

The closed 826-floor materializable runtime world is composed as:

- **761 stable floors** — recovered client DAT payloads with three uint16 planes:
  - tile;
  - object/parts;
  - event.
- **65 resolved supplemental floors** — recovered server LS2MAP payloads with two uint16 planes:
  - tile;
  - object.

The unresolved floor-130 version fork remains excluded from the default 826-floor profile.

## Critical event-layer rule

Server LS2MAP does **not** carry the client DAT event plane.

Therefore supplemental region output uses:

- `event_ids = None`;
- `event_plane_status = ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE`.

It is forbidden to synthesize an all-zero event plane merely to make the arrays look uniform.

NPCs, WarpMan, encounters and other event/world semantics remain separate authoritative runtime data and can later be projected into engine-facing interaction layers.

## Validation

Every payload is checked against the already committed materializable manifest:

- floor identity;
- dimensions;
- SHA-256;
- source class;
- `LATER_RECOVERED` provenance.

No raw tile/object/event plane is committed by the validation workflow.

## Engine-neutral region record

`EngineNeutralMapRegion` returns an inclusive rectangular slice with row-major:

- `tile_ids`;
- `object_ids`;
- optional `event_ids`;
- source kind;
- event-plane status;
- source payload SHA-256.

This is the concrete payload layer that the future renderer/pathing adapter can consume without knowing DAT/LS2MAP file layouts.

## Historical boundary

This source does not establish Taiwan-v1 membership for any recovered25 map.

Taiwan-v1 direct evidence proves the runtime map-materialization mechanism. Concrete recovered25 payload membership remains `LATER_RECOVERED`.
