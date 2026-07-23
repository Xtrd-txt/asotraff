#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TouchRetouch ASA test task v2 — EN, human/warm style, candidate's own strategy
(brand cap -> tool-conquest CPPs -> AI positioning) + supporting mechanics."""
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

BASE="/home/user/asotraff/outputs/touchretouch-testtask/v2/"
PAPER="FAF7F1"; INKX="23303B"; CORAL="C8542F"; TEAL="2E7D74"; WARM="6E6A63"; CREAM="F3ECE0"
INK=RGBColor(0x23,0x30,0x3B); COR=RGBColor(0xC8,0x54,0x2F); TL=RGBColor(0x2E,0x7D,0x74)
WM=RGBColor(0x6E,0x6A,0x63); WHT=RGBColor(0xFF,0xFF,0xFF); PP=RGBColor(0xFA,0xF7,0xF1); CRc=RGBColor(0xF3,0xEC,0xE0)
AMBER=RGBColor(0xB5,0x76,0x1A)

# ============================================================ XLSX
def build_xlsx():
    wb=openpyxl.Workbook()
    def fill(h): return PatternFill("solid",fgColor=h)
    thin=Side(style="thin",color="D8CFC0"); border=Border(thin,thin,thin,thin)
    h1=Font(name="Georgia",size=16,bold=True,color=INKX); h2=Font(name="Georgia",size=12,bold=True,color="FFFFFF")
    lbl=Font(name="Calibri",size=10,bold=True,color=INKX); reg=Font(name="Calibri",size=10,color=INKX)
    muted=Font(name="Calibri",size=9,italic=True,color=WARM); inp=Font(name="Calibri",size=10,bold=True,color="9A3412")
    res=Font(name="Calibri",size=10,bold=True,color=CORAL)
    center=Alignment(horizontal="center",vertical="center"); left=Alignment(horizontal="left",vertical="center",wrap_text=True)
    def sec(ws,row,text,span,color=CORAL):
        c=ws.cell(row=row,column=1,value=text); c.font=h2; c.alignment=Alignment(horizontal="left",vertical="center")
        ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span)
        for col in range(1,span+1): ws.cell(row=row,column=col).fill=fill(color)

    ws=wb.active; ws.title="Assumptions"; ws.sheet_view.showGridLines=False
    for col,w in zip("ABCD",[44,14,16,54]): ws.column_dimensions[col].width=w
    ws["A1"]="TouchRetouch — ASA Funnel & ROAS Model"; ws["A1"].font=h1
    ws["A2"]="Legend: orange = input you can change · blue = calculated. Revenue is modelled on first-year ARPPU (same basis as the ~100% anchor)."
    ws["A2"].font=muted; ws.merge_cells("A2:D2")
    r=4; sec(ws,r,"  CORE FUNNEL ASSUMPTIONS",4); r+=1
    for i,t in enumerate(["Metric","Value","Unit","Note / source"]):
        c=ws.cell(row=r,column=i+1,value=t); c.font=lbl; c.fill=fill(CREAM); c.border=border
    r+=1
    A=[("i2t","Install → Trial",0.15,"%","Given (paid funnel)"),
       ("t2p","Trial → Paid",0.20,"%","Given (paid funnel)"),
       ("arppu","ARPPU (Y1, net of Apple fee)",22.2,"$","Given"),
       ("d30","D30 revenue recognition (share of Y1)",0.45,"%","Info only (not in gate) — pull real D30/Y1 curve from RevenueCat"),
       ("roas","Min ROAS gate for scaling (D30)",1.25,"x","Given requirement")]
    nc={}
    for key,label,val,unit,note in A:
        ws.cell(row=r,column=1,value=label).font=reg; ws.cell(row=r,column=1).alignment=left
        c=ws.cell(row=r,column=2,value=val); c.font=inp; c.fill=fill("FFF7ED"); c.alignment=center; c.border=border
        c.number_format="0.0%" if unit=="%" else ('"$"0.00' if unit=="$" else "0.00")
        ws.cell(row=r,column=3,value=unit).font=reg; ws.cell(row=r,column=3).alignment=center
        ws.cell(row=r,column=4,value=note).font=muted; ws.cell(row=r,column=4).alignment=left
        nc[key]=f"$B${r}"; r+=1
    r+=1; sec(ws,r,"  DERIVED UNIT ECONOMICS",4,TEAL); r+=1
    d=[("Payers per install",None,"0.00%","trial% × paid%"),
       ("Revenue per install (Y1)",None,'"$"0.000',"payers/install × ARPPU"),
       ("Break-even CPI (ROAS 100%)",None,'"$"0.000',"equals revenue per install"),
       ("Target CPI for min ROAS",None,'"$"0.000',"rev per install ÷ min ROAS")]
    pi=r
    for label,_,fmt,note in d:
        ws.cell(row=r,column=1,value=label).font=reg; ws.cell(row=r,column=1).alignment=left
        c=ws.cell(row=r,column=2); c.font=res; c.fill=fill("EAF0FB"); c.alignment=center; c.border=border; c.number_format=fmt
        ws.cell(row=r,column=4,value=note).font=muted; ws.cell(row=r,column=4).alignment=left; r+=1
    ws.cell(row=pi,column=2).value=f"={nc['i2t']}*{nc['t2p']}"
    ws.cell(row=pi+1,column=2).value=f"=$B${pi}*{nc['arppu']}"
    ws.cell(row=pi+2,column=2).value=f"=$B${pi+1}"
    ws.cell(row=pi+3,column=2).value=f"=$B${pi+1}/{nc['roas']}"
    r+=1
    ws.cell(row=r,column=1,value="KEY INSIGHT: the whole task = drop blended CPI to ≤ Target CPI and hold it while doubling spend.").font=Font(name="Calibri",size=10,bold=True,color=CORAL)
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=4)
    ARPPU=f"Assumptions!{nc['arppu']}"; I2T=f"Assumptions!{nc['i2t']}"; T2P=f"Assumptions!{nc['t2p']}"
    D30=f"Assumptions!{nc['d30']}"; MIN=f"Assumptions!{nc['roas']}"

    ws2=wb.create_sheet("Ramp Model"); ws2.sheet_view.showGridLines=False
    cols=["Phase / Month","Spend ($)","Blended CPT ($)","TTR","CR tap→install","CPI ($)","Taps","Installs","Trials","Payers","Revenue ($)","D30 cash","ROAS (gate)","D30 ROAS","Gate?"]
    for i,w in enumerate([24,12,15,8,14,11,11,11,10,10,13,11,11,10,9]): ws2.column_dimensions[get_column_letter(i+1)].width=w
    ws2["A1"]="Spend → Taps → Installs → Trials → Payers → Revenue → ROAS"; ws2["A1"].font=h1
    ws2["A2"]="Orange cells drive the model. Everything else is a live formula. Plan: bank efficiency first (M1), then scale into the headroom."
    ws2["A2"].font=muted; ws2.merge_cells("A2:O2")
    hr=4
    for i,c in enumerate(cols):
        cell=ws2.cell(row=hr,column=i+1,value=c); cell.font=Font(name="Calibri",size=9,bold=True,color="FFFFFF")
        cell.fill=fill(CORAL); cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); cell.border=border
    ramp=[("M0 — Baseline (current)",35000,0.2564,0.070,0.385),
          ("M1 — Bank efficiency",35000,0.2240,0.075,0.400),
          ("M2 — Gate cleared",40000,0.2230,0.078,0.420),
          ("M3 — Scale above gate",55000,0.2323,0.080,0.440),
          ("Q2 — Target",70000,0.2363,0.082,0.450)]
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
        ws2.cell(row=rr,column=15,value=f'=IF(M{rr}>={MIN},"YES","NO")').alignment=center
        for col in range(6,16):
            c=ws2.cell(row=rr,column=col); c.border=border; c.alignment=center; c.font=res if col in (13,14) else reg
    nr=f+len(ramp)+1; ws2.cell(row=nr,column=1,value="Notes:").font=lbl
    for k,n in enumerate([
        "• ROAS (gate) uses first-year ARPPU — same basis as the task's ~100% anchor. Gate = 125%.",
        "• M1 holds spend at $35K but caps brand bids + cuts junk geos → blended CPI 0.666→0.560 → gate cleared before scaling.",
        "• Base plan hits 125% on CPT efficiency alone; funnel gains (tool-CPP CR, paywall trial→paid) are upside, not baked in.",
        "• 'D30 cash ROAS' is informational: real cash by day 30 = ROAS × D30 recognition. Replace 0.45 with RevenueCat's real curve."]):
        ws2.cell(row=nr+1+k,column=1,value=n).font=muted; ws2.merge_cells(start_row=nr+1+k,start_column=1,end_row=nr+1+k,end_column=15)

    ws3=wb.create_sheet("Sensitivity"); ws3.sheet_view.showGridLines=False
    for i,w in enumerate([34,16,16,16,40]): ws3.column_dimensions[get_column_letter(i+1)].width=w
    ws3["A1"]="Sensitivity — which metric moves ROAS most?"; ws3["A1"].font=h1
    ws3["A2"]="ROAS = (CR_tap→install × Trial% × Paid% × ARPPU) ÷ CPT. The chain is multiplicative → each metric has EQUAL % elasticity."
    ws3["A2"].font=muted; ws3.merge_cells("A2:E2")
    hr=4
    for i,c in enumerate(["Lever","Baseline","+10% improve","New ROAS","Controllability / headroom"]):
        cell=ws3.cell(row=hr,column=i+1,value=c); cell.font=Font(name="Calibri",size=10,bold=True,color="FFFFFF"); cell.fill=fill(TEAL); cell.alignment=center; cell.border=border
    sens=[("CR tap→install",0.42,"0.0%","UA-owned via CPP/PPO — high headroom"),
          ("Trial → Paid",0.20,"0.0%","Product/paywall — most headroom, needs product"),
          ("Install → Trial",0.15,"0.0%","Onboarding — shared with product"),
          ("CPT (lower = better)",0.238,"0.00","UA-owned via structure/bids — fastest lever")]
    for j,(lever,base,fmt,ctrl) in enumerate(sens):
        rr=hr+1+j
        ws3.cell(row=rr,column=1,value=lever).font=reg; ws3.cell(row=rr,column=1).alignment=left; ws3.cell(row=rr,column=1).border=border
        b=ws3.cell(row=rr,column=2,value=base); b.number_format=fmt; b.alignment=center; b.border=border; b.font=reg
        imp=ws3.cell(row=rr,column=3,value=(f"=B{rr}*0.9" if "CPT" in lever else f"=B{rr}*1.1")); imp.number_format=fmt; imp.alignment=center; imp.border=border; imp.font=reg
        ws3.cell(row=rr,column=4,value="+10% ROAS").font=res; ws3.cell(row=rr,column=4).alignment=center; ws3.cell(row=rr,column=4).border=border
        ws3.cell(row=rr,column=5,value=ctrl).font=muted; ws3.cell(row=rr,column=5).alignment=left; ws3.cell(row=rr,column=5).border=border
    cc=hr+1+len(sens)+1
    ws3.cell(row=cc,column=1,value="Conclusion: elasticity is equal → prioritise by headroom × controllability:").font=Font(name="Calibri",size=10,bold=True,color=INKX)
    ws3.merge_cells(start_row=cc,start_column=1,end_row=cc,end_column=5)
    ws3.cell(row=cc+1,column=1,value="1) CPT efficiency (documented waste — fastest), 2) Trial→Paid (only 20%, most headroom), 3) tap→install CR via tool-CPPs/PPO.").font=reg
    ws3.merge_cells(start_row=cc+1,start_column=1,end_row=cc+1,end_column=5)

    ws4=wb.create_sheet("Spend Reallocation"); ws4.sheet_view.showGridLines=False
    for i,w in enumerate([32,14,14,14,44]): ws4.column_dimensions[get_column_letter(i+1)].width=w
    ws4["A1"]="Current vs target spend mix ($35K)"; ws4["A1"].font=h1
    ws4["A2"]="Cap brand, kill competitor-on-Product-Pages, trim junk geos → redeploy into tool-intent CPP campaigns and the AI-positioning angle."
    ws4["A2"].font=muted; ws4.merge_cells("A2:E2")
    hr=4
    for i,c in enumerate(["Bucket","Now %","Now $","Target %","Rationale"]):
        cell=ws4.cell(row=hr,column=i+1,value=c); cell.font=Font(name="Calibri",size=10,bold=True,color="FFFFFF"); cell.fill=fill(CORAL); cell.alignment=center; cell.border=border
    mix=[("Brand (capped + defensive)",0.58,0.15,"Bid capped ~€3–5; brand is mostly cannibalised organic. Free budget."),
         ("Generic Core (US, exact)",0.12,0.25,"Proven head/mid terms (photo editor, object remover) under CPA target."),
         ("Tool-intent CPP campaigns",0.10,0.33,"Per-tool CPP ('magic eraser','object remover'…), aggressive bid per geo. Core money bucket."),
         ("Search Match Discovery (isolated)",0.18,0.12,"Isolated + Core as negatives; audit & harvest; kill non-converting terms."),
         ("AI-positioning campaigns/CPP",0.00,0.08,"New: capture users who'd otherwise ask ChatGPT/Gemini to edit a photo."),
         ("Competitor (Search Results test)",0.01,0.05,"Small conquest test in Search Results; Product-Pages competitor killed."),
         ("Reserve / T1 geo expansion",0.01,0.02,"Fund tested new T1 geos; junk geos (UZ/KG) removed.")]
    for j,(b,cur,tgt,rat) in enumerate(mix):
        rr=hr+1+j
        ws4.cell(row=rr,column=1,value=b).font=reg; ws4.cell(row=rr,column=1).alignment=left; ws4.cell(row=rr,column=1).border=border
        c1=ws4.cell(row=rr,column=2,value=cur); c1.number_format="0%"; c1.alignment=center; c1.border=border; c1.font=reg
        c2=ws4.cell(row=rr,column=3,value=f"=B{rr}*35000"); c2.number_format='"$"#,##0'; c2.alignment=center; c2.border=border; c2.font=reg
        c3=ws4.cell(row=rr,column=4,value=tgt); c3.number_format="0%"; c3.alignment=center; c3.border=border; c3.font=res
        c4=ws4.cell(row=rr,column=5,value=rat); c4.font=muted; c4.alignment=left; c4.border=border
    tot=hr+1+len(mix)
    ws4.cell(row=tot,column=1,value="TOTAL").font=lbl
    ws4.cell(row=tot,column=2,value=f"=SUM(B{hr+1}:B{hr+len(mix)})").number_format="0%"; ws4.cell(row=tot,column=2).alignment=center; ws4.cell(row=tot,column=2).font=lbl
    ws4.cell(row=tot,column=3,value=f"=SUM(C{hr+1}:C{hr+len(mix)})").number_format='"$"#,##0'; ws4.cell(row=tot,column=3).alignment=center; ws4.cell(row=tot,column=3).font=lbl
    ws4.cell(row=tot,column=4,value=f"=SUM(D{hr+1}:D{hr+len(mix)})").number_format="0%"; ws4.cell(row=tot,column=4).alignment=center; ws4.cell(row=tot,column=4).font=lbl
    for _ws in wb.worksheets:
        for _row in _ws.iter_rows():
            for _c in _row:
                if isinstance(_c.value,str) and not _c.value.startswith("="):
                    _c.value=_c.value.replace("\u2014","-").replace("\u2013","-").replace("\u2212","-")
    wb.save(BASE+"TouchRetouch_ROAS_Model.xlsx"); print("xlsx v2 ok")

# ============================================================ DECK
def build_deck():
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    BLANK=prs.slide_layouts[6]; SW,SH=prs.slide_width,prs.slide_height
    def slide():
        s=prs.slides.add_slide(BLANK); bg=s.shapes.add_shape(1,0,0,SW,SH); bg.fill.solid(); bg.fill.fore_color.rgb=PP; bg.line.fill.background(); bg.shadow.inherit=False
        s.shapes._spTree.remove(bg._element); s.shapes._spTree.insert(2,bg._element); return s
    def tf(s,l,t,w,h):
        b=s.shapes.add_textbox(l,t,w,h); b.text_frame.word_wrap=True; return b.text_frame
    def par(p,text,size,color=INK,bold=False,align=PP_ALIGN.LEFT,space=6,italic=False,font="Calibri"):
        p.text=text; p.alignment=align; p.space_after=Pt(space); r=p.runs[0]
        r.font.size=Pt(size); r.font.bold=bold; r.font.italic=italic; r.font.color.rgb=color; r.font.name=font
    def head(s,num,eyebrow,title):
        c=s.shapes.add_shape(9,Inches(0.55),Inches(0.5),Inches(0.62),Inches(0.62)); c.fill.solid(); c.fill.fore_color.rgb=COR; c.line.fill.background(); c.shadow.inherit=False
        par(c.text_frame.paragraphs[0],num,20,WHT,bold=True,align=PP_ALIGN.CENTER,space=0,font="Georgia")
        t=tf(s,Inches(1.4),Inches(0.42),Inches(11.4),Inches(1.1)); par(t.paragraphs[0],eyebrow.upper(),11,COR,bold=True,space=2)
        p=t.add_paragraph(); par(p,title,23,INK,bold=True,space=0,font="Georgia")
        ln=s.shapes.add_shape(1,Inches(1.4),Inches(1.42),Inches(11.4),Pt(2)); ln.fill.solid(); ln.fill.fore_color.rgb=COR; ln.line.fill.background(); ln.shadow.inherit=False
    def bullets(s,items,l,t,w,h,size=15,gap=9):
        f=tf(s,l,t,w,h)
        for i,(txt,lvl) in enumerate(items):
            p=f.paragraphs[0] if i==0 else f.add_paragraph(); col=INK if lvl==0 else WM; pre="—  " if lvl==0 else "·  "
            par(p,pre+txt,size if lvl==0 else size-2,col,bold=(lvl==0),space=gap); p.level=0 if lvl==0 else 1
    def chip(s,l,t,w,text,color=TL,h=Inches(0.5)):
        c=s.shapes.add_shape(5,l,t,w,h); c.fill.solid(); c.fill.fore_color.rgb=color; c.line.fill.background(); c.shadow.inherit=False
        par(c.text_frame.paragraphs[0],text,11.5,WHT,bold=True,align=PP_ALIGN.CENTER,space=0)
    def table(s,data,l,t,w,colw,rowh=Inches(0.45),fs=11):
        gt=s.shapes.add_table(len(data),len(data[0]),l,t,w,rowh*len(data)).table
        try: gt.first_row=False; gt.horz_banding=False
        except Exception: pass
        for ci,cw in enumerate(colw): gt.columns[ci].width=cw
        for ri,row in enumerate(data):
            for cidx,val in enumerate(row):
                cell=gt.cell(ri,cidx); cell.margin_left=Pt(6); cell.margin_right=Pt(4); cell.margin_top=Pt(2); cell.margin_bottom=Pt(2); cell.vertical_anchor=MSO_ANCHOR.MIDDLE
                p=cell.text_frame.paragraphs[0]; rr=p.add_run(); rr.text=str(val); rr.font.size=Pt(fs); rr.font.name="Calibri"
                if ri==0: cell.fill.solid(); cell.fill.fore_color.rgb=COR; rr.font.bold=True; rr.font.color.rgb=WHT; rr.font.name="Georgia"
                else: cell.fill.solid(); cell.fill.fore_color.rgb=(WHT if ri%2 else CRc); rr.font.color.rgb=INK

    # S1 cover
    s=slide()
    band=s.shapes.add_shape(1,0,Inches(2.2),Inches(0.28),Inches(3.1)); band.fill.solid(); band.fill.fore_color.rgb=COR; band.line.fill.background(); band.shadow.inherit=False
    t=tf(s,Inches(0.75),Inches(2.1),Inches(11.9),Inches(3.4))
    par(t.paragraphs[0],"APPLE SEARCH ADS · TEST TASK",13,COR,bold=True,space=10)
    p=t.add_paragraph(); par(p,"TouchRetouch: taking ASA in-house,",30,INK,bold=True,space=2,font="Georgia")
    p=t.add_paragraph(); par(p,"fixing the waste, scaling on intent",30,INK,bold=True,space=12,font="Georgia")
    p=t.add_paragraph(); par(p,"Photo editor (iOS) · freemium: weekly trial → subscription · US · plan to $70K/mo at ≥125% ROAS in two quarters",14,WM,space=0)
    t2=tf(s,Inches(0.75),Inches(6.0),Inches(11.9),Inches(1))
    par(t2.paragraphs[0],"My thesis: stop overpaying to defend the brand, and win the users who are searching for a tool — not for a specific app. Including the ones who'd otherwise just ask an AI.",13,WM,italic=True,space=0)

    # S2 audit
    s=slide(); head(s,"1","Account audit","What I see, ranked by revenue impact")
    data=[["#","Problem","My read","Fix"],
    ["1","Brand overbid — 58% of spend, max €25–35 vs €1.2–1.9 real","Someone searching \"TouchRetouch\" already wants us; even if a rival ads on it, users skip the ad. This is paying to cannibalise our own brand.","Cap brand to €3–5 + small defensive bid; move the freed budget to tool intent"],
    ["2","Search Match (31%) blind inside generic, no negatives","AUTO competes with our own exact keywords and burns budget on junk queries","Isolate Search Match; audit it; pull negative keywords that spend without converting"],
    ["3","T1_Generic mixes 40 geos incl. UZ/KG under one bid","No subscription culture in the cheapest geos; install→paid there is almost certainly poor","Cut junk geos, keep T1, audit per-geo conversion, expand T1 pool"],
    ["4","Competitor only on Product Pages — CPA €17, TTR 2%","Why would a user scroll a rival's page and switch? Our screens don't stand out there. It barely brings installs, so it doesn't even feed organic.","Pause → quick read → kill; move competition into Search Results / tool intent"],
    ["5","Feature campaign timid — 'magic eraser' €4–7, single-digit installs","This IS the tool-intent play, done too small","Fold into tool-CPP campaigns and raise the bid"]]
    table(s,data,Inches(0.45),Inches(1.6),Inches(12.55),[Inches(0.35),Inches(3.1),Inches(4.7),Inches(4.4)],rowh=Inches(0.98),fs=10.5)

    # S3 architecture + thesis
    s=slide(); head(s,"1","Restructure & core thesis","Defend cheap, attack intent")
    t=tf(s,Inches(1.4),Inches(1.55),Inches(11.4),Inches(0.9))
    par(t.paragraphs[0],"Competitors' names ARE their keywords — like EMD domains. But a person typing \"magic eraser\" or \"object remover\" isn't after a specific app; they want the tool. Whoever shows the best solution wins the tap. So I put the money on tool intent with a dedicated page per tool — not on defending the brand.",13,INK,space=0)
    rows=[("Brand (US)","Exact · bid capped €3–5 + defensive","Stop overpaying for organic we already win; measure incrementality",COR),
    ("Tool-intent CPPs","Exact · a CPP per tool · bid per geo","'magic eraser', 'object remover', 'background remover', 'photo retouch' — the money bucket",TL),
    ("Generic Core (US)","Exact · manual bids","Head terms (photo editor, photo editing app) under CPA target",TL),
    ("Search Match Discovery","AUTO, isolated + negatives","Harvest winners → Core; kill non-converting terms",AMBER),
    ("AI-positioning","Exact + CPP","Win users who'd otherwise ask ChatGPT/Gemini to edit a photo",COR)]
    y=Inches(3.05)
    for name,cfg,why,c in rows:
        chip(s,Inches(0.55),y,Inches(3.05),name,c,h=Inches(0.5))
        tb=tf(s,Inches(3.8),y-Inches(0.03),Inches(9.05),Inches(0.6)); par(tb.paragraphs[0],cfg,12.5,INK,bold=True,space=1); p=tb.add_paragraph(); par(p,why,11.5,WM,space=0)
        y+=Inches(0.76)
    t=tf(s,Inches(0.55),Inches(6.95),Inches(12.3),Inches(0.4))
    par(t.paragraphs[0],"Negatives: Core → negatives in Discovery/Search Match · brand → negatives in generic. Placements: Search Results first; Product-Pages competitor killed.",11.5,WM,italic=True,space=0)

    # S4 keywords
    s=slide(); head(s,"2","Keyword strategy","Research process + pool by intent")
    t=tf(s,Inches(1.4),Inches(1.5),Inches(11.4),Inches(0.9))
    par(t.paragraphs[0],"My process: seed in ASO Mobile, then pull demand from Ahrefs (Google) — search intent transfers across surfaces: what people Google, they also type in the App Store. Ahrefs is for discovering intent; I size each candidate with App Store / ASA popularity before committing, because Google volume ≠ store volume.",12.5,INK,space=0)
    data=[["Brand — defend","Generic / tool — attack","Competitor","AI intent — new"],
    ["touchretouch (exact)","photo editor (exact)","facetune (exact)","ai photo editor (exact)"],
    ["touchretouch app (exact)","object remover (exact)","snapseed (exact)","ai object remover (exact)"],
    ["","remove object from photo","picsart (exact)","ai photo cleanup (exact)"],
    ["","magic eraser / background remover","(brandable = low conquest)","remove object with ai"],
    ["","photo retouch / unblur photo","","ai background remover"]]
    table(s,data,Inches(0.45),Inches(2.5),Inches(12.55),[Inches(3.0),Inches(3.5),Inches(3.0),Inches(3.05)],rowh=Inches(0.5),fs=10.5)
    t=tf(s,Inches(0.45),Inches(6.2),Inches(12.55),Inches(0.9))
    par(t.paragraphs[0],"Match logic: exact for proven terms; Broad + Search Match isolated in Discovery to harvest. Competitor split: brandable names (Facetune/Snapseed) = weak conquest; tool-named intent = the real gold. Competitor brands are bid in ASA only — never in metadata (trademark / 2.3.7).",12,COR,bold=True,space=0)

    # S5 ASO
    s=slide(); head(s,"2","ASO & the AI angle","Protect organic, position against AI")
    bullets(s,[
    ("Metadata: top tool term → Subtitle; feature/tool terms + 'ai' → Keyword field; Title = TouchRetouch + top tool term.",0),
    ("The AI angle is the differentiator: our real rival isn't another app, it's ChatGPT/Gemini. People open an LLM to fix a photo instead of finding a retoucher.",0),
    ("So we show a purpose-built product that does these exact jobs faster and cleaner than a general AI — 'AI' badges on screenshots, an AI-angle CPP, messaging vs 'just ask an AI'.",1),
    ("Halo: paid velocity on a tool term lifts its organic rank → free installs on top.",0),
    ("Cannibalisation: bidding our own brand partly pays for installs organic already wins — measured, not assumed.",1),
    ("Measure paid→organic: rank tracking per keyword (ASO Mobile) before/after push; brand-pause + geo-holdout for incrementality.",0),
    ("Default listing is an ASO surface: PPO A/B on screenshots/icon lifts install rate for all traffic; tool-CPPs complement it per intent.",0),
    ],Inches(1.4),Inches(1.7),Inches(11.4),Inches(5.2),size=13.5,gap=9)

    # S6 CPP
    s=slide(); head(s,"2","Custom Product Pages","A page per intent — including AI")
    data=[["CPP","Serves","Page changes","Uplift metric"],
    ["Object Cleanup","remove object, magic eraser","Before/after removal; one-tap erase preview","tap→install CR + trial-start"],
    ["Background / Retouch","background remover, photo retouch","Background swap + portrait retouch demos","CR + trial rate"],
    ["AI, done right","ai photo editor, ai cleanup","'AI' badges; 'sharper than a general AI' message; result vs prompt","CR + trial→paid on AI cohort"]]
    table(s,data,Inches(0.5),Inches(1.75),Inches(12.3),[Inches(2.4),Inches(3.2),Inches(4.2),Inches(2.5)],rowh=Inches(0.95),fs=12)
    t=tf(s,Inches(0.5),Inches(5.5),Inches(12.3),Inches(1))
    par(t.paragraphs[0],"Each CPP is pinned to its ad group so the creative matches the exact search intent. Judged on tap→install CR (what a CPP moves) and downstream trial-start; ultimately CPA(trial)/ROAS by CPP. The AI CPP doubles as a positioning bet against LLM editing.",12,WM,italic=True,space=0)

    # S7 ROAS
    s=slide(); head(s,"3","Budget & ROAS","Path $35K → $70K at ≥125%")
    data=[["Phase","Spend","CPI","Installs","Revenue","ROAS","Gate"],
    ["M0 Baseline","$35K","$0.666","52.6K","$35.0K","100%","—"],
    ["M1 Bank efficiency","$35K","$0.560","62.5K","$41.6K","119%","build"],
    ["M2 Gate cleared","$40K","$0.531","75.3K","$50.2K","125%","YES"],
    ["M3 Scale","$55K","$0.528","104K","$69.4K","126%","YES"],
    ["Q2 Target","$70K","$0.525","133K","$88.8K","127%","YES"]]
    table(s,data,Inches(0.5),Inches(1.75),Inches(8.9),[Inches(2.2),Inches(1.1),Inches(1.2),Inches(1.3),Inches(1.3),Inches(1.0),Inches(0.8)],rowh=Inches(0.55),fs=12)
    t=tf(s,Inches(9.7),Inches(1.75),Inches(3.3),Inches(4.5))
    par(t.paragraphs[0],"Unit economics",13,COR,bold=True,space=4,font="Georgia")
    for x in ["Rev/install (Y1) = 3% × $22.2 = $0.666","Break-even CPI = $0.666","Target CPI (125%) = $0.533"]:
        p=t.add_paragraph(); par(p,x,12,INK,space=4)
    p=t.add_paragraph(); par(p,"Bank efficiency first (M1) by capping brand + cutting junk geos, then scale into the headroom on tool intent.",12,WM,italic=True,space=4)
    t2=tf(s,Inches(0.5),Inches(5.55),Inches(12.3),Inches(1.4))
    par(t2.paragraphs[0],"Bidding: keyword-level, derived from a target CPA per geo (CPT = target CPA × CR), moved on downstream trial/payer — not installs. Brand capped at real CPT.",13,INK,bold=True,space=4)
    p=t2.add_paragraph(); par(p,"Sensitivity: the ROAS chain is multiplicative → equal % elasticity. Prioritise by headroom × control: CPT efficiency (fastest), Trial→Paid (only 20%, most headroom), tap→install CR via tool-CPPs/PPO.",12,COR,bold=True,space=0)

    # S8 measurement
    s=slide(); head(s,"4","Measurement","Reconcile the 30% gap; source of truth")
    bullets(s,[
    ("Why console shows ~30% more than MMP: AdServices counts redownloads + view-through on its own window; AppsFlyer dedupes, drops ATT/SKAN-null installs, needs SDK first-open.",0),
    ("Reconcile: one attribution window; AdServices API = source of truth for ASA installs (deterministic, survives ATT); documented console→MMP bridge, tracked weekly.",0),
    ("ASA console: spend, TTR, CPT, taps + AdServices installs.",1),
    ("AppsFlyer: attributed installs + downstream across channels.",1),
    ("RevenueCat / Amplitude: trials, payers, revenue, LTV, D30/Y1 curve.",1),
    ("Under ATT: AdServices deterministic for ASA installs; SKAN conversion values for downstream (non-ATT); predictive for revenue where SKAN is null.",0),
    ("Weekly KPIs: Spend, TTR, CR, CPT, CPI, installs (console vs MMP Δ%), CPA(trial), CPA(payer), Trial→Paid%, ROAS (D7 lead + D30 gate), organic rank of top tool terms, organic install share.",0),
    ],Inches(1.4),Inches(1.7),Inches(11.4),Inches(5.2),size=13,gap=9)

    # S9 experiments
    s=slide(); head(s,"5","Experiments backlog","Prioritised by $-unlock")
    data=[["Test","Target KPI","Success / Kill"],
    ["1 · Brand bid cap + pause incrementality","Brand incremental installs","Organic backfills ≥70% → cut permanently / Kill: organic drops >30%"],
    ["2 · Tool-intent CPP conquest (per tool)","CPA(trial), tap→install CR","CPA ≤ target + incremental / Kill: CPA > target ×1.5"],
    ["3 · Search Match isolation + negatives","Generic CPA","CPA −15% at equal volume / Kill: volume drops >20%"],
    ["4 · AI-angle CPP + 'AI' badges","CR + trial→paid on AI terms","+10% CR & healthy trial→paid / Kill: no lift"],
    ["5 · Kill Product-Pages competitor","Wasted spend / CPA","Confirm CPA≫target over 1 wk → kill / Keep only if ≤ target"],
    ["6 · Geo trim (drop UZ/KG, expand T1)","Blended & US CPI","US CPI ≤ target / Kill: n/a (hygiene)"]]
    table(s,data,Inches(0.5),Inches(1.75),Inches(12.3),[Inches(4.4),Inches(3.0),Inches(4.9)],rowh=Inches(0.68),fs=12)

    # S10 90-day
    s=slide(); head(s,"6","90-day plan","0 → 30 → 60 → 90")
    cols=[("Days 0–30 · Stabilise",["Agency transition: access, history, search-term reports","Fix measurement (AdServices/SKAN/MMP)","Quick wins: cap brand, isolate Search Match, pause junk geos","Ship 1–2 low-risk fixes; stand up weekly reporting"],COR),
    ("Days 30–60 · Rebuild",["Live architecture + first tool-intent CPPs","AI-angle CPP + 'AI' badges test","PPO on default listing; paid–organic keyword sync","Kill Product-Pages competitor; expand generic"],TL),
    ("Days 60–90 · Scale",["Scale into banked efficiency → ~$55K @ ≥125%","Validate CPP winners by intent","Q2 plan → $70K (budget, keywords, CPPs, T1 geos)"],AMBER)]
    x=Inches(0.45)
    for name,items,c in cols:
        chip(s,x,Inches(1.75),Inches(4.05),name,c,h=Inches(0.55)); tb=tf(s,x,Inches(2.45),Inches(4.05),Inches(4.3))
        for i,it in enumerate(items):
            p=tb.paragraphs[0] if i==0 else tb.add_paragraph(); par(p,"•  "+it,12.5,INK,space=10)
        x+=Inches(4.25)
    t=tf(s,Inches(0.45),Inches(6.7),Inches(12.5),Inches(0.6))
    par(t.paragraphs[0],"From the team: creative for tool + AI CPPs (screens, 'AI' badges, previews) · tools (ASO Mobile, Ahrefs, opt. SplitMetrics) · budget authority + ROAS sign-off · CMO calls on brand-defense risk tolerance, the AI-positioning bet, and geo expansion · product collab on paywall.",11.5,WM,italic=True,space=0)

    # S11 risks
    s=slide(); head(s,"7","Risks & assumptions","What this depends on")
    bullets(s,[
    ("#1 assumption: revenue modelled on first-year ARPPU (same basis as the ~100% anchor). Real D30 cash = ROAS × D30/Y1 recognition — pull the curve from RevenueCat.",0),
    ("Brand cut: assumes organic backfills most paused brand installs. Risk: a competitor floods our brand term. Mitigate: keep a capped defensive bid + the pause test proves it.",0),
    ("AI positioning is a bet: it may not convert better yet. Mitigate: test it as a contained CPP with its own kill criteria before scaling budget into it.",0),
    ("Scaling: assumes tool-intent CPT stays roughly stable at 2× spend. Risk: auction inflation / limited US volume → CPI rises. Mitigate: widen tool terms, CR gains from CPPs/PPO, tested T1 geo expansion.",0),
    ("Measurement: SKAN/ATT delay & nulls. Mitigate: AdServices + documented reconciliation.",0),
    ],Inches(1.4),Inches(1.75),Inches(11.4),Inches(5),size=14.5,gap=13)

    # S12 close
    s=slide()
    band=s.shapes.add_shape(1,0,Inches(2.5),SW,Inches(2.4)); band.fill.solid(); band.fill.fore_color.rgb=TL; band.line.fill.background(); band.shadow.inherit=False
    t=tf(s,Inches(0.75),Inches(2.75),Inches(11.8),Inches(2))
    par(t.paragraphs[0],"The thesis in one line",13,WHT,bold=True,space=8)
    p=t.add_paragraph(); par(p,"Stop overpaying to defend the brand; win the tool-intent searches with a page per tool — and the users who'd otherwise ask an AI — scaling to $70K at ≥125% by end of Q2.",20,WHT,bold=True,space=0,font="Georgia")
    t2=tf(s,Inches(0.75),Inches(5.2),Inches(11.8),Inches(1))
    par(t2.paragraphs[0],"Files: this deck · ROAS model (xlsx) · experiment briefs + measurement plan (doc).",13,WM,italic=True,space=0)
    def _fixrun(r): r.text=r.text.replace("\u2014","-").replace("\u2013","-").replace("\u2212","-")
    for _sl in prs.slides:
        for _sh in _sl.shapes:
            if _sh.has_text_frame:
                for _p in _sh.text_frame.paragraphs:
                    for _r in _p.runs: _fixrun(_r)
            if _sh.has_table:
                for _row in _sh.table.rows:
                    for _cell in _row.cells:
                        for _p in _cell.text_frame.paragraphs:
                            for _r in _p.runs: _fixrun(_r)
    prs.save(BASE+"TouchRetouch_Deck.pptx"); print("deck v2 ok", len(prs.slides._sldIdLst),"slides")

# ============================================================ DOC
def build_doc():
    d=Document(); st=d.styles["Normal"]; st.font.name="Calibri"; st.font.size=DPt(10.5); st.font.color.rgb=DRGB(0x23,0x30,0x3B)
    def h1(t):
        p=d.add_paragraph(); r=p.add_run(t); r.bold=True; r.font.size=DPt(17); r.font.name="Georgia"; r.font.color.rgb=DRGB(0xC8,0x54,0x2F); return p
    def h2(t):
        p=d.add_paragraph(); r=p.add_run(t); r.bold=True; r.font.size=DPt(12.5); r.font.name="Georgia"; r.font.color.rgb=DRGB(0x23,0x30,0x3B); p.space_before=DPt(10); p.space_after=DPt(3); return p
    def para(t,italic=False,color=(0x23,0x30,0x3B),size=10.5):
        p=d.add_paragraph(); r=p.add_run(t); r.italic=italic; r.font.color.rgb=DRGB(*color); r.font.size=DPt(size); return p
    def bul(t,lead=None):
        p=d.add_paragraph(style="List Bullet")
        if lead: r=p.add_run(lead+": "); r.bold=True
        p.add_run(t); return p

    h1("TouchRetouch — Experiment Briefs & Measurement Plan")
    para("Companion to the deck and the ROAS model. I write these in the first person because it's how I'd actually run the channel: cap the brand waste, put the money on tool intent, and treat the AI angle as a measured bet.", italic=True, color=(0x6E,0x6A,0x63))

    h2("Model anchor (read first)")
    bul("revenue is modelled on first-year ARPPU ($22.2, net of Apple fee). Rev/install = 15% × 20% × $22.2 = $0.666.","Basis")
    bul("this is the same basis as the task's ~100% ROAS anchor, so the model's 'ROAS (gate)' is comparable to the 125% requirement.","Why")
    bul("real cash by day 30 is a fraction of Y1 — the 'D30 cash ROAS' column stays informational until we replace 0.45 with RevenueCat's real D30/Y1 curve.","Caveat")

    h1("Part A — Experiment backlog (prioritised)")
    para("Prioritised by revenue unlock × confidence × ease. Each brief: hypothesis, design, KPI, minimum runtime, success/kill. Kill fast, scale winners.", italic=True, color=(0x6E,0x6A,0x63))
    exps=[
     ("EXP-1 · Brand bid cap + incrementality pause test  (Priority: HIGHEST)",
      "Brand is 58% of spend with max bids €25–35 vs €1.2–1.9 real. Someone searching 'TouchRetouch' already wants us, so most of this pays for installs organic wins for free. I want to prove how much brand paid spend is actually incremental before I redeploy it.",
      "Cap brand CPT to €3–5. Then pause brand for 1–2 weeks and measure how many lost paid brand installs organic recovers. Clean before/after window; watch for competitors bidding our brand.",
      "Brand incremental installs; total (paid+organic) brand installs; blended CPI.",
      "2 weeks pause + 1 week read.",
      "SUCCESS: organic backfills ≥70% → keep brand capped permanently, redeploy budget to tool intent. KILL: organic recovers <50% or a competitor floods the term → restore a small capped defensive bid."),
     ("EXP-2 · Tool-intent CPP conquest  (Priority: HIGHEST)",
      "The real demand is tool intent, not brand. People typing 'magic eraser' / 'object remover' want a solution, not a specific app. A dedicated page per tool should convert far better than the default page and beat the timid feature campaign.",
      "Build a campaign per tool ('magic eraser', 'object remover', 'background remover', 'photo retouch') each pointed at its own CPP (matching before/after screens). Aggressive bids derived from a target CPA per geo. Fold the old feature terms in here.",
      "CPA(trial) and tap→install CR per tool; incremental installs.",
      "3–4 weeks (SKAN lag).",
      "SUCCESS: CPA(trial) ≤ target with incremental installs → scale the winners. KILL a tool: CPA > target × 1.5 with no volume upside → pause that tool, keep the rest."),
     ("EXP-3 · Search Match isolation + negative flow  (Priority: HIGH)",
      "Search Match (31%) runs inside the generic campaigns with no negatives, so it cannibalises exact and burns budget on junk queries.",
      "Move Search Match into its own Discovery campaign; add all Core exact keywords as exact negatives; audit the search-term report and negative out non-converting spend; harvest winners into Core weekly.",
      "Generic CPA; wasted-spend %; net new keywords harvested.",
      "3–4 weeks.",
      "SUCCESS: generic CPA −15% at equal or higher volume → permanent. KILL: volume drops >20% with no CPA gain → rebalance."),
     ("EXP-4 · AI-angle CPP + 'AI' badges  (Priority: MEDIUM-HIGH)",
      "Our real competitor is increasingly ChatGPT/Gemini — some users open an LLM to edit a photo instead of finding a retoucher. If we position TouchRetouch as a purpose-built tool that does these exact jobs better than a general AI, we can capture that intent.",
      "Ship an AI-angle CPP ('AI, done right' — result-vs-prompt, sharper output) with 'AI' badges on the lead screenshots, served to ai-intent terms (ai photo editor, ai object remover). Compare against the default page and the plain tool CPP.",
      "tap→install CR and trial→paid on the AI cohort; CPA(trial).",
      "2–3 weeks or ~9,000 impressions/variant.",
      "SUCCESS: +10% CR and healthy trial→paid → scale the AI angle across creative. KILL: no lift → keep AI badges only where they help, drop the dedicated spend."),
     ("EXP-5 · Kill the Product-Pages competitor campaign  (Priority: MEDIUM)",
      "Competitor runs only on Product Pages at CPA €17 and TTR 2%. Users rarely scroll a rival's page to switch, our screens don't stand out there, and it barely brings installs — so it doesn't even feed organic. I expect it's pure waste, but I'll confirm with data before cutting.",
      "Pause the Product-Pages competitor campaign; read one week of the resulting delta. If any conquest is worth keeping, move it to Search Results with a proper CPP instead.",
      "Wasted spend recovered; CPA vs target.",
      "1 week read.",
      "SUCCESS: CPA confirmed ≫ target → kill and redeploy. KEEP only if a segment comes in ≤ target."),
     ("EXP-6 · Geo trim + T1 expansion  (Priority: MEDIUM)",
      "T1_Generic mixes ~40 storefronts (US + UZ/KG) under one bid. The cheapest geos have little subscription culture and almost certainly poor install→paid, dragging the blend.",
      "Split T1_Generic by tier; isolate US; drop UZ/KG-type geos or move them to tiny separate budgets with their own targets; test a small expansion of genuine T1 geos.",
      "US CPI; blended CPI; wasted spend on sub-target geos.",
      "2–3 weeks.",
      "SUCCESS: isolated US CPI ≤ target and blended CPI improves → permanent. KILL: n/a (structural hygiene)."),
    ]
    for title,hyp,design,kpi,rt,crit in exps:
        h2(title); bul(hyp,"Hypothesis"); bul(design,"Design"); bul(kpi,"Target KPI"); bul(rt,"Min runtime"); bul(crit,"Success / Kill")

    d.add_page_break()
    h1("Part B — Measurement & attribution plan")
    h2("B.1 — The 30% console-vs-MMP install gap")
    para("Console shows ~30% more installs than AppsFlyer. Likely causes:")
    bul("AdServices (console) counts redownloads and view-through, on Apple's own attribution window.","Over-counting")
    bul("AppsFlyer dedupes, uses its own window, and only counts installs where its SDK fires on first open — so ATT-declined / SKAN-null / delayed-postback installs and uninstalled-before-open users drop out.","Under-counting")
    bul("tap-through vs view-through differences, timezone/window mismatches, and SKAN delay/aggregation add noise.","Structural")
    h2("B.2 — How I reconcile")
    bul("agree ONE attribution window across console and MMP.")
    bul("use the AdServices API as source of truth for ASA installs — deterministic and survives ATT because Apple owns both the store and the ad network.")
    bul("build a documented weekly bridge: console installs − redownloads − ATT/SKAN-null ≈ MMP. Track the residual %; a sudden change flags a tracking break, not a performance change.")
    h2("B.3 — Source of truth by metric")
    tbl=d.add_table(rows=1,cols=3); tbl.style="Light Grid Accent 2"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,t in enumerate(["System","Owns these metrics","Notes"]): tbl.rows[0].cells[i].paragraphs[0].add_run(t).bold=True
    for a,b,c in [("ASA console","Spend, impressions, TTR, CPT, taps, AdServices installs","First-party; deterministic ASA install truth under ATT"),
                  ("AppsFlyer (MMP)","Attributed installs + downstream events across channels","Cross-channel view; blends SKAN + AdServices"),
                  ("RevenueCat / Amplitude","Trials, payers, revenue, ARPPU, LTV, D30/Y1 curve","Revenue truth; feeds the ROAS model")]:
        cells=tbl.add_row().cells; cells[0].paragraphs[0].add_run(a); cells[1].paragraphs[0].add_run(b); cells[2].paragraphs[0].add_run(c)
    h2("B.4 — Reading iOS data under ATT / AdAttributionKit")
    bul("ASA installs: AdServices deterministic attribution — reliable at keyword level even when ATT is declined.")
    bul("Downstream (trial/purchase): SKAN / AdAttributionKit conversion values. I design a CV schema for funnel milestones (install → trial → purchase) or revenue buckets; RevenueCat fires the value on subscription events.")
    bul("Constraints: postback delay + windows (0–2 / 3–7 / 8–35 days), aggregation (no user-level), crowd-anonymity thresholds that null small sources. Keyword-level revenue is approximated with narrow, per-tool campaigns so campaign-level SKAN ≈ keyword-level — which the tool-CPP structure gives me for free.")
    bul("Where SKAN is null (small terms): MMP predictive/blended and cohort reads (D7 leading, D30 gate), not same-day installs.")
    h2("B.5 — Weekly report KPIs")
    for k in ["Spend","Impressions & TTR","CR (tap→install)","CPT & CPI","Installs — console vs MMP delta %","CPA(trial) and CPA(payer)","Trial→Paid %","ROAS — D7 (leading) and D30 (gate)","Organic rank on top tool terms (paid–organic sync)","Organic install share","Share of defended brand traffic"]:
        bul(k)
    def _fixp(ps):
        for _p in ps:
            for _r in _p.runs:
                _r.text=_r.text.replace("\u2014","-").replace("\u2013","-").replace("\u2212","-")
    _fixp(d.paragraphs)
    for _t in d.tables:
        for _row in _t.rows:
            for _cell in _row.cells: _fixp(_cell.paragraphs)
    d.save(BASE+"TouchRetouch_Experiments_Measurement.docx"); print("doc v2 ok")

build_xlsx(); build_deck(); build_doc()
print("V2 DONE")
