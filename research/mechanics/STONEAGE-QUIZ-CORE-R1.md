# StoneAge Quiz Core R1

Status: **fixed-descendant common core plus verified recovered 2.5 active surface closed**

## Evidence controls

Fixed descendant source revisions:

- gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56
- iriselia/StoneAge @ 9e6c8ce2cd8ed532a7157773acd1c61582c178b5
- BismarckDD/stoneage @ 999ffdf1d220ec6666eb65339180689c9caf1876

Recovered specimen:

- bundle SHA-256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5
- Quiz argument aggregate SHA-256 ca0f288083a3f6b6049d69061bb49c9b87cdb7b295543b8d455972d72c94567e
- question-table aggregate SHA-256 fdf6b872320c1593769875a15a9feb1242ffb73f69ffef81de3ff02f5ed780c5
- real-byte probe workflow 35419940820: success
- deterministic core validation workflow 35419980296: success

## Recovered active population

The recovered world graph contains one Quiz template-name value that is duplicated in the template corpus, but every surviving definition of that name selects functionset Quiz. There is therefore no mixed-function load-order ambiguity for this class.

That stable template name is referenced by **22 create records**. Earlier R4 wording that treated the four Quiz template blocks as four instances was incorrect and is superseded by this report.

All 22 create references resolve to secondary files.

## Active configuration shape

All 22 recovered configs contain:

- StartMsg
- Quiznum
- EntryItem
- NoEntryMsg
- Border
- FailureMsg
- Party
- Type
- Answer
- Level

Additional keys:

- Warp: 21/22
- GetItem: 4/22
- ItemFullMsg: 3/22
- EntryStone: 0/22
- Scope: 0/22

Every EntryItem is exactly one starred requirement with quantity 1. Thus the active recovered admission charge is one configured item, not Stone.

Quiznum distribution:

- 1 question: 3 configs
- 2 questions: 3
- 3 questions: 3
- 5 questions: 6
- 7 questions: 3
- 10 questions: 3
- 100 questions: 1

Type is 1 in 21 configs and 0 in one. Because every loaded recovered question has type 1, both forms admit the same recovered type population; nonpositive masks normalize to 0xffff in the fixed code.

Answer is 7 in 21 configs and 0 in one. The value 7 includes answer-type bits 1, 2 and 4, while nonpositive values normalize to 0xffff, so all recovered configs admit all three recovered answer types.

Level masks are 3, 6, 12, 14, 16, 28 and 31. The recovered question table uses level bits 1, 2, 4, 8 and 16, so these masks select staged subsets rather than numeric level ranges.

## Global question table

The recovered question file has 150 non-comment source rows.

- 149 rows have the nine fields consumed by the fixed loader.
- 1 row has only eight fields and is skipped before being counted into the final loaded Quiz array.
- no recovered row triggers the fixed fatal validation for a two-choice question using answer 3 or a free-text question whose answer number is not 1.

Loaded question metadata:

- type 1: 149/149
- level bit 1: 42
- level bit 2: 25
- level bit 4: 30
- level bit 8: 29
- level bit 16: 23
- answer type 1: 22
- answer type 2: 84
- answer type 4: 43

Answer-number distribution in the loaded table is 130x1, 12x2 and 7x3.

R1 does not retain question text, answer text or original rows.

## Admission and capacity

Talk requires a player within distance one.

Before opening the normal start prompt, NPC_QuizItemFullCheck checks reward capacity:

- if any ordinary item slot is empty, the gate passes immediately;
- if inventory is full and EntryItem is configured, the gate passes only when the player currently satisfies that item requirement, on the assumption that admission consumption will free a slot;
- if inventory is full and no usable EntryItem can free a slot, the gate fails.

Only 3/22 recovered configs provide ItemFullMsg. Therefore 19 recovered configs can enter the fixed missing-message path if the player is completely full and lacks the required entry item.

The Quiz NPC keeps at most eight concurrent session slots per NPC instance.

## Entry item lifecycle

On Yes confirmation, the source validates EntryItem and optional EntryStone before allocating a Quiz session.

Unlike Janken, a failed Quiz entry check is a real gate: the NoEntry path is sent and the mutation/start branch is not executed.

Validation and deletion are separate. The generic fixed-source item helper preserves the same quirks seen in Janken:

- each requirement token validates against the original inventory;
- duplicate requirements can therefore reuse the same physical copies during validation;
- starred deletion removes up to the requested count;
- a plain token deletes every matching copy.

Recovered 2.5 uses only one starred token with count 1, so those multi-token/plain-token quirks are dormant in the active specimen. The active path consumes exactly one configured entry item when present.

EntryStone exists in source but is absent from all 22 recovered configs. The source's negative-cost oddity is therefore dormant in this specimen.

## Party warning defect is active

NPC_QUIZPARTY_CHAECK returns false for a player in a party.

However, both the initial Talked path and the question-loop path only display the configured Party message and then continue execution; neither returns.

