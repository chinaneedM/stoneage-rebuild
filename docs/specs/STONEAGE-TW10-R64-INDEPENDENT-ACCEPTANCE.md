# Taiwan 1.0 R64 — Independent original-derived TEST and physical count-slot acceptance

Source acceptance is **bounded original-static syntax only**. Requalify R63 raw JSON SHA256 `91b650db700cf892a7d8c8b2d36a9d49dbeca139be315856d31d59533056c1bd` from its immutable source Action; cross-check R28 original-derived Git blob `3671661219120d45bd922e05b6df371523b42432`. Independently validate R64 artifact custody and exact replay.

Both `0x4c692` and `0x4c6f7` decode `TEST EAX,EAX`; first immediate conditionals at `0x4c694` and `0x4c6f9` are `JE`. The first branch has only one target **inside** the R63 48-byte postcall window; the second has two. The other first-branch target remains **out of scope** and must not be invented or interpreted as unreachable.

Five physical PUSH spellings per call reconcile with R28. The slot at conditional pre-CALL ESP+12 can only be a *candidate* `lpNumberOfBytesWritten` under Win32 x86 stdcall and valid caller frame/preservation assumptions; original register value, pointer, native bytes and resulting disk persistence are unproven. The native BOOL-shaped EAX register return is a separate channel from memory output count.

This independent verifier is not permission to close native I/O, original savedata format, checksum/version/migration, server authority or any Stage A family. Stage B remains blocked until recovery review.
