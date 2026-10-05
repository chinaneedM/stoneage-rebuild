# StoneAge PETSKILL_Vary recovered25 reference R1

Status: **CLOSED_BOUNDED_RECOVERED25_REFERENCE**  
Date: 2026-10-05  
Scope: exact recovered25 callback population/data plus three pinned descendant source profiles.

## 1. Recovered25 population

Verified preservation-bundle data closes the callback population to exactly one row:

- callback: `PETSKILL_Vary`
- skill ID: **600**
- FIELD: **1**
- TARGET: **5**
- COST: **2**
- ILLEGAL: **1000**
- positive enemybase slot uses: **4**
- positive templates: **4**
- OPTION bytes: **22**
- OPTION SHA-256:
  `17e7ff6e7530a5fc2a0964432699f6c82a3dcc79374a2bad6fc547bbdc5e6f99`
- no embedded NUL;
- three ASCII percent signs.

The four exact positive references are all in enemybase skill slot **3**:

| TEMPNO | IMGNUMBER |
|---:|---:|
| 981 | 101427 |
| 982 | 101424 |
| 983 | 101425 |
| 984 | 101426 |

Pinned descendant source proves runtime `CHAR_PETID` is loaded directly from
enemybase `TEMPNO`, so the callback's hard-coded 981/982/983/984 gate maps
directly to these four recovered templates.

## 2. TARGET semantics

TARGET **5** is `PETSKILL_TARGET_NONE`, not a numbered battle position.
The skill therefore requires no player/client target selection. The callback
still receives a battle target carrier and writes it to COM2, while the later
battle action uses `BATTLE_TargetAdjust` only for the visual effect path.

## 3. OPTION byte semantics

The recovered 22-byte OPTION is safely recognized under **CP950** markers:

- attack: **+30.0%**
- defense: **-50.0%**
- quick: **+30.0%**
- no image marker.

The same raw bytes do not expose the corresponding UTF-8 or GBK markers in the
bounded probe. This establishes the recovered-data byte interpretation used for
the exact row; it does not prove the original executable compiler/locale.

## 4. Common fixed-source callback semantics

At gavin `1f90cb6...`, iris `9e6c8ce...`, and Bismarck
`999ffdf...`:

- `_VARY_WOLF` is active;
- source skill symbol is **600**;
- callback rejects actors whose runtime `CHAR_PETID` is not
  981/982/983/984;
- callback writes symbolic `BATTLE_COM_S_VARY`, COM2 target carrier and
  `BATTLE_CHARMODE_C_OK`;
- callback changes `CHAR_BASEIMAGENUMBER` to **101428**;
- callback resets `CHAR_WORKTURN` to **0**;
- `PETSKILL_Use` blocks another skill-600 cast while image is 101428;
- `BATTLE_DexCalc` has no Vary-special initiative branch, so callback-updated
  QUICK feeds the ordinary action ordering;
- `BATTLE_MagicEffect` emits battle animation frames only and does not mutate
  HP/status/combat attributes.

`_FIXWOLF` is active at all three fixed profiles. Its player-pet loyalty /
random-skill corrections are distinct from the recovered enemybase positive
path; the universal `PETSKILL_Use` recast block is relevant to both.

## 5. Material descendant divergence

### gavin / iris profile

The callback parses only:

- attack percent;
- quick percent.

For recovered25 bytes this means:

- ATTACKPOWER = FIXSTR + trunc(FIXSTR * 0.30)
- QUICK = FIXDEX + trunc(FIXDEX * 0.30)
- DEFENCEPOWER is not modified by Vary.

The battle action performs:

- `BATTLE_TargetAdjust`;
- `BATTLE_MultiList`;
- visual-only `BATTLE_MagicEffect` with actor effect 101120 and a target-side
  animation derived from base image / side.

### fixed Bismarck profile

The callback additionally parses defense percent. For the recovered row:

- ATTACKPOWER = FIXSTR + trunc(FIXSTR * 0.30)
- DEFENCEPOWER = FIXTOUGH + trunc(FIXTOUGH * -0.50)
- QUICK = FIXDEX + trunc(FIXDEX * 0.30)

At the fixed Bismarck pin, `_EXPANSION_VARY_WOLF` is **not active**.
Therefore the raw expansion image/effect branch exists in source but its
`BATTLE_MultiList/BATTLE_MagicEffect` body is compiled out for this profile.

No single descendant profile is silently promoted to recovered-original truth.

## 6. Transformation lifetime

After a Vary action, while image 101428 is active:

- `WORKTURN` advances from 0 to 1 on the initial Vary action;
- it increments after each subsequent action by that actor;
- when the counter becomes **>5**, the wolf image is reverted and the counter
  returns to zero.

Thus the transformed state spans **six actor actions including the initial Vary
action**, assuming no earlier battle exit/reset.

Expiry restoration differs by descendant:

- gavin / iris: restore base image, attack and quick;
- Bismarck: restore base image, attack, defense and quick.

Battle teardown independently restores a non-base pet image before normal
parameter recomputation.

## 7. Explicit boundaries

This R1 reference does not establish:

- original JSS/Taiwan-v1 presence or introduction date;
- recovered original executable/compiler identity;
- original numeric value of `BATTLE_COM_S_VARY`;
- which descendant defense semantics match the recovered25 executable;
- whether the fixed Bismarck no-animation action branch or gavin/iris
  visual-effect branch is the recovered executable behavior;
- expansion-image semantics from `_EXPANSION_VARY_WOLF`;
- client display/name text;
- whole-project completion.

Runtime must preserve the gameplay-significant profile divergence explicitly
unless stronger executable evidence resolves it.

## 8. Acceptance

- first-pass fixed-source + preservation probe: **37277985116 PASS**
- CP950 values + lifecycle gate: **37278693485 PASS**
- exact recovered row/templates: **37278937923 PASS**
- final fixed-source call/effect + exact recovered-data gate:
  **37279444143 PASS**

Derived reports:

- `research/recovered/STONEAGE-VARY-SOURCE-AUDIT-R1.txt`
- `research/recovered/STONEAGE-25-VARY-PROBE-R1.txt`

**VARY_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_REFERENCE.**

Pressure remains unchanged at **2444/2486 = 98.31%** until an ordered Vary
runtime is implemented and accepted.
