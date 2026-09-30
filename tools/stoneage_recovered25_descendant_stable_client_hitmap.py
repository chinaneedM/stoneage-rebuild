#!/usr/bin/env python3
"""Recovered25 descendant-stable client hit-map reconstruction profile.

Evidence boundary:
- DAT planes and ADRN records come from the same recovered25 preservation bundle.
- The readHitMap/checkHitMap semantics are supported by three pinned descendant
  client source lineages, including two with explicit _SA_VERSION_25 markers.
- This module therefore implements an explicit reconstruction profile, not a
  claim of machine-code identity with the recovered sa_2903 executable.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_dat_probe import load_adrn


PROFILE_ID = "RECOVERED25_DESCENDANT_STABLE_CLIENT_HITMAP_R1"
EXACT_RECOVERED25_BINARY_PROOF = False
EXPECTED_ADRN_SHA256 = "92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74"
EXPECTED_ADRN_BYTES = 18_765_120
EXPECTED_ADRN_RECORDS = 234_564

CG_INVISIBLE = 99
MAP_SEE_FLAG = 0x4000
EVENT_TYPE_MASK = 0x0FFF
EVENT_NPC = 1

HIT_PASSABLE = 0
HIT_BLOCKED = 1
HIT_OVERRIDE = 2


@dataclass(frozen=True)
class DescendantStableCollisionAttr:
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
        if self.map_number <= 0:
            raise ValueError("map_number must be positive")
        if self.atari_x < 0 or self.atari_y < 0:
            raise ValueError("collision footprint dimensions must be non-negative")

    @property
    def hit_flag(self) -> int:
        return self.hit_raw % 100

    @property
    def priority_type(self) -> int:
        return self.hit_raw // 100


@dataclass(frozen=True)
class DescendantStableCollisionProfile:
    by_map_number: Mapping[int, DescendantStableCollisionAttr]
    source_sha256: str
    source_records: int
    duplicate_map_numbers: int
    profile_id: str = PROFILE_ID
    exact_recovered25_binary_proof: bool = EXACT_RECOVERED25_BINARY_PROOF

    def __post_init__(self) -> None:
        rows = {int(k): v for k, v in self.by_map_number.items()}
        for key, attr in rows.items():
            if key != attr.map_number:
                raise ValueError("collision profile key/map-number drift")
        if not rows:
            raise ValueError("collision profile contains no map-number rows")
        object.__setattr__(self, "by_map_number", MappingProxyType(rows))
        object.__setattr__(self, "source_sha256", str(self.source_sha256).lower())
        object.__setattr__(self, "source_records", int(self.source_records))
        object.__setattr__(self, "duplicate_map_numbers", int(self.duplicate_map_numbers))

    def resolve(self, map_number: int) -> DescendantStableCollisionAttr:
        map_number = int(map_number)
        if map_number not in self.by_map_number:
            raise KeyError(
                f"unresolved recovered25 ADRN map image number {map_number}"
            )
        return self.by_map_number[map_number]


@dataclass(frozen=True)
class DescendantStableClientHitMap:
    width: int
    height: int
    cells: tuple[int, ...]
    profile_id: str = PROFILE_ID
    exact_recovered25_binary_proof: bool = EXACT_RECOVERED25_BINARY_PROOF

    def __post_init__(self) -> None:
        width, height = int(self.width), int(self.height)
        cells = tuple(int(v) for v in self.cells)
        if width < 1 or height < 1:
            raise ValueError("hit-map dimensions must be positive")
        if len(cells) != width * height:
            raise ValueError("hit-map cell count does not match dimensions")
        if any(v not in (HIT_PASSABLE, HIT_BLOCKED, HIT_OVERRIDE) for v in cells):
            raise ValueError("hit-map values must be 0, 1 or 2")
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "cells", cells)

    def value_at(self, x: int, y: int) -> int:
        x, y = int(x), int(y)
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("hit-map coordinate outside bounds")
        return self.cells[y * self.width + x]

    def blocked_at(self, x: int, y: int) -> bool:
        return self.value_at(x, y) == HIT_BLOCKED


def load_recovered25_adrn_collision_profile(
    path: str | Path,
) -> DescendantStableCollisionProfile:
    path = Path(path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_ADRN_SHA256:
        raise ValueError("recovered25 adrn_15.bin SHA-256 drift")
    if len(raw) != EXPECTED_ADRN_BYTES:
        raise ValueError("recovered25 adrn_15.bin byte-size drift")

    decoded = load_adrn(path)
    if int(decoded["records"]) != EXPECTED_ADRN_RECORDS:
        raise ValueError("recovered25 ADRN record-count drift")

    rows = {}
    for map_number, attr in decoded["by_bmp"].items():
        map_number = int(map_number)
        if map_number <= 0:
            continue
        rows[map_number] = DescendantStableCollisionAttr(
            map_number=map_number,
            bitmapno=int(attr["bitmapno"]),
            atari_x=int(attr["atari_x"]),
            atari_y=int(attr["atari_y"]),
            hit_raw=int(attr["hit"]),
            height_flag=int(attr["height"]),
        )

    return DescendantStableCollisionProfile(
        by_map_number=rows,
        source_sha256=digest,
        source_records=int(decoded["records"]),
        duplicate_map_numbers=int(decoded["duplicate"]),
    )


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


def build_descendant_stable_client_hit_map(
    *,
    width: int,
    height: int,
    tile: Sequence[int],
    parts: Sequence[int],
    event: Sequence[int],
    profile: DescendantStableCollisionProfile,
) -> DescendantStableClientHitMap:
    width, height = int(width), int(height)
    size = width * height
    if width < 1 or height < 1:
        raise ValueError("map dimensions must be positive")
    if len(tile) != size or len(parts) != size or len(event) != size:
        raise ValueError("tile/parts/event planes must match width*height")

    hit_map = [HIT_PASSABLE] * size

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

    for i in range(height):
        for j in range(width):
            index = i * width + j
            value = int(parts[index])
            if value > CG_INVISIBLE:
                attr = profile.resolve(value)
                if attr.hit_flag == 0:
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
                elif attr.hit_flag == 2:
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
                elif attr.hit_flag == 1 and 15680 <= value <= 15732:
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

    return DescendantStableClientHitMap(
        width=width,
        height=height,
        cells=tuple(hit_map),
    )
