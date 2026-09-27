#!/usr/bin/env python3
"""Sparse ASCII/OCR residual on the four images of the Yegame-matched Mainland carrier.

This is intentionally narrow: one public carrier, four already-known images,
English/numeric OCR only, one pass per image. It seeks provenance tokens such
as P-RPG, ISBN, StoneAge/JSS/Waei, version strings and barcode-like numerals.
Images are transient and never committed. Chinese OCR is not attempted.
"""
from __future__ import annotations
import hashlib,json,os,re,subprocess,tempfile,urllib.parse

from tools.stoneage_ruten_early_carrier_probe import DETAIL, detail_rows, image_urls, fetch, clean

TARGET="22636573895893"
ROLE="mainland-retail-box"
TOKEN_PATTERNS=(
    re.compile(r"(?i)\bP[-_. ]?RPG[-_. ]?[A-Z0-9]{3,12}\b"),
    re.compile(r"(?i)\b(?:STONE\s*AGE|STONEAGE|JSS|WAEI|WAYI)\b"),
    re.compile(r"(?i)\bV(?:ER(?:SION)?)?\s*[0-9]+(?:\.[0-9]+){1,2}\b"),
    re.compile(r"(?i)\bISBN\s*[-:]?\s*[0-9Xx-]{8,24}\b"),
    re.compile(r"(?<!\d)\d{12,14}(?!\d)"),
)

def normalize_line(s):
    s=" ".join(s.split())
    return s[:1000]

def main():
    print("StoneAge matched Mainland carrier sparse ASCII-OCR residual — R1")
    print(f"TARGET|ruten_id={TARGET}|role={ROLE}|visual_anchor=EN0ZGKJ0002")
    print("SCOPE|4 known public images|max-one-English-OCR-pass-each|transient images|no Chinese OCR|no image commit")
    errors=[];tokens=set();ocr_images=0
    try:
        q=urllib.parse.urlencode({"gno":TARGET,"level":"simple"})
        st,final,h,b=fetch(DETAIL+"?"+q,accept="application/json,*/*")
        rows=detail_rows(json.loads(b.decode("utf-8","replace")))
        urls=[]
        for row in rows:urls.extend(image_urls(row))
        print(f"DETAIL|status={st}|rows={len(rows)}|images={len(urls)}|sha256={hashlib.sha256(b).hexdigest()}")
    except Exception as e:
        print(f"ERROR|scope=detail|kind={type(e).__name__}|message={clean(e)}")
        print("RESOLUTION|OCR_INPUT_UNAVAILABLE")
        return

    for idx,url in enumerate(urls[:4]):
        try:
            st,final,h,ib=fetch(url,accept="image/*,*/*",limit=12*1024*1024)
            suffix=".jpg"
            with tempfile.NamedTemporaryFile(suffix=suffix,delete=False) as tf:
                tf.write(ib);path=tf.name
            try:
                cp=subprocess.run(
                    ["tesseract",path,"stdout","-l","eng","--psm","11"],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=40,check=False
                )
                ocr_images+=1
                raw=cp.stdout or ""
                ascii_lines=[]
                for line in raw.splitlines():
                    line=normalize_line(line)
                    if not line:continue
                    if re.search(r"[A-Za-z0-9]",line):
                        ascii_lines.append(line)
                    for pat in TOKEN_PATTERNS:
                        for m in pat.finditer(line):
                            tokens.add(m.group(0))
                print(f"IMAGE|index={idx}|status={st}|bytes={len(ib)}|sha256={hashlib.sha256(ib).hexdigest()}|ocr_rc={cp.returncode}|ascii_lines={len(ascii_lines)}")
                for line in ascii_lines[:80]:
                    print(f"OCR_LINE|index={idx}|text={clean(line,1000)}")
            finally:
                try:os.unlink(path)
                except OSError:pass
        except Exception as e:
            errors.append((idx,type(e).__name__,str(e)))

    for token in sorted(tokens):
        print(f"IDENTITY_CANDIDATE|value={clean(token)}")
    for idx,k,m in errors:
        print(f"ERROR|scope=image:{idx}|kind={clean(k)}|message={clean(m)}")
    print(f"COUNT|ocr_images={ocr_images}")
    print(f"COUNT|identity_candidates={len(tokens)}")
    print(f"COUNT|errors={len(errors)}")
    if tokens:
        print("RESOLUTION|CARRIER_ASCII_IDENTITY_CANDIDATE_FOUND|verify candidate against source-labelled media metadata before use")
    elif errors:
        print("RESOLUTION|CARRIER_OCR_PARTIAL|do not repeat successful images; only retry failed image reads")
    else:
        print("RESOLUTION|CARRIER_ASCII_OCR_BOUNDED|no provenance-relevant ASCII/numeric token recovered from four matched-carrier images")
    print("EVIDENCE_BOUNDARY|OCR is heuristic; every candidate requires visual/source corroboration before becoming provenance evidence.")

if __name__=="__main__":main()
