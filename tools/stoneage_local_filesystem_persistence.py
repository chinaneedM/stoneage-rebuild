#!/usr/bin/env python3
"""Durable engine-neutral local persistence for StoneAge save payloads.

The store is intentionally schema-transparent: it persists opaque UTF-8 text
and leaves version/schema dispatch to LocalRuntimeSessionCoordinator.

Logical save keys are never interpolated into filesystem paths. Each key is
mapped to a SHA-256 filename inside one configured root directory.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import tempfile


LOCAL_FILESYSTEM_PERSISTENCE_PROFILE = (
    "STONEAGE_LOCAL_FILESYSTEM_PERSISTENCE_R1"
)
_SAVE_SUFFIX = ".save.json"


def _logical_key(value: object) -> str:
    key = str(value).strip()
    if not key:
        raise ValueError("local persistence key must be non-empty")
    return key


def _payload_text(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("local persistence payload must be text")
    return value


def _key_digest(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def _best_effort_fsync_directory(path: Path) -> None:
    """Persist the directory entry where the platform permits it."""

    flags = getattr(os, "O_RDONLY", 0)
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    fd = None
    try:
        fd = os.open(str(path), flags | directory_flag)
        os.fsync(fd)
    except OSError:
        # Windows and some filesystems do not permit directory fsync.
        pass
    finally:
        if fd is not None:
            os.close(fd)


@dataclass(frozen=True)
class LocalFilesystemPersistenceStore:
    """Filesystem-backed LocalPersistenceStore with atomic replacement."""

    root: Path

    profile_id = LOCAL_FILESYSTEM_PERSISTENCE_PROFILE

    def __post_init__(self) -> None:
        root = Path(self.root).expanduser().resolve(strict=False)
        root.mkdir(parents=True, exist_ok=True)
        if not root.is_dir():
            raise ValueError("local persistence root must be a directory")
        object.__setattr__(self, "root", root)

    def _slot_path(self, key: object) -> Path:
        logical = _logical_key(key)
        digest = _key_digest(logical)
        return self.root / f"{digest}{_SAVE_SUFFIX}"

    def save(self, key: str, payload: str) -> None:
        logical = _logical_key(key)
        text = _payload_text(payload)
        destination = self._slot_path(logical)
        raw = text.encode("utf-8")

        fd, temp_name = tempfile.mkstemp(
            prefix=f".{_key_digest(logical)}.",
            suffix=".tmp",
            dir=str(self.root),
        )
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(str(temp_path), str(destination))
            _best_effort_fsync_directory(self.root)
        except Exception:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass
            raise

    def load(self, key: str) -> str | None:
        path = self._slot_path(key)
        if not path.exists():
            return None
        if path.is_symlink():
            raise ValueError("local persistence slot must not be a symbolic link")
        if not path.is_file():
            raise ValueError("local persistence slot must be a regular file")
        try:
            return path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("local persistence slot is not valid UTF-8") from exc
