# Combined ordinary status-magic reference R1

**COMBINED_STATUS_MAGIC_REFERENCE_R1 = CLOSED_CONDITIONAL_BUILD_EXACT_OUTCOMES.**
**Combined ordered runtime remains OPEN.**

This follows the remotely accepted direct-wrapper MP boundary at
`97fb9e5ca78a007f383024b7edc935fd997077e0` and the continuation checkpoint
`0679cb6e1b419ae660c86e8763ced87fe71efc7c`.

## Scope

Positive Combined 627 can select StatusChange magic IDs
139/159/169/179/189; positive Combined 637 selects StatusRecovery ID 61.
This reference audits their ordinary battle parser functions at the same
three fixed descendant pins as the previous Combined audits.

The independent model receives raw OPTION bytes, a source profile and an
explicit execution charset. Native witnesses compile original status labels
and parser functions transiently, using collector stubs for the downstream
multi-target effect functions. No original code or OPTION text is stored.

## Accepted source differences

| Profile | Status scan bound | Actual label count | Conditional builds | Success marker |
| --- | --- | --- | --- | --- |
| gavin | 44 | 32 | UTF-8 / GBK | Single Han character |
| iris | 44 | 32 | UTF-8 / GBK / CP950 | Greek character |
| Bismarck | 12 | 12 | UTF-8 / GBK | Two Han characters |

The marker identities and source hashes are checked by the audit. Builds are
conditional experiments; none is asserted to be the recovered original
compiler's execution charset. As in the earlier Refresh audit, full CP950
source compilation is not admitted for gavin/Bismarck.

## Parser ordering and unsafe domains

- StatusChange scans starting at status index **1**. StatusRecovery starts at
  **0**, allowing a wildcard recovery marker.
- Both compare only the first **two execution bytes** of each label. UTF-8
  prefix collisions preserve the first matching source index rather than
  identifying a whole Unicode character.
- A match advances the pointer by **2 inside the body and 1 in the loop**.
  StatusChange's next search therefore starts three bytes after the match.
  A two-byte status marker immediately followed by `turn` loses its initial
  `t`; a separator matters.
- Both dereference a NULL OPTION. In the two short-table profiles, a nonmatch
  can scan past the actual 32-label array before moving to another input byte.
  Only independently named baseline matches are admitted by this R1 model.
- StatusChange overwrites its cursor with the `turn` search result. If that
  marker is absent, the next success-marker `strstr` receives NULL. The
  apparent duration default of 3 does not make this missing-marker path safe.
- Found `turn` and success markers advance by **sizeof(marker)**, including
  the terminating NUL size, and thus skip one additional separator byte.
  Integer parsing retains source defaults when conversion fails; overflow or
  reads past an exact NUL-terminated input witness are not admitted.
- Success searches begin from the cursor after the `turn` marker, so a
  success field before `turn` is ignored. Missing success alone retains 15.

The independent byte model refuses unsafe inputs. It does not silently repair
the original parser or convert one build's result into another's result.

## Validation

Local source reference: **747 defined native cases** and **38 expected
ASan/UBSan diagnostics** across all seven admitted profile/charset builds.
The 15 independent model tests cover wildcard/base labels, raw byte collisions,
cursor movement, marker order, numeric/default behavior and unsafe domains.

The verified-data workflow additionally checks full recovered `magic.txt`
SHA-256 and all 19 exact crosslink rows before supplying the six status-magic
OPTION byte strings directly to the transient original parsers. It reports
each of the 42 profile/charset/magic outcomes as defined or diagnosed unsafe.
Raw bytes are kept outside the repository. First-pass Action **37266411923
PASS** at input commit `463cc02c2c2fa3087c39548c9c2517cf6de5cfd6` wrote
the actual report at `7f50e1ae836485f2c46a5b2bc16e5a4cc2db9362`.

## Actual recovered-byte outcomes

Of the **42** profile/charset/magic cells, **24 diagnose unsafe table scans**,
**12 safely return FALSE without an effect call**, and **6 safely dispatch**
inside the explicitly conditional **iris CP950** build:

| Magic ID | Parser | Status index | Duration | Success offset |
| --- | --- | --- | --- | --- |
| 61 | StatusRecovery | 0 (wildcard) | — | — |
| 139 | StatusChange | 1 (poison) | 5 | 15 |
| 159 | StatusChange | 4 (stone) | 5 | 15 |
| 169 | StatusChange | 6 (confusion) | 5 | 15 |
| 179 | StatusChange | 5 (drunk) | 5 | 15 |
| 189 | StatusChange | 3 (sleep) | 5 | 15 |

All six real rows are unsafe in gavin UTF-8/GBK and iris UTF-8/GBK because
their raw bytes do not match the admitted label prefixes before the short
table is overrun. Bismarck UTF-8/GBK both safely reject all six without a
match. These are incompatible conditional outcomes, not one original rule.

Second-pass Action **37266742566 PASS** at input commit
`4c9974a1b569d08ac1d9b71d4d38c359fd0601c8` validates all **51** Combined
tests and all 42 independently pinned outcomes. Derived exact-matrix report
commit: `93cada6a5de092018391a837c80cd1c55e1839c3`, tree
`79de70c9cdb1cd3fad0d0e268660e04a173d1d52`.

Native totals with real rows included are **765 defined comparisons** and
**62 expected sanitizer diagnostics**. The accepted matrix is pinned
independently of parser computation; the second pass requires all 42 cells
to reproduce their domain, return, status, duration and success offset.

The success value **15 is an input offset**, not a claim that final application
probability is 15 percent. The original downstream StatusAttackCheck still
uses actor/target stats and explicit RNG, which this parser audit does not
execute. A decoded parameter description cannot override the native parser
result or silently change the profile's marker bytes.

## Remaining boundaries

This closes a conditional **parser** reference only. Target membership,
StatusChange success RNG/application, highest-active StatusRecovery mutation,
actor MP/item-pool provenance, initiative variants, round ordering, command
cancellation and persistent coordinator state remain separate runtime work.

Neither unsafe diagnostics nor a defined parser result constitute executable
Combined coverage. The five Combined skill slots remain outside accepted
pressure coverage until ordered runtime acceptance.
