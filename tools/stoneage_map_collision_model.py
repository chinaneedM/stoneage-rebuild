#!/usr/bin/env python3
"""Stable-descendant StoneAge map collision / overability reference model.

Evidence boundary:
- static cells carry tile-image and object/parts-image identifiers;
- per-image metadata supplies WALKABLE and HAVEHEIGHT;
- ordinary entry uses the object WALKABLE mode to combine tile/object metadata;
- dynamic characters/items may separately block overlap;
- diagonal walking checks both orthogonal side cells through static walkability.

This is strong multi-lineage descendant evidence, not yet a claim that every
1999/Taiwan-v1.0 coefficient/table is independently proven. Unknown image
metadata is rejected instead of defaulted.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence

from tools.stoneage_singleplayer_domain import MapPosition


CHARACTER = "character"
ITEM = "item"
GOLD = "gold"
OTHER = "other"


@dataclass(frozen=True)
class ImageCollisionMeta:
    image_id: int
    walkable: int
    have_height: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "image_id", int(self.image_id))
        object.__setattr__(self, "walkable", int(self.walkable))
        object.__setattr__(self, "have_height", bool(self.have_height))


@dataclass(frozen=True)
class MapCellImages:
    tile_image_id: int
    object_image_id: int


@dataclass(frozen=True)
class DynamicOccupant:
    kind: str
    overable: bool = True


@dataclass(frozen=True)
class CollisionDecision:
    allowed: bool
    reason: str | None = None


@dataclass(frozen=True)
class StaticCollisionMap:
    floor_id: int
    width: int
    height: int
    cells: Mapping[tuple[int, int], MapCellImages]

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        width = int(self.width)
        height = int(self.height)
        if width <= 0 or height <= 0:
            raise ValueError("collision map dimensions must be positive")
        normalized = {}
        for key, value in self.cells.items():
            x, y = int(key[0]), int(key[1])
            if not 0 <= x < width or not 0 <= y < height:
                raise ValueError(f"collision cell outside bounds: {(x, y)}")
            normalized[(x, y)] = value
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "cells", MappingProxyType(normalized))

    def cell_at(self, position: MapPosition) -> MapCellImages:
        if int(position.floor_id) != self.floor_id:
            raise ValueError("position floor does not match collision map")
        if not (0 <= int(position.x) < self.width and 0 <= int(position.y) < self.height):
            raise ValueError("position outside collision map bounds")
        key = (int(position.x), int(position.y))
        if key not in self.cells:
            raise KeyError(f"collision cell data missing at {key}")
        return self.cells[key]


@dataclass(frozen=True)
class CollisionProfile:
    images: Mapping[int, ImageCollisionMeta]

    def __post_init__(self) -> None:
        normalized = {int(key): value for key, value in self.images.items()}
        for key, meta in normalized.items():
            if key != meta.image_id:
                raise ValueError(
                    f"image metadata key {key} does not match image_id {meta.image_id}"
                )
        object.__setattr__(self, "images", MappingProxyType(normalized))

    def meta(self, image_id: int) -> ImageCollisionMeta:
        image_id = int(image_id)
        if image_id not in self.images:
            raise KeyError(f"unknown image collision metadata: {image_id}")
        return self.images[image_id]


def static_point_walkable(
    *,
    tile: ImageCollisionMeta,
    object_part: ImageCollisionMeta,
    is_flying: bool = False,
) -> CollisionDecision:
    """Model descendant MAP_walkAbleFromPoint.

    Non-flying object WALKABLE modes:
    - 0: blocked;
    - 1: defer to tile WALKABLE == 1;
    - 2: force walkable;
    - other: blocked.

    Flying ignores WALKABLE and is blocked only when tile or object has height.
    """
    if is_flying:
        if tile.have_height or object_part.have_height:
            return CollisionDecision(False, "height_blocks_flying")
        return CollisionDecision(True)

    mode = int(object_part.walkable)
    if mode == 0:
        return CollisionDecision(False, "object_walkable_mode_0")
    if mode == 1:
        if int(tile.walkable) == 1:
            return CollisionDecision(True)
        return CollisionDecision(False, "tile_walkable_not_1")
    if mode == 2:
        return CollisionDecision(True)
    return CollisionDecision(False, "unknown_object_walkable_mode")


def dynamic_overlap_allowed(
    occupants: Sequence[DynamicOccupant],
) -> CollisionDecision:
    """Model the target-cell object-overability pass in CHAR_walk."""
    for occupant in occupants:
        if occupant.kind == CHARACTER and not occupant.overable:
            return CollisionDecision(False, "non_overable_character")
        if occupant.kind == ITEM and not occupant.overable:
            return CollisionDecision(False, "non_overable_item")
        # GOLD and other object types do not set notover in the inspected path.
    return CollisionDecision(True)


def point_entry_allowed(
    collision_map: StaticCollisionMap,
    profile: CollisionProfile,
    position: MapPosition,
    *,
    occupants: Sequence[DynamicOccupant] = (),
    is_flying: bool = False,
) -> CollisionDecision:
    cell = collision_map.cell_at(position)
    static = static_point_walkable(
        tile=profile.meta(cell.tile_image_id),
        object_part=profile.meta(cell.object_image_id),
        is_flying=is_flying,
    )
    if not static.allowed:
        return static
    dynamic = dynamic_overlap_allowed(occupants)
    if not dynamic.allowed:
        return dynamic
    return CollisionDecision(True)


def ordinary_step_allowed(
    collision_map: StaticCollisionMap,
    profile: CollisionProfile,
    *,
    origin: MapPosition,
    destination: MapPosition,
    destination_occupants: Sequence[DynamicOccupant] = (),
    is_flying: bool = False,
) -> CollisionDecision:
    """Resolve one ordinary one-cell step including diagonal corner checks.

    The descendant CHAR_walk path checks target static map walkability first.
    For diagonal movement it then checks the two orthogonal side cells with
    MAP_walkAble (static map rule) before doing dynamic overlap checks on the
    target cell.
    """
    if origin.floor_id != destination.floor_id:
        return CollisionDecision(False, "floor_change_not_an_ordinary_step")

    dx = int(destination.x) - int(origin.x)
    dy = int(destination.y) - int(origin.y)
    if dx == 0 and dy == 0:
        return CollisionDecision(False, "zero_length_step")
    if abs(dx) > 1 or abs(dy) > 1:
        return CollisionDecision(False, "step_exceeds_one_cell")

    target_cell = collision_map.cell_at(destination)
    target_static = static_point_walkable(
        tile=profile.meta(target_cell.tile_image_id),
        object_part=profile.meta(target_cell.object_image_id),
        is_flying=is_flying,
    )
    if not target_static.allowed:
        return target_static

    if dx != 0 and dy != 0:
        side_x = MapPosition(origin.floor_id, origin.x + dx, origin.y)
        side_y = MapPosition(origin.floor_id, origin.x, origin.y + dy)
        for side, label in ((side_x, "diagonal_x_side"), (side_y, "diagonal_y_side")):
            cell = collision_map.cell_at(side)
            side_static = static_point_walkable(
                tile=profile.meta(cell.tile_image_id),
                object_part=profile.meta(cell.object_image_id),
                is_flying=is_flying,
            )
            if not side_static.allowed:
                return CollisionDecision(False, label)

    dynamic = dynamic_overlap_allowed(destination_occupants)
    if not dynamic.allowed:
        return dynamic
    return CollisionDecision(True)
