#!/usr/bin/env python3
"""CO related-terms: acha marcas/parasitas que faltavam no matching-terms."""
import csv, re, collections
F="/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/ab8f7c6d-google_co_casino_relatedterms_serps_20260613_213439.csv"
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
    if len(p)>=2 and ".".join(p[-2:]) in SUF2: reg=p[:-2]
    else: reg=p[:-1]
    return (reg[-1] if reg else h)
STOP={"casino","casinos","online","en","vivo","gratis","bono","bonos","registro","login","entrar",
"ingresar","app","descargar","co","com","colombia","apuestas","apuesta","deportivas","juegos","juego",
"slots","tragamonedas","ruleta","opiniones","retiro","deposito","promociones","codigo","oficial",
"sitio","web","es","de","la","el","mi","cuenta","y","real","dinero","casa","mejor","mejores"}
GENERIC={"play","casino","online","juego","apuesta","apuestas","bono","ruleta","slots","tragamonedas","virtual","movil","gana","ganar"}
OFFICIAL={"rushbet","codere","betsson","betplay","wplay","yajuego","luckia","bwin","sportium","bet365",
"stake","bplay","fullreto","zamba","betano","rivalo","megapuesta","1win","mostbet","bbrbet","colbet",
"pinup","betway","wplto","aladdin","spin"}
JUNK={"alimentosdel","bitcoin","monopoly","montecarlo","aladdin","wonderland","guru"}
def brand_of(kw):
    toks=[t for t in re.split(r"[^a-z0-9]+",kw.lower()) if t and t not in STOP]
    b="".join(toks)
    return None if len(b)<4 or b in GENERIC else b

# marcas/dominios ja conhecidos
known_brands=set(); known_doms=set()
for r in csv.DictReader(open("co_parasite_domains_unique.csv",encoding="utf-8")):
    known_doms.add(r["parasite_domain"])
    for b in r["brand(s)"].split(";"): known_brands.add(b)
known_brands|=OFFICIAL

raw=open(F,encoding="utf-16").read()
kw_vol={}; kw_res=collections.defaultdict(list)
for ln in raw.splitlines()[1:]:
    p=[c.strip().strip('"').strip() for c in ln.split("\t")]
    if len(p)<17: continue
    kw=p[0].lower().strip()
    if not kw: continue
    kw_vol[kw]=int(num(p[4]))
    if p[16]=="Organic": kw_res[kw].append((host(p[1]),int(num(p[12]))))

# brands com volume (de keywords)
brand_vol=collections.defaultdict(int)
for kw,v in kw_vol.items():
    b=brand_of(kw)
    if b and b not in JUNK and b not in GENERIC: brand_vol[b]+=v

# parasitas no related
para=collections.defaultdict(lambda:[set(),0])
for kw,res in kw_res.items():
    b=brand_of(kw)
    if not b or b in JUNK: continue
    for dom,tr in res:
        if dom in PLAT or dom in MEDIA: continue
        hn=re.sub(r"[^a-z0-9]","",dom)
        if b not in hn: continue
        lab=label_suf(dom)
        if lab==b or lab in OFFICIAL: continue
        para[dom][0].add(b); para[dom][1]+=tr

new_brands=sorted([(b,v) for b,v in brand_vol.items() if b not in known_brands],key=lambda x:-x[1])
new_doms=sorted([(d,";".join(sorted(v[0])),v[1]) for d,v in para.items() if d not in known_doms],key=lambda x:-x[2])

with open("co_missing_brands.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["new_brand","total_volume_keywords"]); w.writerows(new_brands)
with open("co_new_parasite_domains.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["new_parasite_domain","brand(s)","traffic"]); w.writerows(new_doms)

print(f"related keywords: {len(kw_vol)} | brands detectadas: {len(brand_vol)} | ja conhecidas: {len(known_brands)}")
print(f"\n== MARCAS QUE FALTAVAM (nao estavam antes): {len(new_brands)} ==")
for b,v in new_brands[:40]: print(f"  {b:20} vol={v:>8}")
print(f"\n== NOVOS dominios parasitas: {len(new_doms)} ==")
for d,b,tr in new_doms[:30]: print(f"  {tr:>7} {d:38} [{b}]")
