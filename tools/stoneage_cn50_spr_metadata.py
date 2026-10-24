"""CN5 SPR archive exporter: preserve logical index and physical offset order separately.

Taiwan v1 exporter assumes monotonic index offsets. Mainland 5.0 has
nonmonotonic offset entries, so parse each segment against its *actual next
physical segment*, as already validated by read-only source audit.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import struct
from tools.stoneage_tw10_resource_metadata import (
    DeterministicGzipTsv,SPRADRN_RECORD_SIZE,ANIM_HEADER_SIZE,FRAME_SIZE,
    SENTINEL_BITMAP,parse_spreadrn_record
)


def export_cn50_spr(spreadrn_path,spr_path,group_out,animation_out,frame_out):
    index=Path(spreadrn_path).read_bytes()
    if len(index)%SPRADRN_RECORD_SIZE:
        raise ValueError("non-integral-spr-index")
    rows=[parse_spreadrn_record(index[i:i+SPRADRN_RECORD_SIZE])
          for i in range(0,len(index),SPRADRN_RECORD_SIZE)]
    body=Path(spr_path).read_bytes()
    by_offset=sorted(enumerate(rows), key=lambda x:(x[1][1],x[0]))
    next_physical={}
    for a,b in zip(by_offset,by_offset[1:]):
        next_physical[a[0]]=b[1][1]
    if by_offset:
        next_physical[by_offset[-1][0]]=len(body)
    ordering_inversions=sum(rows[i][1]<rows[i-1][1] for i in range(1,len(rows)))
    total_anims=total_frames=sentinels=0
    with (DeterministicGzipTsv(group_out) as g,
          DeterministicGzipTsv(animation_out) as a,
          DeterministicGzipTsv(frame_out) as f):
        g.write("index\tspr_no\toffset\tanim_count\treserved\tend_offset\tnext_offset\tsegment_sha256\n")
        a.write("group_index\tspr_no\tanim_index\toffset\tdirection\tanim_no\tduration\tframe_count\tend_offset\n")
        f.write("group_index\tspr_no\tanim_index\tframe_index\toffset\tbmp_no\tpos_x\tpos_y\tsound_no\tsentinel\n")
        for gi,(spr_no,start,anim_count,reserved) in enumerate(rows):
            end=next_physical[gi]
            if start>=len(body) or end>len(body) or end<=start:
                raise ValueError(f"invalid-offset-sorted-spr-span:{gi}")
            cursor=start
            for ai in range(anim_count):
                if cursor+ANIM_HEADER_SIZE>end:
                    raise ValueError(f"spr-animation-past-physical-end:{gi}:{ai}")
                base=cursor
                direction,anim_no,duration,frame_count=struct.unpack_from("<HHII",body,cursor)
                cursor+=ANIM_HEADER_SIZE
                total_anims+=1
                if frame_count>(end-cursor)//FRAME_SIZE:
                    raise ValueError(f"spr-frame-range-past-physical-end:{gi}:{ai}")
                for fi in range(frame_count):
                    bmp,x,y,sound=struct.unpack_from("<IhhH",body,cursor)
                    sentinel=int(bmp==SENTINEL_BITMAP)
                    sentinels+=sentinel
                    f.write(f"{gi}\t{spr_no}\t{ai}\t{fi}\t{cursor}\t{bmp}\t{x}\t{y}\t{sound}\t{sentinel}\n")
                    cursor+=FRAME_SIZE
                    total_frames+=1
                a.write(f"{gi}\t{spr_no}\t{ai}\t{base}\t{direction}\t{anim_no}\t{duration}\t{frame_count}\t{cursor}\n")
            if cursor!=end:
                raise ValueError(f"indexed-animation-payload-physical-gap:{gi}:{cursor}:{end}")
            g.write(f"{gi}\t{spr_no}\t{start}\t{anim_count}\t{reserved}\t{cursor}\t{end}\t"
                    f"{hashlib.sha256(body[start:end]).hexdigest()}\n")
    return {"groups":len(rows),"animations":total_anims,"frames":total_frames,
            "sentinel_frames":sentinels,"exact_group_spans":len(rows),
            "spr_bytes":len(body),"nonmonotonic_index_offset_transitions":ordering_inversions,
            "physical_offset_order_distinct_from_record_order":bool(ordering_inversions)}
