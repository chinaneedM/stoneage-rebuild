# TW1.0 R16 original bounded helper and third global reference frontier

**Evidence status:** ORIGINAL-DERIVED CONDITIONAL STATIC; every named callee
effect, native save and runtime initialization is still OPEN.

Original probe run `38251469650`, job `114818598926`, source commit
`309ac5bcc268b5b5d3efeabc257f32ea8f8e1208`, SUCCESS.
The historical archive was retrieved and checked transitively against R15/
earlier original SHA256 gates, analyzed without executing the original,
then purged. Derived-only artifact `11748211374` ZIP SHA256
`6327e33046dc3cb7b578bd711a6be93cff3e5e322f7aa885d9a980fe10575461`.
Inside JSON 4,710 bytes, SHA256
`a17655952b1d9310283c97ab53e689bd0b2c8a07935b0655dac04a65b7f132ca`.

## Callee-specific bounded static effects

The same exact original direct callee `0x484c0` is targeted by two global
write-context CALLs `0x49444` and `0x4945d`. The R8 conservative effect
model visits **five states**, finds an **unsupported_memory** gap at
`0x484c7`, and reaches **zero qualified returns**. No callable effect summary
exists, so neither register value, ownership nor caller state can be promoted.

Other original R15 direct CALL targets were independently sampled:

| Callee | States | Unresolved frontier | Return qualified |
|---|---:|---|---|
| `0x49900` | 5 | nested CALL `0x49909→0x4e2a8`, `0x49912→0x4e2e1` | No |
| `0x4a09c` | 21 | two unsummarized indirect CALLs at `0x4a0c4` and `0x4a0f8` | No |
| `0x4a14d` | 22 | alias write `0x4a17d`; modeled CFG cycle | No |

This is syntax under separate state caps (144/80/80/80), not evidence of a
complete function CFG, ABI, executed path, runtime return values or native IO.

## Third virtual-global original reference candidates

New global `0x172186c`, identified in R15 as the load input to EAX at
`0x49de3`, has a **linear .text candidate universe** of 331,776 original
bytes, 104,229 decoded instructions and 8 decoder-gap bytes. Four direct
references were found without sample truncation:

| Site | Exact static classification |
|---|---|
| `0x49a2c` | write candidate |
| `0x49d78` | write candidate |
| `0x49de3` | read candidate |
| `0x49e88` | write candidate |

There are three write candidates and one read candidate, no immediate
address candidates and no unknown-class direct references in this bounded
scan. This **does not** exhaust indirect aliases, establish feasible executed
writes, prove initialized global contents or identify a save-data object.

**Next R17:** recover exact opcode-class/value-source/branch/frame geometry
of global `0x172186c` write candidates `0x49a2c`, `0x49d78`, `0x49e88`.
Separately examine callee `0x484c0` unsupported-memory operation at
`0x484c7` for named address/ownership and possible callee semantics, and
the two nested 0x49900 targets. Do not permit wrapper/caller continuation
unless the exact effects and path qualifications have independent original
evidence. Original filename→CreateFileA, handle→ReadFile/WriteFile, fixed
128-byte save fields, framing/checksum/migrations/cross-profile semantics
remain OPEN. Continue historical restoration before new-game design.
