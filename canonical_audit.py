#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoria de canonical / hreflang(alternate) + podklejki cross-domain.

Para cada dominio da lista:
  - baixa a pagina (via cloudscraper -> contorna Cloudflare),
  - extrai rel=canonical e todos rel=alternate (hreflang),
  - detecta redirect offsite (301/302 -> outro dominio = podklejka),
  - SE o canonical e/ou algum alternate aponta para um DOMINIO DIFERENTE,
    visita esse dominio e extrai TAMBEM o canonical e os alternates dele.

Entrada: co_satellites_master.csv (coluna 'satellite_url')  OU  domains.txt (1 por linha).
Saidas : canonical_audit_main.csv  +  canonical_audit_crossdomain.csv

== COMO RODAR (cloudscraper) ==
  pip install cloudscraper beautifulsoup4
  python canonical_audit.py
(rode com IP RESIDENCIAL, nao datacenter/VPN)
"""
import csv, os, sys, collections, concurrent.futures as cf
from urllib.parse import urlparse, urljoin

try:
    import cloudscraper
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Instale: pip install cloudscraper beautifulsoup4")

scraper = cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','mobile':False})
HEADERS = {"Accept-Language": "es-CO,es;q=0.9,en;q=0.6"}
TIMEOUT = 25

# --- dominio registravel (eTLD+1) p/ comparar "mesmo site" ---
SUF2 = {"com.co","net.co","org.co","gov.co","edu.co","co.uk","com.br","net.br","com.ar","bet.ar",
        "co.za","co.tz","com.mx","com.pe","com.ve","co.cr","eu.com","it.com","us.com","uk.com"}
def host_of(u):
    h = urlparse(u if "://" in u else "http://"+u).netloc.lower()
    return h[4:] if h.startswith("www.") else h
def regdomain(host):
    host = host.split(":")[0]
    p = host.split(".")
    if len(p) >= 3 and ".".join(p[-2:]) in SUF2: return ".".join(p[-3:])
    return ".".join(p[-2:]) if len(p) >= 2 else host

def fetch(url):
    """retorna (status, final_url, soup|None)"""
    try:
        r = scraper.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        ct = r.headers.get("Content-Type","")
        soup = BeautifulSoup(r.text, "html.parser") if "html" in ct or r.text[:100].lower().count("<html") else BeautifulSoup(r.text,"html.parser")
        return r.status_code, r.url, soup
    except Exception as e:
        return "ERR", type(e).__name__, None

def extract(soup, base_url):
    """canonical (abs), lista de alternates [(hreflang,href_abs)]"""
    if soup is None: return "", []
    can = soup.find("link", rel=lambda x: x and "canonical" in [v.lower() for v in (x if isinstance(x,list) else [x])])
    can_href = urljoin(base_url, can.get("href")) if can and can.get("href") else ""
    alts = []
    for l in soup.find_all("link", rel=lambda x: x and "alternate" in [v.lower() for v in (x if isinstance(x,list) else [x])]):
        hl = l.get("hreflang"); href = l.get("href")
        if hl and href: alts.append((hl, urljoin(base_url, href)))
    return can_href, alts

def load_domains():
    if os.path.exists("co_satellites_master.csv"):
        s=set()
        for r in csv.DictReader(open("co_satellites_master.csv", encoding="utf-8")):
            if r.get("satellite_url"): s.add(r["satellite_url"].strip())
        if s: return sorted(s)
    if os.path.exists("domains.txt"):
        return sorted({l.strip() for l in open("domains.txt") if l.strip()})
    sys.exit("Coloque co_satellites_master.csv ou domains.txt na pasta.")

domains = load_domains()
print(f"Dominios a auditar: {len(domains)}")

cross_cache = {}   # regdomain -> (status, canonical, alternates_str)
def audit_cross(host):
    rd = regdomain(host)
    if rd in cross_cache: return cross_cache[rd]
    st, final, soup = fetch("https://"+host)
    can, alts = extract(soup, "https://"+host)
    res = (st, can, " | ".join(f"{h}:{u}" for h,u in alts))
    cross_cache[rd] = res
    return res

main_rows=[]; cross_rows=[]; dom_brand=collections.defaultdict(set)
if os.path.exists("co_satellites_master.csv"):
    for r in csv.DictReader(open("co_satellites_master.csv",encoding="utf-8")):
        dom_brand[r.get("satellite_url","").strip()].add(r.get("Brand",""))

def process(d):
    src_rd = regdomain(d)
    st, final, soup = fetch("https://"+d)
    final_host = host_of(final) if isinstance(final,str) and "." in final else ""
    offsite_redirect = "yes" if final_host and regdomain(final_host)!=src_rd else "no"
    can, alts = extract(soup, "https://"+d)
    can_rd = regdomain(host_of(can)) if can else ""
    can_offsite = "yes" if can_rd and can_rd!=src_rd else "no"
    alt_str = " | ".join(f"{h}:{u}" for h,u in alts)
    # dominios externos referenciados (canonical / alternate / redirect)
    ext=set()
    if can_offsite=="yes": ext.add(host_of(can))
    for h,u in alts:
        if regdomain(host_of(u))!=src_rd: ext.add(host_of(u))
    if offsite_redirect=="yes": ext.add(final_host)
    return d, st, final if isinstance(final,str) else "", offsite_redirect, can, can_offsite, alt_str, sorted({regdomain(e) for e in ext}), sorted(ext)

with cf.ThreadPoolExecutor(max_workers=8) as ex:
    results=list(ex.map(process, domains))

for d, st, final, offr, can, can_off, alt_str, ext_rd, ext_hosts in results:
    brand=";".join(sorted(dom_brand.get(d,[]))) if dom_brand else ""
    main_rows.append([brand, d, st, final, offr, can, can_off, alt_str, "; ".join(ext_rd)])
    for eh in ext_hosts:                      # puxa canonical/alternate do dominio colado
        cst, ccan, calt = audit_cross(eh)
        cross_rows.append([brand, d, eh, cst, ccan, calt])
    print(d, st, "offsite_redirect="+offr, "canonical_offsite="+can_off, "ext="+(";".join(ext_rd) or "-"))

with open("canonical_audit_main.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","domain","http_status","final_url","offsite_redirect(podklejka)",
        "canonical","canonical_offsite","hreflang_alternates","cross_domains"]); w.writerows(main_rows)
with open("canonical_audit_crossdomain.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","source_domain","cross_domain","cross_http_status",
        "cross_canonical","cross_hreflang_alternates"]); w.writerows(cross_rows)

print(f"\nOK -> canonical_audit_main.csv ({len(main_rows)})  +  canonical_audit_crossdomain.csv ({len(cross_rows)})")
