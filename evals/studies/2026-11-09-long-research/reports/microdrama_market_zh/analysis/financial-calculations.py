"""Arithmetic derived from cited financial disclosures; no model/API calls."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parent
rows=[
('中文在线','2023FY',1408856639.30,None,None,89436870.73,-10103602.49,'CP12 p14; CP13'),
('中文在线','2024FY',1159119215.32,776803695.12,464924899.04,-242889520.02,-52489977.76,'MD012 p30,32; CP12 p14'),
('中文在线','2025FY',1656556589.87,1057239561.26,953175245.88,-670952196.55,-203747067.16,'CP12 p14,32,35'),
('中文在线','2025H1',556485926.04,379127497.44,266109615.45,-226387147.68,-103873040.01,'MD005 p8,21'),
('中文在线','2026H1',577936358.23,291390980.25,254151375.14,-42995299.41,126801681.39,'MD005 p8,21'),
('中文在线','2026YTD9',832731834.90,443549017.24,384001060.45,-132051269.19,42795996.82,'CP01 p2,10,11'),
('掌阅科技','2023FY',2778391268.14,None,None,34844277.76,338409256.80,'CP14 p6,7'),
('掌阅科技','2024FY',2583300230.95,687614866.40,1500189659.01,49291684.29,-75017023.96,'CP14 p6,7,16'),
('掌阅科技','2025FY',3242735278.10,1002002285.45,2078568856.21,-176453565.92,-232536405.65,'CP14 p6,7,16'),
('掌阅科技','2025H1',1526069549.77,444009542.43,1087904808.49,-160141782.55,-227179863.43,'MD008 p6,12'),
('掌阅科技','2026H1',1783793670.53,613002054.27,1108896945.96,-50141750.04,-116528498.87,'MD008 p6,12'),
('掌阅科技','2026YTD9',2775336619.06,873951114.55,1781769896.88,-68409069.35,52734303.86,'CP02 p1,10,13')]
out=[]
for company,period,revenue,cost,sales,net,cfo,source in rows:
    r=dict(company=company,period=period,revenue=revenue,cost=cost,sales_expense=sales,parent_net_income=net,operating_cash_flow=cfo,source=source)
    if cost is not None:
        r.update(gross_profit=revenue-cost,gross_margin_pct=(revenue-cost)/revenue*100,sales_ratio_pct=sales/revenue*100,gross_less_sales=revenue-cost-sales)
    out.append(r)
derived={}
for name in ('中文在线','掌阅科技'):
    h=[r for r in out if r['company']==name and r['period']=='2026H1'][0]
    q=[r for r in out if r['company']==name and r['period']=='2026YTD9'][0]
    derived[name+'_2026Q3']={k:q[k]-h[k] for k in ('revenue','cost','sales_expense','parent_net_income','operating_cash_flow')}
derived['COL_H1_working_capital_effect']=190687601.14-57420760.71-479405.69
derived['Palm_H1_working_capital_effect']=-121745548.23+56535093.65-192500.00
derived['Palm_2025_incremental_revenue']=3242735278.10-2583300230.95
derived['Palm_2025_incremental_gross_profit']=(3242735278.10-1002002285.45)-(2583300230.95-687614866.40)
derived['Palm_2025_incremental_sales_expense']=2078568856.21-1500189659.01
derived['COL_H1_segment_gross_profit']=411260317.48-211311776.05
derived['Palm_H1_advertising_sales_not_purchases']=771.55+24957927.46+129362.05+2289246.92+62001307.09
result={'unit':'CNY unless percentage','author':'/root/microdrama_research','rows':out,'derived':derived}
(ROOT/'financial-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'financial-results.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[-1]));w.writeheader();w.writerows(out)
print(json.dumps(result,ensure_ascii=False,indent=2))
