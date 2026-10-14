# TW1.0 R37 — continuation helper and descriptor/handle candidate bridge

Status: READY after R36 independent original acceptance. No R37 original FACT admitted.

R36 finds the JNE direct target 0x4ed33 and three bounded continuation MOV-to-memory candidates (0x4ed5f AL, 0x4ed72 AL, 0x4ed92 EAX). AL is a low-byte projection with separate conservative EAX provenance, not a full 32-bit stored value. All destination addresses, alias ownership and original values remain unknown. EAX at the last store is an opaque CALL source at 0x4ed87, syntactically targeting 0x4c761.

Highest task: inspect original CALL 0x4ed49 -> 0x4e80a and CALL 0x4ed87 -> 0x4c761 on this continuation, with bounded pre-call PUSH/register geometry, exact direct target/boundary evidence and independent immutable original derivative custody. Qualify partial-register definitions 0x4ed57/0x4ed59/0x4ed69 (currently unmodeled whole-register writes), and trace source and destination address candidates for the three stores and any qualified helper entry stack/memory shapes. The parent later contains CALL 0x4edb0 -> 0x4a8dc (the accepted ReadFile candidate context); retain it as discovery rather than a demonstrated native-save route.

Never infer WINAPI/CRT ABI, nonvolatile ESI preservation, descriptor or successful handle identity, table initialization or alias ownership from names and numeric proximity. Keep actual filename → CreateFileA-result → ReadFile/WriteFile handle/buffer/length128, native framing/checksum/schema/persistence, server authority and cross-version equivalence OPEN. Original executable/media remain transient, unexecuted and unpublished; only bounded derived metadata may enter the repository. Stage A restoration first.
