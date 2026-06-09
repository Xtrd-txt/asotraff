#!/usr/bin/env python3
"""Gera registro unico (domain-level) de marcas de cassino BR:
   Grupo A = marcas licenciadas (.bet.br) + dominios clone/lookalike
   Grupo B = operadores offshore (Curacao etc) populares no BR, sem licenca SPA/MF
"""
import csv

def host(url):
    h = url.split("://", 1)[-1]
    return h.split("/", 1)[0]

def tld_pattern(h):
    parts = h.split(".")
    return "." + ".".join(parts[1:]) if len(parts) > 1 else h

REC = {
    "official":  "Dominio legitimo (.bet.br) — referencia",
    "HIGH":      "Prioridade takedown: WHOIS/redirect/forms; reportar registrador + SPA-MF/Anatel",
    "MED":       "Verificar afiliacao x impersonacao; monitorar",
    "LOW":       "Provavel afiliado/legado; monitorar",
    "offshore_grey":    "Operador sem licenca BR; monitorar / candidato a bloqueio",
    "offshore_blocked": "Ja suspenso/bloqueado (Anatel/SPA-MF)",
}

# ---- GRUPO A: oficial .bet.br ----
officials = {
    "Betano":"https://www.betano.bet.br/","Bet365":"https://www.bet365.bet.br/",
    "Blaze":"https://blaze.bet.br/pt/","KTO":"https://www.kto.bet.br/",
    "EstrelaBet":"https://www.estrelabet.bet.br/pb","Sportingbet":"https://www.sportingbet.bet.br/",
    "Pixbet":"https://pix.bet.br/","Betnacional":"https://betnacional.bet.br/",
    "Esportes da Sorte":"https://m.esportesdasorte.bet.br/","Superbet":"https://superbet.bet.br/",
    "Novibet":"https://www.novibet.bet.br/","Vai de Bet":"https://m.vaidebet.bet.br/",
    "Galera.bet":"https://www.galera.bet.br/","Brazino777":"https://www.brazino777.bet.br/",
    "Bet7k":"https://7k.bet.br/","F12.bet":"https://f12.bet.br/",
    "Betfair":"https://www.betfair.bet.br/","Stake":"https://stake.bet.br/",
    "Betsson":"https://www.betsson.com/br/casino",  # verificar .bet.br
}

