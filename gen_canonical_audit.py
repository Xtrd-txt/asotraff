#!/usr/bin/env python3
"""Audit canonical/hreflang/301-podklejki dos sateites.
Para cada dominio: status, alvo do 301/302 (podklejka), canonical+hreflang DO DOMINIO
e canonical+hreflang DO SITE COLADO (alvo do redirect).
RODAR EM IP RESIDENCIAL / Playwright (Cloudflare bloqueia datacenter -> 403).
Deps: pip install requests beautifulsoup4
Alternativa server-side (sem bloqueio): DataForSEO OnPage instant_pages."""
import csv, collections, sys
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install requests beautifulsoup4")

UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36","Accept-Language":"es-CO,es;q=0.9"}

def head_meta(url):
    """GET sem seguir redirect -> (status, location). Se 200 -> parse meta."""
    try:
        r=requests.get(url,headers=UA,timeout=15,allow_redirects=False)
    except Exception as e:
        return {"status":"ERR","loc":str(e)[:50],"canonical":"","hreflang":"","lang":"","schema":""}
    if 300<=r.status_code<400:
        return {"status":r.status_code,"loc":r.headers.get("Location",""),
                "canonical":"","hreflang":"","lang":"","schema":""}
    s=BeautifulSoup(r.text,"html.parser")
    can=s.find("link",rel=lambda x:x and "canonical" in x)
    alts=[f'{l.get("hreflang")}:{l.get("href")}' for l in s.find_all("link",rel="alternate") if l.get("hreflang")]
    import re,json
    types=set()
    for sc in s.find_all("script",type="application/ld+json"):
        try:
            dd=json.loads(sc.string or "{}")
            for o in (dd if isinstance(dd,list) else [dd]):
                t=o.get("@type") if isinstance(o,dict) else None
                if t: types.add(t if isinstance(t,str) else ",".join(t))
        except: pass
    html=s.find("html")
    return {"status":r.status_code,"loc":"",
            "canonical":can["href"] if can and can.has_attr("href") else "",
            "hreflang":" | ".join(alts),"lang":html.get("lang","") if html else "",
            "schema":";".join(sorted(types))}

def reg(host):
    return host.split("://",1)[-1].split("/",1)[0]

rows=list(csv.DictReader(open("co_satellites_master.csv",encoding="utf-8")))
db=collections.defaultdict(set)
for r in rows: db[r["satellite_url"]].add(r["Brand"])

out=[]
for d in sorted(db):
    m=head_meta("https://"+d)
    glued_dom=glued_can=glued_href=""
    if str(m["status"]) in ("301","302","303","307","308") and m["loc"]:
        tgt=m["loc"] if m["loc"].startswith("http") else "https://"+d.rstrip("/")+m["loc"]
        glued_dom=reg(tgt)
        gm=head_meta(tgt if tgt.startswith("http") else "https://"+glued_dom)
        glued_can=gm["canonical"]; glued_href=gm["hreflang"]
    out.append([";".join(sorted(db[d])),d,m["status"],m["loc"],m["canonical"],m["hreflang"],
                m["lang"],m["schema"],glued_dom,glued_can,glued_href])
    print(d,m["status"],"->",m["loc"] or m["canonical"][:40])

with open("co_canonical_audit.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Brand","domain","http_status","redirect_target(podklejka)",
                "domain_canonical","domain_hreflang","domain_lang","domain_schema",
                "glued_domain","glued_canonical","glued_hreflang"])
    w.writerows(out)
print("\n-> co_canonical_audit.csv")
