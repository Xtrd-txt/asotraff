#!/usr/bin/env python3
"""Tabela final: tabela do usuario + dados Ahrefs reais, filtrada por trafego>=50."""
import csv
def host(u):
    h=u.split("://",1)[-1].split("/",1)[0].lower()
    return h[4:] if h.startswith("www.") else h

# keywords + volume estimado (tabela original)
kw=dict()
with open("parasite_satellites_keywords.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("sat url"): kw[host(r["sat url"])]=(r["keywords"],r["search volume"])

# SERP: top keyword/posicao por dominio
serp=dict()
with open("satellite_keyword_serp.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        d=r["domain"]
        if d not in serp or int(r["traffic_on_kw"])>serp[d][2]:
            serp[d]=(r["keyword"],r["position"],int(r["traffic_on_kw"]))

# Ahrefs (filtrados >=50) = base final
out=[]
with open("filtered_satellites_ahrefs.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        d=r["domain"]; k,v=kw.get(d,("",""))
        sk,sp,_=serp.get(d,("","",0))
        out.append([r["Brand name"],k,v,r["sat url"],
                    int(r["organic_traffic"]),float(r["DR"]),int(r["organic_keywords"]),
                    r["traffic_value_usd"],sk,sp])
out.sort(key=lambda x:-x[4])
with open("Sat_Br_final.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Brand name","keywords","est_search_volume","sat url",
                "ahrefs_organic_traffic","ahrefs_DR","ahrefs_organic_keywords",
                "ahrefs_traffic_value_usd","top_serp_keyword","top_serp_position"])
    w.writerows(out)
print("Linhas:",len(out)," | marcas:",len({r[0] for r in out}))