# (marca, url, risco, sinal)
clones = [
 ("Betano","https://betanoda.com/","HIGH","mimetiza betano.com"),
 ("Betano","https://betano.cassino.br.com/","MED","subdominio br.com"),
 ("Bet365","https://365betcasino.net/","HIGH","typosquat 365bet + bonus"),
 ("Bet365","https://bet365-online.com.br/","MED","marca+sufixo"),
 ("Bet365","https://bet365s.com.br/","MED","typosquat plural"),
 ("Blaze","https://blazeapostasonline.com.br/","MED","alega 'Site Oficial'"),
 ("Blaze","https://blazeaposta.org/","LOW","afiliado/review"),
 ("Blaze","https://blaze-apostas-br.com/","LOW","afiliado/review"),
 ("Blaze","https://blazeaposta.com/","LOW","afiliado/review"),
 ("Blaze","https://blazebrasil.com.br/br/","LOW","afiliado/review"),
 ("KTO","https://kto.uk.com/","HIGH","'Plataforma Oficial' em .uk.com"),
 ("KTO","https://kto-brasil-br.com/","HIGH","alega oficial + 'Aposta Gratis'"),
 ("KTO","https://kto.jogo.com.br/","MED","alega 'Bet Autorizada kto.bet.br'"),
 ("KTO","https://kto-bet.br.com/","MED","subdominio br.com"),
 ("EstrelaBet","https://www.estrelabetoficial.com.br/","HIGH","usa 'oficial' + login"),
 ("EstrelaBet","https://br-estrelabet.com/","HIGH","alega 'Oficiais'"),
 ("EstrelaBet","https://casinosucesso.com/","MED","alega 'oficial site'"),
 ("EstrelaBet","https://estrelabet.com/","LOW","legado/intl"),
 ("Sportingbet","https://sportingbetn.com/","HIGH","typosquat 'sportingbetn'"),
 ("Sportingbet","https://sportingbetcasino.com.br/pt-br/","HIGH","alega 'site oficial'"),
 ("Sportingbet","https://sporting-bet.br.com/","MED","subdominio br.com"),
 ("Sportingbet","https://sportingbetbr.com.br/","MED","marca+sufixo"),
 ("Pixbet","https://pixbet.com/","LOW","dominio .com (verificar operador)"),
 ("Betnacional","https://betnacionalbrasil.com/cadastro.html","HIGH","promete R$5.000 (proibido)->nao licenciado"),
 ("Esportes da Sorte","https://esportesdasortebr.br.com/pt-br/","HIGH","'Site Oficial' em br.com"),
 ("Esportes da Sorte","https://esporte-da-sorte.com/","HIGH","variacao 'esporte' + bonus R$300"),
 ("Esportes da Sorte","https://esportesdasorte-oficial.com.br/pt-br/","HIGH","usa 'oficial'"),
 ("Esportes da Sorte","https://esportes-da-sortes.com/","HIGH","typosquat 'sortes' + 'oficial'"),
 ("Esportes da Sorte","https://esportesdasorte.net.br/","MED","marca+sufixo"),
 ("Esportes da Sorte","https://esportesdasorte-brasil.com.br/","MED","marca+sufixo"),
 ("Esportes da Sorte","https://esportesdasorte.br.com/","MED","subdominio br.com"),
 ("Superbet","https://superbet.app.br/","HIGH","'Download Oficial'"),
 ("Superbet","https://super-bet.br.com/","MED","subdominio br.com"),
 ("Superbet","https://superbetapp.net/","MED","marca+app"),
 ("Novibet","https://novibeth.com/","HIGH","typosquat + bonus R$5.000"),
 ("Novibet","https://novibet-site.com.br/","HIGH","typosquat farm Novbet/Movibet"),
 ("Vai de Bet","https://vaidebet-brazil.com/bonus/","MED","bonus + marca"),
 ("Vai de Bet","https://vai-de-bet.br.com/","MED","subdominio br.com"),
 ("Vai de Bet","https://vaidebetpt.com/","LOW","afiliado/intl"),
 ("Galera.bet","https://galerabetbrasil.com/","HIGH","'Site Oficial' + login"),
 ("Galera.bet","https://galerabet-br.com.br/pt-br/","MED","marca+sufixo"),
 ("Galera.bet","https://galera.cassino.br.com/","MED","subdominio br.com"),
 ("Galera.bet","https://galerabetapostas.com.br/","MED","marca+sufixo"),
 ("Galera.bet","https://galerabet-casino-brazil.com/","MED","marca+sufixo"),
 ("Galera.bet","https://galera-bet-apostas.com/","MED","marca+sufixo"),
 ("Galera.bet","https://galera.bet/","LOW","legado/intl"),
 ("Brazino777","https://www.brazino777-oficial.com.br/","HIGH","usa 'oficial' + R$4.000"),
 ("Brazino777","https://brazino777br.com.br/","HIGH","marca + bonus R$4.000"),
 ("Brazino777","https://brazinos777.com.br/","HIGH","typosquat plural"),
 ("Brazino777","https://brazino-777.br.com/","MED","subdominio br.com"),
 ("Brazino777","https://www.brazinoonline.com.br/","MED","marca+sufixo"),
 ("Brazino777","https://brazino777.cassino.br.com/","MED","subdominio br.com"),
 ("Brazino777","https://www.b777.com.br/","MED","abreviacao b777"),
 ("Brazino777","https://www.brazino777.com.br/","LOW","legado .com.br"),
 ("Bet7k","https://bet7kbr.com/","HIGH","bonus R$7000"),
 ("Bet7k","https://www-bet7k.com/","HIGH","typosquat 'www-'"),
 ("Bet7k","https://bet7k-brazil.com.br/","MED","marca+sufixo"),
 ("Bet7k","https://7k.cassino.br.com/","MED","subdominio br.com"),
 ("Bet7k","https://bet7k.com/","LOW","legado/intl"),
 ("F12.bet","https://f12betbrasil.com.br/","HIGH","bonus R$500"),
 ("F12.bet","https://f12bet.net.br/","MED","alega 'Site Oficial'"),
 ("F12.bet","https://f12.cassino.br.com/","MED","subdominio br.com"),
 ("F12.bet","https://f12-bet-brasil-br.com/","MED","marca+sufixo"),
 ("F12.bet","https://www.f12-bet.com/","LOW","legado/intl"),
 ("Betfair","https://www.betfairss.com/","HIGH","typosquat 'betfairss'"),
 ("Betfair","https://betfairbrasil.com.br/","MED","alega 'Oficial'"),
 ("Betfair","https://betfaircom.net/","MED","marca+sufixo"),
 ("Betfair","https://betfair.cat/","MED","TLD .cat"),
 ("Stake","https://stake.anjeangola.org/","HIGH","dominio aleatorio como 'Guia Oficial'"),
 ("Stake","https://stakecasino.com.br/","MED","alega 'site oficial login'"),
 ("Stake","https://stake-brazil-casino.com/","MED","marca+sufixo"),
 ("Stake","https://stake.app.br/","MED","marca+app"),
 ("Stake","https://stake-brazil.net/","MED","marca+sufixo"),
 ("1xBet","https://1xbet1.com.br/","HIGH","nao licenciado + bonus"),
 ("1xBet","https://1xbetonline.com.br/pt-br/","HIGH","nao licenciado + 'oficial'"),
 ("1xBet","https://1xbet.br.com/","HIGH","subdominio br.com + bonus"),
 ("1xBet","https://1xbetsbrasil.com.br/","HIGH","typosquat plural"),
 ("Betsson","https://betssons.br.com/","HIGH","bonus EUR250 + 'oficial'"),
 ("Betsson","https://betsson-brasil.br.com/","HIGH","'Site oficial'"),
 ("Betsson","https://betssonbrasil.com.br/","MED","marca+sufixo"),
 ("Betsson","https://betssoncassinobrasil.com/","MED","marca+sufixo"),
]

