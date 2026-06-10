#!/usr/bin/env python3
"""Parse 2 SERP files (UTF-16): per-keyword data for live satellites + .gov.br parasites."""
import csv, glob, collections

SERPS=[
 "/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/5d78e841-google_br_1win1xbet20b_matchingterms_serps_20260610_143239.csv",
 "/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/becfb81b-google_br_1win1xbet20b_matchingterms_serps_20260610_143316.csv",
]
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h
def num(s):
    s=str(s).strip().replace(",","")
    try: return float(s)
    except: return 0.0

# live satellites + brand map
live=dict()
with open("filtered_satellites_ahrefs.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f): live[r["domain"]]=r["Brand name"]
# ALL catalogued parasite domains (broader match)
allpar=dict()
with open("parasite_satellites_keywords.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("sat url"): allpar[host(r["sat url"])]=r["Brand name"]

# brand detection for gov parasites (token match)
brand_tokens={"blaze":"Blaze","bet365":"Bet365","betano":"Betano","1xbet":"1xBet","sportingbet":"Sportingbet",
 "kto":"KTO","betnacional":"Betnacional","pixbet":"Pixbet","estrela":"EstrelaBet","superbet":"Superbet",
 "novibet":"Novibet","brazino":"Brazino777","betfair":"Betfair","stake":"Stake","galera":"Galera.bet",
 "esporte":"Esportes da Sorte","vaidebet":"Vai de Bet","vai-de-bet":"Vai de Bet","mostbet":"Mostbet",
 "melbet":"Melbet","1win":"1win","betsson":"Betsson","betwinner":"Betwinner","pin-up":"Pin-Up","pinup":"Pin-Up",
 "parimatch":"Parimatch","22bet":"22Bet","20bet":"20Bet","bodog":"Bodog","cbet":"Cbet","f12":"F12.bet",
 "bet7k":"Bet7k","7k":"Bet7k","ggbet":"GGBet","gg-bet":"GGBet","megapari":"Megapari","linebet":"Linebet",
 "roobet":"Roobet","sportaza":"Sportaza","betobet":"Betobet","betfury":"BetFury","leon":"LeonBet"}

def parse(path):
    rows=[]
    for enc in ("utf-16","utf-8-sig","utf-8"):
        try:
            with open(path,encoding=enc) as f: raw=f.read()
            if "\t" in raw: break
        except: continue
    lines=raw.splitlines()
    for ln in lines[1:]:
        if not ln.strip(): continue
        p=[c.strip().strip('"').strip() for c in ln.split("\t")]
        if len(p)<17: continue
        # cols: 0 Keyword,1 URL,2 Country,3 Difficulty,4 Volume,...,12 Traffic,...,15 Position,16 Type,17 Title
        rows.append(dict(kw=p[0],url=p[1],vol=int(num(p[4])),kd=p[3],
                         traffic=int(num(p[12])),pos=p[15],typ=p[16],
                         title=p[17] if len(p)>17 else ""))
    return rows

allrows=[]
for s in SERPS: allrows+=parse(s)
# dedup identical (kw,url)
seen=set(); rows=[]
for r in allrows:
    k=(r["kw"],r["url"])
    if k in seen: continue
    seen.add(k); rows.append(r)

# (1) per-keyword for ALL catalogued parasite domains found in SERPs
per=[]
for r in rows:
    d=host(r["url"])
    if d in allpar and r["typ"]=="Organic":
        is_live="yes" if d in live else "no"
        per.append([allpar[d],d,is_live,r["kw"],r["vol"],r["pos"],r["traffic"],r["kd"],r["url"]])
per.sort(key=lambda x:(x[0],-x[6]))
with open("satellite_keyword_serp.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["Brand name","domain","is_live(>=50traf)","keyword","kw_volume","position","traffic_on_kw","KD","url"]);w.writerows(per)
covered=sorted({r[1] for r in per})
print("Parasite domains found in SERP exports:",len(covered))
for c in covered: print("   ",c)

# (2) .gov.br parasites
gov=[]
for r in rows:
    d=host(r["url"])
    if ".gov.br" in d and r["typ"]=="Organic":
        b="?"
        u=r["url"].lower()
        for tok,bn in brand_tokens.items():
            if tok in u: b=bn; break
        gov.append([b,d,r["kw"],r["vol"],r["pos"],r["traffic"],r["url"]])
# dedup by url, keep max traffic
gd={}
for g in gov:
    key=g[6]
    if key not in gd or g[5]>gd[key][5]: gd[key]=g
gov=sorted(gd.values(),key=lambda x:-x[5])
with open("gov_parasites.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["Brand name","gov_domain","keyword","kw_volume","position","traffic_on_kw","url"]);w.writerows(gov)

print(f"SERP rows: {len(rows)} | live-sat keyword rows: {len(per)} | gov parasite URLs: {len(gov)}")
print("\n== Per-keyword: catalogued satellites found in SERP ==")
for x in sorted(per,key=lambda r:-r[6]):
    print(f"  {x[0]:14} live={x[2]:3} {x[3]:42} pos#{x[5]:>3} traf={x[6]:>6} {x[1]}")
print("\n== .gov.br parasites (by traffic) ==")
gb=collections.defaultdict(lambda:[0,0])
for g in gov: gb[g[0]][0]+=1; gb[g[0]][1]+=g[5]
for b,(n,t) in sorted(gb.items(),key=lambda x:-x[1][1]):
    print(f"  {b:18} urls={n:2} traffic={t:>7}")
print("\nTop gov URLs:")
for g in gov[:12]:
    print(f"  {g[0]:14} pos#{g[4]:>3} traf={g[5]:>6} kw='{g[2]}' {g[6][:70]}")
