#!/usr/bin/env python3
"""Acha marcas de cassino BR LOW-COMPETITION com volume (do related-set cassino online)."""
import csv, re, statistics as st
F="/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/c129047d-google_br_cassinoonline_relatedterms_serps_20260610_162750.csv"
def n(s):
    s=str(s).strip().replace(",","")
    try: return float(s)
    except: return 0.0
raw=open(F,encoding="utf-16").read()
kws={}
for ln in raw.splitlines()[1:]:
    p=[c.strip().strip('"').strip() for c in ln.split("\t")]
    if len(p)<6: continue
    kw=p[0].lower().strip()
    if not kw: continue
    kd=n(p[3]); vol=int(n(p[4]))
    if kw not in kws or vol>kws[kw][0]: kws[kw]=(vol,kd)

# marcas EMERGENTES de cassino (token de variantes) — curado a partir do dump
EMERG={
 "CassinoBet":["cassinobet","cassino bet br","cassino.bet","cassino bets","cassino bet","um cassino bet"],
 "EJ Cassino":["ejcassino","ej cassino"],
 "777 Casino":["777 casino","777casino","777 cassino"],
 "Score Cassino":["score cassino","cassino scores","cassino score","cassino escore","cassino escore"],
 "Betino":["betino"],
 "Orozino":["orozino"],
 "OCS Bet":["ocs bet net","ocs bet","ocsbet"],
 "Jogoman":["jogoman"],
 "NN55":["nn55.com plataforma","nn55"],
 "13Bet":["13 bet casino","13bet","13 bet"],
 "Plataforma Ouro":["plataforma ouro"],
 "Portal Noca":["portal noca","noca bet","noca"],
 "FG Cassino":["fg jogo cassino","fg cassino","fg bet"],
 "NetBet":["netbet"],
 "Slot Agora":["slot agora"],
 "Jogo da Abelha":["jogo da abelha cassino","jogo da abelha"],
 "Betsson":["betsson"],"Cassino Pix":["plataforma cassino pix","cassino pix"],
}
def lab(kd):
    return "muito baixa" if kd<=10 else "baixa" if kd<=20 else "media" if kd<=35 else "alta"

rows=[]; detail=[]
for brand,tl in EMERG.items():
    matched=[(k,v,kd) for k,(v,kd) in kws.items() if any(re.search(r"(^|[^a-z0-9])"+re.escape(t)+r"([^a-z0-9]|$)",k) for t in tl)]
    if not matched: continue
    vol=sum(v for _,v,_ in matched); kds=[kd for _,_,kd in matched if kd>0]
    mk=int(st.median(kds)) if kds else 0; mn=int(min(kds)) if kds else 0
    rows.append([brand,len(matched),vol,mk,mn,lab(mn),"; ".join(sorted({k for k,_,_ in matched})[:5])])
    for k,v,kd in sorted(matched,key=lambda x:-x[1]): detail.append([brand,k,v,int(kd)])
# opportunity: volume alto + KD baixo -> score = vol/(minKD+1)
rows.sort(key=lambda r:-(r[2]/(r[4]+1)))
with open("lowcomp_casino_brands.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","n_keywords","total_volume","median_KD","min_KD","competicao","sample_keywords"]); w.writerows(rows)
with open("lowcomp_brand_keywords.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","keyword","volume","KD"]); w.writerows(detail)

print("== MARCAS LOW-COMP (ordenado por oportunidade vol/KD) ==")
print(f"  {'Brand':16}{'vol':>8}{'medKD':>7}{'minKD':>7}  competicao")
for b,nk,v,mk,mn,l,_ in rows:
    print(f"  {b:16}{v:>8}{mk:>7}{mn:>7}  {l}")