Because **Party is present in all 22 recovered configs**, this is not merely dormant source code:

> party membership produces a warning but does not actually prevent Quiz participation in the recovered 2.5 shape.

## Question selection

Type, Answer and Level are bit-mask filters, not scalar equality filters.

Eligible questions are selected randomly and the session stores previously used indexes to avoid repetition.

The fixed history array has 100 entries. The source has no protective bounds check when writing oldno[p_old]. The one recovered Quiznum=100 configuration reaches that designed array limit but does not exceed it.

Source-lineage implementation hazards are versioned:

- gavinlinasd returns a pointer to a local stack question-index array, an undefined-lifetime defect;
- iriselia repairs this with caller-owned fixed storage;
- Bismarck uses dynamically resized static storage;
- gavinlinasd/iriselia store session heap pointers through integer work fields, while Bismarck replaces that with a handle table.

These are implementation hazards, not intended game rules.

## Answer semantics

Answer type 1 presents two shuffled choices; answer type 2 presents three shuffled choices. The displayed correct index is stored in session state.

A numeric submission of zero is ignored and does not advance the question.

Answer type 4 is free text. The fixed callback checks:

configured correct answer is a substring of submitted text

rather than exact string equality. Extra prefix/suffix text can therefore still count as correct.

## Result thresholds

Border, GetItem and Warp all use the same threshold-pair rule:

- scan configured threshold/value pairs in their original order;
- return the first pair where score >= threshold;
- do not sort thresholds.

All 22 recovered configs have exactly two Border pairs.

GetItem is present in four configs, each with one threshold pair. Each recovered reward value contains exactly one candidate item, so the source's dot-separated random reward-choice branch is dormant here; recovered rewards are deterministic once their score threshold is met.

Warp is present in 21 configs:

- 6 configs have one threshold/destination pair;
- 15 configs have two pairs;
- 1 config has no Warp.

All 36 recovered Warp destination values have exactly three fields. Coordinates are not retained in this report.

## Result ordering

When the requested Quiznum has been completed, the fixed order is:

1. optional GetItem threshold evaluation and reward grant;
2. Border threshold evaluation and result message;
3. Warp threshold evaluation;
4. release the Quiz session slot;
5. perform the selected warp if one matched.

If item reward creation/addition fails, the function returns immediately before the later Border and Warp handling.

## Persistence boundary

Quiz can mutate inventory, carried Gold in dormant EntryStone configurations, and player position through the normal warp primitive.

The Quiz mutation path itself does not synchronously call the character-save routine. Durable inventory/Gold/location state therefore follows the ordinary character save/logout lifecycle.

## Deterministic artifacts

- tools/stoneage_quiz_usage_probe.py
- tests/test_stoneage_quiz_usage_probe.py
- .github/workflows/probe-stoneage-25-quiz-usage.yml
- research/recovered/STONEAGE-25-QUIZ-USAGE-R1.txt
- tools/stoneage_quiz_core_model.py
- tests/test_stoneage_quiz_core_model.py
- .github/workflows/validate-stoneage-quiz-core.yml

The core model validation passes 17 deterministic tests in GitHub Actions run 35419980296.

## Evidence status

- **FACT:** 22 recovered Quiz create refs resolve through one stable duplicated Quiz template-name value.
- **FACT:** every recovered config consumes one quantity-1 EntryItem on successful admission.
- **FACT:** no recovered Quiz config uses EntryStone.
- **FACT:** Party is configured in all 22 and the fixed callbacks warn without returning.
- **FACT:** 21/22 recovered configs use score-band Warp; all 36 destination payloads have three fields.
- **FACT:** 4/22 recovered configs use one-candidate GetItem rewards.
- **FACT:** the recovered question file contributes 149 loader-valid rows and one short row skipped by the fixed parser.
- **FACT:** Type/Answer/Level are bit masks in the common fixed core.
- **SOURCE QUIRK, ACTIVE:** party membership does not actually block participation.
- **SOURCE QUIRK, ACTIVE:** free-text correctness uses substring matching for the 43 loaded answer-type-4 questions.
- **SOURCE QUIRK, ACTIVE EDGE:** only 3/22 configs define ItemFullMsg despite the full-inventory failure path.
- **SOURCE QUIRK, BOUNDED ACTIVE:** the question-history array is fixed at 100 and one recovered config requests exactly 100 questions.
- **VERSIONED IMPLEMENTATION HAZARD:** question-index/session storage differs substantially across the three public descendant revisions.
- **DORMANT IN RECOVERED 2.5:** EntryStone, multi-candidate random GetItem, Scope, plain/multi-count EntryItem shapes.
- **OPEN:** exact JSS-era Quiz content and whether this subsystem existed in the same form at launch.

## Priority consequence

Quiz is closed for fixed-descendant common behavior plus recovered 2.5 active data. Re-evaluate LuckyMan and Door next; if they expose only a narrow Stone sink and transient world-door state, close the residual ordinary NPC sweep rather than expanding into deferred family/event packages.