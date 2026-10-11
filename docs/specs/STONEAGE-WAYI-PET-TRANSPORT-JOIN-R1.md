# Wayi PET transport and UI guard join R1

Status: **STATIC COMPILED CLIENT PATH**, native PET pair OPEN. Exact accepted operator-linked archive20060915184620 game UPX output921600 bytes/SHA2564193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63; packed369152 bytes/SHA2564b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38. No original code executed or committed.

## Send path and queue

PET emitter0x93c50→hub0x8fe70(+13)→encoder0x8fc10→handoff0x3e300. Handoff tests modeglobalRVA0x4205070: nonzero uses supplied buffer directly, zero calls legacy transform0x3e3d0. Conditional LF append precedes indirect callback throughglobalRVA0xbe1e8 at0x3e358. Setter0x3d9a0 first installs no-op0x3e2e0, then uses nonzero originalarg1. Initializationcall0x5ec43 supplies callbackVA0x45ed20, bufferlimit0x4000 andfdglobal0x4204e24. Thus the compiled initialization path binds the handoff to send-queue0x5ed20.

Queue checks activeglobal0x4204e1c and queuedlength+incominglength<=0x4000, appends into buffer0x4204e30, updates length0x4204e20. Calls throughIAT0xa00d0 are **VirtualProtect**, not socket sends. Later network-loopcall0x5eabb passesfd/queue/length/flags throughthunk0x94e7c→IAT0xa02b8 **WSOCK32.dll ordinal19**. Pinned pefile2024.8.26 [ordinal lookup](https://github.com/erocarrera/pefile/blob/v2024.8.26/ordlookup/wsock32.py) independently maps19 tosend. Tool retains actual ordinal separately. Limited flush argument trace assumes nonempty-queue branch; flags registerEBP remains unresolved in that window. No packet sent/captured by these tools.

## Encoding and directional IDs

Encoder0x8fc10 calls random helper, modulus99, seed permutation2413 via0x90590, bitwise complement, custom64 alphabet via0x8fed0, rotation0x906c0, complement-string0x905c0. Decoder0x8fcd0 removes terminalLF, complement-string, takes6 encoded-seed characters, custom64 decode0x8ff70, complement/permutation3142, inverse rotation0x90620. These are observed code/literal/helper structures compared with pinned autil.cpp, not a fully executed algorithm or golden wire replay. Table0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{} is not conventional Base64.

**Clientsending adds13; clientreceiving subtracts23.** Receiver0x8fda0 takes slice1 through decimal conversion0x9625e, subtracts23 at0x8fde8, searches# among20 slices and returns markerindex-2 as fieldcount. Do not infer that feeding clientformatted140 to this receiving parser is a verified PET reply. Pinned descendant127 is a clientsend definition; no separate equipment acknowledgement can be inferred from that constant.

## Receive join

Line-intake0x5ee80 scans queued bytes forLF, extracts a terminated line and handlesCR before consuming input. Mode-selection0x5eb44 checks the same0x4205070 flag: nonzero callsdispatch0x90990 at0x5eb59; zero callsold0x3c190 at0x5eb66. Dispatcherprefix callsdecoder0x8fcd0 at0x909ab, splitter0x8fb50 at0x909bd withsemicolonliteral0xdb97c, ID/end extractor0x8fda0 at0x909cc. This closes the static generic receive chain, not a particular PET inventory/update reply or server implementation.

## UI condition refinement

| Compiled route | Guards within inspected windows | Destination |
| --- | --- | --- |
| Drag/drop0x52467 | mouse releasebit4, drag!=-1, different slots,mixzero,PETwindow,selectedpet>-1; bothslots>=9→MI fallback; ridingcomparison only fordestination<9 | chosen slot |
| Double-click0x5261b | WORDwarpglobal0x4166190 zero; index0..6 blocks; selectedridingpet blocks | -1 |
| Drag-out0x53203 | releasebit4,drag!=-1,positionboundary,WORDwarpzero,PETwindow; bounded route contains no ridingcomparison | -2 |

When source<9 anddestination>=9, drag/drop jumps directly toPET sender and skips riding check. This is a compiled UI distinction, not proof of server permission. The pickup and double-click boundaries use7 while transfer grouping uses9; they have different purposes and are not one inferred capacity. Pet/from/to names are semantic comparison with pinned menu.cpp, not recovered binary symbols. Earlier broad wording about riding guards is refined, not retroactively erased.

## Reproduction and limits

`python -m tools.stoneage_wayi_pet_transport_probe LOCAL_DECOMPRESSED_CLIENT` uses Capstone5.0.7, strict acceptedhash/length and16 completely decoded aligned windows. It emits call/jump/test/global-write/constant operand metadata, no assembly text. Conditional-edge linkage only names an immediately adjacent CMP/TEST; it does not guess flags across intervening instructions. Hypothetical CMP/Jcc helper masks to1/2/4byte widths and distinguishes signed/unsigned comparisons; it is not native client execution.

12 new controls cover direct/indirect import edges, import thunks, branch targets/fallthrough/comparison linkage, nonadjacent rejection,WORDwidth, callback constants/registerwrites,signedsentinels,bytemasking,7/9 boundaries,unsupportedwidth/condition,wronghash. Plus70 adjacent PET/updater/PE/archive regressions:82 checks.

Fresh comparison source BismarckDD/Stoneage999ffdf1d220ec6666eb65339180689c9caf1876; autil369f2b35a812535557d55496626ff6a2cac1c56b,lssproto_util25ed992b6b9ba58ee174c2df5c4c6e970ba7ec95,protocol17f1900d8845c15308a4b429905ec009e5fd4c0f,menu62754fdd0db1b84c358d61418d253012d149e1d4. No exactsource/build equivalence. Originalcapture2006/mutableheader2005 do not authenticate2005 publisher release.

Pressure2486=2465 bounded closed+18 OPEN+3 historical UB unchanged. Matching native server/owner/drop/save/unique-code behavior, authentic full8.0 package/hash and early-era membership remain OPEN. NEXT: recover actual compiled PET inventory/update receive handler and clientslot-state layout, independently ofsend127; trace original server pair only after provenance/build gate. No engine transition.
