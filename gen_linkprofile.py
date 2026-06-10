#!/usr/bin/env python3
"""Conta links por tipo a partir do Ahrefs batch_analysis (UTF-16).
Saida: link_profile_analysis.csv + agregados para a estrategia."""
import csv, collections
BATCH="/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/e9b83107-batch_analysis_20260610_142950.csv"
PARA="parasite_satellites_keywords.csv"
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h
def n(s):
    s=str(s).strip().replace(",","")
    try: return float(s)
    except: return 0.0

b2={}
with open(PARA,encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("sat url"): b2[host(r["sat url"])]=r["Brand name"]

def dtype(h):
    if h.endswith((".com.br",".net.br",".app.br",".gov.br")): return "EMD local (.br)"
    if h.endswith((".br.com",".uk.com")) or ".cassino.br.com" in h: return "subdomain-farm"
    if h.endswith((".lat",".one",".biz")): return "TLD barato"
    return "EMD geral (.com/.net/.bet)"

with open(BATCH,encoding="utf-16") as f: raw=f.read()
rows=[]
for ln in raw.splitlines():
    if not ln.strip(): continue
    p=[c.strip().strip('"').strip() for c in ln.split("\t")]
    if len(p)<31 or not p[0].isdigit(): continue
    d=host(p[1])
    rows.append(dict(brand=b2.get(d,"?"),domain=d,url=p[1],dtype=dtype(d),
        dr=n(p[6]),org_kw=int(n(p[8])),traffic=int(n(p[14])),
        ref_all=int(n(p[21])),ref_foll=int(n(p[22])),ref_nofoll=int(n(p[23])),
        ref_ip=int(n(p[24])),subnets=int(n(p[25])),
        bl_all=int(n(p[26])),bl_foll=int(n(p[27])),bl_nofoll=int(n(p[28])),
        bl_redirect=int(n(p[29])),bl_internal=int(n(p[30])),
        out_links=int(n(p[34]))))

with open("link_profile_analysis.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["brand","domain","domain_type","DR","organic_kw","traffic",
      "ref_domains","ref_foll","ref_nofoll","ref_ips","subnets",
      "backlinks","bl_followed","bl_nofollow","bl_301_redirect","bl_internal","outgoing_links",
      "pct_followed","pct_301","likely_drop"])
    for r in rows:
        pf=round(100*r["bl_foll"]/r["bl_all"],1) if r["bl_all"] else 0
        p3=round(100*r["bl_redirect"]/r["bl_all"],1) if r["bl_all"] else 0
        drop="yes" if (r["ref_all"]>=100 and r["org_kw"]<60) else ("maybe" if r["ref_all"]>=60 else "no")
        w.writerow([r["brand"],r["domain"],r["dtype"],r["dr"],r["org_kw"],r["traffic"],
          r["ref_all"],r["ref_foll"],r["ref_nofoll"],r["ref_ip"],r["subnets"],
          r["bl_all"],r["bl_foll"],r["bl_nofoll"],r["bl_redirect"],r["bl_internal"],r["out_links"],
          pf,p3,drop])

def stats(sub,label):
    if not sub: return
    import statistics as st
    med=lambda k:int(st.median([r[k] for r in sub]))
    avg=lambda k:round(sum(r[k] for r in sub)/len(sub),1)
    print(f"\n== {label} (n={len(sub)}) ==")
    print(f"  ref_domains  med={med('ref_all')} avg={avg('ref_all')} | foll med={med('ref_foll')}")
    print(f"  backlinks    med={med('bl_all')} avg={avg('bl_all')}")
    print(f"  301 redirect med={med('bl_redirect')} avg={avg('bl_redirect')} | dominios c/301>0: {sum(1 for r in sub if r['bl_redirect']>0)}")
    print(f"  internal BL  med={med('bl_internal')} (proxy paginas internas)")
    print(f"  outgoing lnk med={med('out_links')}")
    print(f"  organic_kw   med={med('org_kw')}")
    print(f"  DR           med={med('dr')}")

live=[r for r in rows if r["traffic"]>=50]
dead=[r for r in rows if r["traffic"]<50]
stats(live,"WINNERS (traffic>=50)")
stats(dead,"DEAD (traffic<50)")

print("\n== Tipos de dominio (todos) ==")
for t,c in collections.Counter(r["dtype"] for r in rows).most_common(): print(f"  {t:32} {c}")
print("\n== Tipos de dominio (so winners) ==")
for t,c in collections.Counter(r["dtype"] for r in live).most_common(): print(f"  {t:32} {c}")
print("\n== Drops provaveis (ref>=100 & kw<60) entre winners ==")
for r in sorted(live,key=lambda x:-x['ref_all']):
    if r["ref_all"]>=100 and r["org_kw"]<60:
        print(f"  {r['brand']:18} {r['domain']:32} ref={r['ref_all']:>4} kw={r['org_kw']:>3} 301={r['bl_redirect']:>3} traf={r['traffic']}")
print("\n== 301 podklejki (bl_redirect>0) entre TODOS ==")
for r in sorted(rows,key=lambda x:-x['bl_redirect'])[:12]:
    if r["bl_redirect"]>0: print(f"  {r['brand']:16} {r['domain']:30} 301-BL={r['bl_redirect']:>4} ref={r['ref_all']} traf={r['traffic']}")
