#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ranking de marcas CO: facilidade de lancar sateite com sucesso.
Criterios: (1) volume de keywords da marca, (2) baixa saturacao de parasitas no SERP,
(3) oficial NAO esta em #1, (4) marca popular na CO."""
import csv, re, collections, math
FILES=["/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/4918f61f-google_co_casino_matchingterms_serps_20260613_212707.csv",
       "/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/ab8f7c6d-google_co_casino_relatedterms_serps_20260613_213439.csv"]
def num(s):
    s=str(s).strip().replace(",","")
    try:return float(s)
    except:return 0.0
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h
PLAT={"google.com","play.google.com","apps.apple.com","youtube.com","m.youtube.com","facebook.com",
"instagram.com","x.com","twitter.com","tiktok.com","reddit.com","linkedin.com","wikipedia.org","casino.guru","es.casino.guru"}
MEDIA={"eltiempo.com","semana.com","marca.com","as.com","futbolred.com","antena2.com","bolavip.com",
"depor.com","goal.com","oddspedia.com","casino.org","legalbet.co","elespectador.com","pulzo.com","infobae.com",
"futbolred.com","futbolete.com","elcolombiano.com","wradio.com.co","rcnradio.com"}
SUF2={"com.co","net.co","org.co","gov.co","edu.co","co.uk","bet.ar","com.ar","co.za","co.tz","it.com","eu.com"}
def label(h):
    p=h.split(".")
    reg=p[:-2] if (len(p)>=2 and ".".join(p[-2:]) in SUF2) else p[:-1]
    return reg[-1] if reg else h
STOP={"casino","casinos","online","en","vivo","gratis","bono","bonos","registro","login","entrar",
"ingresar","app","descargar","co","com","colombia","apuestas","apuesta","deportivas","juegos","juego",
"slots","tragamonedas","ruleta","opiniones","retiro","deposito","promociones","codigo","oficial","sitio",
"web","es","de","la","el","mi","cuenta","y","real","dinero","casa","mejor","mejores","iniciar","sesion",
"sesión","ingreso","inicio","registrarse","futbol","ftbol","logo","poker","como","retirar","jugar"}
GENERIC={"play","casino","online","juego","apuesta","apuestas","bono","ruleta","slots","virtual","gana","ganar"}
OFFICIAL={"rushbet","codere","betsson","betplay","wplay","yajuego","luckia","bwin","sportium","bet365",
"stake","bplay","fullreto","zamba","betano","rivalo","megapuesta","1win","mostbet","bbrbet","colbet",
"pinup","betway","vaycasino","betjuego"}
CANON=[("rusbet","Rushbet"),("rusbeth","Rushbet"),("rushet","Rushbet"),("rushbet","Rushbet"),
("betson","Betsson"),("besson","Betsson"),("betsso","Betsson"),("bettsson","Betsson"),("betsson","Betsson"),
("wolay","Wplay"),("wplau","Wplay"),("wply","Wplay"),("wplay","Wplay"),("betplay","BetPlay"),("bplay","BetPlay"),
("1win","1win"),("mostbet","Mostbet"),("bbrbet","BBRBet"),("rivalo","Rivalo"),("codere","Codere"),
("colbet","Colbet"),("pinup","Pin-Up"),("betway","Betway"),("sportium","Sportium"),("yajuego","YaJuego"),
("luckia","Luckia"),("bwin","Bwin"),("bet365","Bet365"),("megapuesta","Megapuesta"),("zamba","Zamba"),
("fullreto","Fullreto"),("stake","Stake"),("betano","Betano"),("melbet","Melbet"),("20bet","20bet"),
("vaycasino","VayCasino"),("betjuego","BetJuego")]
JUNK={"alimentosdel","bitcoin","monopoly","montecarlo","aladdin","wonderland","guru","sugarrush","spin",
"nine","bizzo","verde","vulkanvegas","crash","mrbet","starburst","hollywood","rush","bonanza"}  # global, nao-CO
def brand_of(kw):
    toks=[t for t in re.split(r"[^a-z0-9]+",kw.lower()) if t and t not in STOP]
    b="".join(toks)
    return None if len(b)<4 or b in GENERIC else b
