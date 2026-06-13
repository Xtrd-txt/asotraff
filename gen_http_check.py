#!/usr/bin/env python3
"""Checa HTTP status dos sateites (co_satellites_master.csv).
RODAR EM IP RESIDENCIAL/BROWSER: de datacenter o Cloudflare devolve 403 (falso negativo).
Para 200 real use Playwright ou proxy residencial."""
import csv,collections,concurrent.futures as cf,urllib.request,urllib.error,ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
rows=list(csv.DictReader(open("co_satellites_master.csv",encoding="utf-8")))
dom_brand=collections.defaultdict(set)
for r in rows: dom_brand[r["satellite_url"]].add(r["Brand"])
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
def check(d):
    try:
        req=urllib.request.Request("https://"+d,headers={"User-Agent":UA,"Accept-Language":"es-CO,es"})
        r=urllib.request.build_opener(NoRedirect).open(req,timeout=10)
        return d,r.status,r.geturl()
    except urllib.error.HTTPError as e:
        return d,e.code,e.headers.get("Location","") if 300<=e.code<400 else ""
    except Exception as e:
        return d,"ERR",type(e).__name__
res={}
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for d,st,info in ex.map(check,sorted(dom_brand)): res[d]=(st,info)
out=[[";".join(sorted(dom_brand[d])),d,res[d][0],res[d][1]] for d in sorted(dom_brand)]
out.sort(key=lambda x:(str(x[2])!="200",x[0].lower()))
with open("co_satellites_httpcheck.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Brand","satellite_url","http_status","final_url/redirect_or_error"]); w.writerows(out)
print(collections.Counter(str(x[2]) for x in out))
