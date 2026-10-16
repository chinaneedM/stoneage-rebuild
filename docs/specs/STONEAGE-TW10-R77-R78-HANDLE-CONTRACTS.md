# TW1.0 R77/R78 bounded handle-table return contracts

Status: original-static syntax and conditional contracts only. Stage A families
remain PARTIAL/OPEN; Stage B remains gated. No original program/API or savedata
payload was executed or archived.

R77 refreshes the exact156-report corpus at main
`b49c0d81ad17dc8c5f691e505a9ca817df2a625d`. The registered six entry address
keys, eight root keys and three operand-array keys have no decoded entry for
0x4e8fb or0x4c953. The former has13 numeric references/no root objects; the
latter28 references/three root objects. These bounded representation results
are not absence claims about every possible retained encoding. Existing R75
already pins the direct caller0x4c78e; only its material handle-source callee
0x4e8fb is acquired. No descendant callee or0x4c953 is expanded.

The original-static producer authenticates the runtime SHA256 and exactly
reproduces R75 and inherited source chain before deriving16 nodes/16 edges,
no frontier/cap and no CALL. Only derived instruction/operand metadata enters
Git. Independent source/job/artifact ZIP/raw/canonical custody is retained in
the R77 receipt. The original archive is transient and purged by CI.

| Site | FACT: retained instruction spelling | Conditional interpretation |
|---|---|---|
|0x4e8fb|MOV EAX,[ESP+4]|first stack word under normal dword near-call geometry|
|0x4e8ff /0x4e905|CMP EAX,global24254560 / JAE|unsigned range guard; no original bound value known|
|0x4e909 /0x4e90c|AND EAX,31 / SAR ECX,5|slot and signed bucket arithmetic|
|0x4e90f|MOV ECX,[global24254304+ECX*4]|table pointer read, content/validity unknown|
|0x4e916|TEST byte[ECX+EAX*8+4],1|bit-value1 guard; no historical flag name assigned|
|0x4e91b /0x4e91e|LEA EAX,[ECX+EAX*8] / JE|LEA preserves the prior TEST flags|
|0x4e920 /0x4e922|MOV EAX,[EAX] / RET|dword table-entry return, not proven valid OS handle|
|0x4e923 /0x4e92a /0x4e934|AND global24252940,0 / MOV global24252936,9 / OR EAX,0xffffffff|failure-shaped local stores and allones result; historical error names unassigned|

R78 qualifies every listed width/base/index/scale/offset/literal and exact
topology. Only EAX, ECX, flags and RET's ESP appear in decoder write lists;
EBP/EBX/ESI/EDI/EDX have no local explicit write and no descendant-call barrier.
There are exactly two explicit memory stores, on the failure-shaped arm.
This local syntactic fact does not establish valid memory, nonaliasing,
exception-free execution or immunity from concurrent/external writes.

Forward and separately authored reverse source traversals agree at both RETs.
The table-read arm's EAX source is0x4e920; the other RET's source is0x4e934.
Two arithmetic descriptions agree on4104 invented words, including signed
and wrap boundaries;256 invented byte cases check the bit-value1 predicate.
No original scalar/table/save value enters those examples. In particular,
SAR on0x80000000 gives a negative bucket; do not silently replace it by SHR,
or assume the unsigned range test proves a positive input without the bound.

R75's PUSH EAX supplies this helper's[ESP+4] only under normal near-call,
valid-stack and nonaliasing premises. The caller compares EAX with-1 and
routes non-allones results to the qualified SetFilePointer suffix. Under the
remaining R76 API/ABI premises this connects the handle-shaped argument to
the table dword. It proves neither the actual table value nor a valid handle,
historical helper name, realized path, seek position/success or persistence.
Matching table-base/index syntax is not matching temporal memory snapshots.

Highest NEXT R79: reuse retained caller/table evidence, then qualify only
material0x4c953 error-helper effects on the nonzero-error/allones return route.
Refresh the retained-first gap before any acquisition. Keep ABI/cleanup,
nonaliasing, global/table stability, actual handles/count/seek results,
flush/close/disk persistence and original schema/version/checksum/migration/
server authority OPEN. Do not turn this into generic CRT/helper exhaustion.
