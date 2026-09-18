# StoneAge Save / Logout Persistence Core R1

Status: **strong convergent descendant evidence; later shared-depot persistence is versioned**  
Scope: ordinary character serialization, periodic/save-point saves, normal logout ordering, SAAC account unlocking, save acknowledgement and failure behavior.

## Why this seam matters

The project now reconstructs battle, death, recovery, inventory/equipment, trade and shop transitions. Those rules are incomplete unless we know which state survives reconnect and when state is considered durable.

The preserved server does **not** provide a modern strongly consistent persistence transaction.

Its ordinary design is:

```
runtime state
 -> serialize
 -> asynchronously send to SAAC
 -> SAAC writes account character file
```

Normal logout goes further:

```
cleanup runtime/character state
 -> asynchronously request save + unlock
 -> immediately delete in-memory character/pets
 -> receive save ACK later
```

A failed save acknowledgement does not reconstruct the destroyed runtime state or retry automatically.

## Evidence set

Fixed source revisions:

- **BismarckDD/stoneage** @ `999ffdf1d220ec6666eb65339180689c9caf1876`
  - `server/gmsv/char/char.c`
  - `server/gmsv/char/char_base.c`
  - `server/gmsv/net/net.c`
  - `server/gmsv/npc/npc_savepoint.c`
  - `server/common/saac_client_recv.c`
  - `server/saac/char.c`
- **gavinlinasd/StoneAge** @ `1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56`
  - corresponding GMSV/SAAC files
- **iriselia/StoneAge** @ `9e6c8ce2cd8ed532a7157773acd1c61582c178b5`
  - corresponding GMSV/SAAC files

## Character serialization surface

`CHAR_makeStringFromCharData` serializes the persistent character object.

The convergent core includes:

- every `CHAR_DATAINT` entry;
- every `CHAR_DATACHAR` string;
- persistent character flags;
- learned character skills;
- concrete carried/equipped item instances by slot;
- titles;
- address-book entries;
- every valid carried pet by pet slot.

Later builds also serialize pool/shared item and pet arrays when those systems are present.

### WORK fields are different

The serializer does **not** iterate `CHAR_WORK*` integer arrays.

Therefore concepts such as:

- battle runtime indices/modes;
- connection fd;
- trade runtime state;
- party runtime bookkeeping;
- channel membership runtime indices;
- many temporary timers/caches;

do not persist merely because they exist in the in-memory `Char` structure.

Some later features explicitly copy selected WORK values into persistent `CHAR_DATAINT` fields before logout. That is a feature-specific bridge, not evidence that WORK state itself is saved.

This separation is critical for the rebuild:

> Persistent character state and session/runtime state are distinct storage domains.

## Deserialization

Login reconstructs a fresh `Char` with defaults and then parses serialized keys back into:

- data integers/strings;
- flags;
- item instances;
- skills;
- titles;
- address book;
- carried pets;
- optional pool items/pets.

Item and pet strings create new runtime item/pet objects and place their indices into the reconstructed character.

Bismarck's fixed parser also enforces an end-of-data checkpoint more strictly than the older gavinlinasd/iriselia parser, whose equivalent rejection was commented in the fixed source.

This integrity checking is versioned; the serialized domains themselves are strongly convergent.

## Periodic autosave

The net loop contains `chardatasavecheck`.

The global scan runs only when:

```
NowTime.tv_sec > previous_scan + 10
```

For each connection, it saves only when all are true:

- connection is in use;
- connection state is `LOGIN`;
- `now - lastCharSaveTime > configured CharSaveinterval`.

The per-character comparison is also strict `>`, not `>=`.

After deciding to save, the code first updates `lastCharSaveTime = NowTime`, unlocks the connection mutex, then calls:

```
CHAR_charSaveFromConnect(fd, FALSE)
```

Thus periodic save requests carry:

```
unlock = FALSE
```

They keep the account/login lock held.

