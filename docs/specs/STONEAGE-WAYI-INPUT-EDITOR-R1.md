# Compiled input editor, terminators and settings writer R1

Exact accepted operator-linked 2006 client: unpacked921600bytes, SHA256
4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63.
This analysis neither runs the original nor reads credentials/actual settings.
Original bytes, source, disassembly and assets are excluded from Git.

## Compiled editing paths

Focussetter0x11940 stores descriptorpointer atRVA0x150d64. Singlebyteeditor
0x113d0 reads BYTE countoffset0x107, limitoffset0x104 and cursoroffset0x109.
It rejects controlbytes<=31 and count>=limit. For the two login descriptors,
only ASCII0..9/A..Z/a..z are admitted. Their already verified initializer
supplies limit12. Thus ordinary editor-generated login text is at most12bytes.
Doublebytehelper0x114e0 requires count<limit-1 and rejects both login descriptors
before inserting either byte. Both helpers move the existing terminator along
with the suffix, then increment count/cursor by1 or2.

The synthetic model requires well-formed count/cursor and an existing NUL;
these model guards are not observed native upstream checks. Normal generated
login text terminates before the first16bytes decoded by the earlier login
path. Other writers/restored/corrupt state are not admitted by this result.

Startup0x1e5a6 passes0x10620 as callback to0x94ef0; initialization stores it at
RVA0x4bb46d0. Two SDK result paths independently call that pointer at0x95273
and0x9554f after writing result-string NULs. Stringcallback0x10620 reads strlen,
clamps its iteration budget86, and calls KERNEL32.IsDBCSLeadByte before choosing
singlebyte or doublebyte helper. A pair starting at85 may consume byte86, past
the loopbudget; this does not attest a safe dangling-lead case. Original
classification depends on active Windows code page; CP936 or Big5 runtime is
not inferred. Maincharcall0x3ff50 and alternate explicitWM_CHAR0x102 branch
0x8dacb call the singlebytehelper directly. No native SDK event is replayed.

## Compiled submit branch versus independently pinned source

Bounded clickbranch0x20c80 scans only the first login buffer for a nonempty
string. On that branch it writes zero at each buffer's own BYTE count index
(0x20cc3/0x20cc9). Empty second field does not change this named UI branch's
return condition. This is not an authentication bypass or server acceptance
claim; WGS/authentication and every other submission path remain separate.

BismarckDD/Stoneage master freshly resolves
2f736808ff4361f5429ee919b718c88fabb60346. Seven exact sourceblob hashes recorded.
Current chat.cpp has the ASCII alphanumeric login restriction commented out,
while still rejecting doublebyte login fields; current main.cpp sendsWM_CHAR
through a GBK-to-UTF8 bridge. Current login.cpp uses18 and checks both inputs
nonempty. Those are lexical source facts, not a whole-source build/runtime
profile or evidence that the compiled specimen follows the later behavior.
Descriptorheader STR_BUFFER_SIZE260, count/limit/cursor field names explain
address observations, without substituting modern source behavior.

## Settings persistence is a separate buffer

Compiled writer0x806ba copies and passes127bytes fromRVA0x4319d28 to encoder
0x8e050 with argument0 and outputcapacity4000, then opens literal
`data\savedata.dat` usingmode`wb+` and writes the returned encoded length.
CRT function names are supported by source comparison; these are not imported
Win32WriteFile calls. Constructor0x808c0 clears31DWORD+WORD+BYTE=127bytes,
setsversionWORD6 and observed sound/pitch/chat settings. It does not read the
two encrypted32byte globals in the bounded constructor/writer windows.
The synthetic factory only models these observed initializer offsets; it does
not encode or write a file.

Pinned savedata.cpp reserves12+12bytes under CDKEY/PASSWORD enum names, but
those named tokens occur only in the enum chain and no szUser/szPassword access
occurs in that file. This does not prove credential persistence, or prove all
historic settings files have zero reserved slots. New constructor zeros remain
separate from loaded bytes and inherited files. Native load/decode/migration,
full per-byte writers and codec framing remain NEXT.

## Acceptance scope

228 project tests plus actual fixed-source profile rederivation. Generated
well-formed bytes only; static edges and source comparisons are not native
input/login/server/save execution. Previous F/N, key, TEA/legacy and13/14item
profile differences remain. Pressure2486=2465+18+3 unchanged. Authentic operator
server, native owner/save/drop/unique lifecycle, exact2005 package/hash and
early-era admission remain OPEN; no modern engine promotion.
