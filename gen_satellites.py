#!/usr/bin/env python3
"""Separa ESPELHOS do operador (remove) de PARASITAS que manipulam o nome (mantem).
Sem WHOIS/redirect (403) -> classificacao LEXICAL + whitelist de operador.
Saida: parasite_satellites_keywords.csv (so parasitas) + removed_mirrors.csv"""
import csv, re

def host(u):
    h = u.split("://",1)[-1].split("/",1)[0]
    return h[4:] if h.startswith("www.") else h
def norm(s): return re.sub(r"[^a-z0-9]","", s.lower())

cores = {
 "Betano":{"betano"},"Bet365":{"bet365"},"Blaze":{"blaze"},"1xBet":{"1xbet"},
 "Pixbet":{"pixbet"},"EstrelaBet":{"estrelabet"},"Esportes da Sorte":{"esportesdasorte"},
 "KTO":{"kto"},"Sportingbet":{"sportingbet"},"1win":{"1win"},"Betnacional":{"betnacional"},
 "Stake":{"stake"},"Pin-Up":{"pinup"},"Superbet":{"superbet"},"Bet7k":{"bet7k","7k"},
 "Novibet":{"novibet"},"Brazino777":{"brazino777","brazino"},"Betfair":{"betfair"},
 "Mostbet":{"mostbet"},"Vai de Bet":{"vaidebet"},"Galera.bet":{"galera","galerabet"},
 "Melbet":{"melbet"},"BC.Game":{"bcgame","bc1game","bc1"},"F12.bet":{"f12bet","f12"},
 "Betsson":{"betsson"},"Betwinner":{"betwinner"},"Parimatch":{"parimatch"},"22Bet":{"22bet"},
 "Bodog":{"bodog"},"Megapari":{"megapari"},"Linebet":{"linebet"},"Roobet":{"roobet"},
 "GGBet":{"ggbet"},"LeonBet":{"leon","leonbet"},"20Bet":{"20bet"},"BetFury":{"betfury","bf1"},
 "Cbet":{"cbet"},"Betobet":{"betobet"},"Sportaza":{"sportaza"},
}
WHITELIST = {  # dominios curtos/legados provaveis do operador -> ESPELHO (remove)
 "estrelabet.com","galera.bet","brazino777.com.br","bet7k.com","pixbet.com","f12-bet.com",
 "betfair.cat","leon.bet","leonbet.com.br","roobet.com","1win.com.br","1xbet.com.br",
 "br.bc1.game","bf1.io",
}
FARM = (".br.com",".uk.com",".anjeangola.org",".lat",".one",".xyz",".net.br",".app.br",".net",".biz")
TOKENS = ["brasil","brazil","oficial","online","aposta","cassino","casino","cazino","login",
          "entrar","vip","promo","cupom","codigo","bonus","jogo","site","pro","sucesso","br-","-br"]

def classify(brand, url):
    h = host(url); seg0 = norm(h.split(".",1)[0]); cs = cores.get(brand,set())
    if h in WHITELIST: return "espelho","whitelist operador (dominio nu/legado)"
    if h.endswith(FARM):  return "parasita", f"subdominio/TLD-farm ({[s for s in FARM if h.endswith(s)][0]})"
    tk = [t for t in TOKENS if t in h]
    if tk:                return "parasita", f"token manipulacao: {tk[0]}"
    if seg0.endswith("br") and seg0 not in cs: return "parasita","label termina em 'br'"
    if seg0 in cs:        return "espelho","nome de marca nu em TLD generico"
    return "parasita","typosquat/variacao do label"

