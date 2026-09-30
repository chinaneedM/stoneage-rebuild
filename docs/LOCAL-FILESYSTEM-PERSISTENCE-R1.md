# Local Filesystem Persistence R1

## Status

**DESIGN / IMPLEMENTED.** This is the minimal durable implementation of the engine-neutral `LocalPersistenceStore` port used by the single-player runtime.

Canonical implementation:

- `tools/stoneage_local_filesystem_persistence.py`
- `tests/test_stoneage_local_filesystem_persistence.py`

Storage profile: `STONEAGE_LOCAL_FILESYSTEM_PERSISTENCE_R1`.

## 1. Scope

The store persists opaque UTF-8 payload text and does not understand StoneAge save schemas.

Schema/version validation remains above this layer in `LocalRuntimeSessionCoordinator`. Therefore the same storage implementation can hold both the current `stoneage.local-runtime-save.r1` envelope and legacy `stoneage.local-runtime-session.r1` payloads without changing compatibility policy.

No cloud sync, accounts, multiplayer transport, launcher, renderer or engine dependency is introduced.

## 2. Logical-key mapping

A caller supplies a logical save key. After non-empty normalization, the UTF-8 key is SHA-256 hashed and stored as:

`<64-hex-digest>.save.json`

inside one configured root directory.

The raw logical key is never concatenated into the path. Strings containing separators or traversal syntax therefore remain ordinary logical identifiers and cannot escape the configured root.

This filename hash is an addressing mechanism, not a security secret or integrity signature.

## 3. Atomic replacement

A save operation:

1. encodes the payload as UTF-8 bytes;
2. creates a temporary file in the same directory as the destination;
3. writes the complete payload;
4. flushes and `fsync`s the temporary file;
5. replaces the destination using `os.replace`;
6. performs best-effort directory `fsync` on platforms/filesystems that support it.

Using the same directory keeps the replace operation on one filesystem. The store cleans up the temporary file if a pre-replace write fails.

This is a local durability boundary, not a transactional multi-slot database.

## 4. Exact payload semantics

The store writes binary UTF-8 bytes and decodes UTF-8 bytes on load. It does not normalize newlines, reorder JSON, alter Unicode text or parse/re-serialize content.

Missing slots return `None` as required by the persistence protocol.

Non-regular or symbolic-link destination slots are rejected on load. Invalid UTF-8 is rejected rather than replaced or silently repaired.

## 5. Evidence and provenance boundary

This component is purely reconstruction infrastructure. It makes no claim about historical StoneAge save-file formats and does not reproduce a legacy client/server persistence mechanism.

Historical/recovered provenance remains inside the versioned runtime and save-state contracts above this storage adapter.


## 6. Integration smoke

The durable store is exercised through the real coordinator save/continue boundary across two separately constructed coordinator instances sharing only the filesystem root. The smoke preserves a session world flag, a moved baseline NPC and a newly created non-overable live item, proving that disk persistence composes with the versioned occupancy-delta contract rather than merely round-tripping opaque strings in isolation.