# ---- GRUPO B: offshore ----
# (marca, jurisdicao, licenca, operador, status, [urls], sinal)
offshore = [
 ("1win","Curacao","8048/JAZ2018-040","1win N.V.","offshore_grey",["https://1win.com.br/","https://1winpro.com.br/pt-br/"],"bonus 500%/R$5.000"),
 ("Mostbet","Curacao","8048/JAZ2016-065","Bizbon N.V.","offshore_grey",["https://mostbetbrasil.com/"],"bonus R$13 mil"),
 ("1xBet","Curacao","Antillephone","1X Corp N.V.","offshore_blocked",["https://1xbet.com.br/","https://1xbet.br.com/"],"bloqueado Anatel"),
 ("Betwinner","Curacao","8048/JAZ","Prevailer B.V.","offshore_blocked",["https://betwinnerbrasil.com.br/"],"suspenso out/2024"),
 ("22Bet","Curacao","8048/JAZ","TechSolutions Group N.V.","offshore_blocked",["https://22bett.com.br/","https://brasil-22bet.com.br/"],"suspenso out/2024"),
 ("Melbet","Curacao","8048/JAZ2020-060","Tutkia Ltd","offshore_grey",["https://melbetbr.com/","https://melbets.com.br/"],"bonus R$1.200"),
 ("Parimatch","Curacao","1668/JAZ (OGL/2024/402)","Pari-Match N.V.","offshore_grey",["https://parimatch-apostas.com.br/pt-br/","https://parimatchs.com.br/"],"bonus R$500"),
 ("Pin-Up","Curacao","8048/JAZ","Carletta N.V.","offshore_grey",["https://pin-up-casino.com/pt/","https://pinupbet.com.br/"],"bonus R$30 mil"),
 ("Megapari","Curacao","8048/JAZ","Antillephone N.V.","offshore_grey",["https://megapari.net.br/"],"bonus R$9.150"),
 ("LeonBet","Curacao","8048/JAZ2016-028","Curacao Gaming Commission","offshore_blocked",["https://leon.bet/","https://leonbet.com.br/en/"],"fora do ar BR"),
 ("BC.Game","Curacao","5536/JAZ (GCB)","BlockDance B.V.","offshore_blocked",["https://br.bc1.game/","https://bcgame.lat/"],"crypto-only; saida BR"),
 ("Roobet","Curacao","OGL/2024/687/0427 (CGA)","Raw Entertainment B.V.","offshore_grey",["https://roobet.com/pt/","https://roobet.br.com/"],"crypto"),
 ("BetFury","Curacao","#365/JAZ","Universe Games B.V.","offshore_grey",["https://bf1.io/","https://betfurycasino.com.br/"],"crypto; bonus 590%"),
 ("Bodog","Curacao","1668/JAZ","Connaught Media B.V.","offshore_blocked",["https://bodogbr.bet/","https://bodog-br.com/"],"suspenso out/2024"),
 ("20Bet","Curacao","8048/JAZ","TechSolutions Group N.V.","offshore_blocked",["https://20bet-brasil.com/","https://20betsite.com/"],"suspenso out/2024"),
 ("Linebet","Curacao","8048/JAZ2016-053 (CGA)","Bumblebee Ltd","offshore_grey",["https://linebet10.com/"],"bonus + cripto"),
 ("GGBet","Curacao","OGL/2024/688/0234","Brivio Ltd","offshore_grey",["https://gg-bet-brasil.com/","https://ggbet-br.com.br/pt-br/"],"foco e-sports"),
 ("Betobet","Curacao","1668/JAZ","Counder B.V.","offshore_grey",["https://betobet-brasil.com/","https://betobet.biz/"],"bonus R$500/R$2.500"),
 ("Cbet","Curacao","#365/JAZ","AK Global N.V.","offshore_grey",["https://cbet-br.com/","https://cbet-gg.br.com/"],"crypto"),
 ("Sportaza","Curacao","8048/JAZ2020-001","Rabidi N.V.","offshore_blocked",["https://sportaza-brasil.com/","https://sportaza.one/casino/"],"bloqueado Anatel out/2024"),
]

