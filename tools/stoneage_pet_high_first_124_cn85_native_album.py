"""PET124: authenticated same-archive native table, local album and portrait resource joins.
No executable execution, account keys, saved personal names, original asset bytes or official server promotion.
"""
import argparse,collections,hashlib,json,mmap,re,struct,subprocess,tempfile,time,zipfile
from pathlib import Path
from tools import stoneage_pet_high_first_122_cn85_complete_transfer as prev
from tools import stoneage_pet_high_first_123_cn85_receipt as receipt
from tools.stoneage_pet126l_cn50_table_graphic_probe import exact_pointer_literals
from tools.stoneage_pet126m_cn50_pe_album_xrefs import parse_objdump,locate_xrefs,pe32_text_identity
from tools.stoneage_tw10_resource_metadata import parse_adrn_record
REPORT=prev.REPORT.parent/"PET-HIGH-FIRST-124-CN85-NATIVE-ALBUM-R1.json"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pinned(artifact):
    assert len(artifact.read_bytes())==124361 and sha(artifact.read_bytes())==receipt.ZIP
    with zipfile.ZipFile(artifact) as z:
        assert len(z.namelist())==1
        raw=z.read(z.namelist()[0])
    assert raw==prev.REPORT.read_bytes() and sha(raw)==receipt.SHA and prev.old.p.idx.blob(raw)==receipt.BLOB
    d=json.loads(raw);assert d["original_client_verified"] and d["pet_payload_extracted"] and d["official_closures"]==0
    return d
def extract_real(root,a):
    name="real_185.bin";target=root/"real";target.mkdir()
    p=subprocess.run(["unshield","-j","-d",str(target),"x",str(root/"data1.cab"),name],capture_output=True,timeout=180,check=False)
    matches=list(target.rglob(name));assert p.returncode==0 and len(matches)==1
    expected=[x for x in a["directory"]["all_entries"] if x["name"]=="Files\\"+name];assert len(expected)==1 and matches[0].stat().st_size==expected[0]["size"]
    return matches[0],dict(name=name,source_path=expected[0]["name"],**prev.old.hash_file(matches[0]))
def native_table(path,prior_program):
    raw=path.read_bytes();assert sha(raw)==prior_program["sha256"]
    a,b=prior_program["candidates"];start=a["file_offset"];end=b["file_offset"]+28*b["rows"]
    table=raw[start:end];assert len(table)==627*28
    assert sha(table[:544*28])==a["table_source_sha256"] and sha(table[593*28:])==b["table_source_sha256"]
    entries=[]
    for i in range(627):
        rec=table[i*28:(i+1)*28];slot,field,face=struct.unpack("<i20sI",rec)
        row=dict(ordinal=i,slot=slot,face=face,source_record_sha256=sha(rec),strict_old_parser=prev.parse_row(raw,start+i*28,"gb18030") is not None)
        name,sep,pad=field.partition(b"\0")
        try:
            label=name.decode("gb18030","strict")
            if label and len(label)<=20 and all(c.isprintable() for c in label):
                row["compiled_label"]=label
        except UnicodeDecodeError:pass
        row["nul_terminated"]=bool(sep);row["nonzero_padding_bytes"]=sum(bool(x) for x in pad)
        row["classification"]="OLD_STRICT" if row["strict_old_parser"] else "UNRESOLVED_RECORD_SHAPE"
        entries.append(row)
    # PE source literals and short disassembly contexts; not proven selector.
    imagebase,_=pe32_text_identity(raw)
    dis=subprocess.run(["objdump","-d","-M","intel",str(path)],capture_output=True,check=True,timeout=60,text=True).stdout
    ins=parse_objdump(dis)
    refs={}
    for label,off in [("table_start",start),("table_face_field",start+24),("table_second_segment",b["file_offset"])]:
        x=exact_pointer_literals(raw,off)
        refs[label]=dict(literals=x,decoded_contexts=locate_xrefs(ins,x.get("literal_va_locations",[]),imagebase))
    layout=[]
    # Only numeric operands potentially tied to the candidate 570*80+16 structure.
    for x in ins:
        if re.search(r"(?<![0-9a-f])0x(?:b230|b220|23a)(?![0-9a-f])",x["instruction"],re.I):
            layout.append(x)
    return dict(program=path.name,source_sha256=sha(raw),table_start=start,table_end=end,table_sha256=sha(table),entries=entries,table_reference_candidates=refs,layout_numeric_operand_candidates=layout[:64],layout_operand_count=len(layout),native_selector_proven=False)
