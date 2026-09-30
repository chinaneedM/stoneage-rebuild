#!/usr/bin/env python3
"""Recovered25 pet-skill runtime index for local reconstruction.

Only execution-facing fields are retained from the verified local data:
ID/FIELD/TARGET/COST/ILLEGAL plus FUNCNAME and raw OPTION bytes. Display names,
comments, FREE/KINDCODE text and trailing preservation columns are deliberately
not retained.

The active recovered25 specimen uses the _CFREE_petskill six-string prefix.
petskillfile1/petskillfile2 are compile-time alternatives in the fixed source;
when both keys are present this loader requires them to resolve to the same
file rather than guessing the build macro.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_singleplayer_world import LATER_RECOVERED


SOURCE_VERSION = "recovered25"
CHAR_FIELDS = 6
INT_FIELDS = ("ID", "FIELD", "TARGET", "COST", "ILLEGAL")
MIN_FIELDS = CHAR_FIELDS + len(INT_FIELDS)

STABLE_COMMON_CALLBACKS = frozenset(
    {
        "PETSKILL_None",
        "PETSKILL_NormalAttack",
        "PETSKILL_NormalGuard",
        "PETSKILL_ContinuationAttack",
        "PETSKILL_ChargeAttack",
        "PETSKILL_Guardian",
        "PETSKILL_PowerBalance",
        "PETSKILL_Mighty",
        "PETSKILL_StatusChange",
        "PETSKILL_EarthRound",
        "PETSKILL_GuardBreak",
        "PETSKILL_Abduct",
        "PETSKILL_Steal",
        "PETSKILL_Merge",
        "PETSKILL_NoGuard",
    }
)


def _source_int(token: bytes) -> int:
    token = token.strip()
    if not token:
        return -1
    try:
        return int(token, 10)
    except ValueError as exc:
        raise ValueError("pet-skill integer field is not decimal") from exc


def _setup_skill_paths(setup: Path | None) -> tuple[str, ...]:
    if setup is None:
        return ()
    setup = Path(setup)
    if not setup.is_file():
        raise ValueError("recovered25 pet-skill setup must be a file")
    values = []
    for raw in setup.read_bytes().splitlines():
        line = raw.split(b"#", 1)[0].strip()
        if b"=" not in line:
            continue
        key, value = line.split(b"=", 1)
        key = key.decode("ascii", "ignore").strip().lower()
        if key not in {"petskillfile1", "petskillfile2"}:
            continue
        value = value.decode("utf-8", "replace").strip()
        if value:
            values.append(Path(value.replace("\\", "/")).name)
    return tuple(values)


@dataclass(frozen=True)
class Recovered25PetSkillEntry:
    skill_id: int
    field: int
    target: int
    cost: int
    illegal: int
    function_name: str
    option_bytes: bytes

    def __post_init__(self) -> None:
        object.__setattr__(self, "skill_id", int(self.skill_id))
        object.__setattr__(self, "field", int(self.field))
        object.__setattr__(self, "target", int(self.target))
        object.__setattr__(self, "cost", int(self.cost))
        object.__setattr__(self, "illegal", int(self.illegal))
        function_name = str(self.function_name)
        if not function_name:
            raise ValueError("pet-skill callback name must be non-empty")
        object.__setattr__(self, "function_name", function_name)
        object.__setattr__(self, "option_bytes", bytes(self.option_bytes))

    @property
    def stable_common_callback(self) -> bool:
        return self.function_name in STABLE_COMMON_CALLBACKS

    def ascii_option(self) -> str:
        """Decode only when a reconstructed handler proves an ASCII grammar."""
        try:
            return self.option_bytes.decode("ascii", "strict")
        except UnicodeDecodeError as exc:
            raise ValueError(
                "pet-skill OPTION is not ASCII; encoding-dependent parser required"
            ) from exc

    def unambiguous_cp950_big5_option(self) -> str:
        """Decode OPTION only when both plausible recovered codecs agree.

        The recovered25 bundle still contains unresolved CP950/Big5 text
        provenance. Mechanics may consume OPTION text only when strict decoding
        succeeds under both codecs and yields exactly the same Unicode string.
        """

        try:
            cp950 = self.option_bytes.decode("cp950", "strict")
            big5 = self.option_bytes.decode("big5", "strict")
        except UnicodeDecodeError as exc:
            raise ValueError(
                "pet-skill OPTION cannot be decoded strictly by both CP950 "
                "and Big5"
            ) from exc
        if cp950 != big5:
            raise ValueError(
                "pet-skill OPTION has unresolved CP950/Big5 decoding divergence"
            )
        return cp950



@dataclass(frozen=True)
class Recovered25PetSkillRuntime:
    skills: Mapping[int, Recovered25PetSkillEntry]
    source_file: str
    source_version: str = SOURCE_VERSION
    evidence_role: str = LATER_RECOVERED

    def __post_init__(self) -> None:
        if self.source_version != SOURCE_VERSION:
            raise ValueError("pet-skill runtime source-version drift")
        if self.evidence_role != LATER_RECOVERED:
            raise ValueError("pet-skill runtime must remain LATER_RECOVERED")
        source_file = str(self.source_file).strip()
        if not source_file:
            raise ValueError("pet-skill runtime source file must be non-empty")
        normalized = {int(key): value for key, value in self.skills.items()}
        for key, entry in normalized.items():
            if key != int(entry.skill_id):
                raise ValueError(
                    f"pet-skill runtime key {key} != ID {entry.skill_id}"
                )
        object.__setattr__(self, "source_file", source_file)
        object.__setattr__(self, "skills", MappingProxyType(normalized))

    def unresolved_skill_ids(self, skill_ids) -> tuple[int, ...]:
        return tuple(
            sorted(
                {
                    int(skill_id)
                    for skill_id in skill_ids
                    if int(skill_id) > 0
                    and int(skill_id) not in self.skills
                }
            )
        )


def _active_petskill_path(data_dir: Path, setup: Path | None) -> Path:
    data_dir = Path(data_dir)
    configured = _setup_skill_paths(setup)
    existing = tuple(
        name
        for name in configured
        if (data_dir / name).is_file()
    )
    unique = tuple(dict.fromkeys(existing))
    if len(unique) > 1:
        raise ValueError(
            "petskillfile1/petskillfile2 resolve to different existing files; "
            "build macro is unresolved"
        )
    if unique:
        return data_dir / unique[0]
    fallback = data_dir / "petskill.txt"
    if fallback.is_file():
        return fallback
    raise ValueError("active recovered25 pet-skill file not found")


def load_recovered25_petskill_runtime(
    *,
    data_dir: Path,
    setup: Path | None = None,
) -> Recovered25PetSkillRuntime:
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise ValueError("recovered25 pet-skill data_dir must be a directory")

    path = _active_petskill_path(data_dir, setup)
    skills: dict[int, Recovered25PetSkillEntry] = {}
    for raw in path.read_bytes().splitlines():
        line = raw.strip()
        if not line or line.startswith(b"#"):
            continue
        fields = [
            token.strip()
            for token in line.replace(b"\t", b" ").split(b",")
        ]
        if len(fields) < MIN_FIELDS:
            raise ValueError(
                "active recovered25 pet-skill row is shorter than "
                "six-string-prefix schema"
            )
        try:
            function_name = fields[2].decode("ascii", "strict")
        except UnicodeDecodeError as exc:
            raise ValueError(
                "active recovered25 pet-skill callback is not ASCII"
            ) from exc
        values = tuple(
            _source_int(fields[CHAR_FIELDS + index])
            for index in range(len(INT_FIELDS))
        )
        entry = Recovered25PetSkillEntry(
            skill_id=values[0],
            field=values[1],
            target=values[2],
            cost=values[3],
            illegal=values[4],
            function_name=function_name,
            option_bytes=fields[3],
        )
        if entry.skill_id in skills:
            raise ValueError(
                f"duplicate recovered25 pet-skill ID {entry.skill_id}"
            )
        skills[entry.skill_id] = entry

    if not skills:
        raise ValueError("active recovered25 pet-skill runtime is empty")
    return Recovered25PetSkillRuntime(
        skills=skills,
        source_file=path.name,
    )
