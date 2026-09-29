# ---- Summary
sm=wb.create_sheet("Summary",1)
sm["A1"]="Priority list by topic code"; sm["A1"].font=Font(name=F,size=16,bold=True,color=NAVY)
lab=[("Source",'All'),("Exam",'All'),("Year from",2022),("Year to",2030)]
for i,(l,v) in enumerate(lab,3):
    sm.cell(i,1,l).font=Font(name=F,bold=True); c=sm.cell(i,2,v); c.fill=inp_fill; c.font=base
dv=DataValidation(type="list",formula1="=Lists!$D$2:$D$6"); sm.add_data_validation(dv); dv.add("B3")
dv=DataValidation(type="list",formula1="=Lists!$E$2:$E$4"); sm.add_data_validation(dv); dv.add("B4")
M=lambda col:f"Master!${col}$2:${col}${N}"
F_=f'{M("C")},IF($B$3="All","*",$B$3),{M("B")},">="&$B$5,{M("B")},"<="&$B$6'
ex=f'{M("D")},IF($B$4="All","*",$B$4)'
info=[("D3","Exam 1 papers included",f'=IF(OR($B$4="All",$B$4="Exam 1"),COUNTIFS({M("S")},1,{M("D")},"Exam 1",{F_}),0)'),
      ("D4","Exam 2 papers included",f'=IF(OR($B$4="All",$B$4="Exam 2"),COUNTIFS({M("S")},1,{M("D")},"Exam 2",{F_}),0)'),
      ("D5","Marks with success data",f'=SUMIFS({M("F")},{M("M")},"<>",{ex},{F_})'),
      ("D6","Average success rate (all topics)",f'=IFERROR((D5*0+SUMIFS({M("F")},{M("M")},"<>",{ex},{F_})-SUMIFS({M("Q")},{ex},{F_}))/SUMIFS({M("F")},{M("M")},"<>",{ex},{F_}),0.6)')]
for addr,label,f in info:
    r=int(addr[1:]); sm.cell(r,4,label).font=base; x=sm.cell(r,7,f); x.font=Font(name=F,bold=True)
sm["G6"].number_format="0%"
sm["A7"]="Yellow cells are filters. How often a topic appears uses every included paper; success rates come only from papers with published statistics (VCAA main exams). See README."; sm["A7"].font=Font(name=F,italic=True,size=9)
H=["Code","Area of study","Topic","Questions","Marks","Questions per sitting","Share of exam marks","Success rate","Marks behind success rate","Exam % lost per sitting","Rank","Priority tier","Calculate","Interpret","Construct","Technology"]
W=[8,24,52,10,8,10,10,9,10,11,7,24,9,9,9,10]
HR=9
for c,h in enumerate(H,1):
    x=sm.cell(HR,c,h); x.font=hdr_font; x.fill=hdr_fill; x.alignment=Alignment(wrap_text=True,vertical="center"); sm.column_dimensions[L(c)].width=W[c-1]
sm.row_dimensions[HR].height=45
first=HR+1; last=HR+len(CODES)
for i,(code,u,aos,topic) in enumerate(CODES):
    r=first+i; crit=f'{M("G")},$A{r},{ex},{F_}'
    sh=lambda e,n:f'IF(${n}>0,SUMIFS({M("F")},{M("G")},$A{r},{M("D")},"{e}",{F_})/SUMIFS({M("F")},{M("D")},"{e}",{F_}),0)'
    vals=[code,aos,topic,
      f'=COUNTIFS({crit})',
      f'=SUMIFS({M("F")},{crit})',
      f'=IFERROR(COUNTIFS({M("G")},$A{r},{M("D")},"Exam 1",{F_})/$G$3,0)*($G$3>0)+IFERROR(COUNTIFS({M("G")},$A{r},{M("D")},"Exam 2",{F_})/$G$4,0)*($G$4>0)',
      f'=IFERROR(({sh("Exam 1","G$3")}+{sh("Exam 2","G$4")})/(($G$3>0)+($G$4>0)),0)',
      f'=IF(I{r}>0,(I{r}-SUMIFS({M("Q")},{crit}))/I{r},$G$6)',
      f'=SUMIFS({M("F")},{M("M")},"<>",{crit})',
      f'=G{r}*(1-H{r})',
      f'=IF(D{r}=0,"",RANK(J{r},$J${first}:$J${last}))',
      f'=IF(D{r}=0,"Not yet examined (still examinable)",IF(K{r}<=9,"Must master",IF(K{r}<=20,"Should master","Know it")))']
    for t in ["C","I","K","T"]: vals.append(f'=COUNTIFS({crit},{M("K")},"{t}")')
    for c,v in enumerate(vals,1):
        x=sm.cell(r,c,v); x.font=base; x.border=Border(bottom=thin)
    sm.cell(r,6).number_format="0.0"; sm.cell(r,7).number_format="0.0%"; sm.cell(r,8).number_format="0%"; sm.cell(r,10).number_format="0.00%"
    sm.cell(r,8).comment=None
rng=f"L{first}:L{last}"
for txt,col in (("Must master","F8CBAD"),("Should master","FFE699"),("Know it","C6EFCE"),("Not yet","D9D9D9")):
    sm.conditional_formatting.add(rng,FormulaRule(formula=[f'LEFT(L{first},{len(txt)})="{txt}"'],fill=PatternFill("solid",fgColor=col)))
sm.conditional_formatting.add(f"H{first}:H{last}",ColorScaleRule(start_type="num",start_value=0.3,start_color="F8696B",mid_type="num",mid_value=0.55,mid_color="FFEB84",end_type="num",end_value=0.85,end_color="63BE7B"))
sm.conditional_formatting.add(f"J{first}:J{last}",ColorScaleRule(start_type="min",start_color="FFFFFF",end_type="max",end_color="F8696B"))
sm.conditional_formatting.add(f"I{first}:I{last}",CellIsRule(operator="lessThan",formula=["5"],font=Font(name=F,color="C00000",italic=True)))
ar=last+3
sm.cell(ar-1,1,"By area of study").font=Font(name=F,size=12,bold=True,color=NAVY)
for c,h in enumerate(["","Area of study","","Questions","Marks","Questions per sitting","Share of exam marks","Success rate","Marks behind success rate","Exam % lost per sitting"],1):
    if h: x=sm.cell(ar,c,h); x.font=hdr_font; x.fill=hdr_fill; x.alignment=Alignment(wrap_text=True)
for i,a in enumerate(["Data analysis","Recursion & financial modelling","Matrices","Networks & decision maths"]):
    r=ar+1+i; B_=lambda col:f'SUMIF($B${first}:$B${last},$B{r},{col}${first}:{col}${last})'
    sm.cell(r,2,a)
    for c,col in ((4,"$D"),(5,"$E"),(6,"$F"),(7,"$G"),(9,"$I"),(10,"$J")): sm.cell(r,c,f'={B_(col)}')
    sm.cell(r,8,f'=IFERROR(SUMPRODUCT(($B${first}:$B${last}=$B{r})*($I${first}:$I${last})*($H${first}:$H${last}))/I{r},"")')
    for c in range(2,11): sm.cell(r,c).font=base
    sm.cell(r,6).number_format="0.0"; sm.cell(r,7).number_format="0.0%"; sm.cell(r,8).number_format="0%"; sm.cell(r,10).number_format="0.0%"
sm.freeze_panes=f"D{HR+1}"
sm.auto_filter.ref=f"A{HR}:P{last}"

