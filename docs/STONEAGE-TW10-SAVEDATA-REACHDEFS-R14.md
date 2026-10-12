# TW1.0 R14 bounded reaching register definitions (original-only evidence)

**Status:** independently guarded static evidence candidate; it is neither a
qualified helper effect nor evidence of original executed native persistence.
See the R14 source workflow and strict custody workflow for acceptance.

- Source pinned original run: `38247625998`, commit
  `1b4c039f5a9b82b7bf58d59b1ef187ac0f97c678`.
- Derived-only artifact ID `11745719771`, zipped SHA256
  `8d7a3e0f332f09103c79965519e42475d344b241863bdd461dc9dce2185976c4`.
- Inner 3,026-byte derived JSON SHA256
  `c2111943e99c1ba0b44792434cfa8060fd4c8d4726fc22b778cf6db808434af9`.
- Prior R13 hash gates and verified original client/archive identity were
  rechecked before R14, using only temporary original binary extraction. The
  repository includes **no proprietary original binary**.

## Exactly bounded findings

At helper write **0x49dec**, EBX reaches a local 32-bit **copy from EAX** at
**0x49de8** in a 139-node/158-edge graph anchored at 0x49d93. This is one
immediate reaching-register definition, **not** a known EAX value or evidence
that the EBP+8 write belongs to a particular caller object. The graph has 27
branch sites, two opaque CALL barriers and three external edges, so its anchor
is not a proved whole-function entry or complete CFG.

At globals in the 48-node/53-edge graph anchored at 0x4943c:

| Write | Source register | Conservatively reaching source |
| --- | --- | --- |
| 0x4943c | EAX | Entry-origin UNKNOWN at 0x4943c |
| 0x4944a | EAX | Opaque CALL barrier at 0x49444 |
| 0x49457 | ESI | Opaque CALL barrier at 0x49444 |
| 0x49463 | EAX | Opaque CALL barrier at 0x4945d |

The graph has six branch sites and three opaque CALL sites. Its empty
**out-of-window frontier** does not prove the graph starts at the actual
function entry or that the original caller reaches each site. All CALL
fallthroughs are strictly structural return assumptions. No ABI-preserved
registers, call summaries or branch outcomes were guessed.

**Next original R15 frontier:** bound the EAX register provenance upstream of
0x49de8; identify exact EBP/ESP establishment, enclosing function entries and
external incoming edges; independently summarize the intervening 0x49444 and
0x4945d CALLs before any global-value/path promotion. Then pursue actual
filename/handle/ReadFile/WriteFile buffering and native-save framing only when
supported by original evidence. All original native IO, 128-byte schema,
checksum, runtime global initialization, object ownership and named effect
admissions remain OPEN.