rows = []
# Grupo A oficiais
for brand, url in officials.items():
    h = host(url)
    rows.append(["A-licenciada", brand, h, url, "oficial", "official",
                 "Brasil SPA/MF", ".bet.br", "", "AUTORIZADO", tld_pattern(h),
                 "dominio oficial", REC["official"]])
# Grupo A clones
for brand, url, risk, sig in clones:
    h = host(url)
    typ = "afiliado" if risk == "LOW" else "clone/lookalike"
    rows.append(["A-licenciada", brand, h, url, typ, risk,
                 "", "", "", "NAO AUTORIZADO", tld_pattern(h), sig, REC[risk]])
# Grupo B offshore
for brand, jur, lic, op, status, urls, sig in offshore:
    for url in urls:
        h = host(url)
        rows.append(["B-offshore", brand, h, url, "offshore", status,
                     jur, lic, op, status.replace("offshore_","").upper(),
                     tld_pattern(h), sig, REC[status]])

header = ["grupo","marca","dominio","url","tipo","risco_status",
          "jurisdicao_licenca","numero_licenca","operador","status_br",
          "padrao_tld","sinal","recomendacao"]

with open("casino_brand_registry.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

print("Linhas:", len(rows))
from collections import Counter
print("Por grupo:", dict(Counter(r[0] for r in rows)))
print("Por risco/status:", dict(Counter(r[5] for r in rows)))
print("Marcas unicas:", len({r[1] for r in rows}))
