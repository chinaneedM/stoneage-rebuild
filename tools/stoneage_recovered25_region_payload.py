#!/usr/bin/env python3
"""Concrete recovered25 region payload source.

Stable world floors use recovered client DAT three-plane payloads.
Resolved supplemental floors use recovered server LS2MAP two-plane payloads.

The two formats are intentionally not flattened:
- client DAT supplies tile + object/parts + event planes;
- server LS2MAP supplies tile + object planes only;
- missing LS2MAP event data remains None because NPC/event semantics are a
  separate authoritative world layer, not an all-zero synthetic plane.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.stoneage_dat_probe import parse_dat
from tools.stoneage_local_runtime_core import (
    MaterializedWorldRegion,
    RuntimeBootstrapProfile,
    WorldRegionRequest,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    RECOVERED25_PROFILE,
    Recovered25WorldProfileAdapter,
)
from tools.stoneage_server_static_map import parse_ls2map
from tools.stoneage_singleplayer_world import LATER_RECOVERED


CLIENT_DAT_THREE_PLANE="CLIENT_DAT_THREE_PLANE"
SERVER_LS2MAP_TWO_PLANE="SERVER_LS2MAP_TWO_PLANE"
EVENT_PLANE_PRESENT="RECOVERED_CLIENT_DAT"
EVENT_PLANE_SEPARATE="ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE"


@dataclass(frozen=True)
class Recovered25PayloadSourcePlan:
    stable_dat_floor_ids:frozenset[int]
    supplemental_ls2map_floor_ids:frozenset[int]

    @property
    def floor_ids(self)->frozenset[int]:
        return self.stable_dat_floor_ids|self.supplemental_ls2map_floor_ids

    def __post_init__(self)->None:
        if self.stable_dat_floor_ids & self.supplemental_ls2map_floor_ids:
            raise ValueError("payload source plan contains overlapping floor classes")


def build_payload_source_plan(
    adapter:Recovered25WorldProfileAdapter,
)->Recovered25PayloadSourcePlan:
    extension=adapter.runtime.base.extension
    plan=Recovered25PayloadSourcePlan(
        stable_dat_floor_ids=frozenset(extension.stable_world.by_floor),
        supplemental_ls2map_floor_ids=frozenset(extension.resolved_by_floor),
    )
    if plan.floor_ids!=frozenset(adapter.topology.maps):
        raise ValueError("payload source plan does not cover materializable topology")
    return plan


@dataclass(frozen=True)
class EngineNeutralMapRegion:
    floor_id:int
    map_width:int
    map_height:int
    x1:int
    y1:int
    x2:int
    y2:int
    tile_ids:tuple[int,...]
    object_ids:tuple[int,...]
    event_ids:tuple[int,...]|None
    source_kind:str
    event_plane_status:str
    payload_sha256:str

    def __post_init__(self)->None:
        width=int(self.x2)-int(self.x1)+1
        height=int(self.y2)-int(self.y1)+1
        cells=width*height
        if width<=0 or height<=0:
            raise ValueError("region dimensions must be positive")
        if len(self.tile_ids)!=cells or len(self.object_ids)!=cells:
            raise ValueError("region tile/object plane length drift")
        if self.event_ids is not None and len(self.event_ids)!=cells:
            raise ValueError("region event plane length drift")
        if self.source_kind==CLIENT_DAT_THREE_PLANE:
            if self.event_ids is None or self.event_plane_status!=EVENT_PLANE_PRESENT:
                raise ValueError("client DAT region must retain event plane")
        elif self.source_kind==SERVER_LS2MAP_TWO_PLANE:
            if self.event_ids is not None or self.event_plane_status!=EVENT_PLANE_SEPARATE:
                raise ValueError("server LS2MAP region must not fabricate event plane")
        else:
            raise ValueError("unknown recovered25 region source kind")


def _slice_plane(
    values,
    *,
    map_width:int,
    x1:int,
    y1:int,
    x2:int,
    y2:int,
)->tuple[int,...]:
    out=[]
    for y in range(int(y1),int(y2)+1):
        start=y*int(map_width)+int(x1)
        end=y*int(map_width)+int(x2)+1
        out.extend(int(v) for v in values[start:end])
    return tuple(out)


def _index_files(root:Path)->Mapping[str,Path]:
    root=Path(root)
    rows={}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel=path.relative_to(root).as_posix().lower()
        name=path.name.lower()
        for key in (rel,name):
            if key in rows and rows[key]!=path:
                # A full relative path remains unambiguous even if basename is not.
                if "/" not in key:
                    rows.pop(key,None)
                    continue
                raise ValueError(f"duplicate case-folded payload path: {key}")
            rows[key]=path
    return MappingProxyType(rows)


def _resolve(index:Mapping[str,Path],relative:str)->Path:
    key=str(relative).replace("\\","/").lstrip("./").lower()
    path=index.get(key)
    if path is None:
        path=index.get(Path(key).name)
    if path is None:
        raise FileNotFoundError(f"recovered payload path not found: {relative}")
    return path


class Recovered25RegionPayloadSource:
    """Bundle-backed provider for actual recovered25 map planes."""

    def __init__(
        self,
        *,
        profile:RuntimeBootstrapProfile,
        adapter:Recovered25WorldProfileAdapter,
        client_dat_dir:Path,
        server_map_root:Path,
    )->None:
        if profile.runtime_world_profile!=RECOVERED25_PROFILE:
            raise ValueError("region payload source requires recovered25 profile")
        if profile.contract_id!=adapter.profile.contract_id:
            raise ValueError("region payload source adapter/profile drift")
        self.profile=profile
        self.adapter=adapter
        self.client_dat_dir=Path(client_dat_dir)
        self.server_map_root=Path(server_map_root)
        if not self.client_dat_dir.is_dir():
            raise ValueError("client DAT directory is missing")
        if not self.server_map_root.is_dir():
            raise ValueError("server map root is missing")
        self.plan=build_payload_source_plan(adapter)
        self._client_index=_index_files(self.client_dat_dir)
        self._server_index=_index_files(self.server_map_root)

    def _stable_payload(self,floor_id:int):
        row=self.adapter.runtime.base.extension.stable_world.by_floor[int(floor_id)]
        path=_resolve(self._client_index,row.path)
        raw=path.read_bytes()
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=row.map_sha256:
            raise ValueError(f"stable DAT SHA drift for floor {floor_id}")
        width,height,tile,obj,event=parse_dat(path)
        if (int(width),int(height))!=(row.width,row.height):
            raise ValueError(f"stable DAT dimension drift for floor {floor_id}")
        return width,height,tile,obj,event,digest,CLIENT_DAT_THREE_PLANE,EVENT_PLANE_PRESENT

    def _supplemental_payload(self,floor_id:int):
        row=self.adapter.runtime.base.extension.resolved_by_floor[int(floor_id)]
        paths=tuple(sorted(row.server_paths,key=str.lower))
        if not paths:
            raise ValueError("supplemental floor lacks server path")
        selected=_resolve(self._server_index,paths[0])
        raw=selected.read_bytes()
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=row.map_sha256:
            raise ValueError(f"supplemental LS2MAP SHA drift for floor {floor_id}")
        parsed=parse_ls2map(raw)
        if parsed.floor_id!=int(floor_id):
            raise ValueError(f"supplemental LS2MAP embedded id drift for floor {floor_id}")
        if (parsed.width,parsed.height)!=(row.width,row.height):
            raise ValueError(f"supplemental LS2MAP dimension drift for floor {floor_id}")
        return (
            parsed.width,parsed.height,parsed.tile_ids,parsed.object_ids,None,
            digest,SERVER_LS2MAP_TWO_PLANE,EVENT_PLANE_SEPARATE,
        )

    def _full_payload(self,floor_id:int):
        floor_id=int(floor_id)
        if floor_id in self.plan.stable_dat_floor_ids:
            return self._stable_payload(floor_id)
        if floor_id in self.plan.supplemental_ls2map_floor_ids:
            return self._supplemental_payload(floor_id)
        raise KeyError(f"floor {floor_id} is outside recovered25 payload plan")

    def materialize_region(
        self,
        request:WorldRegionRequest,
    )->MaterializedWorldRegion:
        if request.world_profile!=self.profile.runtime_world_profile:
            raise ValueError("region payload request world-profile mismatch")
        definition=self.adapter.map_definition(request.floor_id)
        if (
            request.x1<0 or request.y1<0
            or request.x2>=definition.width
            or request.y2>=definition.height
        ):
            raise ValueError("region payload request exceeds map bounds")

        width,height,tile,obj,event,digest,kind,event_status=(
            self._full_payload(request.floor_id)
        )
        region=EngineNeutralMapRegion(
            floor_id=int(request.floor_id),
            map_width=int(width),
            map_height=int(height),
            x1=int(request.x1),y1=int(request.y1),
            x2=int(request.x2),y2=int(request.y2),
            tile_ids=_slice_plane(
                tile,map_width=width,x1=request.x1,y1=request.y1,
                x2=request.x2,y2=request.y2,
            ),
            object_ids=_slice_plane(
                obj,map_width=width,x1=request.x1,y1=request.y1,
                x2=request.x2,y2=request.y2,
            ),
            event_ids=(
                None if event is None else _slice_plane(
                    event,map_width=width,x1=request.x1,y1=request.y1,
                    x2=request.x2,y2=request.y2,
                )
            ),
            source_kind=kind,
            event_plane_status=event_status,
            payload_sha256=digest,
        )
        provenance=definition.provenance
        if provenance is None or provenance.content_role!=LATER_RECOVERED:
            raise ValueError("region payload map lost LATER_RECOVERED provenance")
        return MaterializedWorldRegion(
            request=request,
            payload=region,
            provenance={
                "world_profile":self.profile.runtime_world_profile,
                "evidence_role":self.profile.runtime_world_evidence_role,
                "content_role":provenance.content_role,
                "resource_role":provenance.resource_role,
                "source_versions":tuple(provenance.source_versions),
                "evidence_refs":tuple(provenance.evidence_refs),
                "payload_sha256":digest,
                "payload_kind":kind,
                "event_plane_status":event_status,
            },
        )

    def validate_all_payloads(self)->Mapping[str,int]:
        counts={
            "materializable_floors":0,
            "client_dat_three_plane_floors":0,
            "server_ls2map_two_plane_floors":0,
            "event_plane_present_floors":0,
            "event_plane_separate_floors":0,
        }
        for floor_id in sorted(self.plan.floor_ids):
            definition=self.adapter.map_definition(floor_id)
            width,height,_tile,_obj,event,_digest,kind,event_status=(
                self._full_payload(floor_id)
            )
            if (width,height)!=(definition.width,definition.height):
                raise ValueError(f"payload/topology dimension drift for floor {floor_id}")
            counts["materializable_floors"]+=1
            if kind==CLIENT_DAT_THREE_PLANE:
                counts["client_dat_three_plane_floors"]+=1
                counts["event_plane_present_floors"]+=int(event is not None)
            elif kind==SERVER_LS2MAP_TWO_PLANE:
                counts["server_ls2map_two_plane_floors"]+=1
                counts["event_plane_separate_floors"]+=int(
                    event is None and event_status==EVENT_PLANE_SEPARATE
                )
        return MappingProxyType(counts)