def album_summary(path,rows):
    raw=path.read_bytes();stride=16+570*80;assert len(raw)==99*stride
    # Do not emit local headers, user names, free names, keys, or numeric stats.
    labels={r["slot"]:r.get("compiled_label") for r in rows if 0<=r["slot"]<570 and r.get("compiled_label")}
    flags=collections.Counter();known_matches=0;nonempty_names=0;decodable_names=0
    per_slot=collections.Counter()
    for b in range(99):
        for s in range(570):
            off=b*stride+16+s*80;rec=raw[off:off+80]
            flag=struct.unpack_from("<i",rec,76)[0];flags[str(flag) if flag in (0,1,2) else "OTHER"]+=1
            if flag not in (1,2):continue
            per_slot[s]+=1
            name=rec[:17].split(b"\0",1)[0]
            if name:nonempty_names+=1
            try:
                text=name.decode("gb18030","strict");decodable_names+=1
                known_matches+=int(bool(text) and text==labels.get(s))
            except UnicodeDecodeError:pass
    return dict(candidate_slots=570,candidate_blocks=99,candidate_record_bytes=80,candidate_header_bytes=16,flag_histogram=dict(flags),flag_1_2_positions=sum(per_slot.values()),slots_with_flag_1_2=len(per_slot),nonempty_flag_1_2_name_count=nonempty_names,decodable_flag_1_2_name_count=decodable_names,exact_compiled_slot_label_matches=known_matches,private_names_or_headers_published=False,layout_confirmed=False)
def joins(adrn,real,rows,spr):
    names=[r for r in rows if r["strict_old_parser"] and r["slot"]>=0]
    faces={r["face"] for r in names};by=collections.defaultdict(list)
    groups=collections.defaultdict(list)
    for x in spr["group_rows"]:groups[int(x["spr_no"])].append(int(x["index"]))
    raw=adrn.read_bytes();assert len(raw)%80==0
    with real.open("rb") as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
        for i in range(0,len(raw),80):
            x=parse_adrn_record(raw[i:i+80])
            if x["map_number"] not in faces:continue
            off=x["adder"];size=x["size"]
            valid=0<=off and size>=16 and off+size<=len(mm)
            block=mm[off:off+size] if valid else b""
            rd=block[:2]==b"RD" and len(block)>=16
            dims=struct.unpack_from("<iiI",block,4) if rd else None
            by[x["map_number"]].append(dict(adrn_index=i//80,bitmapno=x["bitmapno"],offset=off,size=size,width=x["width"],height=x["height"],rd_magic=rd,rd_dimensions_match=bool(dims and dims[:2]==(x["width"],x["height"])),rd_size_field=dims[2] if dims else None,rd_sha256=sha(block) if valid else None))
    links=[dict(ordinal=r["ordinal"],slot=r["slot"],face=r["face"],compiled_label=r["compiled_label"],face_map_number_candidates=by[r["face"]],ordinal_spr_group_indices=groups[100250+r["ordinal"]],slot_spr_group_indices=groups[100250+r["slot"]],native_selector_proven=False) for r in names]
    return dict(rows=links,face_map_number_rows=sum(bool(x["face_map_number_candidates"]) for x in links),unique_face_map_number_rows=sum(len(x["face_map_number_candidates"])==1 for x in links),ordinal_spr_rows=sum(bool(x["ordinal_spr_group_indices"]) for x in links),slot_spr_rows=sum(bool(x["slot_spr_group_indices"]) for x in links),native_selector_proven=False)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);args=ap.parse_args()
    d=pinned(args.artifact);cap=json.loads(prev.old.p.R117.read_bytes())["results"][0];a=json.loads(prev.old.prev.REPORT.read_bytes())["results"][0]
    out=dict(schema="stoneage.pet124.cn85.native_album.r1",prior_report_git_blob=receipt.BLOB,prior_report_sha256=receipt.SHA,prior_artifact=15120807113,original_assets_published=False,official_closures=0,original_client_reacquired=False,analysis={})
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);archive=root/"StoneAge.zip"
        try:
            out["transfer"]=prev.transfer(cap,archive)
            assert out["transfer"]["complete"] and out["transfer"]["cdx_digest_matches"] and out["transfer"]["sha256"]==d["transfer"]["sha256"]
            assert prev.old.inspect_zip(archive,root,cap,a)==d["zip_members"]
            out["original_client_reacquired"]=True
            r=prev.old.extract(root,a);paths={x.name:x for x in (root/"selected").rglob("*") if x.is_file()}
            known={x["name"]:x["sha256"] for x in d["selected_resources"]}
            assert len(r)==6 and all(x["result"]=="EXTRACTED_SIZE_VERIFIED" and x["sha256"]==known[x["name"]] for x in r)
            out["resource_receipts"]=r
            programs=[]
            for j,name in enumerate(prev.PROGRAMS,1):
                x,path=prev.select(root,a,name);assert path is not None and x["sha256"]==known[name]
                r.append(x);programs.append(native_table(path,d["analysis"]["compiled_table_candidates"][j]))
            out["analysis"]["programs"]=programs
            out["analysis"]["table_full_span_equal"]=programs[0]["table_sha256"]==programs[1]["table_sha256"]
            out["analysis"]["album"]=album_summary(paths["album_47.dat"],programs[0]["entries"])
            real,rec=extract_real(root,a);out["real_receipt"]=rec
            out["analysis"]["resource_links"]=joins(paths["adrn_185.bin"],real,programs[0]["entries"],d["analysis"]["spr"])
        except (OSError,AssertionError,ValueError,struct.error,zipfile.BadZipFile,subprocess.SubprocessError) as e:out["blocker"]=type(e).__name__+": "+str(e)[:200]
    REPORT.write_bytes(prev.old.prior.dump(out));print("PET124_REPORT_SHA256="+sha(REPORT.read_bytes()),flush=True)
    print("PET124_RESULT="+json.dumps({k:v for k,v in out.items() if k!="analysis"},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
