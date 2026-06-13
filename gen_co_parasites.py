#!/usr/bin/env python3
"""CO 'casino' branded matching-terms: dedup keywords, coleta sateites parasitas."""
import csv, re, collections
F="/root/.claude/uploads/d028c233-fc6a-5e5a-9723-bd8bfecfe58d/4918f61f-google_co_casino_matchingterms_serps_20260613_212707.csv"
def num(s):
    s=str(s).strip().replace(",","")
    try:return float(s)
    except:return 0.0
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h

PLAT={"google.com","play.google.com","apps.apple.com","youtube.com","m.youtube.com","facebook.com",
"instagram.com","x.com","twitter.com","tiktok.com","reddit.com","linkedin.com","wikipedia.org",
"pinterest.com","t.me","telegram.org","whatsapp.com","apple.com","microsoft.com","github.com"}
MEDIA={"eltiempo.com","semana.com","marca.com","as.com","futbolred.com","antena2.com","bolavip.com",
"depor.com","redgol.cl","goal.com","oddspedia.com","casino.org","legalbet.co","futbolete.com",
"elespectador.com","pulzo.com","minuto30.com","caracoltv.com","rcnradio.com","infobae.com",
"telecomasia.net","ghanasoccernet.com","apuestalegal.pe","casino.online","sportytrader.com"}

SUF2={"com.co","net.co","org.co","gov.co","edu.co","co.uk","com.br","net.br","bet.ar","com.ar"}
def label_suf(h):
    p=h.split(".")
    if len(p)>=2 and ".".join(p[-2:]) in SUF2: reg=p[:-2]; suf=".".join(p[-2:])
    else: reg=p[:-1]; suf=p[-1] if p else ""
    return (reg[-1] if reg else h), suf
STOP={"casino","casinos","online","en","vivo","gratis","bono","bonos","registro","registrarse",
"login","ingresar","entrar","iniciar","sesion","sesión","app","aplicacion","descargar","co","com",
"colombia","apuestas","apuesta","deportivas","juegos","juego","slots","tragamonedas","ruleta",
"opiniones","retiro","retiros","deposito","promociones","codigo","promocional","oficial","sitio",
"web","es","de","la","el","mi","cuenta","y","real","dinero","casa","mejor","mejores"}
GENERIC={"play","casino","online","juego","apuesta","apuestas","bono","mejor","mejores","ruleta","slots"}
OFFICIAL={"rushbet","codere","betsson","betplay","wplay","yajuego","luckia","bwin","sportium",
"bet365","stake","bplay","fullreto","zamba","betano","rivalo","megapuesta"}
JUNK={"alimentosdel","bitcoin","monopoly","montecarlo","aladdin","wonderland"}
def brand_of(kw):
    toks=[t for t in re.split(r"[^a-z0-9]+",kw.lower()) if t and t not in STOP]
    b="".join(toks)
    if len(b)<4 or b in GENERIC: return None
    return b

# parse: keyword -> {vol,kd, results:[(domain,pos,traffic)]}
data=collections.OrderedDict()
raw=open(F,encoding="utf-16").read()
for ln in raw.splitlines()[1:]:
    p=[c.strip().strip('"').strip() for c in ln.split("\t")]
    if len(p)<17: continue
    kw=p[0].lower().strip()
    if not kw: continue
    if kw not in data: data[kw]={"vol":int(num(p[4])),"kd":int(num(p[3])),"res":[]}
    if p[16]=="Organic":
        data[kw]["res"].append((host(p[1]),p[15],int(num(p[12]))))

by_kw=[]; dom_agg=collections.defaultdict(lambda:[set(),0,set()])  # dom -> (keywords,traffic,brands)
for kw,d in data.items():
    brand=brand_of(kw)
    seen=set()
    for dom,pos,tr in d["res"]:
        if dom in seen: continue
        seen.add(dom)
        if dom in PLAT or dom in MEDIA or any(dom.endswith("."+m) for m in PLAT|MEDIA): continue
        if not brand: continue
        hn=re.sub(r"[^a-z0-9]","",dom)
        if brand not in hn: continue  # nao contem a marca -> nao e sateite da marca
        lab,suf=label_suf(dom)
        if lab==brand: continue  # nome registravel == marca -> dominio do operador (qualquer TLD)
        if lab in OFFICIAL: continue          # operador conhecido (qualquer TLD)
        if brand in JUNK: continue            # falso-positivo (nao e marca de cassino)
        if dom.endswith((".uptodown.com",".softonic.com",".com.br")): continue  # app-dirs/outros
        by_kw.append([kw,d["vol"],d["kd"],brand,dom,pos,tr])
        dom_agg[dom][0].add(kw); dom_agg[dom][1]+=tr; dom_agg[dom][2].add(brand)

by_kw.sort(key=lambda x:(-x[1],x[0],x[5]))
with open("co_parasites_by_keyword.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["keyword","volume","KD","brand","parasite_domain","position","traffic"]); w.writerows(by_kw)
uniq=sorted(([d,len(v[0]),v[1],";".join(sorted(v[2]))] for d,v in dom_agg.items()),key=lambda x:-x[2])
with open("co_parasite_domains_unique.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["parasite_domain","n_keywords","total_traffic","brand(s)"]); w.writerows(uniq)

print(f"Unique keywords: {len(data)} | parasite rows: {len(by_kw)} | unique parasite domains: {len(uniq)}")
print("\n== TOP parasite domains (por traffic) ==")
for d,nk,tr,br in uniq[:30]: print(f"  {tr:>7}  kw={nk:<2} {d:38} [{br}]")
