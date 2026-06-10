#!/usr/bin/env python3
"""Filtra registro -> apenas sateites NAO oficiais.
Colunas: Brand name, keywords, search volume (BR, ESTIMADO), sat url
Volumes sao ESTIMATIVAS (nao DataForSEO)."""
import csv, re

def host(u): return u.split("://",1)[-1].split("/",1)[0]

# volume BR estimado do termo de marca principal (mensal)
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

def kw_and_vol(brand, dom):
    """Escolhe keyword de marca + volume estimado pelo padrao do dominio."""
    base = brand_vol.get(brand, 20000)
    b = brand.lower().replace(".bet","").replace(".game"," game").replace("777","777").replace(".","").strip()
    b = re.sub(r"\s+"," ",b)
    d = dom.lower()
    if "cassino" in d or "casino" in d or "cazino" in d:
        return f"{b} cassino", int(base*0.35)
    if "oficial" in d:
        return f"{b} site oficial", int(base*0.12)
    if "codigo" in d or "promo" in d or "cupom" in d:
        return f"codigo promocional {b}", int(base*0.10)
    if "app" in d:
        return f"{b} app", int(base*0.09)
    if "login" in d or "entrar" in d:
        return f"{b} login", int(base*0.11)
    if "bonus" in d or "bonus" in d:
        return f"{b} bonus", int(base*0.10)
    return b, base  # termo de marca puro

rows_out = []
with open("casino_brand_registry.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["risco_status"] == "official":      # remove oficiais .bet.br
            continue
        kw, vol = kw_and_vol(r["marca"], r["dominio"])
        rows_out.append([r["marca"], kw, vol, r["url"]])

# ordena por marca, depois maior volume
rows_out.sort(key=lambda x:(x[0].lower(), -x[2]))

with open("parasite_satellites_keywords.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Brand name","keywords","search volume","sat url"])
    for br,kw,vol,url in rows_out:
        w.writerow([br,kw,f"{vol:,}",url])

print("Sateites (linhas):", len(rows_out))
print("Marcas unicas:", len({r[0] for r in rows_out}))
