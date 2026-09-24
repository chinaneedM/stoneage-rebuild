#!/usr/bin/env python3
"""Discover the public DiscMaster search form schema.

This probe fetches only the public search page and records normalized form
metadata so later archaeology probes can submit exact file/content searches
without guessing query parameter names. No DiscMaster file payload is fetched.
"""

from __future__ import annotations

import hashlib
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

SEARCH_URL="https://discmaster.textfiles.com/search"
UA="stoneage-rebuild-archaeology/1.0"


def clean(value,limit=1000):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


class SearchFormParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms=[]
        self._form=None
        self._select=None

    @staticmethod
    def attrs_dict(attrs):
        return {str(k).lower(): ("" if v is None else str(v)) for k,v in attrs}

    def handle_starttag(self,tag,attrs):
        tag=tag.lower()
        a=self.attrs_dict(attrs)
        if tag=="form":
            self._form={
                "action":a.get("action",""),
                "method":a.get("method","get").lower(),
                "inputs":[],
                "selects":[],
            }
            self.forms.append(self._form)
            return
        if self._form is None:
            return
        if tag=="input":
            self._form["inputs"].append({
                "name":a.get("name",""),
                "type":a.get("type","text").lower(),
                "value":a.get("value",""),
                "checked":"checked" in a,
                "placeholder":a.get("placeholder",""),
            })
        elif tag=="select":
            self._select={
                "name":a.get("name",""),
                "multiple":"multiple" in a,
                "options":[],
            }
            self._form["selects"].append(self._select)
        elif tag=="option" and self._select is not None:
            self._select["options"].append({
                "value":a.get("value",""),
                "selected":"selected" in a,
            })

    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag=="select":
            self._select=None
        elif tag=="form":
            self._form=None
            self._select=None


def fetch(url=SEARCH_URL,timeout=20):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=timeout) as response:
        body=response.read()
        return {
            "status":int(getattr(response,"status",response.getcode())),
            "final":response.geturl(),
            "body":body,
        }


def parse_forms(body):
    parser=SearchFormParser()
    parser.feed(body.decode("utf-8","replace"))
    return parser.forms


def main():
    print("StoneAge DiscMaster search-schema probe — R1")
    print("SCOPE|public-search-form-metadata|parameter-discovery|no-file-payload")
    try:
        result=fetch()
    except Exception as exc:
        print(f"ERROR|phase=fetch|kind={type(exc).__name__}|message={clean(exc)}")
        print("RESOLUTION|INCONCLUSIVE|DiscMaster search page unavailable")
        return

    body=result["body"]
    forms=parse_forms(body)
    print(
        f"FETCH|status={result['status']}|bytes={len(body)}|"
        f"sha256={hashlib.sha256(body).hexdigest()}|final={clean(result['final'])}"
    )
    print(f"COUNT|forms|{len(forms)}")
    named=0
    for n,form in enumerate(forms,1):
        target=urljoin(result["final"],form["action"] or result["final"])
        print(
            f"FORM|index={n}|method={clean(form['method'])}|"
            f"action={clean(target)}|inputs={len(form['inputs'])}|selects={len(form['selects'])}"
        )
        for field in form["inputs"]:
            if field["name"]:
                named+=1
            print(
                f"INPUT|form={n}|name={clean(field['name'])}|type={clean(field['type'])}|"
                f"value={clean(field['value'])}|checked={int(field['checked'])}|"
                f"placeholder={clean(field['placeholder'])}"
            )
        for select in form["selects"]:
            if select["name"]:
                named+=1
            values=",".join(
                (("*" if option["selected"] else "")+clean(option["value"],120))
                for option in select["options"]
            )
            print(
                f"SELECT|form={n}|name={clean(select['name'])}|multiple={int(select['multiple'])}|"
                f"options={len(select['options'])}|values={clean(values,1800)}"
            )

    print(f"COUNT|named_fields|{named}")
    if forms and named:
        print("RESOLUTION|DISCMaster_SEARCH_SCHEMA_DERIVED|use exact field names for follow-on searches")
    else:
        print("RESOLUTION|INCONCLUSIVE|no named search fields recovered")


if __name__=="__main__":
    main()