The setup file found in gavinlinasd contains `CharSaveinterval=180`, but that is a configuration value, not a universal engine constant. R1 models the interval as input.

## Save-point save

The save-point NPC updates persistent location/save-point related fields such as `CHAR_LASTTALKELDER` and save-point flags.

When the save-point configuration enables saving, it sends:

```
CHAR_charSaveFromConnectAndChar(fd, ch, FALSE)
```

Again:

```
unlock = FALSE
```

Therefore touching a record point can make current character state durable without ending the login lock/session.

## Save send is asynchronous

`CHAR_charSaveFromConnectAndChar`:

1. serializes the current character;
2. sends `ACCharSave` to SAAC;
3. returns TRUE immediately when the local serialization/send path was constructed.

It does **not** wait for SAAC to report successful disk persistence.

Therefore the GMSV return value means approximately:

> save request successfully formed/sent

not:

> durable character write confirmed.

This distinction applies to periodic/save-point saves as well as logout.

## Items deleted before logout save

Before normal logout serialization, `CHAR_dropItemAtLogout` iterates the entire item array.

Any item whose:

```
ITEM_DROPATLOGOUT == TRUE
```

is:

- logged as `LogoutDel`;
- removed from the character slot;
- its concrete item object destroyed.

Only after this cleanup does final logout serialization occur.

Therefore such items are intentionally absent from the persisted logout snapshot.

Despite the old field/comment name saying "drop", this function does not place the item on the map; it deletes the item instance.

## Normal logout ordering

Across all three fixed lineages, normal logout performs this core ordering.

### 1. Resolve active battle

If the character is in a battle:

- send escape/DP handling;
- add pending battle work EXP/point contribution into persistent duel-point state;
- exit the battle.

Bismarck also sets a later battle-escape WORK marker.

### 2. Remove logout-only items

Run `CHAR_dropItemAtLogout`.

### 3. Tear down runtime relationships

Common/largely convergent cleanup includes:

- discharge party;
- notify family/channel systems;
- remove chat/vendor/session references where enabled;
- pick up/remove follow-pet runtime state;
- clear runtime membership arrays.

Later feature cleanup is macro-controlled.

### 4. Convert selected runtime timers to persistent fields

Examples in later builds include silent-time and temporary EXP-effect handling.

These are explicit feature-specific copies/adjustments.

### 5. Set last-leave time

```
CHAR_LASTLEAVETIME = time(NULL)
```

This happens before the final save.

### 6. Send logout save

When `save == TRUE`:

```
CHAR_charSaveFromConnect(..., TRUE)
```

The `unlock` argument is TRUE.

### 7. Destroy runtime character

After **sending** the save request—not after receiving its acknowledgement—the server proceeds to:

- login/logout notification;
- destroy carried pet runtime objects;
- destroy the character runtime object.

Thus the runtime source of truth no longer exists while the storage write may still be in flight.

## Normal call sites use `save=TRUE`

Fixed ordinary logout/disconnect paths observed in all three lineages invoke:

```
CHAR_logout(..., TRUE)
```

This includes normal client logout and network disconnect cleanup.

The function supports a `save` boolean, but no ordinary fixed logout/disconnect call site using `FALSE` was found in this audit.

R1 therefore treats `save=FALSE` as an available internal API branch, not a normal player-session rule.

## SAAC logout-save ordering

The account server's `charSave` has a particularly important ordering.

When:

```
unlock == TRUE
```

it first performs the account/user unlock operation.

Only afterward does it:

1. build/validate the combined save string;
2. resolve the character slot;
3. call the character-file write;
4. return SUCCESSFUL/FAILED to GMSV.

So the source ordering is:

```
unlock account
 -> construct save envelope
 -> resolve character slot
 -> write character file
 -> send save result
```

The account is therefore unlocked **before durable character write is known to have succeeded**.

This is not a modern safe commit protocol.

## Logout save acknowledgement

When GMSV later receives the SAAC result in state `WHILELOGOUTSAVE`:

