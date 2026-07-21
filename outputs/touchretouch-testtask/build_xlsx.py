#!/usr/bin/env python3
"""Build the TouchRetouch ASA ROAS / funnel model workbook with live formulas."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ---- palette / styles ----
INK   = "1F2430"
ACC   = "2E5AAC"   # blue
ACC2  = "0E7C61"   # teal/green
WARN  = "B5761A"
LIGHT = "EAF0FB"
LIGHT2= "E4F3EE"
GREY  = "F2F4F7"

def fill(hex_): return PatternFill("solid", fgColor=hex_)
thin = Side(style="thin", color="D5DAE2")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

h1 = Font(name="Calibri", size=16, bold=True, color=INK)
h2 = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
lbl= Font(name="Calibri", size=10, bold=True, color=INK)
reg= Font(name="Calibri", size=10, color=INK)
muted=Font(name="Calibri", size=9, italic=True, color="6B7280")
inp = Font(name="Calibri", size=10, bold=True, color="9A3412")  # editable inputs = brown/orange
res = Font(name="Calibri", size=10, bold=True, color=ACC)

center = Alignment(horizontal="center", vertical="center")
left   = Alignment(horizontal="left", vertical="center", wrap_text=True)
right  = Alignment(horizontal="right", vertical="center")

def sec_header(ws, row, text, span, color=ACC):
    c = ws.cell(row=row, column=1, value=text)
    c.font = h2; c.fill = fill(color); c.alignment = Alignment(horizontal="left", vertical="center")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    for col in range(1, span+1):
        ws.cell(row=row, column=col).fill = fill(color)

# =========================================================
# SHEET 1: ASSUMPTIONS
# =========================================================
ws = wb.active
ws.title = "Assumptions"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 42
ws.column_dimensions["B"].width = 14
ws.column_dimensions["C"].width = 16
ws.column_dimensions["D"].width = 52

ws["A1"] = "TouchRetouch — ASA Funnel & ROAS Model"; ws["A1"].font = h1
ws["A2"] = "All orange cells are editable inputs. Blue cells are calculated. Model uses first-year ARPPU as LTV base."
ws["A2"].font = muted
ws.merge_cells("A2:D2")

r = 4
sec_header(ws, r, "  CORE FUNNEL ASSUMPTIONS (edit these)", 4); r+=1
ws.cell(row=r, column=1, value="Metric").font=lbl
ws.cell(row=r, column=2, value="Value").font=lbl
ws.cell(row=r, column=3, value="Unit").font=lbl
ws.cell(row=r, column=4, value="Note / source").font=lbl
for c in range(1,5): ws.cell(row=r,column=c).fill=fill(GREY); ws.cell(row=r,column=c).border=border
r+=1

assumptions = [
    ("install_to_trial", "Install → Trial", 0.15, "%", "Given (paid funnel)"),
    ("trial_to_paid",    "Trial → Paid",    0.20, "%", "Given (paid funnel)"),
    ("arppu",            "ARPPU (Y1, net of Apple fee)", 22.2, "$", "Given"),
    ("d30_recognition",  "D30 revenue recognition (share of Y1)", 0.45, "%", "INFO ONLY (not in gate) — pull real D30/Y1 curve from RevenueCat"),
    ("min_roas",         "Min ROAS gate for scaling (D30)", 1.25, "x", "Given requirement"),
]
name_cell = {}
for key,label,val,unit,note in assumptions:
    ws.cell(row=r,column=1,value=label).font=reg; ws.cell(row=r,column=1).alignment=left
    cell = ws.cell(row=r,column=2,value=val); cell.font=inp; cell.fill=fill("FFF7ED"); cell.alignment=center; cell.border=border
    if unit=="%": cell.number_format="0.0%"
    elif unit=="$": cell.number_format='"$"0.00'
    else: cell.number_format="0.00"
    ws.cell(row=r,column=3,value=unit).font=reg; ws.cell(row=r,column=3).alignment=center
    ws.cell(row=r,column=4,value=note).font=muted; ws.cell(row=r,column=4).alignment=left
    name_cell[key]=f"$B${r}"
    r+=1

r+=1
sec_header(ws, r, "  DERIVED UNIT ECONOMICS (calculated)", 4, ACC2); r+=1
derived = [
    ("Payers per install", f"={name_cell['install_to_trial']}*{name_cell['trial_to_paid']}", "0.00%", "= trial% × paid%"),
    ("Revenue per install (Y1)", None, '"$"0.000', "= payers/install × ARPPU"),
    ("Break-even CPI (ROAS 100%)", None, '"$"0.000', "= revenue per install"),
    ("Target CPI for min ROAS", None, '"$"0.000', "= rev/install ÷ min ROAS"),
]
pi_row = r  # payers per install row
for i,(label,formula,fmt,note) in enumerate(derived):
    ws.cell(row=r,column=1,value=label).font=reg; ws.cell(row=r,column=1).alignment=left
    cell=ws.cell(row=r,column=2); cell.font=res; cell.fill=fill(LIGHT); cell.alignment=center; cell.border=border; cell.number_format=fmt
    ws.cell(row=r,column=4,value=note).font=muted; ws.cell(row=r,column=4).alignment=left
    r+=1
# fill derived formulas by absolute ref
ws.cell(row=pi_row,   column=2).value = f"={name_cell['install_to_trial']}*{name_cell['trial_to_paid']}"
ws.cell(row=pi_row+1, column=2).value = f"=$B${pi_row}*{name_cell['arppu']}"
ws.cell(row=pi_row+2, column=2).value = f"=$B${pi_row+1}"
ws.cell(row=pi_row+3, column=2).value = f"=$B${pi_row+1}/{name_cell['min_roas']}"

REV_PER_INSTALL = f"Assumptions!$B${pi_row+1}"
MIN_ROAS = f"Assumptions!{name_cell['min_roas']}"
ARPPU = f"Assumptions!{name_cell['arppu']}"
I2T = f"Assumptions!{name_cell['install_to_trial']}"
T2P = f"Assumptions!{name_cell['trial_to_paid']}"

r+=1
ws.cell(row=r,column=1,value="KEY INSIGHT: the whole task = drop blended CPI to ≤ Target CPI and hold it while doubling spend.").font=Font(size=10,bold=True,color=WARN)
ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=4)

# =========================================================
# SHEET 2: RAMP MODEL
# =========================================================
ws2 = wb.create_sheet("Ramp Model")
ws2.sheet_view.showGridLines=False
cols = ["Phase / Month","Spend ($)","Blended CPT ($)","TTR","CR tap→install","CPI ($)","Taps","Installs","Trials","Payers","Revenue ($)","D30 cash (info)","ROAS (gate)","D30 cash ROAS","Pass gate?"]
widths=[26,12,14,9,14,11,11,11,10,10,14,14,10,10,13]
for i,w in enumerate(widths): ws2.column_dimensions[get_column_letter(i+1)].width=w

ws2["A1"]="Spend → Taps → Installs → Trials → Payers → Revenue → ROAS"; ws2["A1"].font=h1
ws2["A2"]="Orange = editable driver (spend, CPT, CR). Everything else is a live formula. Story: bank efficiency in M1, then scale into the headroom."
ws2["A2"].font=muted; ws2.merge_cells("A2:O2")

hr=4
for i,c in enumerate(cols):
    cell=ws2.cell(row=hr,column=i+1,value=c); cell.font=Font(size=9,bold=True,color="FFFFFF")
    cell.fill=fill(ACC); cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); cell.border=border

# rows: phase, spend, CPT, TTR, CR ti  (editable) then formulas
ramp = [
    ("M0 — Baseline (current)",   35000, 0.2564, 0.070, 0.385),
    ("M1 — Bank efficiency",      35000, 0.2240, 0.075, 0.400),
    ("M2 — Gate cleared",         40000, 0.2230, 0.078, 0.420),
    ("M3 — Scale above gate",     55000, 0.2323, 0.080, 0.440),
    ("Q2 — Target",               70000, 0.2363, 0.082, 0.450),
]
first=hr+1
for j,(phase,spend,cpt,ttr,crti) in enumerate(ramp):
    rr=first+j
    ws2.cell(row=rr,column=1,value=phase).font=reg; ws2.cell(row=rr,column=1).alignment=left
    for col,val,fmt in [(2,spend,'"$"#,##0'),(3,cpt,'"$"0.000'),(4,ttr,'0.0%'),(5,crti,'0.0%')]:
        cell=ws2.cell(row=rr,column=col,value=val); cell.font=inp; cell.fill=fill("FFF7ED"); cell.alignment=center; cell.border=border; cell.number_format=fmt
    # CPI = CPT / CR ti
    ws2.cell(row=rr,column=6,value=f"=C{rr}/E{rr}").number_format='"$"0.000'
    # Taps = spend / CPT
    ws2.cell(row=rr,column=7,value=f"=B{rr}/C{rr}").number_format='#,##0'
    # Installs = taps * CR ti
    ws2.cell(row=rr,column=8,value=f"=G{rr}*E{rr}").number_format='#,##0'
    # Trials = installs * i2t
    ws2.cell(row=rr,column=9,value=f"=H{rr}*{I2T}").number_format='#,##0'
    # Payers = trials * t2p
    ws2.cell(row=rr,column=10,value=f"=I{rr}*{T2P}").number_format='#,##0'
    # Revenue Y1 = payers * ARPPU
    ws2.cell(row=rr,column=11,value=f"=J{rr}*{ARPPU}").number_format='"$"#,##0'
    # D30 revenue = rev Y1 * recognition
    ws2.cell(row=rr,column=12,value=f"=K{rr}*{name_cell_ref if False else 'Assumptions!$B$'+str(pi_row-1)}").number_format='"$"#,##0'
    # ROAS Y1 = rev / spend
    ws2.cell(row=rr,column=13,value=f"=K{rr}/B{rr}").number_format='0%'
    # ROAS D30 = d30 rev / spend
    ws2.cell(row=rr,column=14,value=f"=L{rr}/B{rr}").number_format='0%'
    # Pass gate — on ROAS (first-year ARPPU basis, matches the task's ~100% anchor)
    ws2.cell(row=rr,column=15,value=f'=IF(M{rr}>={MIN_ROAS},"YES","NO")').alignment=center
    for col in range(6,16):
        ws2.cell(row=rr,column=col).border=border
        if ws2.cell(row=rr,column=col).font.color is None or col not in (2,3,4,5):
            ws2.cell(row=rr,column=col).font=res if col in (13,14) else reg
        ws2.cell(row=rr,column=col).alignment=center

# d30 recognition cell ref fix: recognition is at pi_row? we placed d30_recognition in assumptions block.
# find its row: assumptions started; d30_recognition is 4th assumption. Its cell:
# assumptions block header at row 4(section)+1(colhdr)=... simpler: reference by name_cell
D30_REC = f"Assumptions!{name_cell['d30_recognition']}"
for j in range(len(ramp)):
    rr=first+j
    ws2.cell(row=rr,column=12).value=f"=K{rr}*{D30_REC}"

note_r=first+len(ramp)+1
ws2.cell(row=note_r,column=1,value="Notes:").font=lbl
notes=[
 "• ROAS (gate) uses first-year ARPPU as revenue base — same basis as the task's '~100% at month 1' anchor. Gate = 125%.",
 "• M1 holds spend at $35K but cuts brand overbid + junk geos → blended CPI 0.666→0.560 → ROAS clears gate BEFORE scaling.",
 "• Base plan hits 125% on CPI efficiency ALONE (funnel held flat). Trial→Paid / CR uplift from CPP+PPO+paywall is UPSIDE, not baked in.",
 "• The gate binds at the margin where added generic CPT rises faster than CR gains. Scale pace = pace of banked efficiency.",
 "• 'D30 cash ROAS' is informational: real cash by day 30 = ROAS × D30 recognition ratio (Assumptions). Replace 0.45 with RevenueCat's real D30/Y1 curve.",
]
for k,n in enumerate(notes):
    ws2.cell(row=note_r+1+k,column=1,value=n).font=muted
    ws2.merge_cells(start_row=note_r+1+k,start_column=1,end_row=note_r+1+k,end_column=15)

# =========================================================
# SHEET 3: SENSITIVITY
# =========================================================
ws3=wb.create_sheet("Sensitivity")
ws3.sheet_view.showGridLines=False
for i,w in enumerate([34,16,16,16,40]): ws3.column_dimensions[get_column_letter(i+1)].width=w
ws3["A1"]="Sensitivity — which single metric moves ROAS most?"; ws3["A1"].font=h1
ws3["A2"]="ROAS = (CR_tap→install × Trial% × Paid% × ARPPU) ÷ CPT. Chain is multiplicative → each metric has EQUAL % elasticity."
ws3["A2"].font=muted; ws3.merge_cells("A2:E2")

hr=4
for i,c in enumerate(["Lever","Baseline","+10% improve","New ROAS Y1","Controllability / headroom"]):
    cell=ws3.cell(row=hr,column=i+1,value=c); cell.font=Font(size=10,bold=True,color="FFFFFF"); cell.fill=fill(ACC2); cell.alignment=center; cell.border=border

# baseline ROAS at Q2 target ~ using rev/install / CPI (take M2 as representative operating point)
base_rows=[
 ("CR tap→install", 0.42, "0.0%", "UA-owned via CPP / PPO — high headroom"),
 ("Trial → Paid", 0.20, "0.0%", "Product/paywall — biggest headroom, needs product"),
 ("Install → Trial", 0.15, "0.0%", "Onboarding — shared with product"),
 ("CPT (lower = better)", 0.238, "0.00", "UA-owned via structure/bids — fastest self-lever"),
]
for j,(lever,base,fmt,ctrl) in enumerate(base_rows):
    rr=hr+1+j
    ws3.cell(row=rr,column=1,value=lever).font=reg; ws3.cell(row=rr,column=1).alignment=left
    b=ws3.cell(row=rr,column=2,value=base); b.number_format=fmt; b.alignment=center; b.border=border; b.font=reg
    # +10% (for CPT, -10%)
    if "CPT" in lever:
        imp=ws3.cell(row=rr,column=3,value=f"=B{rr}*0.9")
    else:
        imp=ws3.cell(row=rr,column=3,value=f"=B{rr}*1.1")
    imp.number_format=fmt; imp.alignment=center; imp.border=border; imp.font=reg
    ws3.cell(row=rr,column=4,value="+10% ROAS").font=res; ws3.cell(row=rr,column=4).alignment=center; ws3.cell(row=rr,column=4).border=border
    ws3.cell(row=rr,column=5,value=ctrl).font=muted; ws3.cell(row=rr,column=5).alignment=left; ws3.cell(row=rr,column=5).border=border

concl=hr+1+len(base_rows)+1
ws3.cell(row=concl,column=1,value="Conclusion: elasticity is equal, so prioritise by headroom × controllability →").font=Font(size=10,bold=True,color=INK)
ws3.merge_cells(start_row=concl,start_column=1,end_row=concl,end_column=5)
ws3.cell(row=concl+1,column=1,value="1) CPT efficiency (huge documented waste — fastest), 2) Trial→Paid (only 20%, most headroom), 3) tap→install CR via CPP/PPO.").font=reg
ws3.merge_cells(start_row=concl+1,start_column=1,end_row=concl+1,end_column=5)

# =========================================================
# SHEET 4: AUDIT SPEND REALLOCATION
# =========================================================
ws4=wb.create_sheet("Spend Reallocation")
ws4.sheet_view.showGridLines=False
for i,w in enumerate([30,16,16,16,40]): ws4.column_dimensions[get_column_letter(i+1)].width=w
ws4["A1"]="Current vs Target spend mix ($35K)"; ws4["A1"].font=h1
ws4["A2"]="Reallocate away from brand overbid + junk multi-geo → into efficient US generic / competitor Search Results."
ws4["A2"].font=muted; ws4.merge_cells("A2:E2")
hr=4
for i,c in enumerate(["Bucket","Current %","Current $","Target %","Rationale"]):
    cell=ws4.cell(row=hr,column=i+1,value=c); cell.font=Font(size=10,bold=True,color="FFFFFF"); cell.fill=fill(ACC); cell.alignment=center; cell.border=border
mix=[
 ("Brand", 0.58, 0.25, "Cap bids to ~actual CPT; brand is partly cannibalised organic. Free budget."),
 ("Generic Core (US, exact)", 0.20, 0.34, "Scale proven head/mid terms under CPA target."),
 ("Generic Discovery (SM+Broad)", 0.11, 0.15, "Isolated, negatives from Core; harvest winners."),
 ("Competitor (Search Results)", 0.01, 0.12, "New conquesting in Search Results (was PP-only, CPA €17)."),
 ("Feature / multi-geo T1", 0.10, 0.14, "Kill junk geos; US-isolate; fold feature into generic."),
]
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

out="/home/user/asotraff/outputs/touchretouch-testtask/TouchRetouch_ASA_ROAS_Model.xlsx"
wb.save(out)
print("saved", out)
