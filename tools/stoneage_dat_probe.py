#!/usr/bin/env python3
import argparse,array,collections,struct,sys
from pathlib import Path

CG_INVISIBLE=99
MAP_READ_FLAG=0x8000
MAP_SEE_FLAG=0x4000
EVENT_MASK=0x0fff
EVENT_NAMES={0:"NONE",1:"NPC",2:"ENEMY",3:"WARP",4:"DOOR",5:"ALTERRATIVE",6:"WARP_MORNING",7:"WARP_NOON",8:"WARP_NIGHT"}
ADRN_RECORD_SIZE=80

def _u16(data):
    a=array.array("H"); a.frombytes(data)
    if sys.byteorder!="little": a.byteswap()
    return a

def parse_dat(path):
    data=path.read_bytes()
    if len(data)<8: raise ValueError("short_header")
    w,h=struct.unpack_from("<II",data,0)
    if not (0<w<=10000 and 0<h<=10000): raise ValueError(f"bad_dimensions:{w}x{h}")
    n=w*h; expected=8+n*6
    if len(data)!=expected: raise ValueError(f"bad_size:{len(data)}:{expected}")
    v=_u16(data[8:])
    return w,h,v[:n],v[n:2*n],v[2*n:3*n]

def load_adrn(path):
    data=path.read_bytes()
    if len(data)%80: raise ValueError("adrn_remainder")
    by_bmp={}; duplicate=0
    for i in range(0,len(data),80):
        r=data[i:i+80]
        bitmapno=struct.unpack_from("<I",r,0)[0]
        bmpnumber=struct.unpack_from("<I",r,76)[0]
        attr={"bitmapno":bitmapno,"atari_x":r[28],"atari_y":r[29],
              "hit":struct.unpack_from("<H",r,30)[0],
              "height":struct.unpack_from("<h",r,32)[0]}
        if bmpnumber in by_bmp and bmpnumber: duplicate+=1
        by_bmp[bmpnumber]=attr
    return {"bytes":len(data),"records":len(data)//80,"by_bmp":by_bmp,"duplicate":duplicate}

def consecutive_runs(counter):
    vals=sorted(counter)
    if not vals:return []
    out=[]; start=prev=vals[0]; refs=counter[start]
    for v in vals[1:]:
        if v==prev+1:
            prev=v; refs+=counter[v]
        else:
            out.append((start,prev,prev-start+1,refs))
            start=prev=v; refs=counter[v]
    out.append((start,prev,prev-start+1,refs))
    return out

def unresolved_profile(counter, adrn_keys):
    keys=sorted(k for k in adrn_keys if k>CG_INVISIBLE)
    lo=keys[0] if keys else None; hi=keys[-1] if keys else None
    classes=collections.Counter()
    for v,n in counter.items():
        if lo is None:
            classes["no_adrn_domain_refs"]+=n
        elif v<lo:
            classes["below_adrn_domain_refs"]+=n
        elif v>hi:
            classes["above_adrn_domain_refs"]+=n
        else:
            classes["within_adrn_gap_refs"]+=n
        if 100<=v<=19999:
            classes["legacy_map_range_refs"]+=n
        elif v>19999:
            classes["above_legacy_map_range_refs"]+=n
        else:
            classes["below_legacy_map_range_refs"]+=n
    classes["unresolved_refs"]=sum(counter.values())
    classes["unresolved_unique"]=len(counter)
    classes["adrn_domain_min"]=lo if lo is not None else -1
    classes["adrn_domain_max"]=hi if hi is not None else -1
    runs=consecutive_runs(counter)
    return {
        "classes":classes,
        "runs_by_length":sorted(runs,key=lambda x:(-x[2],-x[3],x[0])),
        "runs_by_refs":sorted(runs,key=lambda x:(-x[3],-x[2],x[0])),
        "top_ids":counter.most_common(40),
    }

def bucket(v):
    if v==0:return "zero"
    if v<=19:return "control_1_19"
    if v<=39:return "environment_20_39"
    if v<=59:return "bgm_40_59"
    if v<=79:return "legacy_special_60_79"
    if v<=99:return "reserved_80_99"
    return "graphic_gt_99"

def analyze(dat_dir,adrn_path=None):
    tile=collections.Counter(); parts=collections.Counter(); events=collections.Counter()
    dims=collections.Counter(); invalid=[]; valid=[]; cells=0
    files=sorted((p for p in dat_dir.iterdir() if p.is_file() and p.suffix.lower()==".dat"),key=lambda p:p.name.lower())
    event_file_stats=[]; event_anomalies=[]
    for p in files:
        try:w,h,t,pa,e=parse_dat(p)
        except ValueError as exc:
            invalid.append((p.name,p.stat().st_size,str(exc))); continue
        valid.append((p.name,w,h)); dims[(w,h)]+=1; cells+=w*h
        tile.update(t); parts.update(pa); events.update(e)
        unknown_values=[v for v in e if (v&EVENT_MASK) not in EVENT_NAMES]
        unknown=len(unknown_values)
        unknown_read=sum(1 for v in unknown_values if v&MAP_READ_FLAG)
        event_file_stats.append((p.name,w,h,unknown,unknown_read))
        reserved_high=sum(1 for v in e if v&0x3000)
        if unknown or reserved_high:
            raw=collections.Counter(unknown_values)
            low=collections.Counter(v&EVENT_MASK for v in unknown_values)
            event_anomalies.append({
                "name":p.name,"w":w,"h":h,"cells":w*h,"unknown":unknown,
                "reserved_high":reserved_high,"unique_raw":len(raw),"unique_low":len(low),
                "known":len(e)-unknown,
                "raw_top":raw.most_common(20),"low_top":low.most_common(20),
                "low_counts":low,
                "event_eq_tile":sum(1 for a,b in zip(e,t) if a==b),
                "event_eq_parts":sum(1 for a,b in zip(e,pa) if a==b),
                "low_eq_tile_low":sum(1 for a,b in zip(e,t) if (a&EVENT_MASK)==(b&EVENT_MASK)),
                "low_eq_parts_low":sum(1 for a,b in zip(e,pa) if (a&EVENT_MASK)==(b&EVENT_MASK)),
            })
    def buckets(c):
        o=collections.Counter()
        for v,n in c.items():o[bucket(v)]+=n
        return o
    low=collections.Counter(); high=collections.Counter()
    read=see=both=unknown_total=unknown_read_total=unknown_see_total=0
    for v,n in events.items():
        low[v&EVENT_MASK]+=n; high[v&0xf000]+=n
        if v&MAP_READ_FLAG:read+=n
        if v&MAP_SEE_FLAG:see+=n
        if v&(MAP_READ_FLAG|MAP_SEE_FLAG)==(MAP_READ_FLAG|MAP_SEE_FLAG):both+=n
        if (v&EVENT_MASK) not in EVENT_NAMES:
            unknown_total+=n
            if v&MAP_READ_FLAG: unknown_read_total+=n
            if v&MAP_SEE_FLAG: unknown_see_total+=n
    out={"files":len(files),"valid":valid,"invalid":invalid,"dims":dims,"cells":cells,
         "tile":tile,"parts":parts,"events":events,"tile_buckets":buckets(tile),
         "parts_buckets":buckets(parts),"event_low":low,"event_high":high,
         "read":read,"see":see,"both":both,
         "event_unknown_total":unknown_total,"event_unknown_read":unknown_read_total,
         "event_unknown_see":unknown_see_total,
         "event_file_stats":sorted(event_file_stats,key=lambda x:(-x[3],x[0])),
         "event_anomalies":sorted(event_anomalies,key=lambda x:(-x["unknown"],-x["reserved_high"],x["name"]))}
    if adrn_path:
        adrn=load_adrn(adrn_path); out["adrn"]=adrn
        for anomaly in out["event_anomalies"]:
            mapped_cells=sum(n for v,n in anomaly["low_counts"].items() if v>CG_INVISIBLE and v in adrn["by_bmp"])
            mapped_unique=sum(1 for v in anomaly["low_counts"] if v>CG_INVISIBLE and v in adrn["by_bmp"])
            anomaly["unknown_low12_adrn_mapped_cells"]=mapped_cells
            anomaly["unknown_low12_adrn_mapped_unique"]=mapped_unique
        unresolved_files=[]
        for p in files:
            try:w,h,t,pa,e=parse_dat(p)
            except ValueError:continue
            tu=collections.Counter(v for v in t if v>CG_INVISIBLE and v not in adrn["by_bmp"])
            pu=collections.Counter(v for v in pa if v>CG_INVISIBLE and v not in adrn["by_bmp"])
            if tu or pu:
                unresolved_files.append({
                    "name":p.name,"w":w,"h":h,
                    "tile_refs":sum(tu.values()),"tile_unique":len(tu),
                    "parts_refs":sum(pu.values()),"parts_unique":len(pu),
                    "tile_top":tu.most_common(5),"parts_top":pu.most_common(5),
                })
        out["graphic_unresolved_files"]=sorted(
            unresolved_files,
            key=lambda x:(-(x["tile_refs"]+x["parts_refs"]),-x["tile_refs"],x["name"].lower())
        )
        for name,c in (("tile_graphics",tile),("parts_graphics",parts)):
            refs=mapped=0; unresolved=collections.Counter(); hit=collections.Counter()
            footprint=collections.Counter(); prio=collections.Counter()
            for v,n in c.items():
                if v<=CG_INVISIBLE:continue
                refs+=n; a=adrn["by_bmp"].get(v)
                if a is None: unresolved[v]+=n; continue
                mapped+=n; hit[a["hit"]%100]+=n; prio[a["hit"]//100]+=n
                footprint[(a["atari_x"],a["atari_y"])]+=n
            out[name]={"refs":refs,"mapped":mapped,"unresolved":unresolved,
                       "hit":hit,"prio":prio,"footprint":footprint,
                       "unresolved_profile":unresolved_profile(unresolved,adrn["by_bmp"])}
    return out

def emit(r):
    print("StoneAge recovered client DAT probe — R1")
    print("No proprietary DAT payload bytes are stored in this report.")
    print(f"CG_INVISIBLE|{CG_INVISIBLE}")
    print(f"MAP_READ_FLAG|0x{MAP_READ_FLAG:04x}")
    print(f"MAP_SEE_FLAG|0x{MAP_SEE_FLAG:04x}")
    print(f"EVENT_MASK|0x{EVENT_MASK:04x}")
    print(f"DAT_FILE_COUNT|{r['files']}")
    print(f"DAT_VALID_COUNT|{len(r['valid'])}")
    print(f"DAT_INVALID_COUNT|{len(r['invalid'])}")
    print(f"DAT_TOTAL_CELLS|{r['cells']}")
    for (w,h),n in r["dims"].most_common(30):print(f"DAT_DIMENSION|{w}|{h}|{n}")
    for name,size,why in r["invalid"][:40]:print(f"DAT_INVALID|{name}|{size}|{why}")
    order=["zero","control_1_19","environment_20_39","bgm_40_59","legacy_special_60_79","reserved_80_99","graphic_gt_99"]
    for layer in ("tile","parts"):
        for b in order:print(f"{layer.upper()}_BUCKET|{b}|{r[layer+'_buckets'].get(b,0)}")
        for v,n in r[layer].most_common(30):print(f"{layer.upper()}_TOP_VALUE|{v}|{n}")
    print(f"EVENT_READ_FLAG_CELLS|{r['read']}")
    print(f"EVENT_SEE_FLAG_CELLS|{r['see']}")
    print(f"EVENT_BOTH_FLAGS_CELLS|{r['both']}")
    print(f"EVENT_UNKNOWN_LOW12_CELLS|{r['event_unknown_total']}")
    print(f"EVENT_UNKNOWN_WITH_READ_FLAG|{r['event_unknown_read']}")
    print(f"EVENT_UNKNOWN_WITH_SEE_FLAG|{r['event_unknown_see']}")
    for name,w,h,unknown,unknown_read in r["event_file_stats"][:40]:
        if unknown:
            print(f"EVENT_UNKNOWN_FILE|{name}|{w}|{h}|{unknown}|{unknown_read}")
    for a in r["event_anomalies"][:20]:
        print(f"EVENT_ANOMALY_FILE|{a['name']}|{a['w']}|{a['h']}|{a['cells']}|known={a['known']}|unknown={a['unknown']}|reserved_high={a['reserved_high']}|unique_raw={a['unique_raw']}|unique_low12={a['unique_low']}")
        print(f"EVENT_ANOMALY_LAYER_EQUALITY|{a['name']}|raw_eq_tile={a['event_eq_tile']}|raw_eq_parts={a['event_eq_parts']}|low12_eq_tile_low12={a['low_eq_tile_low']}|low12_eq_parts_low12={a['low_eq_parts_low']}")
        if "unknown_low12_adrn_mapped_cells" in a:
            print(f"EVENT_ANOMALY_ADRN_OVERLAP|{a['name']}|mapped_cells={a['unknown_low12_adrn_mapped_cells']}|mapped_unique={a['unknown_low12_adrn_mapped_unique']}")
        for v,n in a["raw_top"]:print(f"EVENT_ANOMALY_RAW_TOP|{a['name']}|0x{v:04x}|{n}")
        for v,n in a["low_top"]:print(f"EVENT_ANOMALY_LOW12_TOP|{a['name']}|{v}|{n}")
    for v,n in sorted(r["event_high"].items()):print(f"EVENT_HIGH_NIBBLE|0x{v:04x}|{n}")
    for v,n in r["event_low"].most_common():
        print(f"EVENT_LOW12|{v}|{EVENT_NAMES.get(v,'UNKNOWN')}|{n}")
    if "adrn" in r:
        a=r["adrn"]
        print(f"ADRN_BYTES|{a['bytes']}")
        print(f"ADRN_RECORD_COUNT|{a['records']}")
        print(f"ADRN_BMPNUMBER_INDEX_SIZE|{len(a['by_bmp'])}")
        print(f"ADRN_DUPLICATE_BMPNUMBERS|{a['duplicate']}")
        print(f"GRAPHIC_UNRESOLVED_FILE_COUNT|{len(r.get('graphic_unresolved_files',[]))}")
        for x in r.get("graphic_unresolved_files",[])[:40]:
            print(f"GRAPHIC_UNRESOLVED_FILE|{x['name']}|{x['w']}|{x['h']}|tile_refs={x['tile_refs']}|tile_unique={x['tile_unique']}|parts_refs={x['parts_refs']}|parts_unique={x['parts_unique']}")
            if x["tile_top"]:print(f"GRAPHIC_UNRESOLVED_FILE_TILE_TOP|{x['name']}|"+",".join(f"{v}:{n}" for v,n in x["tile_top"]))
            if x["parts_top"]:print(f"GRAPHIC_UNRESOLVED_FILE_PARTS_TOP|{x['name']}|"+",".join(f"{v}:{n}" for v,n in x["parts_top"]))
        for layer in ("tile_graphics","parts_graphics"):
            g=r[layer]; p=layer.upper()
            print(f"{p}_REFS|{g['refs']}")
            print(f"{p}_MAPPED_REFS|{g['mapped']}")
            print(f"{p}_UNRESOLVED_REFS|{sum(g['unresolved'].values())}")
            print(f"{p}_UNRESOLVED_UNIQUE|{len(g['unresolved'])}")
            if g["unresolved"]:print(f"{p}_UNRESOLVED_SAMPLE|"+",".join(map(str,sorted(g["unresolved"])[:40])))
            up=g["unresolved_profile"]; cl=up["classes"]
            print(f"{p}_ADRN_DOMAIN|{cl['adrn_domain_min']}|{cl['adrn_domain_max']}")
            for key in ("within_adrn_gap_refs","below_adrn_domain_refs","above_adrn_domain_refs","legacy_map_range_refs","above_legacy_map_range_refs","below_legacy_map_range_refs"):
                print(f"{p}_UNRESOLVED_CLASS|{key}|{cl.get(key,0)}")
            for v,n in up["top_ids"][:20]:print(f"{p}_UNRESOLVED_TOP_ID|{v}|{n}")
            for s,e,count,refs in up["runs_by_length"][:20]:print(f"{p}_UNRESOLVED_RUN_BY_LENGTH|{s}|{e}|{count}|{refs}")
            for s,e,count,refs in up["runs_by_refs"][:20]:print(f"{p}_UNRESOLVED_RUN_BY_REFS|{s}|{e}|{count}|{refs}")
            for v,n in sorted(g["hit"].items()):print(f"{p}_HIT_MOD100|{v}|{n}")
            for v,n in sorted(g["prio"].items()):print(f"{p}_PRIO_TYPE|{v}|{n}")
            for (x,y),n in g["footprint"].most_common(20):print(f"{p}_FOOTPRINT|{x}|{y}|{n}")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--dat-dir",type=Path,required=True); ap.add_argument("--adrn",type=Path)
    a=ap.parse_args(); emit(analyze(a.dat_dir,a.adrn))
if __name__=="__main__":main()
