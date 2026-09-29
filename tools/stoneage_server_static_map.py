#!/usr/bin/env python3
"""Recovered server-map -> engine-neutral static collision bridge.

LS2MAP parsing is direct recovered-format evidence. mapset parsing mirrors the
pinned descendant loader's relevant column semantics:
- token 1: image id;
- token 4: WALKABLE, default 1 when absent;
- token 5: HAVEHEIGHT, default 0 when absent;
- duplicate image ids are last-definition-wins, matching MAP_imgfilt overwrite.

The bridge never fabricates missing image metadata. Concrete recovered-2.5 map
content remains LATER_RECOVERED.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_map_collision_model import (
    CollisionProfile,
    ImageCollisionMeta,
    MapCellImages,
    StaticCollisionMap,
    static_point_walkable,
)


LS2MAP_MAGIC = b"LS2MAP"
LS2MAP_HEADER_SIZE = 44
MAPSET_MAX_IMAGE_ID = 65534


@dataclass(frozen=True)
class RecoveredServerStaticMap:
    floor_id: int
    width: int
    height: int
    tile_ids: tuple[int, ...]
    object_ids: tuple[int, ...]
    payload_sha256: str

    def __post_init__(self) -> None:
        floor_id = int(self.floor_id)
        width = int(self.width)
        height = int(self.height)
        tile_ids = tuple(int(v) for v in self.tile_ids)
        object_ids = tuple(int(v) for v in self.object_ids)
        if floor_id < 0:
            raise ValueError("floor id cannot be negative")
        if width <= 0 or height <= 0:
            raise ValueError("server map dimensions must be positive")
        cells = width * height
        if len(tile_ids) != cells or len(object_ids) != cells:
            raise ValueError("server map plane size drift")
        digest = str(self.payload_sha256).lower()
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError("server map payload SHA-256 is invalid")
        object.__setattr__(self, "floor_id", floor_id)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "tile_ids", tile_ids)
        object.__setattr__(self, "object_ids", object_ids)
        object.__setattr__(self, "payload_sha256", digest)

    @property
    def used_image_ids(self) -> frozenset[int]:
        return frozenset(self.tile_ids) | frozenset(self.object_ids)

    def collision_map(self) -> StaticCollisionMap:
        cells = {}
        for index, (tile, obj) in enumerate(zip(self.tile_ids, self.object_ids)):
            x = index % self.width
            y = index // self.width
            cells[(x, y)] = MapCellImages(
                tile_image_id=tile,
                object_image_id=obj,
            )
        return StaticCollisionMap(
            floor_id=self.floor_id,
            width=self.width,
            height=self.height,
            cells=cells,
        )


@dataclass(frozen=True)
class RecoveredMapsetProfile:
    images: Mapping[int, ImageCollisionMeta]
    duplicate_image_ids: tuple[int, ...]
    row_count: int
    payload_sha256: str

    def __post_init__(self) -> None:
        images = dict(self.images)
        duplicates = tuple(sorted(set(int(v) for v in self.duplicate_image_ids)))
        row_count = int(self.row_count)
        digest = str(self.payload_sha256).lower()
        if row_count < len(images):
            raise ValueError("mapset row count smaller than unique image count")
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError("mapset payload SHA-256 is invalid")
        object.__setattr__(self, "images", MappingProxyType(images))
        object.__setattr__(self, "duplicate_image_ids", duplicates)
        object.__setattr__(self, "row_count", row_count)
        object.__setattr__(self, "payload_sha256", digest)

    def collision_profile_for(self, server_map: RecoveredServerStaticMap) -> CollisionProfile:
        missing = sorted(server_map.used_image_ids - set(self.images))
        if missing:
            raise ValueError(
                f"server map references image ids absent from mapset: {missing}"
            )
        return CollisionProfile(
            images={
                image_id: self.images[image_id]
                for image_id in sorted(server_map.used_image_ids)
            }
        )


def parse_ls2map(data: bytes) -> RecoveredServerStaticMap:
    raw = bytes(data)
    if len(raw) < LS2MAP_HEADER_SIZE or raw[:6] != LS2MAP_MAGIC:
        raise ValueError("not_ls2map")
    floor_id = struct.unpack_from(">H", raw, 6)[0]
    width = struct.unpack_from(">H", raw, 40)[0]
    height = struct.unpack_from(">H", raw, 42)[0]
    cells = width * height
    expected = LS2MAP_HEADER_SIZE + cells * 4
    if len(raw) != expected:
        raise ValueError(
            f"server_map_bad_size:{len(raw)}:{expected}:{width}:{height}"
        )
    tile_offset = LS2MAP_HEADER_SIZE
    object_offset = tile_offset + cells * 2
    tile_ids = struct.unpack_from(f">{cells}H", raw, tile_offset)
    object_ids = struct.unpack_from(f">{cells}H", raw, object_offset)
    return RecoveredServerStaticMap(
        floor_id=floor_id,
        width=width,
        height=height,
        tile_ids=tile_ids,
        object_ids=object_ids,
        payload_sha256=hashlib.sha256(raw).hexdigest(),
    )


def parse_mapset_collision_profile(data: bytes) -> RecoveredMapsetProfile:
    raw = bytes(data)
    images: dict[int, ImageCollisionMeta] = {}
    duplicates: list[int] = []
    row_count = 0

    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(b"#"):
            continue
        tokens = line.split()
        if not tokens:
            continue
        try:
            image_id = int(tokens[0], 10)
        except ValueError:
            continue
        if not 0 <= image_id <= MAPSET_MAX_IMAGE_ID:
            raise ValueError(f"mapset image id outside descendant range: {image_id}")

        walkable = 1
        have_height = 0
        if len(tokens) >= 4:
            walkable = int(tokens[3], 10)
        if len(tokens) >= 5:
            have_height = int(tokens[4], 10)

        if image_id in images:
            duplicates.append(image_id)
        images[image_id] = ImageCollisionMeta(
            image_id=image_id,
            walkable=walkable,
            have_height=bool(have_height),
        )
        row_count += 1

    if not images:
        raise ValueError("mapset contains no parseable image rows")
    return RecoveredMapsetProfile(
        images=images,
        duplicate_image_ids=tuple(duplicates),
        row_count=row_count,
        payload_sha256=hashlib.sha256(raw).hexdigest(),
    )


@dataclass(frozen=True)
class ServerStaticCollisionSummary:
    floor_id: int
    width: int
    height: int
    cells: int
    unique_tile_ids: int
    unique_object_ids: int
    used_image_ids: int
    missing_image_ids: tuple[int, ...]
    duplicate_mapset_ids_used: tuple[int, ...]
    ordinary_walkable_cells: int | None
    flying_walkable_cells: int | None
    server_map_sha256: str
    mapset_sha256: str


def summarize_static_collision(
    server_map: RecoveredServerStaticMap,
    mapset: RecoveredMapsetProfile,
) -> ServerStaticCollisionSummary:
    used = server_map.used_image_ids
    missing = tuple(sorted(used - set(mapset.images)))
    duplicates_used = tuple(sorted(used & set(mapset.duplicate_image_ids)))

    ordinary: int | None = None
    flying: int | None = None
    if not missing:
        ordinary = 0
        flying = 0
        for tile_id, object_id in zip(server_map.tile_ids, server_map.object_ids):
            tile = mapset.images[tile_id]
            obj = mapset.images[object_id]
            if static_point_walkable(tile=tile, object_part=obj).allowed:
                ordinary += 1
            if static_point_walkable(
                tile=tile,
                object_part=obj,
                is_flying=True,
            ).allowed:
                flying += 1

    return ServerStaticCollisionSummary(
        floor_id=server_map.floor_id,
        width=server_map.width,
        height=server_map.height,
        cells=server_map.width * server_map.height,
        unique_tile_ids=len(set(server_map.tile_ids)),
        unique_object_ids=len(set(server_map.object_ids)),
        used_image_ids=len(used),
        missing_image_ids=missing,
        duplicate_mapset_ids_used=duplicates_used,
        ordinary_walkable_cells=ordinary,
        flying_walkable_cells=flying,
        server_map_sha256=server_map.payload_sha256,
        mapset_sha256=mapset.payload_sha256,
    )