- SUCCESSFUL -> tell client `success`;
- failure -> tell client `Cannot save`.

In **both** cases it then:

- sets connection state to `NOTLOGIN`;
- sets character index to `-1`.

There is no branch that:

- retries the save;
- recreates the destroyed character;
- restores the old account lock;
- rolls back logout cleanup.

The runtime character was already deleted by `_CHAR_logout`.

Therefore an actual disk-write failure after logout carries genuine last-state loss risk.

## Why this matters for the modern rebuild

For historical reconstruction, preserve these facts.

For a modern implementation, this is a clear candidate for intentional improvement:

```
old visible semantics
 + durable transaction/snapshot
 + write acknowledgement
 + unlock only after committed save
```

That can preserve game behavior without inheriting the old crash/data-loss window.

The project should keep those two statements separate:

- **historical rule:** old server was asynchronous and weakly durable;
- **future design option:** rebuild can provide stronger persistence guarantees.

## Shared depot/pet storage is later

The earlier candidate seam, account-shared pet storage, is controlled by macros such as:

- `_CHAR_POOLPET`;
- `_NPC_DEPOTPET`.

The preserved generated version text explicitly presents it as an optional later shared pet warehouse, with 30 depot pet slots in these branches.

It is therefore not promoted into the early persistence core merely because current descendants support it.

The same separation applies to shared item depot persistence.

## Deterministic model

Repository artifacts:

- `tools/stoneage_save_logout_model.py`
- `tests/test_stoneage_save_logout_model.py`
- `.github/workflows/validate-stoneage-save-logout.yml`

Regression coverage includes:

- strict 10-second periodic sweep gate;
- strict configured autosave interval;
- periodic/save-point `unlock=FALSE`;
- logout `unlock=TRUE`;
- serialization surfaces versus WORK/runtime fields;
- optional shared pool serialization;
- deletion of DROPATLOGOUT items before snapshot;
- battle/cleanup/save/runtime-destruction ordering;
- SAAC unlock-before-write ordering;
- asynchronous send semantics;
- failure acknowledgement with no retry/rollback;
- ordinary fixed logout call sites using save=TRUE.

## Evidence status

- **FACT:** character save serializes persistent data/string fields, flags, skills, items, titles, address book and carried pets.
- **FACT:** generic WORK/runtime arrays are not part of the character serializer.
- **FACT:** periodic save is controlled by configurable interval and uses `unlock=FALSE`.
- **FACT:** save-point save uses `unlock=FALSE`.
- **FACT:** save-send functions return before SAAC persistence acknowledgement.
- **FACT:** `ITEM_DROPATLOGOUT` items are destroyed before the logout snapshot.
- **FACT:** normal logout performs cleanup/state conversion before final save.
- **FACT:** fixed ordinary logout/disconnect call sites pass `save=TRUE`.
- **FACT:** final logout save passes `unlock=TRUE`.
- **FACT:** SAAC unlocks the account before attempting the character-file write.
- **FACT:** runtime character/pet objects are deleted immediately after sending the logout-save request.
- **FACT:** failed ordinary logout save returns `Cannot save` with no automatic retry or runtime rollback.
- **VERSIONED:** strict DATAEND parsing, shared depot arrays, online-time/timed-effect persistence bridges and other later fields.
- **OPEN:** exact 1999/early-1.x save schema size and every field present in the commercial build.
- **OPEN:** production operational mitigations outside source (backups, watchdogs, manual restoration, filesystem semantics).
- **OPEN:** exact chronology of shared item/pet depot extensions.

## Next technical seam

With persistence boundaries explicit, the ordinary deterministic loop is now substantially closed from runtime action through durable character state. The next step should be a **fresh milestone/gap audit**, not blindly adding later systems. Candidate gaps should be classified as:

1. early/core mechanics still missing;
2. later but historically important optional systems;
3. data/content extraction gaps;
4. future modern-rebuild engineering improvements.

That audit should choose the next seam from evidence rather than from feature popularity.