def canon(b):
    for frag,name in CANON:
        if frag in b: return name
    return None  # desconhecido -> ignora p/ ranking de marcas CO

# parse
kwvol={}; kwrows=collections.defaultdict(list)  # keyword -> [(domain,pos,type)]
for path in FILES:
    for ln in open(path,encoding="utf-16").read().splitlines()[1:]:
        p=[c.strip().strip('"').strip() for c in ln.split("\t")]
        if len(p)<17: continue
        kw=p[0].lower().strip()
        if not kw: continue
        kwvol[kw]=max(kwvol.get(kw,0),int(num(p[4])))
        try: pos=int(num(p[15]))
        except: pos=999
        kwrows[kw].append((host(p[1]),pos,p[16]))

def dom_class(dom,brand_token):
    if dom in PLAT or any(dom.endswith("."+x) for x in PLAT): return "platform"
    if dom in MEDIA or any(dom.endswith("."+x) for x in MEDIA): return "media"
    hn=re.sub(r"[^a-z0-9]","",dom); lab=label(dom)
    if brand_token in hn:
        return "official" if (lab==brand_token or lab in OFFICIAL) else "parasite"
    return "other"

B=collections.defaultdict(lambda:{"vol":{}, "paras":{}, "headkw":("",0), "top1":collections.Counter(), "top1ex":{}})
for kw,vol in kwvol.items():
    bt=brand_of(kw); br=canon(bt) if bt else None
    if not br or bt in JUNK: continue
    d=B[br]; d["vol"][kw]=vol
    if vol>d["headkw"][1]: d["headkw"]=(kw,vol)
    # parasitas + posicoes
    for dom,pos,typ in kwrows[kw]:
        if typ!="Organic": continue
        c=dom_class(dom,bt)
        if c=="parasite":
            if dom not in d["paras"] or pos<d["paras"][dom]: d["paras"][dom]=pos
    # quem esta no #1 organico
    ones=[dom for dom,pos,typ in kwrows[kw] if pos==1 and typ=="Organic"]
    if ones: d["top1ex"][kw]=dom_class(ones[0],bt)

rows=[]
for br,d in B.items():
    tvol=sum(d["vol"].values()); nkw=len(d["vol"]); npar=len(d["paras"])
    best_par=min(d["paras"].values()) if d["paras"] else 99
    hk=d["headkw"][0]; top1=d["top1ex"].get(hk,"?")
    off_top1 = "yes" if top1=="official" else "no"
    # ease score (criterios do usuario: off NAO #1 + baixa saturacao + volume + CO)
    s=0
    s+= 3 if tvol>=20000 else 2 if tvol>=5000 else 1 if tvol>=1000 else 0
    s+= 3 if npar<=2 else 2 if npar<=4 else 1 if npar<=6 else 0     # saturacao
    s+= 4 if off_top1=="no" else 0                                  # oficial NAO #1 (peso alto)
    s+= 2 if best_par>3 else 0                                      # nenhum parasita travou top-3
    # verdict
    if off_top1=="no" and npar<=2 and tvol>=1000: v="OTIMO (off nao #1 + livre + volume)"
    elif off_top1=="no" and npar<=4: v="BOM (off nao #1, pouca saturacao)"
    elif npar<=2 and tvol>=20000: v="ALTO VOLUME (off #1, mas SERP pouco saturado)"
    elif npar>=6: v="SATURADO (evitar)"
    else: v="medio"
    rows.append([br,tvol,nkw,npar,(best_par if best_par<99 else ""),top1,off_top1,s,v])
rows.sort(key=lambda x:(-x[7],-x[1]))
with open("co_brand_opportunity.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","total_volume","n_keywords","parasite_domains_in_serp",
        "best_parasite_position","top1_organic_type","official_is_top1","ease_score","verdict"]); w.writerows(rows)
print(f"{'Brand':12}{'vol':>8}{'paras':>6}{'offTop1':>8}{'EASE':>5}  verdict")
for br,tv,nk,np,bp,t1,ot,s,v in rows:
    print(f"  {br:12}{tv:>8}{np:>6}{ot:>8}{s:>5}  {v}")
