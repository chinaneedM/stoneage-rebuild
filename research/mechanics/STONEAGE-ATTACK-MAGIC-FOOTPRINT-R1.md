# StoneAge AttackMagic footprint geometry R1

Date: 2026-10-01

## Scope

This layer reconstructs the fixed-descendant `BATTLE_MultiAttMagic` target footprint before per-target dodge/damage execution. It covers battle-slot geometry, `attmagic.bin` side-record selection, `siField[3][5]` expansion, `BATTLE_MultiList` retarget/fallback behavior relevant to AttackMagic, and the historical `SortLoc` boundary.

Pinned descendant controls remain gavin `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`, iris `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`, and Bismarck `999ffdf1d220ec6666eb65339180689c9caf1876`. The geometry and primary footprint code converge across all three; this is descendant evidence, not launch-era Taiwan-1.0 proof.

## Battle-slot geometry

All three define the same 4x5 table:

```text
row 0: 13 11 10 12 14
row 1: 18 16 15 17 19
row 2:  8  6  5  7  9
row 3:  3  1  0  2  4
```

Selectors are 20 side-0, 21 side-1, 22 all, 23 side-1 back row, 24 side-1 front row, 25 side-0 front row, and 26 side-0 back row. The recovered AttackMagic `TargetIndex` table emits only single slots, 20, 25, or 26; it does not emit 22.

## `attmagic.bin` adjacent side pairs

The loader divides raw record count by two to obtain the number of magic indices, but does not discard half of the array. `BATTLE_MultiAttMagic` selects `IDX*2+1` for attacker slots 0..9 and `IDX*2` for attacker slots 10..19. Therefore the recovered 54-record file represents 27 adjacent side-specific pairs. The earlier R1 probe's records[i] versus records[i+27] statistic did not represent execution pairing. R2 reports adjacent-pair semantics and evaluates all 54 records.

## Matrix and retargeting

`tagAttMagic` ends in `int siField[3][5]`, words 18..32 of each 132-byte record. Single targets anchor the matrix at their `CharTableIdx` coordinate; the source walks `base_y-1..base_y+1`, clips to the target side's two rows, and maps five relative columns around `base_x`. Selectors 20/21 apply the first two matrix rows to the side's two battle rows. Selectors 23..26 use the same clipped three-row walk across all five columns.

Before this expansion, `BATTLE_MultiList` can retarget a dead single target within its own side using rejection sampling over `rand()%10`, or fall an empty row selector back to the other row on the same side. R1 therefore injects retarget rolls rather than choosing a replacement silently.

## Historical `SortLoc` boundary

After footprint construction the source calls `qsort(..., SortLoc)`. The left-up (`slot >= 10`) branch is conventional. The right-down branch converges on `return ele2basex - ele1basey;`, mixing X from the second target with Y from the first. The model does not repair it.

For affected right-down multi-target sets this comparator can violate the sorting contract: slot 0 versus 1 and 1 versus 0 can both compare negative, and some self-comparisons are non-zero. Exact qsort output is therefore libc/implementation dependent, and that matters because dodge/damage RNG is consumed in sorted target order.

R1 reconstructs target membership exactly, exposes the exact comparator, returns a source order only when the comparator is a strict ordering for the concrete set, and otherwise returns no portable sorted order. Runtime composition must fail closed at that ordering boundary unless a specific legacy qsort/ABI is established or a later explicit modern-design order is chosen.

Marker: `FIXED_DESCENDANT_ATTACKMAGIC_FOOTPRINT_GEOMETRY_R1 = CANDIDATE`
