#!/usr/bin/env python3
"""Gera 2 tabelas da estrategia de lancamento EMD."""
import csv

# (1) matriz estrategica por criterio do TZ
matrix=[
 ["Бренди (вибір)","11 брендів мають живі паразити","26 брендів — мертві мережі",
  "10 брендів: 5 жирних (Betano, Esportes da Sorte, KTO, 1xBet, Sportingbet) + 5 середніх (Cbet, 20Bet, Vai de Bet, Mostbet, Pin-Up). Пріоритет середнім/офшорним — кращий ROI"],
 ["Сайтів на 1 бренд","кластер 2-7 (Esportes 7, Mostbet 3)","часто 1 одностранічник",
  "5 сайтів/бренд (разом ~50 на тест)"],
 ["Типи доменів","локальні .br=10, загальні=7, ферма *.br.com=5","-",
  "Мікс/бренд: 2×.com.br + 1×.com + 1×*.br.com (DR90 ферма) + 1×дроп"],
 ["Дропи: ref-домени","медіана 433 ref","медіана 135 ref",
  "Брати дроп з 150-450 BR-ref (vai-de-bet.br.com=1276/1kw, en.mostbetbr.net=2032)"],
 ["Дропи: тема/гео","Top Country = br","-","Тема спорт/новини/беттінг PT-BR, гео BR, ~15% dofollow, не токсичний"],
 ["Внутрішні сторінки","internal links медіана 239","internal links медіана 4",
  "ОБОВ'ЯЗКОВО: хаб + 5-10 сторінок (/cassino /cadastro /bonus /app /login) з перелінковкою (≥200 internal)"],
 ["Лінки: обсяг","медіана 1201 BL / 433 ref","медіана 185 BL / 135 ref",
  "Ціль ~430 ref-доменів, ~1200 backlinks"],
 ["Лінки: типи","~15% dofollow (foll 69 з 433)","-","Переважно nofollow, BR-донори, тематичні"],
 ["Лінки: коли від запуску","немає в статичному зрізі","-",
  "Потрібен Ahrefs експорт 'New/Lost by date'; gen_linkprofile.py рахує типи зараз"],
 ["301-підклейки","працює лише на сайтах з контентом","linebet10=273/pin-up-casino=218 → трафік 0",
  "Betano.cassino.br.com=31 301 → 2688 трафіку ✅. Склейка дропів ТІЛЬКИ як підсилення, не основа"],
 ["Каноникал","потрібен краул (403)","-","Фіксується через gen_onpage_audit.py (колонки canonical + redirect_to)"],
 ["Махінації","ферма *.br.com (чужий DR90); 301-склейка дропів; 'oficial'+welcome-бонус; .gov.br-паразитинг","-",
  ".gov.br = найжирніший вектор (web3.antaq.gov.br #7 'betano cassino online' 4216 трафіку)"],
 ["Текст (обсяг слів)","ПОТРІБЕН КРАУЛ","ПОТРІБЕН КРАУЛ","Запустити gen_onpage_audit.py → колонка words"],
 ["Картинки","ПОТРІБЕН КРАУЛ","-","onpage_audit.py → колонка images"],
 ["OpenGraph (так/ні)","ПОТРІБЕН КРАУЛ","-","onpage_audit.py → колонка opengraph"],
 ["Розмітка schema (так/ні)","ПОТРІБЕН КРАУЛ","-","onpage_audit.py → колонка schema_markup"],
 ["DR","медіана 14 (ферма *.br.com інфляція до 90)","медіана 8","Орієнтир — трафік+keywords, не DR (ферма дає фейк-DR90)"],
 ["Висновок","Не дорвей, а мультисторінковий сайт + 430 ref + дроп/ферма для DR + вибіркова 301","",
  "Еталон копіювання: esporte-da-sorte.com (61.8k), cbet-gg.br.com (17.9k)"],
]
with open("launch_strategy_matrix.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Параметр (ТЗ)","Дані winners","Дані dead","Рекомендація / стратегія"]); w.writerows(matrix)

# (2) plano por marca
plan=[
 ["Betano","жирний",1830000,"betano.cassino.br.com",2688,5,"2×.com.br,1×.com,1×*.br.com,1×дроп","середній (офіціал+gov оборона)"],
 ["Esportes da Sorte","жирний",450000,"esporte-da-sorte.com",61805,5,"2×.com.br,1×.com,1×*.br.com,1×дроп","★ ВИСОКИЙ (еталон)"],
 ["KTO","жирний",368000,"kto.jogo.com.br",4517,5,"2×.com.br,1×.com,1×*.br.com,1×дроп","високий"],
 ["1xBet","жирний",673000,"1xbetonline.com.br",159,5,"2×.com.br,1×.com,1×*.br.com,1×дроп","середній"],
 ["Sportingbet","жирний",301000,"sportingbetcasino.com.br",0,5,"2×.com.br,1×.com,1×*.br.com,1×дроп","тест (складний)"],
 ["Cbet","середній",27100,"cbet-gg.br.com",17899,5,"2×*.br.com,2×.com.br,1×дроп","★ ВИСОКИЙ (best ROI)"],
 ["20Bet","середній",33100,"20betsite.com",2089,5,"2×.com,2×.com.br,1×дроп","високий"],
 ["Vai de Bet","середній",135000,"vai-de-bet.br.com",1483,5,"2×*.br.com,2×.com.br,1×дроп","високий"],
 ["Mostbet","середній",165000,"mostbet.net.br",203,5,"2×.com.br,1×.net.br,1×.com,1×дроп","середній (мережа дропів)"],
 ["Pin-Up","середній",246000,"pinupbet.com.br",310,5,"2×.com.br,1×.com,1×*.br.com,1×дроп","середній"],
]
with open("brand_launch_plan.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Бренд","Тір","Частотка (бренд-кей)","Доведений топ-паразит","Трафік паразита/міс","Сайтів","Мікс доменів","Пріоритет"]); w.writerows(plan)

print("launch_strategy_matrix.csv:",len(matrix),"рядків")
print("brand_launch_plan.csv:",len(plan),"брендів")
