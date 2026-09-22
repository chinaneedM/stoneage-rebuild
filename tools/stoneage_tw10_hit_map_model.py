#!/usr/bin/env python3
"""Taiwan StoneAge v1.0 client hit-map reconstruction model.

The image collision attributes come from the accepted retail client's
80-byte ADRN records. The algorithm mirrors the stable client readHitMap path
used to derive the local hitMap from tile / parts / event planes.

This is separate from the descendant server WALKABLE/HAVEHEIGHT model.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
import gzip
from pathlib import Path
import struct
from types import MappingProxyType
from typing import Mapping, Sequence


CG_INVISIBLE = 99
MAP_SEE_FLAG = 0x4000
EVENT_TYPE_MASK = 0x0FFF
EVENT_NPC = 1

HIT_PASSABLE = 0
HIT_BLOCKED = 1
HIT_OVERRIDE = 2


@dataclass(frozen=True)
class TaiwanV10CollisionAttr:
    map_number: int
    bitmapno: int
    atari_x: int
    atari_y: int
    hit_raw: int
    height_flag: int = 0

    def __post_init__(self) -> None:
        for name in (
            "map_number",
            "bitmapno",
            "atari_x",
            "atari_y",
            "hit_raw",
            "height_flag",
        ):
            object.__setattr__(self, name, int(getattr(self, name)))
        if self.atari_x < 0 or self.atari_y < 0:
            raise ValueError("ADRN collision footprint dimensions must be non-negative")

    @property
    def hit_flag(self) -> int:
        return self.hit_raw % 100

    @property
    def priority_type(self) -> int:
        return self.hit_raw // 100


@dataclass(frozen=True)
class TaiwanV10CollisionProfile:
    by_map_number: Mapping[int, TaiwanV10CollisionAttr]

    def __post_init__(self) -> None:
        normalized = {int(key): value for key, value in self.by_map_number.items()}
        for key, attr in normalized.items():
            if key != attr.map_number:
                raise ValueError(
                    f"collision mapping key {key} does not match map_number "
                    f"{attr.map_number}"
                )
        object.__setattr__(self, "by_map_number", MappingProxyType(normalized))

    def resolve(self, map_number: int) -> TaiwanV10CollisionAttr:
        map_number = int(map_number)
        if map_number not in self.by_map_number:
            raise KeyError(f"unresolved Taiwan v1.0 map image number {map_number}")
        return self.by_map_number[map_number]


_COLLISION_PROFILE_REQUIRED_COLUMNS = frozenset(
    {
        "map_number",
        "bitmapno",
        "atari_x",
        "atari_y",
        "hit_raw",
        "hit_flag",
        "priority_type",
        "height_flag",
    }
)


def load_taiwan_v10_collision_profile(
    path: str | Path,
) -> TaiwanV10CollisionProfile:
    """Load the derived Taiwan-v1 collision TSV without original ADRN bytes."""
    rows: dict[int, TaiwanV10CollisionAttr] = {}
    with gzip.open(Path(path), "rt", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        columns = set(reader.fieldnames or ())
        missing = _COLLISION_PROFILE_REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(
                "collision metadata is missing required columns: "
                + ", ".join(sorted(missing))
            )

        for line_number, row in enumerate(reader, start=2):
            map_number = int(row["map_number"])
            if map_number <= 0:
                raise ValueError(
                    f"collision metadata line {line_number} has non-positive map_number"
                )
            if map_number in rows:
                raise ValueError(
                    f"collision metadata contains duplicate map_number {map_number}"
                )
            attr = TaiwanV10CollisionAttr(
                map_number=map_number,
                bitmapno=int(row["bitmapno"]),
                atari_x=int(row["atari_x"]),
                atari_y=int(row["atari_y"]),
                hit_raw=int(row["hit_raw"]),
                height_flag=int(row["height_flag"]),
            )
            if int(row["hit_flag"]) != attr.hit_flag:
                raise ValueError(
                    f"collision metadata line {line_number} has inconsistent hit_flag"
                )
            if int(row["priority_type"]) != attr.priority_type:
                raise ValueError(
                    f"collision metadata line {line_number} has inconsistent priority_type"
                )
            rows[map_number] = attr

    if not rows:
        raise ValueError("collision metadata contains no map-number rows")
    return TaiwanV10CollisionProfile(rows)


@dataclass(frozen=True)
class TaiwanV10HitMap:
    width: int
    height: int
    cells: tuple[int, ...]

    def __post_init__(self) -> None:
        width = int(self.width)
        height = int(self.height)
        if width < 1 or height < 1:
            raise ValueError("hit-map dimensions must be positive")
        if len(self.cells) != width * height:
            raise ValueError("hit-map cell count does not match dimensions")
        if any(int(value) not in (0, 1, 2) for value in self.cells):
            raise ValueError("hit-map values must be 0, 1 or 2")
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "cells", tuple(int(x) for x in self.cells))

    def value_at(self, x: int, y: int) -> int:
        x, y = int(x), int(y)
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("hit-map coordinate outside bounds")
        return self.cells[y * self.width + x]

    def blocked_at(self, x: int, y: int) -> bool:
        # v1 checkHitMap blocks only value 1. Value 2 is an override marker.
        return self.value_at(x, y) == HIT_BLOCKED


@dataclass(frozen=True)
class StoneAgeDatMapCache:
    """Strict three-plane map\\%d.dat cache representation.

    The binary layout is descendant-source-corroborated. A successfully parsed
    cache is not, by itself, evidence that its payload belongs to Taiwan v1.0.
    Provenance must be established independently before historical use.
    """

    width: int
    height: int
    tile: tuple[int, ...]
    parts: tuple[int, ...]
    event: tuple[int, ...]

    def __post_init__(self) -> None:
        width = int(self.width)
        height = int(self.height)
        if width < 1 or height < 1:
            raise ValueError("map-cache dimensions must be positive")
        size = width * height

        normalized = {}
        for name in ("tile", "parts", "event"):
            plane = tuple(int(value) for value in getattr(self, name))
            if len(plane) != size:
                raise ValueError(
                    f"map-cache {name} plane length does not match width*height"
                )
            if any(value < 0 or value > 0xFFFF for value in plane):
                raise ValueError(f"map-cache {name} values must fit uint16")
            normalized[name] = plane

        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        for name, plane in normalized.items():
            object.__setattr__(self, name, plane)


def parse_stoneage_dat_map_cache(
    data: bytes | bytearray | memoryview,
) -> StoneAgeDatMapCache:
    """Parse the exact width/height + tile/parts/event uint16 cache layout."""
    raw = bytes(data)
    if len(raw) < 8:
        raise ValueError("map cache is shorter than its 8-byte header")
    width, height = struct.unpack_from("<II", raw, 0)
    if width < 1 or height < 1:
        raise ValueError("map-cache dimensions must be positive")
    cells = width * height
    expected = 8 + cells * 2 * 3
    if len(raw) != expected:
        raise ValueError(
            f"map-cache size {len(raw)} does not match expected {expected}"
        )
    values = struct.unpack_from(f"<{cells * 3}H", raw, 8)
    return StoneAgeDatMapCache(
        width=width,
        height=height,
        tile=tuple(values[:cells]),
        parts=tuple(values[cells : cells * 2]),
        event=tuple(values[cells * 2 :]),
    )


def _validate_planes(
    width: int,
    height: int,
    tile: Sequence[int],
    parts: Sequence[int],
    event: Sequence[int],
) -> int:
    width, height = int(width), int(height)
    if width < 1 or height < 1:
        raise ValueError("map dimensions must be positive")
    size = width * height
    if len(tile) != size or len(parts) != size or len(event) != size:
        raise ValueError("tile/parts/event planes must match width*height")
    return size


def _direct_small_code(
    value: int,
    event_value: int,
    current: int,
    *,
    tile_plane: bool,
) -> int:
    value = int(value)
    if value == 0:
        if not tile_plane:
            return current
        if (int(event_value) & MAP_SEE_FLAG) == 0:
            return current
    if value in (0, 1, 2, 5, 6, 9, 10):
        return HIT_BLOCKED if current != HIT_OVERRIDE else current
    if value == 4:
        return HIT_OVERRIDE
    return current


def _apply_footprint(
    hit_map: list[int],
    *,
    width: int,
    row: int,
    col: int,
    footprint_x: int,
    footprint_y: int,
    value: int,
    preserve_override: bool,
) -> None:
    for k in range(int(footprint_y)):
        for l in range(int(footprint_x)):
            y = row - k
            x = col + l
            if y < 0 or x >= width:
                continue
            index = y * width + x
            if preserve_override and hit_map[index] == HIT_OVERRIDE:
                continue
            hit_map[index] = int(value)


def build_taiwan_v10_hit_map(
    *,
    width: int,
    height: int,
    tile: Sequence[int],
    parts: Sequence[int],
    event: Sequence[int],
    profile: TaiwanV10CollisionProfile,
) -> TaiwanV10HitMap:
    """Mirror the v1-compatible readHitMap ordering from tile/parts/event."""
    size = _validate_planes(width, height, tile, parts, event)
    width, height = int(width), int(height)
    hit_map = [HIT_PASSABLE] * size

    # Tile pass.
    for i in range(height):
        for j in range(width):
            index = i * width + j
            value = int(tile[index])
            if value > CG_INVISIBLE or 60 <= value <= 79:
                hit = profile.resolve(value).hit_flag
                if hit == 0 and hit_map[index] != HIT_OVERRIDE:
                    hit_map[index] = HIT_BLOCKED
                elif hit == 2:
                    hit_map[index] = HIT_OVERRIDE
            else:
                hit_map[index] = _direct_small_code(
                    value,
                    int(event[index]),
                    hit_map[index],
                    tile_plane=True,
                )

    # Parts/object pass.
    for i in range(height):
        for j in range(width):
            index = i * width + j
            value = int(parts[index])

            if value > CG_INVISIBLE:
                attr = profile.resolve(value)
                hit = attr.hit_flag
                if hit == 0:
                    _apply_footprint(
                        hit_map,
                        width=width,
                        row=i,
                        col=j,
                        footprint_x=attr.atari_x,
                        footprint_y=attr.atari_y,
                        value=HIT_BLOCKED,
                        preserve_override=True,
                    )
                elif hit == 2:
                    _apply_footprint(
                        hit_map,
                        width=width,
                        row=i,
                        col=j,
                        footprint_x=attr.atari_x,
                        footprint_y=attr.atari_y,
                        value=HIT_OVERRIDE,
                        preserve_override=False,
                    )
                elif hit == 1 and 15680 <= value <= 15732:
                    # The active source loops the footprint but only changes k=l=0.
                    hit_map[index] = HIT_BLOCKED
            elif 60 <= value <= 79:
                hit = profile.resolve(value).hit_flag
                if hit == 0 and hit_map[index] != HIT_OVERRIDE:
                    hit_map[index] = HIT_BLOCKED
                elif hit == 2:
                    hit_map[index] = HIT_OVERRIDE
            else:
                hit_map[index] = _direct_small_code(
                    value,
                    int(event[index]),
                    hit_map[index],
                    tile_plane=False,
                )

            if (int(event[index]) & EVENT_TYPE_MASK) == EVENT_NPC:
                hit_map[index] = HIT_BLOCKED

    return TaiwanV10HitMap(width, height, tuple(hit_map))


def build_taiwan_v10_hit_map_from_cache(
    cache: StoneAgeDatMapCache,
    *,
    profile: TaiwanV10CollisionProfile,
) -> TaiwanV10HitMap:
    """Compose a provenance-approved three-plane cache with Taiwan-v1 metadata."""
    if not isinstance(cache, StoneAgeDatMapCache):
        raise TypeError("cache must be StoneAgeDatMapCache")
    return build_taiwan_v10_hit_map(
        width=cache.width,
        height=cache.height,
        tile=cache.tile,
        parts=cache.parts,
        event=cache.event,
        profile=profile,
    )


def build_taiwan_v10_hit_map_from_dat(
    data: bytes | bytearray | memoryview,
    *,
    profile: TaiwanV10CollisionProfile,
) -> TaiwanV10HitMap:
    """Parse a three-plane cache and run the Taiwan-v1 hit-map algorithm.

    This function deliberately performs no provenance inference. In particular,
    parsing a mixed 2.5 DAT does not promote it into the Taiwan-v1/JSS baseline.
    """
    return build_taiwan_v10_hit_map_from_cache(
        parse_stoneage_dat_map_cache(data),
        profile=profile,
    )
