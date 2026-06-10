#!/usr/bin/env python3
"""On-page audit dos sateites (texto/imagens/OpenGraph/schema/canonical/301).
Rodar ONDE OS SITES SAO ACESSIVEIS (Cloudflare bloqueia datacenter -> use Playwright
ou proxy residencial). Le Sat_Br_final.csv (coluna 'sat url'), gera onpage_audit.csv.
Deps: pip install requests beautifulsoup4   (ou playwright p/ contornar Cloudflare)"""
import csv, re, sys
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install requests beautifulsoup4")

UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36","Accept-Language":"pt-BR,pt;q=0.9"}

def audit(url):
    r=requests.get(url,headers=UA,timeout=20,allow_redirects=False)
    info=dict(status=r.status_code, redirect_to=r.headers.get("Location","") if 300<=r.status_code<400 else "")
    if info["redirect_to"]:  # registra 301/302 (podklejka)
        return info | dict(words=0,images=0,opengraph="",schema="",canonical="",h1="")
    r=requests.get(url,headers=UA,timeout=20)
    s=BeautifulSoup(r.text,"html.parser")
    for t in s(["script","style","noscript"]): t.extract()
    text=re.sub(r"\s+"," ",s.get_text(" ")).strip()
    canon=s.find("link",rel=lambda x:x and "canonical" in x)
    og=s.find("meta",property=lambda x:x and x.startswith("og:"))
    # schema @type(s)
    import json as _j
    types=set()
    for sc in BeautifulSoup(r.text,"html.parser").find_all("script",type="application/ld+json"):
        try:
            data=_j.loads(sc.string or "{}")
            for obj in (data if isinstance(data,list) else [data]):
                t=obj.get("@type") if isinstance(obj,dict) else None
                if t: types.add(t if isinstance(t,str) else ",".join(t))
        except: pass
    # hreflang/alternate + html lang
    hrefs=[(l.get("hreflang"),l.get("href")) for l in BeautifulSoup(r.text,"html.parser").find_all("link",rel="alternate") if l.get("hreflang")]
    htmltag=BeautifulSoup(r.text,"html.parser").find("html")
    lang=htmltag.get("lang","") if htmltag else ""
    h1=s.find("h1")
    return info | dict(
        words=len(text.split()),
        images=len(s.find_all("img")),
        opengraph="yes" if og else "no",
        schema=";".join(sorted(types)) if types else "no",
        canonical=canon["href"] if canon and canon.has_attr("href") else "",
        hreflang=" | ".join(f"{h}:{u}" for h,u in hrefs) if hrefs else "",
        html_lang=lang,
        h1=(h1.get_text(strip=True)[:60] if h1 else ""))

rows=[]
with open("Sat_Br_final.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        u=r["sat url"]; u=u if u.startswith("http") else "https://"+u
        try: a=audit(u)
        except Exception as e: a=dict(status="ERR",redirect_to=str(e)[:60],words=0,images=0,opengraph="",schema="",canonical="",h1="")
        rows.append([r["Brand name"],r["sat url"],a["status"],a["redirect_to"],
                     a["words"],a["images"],a["opengraph"],a["schema"],a["canonical"],
                     a.get("hreflang",""),a.get("html_lang",""),a["h1"]])
        print(r["sat url"],a["status"],"words=",a["words"],"img=",a["images"],"og=",a["opengraph"],"schema=",a["schema"],"canon=",a["canonical"][:40])

with open("onpage_audit.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["brand","sat url","http_status","redirect_to(301/302)",
        "words","images","opengraph","schema_markup","canonical","hreflang_alternate","html_lang","h1"]); w.writerows(rows)
print("\n-> onpage_audit.csv")
