#!/usr/bin/env python3
"""Limpa brand_keywords_combined.csv: tira lixo global do cluster 777 Casino."""
import csv
rows=list(csv.DictReader(open("brand_keywords_combined.csv",encoding="utf-8")))

# modificadores que indicam OUTRO cassino (nao a marca BR '777 Casino')
JUNK={"love","hot","club","win","lucky","big","gold","golden","mega","vegas","royal","dragon",
 "panda","lord","gods","god","jackpot","social","house","classic","double","triple","wild","fortune",
 "lucky7","crazy","grand","star","diamond","silver","party","spin","spins","slots","slotomania",
 "heart","hearts","cash","money","real","cleopatra","buffalo","sweet","pop","fire","magic","funzpoints",
 "high","luckyland","chumba","pulsz","gunsbet","cherry","ruby","rich","golden","gametwist"}
OTHER_BRANDS={"brazino":"Brazino777","betano":"Betano","blaze":"Blaze","stake":"Stake","betfair":"Betfair"}

clean=[]; removed=0; moved=0
for r in rows:
    b=r["Brand name"]; kw=r["keyword"].lower(); v=int(r["search volume"]); kd=r["KD"]
    if b=="777 Casino":
        rb=next((OTHER_BRANDS[t] for t in OTHER_BRANDS if t in kw),None)
        if rb: clean.append([rb,r["keyword"],v,kd]); moved+=1; continue
        # '777' e nome global -> manter SO nucleo PT-BR (whitelist de tokens)
        ALLOWED={"777","777casino","777cassino","casino","cassino","bet","login","online","app",
                 "br","brasil","gratis","grátis","bonus","bônus","cadastro","baixar","jogo","jogos",
                 "jogar","mobile","vip","slot","slots","de","do","da"}
        words=set(w for w in kw.replace("."," ").replace("-"," ").split() if w)
        if words-ALLOWED:  # tem token estrangeiro/prefixo/junk -> remove
            removed+=1; continue
    clean.append([b,r["keyword"],v,kd])

clean.sort(key=lambda x:(x[0].lower(),-x[2]))
with open("brand_keywords_combined.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","keyword","search volume","KD"]); w.writerows(clean)

import collections
byb=collections.defaultdict(lambda:[0,0])
for b,k,v,kd in clean: byb[b][0]+=1; byb[b][1]+=v
print(f"Removido lixo 777: {removed} | reatribuido: {moved} | linhas finais: {len(clean)} | marcas: {len(byb)}")
print("\n== 777 Casino LIMPO ==")
for b,k,v,kd in clean:
    if b=="777 Casino": print(f"   {v:>6} KD={kd:>3} {k}")
