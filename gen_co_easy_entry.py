#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CO 1win/20bet/bbrbet/stake...: acha keywords onde oficial NAO esta em #1
(da p/ entrar), marca quem segura o #1 (parasita = perfivel), filtra datas,
e da intent em RU p/ keywords em espanhol."""
import csv, re, collections, sys
DEFAULT=["/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/2c033bbd-google_co_1win20betbbr_matchingterms_serps_20260613_225843.csv",
       "/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/e0559009-google_co_1win20betbbrb_relatedterms_serps_20260613_225836.csv"]
OUT = sys.argv[1] if len(sys.argv)>1 else "co_easy_entry_keywords.csv"
FILES = sys.argv[2:] if len(sys.argv)>2 else DEFAULT
def num(s):
    s=str(s).strip().replace(",","")
    try:return float(s)
    except:return 0.0
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h
PLAT={"google.com","play.google.com","apps.apple.com","youtube.com","m.youtube.com","facebook.com",
"instagram.com","x.com","twitter.com","tiktok.com","reddit.com","linkedin.com","wikipedia.org","casino.guru","es.casino.guru","aptoide.com"}
MEDIA={"eltiempo.com","semana.com","marca.com","as.com","futbolred.com","antena2.com","bolavip.com",
"depor.com","goal.com","oddspedia.com","casino.org","legalbet.co","elespectador.com","pulzo.com","infobae.com",
"futbolete.com","elcolombiano.com","wradio.com.co","rcnradio.com","ligadeapuestas.com","softonic.com","uptodown.com"}
SUF2={"com.co","net.co","org.co","co.uk","bet.ar","com.ar","co.za","it.com","eu.com","com.mx","com.pe"}
def label(h):
    p=h.split(".")
    reg=p[:-2] if (len(p)>=2 and ".".join(p[-2:]) in SUF2) else p[:-1]
    return reg[-1] if reg else h
STOP={"casino","casinos","online","en","vivo","gratis","bono","bonos","registro","login","entrar","ingresar",
"app","descargar","co","com","colombia","apuestas","apuesta","deportivas","juegos","juego","slots","tragamonedas",
"ruleta","opiniones","retiro","deposito","promociones","codigo","oficial","sitio","web","es","de","la","el","mi",
"cuenta","y","real","dinero","casa","mejor","mejores","iniciar","sesion","sesión","ingreso","inicio","registrarse",
"como","retirar","jugar","sacar","recargar","aviator","plinko","crash","movil","celular","aplicacion","apk"}
GENERIC={"play","casino","online","juego","apuesta","apuestas","bono","ruleta","slots","virtual","gana","ganar"}
OFFICIAL={"rushbet","codere","betsson","betplay","wplay","yajuego","luckia","bwin","sportium","bet365","stake",
"bplay","fullreto","zamba","betano","rivalo","megapuesta","1win","mostbet","bbrbet","colbet","pinup","betway","20bet",
"roobet","megapari","verde","verdecasino","nine","ninecasino","bizzo","bizzocasino","wazamba","mrbet","ggbet",
"rabona","ivibet","boomerang","sportaza","leon","leonbet","spinbetter","cbet","betfury","vulkanvegas","melbet","betwinner","1xbet","22bet"}
CANON=[("rusbet","Rushbet"),("rushet","Rushbet"),("rushbet","Rushbet"),("betson","Betsson"),("betsso","Betsson"),
("betsson","Betsson"),("wolay","Wplay"),("wply","Wplay"),("wplay","Wplay"),("betplay","BetPlay"),("bplay","BetPlay"),
("1win","1win"),("20bet","20bet"),("mostbet","Mostbet"),("bbrbet","BBRBet"),("rivalo","Rivalo"),("codere","Codere"),
("colbet","Colbet"),("pinup","Pin-Up"),("betway","Betway"),("sportium","Sportium"),("yajuego","YaJuego"),
("luckia","Luckia"),("bwin","Bwin"),("bet365","Bet365"),("megapuesta","Megapuesta"),("zamba","Zamba"),
("fullreto","Fullreto"),("stake","Stake"),("betano","Betano"),("melbet","Melbet"),
("roobet","Roobet"),("megapari","Megapari"),("verde","Verde"),("ninecasino","Nine"),("nine","Nine"),
("bizzo","Bizzo"),("wazamba","Wazamba"),("mrbet","Mr.Bet"),("ggbet","GGbet"),("rabona","Rabona"),
("ivibet","Ivibet"),("boomerang","Boomerang"),("sportaza","Sportaza"),("leon","Leon"),("spinbetter","Spinbetter"),
("cbet","Cbet"),("betfury","Betfury"),("vulkanvegas","VulkanVegas"),("betwinner","Betwinner"),("22bet","22Bet"),("1xbet","1xBet")]
def brand_of(kw):
    toks=[t for t in re.split(r"[^a-z0-9]+",kw.lower()) if t and t not in STOP]
    b="".join(toks); return None if len(b)<4 or b in GENERIC else b
def canon(b):
    for frag,name in CANON:
        if frag in b: return name
    return None
ROOTS={"Rushbet":["rushbet"],"Betsson":["betsson"],"Bwin":["bwin"],"BetPlay":["betplay","bplay"],
"1win":["1win"],"20bet":["20bet"],"Mostbet":["mostbet"],"BBRBet":["bbrbet"],"Stake":["stake"],
"Pin-Up":["pinup"],"Wplay":["wplay"],"Codere":["codere"],"Rivalo":["rivalo"],"Colbet":["colbet"],
"Zamba":["zamba"],"YaJuego":["yajuego"],"Melbet":["melbet"],"Luckia":["luckia"],"Sportium":["sportium"],
"Megapuesta":["megapuesta"],"Fullreto":["fullreto"],"Betway":["betway"],"Bet365":["bet365"],"Betano":["betano"],
"Roobet":["roobet"],"Megapari":["megapari"],"Verde":["verde","verdecasino"],"Nine":["nine","ninecasino"],
"Bizzo":["bizzo","bizzocasino"],"Wazamba":["wazamba"],"Mr.Bet":["mrbet"],"GGbet":["ggbet"],"Rabona":["rabona"],
"Ivibet":["ivibet"],"Boomerang":["boomerang"],"Sportaza":["sportaza"],"Leon":["leon","leonbet"],
"Spinbetter":["spinbetter"],"Cbet":["cbet"],"Betfury":["betfury"],"VulkanVegas":["vulkanvegas"],
"Betwinner":["betwinner"],"22Bet":["22bet"],"1xBet":["1xbet"],"Melbet":["melbet"]}
DATE=re.compile(r"\b(19|20)\d{2}\b|\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre|hoy|ayer|ma[nñ]ana|actualizado)\b")
def is_date(kw): return bool(DATE.search(kw.lower()))
INTENT=[(("registr","crear cuenta","abrir cuenta","inscrib","afili","registrate"),"Регистрация / создать аккаунт"),
(("iniciar sesion","iniciar sesión","login","ingres","entrar","acceder","acceso","mi cuenta"),"Вход в аккаунт"),
(("retir","sacar","cobrar","paga","retirada"),"Вывод средств"),
(("deposit","recarg","metodos de pago","método"),"Депозит / пополнение"),
(("bono","bonos","codigo","código","promo","cupon","cupón","sin deposito","giros gratis","freebet","free bet"),"Бонус / промокод"),
(("descarg","app","aplicac","apk","movil","móvil","celular","instalar","android","ios"),"Скачать приложение"),
(("confiable","seguro","legal","opinion","reseñ","resen","review","estafa","funciona","paga de verdad","es bueno","es real"),"Надёжность / отзывы"),
(("aviator","plinko","ruleta","tragamonedas","slot","blackjack","mines","dado","en vivo","crash"),"Игры казино"),
(("apuesta","apostar","deportiv","futbol","fútbol","pronostico"),"Ставки на спорт"),
(("como funciona","como jugar","como apostar","tutorial","guia","guía","como "),"Как пользоваться / гайд")]
def intent_ru(kw,lang):
    k=kw.lower()
    for frags,name in INTENT:
        if any(f in k for f in frags): return name
    if "spanish" in lang.lower(): return "Навигационный (бренд)"
    return ""

kwvol={}; kwkd={}; kwlang={}; kwrows=collections.defaultdict(list)
for path in FILES:
    for ln in open(path,encoding="utf-16").read().splitlines()[1:]:
        p=[c.strip().strip('"').strip() for c in ln.split("\t")]
        if len(p)<17: continue
        kw=p[0].lower().strip()
        if not kw: continue
        kwvol[kw]=max(kwvol.get(kw,0),int(num(p[4]))); kwkd[kw]=int(num(p[3]))
        kwlang[kw]=p[32] if len(p)>32 else ""
        try: pos=int(num(p[15]))
        except: pos=999
        kwrows[kw].append((host(p[1]),pos,p[16]))

def cls(dom,roots):
    if dom in PLAT or any(dom.endswith("."+x) for x in PLAT): return "platform"
    if dom in MEDIA or any(dom.endswith("."+x) for x in MEDIA): return "media"
    hn=re.sub(r"[^a-z0-9]","",dom); lab=label(dom)
    if any(rt.replace("-","") in hn for rt in roots):
        return "official" if (lab in roots or lab in OFFICIAL) else "parasite"
    return "other"

rows=[]
for kw,vol in kwvol.items():
    if is_date(kw): continue
    bt=brand_of(kw); br=canon(bt) if bt else None
    if not br: continue
    roots=ROOTS.get(br,[bt])
    ones=[(d,t) for d,pos,t in kwrows[kw] if pos==1]
    org1=[d for d,t in ones if t=="Organic"]
    if not org1: continue
    top1=org1[0]; ttype=cls(top1,roots)
    if ttype=="official": continue            # oficial #1 -> nao e oportunidade
    beat = top1 if ttype=="parasite" else ""
    rows.append([br,kw,vol,kwkd[kw],top1,ttype,beat,intent_ru(kw,kwlang[kw])])
rows.sort(key=lambda x:(x[0].lower(),-x[2]))
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","keyword","volume","KD","top1_domain","top1_type","beat_parasite","user_intent_ru"]); w.writerows(rows)

byb=collections.defaultdict(lambda:[0,0,0])
for br,kw,v,kd,t1,tt,beat,it in rows:
    byb[br][0]+=1; byb[br][1]+=v
    if tt=="parasite": byb[br][2]+=1
print(f"Oportunidades (oficial NAO #1, sem datas): {len(rows)}\n")
print(f"{'Brand':10}{'kw_opp':>7}{'vol':>9}{'#1=parasita':>13}")
for br,(n,v,pc) in sorted(byb.items(),key=lambda x:-x[1][1]):
    print(f"  {br:10}{n:>6}{v:>9}{pc:>10}")
print("\n== exemplos (top vol) ==")
for r in rows[:25]:
    print(f"  {r[0]:8} v={r[2]:>6} KD={r[3]:>2} #1={r[5]:<9}{r[4][:26]:<27} | {r[7]}  <= {r[1]}")
