#!/usr/bin/env python3
"""Une matching + related (CO casino) numa tabela: brand, satellite url, keyword, volume, traffic."""
import csv, re, collections
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
"depor.com","goal.com","oddspedia.com","casino.org","legalbet.co","elespectador.com","pulzo.com","infobae.com"}
SUF2={"com.co","net.co","org.co","gov.co","edu.co","co.uk","bet.ar","com.ar","co.za","co.tz","it.com"}
def label_suf(h):
    p=h.split(".")
    reg=p[:-2] if (len(p)>=2 and ".".join(p[-2:]) in SUF2) else p[:-1]
    return reg[-1] if reg else h
STOP={"casino","casinos","online","en","vivo","gratis","bono","bonos","registro","login","entrar",
"ingresar","app","descargar","co","com","colombia","apuestas","apuesta","deportivas","juegos","juego",
"slots","tragamonedas","ruleta","opiniones","retiro","deposito","promociones","codigo","oficial",
"sitio","web","es","de","la","el","mi","cuenta","y","real","dinero","casa","mejor","mejores",
"iniciar","sesion","sesión","ingreso","inicio","registrarse","futbol","ftbol","logo","poker"}
GENERIC={"play","casino","online","juego","apuesta","apuestas","bono","ruleta","slots","tragamonedas","virtual","movil","gana","ganar"}
OFFICIAL={"rushbet","codere","betsson","betplay","wplay","yajuego","luckia","bwin","sportium","bet365",
"stake","bplay","fullreto","zamba","betano","rivalo","megapuesta","1win","mostbet","bbrbet","colbet",
"pinup","betway","vaycasino","betjuego"}
JUNK={"alimentosdel","bitcoin","monopoly","montecarlo","aladdin","wonderland","guru","sugarrush","spin"}
# normaliza variacoes ortograficas -> marca canonica
CANON=[("rusbet","Rushbet"),("rusbeth","Rushbet"),("rushet","Rushbet"),("rusbel","Rushbet"),("rushbet","Rushbet"),
("betson","Betsson"),("besson","Betsson"),("betsoon","Betsson"),("betsom","Betsson"),("beetson","Betsson"),
("bettsson","Betsson"),("betason","Betsson"),("betsso","Betsson"),("betss","Betsson"),("betsson","Betsson"),
("wolay","Wplay"),("wplau","Wplay"),("wply","Wplay"),("wplay","Wplay"),("betplay","BetPlay"),("bplay","BetPlay"),
("1win","1win"),("mostbet","Mostbet"),("bbrbet","BBRBet"),("rivalo","Rivalo"),("codere","Codere"),
("colbet","Colbet"),("pinup","Pin-Up"),("betway","Betway"),("sportium","Sportium"),("yajuego","YaJuego"),
("luckia","Luckia"),("bwin","Bwin"),("bet365","Bet365"),("megapuesta","Megapuesta"),("vaycasino","VayCasino"),
("betjuego","BetJuego"),("zamba","Zamba"),("fullreto","Fullreto"),("stake","Stake"),("betano","Betano")]
def brand_of(kw):
    toks=[t for t in re.split(r"[^a-z0-9]+",kw.lower()) if t and t not in STOP]
    b="".join(toks)
    return None if len(b)<4 or b in GENERIC else b
def canon(b):
    for frag,name in CANON:
        if frag in b: return name
    return b  # desconhecido -> token cru

rows={}  # (brand,domain,keyword) -> (vol,kd,traffic)
for path in FILES:
    raw=open(path,encoding="utf-16").read()
    for ln in raw.splitlines()[1:]:
        p=[c.strip().strip('"').strip() for c in ln.split("\t")]
        if len(p)<17 or p[16]!="Organic": continue
        kw=p[0].lower().strip();
        b=brand_of(kw)
        if not b or b in JUNK: continue
        dom=host(p[1])
        if dom in PLAT or dom in MEDIA: continue  # so plataformas/midia; mantem tudo que ranqueia em CO
        if dom.endswith((".softonic.com",".uptodown.com",".aptoide.com")) or any(x in dom for x in ("softonic.","uptodown.","aptoide.")): continue  # app-dirs fora
        hn=re.sub(r"[^a-z0-9]","",dom)
        if b not in hn: continue
        lab=label_suf(dom)
        if lab==b or lab in OFFICIAL: continue   # dominio do operador
        brand=canon(b); vol=int(num(p[4])); kd=int(num(p[3])); tr=int(num(p[12]))
        key=(brand,dom,kw)
        if key not in rows or vol>rows[key][0]: rows[key]=(vol,kd,tr)

out=sorted(([b,d,k,v[0],v[1],v[2]] for (b,d,k),v in rows.items()),key=lambda x:(x[0].lower(),-x[3],x[1]))
with open("co_satellites_master.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","satellite_url","keyword","search_volume","KD","traffic"]); w.writerows(out)

dom_b=collections.defaultdict(set);
for b,d,k,v,kd,tr in out: dom_b[b].add(d)
print(f"Linhas (brand x domain x keyword): {len(out)} | marcas: {len(dom_b)} | dominios unicos: {len({r[1] for r in out})}")
print("\n== dominios sateites por marca ==")
for b in sorted(dom_b,key=lambda x:-len(dom_b[x])):
    print(f"  {b:14} {len(dom_b[b])} dominios: {', '.join(sorted(dom_b[b])[:6])}{' ...' if len(dom_b[b])>6 else ''}")
