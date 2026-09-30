#!/usr/bin/env python3
"""Engine-neutral StoneAge client hit-map core.

The semantics in this module are the audited descendant-stable client
readHitMap/checkHitMap family. Version-specific adapters are responsible for
supplying collision attributes and for declaring their own provenance.

This module deliberately contains no claim that any particular recovered
binary is byte-identical to a pinned public source lineage.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence


CG_INVISIBLE = 99
MAP_SEE_FLAG = 0x4000
EVENT_TYPE_MASK = 0x0FFF
EVENT_NPC = 1

HIT_PASSABLE = 0
HIT_BLOCKED = 1
HIT_OVERRIDE = 2

SEMANTIC_PROFILE = "STONEAGE_DESCENDANT_STABLE_CLIENT_HITMAP_R1"


@dataclass(frozen=True)
class ClientCollisionAttr:
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
            raise ValueError("client collision map number must be positive")
        if self.atari_x < 0 or self.atari_y < 0:
            raise ValueError("client collision footprint must be non-negative")

    @property
    def hit_flag(self) -> int:
        return self.hit_raw % 100

    @property
    def priority_type(self) -> int:
        return self.hit_raw // 100


@dataclass(frozen=True)
class ClientCollisionProfile:
    by_map_number: Mapping[int, ClientCollisionAttr]

    def __post_init__(self) -> None:
        normalized = {int(k): v for k, v in self.by_map_number.items()}
        for key, attr in normalized.items():
            if key != attr.map_number:
                raise ValueError("collision profile key/map-number mismatch")
        object.__setattr__(
            self,
            "by_map_number",
            MappingProxyType(normalized),
        )

    def resolve(self, map_number: int) -> ClientCollisionAttr:
        map_number = int(map_number)
        if map_number not in self.by_map_number:
            raise KeyError(f"unresolved client collision map number {map_number}")
        return self.by_map_number[map_number]


@dataclass(frozen=True)
class ClientHitMap:
    width: int
    height: int
    cells: tuple[int, ...]

    def __post_init__(self) -> None:
        width = int(self.width)
        height = int(self.height)
        if width < 1 or height < 1:
            raise ValueError("hit-map dimensions must be positive")
        cells = tuple(int(v) for v in self.cells)
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
    cells = width * height
    if len(tile) != cells or len(parts) != cells or len(event) != cells:
        raise ValueError("tile/parts/event planes must match width*height")
    return cells


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


def build_client_hit_map(
    *,
    width: int,
    height: int,
    tile: Sequence[int],
    parts: Sequence[int],
    event: Sequence[int],
    profile: ClientCollisionProfile,
) -> ClientHitMap:
    """Build the audited descendant-stable client hit map."""

    cells = _validate_planes(width, height, tile, parts, event)
    width, height = int(width), int(height)
    hit_map = [HIT_PASSABLE] * cells

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

    return ClientHitMap(width=width, height=height, cells=tuple(hit_map))
