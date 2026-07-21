#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ukrainian, human-styled versions of the TouchRetouch ASA test task (xlsx + deck + doc)."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from docx import Document
from docx.shared import Pt as DPt, RGBColor as DRGB
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE="/home/user/asotraff/outputs/touchretouch-testtask/"

# ---------- warm human palette ----------
PAPER="FAF7F1"; INKX="23303B"; CORAL="C8542F"; TEAL="2E7D74"; WARM="6E6A63"; LINE="E3DCD0"
CREAM="F3ECE0"
INK=RGBColor(0x23,0x30,0x3B); COR=RGBColor(0xC8,0x54,0x2F); TL=RGBColor(0x2E,0x7D,0x74)
WM=RGBColor(0x6E,0x6A,0x63); WHT=RGBColor(0xFF,0xFF,0xFF); PP=RGBColor(0xFA,0xF7,0xF1); CR=RGBColor(0xF3,0xEC,0xE0)

# =========================================================
# 1) XLSX (UA, warm headers, bug fixed — no notes starting with '=')
# =========================================================
def build_xlsx():
    wb=openpyxl.Workbook()
    def fill(h): return PatternFill("solid", fgColor=h)
    thin=Side(style="thin", color="D8CFC0"); border=Border(thin,thin,thin,thin)
    h1=Font(name="Georgia",size=16,bold=True,color=INKX)
    h2=Font(name="Georgia",size=12,bold=True,color="FFFFFF")
    lbl=Font(name="Calibri",size=10,bold=True,color=INKX)
    reg=Font(name="Calibri",size=10,color=INKX)
    muted=Font(name="Calibri",size=9,italic=True,color=WARM)
    inp=Font(name="Calibri",size=10,bold=True,color="9A3412")
    res=Font(name="Calibri",size=10,bold=True,color=CORAL)
    center=Alignment(horizontal="center",vertical="center")
    left=Alignment(horizontal="left",vertical="center",wrap_text=True)
    def sec(ws,row,text,span,color=CORAL):
        c=ws.cell(row=row,column=1,value=text); c.font=h2; c.alignment=Alignment(horizontal="left",vertical="center")
        ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span)
        for col in range(1,span+1): ws.cell(row=row,column=col).fill=fill(color)

    ws=wb.active; ws.title="Припущення"; ws.sheet_view.showGridLines=False
    for col,w in zip("ABCD",[44,14,16,54]): ws.column_dimensions[col].width=w
    ws["A1"]="TouchRetouch — модель воронки та ROAS (Apple Search Ads)"; ws["A1"].font=h1
    ws["A2"]="Помаранчеві клітинки — редаговані вхідні. Сині — розраховані. Дохід рахується на базі ARPPU за перший рік."
    ws["A2"].font=muted; ws.merge_cells("A2:D2")
    r=4; sec(ws,r,"  ОСНОВНІ ПРИПУЩЕННЯ ВОРОНКИ (редагуй ці)",4); r+=1
    for i,t in enumerate(["Показник","Значення","Од.","Примітка / джерело"]):
        c=ws.cell(row=r,column=i+1,value=t); c.font=lbl; c.fill=fill(CREAM); c.border=border
    r+=1
    A=[("i2t","Інстал → Тріал",0.15,"%","Дано (платна воронка)"),
       ("t2p","Тріал → Оплата",0.20,"%","Дано (платна воронка)"),
       ("arppu","ARPPU (1-й рік, без комісії Apple)",22.2,"$","Дано"),
       ("d30","Визнання доходу на D30 (частка річного)",0.45,"%","ЛИШЕ ДОВІДКА (не в гейті) — взяти реальну криву D30/рік з RevenueCat"),
       ("roas","Мін. ROAS для масштабування (D30)",1.25,"x","Вимога з завдання")]
    nc={}
    for key,label,val,unit,note in A:
        ws.cell(row=r,column=1,value=label).font=reg; ws.cell(row=r,column=1).alignment=left
        c=ws.cell(row=r,column=2,value=val); c.font=inp; c.fill=fill("FFF7ED"); c.alignment=center; c.border=border
        c.number_format="0.0%" if unit=="%" else ('"$"0.00' if unit=="$" else "0.00")
        ws.cell(row=r,column=3,value=unit).font=reg; ws.cell(row=r,column=3).alignment=center
        ws.cell(row=r,column=4,value=note).font=muted; ws.cell(row=r,column=4).alignment=left
        nc[key]=f"$B${r}"; r+=1
    r+=1; sec(ws,r,"  ПОХІДНА ЮНІТ-ЕКОНОМІКА (розрахунок)",4,TEAL); r+=1
    d=[("Платників на інстал",f"={nc['i2t']}*{nc['t2p']}","0.00%","тріал% × оплата%"),
       ("Дохід на інстал (рік)",None,'"$"0.000',"платників/інстал × ARPPU"),
       ("Беззбитковий CPI (ROAS 100%)",None,'"$"0.000',"дорівнює доходу на інстал"),
       ("Цільовий CPI для мін. ROAS",None,'"$"0.000',"дохід/інстал ÷ мін. ROAS")]
    pi=r
    for label,formula,fmt,note in d:
        ws.cell(row=r,column=1,value=label).font=reg; ws.cell(row=r,column=1).alignment=left
        c=ws.cell(row=r,column=2); c.font=res; c.fill=fill("EAF0FB"); c.alignment=center; c.border=border; c.number_format=fmt
        ws.cell(row=r,column=4,value=note).font=muted; ws.cell(row=r,column=4).alignment=left; r+=1
    ws.cell(row=pi,column=2).value=f"={nc['i2t']}*{nc['t2p']}"
    ws.cell(row=pi+1,column=2).value=f"=$B${pi}*{nc['arppu']}"
    ws.cell(row=pi+2,column=2).value=f"=$B${pi+1}"
    ws.cell(row=pi+3,column=2).value=f"=$B${pi+1}/{nc['roas']}"
    r+=1
    ws.cell(row=r,column=1,value="ГОЛОВНЕ: уся задача = опустити блендовий CPI до ≤ цільового і втримати, подвоюючи витрати.").font=Font(name="Calibri",size=10,bold=True,color=CORAL)
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=4)

    ARPPU=f"Припущення!{nc['arppu']}"; I2T=f"Припущення!{nc['i2t']}"; T2P=f"Припущення!{nc['t2p']}"
    D30=f"Припущення!{nc['d30']}"; MIN=f"Припущення!{nc['roas']}"

    ws2=wb.create_sheet("Модель"); ws2.sheet_view.showGridLines=False
    cols=["Фаза / місяць","Витрати ($)","Блендовий CPT ($)","TTR","CR тап→інстал","CPI ($)","Тапи","Інстали","Тріали","Платники","Дохід ($)","D30 кеш","ROAS (гейт)","D30 ROAS","Гейт?"]
    for i,w in enumerate([24,12,15,8,14,11,11,11,10,10,13,11,11,10,9]): ws2.column_dimensions[get_column_letter(i+1)].width=w
    ws2["A1"]="Витрати → Тапи → Інстали → Тріали → Платники → Дохід → ROAS"; ws2["A1"].font=h1
    ws2["A2"]="Помаранчеве — редаговані драйвери. Решта — живі формули. Логіка: спершу банкуємо ефективність (M1), потім масштабуємо в запас."
    ws2["A2"].font=muted; ws2.merge_cells("A2:O2")
    hr=4
    for i,c in enumerate(cols):
        cell=ws2.cell(row=hr,column=i+1,value=c); cell.font=Font(name="Calibri",size=9,bold=True,color="FFFFFF")
        cell.fill=fill(CORAL); cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); cell.border=border
    ramp=[("M0 — Базовий (зараз)",35000,0.2564,0.070,0.385),
          ("M1 — Банк ефективності",35000,0.2240,0.075,0.400),
          ("M2 — Гейт пройдено",40000,0.2230,0.078,0.420),
          ("M3 — Скейл понад гейт",55000,0.2323,0.080,0.440),
          ("Q2 — Ціль",70000,0.2363,0.082,0.450)]
    f=hr+1
    for j,(ph,sp,cpt,ttr,cr) in enumerate(ramp):
        rr=f+j
        ws2.cell(row=rr,column=1,value=ph).font=reg; ws2.cell(row=rr,column=1).alignment=left
        for col,val,fmt in [(2,sp,'"$"#,##0'),(3,cpt,'"$"0.000'),(4,ttr,'0.0%'),(5,cr,'0.0%')]:
            c=ws2.cell(row=rr,column=col,value=val); c.font=inp; c.fill=fill("FFF7ED"); c.alignment=center; c.border=border; c.number_format=fmt
        ws2.cell(row=rr,column=6,value=f"=C{rr}/E{rr}").number_format='"$"0.000'
        ws2.cell(row=rr,column=7,value=f"=B{rr}/C{rr}").number_format='#,##0'
        ws2.cell(row=rr,column=8,value=f"=G{rr}*E{rr}").number_format='#,##0'
        ws2.cell(row=rr,column=9,value=f"=H{rr}*{I2T}").number_format='#,##0'
        ws2.cell(row=rr,column=10,value=f"=I{rr}*{T2P}").number_format='#,##0'
        ws2.cell(row=rr,column=11,value=f"=J{rr}*{ARPPU}").number_format='"$"#,##0'
        ws2.cell(row=rr,column=12,value=f"=K{rr}*{D30}").number_format='"$"#,##0'
        ws2.cell(row=rr,column=13,value=f"=K{rr}/B{rr}").number_format='0%'
        ws2.cell(row=rr,column=14,value=f"=L{rr}/B{rr}").number_format='0%'
        ws2.cell(row=rr,column=15,value=f'=IF(M{rr}>={MIN},"ТАК","НІ")').alignment=center
        for col in range(6,16):
            c=ws2.cell(row=rr,column=col); c.border=border; c.alignment=center
            c.font=res if col in (13,14) else reg
    nr=f+len(ramp)+1
    ws2.cell(row=nr,column=1,value="Нотатки:").font=lbl
    for k,n in enumerate([
        "• ROAS (гейт) рахується на базі річного ARPPU — той самий базис, що й якір «~100% на 1-му місяці». Гейт = 125%.",
        "• M1 тримає витрати на $35K, але ріже переплату по бренду + сміттєві гео → CPI 0.666→0.560 → гейт пройдено ДО масштабування.",
        "• Базовий план дає 125% на самій CPT-ефективності (воронка фіксована). Приріст CR/Тріал→Оплата (CPP+PPO+пейвол) — це апсайд, не закладено.",
        "• «D30 ROAS» — довідковий: реальний кеш на D30 = ROAS × коеф. визнання (Припущення). Заміни 0.45 на реальну криву RevenueCat."]):
        ws2.cell(row=nr+1+k,column=1,value=n).font=muted; ws2.merge_cells(start_row=nr+1+k,start_column=1,end_row=nr+1+k,end_column=15)
    # ---- Sheet 3: Чутливість ----
    ws3=wb.create_sheet("Чутливість"); ws3.sheet_view.showGridLines=False
    for i,w in enumerate([34,16,16,16,40]): ws3.column_dimensions[get_column_letter(i+1)].width=w
    ws3["A1"]="Чутливість — який показник найбільше рухає ROAS?"; ws3["A1"].font=h1
    ws3["A2"]="ROAS = (CR_тап→інстал × Тріал% × Оплата% × ARPPU) ÷ CPT. Ланцюг мультиплікативний → у кожного показника РІВНА % еластичність."
    ws3["A2"].font=muted; ws3.merge_cells("A2:E2")
    hr=4
    for i,c in enumerate(["Важіль","База","+10% покращення","Новий ROAS","Контроль / запас"]):
        cell=ws3.cell(row=hr,column=i+1,value=c); cell.font=Font(name="Calibri",size=10,bold=True,color="FFFFFF"); cell.fill=fill(TEAL); cell.alignment=center; cell.border=border
    sens=[("CR тап→інстал",0.42,"0.0%","UA-керований через CPP / PPO — великий запас"),
          ("Тріал → Оплата",0.20,"0.0%","Продукт/пейвол — найбільший запас, треба продукт"),
          ("Інстал → Тріал",0.15,"0.0%","Онбординг — спільно з продуктом"),
          ("CPT (менше = краще)",0.238,"0.00","UA-керований через структуру/біди — найшвидший важіль")]
    for j,(lever,base,fmt,ctrl) in enumerate(sens):
        rr=hr+1+j
        ws3.cell(row=rr,column=1,value=lever).font=reg; ws3.cell(row=rr,column=1).alignment=left; ws3.cell(row=rr,column=1).border=border
        b=ws3.cell(row=rr,column=2,value=base); b.number_format=fmt; b.alignment=center; b.border=border; b.font=reg
        imp=ws3.cell(row=rr,column=3,value=(f"=B{rr}*0.9" if "CPT" in lever else f"=B{rr}*1.1")); imp.number_format=fmt; imp.alignment=center; imp.border=border; imp.font=reg
        ws3.cell(row=rr,column=4,value="+10% ROAS").font=res; ws3.cell(row=rr,column=4).alignment=center; ws3.cell(row=rr,column=4).border=border
        ws3.cell(row=rr,column=5,value=ctrl).font=muted; ws3.cell(row=rr,column=5).alignment=left; ws3.cell(row=rr,column=5).border=border
    cc=hr+1+len(sens)+1
    ws3.cell(row=cc,column=1,value="Висновок: еластичність рівна, тож пріоритет за запасом × контрольованістю →").font=Font(name="Calibri",size=10,bold=True,color=INKX)
    ws3.merge_cells(start_row=cc,start_column=1,end_row=cc,end_column=5)
    ws3.cell(row=cc+1,column=1,value="1) CPT-ефективність (задокументоване марнотратство — найшвидше), 2) Тріал→Оплата (лише 20%, найбільший запас), 3) tap→install CR через CPP/PPO.").font=reg
    ws3.merge_cells(start_row=cc+1,start_column=1,end_row=cc+1,end_column=5)

    # ---- Sheet 4: Перерозподіл витрат ----
    ws4=wb.create_sheet("Перерозподіл"); ws4.sheet_view.showGridLines=False
    for i,w in enumerate([30,16,16,16,42]): ws4.column_dimensions[get_column_letter(i+1)].width=w
    ws4["A1"]="Поточний vs цільовий розподіл витрат ($35K)"; ws4["A1"].font=h1
    ws4["A2"]="Перекидаю з бренд-переплати + сміттєвих мульти-гео → в ефективний US generic / competitor Search Results."
    ws4["A2"].font=muted; ws4.merge_cells("A2:E2")
    hr=4
    for i,c in enumerate(["Бакет","Зараз %","Зараз $","Ціль %","Обґрунтування"]):
        cell=ws4.cell(row=hr,column=i+1,value=c); cell.font=Font(name="Calibri",size=10,bold=True,color="FFFFFF"); cell.fill=fill(CORAL); cell.alignment=center; cell.border=border
    mix=[("Бренд",0.58,0.25,"Кап біда до ~факту; бренд частково канібалізує органіку. Звільняю бюджет."),
         ("Generic Core (US, exact)",0.20,0.34,"Масштабую перевірені head/mid-терміни під CPA-таргет."),
         ("Generic Discovery (SM+Broad)",0.11,0.15,"Ізольовано, негативи з Core; харвест переможців."),
         ("Competitor (Search Results)",0.01,0.12,"Новий conquesting у Search Results (був лише PP, CPA €17)."),
         ("Feature / мульти-гео T1",0.10,0.14,"Ріжу сміттєві гео; ізолюю US; feature у generic.")]
    for j,(b,cur,tgt,rat) in enumerate(mix):
        rr=hr+1+j
        ws4.cell(row=rr,column=1,value=b).font=reg; ws4.cell(row=rr,column=1).alignment=left; ws4.cell(row=rr,column=1).border=border
        c1=ws4.cell(row=rr,column=2,value=cur); c1.number_format="0%"; c1.alignment=center; c1.border=border; c1.font=reg
        c2=ws4.cell(row=rr,column=3,value=f"=B{rr}*35000"); c2.number_format='"$"#,##0'; c2.alignment=center; c2.border=border; c2.font=reg
        c3=ws4.cell(row=rr,column=4,value=tgt); c3.number_format="0%"; c3.alignment=center; c3.border=border; c3.font=res
        c4=ws4.cell(row=rr,column=5,value=rat); c4.font=muted; c4.alignment=left; c4.border=border
    tot=hr+1+len(mix)
    ws4.cell(row=tot,column=1,value="РАЗОМ").font=lbl
    ws4.cell(row=tot,column=2,value=f"=SUM(B{hr+1}:B{hr+len(mix)})").number_format="0%"; ws4.cell(row=tot,column=2).alignment=center; ws4.cell(row=tot,column=2).font=lbl
    ws4.cell(row=tot,column=3,value=f"=SUM(C{hr+1}:C{hr+len(mix)})").number_format='"$"#,##0'; ws4.cell(row=tot,column=3).alignment=center; ws4.cell(row=tot,column=3).font=lbl
    ws4.cell(row=tot,column=4,value=f"=SUM(D{hr+1}:D{hr+len(mix)})").number_format="0%"; ws4.cell(row=tot,column=4).alignment=center; ws4.cell(row=tot,column=4).font=lbl

    wb.save(BASE+"TouchRetouch_ROAS_модель_UA.xlsx"); print("xlsx UA ok (4 sheets)")

