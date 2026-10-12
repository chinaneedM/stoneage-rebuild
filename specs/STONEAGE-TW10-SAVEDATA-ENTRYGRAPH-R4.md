# Taiwan 1.0 savedata R4 — bounded PE entrypoint graph

Status: **DESIGN of a bounded static gate** pending full verified original-byte
execution. R3 is already accepted as four alternative x86-32 push-immediate
*decodings*. Neither the source file's presence in a PE .text section nor an
alternative single-instruction decode establishes a code boundary.

R4 starts from the original PE AddressOfEntryPoint and follows **only**
statically encoded control-flow in the original raw .text section. Each unique
instruction start is decoded once; direct CALL targets and CALL return paths,
conditional branch targets and fallthrough, unconditional JMP targets, and
ordinary fallthrough are traversed. RET, INT and other terminal instructions
stop paths. Indirect transfers are counted but never invented.

Limits: at most 120,000 decoded starts, 200,000 queued paths, 240,000
edges; a truncated traversal produces graph_limit_hit=true. No cross-section
control-flow, callback registration, import thunk traversal, relocations,
exception handlers, dynamic dispatch, self-modifying code, or OS execution.
Even a graph walk without hitting limits is **not complete runtime
reachability**. Conversely, observing a site on a plausible entrypoint path is
not proof that this path actually executes.

For the four R3-pinned word RVAs (0x40065, 0x400e5, 0x40116,
0x402a1), R4 first requires independently pinned sa_3.exe and savedata.dat
SHA256 and the identical single push-immediate decoding at candidate start
RVAs 0x40064, 0x400e4, 0x40115, 0x402a0. It emits counts for candidate
entrypoint-graph membership, other instruction overlap, candidate incoming
static edges, overall graph size and unresolved indirect transfers. No bytes,
operand listings, decompressed client, or original save are published.

A zero incoming edge or unseen candidate means only **not observed by this
bounded traversal**. R4 does not label a site embedded data, prove native
savedata IO, infer a 128-byte field layout/checksum, or import later Wayi
settings rules. These remain independent OPEN gates.

The original archive acquisition requires complete catalog-pinned MD5+SHA1,
valid HTTPS Archive storage path with byte-range validation, extracted BIN
size and the precise original embedded SHA256 before R4 output is considered
a candidate for acceptance. Stop without a positive verification signal if
the archive is unavailable. Store only a small derived JSON artifact after
transient copyrighted originals have been purged.
