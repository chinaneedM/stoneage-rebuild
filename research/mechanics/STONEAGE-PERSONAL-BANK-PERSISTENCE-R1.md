# StoneAge Personal Bank Persistence R1

Status: **fixed-descendant personal-bank mutation and save boundary closed**

## Scope

This pass isolates the player-owned `CHAR_BANKGOLD` subaccount from the broader family-bank package.

It answers four separate questions:

1. what the Bankman NPC itself does;
2. where personal deposit/withdraw mutation actually occurs;
3. how `CHAR_BANKGOLD` becomes durable character data;
4. how that path differs from the shared family treasury.

Evidence revisions:

- `gavinlinasd/StoneAge` @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`;
- `iriselia/StoneAge` @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`;
- `BismarckDD/stoneage` @ `999ffdf1d220ec6666eb65339180689c9caf1876`.

The recovered 2.5 world graph registers `FUNCTIONSET|Bankman|1`, proving the class is present in that specimen, but R1 does not infer launch-era chronology from later fixed source.

## Bankman is the UI adapter, not the mutation owner

The common Bankman callback opens the family/bank client protocol.

For the personal-account branch it sends:

```
B|G|<CHAR_BANKGOLD>
```

The NPC callback does not itself change either carried Gold or bank Gold.

A separate Bankman branch requests family-account data through SAAC. This is the first hard separation between the player-owned subaccount and the shared family treasury.

## Personal-bank mutation lives in FAMILY_Bank

Family-protocol dispatch routes the bank command to `FAMILY_Bank`.

Its `G` subcommand is the personal account.

Let:

- `cash = CHAR_GOLD`;
- `bank = CHAR_BANKGOLD`;
- `toBank` be the signed client amount.

The accepted mutation is:

```
new_cash = cash - toBank
new_bank = bank + toBank
```

Therefore:

- positive `toBank` = deposit carried Stone into personal bank;
- negative `toBank` = withdraw personal bank Stone into carried cash.

The server validates both projected balances before mutation.

## Access and family coupling

This personal account is not an unrestricted modern bank account.

The common gate rejects a player when both are true:

```
CHAR_FMINDEX <= 0
CHAR_BANKGOLD < 1
```

That creates a specific historical behavior:

- current family member: can open the account even at zero balance;
- non-member with zero balance: denied;
- former/non-member with residual personal-bank balance: can still access the account;
- positive deposits additionally require current family membership;
- a former member can therefore withdraw residual funds, but cannot add new deposits.

This coupling must be preserved in the archaeology model even if a future redesign chooses a cleaner standalone bank.

## Bounds

Every accepted personal transfer preserves:

```
0 <= new_cash <= CHAR_getMaxHaveGold(player)
0 <= new_bank <= CHAR_MAXBANKGOLDHAVE
```

The carried-Gold cap is queried dynamically through `CHAR_getMaxHaveGold`.

The fixed descendants disagree on the compiled bank ceiling:

- gavinlinasd / iriselia: `CHAR_MAXBANKGOLDHAVE = 1000 * 10000 = 10,000,000`;
- Bismarck fixed source: `CHAR_MAXBANKGOLDHAVE = 10000 * 10000 = 100,000,000`.

Bismarck also raises its compiled ordinary Gold constant relative to the older two branches.

These are **VERSIONED** constants, not a single timeless rule.

Bismarck's later personal-bank branch also routes a withdrawal underflow through an explicit error check, while gavinlinasd/iriselia reject the same invalid final state in the earlier compound bounds predicate. The accepted state space remains the same.

## Zero amount

The fixed predicate does not reject `toBank == 0`.

For an otherwise eligible account, zero therefore passes the personal branch and leaves balances unchanged. R1 preserves this literal source behavior rather than adding a modern nonzero validation.

## Shared family treasury is a different account

The `T` subcommand is not `CHAR_BANKGOLD`.