# =========================================================
# 2) DECK (UA, human/warm/serif)
# =========================================================
def build_deck():
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    BLANK=prs.slide_layouts[6]; SW,SH=prs.slide_width,prs.slide_height
    def slide():
        s=prs.slides.add_slide(BLANK)
        bg=s.shapes.add_shape(1,0,0,SW,SH); bg.fill.solid(); bg.fill.fore_color.rgb=PP; bg.line.fill.background(); bg.shadow.inherit=False
        s.shapes._spTree.remove(bg._element); s.shapes._spTree.insert(2,bg._element); return s
    def tf(s,l,t,w,h):
        b=s.shapes.add_textbox(l,t,w,h); b.text_frame.word_wrap=True; return b.text_frame
    def par(p,text,size,color=INK,bold=False,align=PP_ALIGN.LEFT,space=6,italic=False,font="Calibri"):
        p.text=text; p.alignment=align; p.space_after=Pt(space)
        r=p.runs[0]; r.font.size=Pt(size); r.font.bold=bold; r.font.italic=italic; r.font.color.rgb=color; r.font.name=font
    def head(s,num,eyebrow,title):
        # numbered circle
        c=s.shapes.add_shape(9,Inches(0.55),Inches(0.5),Inches(0.62),Inches(0.62))
        c.fill.solid(); c.fill.fore_color.rgb=COR; c.line.fill.background(); c.shadow.inherit=False
        par(c.text_frame.paragraphs[0],num,20,WHT,bold=True,align=PP_ALIGN.CENTER,space=0,font="Georgia")
        t=tf(s,Inches(1.4),Inches(0.42),Inches(11.4),Inches(1.1))
        par(t.paragraphs[0],eyebrow.upper(),11,COR,bold=True,space=2)
        p=t.add_paragraph(); par(p,title,24,INK,bold=True,space=0,font="Georgia")
        ln=s.shapes.add_shape(1,Inches(1.4),Inches(1.45),Inches(11.4),Pt(2))
        ln.fill.solid(); ln.fill.fore_color.rgb=COR; ln.line.fill.background(); ln.shadow.inherit=False
    def bullets(s,items,l,t,w,h,size=15,gap=9):
        f=tf(s,l,t,w,h)
        for i,(txt,lvl) in enumerate(items):
            p=f.paragraphs[0] if i==0 else f.add_paragraph()
            col=INK if lvl==0 else WM; pre="—  " if lvl==0 else "·  "
            par(p,pre+txt,size if lvl==0 else size-2,col,bold=(lvl==0),space=gap); p.level=0 if lvl==0 else 1
    def chip(s,l,t,w,text,color=TL,h=Inches(0.5)):
        c=s.shapes.add_shape(5,l,t,w,h); c.fill.solid(); c.fill.fore_color.rgb=color; c.line.fill.background(); c.shadow.inherit=False
        tfr=c.text_frame; tfr.word_wrap=True; par(tfr.paragraphs[0],text,11.5,WHT,bold=True,align=PP_ALIGN.CENTER,space=0)
    def table(s,data,l,t,w,colw,rowh=Inches(0.45),fs=11):
        gt=s.shapes.add_table(len(data),len(data[0]),l,t,w,rowh*len(data)).table
        try:
            gt.first_row=False; gt.horz_banding=False
        except Exception: pass
        for ci,cw in enumerate(colw): gt.columns[ci].width=cw
        for ri,row in enumerate(data):
            for cidx,val in enumerate(row):
                cell=gt.cell(ri,cidx); cell.margin_left=Pt(6); cell.margin_right=Pt(4); cell.margin_top=Pt(2); cell.margin_bottom=Pt(2)
                cell.vertical_anchor=MSO_ANCHOR.MIDDLE
                p=cell.text_frame.paragraphs[0]; rr=p.add_run(); rr.text=str(val); rr.font.size=Pt(fs); rr.font.name="Calibri"
                if ri==0:
                    cell.fill.solid(); cell.fill.fore_color.rgb=COR; rr.font.bold=True; rr.font.color.rgb=WHT; rr.font.name="Georgia"
                else:
                    cell.fill.solid(); cell.fill.fore_color.rgb=(WHT if ri%2 else CR); rr.font.color.rgb=INK

    # S1 cover
    s=slide()
    band=s.shapes.add_shape(1,0,Inches(2.2),Inches(0.28),Inches(3.0)); band.fill.solid(); band.fill.fore_color.rgb=COR; band.line.fill.background(); band.shadow.inherit=False
    t=tf(s,Inches(0.75),Inches(2.15),Inches(11.8),Inches(3.2))
    par(t.paragraphs[0],"APPLE SEARCH ADS · ТЕСТОВЕ ЗАВДАННЯ",13,COR,bold=True,space=10)
    p=t.add_paragraph(); par(p,"TouchRetouch: забираю канал in-house,",30,INK,bold=True,space=2,font="Georgia")
    p=t.add_paragraph(); par(p,"лагоджу і готую до масштабування",30,INK,bold=True,space=12,font="Georgia")
    p=t.add_paragraph(); par(p,"Фоторедактор (iOS) · freemium: тижневий тріал → підписка · ринок US · план на 2 квартали до $70K/міс при ROAS ≥125%",14,WM,space=0)
    t2=tf(s,Inches(0.75),Inches(6.0),Inches(11.8),Inches(1))
    par(t2.paragraphs[0],"Коротко: спершу зрізаю зайве по бренду й гео, банкую запас по ROAS — і лише потім масштабую ефективний US generic та competitor у цей запас.",13,WM,italic=True,space=0)

    # S2 audit
    s=slide(); head(s,"1","Аудит акаунта","Що я побачив і що болить найбільше")
    t=tf(s,Inches(1.4),Inches(1.55),Inches(11.4),Inches(0.5))
    par(t.paragraphs[0],"Проблеми відсортовані за впливом на дохід — зверху те, що коштує найбільше грошей.",12.5,WM,italic=True,space=0)
    data=[["#","Проблема","Чому це гроші","Що роблю"],
    ["1","Бренд = 58% витрат (~$20K) + канібалізація","Плачу за інстали, які органіка бере безкоштовно; макс. бід €25–35 при факті €1.2–1.9","Кап біда ~€2–3; pause-тест; перекидаю бюджет"],
    ["2","Search Match (31%) у тих же generic, без негативів","SM конкурує з власними exact-ключами, крутить наосліп","Виношу в окремий Discovery; Core як негативи"],
    ["3","T1_Generic: 40 сторфронтів під одним бідом","US конкурує з UZ/KG-сміттям (TTR 4–5%)","Ділю по гео/тирах; ізолюю US; ріжу сміття"],
    ["4","Competitor лише на Product Pages (CPA €17)","x10 неефективно; немає conquesting у Search Results","Запускаю competitor у Search Results"],
    ["5","Feature: одиничні інстали по €4–7","Не масштабується, переплата на копійках об'єму","Згортаю в generic ad group"],
    ["6","Console vs MMP розходяться на 30%","Не можна довіряти ROAS — це фундамент","Реконсиляція (див. вимірювання)"]]
    table(s,data,Inches(0.5),Inches(2.1),Inches(12.5),[Inches(0.4),Inches(3.7),Inches(4.6),Inches(3.8)],rowh=Inches(0.72),fs=11)

    # S3 architecture
    s=slide(); head(s,"1","Реструктуризація","Якою я роблю архітектуру акаунта")
    rows=[("Бренд (US)","Exact · бід капнутий ~€2–3","Дешево захищаю, не переплачую; міряю інкремент",COR),
    ("Generic Core (US)","Exact · ручні біди","Перевірені head/mid-ключі під CPA-таргет",TL),
    ("Generic Discovery","Search Match + Broad, ІЗОЛЬОВАНО","Шукаю нове → харвест у Core; Core як негативи",TL),
    ("Competitor (US)","Exact · Search Results","Conquesting зі своїм CPP (був лише PP, CPA €17)",COR),
    ("Feature","Ad group всередині Generic","Без окремого зоопарку дрібних термінів",WM)]
    y=Inches(1.8)
    for name,cfg,why,c in rows:
        chip(s,Inches(0.55),y,Inches(3.0),name,c,h=Inches(0.55))
        t=tf(s,Inches(3.75),y-Inches(0.02),Inches(9.1),Inches(0.7))
        par(t.paragraphs[0],cfg,13,INK,bold=True,space=2); p=t.add_paragraph(); par(p,why,12,WM,space=0)
        y+=Inches(0.9)
    t=tf(s,Inches(0.55),Inches(6.55),Inches(12.3),Inches(0.8))
    par(t.paragraphs[0],"Негативи: Core-ключі → негативи в Discovery/Search Match · бренд-терміни → негативи в Generic і Competitor. Плейсменти: Search Results — основний; Search/Today tab — тестами; Product Pages лише там, де окупається.",12,INK,italic=True,space=0)

    # S4 keywords
    s=slide(); head(s,"2","Ключі","Процес + приклад пулу за інтентом")
    t=tf(s,Inches(1.4),Inches(1.55),Inches(11.4),Inches(0.55))
    par(t.paragraphs[0],"Процес: сіди з продукту + автосаджест App Store + AppTweak/ASOMobile (обсяг/складність/інтент) + search-term звіти ASA + метадата конкурентів + харвест з Discovery. Ре-ресёрч щокварталу.",12,WM,space=0)
    data=[["Бренд","Generic","Competitor","Feature"],
    ["touchretouch (exact)","photo editor (exact)","facetune (exact)","magic eraser (exact)"],
    ["touchretouch app (exact)","object remover (exact)","snapseed (exact)","remove people (exact)"],
    ["","remove object from photo","picsart (exact)","background eraser (exact)"],
    ["","photo retouch (exact)","lightroom (exact)","unwanted object remover"],
    ["","unblur / photo enhancer","youcam perfect (exact)","object eraser (exact)"]]
    table(s,data,Inches(0.5),Inches(2.25),Inches(12.3),[Inches(3.0),Inches(3.3),Inches(3.0),Inches(3.0)],rowh=Inches(0.5),fs=11)
    t=tf(s,Inches(0.5),Inches(5.95),Inches(12.3),Inches(1.1))
    par(t.paragraphs[0],"Логіка match: exact для перевірених; Broad+Search Match — ізольовано в Discovery для харвесту. Бренди конкурентів: бідю в ASA, але НІКОЛИ не в метадаті (trademark / 2.3.7).",12,COR,bold=True,space=0)

    # S5 ASO
    s=slide(); head(s,"2","ASO та синк paid↔organic","Захищаю і ростю органічний ранг")
    bullets(s,[
    ("Метадата: топ generic-head → Subtitle; feature-терміни → Keyword field; Title = TouchRetouch + топ-категорійний термін.",0),
    ("Бренди конкурентів — бідю лише в ASA, тримаю поза метадатою (trademark).",1),
    ("Halo: платна install velocity піднімає органічний ранг по тому ж ключу → безкоштовні інстали зверху.",0),
    ("Канібалізація: бід по власному бренду частково платить за те, що органіка взяла б безкоштовно.",1),
    ("Міряю paid→organic: трекінг органічного рангу по ключу (AppTweak) до/після платного пушу.",0),
    ("Інкрементальність: brand-pause тест + geo-holdout, щоб виділити реальний інкремент платки.",1),
    ("Дефолтна сторінка — теж ASO: PPO A/B на скрінах/іконці для росту install rate; CPP доповнює її під інтент.",0),
    ],Inches(1.4),Inches(1.75),Inches(11.4),Inches(5),size=15,gap=12)

    # S6 CPP
    s=slide(); head(s,"2","Custom Product Pages","3 концепти під теми ключів")
    data=[["CPP","Під які ключі","Що змінюється на сторінці","Метрика оцінки"],
    ["Object Cleanup","remove object, magic eraser","Before/after видалення; one-tap erase у preview","tap→install CR + trial-start"],
    ["AI Enhance / Retouch","photo enhancer, ai editor, retouch","Портрет-ретуш/енхенс; «AI в один тап»","CR + trial rate"],
    ["Competitor Switch","facetune, snapseed, picsart","«Все що вони, але швидше»; знайомі UI-патерни","CR з competitor + trial→paid"]]
    table(s,data,Inches(0.5),Inches(1.75),Inches(12.3),[Inches(2.4),Inches(3.2),Inches(4.2),Inches(2.5)],rowh=Inches(0.95),fs=12)
    t=tf(s,Inches(0.5),Inches(5.5),Inches(12.3),Inches(1))
    par(t.paragraphs[0],"Оцінюю передусім за tap→install CR (на що CPP впливає) та trial-start; зрештою — CPA(trial)/ROAS по CPP. Кожен CPP пришпилений до свого ad group, щоб креатив збігався з інтентом пошуку.",12,WM,italic=True,space=0)

    # S7 ROAS
    s=slide(); head(s,"3","Бюджет і ROAS","Шлях $35K → $70K при ≥125%")
    data=[["Фаза","Витрати","CPI","Інстали","Дохід","ROAS","Гейт"],
    ["M0 Базовий","$35K","$0.666","52.6K","$35.0K","100%","—"],
    ["M1 Банк ефект.","$35K","$0.560","62.5K","$41.6K","119%","білд"],
    ["M2 Гейт пройдено","$40K","$0.531","75.3K","$50.2K","125%","ТАК"],
    ["M3 Скейл","$55K","$0.528","104K","$69.4K","126%","ТАК"],
    ["Q2 Ціль","$70K","$0.525","133K","$88.8K","127%","ТАК"]]
    table(s,data,Inches(0.5),Inches(1.75),Inches(8.9),[Inches(2.2),Inches(1.1),Inches(1.2),Inches(1.3),Inches(1.3),Inches(1.0),Inches(0.8)],rowh=Inches(0.55),fs=12)
    t=tf(s,Inches(9.7),Inches(1.75),Inches(3.3),Inches(4.5))
    par(t.paragraphs[0],"Юніт-економіка",13,COR,bold=True,space=4,font="Georgia")
    for x in ["Дохід/інстал (рік) = 3% × $22.2 = $0.666","Беззбитк. CPI = $0.666","Цільовий CPI (125%) = $0.533"]:
        p=t.add_paragraph(); par(p,x,12,INK,space=4)
    p=t.add_paragraph(); par(p,"Спершу банкую ефективність (M1), потім масштабую в запас. Гейт беру на самому CPI — приріст воронки це апсайд.",12,WM,italic=True,space=4)
    t2=tf(s,Inches(0.5),Inches(5.6),Inches(12.3),Inches(1.3))
    par(t2.paragraphs[0],"Біддінг: старт від цільового CPA (CPT = CPA × CR); рухаю по downstream (trial/payer, не інстали); бренд — кап у факта.",13,INK,bold=True,space=4)
    p=t2.add_paragraph(); par(p,"Чутливість: ланцюг ROAS мультиплікативний → рівна еластичність. Пріоритет за headroom × контроль: CPT-ефективність (найшвидше), Тріал→Оплата (найбільший запас, 20%), tap→install CR (CPP/PPO).",12,COR,bold=True,space=0)

    # S8 measurement
    s=slide(); head(s,"4","Вимірювання","Зводжу 30% розрив; source of truth")
    bullets(s,[
    ("30% console>MMP: AdServices рахує redownloads і view-through, інше вікно; MMP дедуплікує, губить ATT/SKAN-null інстали, потребує SDK first-open.",0),
    ("Реконсиляція: єдине вікно атрибуції; AdServices API = source of truth по ASA-інсталах (детерміновано, переживає ATT); документований міст console→MMP щотижня.",0),
    ("Source of truth — ASA console: витрати, TTR, CPT, тапи + AdServices інстали.",1),
    ("MMP (AppsFlyer): атрибутовані інстали + downstream по каналах.",1),
    ("RevenueCat / Amplitude: тріали, платники, дохід, LTV, крива D30/рік.",1),
    ("Під ATT: AdServices детермінує ASA-інстали; SKAN conversion values — downstream (не-ATT); предиктив/blended — по доходу.",0),
    ("Тижневі KPI: витрати, TTR, CR, CPT, CPI, інстали (console vs MMP Δ%), CPA(trial), CPA(payer), Тріал→Оплата%, ROAS (D7 як сигнал + D30 гейт), органічний ранг топ-ключів, частка органіки.",0),
    ],Inches(1.4),Inches(1.75),Inches(11.4),Inches(5.2),size=13,gap=9)

    # S9 experiments
    s=slide(); head(s,"5","Беклог експериментів","Пріоритет за $-анлоком")
    data=[["Тест","Цільовий KPI","Success / Kill"],
    ["1 · Кап бренд-біда + pause-інкремент","Бренд incremental installs","Органіка бекфілить ≥70% → ріжу назавжди / Kill: органіка −>30%"],
    ["2 · Ізоляція Search Match + негативи","Generic CPA","CPA −15% при тому ж об'ємі / Kill: об'єм −>20%"],
    ["3 · Competitor у Search Results","CPA(trial)","CPA ≤ таргет, інкремент+ / Kill: CPA > generic ×1.5"],
    ["4 · CPP «Object Cleanup» vs дефолт","tap→install CR + trial","+10% CR стат-знач / Kill: нема лифта"],
    ["5 · PPO скрін-тест (дефолт)","Store install rate","+5% стат-знач / Kill: нема лифта"],
    ["6 · Гео-сплит T1 (ізоляція US)","US CPI","US CPI ≤ таргет / Kill: —"]]
    table(s,data,Inches(0.5),Inches(1.75),Inches(12.3),[Inches(4.4),Inches(3.0),Inches(4.9)],rowh=Inches(0.68),fs=12)

    # S10 90-day
    s=slide(); head(s,"6","План на 90 днів","0 → 30 → 60 → 90")
    cols=[("Дні 0–30 · Стабілізація",["Переходка від агентства: доступи, історія, звіти","Аудит + фікс вимірювання (AdServices/SKAN/MMP)","Quick wins: кап бренд-біда, ізоляція SM, пауза сміттєвих гео","1–2 low-risk фікси; ставлю репортинг"],COR),
    ("Дні 30–60 · Ребілд",["Жива архітектура: Brand/Core/Discovery/Competitor-SR/Feature","Перші CPP + PPO тести","Синк paid–organic по ключах","Розширення generic + competitor"],TL),
    ("Дні 60–90 · Скейл",["Масштабую в запас → ~$55K при ≥125%","Валідую CPP-переможців","План Q2 → $70K (бюджет, ключі, CPP, гео)"],RGBColor(0xB5,0x76,0x1A))]
    x=Inches(0.45)
    for name,items,c in cols:
        chip(s,x,Inches(1.75),Inches(4.05),name,c,h=Inches(0.55))
        t=tf(s,x,Inches(2.45),Inches(4.05),Inches(4.3))
        for i,it in enumerate(items):
            p=t.paragraphs[0] if i==0 else t.add_paragraph(); par(p,"•  "+it,13,INK,space=10)
        x+=Inches(4.25)
    t=tf(s,Inches(0.45),Inches(6.65),Inches(12.5),Inches(0.7))
    par(t.paragraphs[0],"Що треба від команди: креатив під 2–3 CPP · тули (AppTweak/ASOMobile, опц. SplitMetrics) · повноваження по бюджету + підпис ROAS-таргета · рішення CMO по риск-толерантності бренд-захисту та гео · колаборація з продуктом по пейволу (Тріал→Оплата).",12,WM,italic=True,space=0)

    # S11 risks
    s=slide(); head(s,"7","Ризики та припущення","На чому тримається модель")
    bullets(s,[
    ("Головне припущення: дохід на базі річного ARPPU (той самий базис, що й якір «~100%»). Реальний кеш на D30 = ROAS × коеф. визнання — взяти криву з RevenueCat.",0),
    ("Інкремент бренду: припускаю, що органіка підхопить більшість паузнутих інсталів. Ризик — конкуренти бідять по бренду. Мітигація: капнутий захисний бід + моніторинг.",0),
    ("Скейл: припускаю ~стабільний generic CPT при подвоєнні. Ризик — інфляція аукціону / ліміт US-об'єму → CPI росте → ROAS ламається. Мітигація: розширення ключів, приріст CR через CPP/PPO, гео-експансія.",0),
    ("Вимірювання: SKAN/ATT шум і затримка. Мітигація: AdServices + документована реконсиляція.",0),
    ("Зовнішнє: сезонність, бідінг конкурентів, ATT opt-in. Моніторю й переоцінюю щомісяця.",0),
    ],Inches(1.4),Inches(1.8),Inches(11.4),Inches(5),size=15,gap=15)

    # S12 close
    s=slide()
    band=s.shapes.add_shape(1,0,Inches(2.5),SW,Inches(2.4)); band.fill.solid(); band.fill.fore_color.rgb=TL; band.line.fill.background(); band.shadow.inherit=False
    t=tf(s,Inches(0.75),Inches(2.75),Inches(11.8),Inches(2))
    par(t.paragraphs[0],"Теза в одному реченні",13,WHT,bold=True,space=8)
    p=t.add_paragraph(); par(p,"Зрізаю зайве по бренду й гео, банкую запас по ROAS — і масштабую ефективний US generic та competitor у цей запас, виходячи на $70K при ≥125% до кінця Q2.",20,WHT,bold=True,space=0,font="Georgia")
    t2=tf(s,Inches(0.75),Inches(5.2),Inches(11.8),Inches(1))
    par(t2.paragraphs[0],"Файли: ця презентація · ROAS-модель (xlsx, редагована) · брифи експериментів + план вимірювання (doc).",13,WM,italic=True,space=0)

    prs.save(BASE+"TouchRetouch_презентація_UA.pptx"); print("deck UA ok", len(prs.slides._sldIdLst),"slides")

