# JSS2001 player status, character level-up and knockout source contract R1

Task: `JSS2001-PLAYER-STATUS-LEVELUP-AND-KNOCKOUT-01`. This recovers the
meaning of player parameters, bonus allocation and knockout consequences from
one already authenticated early operator manual. It does not implement a game.

## Source and finite scope

Original: http://www.titan.co.jp/stoneage/manual02.html. Exact replay:
https://web.archive.org/web/20010418083149id_/http://www.titan.co.jp/stoneage/manual02.html.
28434 bytes, SHA256 `50b9771ec501067136629c8e083a190e979e53dd9ba141903f78b76d43b602cc`,
strict Shift-JIS. Only anchors3040/8020/8060; no image, executable or new link.
Stop after three source-qualified tutorial records and nineteen bound status
table labels. They are not nineteen game entities or protocol fields.

The original and all three generic section fingerprints already exist in
`JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json`; its manual02 creation contract is
null. The new result is behavior semantics, not a new original or first hash.
Prior pet, service and mail/venue semantic contracts are retained unchanged.

## FACT — descriptions within the 2001 Japanese manual

| Context | Source-described behavior | Still unknown |
|---|---|---|
|3040, status|19 labels; Ctrl+S; title button; DP rises on level-up and player-versus-player victory|DP amount, title layout and original offsets|
|3040, EXP/NEXT|EXP prose limits recipients to characters and pets knocking out enemies; NEXT is EXP needed for next level|last-hit/sharing algorithm, eligible subsets, reward and threshold formulas|
|3040, derived parameters|damage lowers durability; zero means knockout; spells lower spirit; attack/defense influence damage; agility influences speed/evasion; charm mainly concerns player/pet relation|coefficients, caps, original numerical values|
|3040, elements|earth→water/wind, water→fire/earth, fire→wind/water, wind→earth/fire are attack/defense **influence** pairs|sign, superiority, elemental ratios and damage multipliers|
|3040, primary parameters|vitality relates to durability; strength to attack; toughness to defense; quickness to attack speed/evasion|conversion formulas; primary and derived stats are not established as identical fields|
|8020, knockout|both character and pet revive at value1 after battle ends; depending on knockout damage, return to SP is possible|return threshold, operation order and runtime transaction|
|8020, distinct consequences|player charm decreases slightly; pet loyalty decreases|both deltas; other EXP/level/money/inventory/pet losses are not settled by omission|
|8060, character level-up|bonus points assigned through UP to four primary stats; charm and DP rise automatically|point count, deltas, caps, respec, pet growth or elemental bonus allocation|

3040 says durability (耐久力) reaches zero;8020 uses the word vitality (体力)
for zero and revival1. Preserve the wording/context. Neither prose licenses a
wire-offset join, an equality of primary vitality and current durability, or an
original server save-field identification. No equation or penalty number is
introduced. Creation's20 stat/10 element points cannot fill per-level unknowns.

## Verification and durable custody

The parser binds each of19 labels to its own two-cell table row before deriving
relations; per-row description hashes and all three section hashes survive in
the permanent JSON. Whole source SHA/length and exact final URL are required.
Adversarial tests cover EXP sharing inventions, element multipliers, mistaken
stat identity, DP triggers, knockout timing/conditional SP, charm/loyalty,
unmentioned losses and level-up/creation/pet-growth conflation.

The independent workflow reacquires the one known source, derives the complete
report, compares bytes and uploads only derived JSON. Passing status, ZIP/raw
digest, Git blob and exact main acceptance must be observed before recording
success. Original HTML/assets remain outside Git; no asset reuse rights inferred.

Stage A remains7 PARTIAL+2 OPEN; Stage B/game/wiki GATED; R79
PAUSED_NON_BLOCKING.2001 capture is not1999 launch, TW1.0 or CN1.82 same-build
proof. Next: `JSS2001-PLAYER-PET-STATUS-AND-CREATION-BOUNDARY-01`, a finite
offline comparison against existing pet status and creation contracts, with
zero new source/asset requests, separating shared labels from field identity
and initial allocation from later growth. Then return to material coverage.