It operates on the family treasury state (`familyTax` in the fixed source), applies family-role checks, and sends a SAAC `ACFixFMData` request with the family-Gold field.

So reconstruction must keep:

```
G -> player-owned CHAR_BANKGOLD
T -> shared family treasury / SAAC family data
```

as distinct persistence domains.

## Persistence boundary

`CHAR_BANKGOLD` is an ordinary integer member of the character record.

The character integer-name table maps it to:

```
bankgld
```

`CHAR_makeStringFromCharData` serializes every integer field using that table. Standard character save then sends the resulting character blob to SAAC through `ACCharSave`.

The older SAAC parsing branch independently exposes `nbankgld=` when extracting player data, corroborating that the value is part of persistent character state.

### No synchronous save in FAMILY_Bank

The personal `G` branch:

- updates `CHAR_GOLD`;
- updates `CHAR_BANKGOLD`;
- sends Gold status;
- writes transaction logs;

but contains no `CHAR_charSave*` call.

Durability therefore occurs through the ordinary character-save lifecycle: periodic save and the other normal save/logout paths.

**FACT:** personal-bank mutation is persistent character state.

**FACT:** the bank operation itself does not synchronously commit that state to SAAC.

**CONSEQUENCE:** there is a normal deferred-save window between accepted bank mutation and the next character save. A reconstruction that adds immediate transactional durability would be an engineering redesign, not a literal statement about this fixed source.

## Other writers

Later source also contains additional `CHAR_BANKGOLD` writers in systems such as vendor/payment overflow and family/manor reward paths.

Those usages reinforce that `CHAR_BANKGOLD` is character-owned persistent money rather than the shared family treasury, but their package-specific reward/trade rules are outside this R1 Bankman seam.

## Evidence status

- **FACT:** Bankman opens the personal bank by sending current `CHAR_BANKGOLD`; it does not perform the balance mutation itself.
- **FACT:** `FAMILY_Bank` subcommand `G` performs the personal `CHAR_GOLD <-> CHAR_BANKGOLD` transfer.
- **FACT:** positive amount deposits and negative amount withdraws.
- **FACT:** projected carried cash and personal-bank balance must stay within their caps.
- **FACT:** current family membership is required for new positive deposits.
- **FACT:** a non-member with residual `CHAR_BANKGOLD` may still withdraw it.
- **FACT:** `CHAR_BANKGOLD` serializes as `bankgld` in the ordinary character record.
- **FACT:** the personal-bank mutation branch does not immediately call the character-save routine.
- **FACT:** shared family treasury mutation uses a separate `T` path and SAAC family-data update.
- **VERSIONED:** personal-bank and carried-Gold compile-time ceilings differ between the older two descendants and Bismarck.
- **VERSIONED:** Bismarck adds an explicit withdrawal-underflow error branch while preserving the same valid end-state constraint.
- **OPEN:** exact commercial introduction release of the family-coupled personal bank; fixed-source family comments are later than the 1999 launch and must not be projected backward without independent evidence.
- **OPEN:** exact recovered 2.5 Bankman configuration/dialogue semantics beyond the class registration already present in the world graph.

## Deterministic model

Repository artifacts:

- `tools/stoneage_personal_bank_model.py`;
- `tests/test_stoneage_personal_bank_model.py`;
- `.github/workflows/validate-stoneage-personal-bank.yml`.

The model covers the access gate, signed transfer semantics, projected-balance validation, former-member withdrawal behavior, versioned bank caps, command-domain split and deferred standard-character-save boundary.

## Priority consequence

The Bankman personal subaccount no longer justifies opening the whole family package.

Next, perform a fresh residual non-family NPC triage against the recovered 2.5 function set. Prefer classes with direct persistent mutation or ordinary economy/world-state effects; leave Raceman, Scheduleman, ManorSman, FMPK/FMWarp, family administration and VIP packages deferred unless a core dependency is discovered.
