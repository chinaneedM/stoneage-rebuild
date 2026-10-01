# StoneAge AttackMagic command / target / DirectUse boundary R1

Date: 2026-10-01

## Scope

This reconstruction is deliberately narrower than a full attack-magic damage
implementation. It closes the recovered25 pet-skill command encoding, fixed
target-selector rewrite, and the arguments handed to `MAGIC_DirectUse`.
It does **not** claim that the downstream `MAGIC_AttMagic_Battle` /
`BATTLE_MultiAttMagic` damage core has already been reconstructed.

Pinned descendant controls:

- gavinlinasd/StoneAge `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- iriselia/StoneAge `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- BismarckDD/stoneage `999ffdf1d220ec6666eb65339180689c9caf1876`.

These are descendant implementation evidence, not launch-era Taiwan-v1 proof.

## Fixed-source facts

All three pinned branches compile their AttackMagic feature guard and converge
on the same command/execution skeleton:

1. `PETSKILL_AttackMagic` selects `BATTLE_COM_S_ATTACK_MAGIC`;
2. COM2 receives the requested battle target;
3. LOW(COM3) receives the magic ID;
4. the battle executor reads LOW(COM3), rewrites target shape from a 25-entry
   magic-ID table, then calls `MAGIC_DirectUse`;
5. the guarded enum layout places `BATTLE_COM_S_ATTACK_MAGIC` at numeric
   command value **2002**.

The exact target table is:

```text
301 -1   302 -1   303 26   304 -1   305 20
306 20   307 -1   308 -1   309 -1   310 -1
311 26   312 20   313 -1   314 -1   315 -1
316 -1   317 26   318 20   319 -1   320 -1
321 26   322 -1   323 26   324 20   325 20
```

For area 26, original targets 0..4 remain selector 26 and other battle slots
become selector 25. For area 20, the fixed gavin/iris behavior selects 20.
Bismarck contains an optional `_OPEN_E_PETSKILL` side-aware 20/21 branch, but
that macro is not defined in the pinned Bismarck `version.h`; it is preserved
as an explicit optional version layer rather than projected into recovered25.

## HIGH(COM3) divergence

The descendant HIGH(COM3) encoding divergence is real and remains versioned:

- gavin/iris initialize `magic=313`, `item=19659`, parse `magic`, then
  search for `item` from the advanced source pointer and write the resulting
  item value to HIGH(COM3);
- Bismarck retains the magic parse but comments out the item parse and the
  HIGH(COM3) write. Its LOW-half setter therefore preserves whatever high-half
  state already existed.

The command encoding diverges, but a later source audit narrows its runtime
effect for **non-player AttackMagic**. `MAGIC_DirectUse` does pass `itemnum`
straight to the dynamic existing-item table, while the recovered 196xx values
are configuration IDs and are not guaranteed existing-item instance indexes.
However an invalid `ITEM_getInt(..., ITEM_MAGICUSEMP)` returns a negative MP
value without aborting; `MAGIC_AttMagic` skips MP check/deduction for
non-player casters; and `MAGIC_AttMagic_Battle` does not read its `mp`
argument. Thus HIGH(COM3) is provenance-significant but **execution-dead for
non-player AttackMagic footprint/damage** in the pinned descendants.

The gavin/iris missing-`magic` path is also not normalized: their second
`strstr` reuses the pointer returned by the first `strstr("magic")`. If that
first search fails, the historical C cursor becomes invalid/undefined. The
reference model fails closed at that boundary instead of inventing a safe
fallback.

## Direct recovered25 evidence

The preservation-bundle probe and full runtime-stack validation establish:

- AttackMagic population: **25 unique skill IDs / 106 positive enemybase slot uses**;
- all **25/25** rows are FIELD=BATTLE, ILLEGAL=0, ASCII, and strict CP950/Big5
  decode-identically;
- all **25/25** rows contain a numeric `magic` marker followed by a numeric
  `item` marker;
- no recovered row places `item` before `magic`;
- magic IDs are exactly **301..325**, 25 distinct values;
- item IDs are exactly **19647..19671**, 25 distinct values;
- same-row pairing is complete **25/25**;
- the observed pair delta is uniformly **item - magic = 19346**.

The uniform delta is an observed population property only. R1 does **not**
promote it to a general derivation rule; recovered25 execution reads each
explicit item value from the recovered option row.

Validation source commit `ccb037e4ae105c48a2dc44fb514eae84dd5ca9c7`
passed recovered25 region/runtime-stack workflow **36842103889**. The derived
report write-back advanced `main` to
`537d98ae3088e457cb028d4eccf815556bc40559`.

## Reconstruction policy

`tools/stoneage_attack_magic_model.py` keeps three named profiles:

- `RECOVERED25_EXPLICIT_ITEM`: requires numeric magic and item markers and
  uses the recovered explicit item as HIGH(COM3);
- `GAVIN_IRIS_ITEM_HIGH`: preserves the earlier explicit/default item write,
  while failing closed for the invalid missing-magic cursor case;
- `BISMARCK_HIGH_RESIDUE`: preserves prior HIGH(COM3) and does not consume
  the option's item token.

The model then projects the encoded command through the fixed target table to
a `MagicDirectUseRequest(magic_id, target, item_index)`. It stops there.

## Evidence boundary

**FACT:** recovered25 supplies the explicit item token for every AttackMagic
row and those tokens cross-link 25/25 to the corresponding item configuration.
For non-player AttackMagic, the later MP value derived from HIGH(COM3) is
execution-dead before footprint/damage.

**VERSIONED:** Bismarck's removed item write/high-half residue behavior is kept
as its own descendant profile rather than overwritten.

**DESIGN:** recovered25 uses the explicit-item profile because it preserves all
directly recovered fields and avoids throwing away 25/25 observed item tokens.

**CLOSED DOWNSTREAM LAYERS:** the recovered magic/item/IDX cross-link,
`attmagic.bin` footprint geometry, and active `_FIX_MAGICDAMAGE` arithmetic
were subsequently reconstructed and independently validated. Runtime admission
still fails closed whenever the historical right-down `SortLoc/qsort` target
order is nonportable.

Marker: **RECOVERED25_ATTACKMAGIC_COMMAND_BOUNDARY_R1 = CLOSED**


## Non-player item-token semantic correction — 2026-10-01

- gavin/iris fixed builds leave `_IMPOROVE_ITEMTABLE` disabled; Bismarck uses an explicit item-ID-to-template-row index. Neither mechanism makes recovered configuration ID `196xx` an authoritative dynamic existing-item instance index.
- Existing-item allocation uses a rotating free-slot `Sindex`, so instance identity is runtime-dependent.
- `MAGIC_DirectUse` does not abort on a negative item-derived MP value.
- `MAGIC_AttMagic` explicitly does not consume MP for non-player casters.
- `MAGIC_AttMagic_Battle` ignores its `mp` argument.
- Therefore recovered item IDs remain required cross-link/provenance evidence but are not used as runtime instance addresses in the reconstructed non-player AttackMagic path.
