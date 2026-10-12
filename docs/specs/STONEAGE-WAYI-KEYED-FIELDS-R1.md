# Wayi compiled keyed fields and login-key order R1

Exact accepted operator-linked2006capture; unpacked921600byte SHA256
4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63.
Derived static operands only. Original game/source/assets/disassembly are not
committed or executed. Synthetic vectors do not attest captured packets.

## Compiled field arithmetic

| Field | Outgoing client | Incoming client |
|---|---|---|
| int32 | permutation3142, complement, low-bit-first packing with key addition | key subtraction, unpack, complement, permutation2413 |
| byte string | low-bit-first packing with key subtraction | key addition, unpack |

Four helpers0x90080/0x90190/0x90310/0x90420 use masking63 and cyclic nonempty
C-string keys. Cursor starts0 for each invocation, advances for each emitted
symbol, wraps atkeyNUL. Trailing symbol only emitted for nonzero residual.
No standard Base64 padding. Thus int-1 has five symbols: decoder writes three
zero data bytes and terminatingNUL supplies the fourthzero to the int32 read.
This is not evidence of an upstream fixedsix-symbol integer requirement.
Stringchecksum is byte length (Big5-like fourbytes differs from twocharacters).
Integerchecksum is returned int32; aggregate signed overflow is not resolved.

Strict synthetic model errors do not establish native malformed-input guards.
Original lookup helpers retain prior matched pointers on some invalidsymbols;
model rejects suchinput without running it. Keys that differ by64 perbyte alias
under the6bit mask; codec is not modeled as a cryptographic authenticator.
Highbit key tests concern only low-six-bit observed arithmetic, not Csource
signedchar/undefined memory behavior. Decoder termination and invalidcases stay
separate from tested generatedtokens. Emptystrings are valid withnonemptykeys.

## Compiled login sequence and upstream refinement

Whole boundedconnectfunction0x5f510..0x5fa7b resetsmodeglobalRVA0x4205070 to0
at0x5f704. Receivedbufferfirstbyte E goeserror; F setsmode0x0f000001 at0x5f81c.
Otherfirstbytes takeversionerror inthisboundedbranch. Nfromcurrentdescendant
client source is not a compatible greeting merely because both are newer modes.
No actual received greeting or selectedsession is observed.

Atstate71 (0x47), fourDWORDglobalRVA0x15d834..0x15d840 arecopiedto16bytestackbase;
second16byteglobalRVA0x15ca78..0x15ca84 toanotherstackbuffer. Bothtransformvia
0x8f150 withlocalkeypointerRVA0xa248c,size16,mode1; wrapperroundsupto8byteblocks
andcallstwointernalhelpers. Actual transformprimitive/fullUI assignment isNEXT;
sourceuserId/password names arecomparison labels, notprovenoriginalUI identity.

Nonzero mode calls0x93500: twostringfields via0x908a0, sumtheirreturnedbyte
lengths, thenintegerchecksum via0x907a0, sendlogical71 via0x8fe70. Onlyafterthat
sendcall do post-loginbranches copyfirsttransformedstackbaseintofieldkeybuffer
andappendsuffix. Therefore thisloginemitterusesprevious/defaultfieldkey;
subsequentfieldsuseupdatedkey. Zeromodefallback0x3bd10 isaseparateoldfamily,
notreconstructed here. The defaultkeycopy, fieldkeybuffer andconditional
suffixes retain precedingcodecledger. No credentials are supplied orextracted.

## Separately pinned SOURCE / preprocessing profile

BismarckDD/Stoneage freshlyverifiedmaster
2f736808ff4361f5429ee919b718c88fabb60346; sixwholeblobpins inledger.
Despitefilename gmsv_server_send.c, incomingdispatcher
GmsvServer_ServerDispatchMessage getsconnectionCdkey, appends`shiqi.hk`, thenselectsdecoder under_NEW_FUNC_DECRYPT.
Exactboundedselector withpinnedversion.h/correct_bug.h/common.h preprocessed:
defaultselectsTEA/hex, explicitcontrolledundefselectslegacyouterdecoder.
Thisis morethan macro membership, but stillnotwholetranslationunit,
compiler/buildsystem/deployment ora matchingoperatorserver. Branch selected
profilesandfragmentSHA256 rederived inCI fromfixedGitblobs. Descendantsource
key defaults differ; prior13-vs14itemfield mismatchpersists. Fieldhelper
structureagreement alone doesnotadmitnativepairedruntime.

## NEXT

Recoverinputtransformprimitive/initialuser-inputglobalwriters, originalmode
admission/default-key transition andcross-profilecomplete framing/checksum
vectors. Independentlyauthenticateafourteenfieldoriginalserver beforeadmitting
nativePET/owner-save-drop-unique lifecycle. Full2005publisherpackage/hashremain
opportunistic. Pressure2486=2465boundedclosed+18OPEN+3historicalUB unchanged;
noearlyera ormodernengine promotion.
