#!/usr/bin/env python3
"""Extrai clusters de marca dos 2 novos arquivos (matching+related terms) e funde
no brand_keywords_combined.csv."""
import csv, re, collections
NEW=["/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/840a1357-google_br_13betcasino777ca_matchingterms_20260610_172538.csv",
     "/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/47f6e1ce-google_br_13betcasino777cas_relatedterms_20260610_172640.csv"]
def num(s):
    s=str(s).strip().replace(",","")
    try:return float(s)
    except:return 0.0

kws={}  # keyword -> (vol,kd)
for path in NEW:
    raw=open(path,encoding="utf-16").read()
    for ln in raw.splitlines()[1:]:
        p=[c.strip().strip('"').strip() for c in ln.split("\t")]
        if len(p)<5 or not p[0].isdigit(): continue
        kw=p[1].lower().strip(); kd=num(p[3]); vol=int(num(p[4]))
        if not kw: continue
        if kw not in kws or vol>kws[kw][0]: kws[kw]=(vol,kd)
print("Unique keywords (novos arquivos):",len(kws))

# token -> marca (conhecidas + emergentes; ordem por especificidade)
M={
 "777 casino":"777 Casino","777casino":"777 Casino","777 cassino":"777 Casino","777cassino":"777 Casino",
 "casino 777":"777 Casino","cassino 777":"777 Casino",
 "cassinobet":"CassinoBet","cassino bet":"CassinoBet","cassino.bet":"CassinoBet","cassino bets":"CassinoBet",
 "ejcassino":"EJ Cassino","ej cassino":"EJ Cassino","ej bet":"EJ Cassino",
 "13bet":"13Bet","13 bet":"13Bet",
 "score cassino":"Score Cassino","cassino score":"Score Cassino","cassino scores":"Score Cassino","cassino escore":"Score Cassino",
 "betino":"Betino","orozino":"Orozino","ocs bet":"OCS Bet","ocsbet":"OCS Bet","jogoman":"Jogoman",
 "nn55":"NN55","plataforma ouro":"Plataforma Ouro","portal noca":"Portal Noca","noca bet":"Portal Noca",
 "fg cassino":"FG Cassino","fg bet":"FG Cassino","netbet":"NetBet","slot agora":"Slot Agora",
 "jogo da abelha":"Jogo da Abelha",
 "betano":"Betano","bet365":"Bet365","blaze":"Blaze","1xbet":"1xBet","pixbet":"Pixbet","estrelabet":"EstrelaBet",
 "estrela bet":"EstrelaBet","esportes da sorte":"Esportes da Sorte","esporte da sorte":"Esportes da Sorte",
 "kto":"KTO","sportingbet":"Sportingbet","betnacional":"Betnacional","superbet":"Superbet","novibet":"Novibet",
 "brazino":"Brazino777","betfair":"Betfair","stake":"Stake","galera":"Galera.bet","vai de bet":"Vai de Bet",
 "vaidebet":"Vai de Bet","mostbet":"Mostbet","melbet":"Melbet","1win":"1win","betsson":"Betsson",
 "betwinner":"Betwinner","pin-up":"Pin-Up","pin up":"Pin-Up","pinup":"Pin-Up","parimatch":"Parimatch",
 "22bet":"22Bet","bodog":"Bodog","cbet":"Cbet","f12":"F12.bet","bet7k":"Bet7k","ggbet":"GGBet",
 "megapari":"Megapari","linebet":"Linebet","roobet":"Roobet","betobet":"Betobet","betfury":"BetFury",
 "brabet":"BraBet","betpix":"BetPix365","bet da sorte":"Bet da Sorte","betdasorte":"Bet da Sorte",
 "aposta ganha":"Aposta Ganha","cassino pix":"Cassino Pix",
}
toks=sorted(M,key=len,reverse=True)
def brand_of(kw):
    for t in toks:
        if re.search(r"(^|[^a-z0-9])"+re.escape(t)+r"([^a-z0-9]|$)",kw): return M[t]
    return None

# merge: comeca do combinado anterior
combined={}
try:
    for r in csv.DictReader(open("brand_keywords_combined.csv",encoding="utf-8")):
        combined[(r["Brand name"],r["keyword"])]=(int(r["search volume"]),"")
except FileNotFoundError: pass

added=0
for kw,(vol,kd) in kws.items():
    b=brand_of(kw)
    if not b: continue
    key=(b,kw)
    if key not in combined: added+=1
    combined[key]=(vol,int(kd))

out=sorted([x for x in combined.items() if x[1][0]>0],key=lambda x:(x[0][0].lower(),-x[1][0]))
with open("brand_keywords_combined.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","keyword","search volume","KD"])
    for (b,k),(v,kd) in out: w.writerow([b,k,v,kd])

byb=collections.defaultdict(lambda:[0,0])
for (b,k),(v,kd) in combined.items(): byb[b][0]+=1; byb[b][1]+=v
print(f"Novas linhas adicionadas: {added} | total: {len(out)} | marcas: {len(byb)}")
print("\n== Clusters por marca (n_kw, vol total) — foco top-3 + emergentes ==")
for b,(n,v) in sorted(byb.items(),key=lambda x:-x[1][1]):
    print(f"  {b:18} kw={n:3} vol_total={v:>9}")
print("\n== TOP-3 detalhe ==")
for target in ("CassinoBet","777 Casino","EJ Cassino"):
    ks=sorted([(k,v,kd) for (b,k),(v,kd) in combined.items() if b==target],key=lambda x:-x[1])
    print(f"\n  [{target}] ({len(ks)} ключів):")
    for k,v,kd in ks[:15]: print(f"     {v:>7}  KD={kd}  {k}")
