# TW1.0 R56 conditional application frame and write-request binding

Status: conditional numeric metadata specification on invented storage and explicit stubs. Actual native persistence remains OPEN.

The exact R54 report supplies all17 helper0x49160 instruction shapes and18 edges, all55 writer-caller0x40020 shapes and54 edges, and the R55 transform's129 shapes. R55 supplies the accepted conditional writer arithmetic. R56 reads only these SHA-pinned numeric reports and fabricated arrays. Its restricted model has no executable loader, original save input, OS file I/O or native API. CALL-shaped observations dispatch only explicitly named numerical helper/transform abstractions and invented open/write/close stubs; no original binary is executed.

## Helper hardware geometry

Let S be caller ESP just before CALL0x40025. A fabricated near-CALL marker enters the helper at S-4; PUSH ECX stores the four-byte value at S-8. LEA ECX,[ESP+8] obtains S. The4096-byte loop subtracts whole pages from ECX and EAX, followed by the remaining EAX amount. TEST memory operands perform invented reads; their decoder read annotations remain unchanged in the source metadata. They are not replaced with observed original probe values.

The helper rewrites ESP to the resulting ECX coordinate, restores saved ECX from the old stack, loads the old return marker, then PUSH/RET relocates it. Under valid32-bit memory/stack/near-return conditions, continuation ESP is S-requested_amount. For the caller literal4132, this is S-4132. This is a conditional hardware relation, not proof that any original stack allocation or memory probe succeeded.

An independent closed expression for tested probe offsets is the whole-page sequence -4096,-8192,...,-4096*floor(amount/4096), followed by -amount. An exact page multiple therefore repeats the final address; amount0 yields one read at S. The invented domain0..65536 is a model bound, not an original argument-range claim.305 fixtures cover zero, all amounts0..256, page boundaries through65536 and literal4132; every helper instruction is exercised. A failed invented probe stops qualification.

## Copy and storage

The caller's31 repeated dword copies followed by a word and a byte copy yield127 copied bytes only with clear DF, compatible flat source/ES destination segments, valid source/destination addresses and initialized source memory. Unknown DF/segments remain unqualified. Invented source bytes are deliberately generated; original globals/save values are not read.

| Conditional region | Half-open offsets relative to S |
|---|---|
| Length cell | [-4132,-4128) |
|127-byte snapshot | [-4128,-4001) |
| Padding | [-4001,-4000) |
|4000-byte output capacity | [-4000,0) |

The saved ESI/EDI words and physical call arguments lie below these regions. This separation is conditional on the helper and copy premises; it does not establish actual ABI/alias validity.

The six transform slots resolve to snapshot pointer,count127,seed0,output pointer,length-cell pointer,capacity4000. The R55 normal model stores count128 and writes128 output bytes. Its input mutation changes only the fabricated snapshot, while its stack-local byte and overwritten pointer slot remain governed by the R55 model.

## From transform to write request

With ordinary near-return stack geometry and preservation of live storage across the opaque calls, the independent caller algebra and concrete invented model agree:

| Site | Conditional ESP before instruction | Relevant address |
|---|---:|---|
| Transform CALL0x4005a | S-4164 | six physical arguments |
| Open CALL0x40069 | S-4172 | two more pushes |
| Load0x40080 after ADD ESP,32 | S-4140 | [ESP+8]=S-4132 length cell |
| Write CALL0x40090 | S-4156 | slots0:buffer S-4000;4:literal1;8:count128;12:opaque open-return shape |
| Post-write load0x40095 | S-4156 | [ESP+24]=S-4132 length cell |

The write-buffer LEA0x40086 resolves to S-4000. Under the stated premises, the requested buffer bytes and count match the transform output.256 invented snapshots cover every derived key byte and verify this correspondence. No bytes are written to a file.

Stack geometry alone does not qualify memory contents. An invented open-stub overwrite of the length cell changes the write count from128 to127 while preserving ESP. Another overwrite changes output content while preserving the pointer. The report retains both counterexamples. Without explicit opaque-memory preservation, content/count binding is unknown; without opaque-stack preservation, downstream coordinates are unknown. Known prefix geometry is retained separately.

## Return paths and limits

Seven invented return-path cases cover open0, write0/127/128/129/0x80000000/0xffffffff and close0/0xffffffff. These values are test inputs, not established native error conventions. Together with the successful key fixtures they exercise all55 caller shapes.

The bounded caller tests the open-return-shaped value, then compares write EAX with the reloaded count through unsigned JAE0x4009e. The short-return path returns literal0 without the close-call candidate in this graph. The >=count path reaches CALL0x400ac, then overwrites the close-return-shaped EAX with literal1 at0x400b4. Thus a modeled literal1 does not prove a successful close/flush or persistence; a high-bit invented write return can also take that unsigned path. Actual wrapper return meanings and any resource-leak claim remain OPEN.

A separate all-path ESP algebra checks every55 caller sites, the three normal-return exits and the five recorded concrete witness coordinates. Omitting the opaque-stack premise leaves downstream states unknown rather than forcing zero call effects.54 new controls cover page/marker/ECX/failed-probe behavior, signedness and copy assumptions, stub paths, memory-clobber counterexamples, custody/report corruption and independent-algebra mutations. This is finite conditional verification, not exhaustive native execution evidence.

Open: actual stack/REP/callee preservation, native wrapper returned-count/error semantics, close/flush success, original bytes and field meanings, tag/version/migration/checksum/schema/persistence, original server authority and cross-version equivalence. Stage A subsystem gates are unchanged.
