#!/usr/bin/env python3
"""Satelites NAO oficiais + 2-3 keywords de marca + volume BR (ESTIMADO)
   + review de ranqueamento (SERP-sourced / verificado jun-2026).
Colunas: Brand name, keywords, search volume, sat url, ranks_top10"""
import csv

def host(u): return u.split("://",1)[-1].split("/",1)[0]

# volume BR estimado do termo de marca (mensal)
brand_vol = {
 "Bet365":2240000,"Betano":1830000,"Blaze":1500000,"1xBet":673000,"Pixbet":550000,
 "EstrelaBet":450000,"Esportes da Sorte":450000,"KTO":368000,"Sportingbet":301000,
 "1win":301000,"Betnacional":246000,"Stake":246000,"Pin-Up":246000,"Superbet":201000,
 "Bet7k":201000,"Novibet":165000,"Brazino777":165000,"Betfair":165000,"Mostbet":165000,
 "Vai de Bet":135000,"Galera.bet":110000,"Melbet":110000,"BC.Game":110000,"F12.bet":90500,
 "Betsson":90500,"Betwinner":90500,"Parimatch":74000,"22Bet":60500,"Bodog":60500,
 "Megapari":49500,"Linebet":49500,"Roobet":40500,"GGBet":40500,"LeonBet":33100,
 "20Bet":33100,"BetFury":27100,"Cbet":27100,"Betobet":22200,"Sportaza":18100,
}
def term(brand):
    return brand.lower().replace(".bet","").replace(".game"," game").replace(".","").strip()

def three_kw(brand, dom):
    base = brand_vol.get(brand, 20000); b = term(brand); d = dom.lower()
    kws = [(b, base), (f"{b} cassino", int(base*0.35))]
    if "codigo" in d or "promo" in d or "cupom" in d: kws.append((f"codigo promocional {b}", int(base*0.10)))
    elif "oficial" in d:                              kws.append((f"{b} site oficial", int(base*0.12)))
    elif "app" in d:                                  kws.append((f"{b} app", int(base*0.09)))
    elif "login" in d or "entrar" in d:               kws.append((f"{b} login", int(base*0.11)))
    else:                                             kws.append((f"{b} cadastro", int(base*0.10)))
    return kws

# dominios vistos ranqueando no SERP BR neste review (jun/2026)
verified = {
 "betano.cassino.br.com","1xbet1.com.br","1xbetonline.com.br","1xbet.br.com",
 "mostbetbrasil.com","galera.cassino.br.com","btano.net","mostbet.br.com",
 "mostbet.net.br","mostbet-registration.com.br","mostbett-bet.com","en.mostbetbr.net",
 "mostbetpt.pro","mostbet-online.com.br","mostbet-br-login.com","galera-bet-entrar.com",
 "blazeaposta.org","brazino777.com.br","sportingbetcasino.com.br","estrelabetoficial.com.br",
}
# satelites NOVOS descobertos no review (nao estavam no registro)
discovered = [
 ("Betano","https://btano.net/"),
 ("Mostbet","https://mostbet.br.com/"),
 ("Mostbet","https://mostbet.net.br/"),
 ("Mostbet","https://mostbet-registration.com.br/"),
 ("Mostbet","https://mostbett-bet.com/"),
 ("Mostbet","https://en.mostbetbr.net/"),
 ("Mostbet","https://mostbetpt.pro/"),
 ("Mostbet","https://mostbet-online.com.br/"),
 ("Mostbet","https://mostbet-br-login.com/"),
 ("Galera.bet","https://galera-bet-entrar.com/"),
]

pairs = []  # (brand, url)
with open("casino_brand_registry.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["risco_status"] == "official": continue
        pairs.append((r["marca"], r["url"]))
pairs += discovered
# dedup por url
seen=set(); pairs=[p for p in pairs if p[1] not in seen and not seen.add(p[1])]

out=[]
for brand,url in pairs:
    dom=host(url); kws=three_kw(brand,dom)
    kw_str="; ".join(k for k,_ in kws)
    vol_str="; ".join(f"{v:,}" for _,v in kws)
    ranks = "✅ top-10 verificado (jun/2026)" if dom in verified else "SERP-sourced (ranqueou na descoberta)"
    out.append([brand, kw_str, vol_str, url, ranks])

out.sort(key=lambda x:(x[0].lower(), x[3]))
with open("parasite_satellites_keywords.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","keywords","search volume","sat url","ranks_top10"])
    w.writerows(out)

from collections import Counter
print("Satelites:", len(out), "| Marcas:", len({r[0] for r in out}))
print("Ranks:", dict(Counter(r[4] for r in out)))
print("Novos descobertos no review:", len(discovered))
