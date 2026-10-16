# TW1.0 R75/R76 — Local helper effects and conditional seek contracts

Stage A original-static metadata and invented symbolic stack labels only.
Original executables, APIs and savedata payloads are never executed/evaluated.

## Retained-first source scope

Fresh main15923c8bccb0c9d89c62300591f97d1ab5f2fd17/tree
24edaa9f53cb5cbade487ea3fc279cf1c1d48a49 contains150 savedata JSON reports.
R46 already retains the0x4c761 entry, three decoded rows,51-node/55-edge graph,
physical stack suffix and SetFilePointer import identity; R37 retains the same
helper surface. The refreshed150-report census preserves that entry rather
than declaring it absent, with48 missing rows in six registered address-key /
three operand-array-key representations.

To inventory every possible local nonvolatile-register/stack restore, memory
store, RET and controlling branch, R75 decodes the complete **already bounded
51-node helper**. It does not expand any of its four descendant callees.
Runtime SHA256cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a
and exact original R73 reproduction are required. Recovered graph and complete
R46/R37 call/memory surfaces match; the three retained operand overlaps agree.
No original savedata payload is opened by this acquisition.

Source Action38888448211 atb3d92a453bcb0a093ed36417db3588bd691c0811:
synthetic116931835622(48 tests), original-static116931879732,
independent-archive116932146715. Derived-only artifact12040258731 ZIP2743 bytes,
SHA2564cd9097e869802b8bd107f737ac68183c78f42f7a4b9b75a6a639adc3d6e069f;
sole25435-byte report SHA256bcec13f8eb8d0b6182a38aa8b0ba67a7f20ca1d9b33ca1c9a76a1448f62b7d85,
Git blob757c22945d7e18263b154e88f52376d0ab58d42c. Independent local ZIP/raw/Git
comparison passes. Canonical archive97d2e781959c2d86a3840020292e2146cebb286b/tree
d8d9f7f66bb8174df2b07563d58af49cc641bacb preserves only metadata/custody;
independent review must be triggered separately from bot archival.

## Qualified facts and conditional interpretation

| Sites | Static FACT | Boundary |
|---|---|---|
|0x4c765/0x4c76c/0x4c76d and0x4c7f7..0x4c7fa|PUSH EBX/ESI/EDI; shared POP EDI/ESI/EBX; near RET|saved-slot integrity and intervening call cleanup are not automatic|
|0x4c78e|direct CALL0x4e8fb, followed by POP ECX after CMP|handle-shaped EAX result and actual callee effects remain opaque|
|0x4c7a5..0x4c7b0|PUSH[ESP+24], PUSH0, PUSH[ESP+28], PUSH EAX; imported SetFilePointer|physical binding depends on explicit stack premises|
|0x4c7b6..0x4c7c9|preserve EAX-shaped return in EBX; compare with-1; conditional GetLastError; TEST/JE|EBX preservation across the extra call remains unproven|
|0x4c7d6|AND byte[EAX+ESI+4],253|local bit2 clear; address identity and other callee writes remain unknown|

The graph has seven structural root-to-RET paths. They overapproximate feasible
execution: a path taking a nonzero TEST result after local XOR-zero is not
claimed feasible. A symbolic ledger with invented entry-register/stack labels
checks all seven paths, plus separately written scalar PUSH/POP/call-cleanup
accounting. Under declared returning-call cleanups0/16/0/0, valid x86 dword
stack geometry and no overwrite of saved slots/arguments by aliases or callees,
all paths restore the three saved tokens and return-address slot. Wrong cleanup
or a saved-slot clobber breaks that result in adverse controls. This is a
conditional local restoration contract, not actual ABI preservation.

There is no explicit local EBP write; calls still kill EBP knowledge. Strict
forward/reverse queries preserve opaque EBP, table-pointer/ESI, and intermediate
EBX dependencies. Caller/helper table-address identity and actual register
values are not admitted. A256-value invented byte model confirms AND253 clears
bit2 and leaves masks32/128 unchanged **for that local operation only**. It does
not prove a stable historical table byte across the helper.

Under the caller's qualified zero-EDI/PUSH2/PUSH EDI/PUSH ECX route and the
explicit stack premises, the four physical native argument tokens reconcile:

| Documented argument role | Conditional token |
|---|---|
|hFile|opaque EAX result from0x4e8fb|
|lDistanceToMove|0|
|lpDistanceToMoveHigh|NULL-shaped0|
|dwMoveMethod|2|

Microsoft's current API reference defines method2 as FILE_END; with zero
distance, this is a request to position at the current EOF of a valid seekable
file. Its x86 __stdcall reference supplies right-to-left argument order and
callee argument cleanup. These references support a **conditional API/ABI
interpretation**, not a claim that the original client used that convention
correctly, reached the call, had a valid handle, moved the pointer or persisted
bytes. Historical mode-mask names remain unproven.

Primary contract references, accessed2026-10-16:
- https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfilepointer
- https://learn.microsoft.com/en-us/cpp/cpp/stdcall?view=msvc-170

Highest NEXT R77: retained-first evidence for0x4e8fb handle-source and
caller-visible effects, and0x4c953 only where required by error/helper paths.
Preserve ABI/cleanup, saved-slot nonaliasing, table-address and actual native
position/count/persistence boundaries. Stage A families PARTIAL/OPEN; Stage B
gated. No production-game architecture/design change.
