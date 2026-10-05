# StoneAge Combined reference R1

## Status

**COMBINED_REFERENCE_R1 = OPEN_SOURCE_AND_DATA_AUDIT.**

Pressure ranking on verified `main` selected `PETSKILL_Combined` as the
next OPEN callback. The positively referenced recovered25 IDs are **627, 632
and 637**, with **5 enemybase slot uses across 5 templates**.

The first hash-verified bundle observation in Action **37262367447** corrected
the pre-audit population hypothesis: the full callback family contains
**627, 629, 630, 632, 637, 646 and 648**. IDs 629, 630, 646 and 648 have zero
positive enemybase slot references in this recovered25 corpus and therefore
remain data evidence rather than executable candidates. This seven-row
population must reproduce under the corrected gate before it is accepted.

No runtime implementation is admitted by this document yet.

## Fixed descendant audit target

The reference audit is pinned to the same three fixed later-source profiles
used by the preceding pet-skill closures:

- gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
- iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
- BismarckDD `999ffdf1d220ec6666eb65339180689c9caf1876`

Action **37262367447** reproduced the fixed-source audit before the data
population expectation stopped the workflow. The shared callback shape is:
OPTION supplies a declared list length and magic IDs; lengths above ten are
clamped to ten; one raw `rand()%count` selection writes
`BATTLE_COM_JYUJYUTU` (numeric 2000), target, selected magic in LOW(COM3),
zero in HIGH(COM3), and the battle dispatcher calls `MAGIC_DirectUse`.

A real descendant-profile divergence is retained rather than normalized:
gavin/iris calculate Combined initiative from `WORKQUICK+20` minus a
0..30%-of-work random interval, while the fixed Bismarck profile uses
`WORKQUICK+20` minus a fixed 0..15 random interval.

## Safety boundary

Malformed OPTION behavior is deliberately not normalized. The fixed source
does not guard nonpositive counts before `rand()%count`, and missing listed
magic tokens can leave `kill[]` elements uninitialized. The accepted model
therefore covers only hash-verified recovered25 rows whose OPTION structure is
proved well formed.

The marker lexeme is localized across descendant profiles and is recorded only
as a hash; raw source text or raw recovered OPTION bytes are not stored.

## First-pass data objective

The recovered25 probe must prove, from the hash-verified preservation bundle:

- callback population exactly IDs 627, 629, 630, 632, 637, 646, 648;
- positively referenced IDs exactly 627, 632, 637;
- exactly 5 positive enemybase slot references / 5 templates;
- every actual OPTION has a positive declared count and enough numeric magic
  IDs after the source's max-10 clamp;
- exact metadata, OPTION hashes, marker hashes, declared counts and selected
  magic-ID lists are emitted as derived facts.

The first pass intentionally leaves exact-row pinning OPEN. A second pass will
pin the observed derived rows before source/data reference closure.
