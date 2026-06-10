#!/usr/bin/env python3
"""Re-analise com dados Ahrefs (batch_analysis). Filtra trafego 0 e baixa-freq.
Saidas: filtered_satellites_ahrefs.csv + brand_reanalysis.csv"""
import csv, collections

BATCH="/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/e9b83107-batch_analysis_20260610_142950.csv"
PARA ="parasite_satellites_keywords.csv"
THRESHOLD=50  # corta trafego < 50 (0 + baixa-freq)

def H(u):
    u=u.split("://",1)[-1]
    return u.split("/",1)[0].lower().lstrip("www.") if False else u.split("/",1)[0].lower()
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h
def num(s):
    s=s.strip().replace(",","")
    if s in("","-"): return 0.0
    try: return float(s)
    except: return 0.0

# brand map host->brand
b2=dict()
with open(PARA,encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("sat url"): b2[host(r["sat url"])]=r["Brand name"]

# parse Ahrefs (UTF-16, tab, quoted)
rows=[]
with open(BATCH,encoding="utf-16") as f:
    raw=f.read()
for ln in raw.splitlines():
    if not ln.strip(): continue
    parts=[p.strip().strip('"').strip() for p in ln.split("\t")]
    if len(parts)<17 or parts[0] in("#",""): continue
    if not parts[0].isdigit(): continue
    target=parts[1]; dr=num(parts[6]); rank=parts[7]; tot=int(num(parts[8]))
    top3=int(num(parts[9])); traf=int(num(parts[14])); val=num(parts[15]); ctry=parts[16]
    dom=host(target)
    brand=b2.get(dom) or b2.get(dom.lstrip("www."),"?")
    rows.append(dict(brand=brand,domain=dom,url=target,dr=dr,kw=tot,top3=top3,
                     traffic=traf,value=val,country=ctry))

kept=[r for r in rows if r["traffic"]>=THRESHOLD]
dropped=[r for r in rows if r["traffic"]<THRESHOLD]
kept.sort(key=lambda r:-r["traffic"])

with open("filtered_satellites_ahrefs.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","domain","sat url","DR","organic_keywords","kw_top3","organic_traffic","traffic_value_usd","top_country"])
    for r in kept: w.writerow([r["brand"],r["domain"],r["url"],r["dr"],r["kw"],r["top3"],r["traffic"],round(r["value"],2),r["country"]])

# re-analise por marca (so sobreviventes)
agg=collections.defaultdict(lambda:dict(n=0,traf=0,val=0.0,top=("",0)))
for r in kept:
    a=agg[r["brand"]]; a["n"]+=1; a["traf"]+=r["traffic"]; a["val"]+=r["value"]
    if r["traffic"]>a["top"][1]: a["top"]=(r["domain"],r["traffic"])
bre=sorted(agg.items(),key=lambda x:-x[1]["traf"])
with open("brand_reanalysis.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","surviving_parasites","total_parasite_traffic","total_value_usd","top_parasite","top_parasite_traffic"])
    for b,a in bre: w.writerow([b,a["n"],a["traf"],round(a["val"],2),a["top"][0],a["top"][1]])

print(f"Total dominios Ahrefs: {len(rows)} | MANTIDOS (>= {THRESHOLD}): {len(kept)} | CORTADOS: {len(dropped)}")
print(f"Marcas com parasita ativo: {len(agg)} / {len({r['brand'] for r in rows})}")
print("\nTOP marcas por trafego parasita capturado:")
for b,a in bre[:12]:
    print(f"  {b:20} sats={a['n']:2} trafego={a['traf']:>7} valor=${a['val']:>9.0f} top={a['top'][0]}")
brands_all={r['brand'] for r in rows}; brands_kept=set(agg)
print("\nMarcas SEM parasita com trafego (rede inefetiva):")
print(" ", ", ".join(sorted(brands_all-brands_kept)))
