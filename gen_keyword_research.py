#!/usr/bin/env python3
"""Research keywords 'cassino online' related: extrai brandados, estrutura, acha
marcas BR low-competition com volume."""
import csv, re, collections, statistics as st
F="/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/c129047d-google_br_cassinoonline_relatedterms_serps_20260610_162750.csv"
def n(s):
    s=str(s).strip().replace(",","")
    try: return float(s)
    except: return 0.0

with open(F,encoding="utf-16") as f: raw=f.read()
# unique keyword -> (volume, kd)
kws={}
for ln in raw.splitlines()[1:]:
    if not ln.strip(): continue
    p=[c.strip().strip('"').strip() for c in ln.split("\t")]
    if len(p)<6: continue
    kw=p[0].lower().strip()
    if not kw: continue
    kd=n(p[3]); vol=int(n(p[4]))
    if kw not in kws or vol>kws[kw][0]: kws[kw]=(vol,kd)
print("Unique keywords:",len(kws))

# marcas conhecidas (token -> canonico)
B={"betano":"Betano","bet365":"Bet365","blaze":"Blaze","1xbet":"1xBet","pixbet":"Pixbet",
"estrela bet":"EstrelaBet","estrelabet":"EstrelaBet","esporte da sorte":"Esportes da Sorte",
"esportes da sorte":"Esportes da Sorte","kto":"KTO","sportingbet":"Sportingbet","betnacional":"Betnacional",
"bet nacional":"Betnacional","superbet":"Superbet","novibet":"Novibet","brazino":"Brazino777",
"betfair":"Betfair","stake":"Stake","galera":"Galera.bet","vai de bet":"Vai de Bet","vaidebet":"Vai de Bet",
"mostbet":"Mostbet","melbet":"Melbet","1win":"1win","betsson":"Betsson","betwinner":"Betwinner",
"pin-up":"Pin-Up","pin up":"Pin-Up","pinup":"Pin-Up","parimatch":"Parimatch","22bet":"22Bet","bodog":"Bodog",
"cbet":"Cbet","f12":"F12.bet","bet7k":"Bet7k","7k":"Bet7k","ggbet":"GGBet","gg bet":"GGBet","megapari":"Megapari",
"linebet":"Linebet","roobet":"Roobet","sportaza":"Sportaza","betobet":"Betobet","betfury":"BetFury",
"leon":"LeonBet","20bet":"20Bet","brabet":"BraBet","br4bet":"Br4Bet","lotogreen":"LotoGreen","betpix":"BetPix365",
"betpix365":"BetPix365","hanz":"Hanz","bullsbet":"BullsBet","jonbet":"JonBet","rei do pitaco":"Rei do Pitaco",
"reidopitaco":"Rei do Pitaco","aposta ganha":"Aposta Ganha","apostaganha":"Aposta Ganha","betboom":"BetBoom",
"betao":"Betao","betão":"Betao","h2bet":"H2Bet","lampions":"Lampions Bet","mcgames":"MC Games","mc games":"MC Games",
"bet da sorte":"Bet da Sorte","betdasorte":"Bet da Sorte","pagbet":"PagBet","luva bet":"Luva Bet","luvabet":"Luva Bet",
"verabet":"Vera Bet","vera bet":"Vera Bet","betvip":"BetVip","betsul":"BetSul","rivalo":"Rivalo","betmotion":"BetMotion",
"betfast":"BetFast","seguro bet":"Seguro Bet","segurobet":"Seguro Bet","tivobet":"TivoBet","betpark":"BetPark",
"p9":"P9","faz1bet":"Faz1Bet","betesporte":"BetEsporte","betspeed":"BetSpeed","donald":"Donald Bet","cassino pix":"Cassino Pix"}
toks=sorted(B,key=len,reverse=True)

def brand_of(kw):
    for t in toks:
        if re.search(r"(^|[^a-z0-9])"+re.escape(t)+r"([^a-z0-9]|$)",kw): return B[t]
    return None

branded=collections.defaultdict(list); nonbrand=[]
for kw,(vol,kd) in kws.items():
    b=brand_of(kw)
    if b: branded[b].append((kw,vol,kd))
    else: nonbrand.append((kw,vol,kd))

# (1) branded keywords estruturado
with open("branded_keywords.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","keyword","volume","KD"])
    for b in sorted(branded):
        for kw,vol,kd in sorted(branded[b],key=lambda x:-x[1]): w.writerow([b,kw,vol,kd])

# (2) brand summary + low competition flag
rows=[]
for b,lst in branded.items():
    vols=[v for _,v,_ in lst]; kds=[k for _,_,k in lst if k>0]
    rows.append((b,len(lst),sum(vols),int(st.median(kds)) if kds else 0,min(kds) if kds else 0))
rows.sort(key=lambda x:-x[2])
with open("brand_keyword_summary.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","n_keywords","total_volume","median_KD","min_KD"]); w.writerows(rows)

# (3) emerging/unknown brand-like tokens (nao na lista) com pattern de marca
pat=re.compile(r"\b([a-z]{2,}(?:bet|win|777|bull|luck|sorte|cassino|casino|aposta))\b|\b(bet[a-z0-9]{2,}|[a-z]{3,}bet)\b")
cand=collections.defaultdict(lambda:[0,[]])
for kw,vol,kd in nonbrand:
    for m in pat.finditer(kw):
        tok=[g for g in m.groups() if g][0]
        if tok in ("aposta","apostas","casino","cassino","betano"): continue
        cand[tok][0]+=vol; cand[tok][1].append(kd)
emerg=sorted(((t,v[0],int(st.median(v[1])) if v[1] else 0) for t,v in cand.items() if v[0]>=300),key=lambda x:-x[1])

print("\n== BRANDS por volume (todos brandados) ==")
for b,nk,tv,mk,mnk in rows[:25]:
    print(f"  {b:18} kw={nk:3} vol={tv:>8} medKD={mk:>3} minKD={mnk}")
print("\n== LOW-COMP brands (medKD<=12 & vol>=1000) ==")
for b,nk,tv,mk,mnk in sorted(rows,key=lambda x:(x[3],-x[2])):
    if mk<=12 and tv>=1000: print(f"  {b:18} vol={tv:>7} medKD={mk:>2} minKD={mnk} kw={nk}")
print("\n== Possiveis marcas EMERGENTES (nao na lista) ==")
for t,v,mk in emerg[:25]: print(f"  {t:18} vol={v:>7} medKD={mk}")
print("\nnon-branded keywords:",len(nonbrand)," | branded:",sum(len(v) for v in branded.values()))
