# Taiwan 1.0 R63 — Original client narrowly targeted WriteFile postcall operand probe

**Status:** New original-static probe implementation, not a native persistence certificate. This probe exists only because the accepted R62 census found no complete decoded instruction-and-operands rows for both postcall RVAs across the 32 retained R27–R58 reports. It does not conclude historical behavior from their absence.

## Exact scope

Use the already authenticated freely retrievable TW1.0 archive through the existing bounded parallel-download utility in a disposable CI runner. Verify extracted `sa_3.exe` SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`. Decode the accepted R28 root `0x4c5b4` only (139 nodes, 156 edges); require both `KERNEL32.dll!WriteFile` import slot associations at `0x4c68c` and `0x4c6f1`, IAT `0x520a4`. Extract bounded non-byte instruction/operand rows in small address windows at those call sites and their conditional continuations `0x4c692` and `0x4c6f7`, with only local static graph edges.

No runtime code is executed. No original executable bytes, original save payload, game assets or whole-file original archive are uploaded. Original input files are purged even when a CI step fails. Derived JSON alone may be uploaded after successful source and synthetic checks.

## Proof boundary

The presence of a decoded original `cmp`, `test`, `jne` or arithmetic instruction does not prove that an original branch was taken, the Windows API ran, a caller/callee register was preserved, a written-byte-count pointer was valid or any bytes were persisted. `EAX` remains an opaque native return until a separate source/ABI/value analysis qualifies it. Stage A systems remain PARTIAL/OPEN; Stage B new-game design remains gated.

## Acceptance order

First independently run the synthetic safety suite. Then obtain an authenticated CI-produced **derived-only** original-static report and verify source custody, exact operands, the root CFG, non-promotion flags and path/scope constraints before adding the report as canonically accepted evidence. Until source CI and independent evidence receipt succeed, this commit proves the bounded analyzer and workflow only, not any original instruction mnemonic at the postcall sites.