# =========================================================
# 3) DOC (UA, human memo voice)
# =========================================================
def build_doc():
    d=Document(); st=d.styles["Normal"]; st.font.name="Calibri"; st.font.size=DPt(10.5); st.font.color.rgb=DRGB(0x23,0x30,0x3B)
    def h1(t):
        p=d.add_paragraph(); r=p.add_run(t); r.bold=True; r.font.size=DPt(17); r.font.name="Georgia"; r.font.color.rgb=DRGB(0xC8,0x54,0x2F); return p
    def h2(t):
        p=d.add_paragraph(); r=p.add_run(t); r.bold=True; r.font.size=DPt(12.5); r.font.name="Georgia"; r.font.color.rgb=DRGB(0x23,0x30,0x3B)
        p.space_before=DPt(10); p.space_after=DPt(3); return p
    def para(t,italic=False,color=(0x23,0x30,0x3B),size=10.5):
        p=d.add_paragraph(); r=p.add_run(t); r.italic=italic; r.font.color.rgb=DRGB(*color); r.font.size=DPt(size); return p
    def bul(t,lead=None):
        p=d.add_paragraph(style="List Bullet")
        if lead: r=p.add_run(lead+": "); r.bold=True
        p.add_run(t); return p

    h1("TouchRetouch — брифи експериментів і план вимірювання")
    para("Це супровід до презентації та ROAS-моделі. Тут я розписав, у якому порядку тестуватиму канал і як міритиму iOS-дані під ATT. Пишу від першої особи — так, як реально вестиму роботу.", italic=True, color=(0x6E,0x6A,0x63))

    h2("Спершу про базис моделі")
    bul("дохід рахую на базі ARPPU за перший рік ($22.2, без комісії Apple). Дохід/інстал = 15% × 20% × $22.2 = $0.666.","Базис")
    bul("це той самий базис, що й якір завдання «~100% ROAS на 1-му місяці», тож «ROAS (гейт)» у моделі можна порівнювати з вимогою 125%.","Чому так")
    bul("реальний кеш на день 30 — лише частина річного; колонка «D30 кеш ROAS» довідкова, поки не заміню 0.45 на реальну криву D30/рік з RevenueCat.","Застереження")

    h1("Частина A — беклог експериментів")
    para("Пріоритезую за розкриттям доходу × впевненість × легкість (ICE). У кожного брифа — гіпотеза, дизайн, KPI, мінімальний час і критерії масштабувати/вбити. Вбиваю швидко, переможців масштабую.", italic=True, color=(0x6E,0x6A,0x63))
    exps=[
     ("EXP-1 · Кап бренд-біда + pause-тест інкрементальності  (Пріоритет: НАЙВИЩИЙ)",
      "Бренд — 58% витрат, макс. біди €25–35 при факті €1.2–1.9. Значна частина — трафік, який ми й так беремо органікою #1. Кап біда + pause-тест покажуть, скільки бренд-витрат реально інкрементальні.",
      "Капаю бренд-CPT до ~€2–3. Потім ставлю бренд на паузу на 1–2 тижні й дивлюся, скільки втрачених платних бренд-інсталів підхоплює органіка. Чисте вікно до/після, слідкую за бідінгом конкурентів по бренду.",
      "Бренд incremental installs; сумарні (paid+organic) бренд-інстали; блендовий CPI.",
      "2 тижні паузи (мін.) + 1 тиждень на зчитування.",
      "SUCCESS: органіка бекфілить ≥70% паузнутих → лишаю бренд-біди капнутими назавжди, звільнений бюджет у generic. KILL: органіка <50% АБО конкурент залив бренд → повертаю капнутий захисний бід."),
     ("EXP-2 · Ізоляція Search Match + флоу негативів  (Пріоритет: ВИСОКИЙ)",
      "Search Match (31%) крутиться в generic разом з exact-ключами й без негативів, тож канібалізує exact і працює наосліп на Maximize Conversions.",
      "Виношу Search Match в окремий Discovery. Додаю всі Core exact-ключі туди exact-негативами. Щотижня харвестю конвертні search-terms у Core.",
      "Generic CPA; % змарнованих витрат; нові ключі з харвесту.",
      "3–4 тижні (лаг SKAN-постбеків).",
      "SUCCESS: generic CPA −15% при рівному чи вищому об'ємі → роблю постійним. KILL: об'єм −>20% без виграшу в CPA → відкат/ребаланс."),
     ("EXP-3 · Competitor conquesting у Search Results  (Пріоритет: ВИСОКИЙ)",
      "Competitor крутиться лише на Product Pages (CPA €17 vs €0.75–2), а keyword-conquesting у Search Results — найінтентнішому плейсменті — немає взагалі.",
      "Запускаю Competitor у Search Results з exact-термінами конкурентів (facetune, snapseed, picsart, lightroom, youcam). Пришпилюю CPP «Competitor Switch». Product Pages competitor переробляю або ріжу.",
      "CPA(trial) з competitor; incremental installs; Тріал→Оплата на competitor-когорті.",
      "3–4 тижні.",
      "SUCCESS: CPA(trial) ≤ таргет з позитивним інкрементом → масштабую. KILL: CPA > generic × 1.5 без виграшу в об'ємі → лишаю лише найкращі терміни."),
     ("EXP-4 · CPP «Object Cleanup» vs дефолтна сторінка  (Пріоритет: СЕРЕДНЬО-ВИСОКИЙ)",
      "Інтент «remove object» обслуговує дефолтна сторінка, а не заточена. CPP під інтент має підняти tap→install CR.",
      "Показую CPP «Object Cleanup» (before/after видалення, one-tap erase у preview) на object-removal ad groups через ASA. Порівнюю з дефолтом на тих же термінах.",
      "tap→install CR; trial-start rate; CPA(trial) по сторінці.",
      "До ~9 000 показів/варіант або 2 тижні (для ~10% лифта при 80% power).",
      "SUCCESS: +10% CR (стат-знач) → викочую CPP на ці ad groups; будую наступний. KILL: нема лифта після цільових показів → ітерую креатив або знімаю."),
     ("EXP-5 · PPO A/B скріншотів на дефолтній сторінці  (Пріоритет: СЕРЕДНІЙ)",
      "Дефолтна сторінка конвертить І органіку, І paid-to-default; тест скрінів/іконки підіймає install rate по всьому трафіку.",
      "Запускаю Product Page Optimization: до 3 варіантів проти дефолта (ведучий скрін = готовий before/after; альт-герой; варіант іконки). Apple ділить трафік і рахує статистично.",
      "Store install rate (показ→інстал); downstream trial rate.",
      "До статзначущості (керує Apple), зазвичай 2–4 тижні.",
      "SUCCESS: +5% install rate (стат-знач) → промоую переможця в дефолт. KILL: нема лифта → лишаю дефолт, пробую сміливіший напрям."),
     ("EXP-6 · Гео-сплит T1_Generic (ізоляція US)  (Пріоритет: СЕРЕДНІЙ)",
      "T1_Generic мішає ~40 сторфронтів (US + UZ/KG) під одним бюджетом і бідом; дешеві сміттєві гео (TTR 4–5%) з'їдають бюджет, що мав би йти в US.",
      "Ділю T1_Generic по тирах гео; ізолюю US в окрему кампанію зі своїми бідами; низькоцінні гео — в окремі малобюджетні кампанії зі своїми таргетами або пауза.",
      "US CPI; блендовий CPI; змарновані витрати на sub-target гео.",
      "2–3 тижні.",
      "SUCCESS: ізольований US CPI ≤ таргет і блендовий CPI покращується → роблю постійним. KILL: н/д (структурна гігієна)."),
    ]
    for title,hyp,design,kpi,rt,crit in exps:
        h2(title); bul(hyp,"Гіпотеза"); bul(design,"Дизайн"); bul(kpi,"Цільовий KPI"); bul(rt,"Мін. час"); bul(crit,"Success / Kill")

    d.add_page_break()
    h1("Частина B — план вимірювання та атрибуції")
    h2("B.1 — Розрив 30% console vs MMP")
    para("Console показує ~30% більше інсталів за AppsFlyer. Ймовірні причини:")
    bul("AdServices (console) рахує redownloads і view-through, своє вікно атрибуції.","Бік завищення")
    bul("AppsFlyer дедуплікує, застосовує своє вікно, рахує лише інстали, де SDK спрацював на first-open — тож ATT-declined / SKAN-null / затримані постбеки й видалення-до-відкриття випадають.","Бік заниження")
    bul("Різниця tap-through vs view-through, таймзони/вікна, затримка й агрегація SKAN додають шуму.","Структурне")
    h2("B.2 — Як зводжу")
    bul("узгоджую ЄДИНЕ вікно атрибуції для console і MMP.")
    bul("AdServices API = source of truth по ASA-інсталах — детерміновано й переживає ATT, бо Apple володіє і стором, і рекламою.")
    bul("будую документований щотижневий міст: console інстали − redownloads − ATT/SKAN-null ≈ MMP. Слідкую за залишковим %; різкий стрибок = зламаний трекінг, а не зміна перформансу.")
    h2("B.3 — Source of truth по метриках")
    tbl=d.add_table(rows=1,cols=3); tbl.style="Light Grid Accent 2"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,t in enumerate(["Система","Які метрики","Нотатка"]): tbl.rows[0].cells[i].paragraphs[0].add_run(t).bold=True
    for a,b,c in [("ASA console","Витрати, покази, TTR, CPT, тапи, AdServices інстали","First-party; детермінована істина по ASA-інсталах під ATT"),
                  ("AppsFlyer (MMP)","Атрибутовані інстали + downstream по каналах","Крос-канальний вид; blend SKAN + AdServices"),
                  ("RevenueCat / Amplitude","Тріали, платники, дохід, ARPPU, LTV, крива D30/рік","Істина по доходу; годує ROAS-модель")]:
        cells=tbl.add_row().cells; cells[0].paragraphs[0].add_run(a); cells[1].paragraphs[0].add_run(b); cells[2].paragraphs[0].add_run(c)
    h2("B.4 — Читання iOS-даних під ATT / AdAttributionKit")
    bul("ASA-інстали: AdServices детермінована атрибуція — надійна на рівні ключа навіть при відмові ATT.")
    bul("Downstream (trial/purchase): SKAN / AdAttributionKit conversion values. Проектую CV-схему під етапи воронки (install → trial → purchase) або revenue-бакети; RevenueCat тригерить значення на подіях підписки.")
    bul("Обмеження: затримка постбеків + вікна (0–2 / 3–7 / 8–35 днів), агрегація (без user-level), пороги crowd-anonymity, що обнуляють дрібні джерела. Тому keyword-level дохід апроксимую вузькою структурою ad group, щоб campaign-level SKAN ≈ keyword-level.")
    bul("Де SKAN null (дрібні ключі): MMP предиктив/blended і оцінка по когорті (D7 як сигнал, D30 як гейт), а не по інсталах в моменті.")
    h2("B.5 — KPI тижневого звіту")
    for k in ["Витрати","Покази і TTR","CR (тап→інстал)","CPT і CPI","Інстали — console vs MMP Δ%","CPA(trial) і CPA(payer)","Тріал→Оплата %","ROAS — D7 (сигнал) і D30 (гейт)","Органічний ранг топ-ключів (синк paid–organic)","Частка органічних інсталів","Частка захищеного бренд-трафіку"]:
        bul(k)

    d.save(BASE+"TouchRetouch_експерименти_вимірювання_UA.docx"); print("doc UA ok")

build_xlsx(); build_deck(); build_doc()
print("ALL UA FILES BUILT")
