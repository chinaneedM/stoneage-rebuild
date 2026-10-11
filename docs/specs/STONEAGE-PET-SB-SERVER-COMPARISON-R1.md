# PET S46/B server output versus captured client layout R1

Status: **SOURCE_PREPROCESSING_COMPARED_TO_COMPILED_CLIENT_NOT_PAIRED_RUNTIME**.
Fresh rebuild main at startup: `152d71913b0c5b5b7d910a61b86c89972f574da5`,
tree `64140029cb0d7a7d5dcca5caadc7b5ba6f0e96db`; latest main Actions
38162331394/38162331325 success. No original program executed.

## Two separately pinned source profiles

Previous Bismarck descendant `999ffdf1d220ec6666eb65339180689c9caf1876` and
freshly resolved HEAD `2f736808ff4361f5429ee919b718c88fabb60346` are nine
commits apart. Neither is an authenticated operator server build. Their item
serializer and PET move/send bodies have identical Git blobs; protocol wrappers
and headers differ. Pin each profile separately. The auditor checks nine named
blobs plus all 40 transitive non-system preprocessing dependencies per profile.

GCC preprocessing verifies both default and controlled `-D_PET_ITEM` paths.
This does not compile or run the server and does not certify deployed flags.

| Property | Previous source | Fresh source | Captured client |
|---|---|---|---|
| Default PET item sender | excluded | excluded | compiled receive B branch present |
| Forced PET sender | present | present | no server counterpart established |
| PET slots | 7 | 7 | 7 |
| Player equipment slots | 9 | 9 | UI threshold 9 independently observed |
| Populated item fields | 13 | 13 | 14 |
| Empty item fields | 13 | 13 | clears empty-name row; fixed step 14 |
| Last field | type | type | jigsaw after type |

Both source headers enable damage, pile and alchemist fields. Forcing PET_ITEM
alone does not append the missing fourteenth field. Original client evidence
remains the accepted operator-linked September15 2006 capture, decompressed
SHA256 `4193a7e1b20b996f7902424ae05092b455c5dbbe3f133d331a4897bbc7abfe63`;
mutable July2005 headers do not establish exact original2005 release identity.

## Payload field comparison

| Position | Captured client destination label | Source producer |
|---|---|---|
| 1 | name | escaped ITEM_SECRETNAME |
| 2 | name2 | empty paramshow |
| 3 | color | selected item color |
| 4 | memo | escaped ITEM_EFFECTSTRING |
| 5 | graNo | ITEM_BASEIMAGENUMBER |
| 6 | field | ITEM_ABLEUSEFIELD |
| 7 | target | ITEM_TARGET |
| 8 | level | ITEM_LEVEL |
| 9 | sendFlag | composed flags |
| 10 | damage | durability text |
| 11 | pile | ITEM_USEPILENUMS |
| 12 | alch | INGNAME0 |
| 13 | type | ITEM_TYPE |
| 14 | jigsaw | absent |

The source B payload begins with category and decimal pet ID, followed by seven
item rows; empty source rows contain twelve internal separators. Each row gets
one appended separator, and the final separator is chopped. A seven-populated-row,
ASCII, delimiter-free synthetic alignment shows why the mismatch matters:
client field14 of row0 consumes source row1's name; client row1 begins on source
row1's field2. Subsequent rows drift further; the last client row extends past
the 91 source fields. This is structural analysis, not original malformed-packet
execution or a claim about every possible empty/multibyte payload.

The source uses initial length2 for B plus pet ID, buffer1024 and row token512;
its overflow-send path does not reset the length accumulator. These are observed
source assumptions and an unresolved bounds issue, not a tested exploit or new
historical UB pressure classification. Declared source capacities do not apply
to the original client's 388-byte records.

## Conditional source request and follow-up chain

Both late profiles preserve the optional move route. Each accepted exchange
direction writes two actor slot indices, then calls player item update, pet item
update, pet parameter recalculation and K status update in that order. There are
four source setter statements across two branches, not four writes per request.
Player update wrapper leads to logical I22; pet update is logical S46/category B.
S sender appends encoded string followed by its checksum; source checksum is
string byte length, not an additive sum of the item fields. In NEW/80 source
framing, outgoing +23 gives formatted69 for S46, consistent with independently
observed original client incoming -23. That directional agreement does not
certify keys, encoding, an emitted packet or a matching server build.

The B empty-header sender is also present in pet-placement code, separately from
movePetItem. Do not call all B messages a PET127 acknowledgement.

In the pet-to-player branch, an occupied backpack destination enters a guard
that compares `(type - ITEM_PET_HEAD)` against **toindex**, while the destination
is >=9 and admissible pet type offsets are 0..6. Therefore this bounded late
source branch rejects such an occupied swap. Empty-backpack removal bypasses
that item-type guard. This is a descendant-source defect/behavior, not evidence
that the archived operator build shared it; no original code was patched.

## Reproducibility and boundary

`tools/stoneage_pet_sb_server_audit.py` verifies hashes, preprocessing, formats,
empty fields, enum limits and ordered outputs. Derived ledger:
`research/recovered/STONEAGE-PET-SB-SERVER-COMPARISON-R1.json`. Functional parser,
alignment and mutation checks are independent of original execution. CI repeats
the exact two source checkouts and compares source-free derived results to the
ledger. Original source, programs, assets and disassembly remain outside Git.

**OPEN:** original publisher-compatible fourteen-field/jigsaw server build,
deployment/configuration provenance, authenticated client/server pair, native
PET127 request and S/B output, physical item owner/save/drop/unique identity.
No JSS1999/Taiwan1.0 feature or modern-engine promotion. Pressure remains
2486 = 2465 bounded closed + 18 OPEN + 3 historical UB.

Highest NEXT: recover the compiled client's ordinary I22 inventory receive
layout and compare its stride/slot-index rules with these source outputs. Use
that independent second message family to distinguish shared payload profiles
before admitting any candidate server; compatible original server provenance
and native paired runtime remain separate gates.
