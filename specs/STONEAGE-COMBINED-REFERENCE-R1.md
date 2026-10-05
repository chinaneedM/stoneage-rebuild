# StoneAge Combined reference R1

## Status

**COMBINED_REFERENCE_R1 = CLOSED_BOUNDED_RECOVERED25_WELLFORMED_OPTION_REFERENCE.**

The verified recovered25 callback family is exactly **627, 629, 630, 632,
637, 646, 648**. Only **627, 632 and 637** have positive enemybase slot
references: **5 uses across 5 templates**. IDs 629, 630, 646 and 648 remain
zero-reference data evidence and are not admitted as executable candidates.

No ordered runtime is admitted by this reference closure.

## Fixed descendant source reference

The audit is pinned to the same three fixed later-source profiles used by the
preceding pet-skill closures:

- gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- BismarckDD `999ffdf1d220ec6666eb65339180689c9caf1876`

The reproducible source audit closes the well-formed OPTION reference:

- callback registration and feature gates are active;
- the declared OPTION count is read and clamped to a maximum of ten;
- one raw `rand()%count` selection chooses a magic ID;
- the callback writes symbolic `BATTLE_COM_JYUJYUTU`, whose pinned
  descendant enum value is 2000;
- target goes to COM2, selected magic to LOW(COM3), HIGH(COM3) is cleared;
- the battle dispatcher calls `MAGIC_DirectUse`;
- the defender-side Combined command changes the pinned descendant dodge
  parameter from 0.02 to 0.027.

The source audit resolution is
`COMBINED_FIXED_SOURCE_CLOSED_WELLFORMED_OPTION_REFERENCE`.

## Preserved descendant differences

Real differences are recorded rather than flattened:

- gavin/iris use a NULL-pointer OPTION guard; fixed Bismarck uses a
  pointer-to-literal-NUL comparison;
- gavin/iris leave the historical count/kill declaration uninitialized,
  while fixed Bismarck initializes count to zero;
- gavin/iris initiative uses
  `WORKQUICK+20 - RAND(0, work*0.3)`;
- fixed Bismarck initiative uses
  `WORKQUICK+20 - RAND(0, 15)`.

Therefore a later runtime must choose or model the initiative profile
explicitly. Reference closure does not silently designate one descendant as
the original behavior.

## Recovered25 exact-row evidence

Corrected first-pass Action **37262695753 PASS** established the complete
seven-row population and the 5-use/5-template reference set. Second-pass
exact-pin Action **37262850204 PASS** at input commit
`a3029a77c43bba60aef13a930d0bfb3a07361abb` closed all exact rows. The
derived report was written back at commit
`8252a51966450a0b5b515d051e52b3c84d61ae65`.

The full recovered `petskill` SHA-256 is
`f9cefefda40e3a5de9b8cdcb9f8d5c75cd768257bb9b12f7591e86d61fe2f6d4`.

Positive recovered rows are:

- ID 627: TARGET 3, ILLEGAL 2000, 1 slot reference, declared/effective count
  6, magic IDs 21/139/159/169/179/189;
- ID 632: TARGET 1, ILLEGAL 5000, 2 slot references, declared/effective count
  1, magic ID 240;
- ID 637: TARGET 2, ILLEGAL 20000, 2 slot references, declared/effective count
  1, magic ID 61.

Exact metadata, OPTION lengths and SHA-256 values, marker hash, counts and
magic-ID lists for all seven rows are pinned in
`research/recovered/STONEAGE-25-COMBINED-PROBE-R1.txt`. Raw OPTION bytes,
names, descriptions and assets are not stored.

The recovered probe resolutions are:

- `RECOVERED25_COMBINED_POPULATION_CLOSED`
- `RECOVERED25_COMBINED_WELLFORMED_OPTION_CLOSED`
- `RECOVERED25_COMBINED_EXACT_ROWS_CLOSED`
- `RECOVERED25_COMBINED_ORDERED_RUNTIME_OPEN`

## Safety and provenance boundaries

Malformed OPTION behavior is not normalized. Nonpositive counts reach
historical modulo/index undefined behavior, and missing listed magic tokens can
leave historical array elements uninitialized. Those malformed domains are
outside R1.

The marker lexeme is localized across descendant profiles and stored only as a
hash. The fixed descendant audit is later-source evidence; it does not prove
original JSS/Taiwan-v1 membership, original binary/compiler identity, or the
original game's numeric command encoding.

## Runtime handoff

The next runtime stage must:

- admit only positively referenced recovered IDs **627/632/637**;
- recheck the exact seven-row population and exact row pins as data evidence;
- keep IDs 629/630/646/648 data-only unless independent positive use appears;
- consume one explicit reduced selection draw only when Combined executes;
- preserve selected magic ID, target and direct-magic dispatch ownership;
- preserve Nocast/direct-magic failure boundaries rather than fabricating an
  effect;
- resolve the descendant initiative-profile divergence explicitly;
- continue using symbolic command identity instead of claiming original
  historical COM1 provenance.
