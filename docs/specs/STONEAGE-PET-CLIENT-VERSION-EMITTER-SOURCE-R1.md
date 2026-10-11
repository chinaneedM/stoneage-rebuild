# PET client version macro and optional packet emitter — pinned source orientation R1

Status: **SOURCE_ONLY_PINNED_HEADER_EMITTER_ORIENTATION** (not a runtime acceptance; not a deployed client/server proof).

## Question

After the late Bismarck server-side optional `LSSPROTO_PET_ITEM_RECV` -> `GmsvServer_PETITEM_recv` -> `CHAR_movePetItem` chain was established under `_PET_ITEM`, determine what the **client-side pinned source** actually establishes about compile selection, packet number and emitter. Do not infer a user-triggered packet from a sender definition.

## Bounded primary technical evidence

The following observations were directly checked by seven read-only structural assertions against exact files in late-descendant repository `BismarckDD/Stoneage`, commit `999ffdf1d220ec6666eb65339180689c9caf1876`:

| Pinned file | Git blob SHA | Observation |
| --- | --- | --- |
| `client/resources/version.h` | `35bd4446a740a189c1ad9439e30e61fe169d5f46` | Line 8 selects `_SA_VERSION_25` in the checked-in header. Lines 439–443 define `_PET_ITEM` **inside** `#ifdef _SA_VERSION_80`; the raw presence of the define is not default enablement. |
| `client/stoneage/proto/protocol.h` | `bb70087ef1b1915748da23935584eda2c8178cb0` | Gated client packet constant `LSSPROTO_PET_ITEM_EQUIP_SEND = 127` and declaration of `lssproto_PetItemEquip_send`. |
| `client/stoneage/proto/protocol.cpp` | `17f1900d8845c15308a4b429905ec009e5fd4c0f` | Lines 2278–2294 guard a sender definition under `_PET_ITEM`; its five arguments plus checksum are serialized and passed to `util_SendMesg(fd, LSSPROTO_PET_ITEM_EQUIP_SEND, szBuffer)`. |
| `server/common/gmsv_server.h` | `708fe1b9f73be4952677fda474f10e86d9a56306` | Conditional `LSSPROTO_PET_ITEM_RECV = 127`, numerically consistent with the client-side optional sender. |
| `server/gmsv/include/version.h` | `b3fc0c80705973bc8d088287c98a5d66171bb6c2` | No direct `#define _PET_ITEM` in this pinned server version header; existing server-default preprocessing gate is recorded separately. |

These are source-only late-descendant statements. Header selection is not an exhaustive effective macro inventory for an externally overridden build. `_SA_VERSION_80` could be supplied by an alternate build or config; no such production invocation has been established. The client header's checked-in `_SA_VERSION_25` selection by itself does **not** enable the version-8 PET feature. Its `_PET_ITEM` define cannot be cited as an unconditional default client/server macro mismatch.

## What remains OPEN

1. **Full pinned-client caller inventory:** a search of the currently indexed descendant `master` surfaced the emitter declaration and definition, but is not an exhaustive scan of the **pinned commit**. Scan all pinned client C/C++ and generated/build routes for any invocation of `lssproto_PetItemEquip_send`; separate definition, prototype, UI call, indirect call and generated callback.
2. **Real compiled configurations:** run a pinned-client header/preprocessor experiment for checked-in selection and a clearly counterfactual `_SA_VERSION_80` setting; inspect the actual project/IDE compile definitions and include order. Match to a separately certified server `_PET_ITEM` build. No historical deployment conclusion from feature-toggle probes.
3. **Authentic request path:** demonstrate actual UI/keyboard/item drag-drop action -> emitted opcode 127 -> enabled server decoder/handler -> PET slot/item owner transition, preserving negative guards and source provenance. A sender implementation alone is insufficient.
4. **Original-version boundary:** source is from a late derivative, not JSS 1999 or Taiwan/Waei 1.0. No natural PET carrying alias, unique-code identity, first-release feature membership or design requirement is promoted.

Previous bounded source gate: `docs/specs/STONEAGE-PET-ITEM-PROTOCOL-CROSSMODULE-R1.md`. This note **extends** the client side and **does not supersede** its server-side findings.

Historical pressure unchanged: 2486 = 2465 bounded closed + 18 OPEN + 3 historical UB; **zero** promotion to early history. No proprietary client/server files or assets are committed.

Receipt: `research/recovered/STONEAGE-PET-CLIENT-VERSION-EMITTER-SOURCE-R1.json`.

Highest NEXT: perform a full pinned-client source tree and build-configuration audit, including actual callers (not simply definitions), then a source-only compile matrix and, only if justified, a bounded native/original dispatch witness.