# keywords + volume (ESTIMADO)
brand_vol = {"Bet365":2240000,"Betano":1830000,"Blaze":1500000,"1xBet":673000,"Pixbet":550000,
 "EstrelaBet":450000,"Esportes da Sorte":450000,"KTO":368000,"Sportingbet":301000,"1win":301000,
 "Betnacional":246000,"Stake":246000,"Pin-Up":246000,"Superbet":201000,"Bet7k":201000,"Novibet":165000,
 "Brazino777":165000,"Betfair":165000,"Mostbet":165000,"Vai de Bet":135000,"Galera.bet":110000,
 "Melbet":110000,"BC.Game":110000,"F12.bet":90500,"Betsson":90500,"Betwinner":90500,"Parimatch":74000,
 "22Bet":60500,"Bodog":60500,"Megapari":49500,"Linebet":49500,"Roobet":40500,"GGBet":40500,
 "LeonBet":33100,"20Bet":33100,"BetFury":27100,"Cbet":27100,"Betobet":22200,"Sportaza":18100}
def term(b): return b.lower().replace(".bet","").replace(".game"," game").replace(".","").strip()
def three_kw(brand, dom):
    base=brand_vol.get(brand,20000); b=term(brand); d=dom.lower()
    k=[(b,base),(f"{b} cassino",int(base*.35))]
    if   any(x in d for x in("codigo","promo","cupom")): k.append((f"codigo promocional {b}",int(base*.10)))
    elif "oficial" in d:                                 k.append((f"{b} site oficial",int(base*.12)))
    elif "app" in d:                                     k.append((f"{b} app",int(base*.09)))
    elif any(x in d for x in("login","entrar")):         k.append((f"{b} login",int(base*.11)))
    else:                                                k.append((f"{b} cadastro",int(base*.10)))
    return k
verified = {"betano.cassino.br.com","1xbet1.com.br","1xbetonline.com.br","1xbet.br.com","mostbetbrasil.com",
 "galera.cassino.br.com","btano.net","mostbet.br.com","mostbet.net.br","mostbet-registration.com.br",
 "mostbett-bet.com","en.mostbetbr.net","mostbetpt.pro","mostbet-online.com.br","mostbet-br-login.com",
 "galera-bet-entrar.com","blazeaposta.org","brazino777.com.br","sportingbetcasino.com.br","estrelabetoficial.com.br"}
discovered=[("Betano","https://btano.net/"),("Mostbet","https://mostbet.br.com/"),("Mostbet","https://mostbet.net.br/"),
 ("Mostbet","https://mostbet-registration.com.br/"),("Mostbet","https://mostbett-bet.com/"),("Mostbet","https://en.mostbetbr.net/"),
 ("Mostbet","https://mostbetpt.pro/"),("Mostbet","https://mostbet-online.com.br/"),("Mostbet","https://mostbet-br-login.com/"),
 ("Galera.bet","https://galera-bet-entrar.com/")]

pairs=[]
with open("casino_brand_registry.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["risco_status"]=="official": continue
        pairs.append((r["marca"],r["url"]))
pairs+=discovered
seen=set(); pairs=[p for p in pairs if p[1] not in seen and not seen.add(p[1])]

paras=[]; mirrors=[]
for brand,url in pairs:
    cl,reason=classify(brand,url); dom=host(url)
    if cl=="espelho":
        mirrors.append([brand,dom,url,reason]); continue
    kw=three_kw(brand,dom)
    paras.append([brand,"; ".join(k for k,_ in kw),"; ".join(f"{v:,}" for _,v in kw),url,
                  "✅ top-10 verificado (jun/2026)" if dom in verified else "SERP-sourced",reason])

paras.sort(key=lambda x:(x[0].lower(),x[3])); mirrors.sort(key=lambda x:(x[0].lower(),x[1]))
with open("parasite_satellites_keywords.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","keywords","search volume","sat url","ranks_top10","parasite_signal"]); w.writerows(paras)
with open("removed_mirrors.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand name","domain","url","mirror_reason"]); w.writerows(mirrors)

print("PARASITAS:",len(paras)," | ESPELHOS removidos:",len(mirrors))
print("Espelhos:")
for m in mirrors: print("  -",m[0],m[1])
