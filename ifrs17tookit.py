# -*- coding: utf-8 -*-
# =============================================================================
#  AFRICAN ACTUARIAL CONSULTANTS — COMPREHENSIVE ACTUARIAL TOOLKIT
#  Main App with Multi-Page Navigation
#  Theme: Light Blue (#4A90D9), Black, White
#  Run:  streamlit run app.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date
import re

st.set_page_config(page_title="AAC Actuarial Toolkit", layout="wide", initial_sidebar_state="expanded")

# =============================================================================
#  CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Calisto MT', 'Georgia', serif; font-size: 11pt; }
    h1, h2, h3, h4, h5, h6, p, div, span, label { font-family: 'Calisto MT', 'Georgia', serif !important; }
    .header { background-color: #000000; padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #4A90D9; }
    .header .logo { color: #4A90D9; font-size: 1.5rem; font-weight: bold; }
    .nav-links a { color: #FFFFFF; margin-left: 2rem; text-decoration: none; font-weight: 500; }
    .nav-links a:hover { color: #4A90D9; }
    .hero { background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%); color: #FFFFFF; padding: 3rem 2rem; text-align: center; border-bottom: 3px solid #4A90D9; }
    .hero h1 { color: #4A90D9; font-size: 2.8rem; margin-bottom: 0.5rem; }
    .hero p { font-size: 1.2rem; max-width: 800px; margin: 0 auto; }
    .card { background-color: #F9F9F9; border: 1px solid #4A90D9; border-radius: 8px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1.5rem; text-align: center; transition: transform 0.2s; }
    .card:hover { transform: translateY(-3px); }
    .card h3 { color: #4A90D9; margin-top: 0; }
    .footer { background-color: #000000; color: #FFFFFF; text-align: center; padding: 1.5rem; border-top: 3px solid #4A90D9; margin-top: 3rem; }
    .footer a { color: #4A90D9; }
    .stButton > button { background-color: #4A90D9 !important; color: #FFFFFF !important; border: none !important; border-radius: 4px !important; font-weight: bold !important; padding: 0.75rem 1.5rem !important; width: 100% !important; font-family: 'Calisto MT', 'Georgia', serif !important; }
    .stButton > button:hover { background-color: #357ABD !important; color: #FFFFFF !important; }
    .section-container { background-color: #F9F9F9; border: 2px solid #4A90D9; border-radius: 10px; padding: 1.5rem; margin-bottom: 1.5rem; }
    .section-container h3 { color: #4A90D9; margin-top: 0; font-size: 1.2rem; font-weight: bold; }
    .breadcrumb { background-color: #F0F0F0; padding: 0.5rem 1rem; border-radius: 5px; margin-bottom: 1rem; font-size: 0.9rem; border-left: 3px solid #4A90D9; }
    .breadcrumb span { color: #4A90D9; font-weight: bold; }
    .stFileUploader { border: 2px dashed #4A90D9 !important; border-radius: 10px !important; padding: 1rem !important; }
    .data-check-info { background-color: #E3F2FD; border: 2px solid #4A90D9; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .data-check-warning { background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .data-check-error { background-color: #FFEBEE; border: 2px solid #F44336; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .data-check-success { background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .dataframe { border: 1px solid #4A90D9 !important; border-radius: 8px !important; overflow: hidden !important; }
    .stSelectbox [data-baseweb="select"], .stMultiSelect [data-baseweb="select"] { border: 1px solid #4A90D9 !important; border-radius: 4px !important; }
    .required-container { background-color: #F9F9F9; border: 2px solid #4A90D9; border-radius: 10px; padding: 1rem; text-align: center; min-height: 120px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; }
    .required-container h3 { color: #4A90D9; font-size: 1.2rem; font-weight: bold; }
    .required-container p { color: #666666; font-size: 0.85rem; }
    .grouping-container { background-color: #F9F9F9; border: 2px solid #4A90D9; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .grouping-container h3 { color: #4A90D9; font-size: 1.2rem; font-weight: bold; }
    .main-container { max-width: 1400px; margin: 2rem auto; padding: 0 2rem; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
#  SESSION STATE & NAVIGATION
# =============================================================================

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'breadcrumb' not in st.session_state: st.session_state.breadcrumb = ['Home']

def navigate_to(page, breadcrumb_label=None):
    st.session_state.page = page
    if breadcrumb_label: st.session_state.breadcrumb = breadcrumb_label

def go_home():
    st.session_state.page = 'home'; st.session_state.breadcrumb = ['Home']

# =============================================================================
#  HEADER & BREADCRUMB
# =============================================================================

st.markdown('<div class="header"><div class="logo">AAC Actuarial Toolkit</div><div class="nav-links"><a href="javascript:void(0)" onclick="window.location.reload()">Home</a></div></div>', unsafe_allow_html=True)

def show_breadcrumb():
    if len(st.session_state.breadcrumb) > 1 or st.session_state.breadcrumb[0] != 'Home':
        bc = " > ".join([f"<span>{b}</span>" for b in st.session_state.breadcrumb])
        st.markdown(f'<div class="breadcrumb">{bc}</div>', unsafe_allow_html=True)

def back_button(target_page, target_breadcrumb):
    st.markdown("<br>", unsafe_allow_html=True)
    current = st.session_state.page
    if st.button("Back", key=f"back_{current}_to_{target_page}"):
        navigate_to(target_page, target_breadcrumb); st.rerun()

# =============================================================================
#  NAVIGATION MENUS
# =============================================================================

def render_home():
    st.markdown('<div class="hero"><h1>African Actuarial Consultants</h1><p>Comprehensive Actuarial Reserving Toolkit — IFRS 17 Compliant</p><p style="margin-top:1rem;font-size:1rem;">Liability for Remaining Coverage (LRC) | Liability for Incurred Claims (LIC)</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>LRC — Liability for Remaining Coverage</h3><p>Unexpired risk reserve calculations for premium liabilities.</p><p style="font-size:0.85rem;color:#666;">UPR Calculator | Loss Component</p></div>', unsafe_allow_html=True)
        if st.button("Go to LRC Calculators", key="nav_home_lrc"): navigate_to('lrc', ['Home', 'LRC']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>LIC — Liability for Incurred Claims</h3><p>Outstanding claims reserves, IBNR, ULAE, Risk Adjustment.</p><p style="font-size:0.85rem;color:#666;">Fulfilment Cashflows | Risk Adjustment</p></div>', unsafe_allow_html=True)
        if st.button("Go to LIC Calculators", key="nav_home_lic"): navigate_to('lic', ['Home', 'LIC']); st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True); st.info("Select LRC or LIC above.")

def render_lrc():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding:2rem;"><h1>LRC — Liability for Remaining Coverage</h1><p>Unexpired risk reserve and loss component calculations</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>UPR Calculator</h3><p>Unearned Premium Reserve — 365th, 24th, and 8th methods.</p></div>', unsafe_allow_html=True)
        if st.button("Open UPR Calculator", key="nav_lrc_upr"): navigate_to('upr_calculator', ['Home','LRC','UPR Calculator']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Loss Component</h3><p>Loss Ratio, Commission Ratio, Combined Ratio, Loss Component.</p></div>', unsafe_allow_html=True)
        if st.button("Open Loss Component", key="nav_lrc_loss"): navigate_to('loss_component', ['Home','LRC','Loss Component']); st.rerun()
    back_button('home', ['Home'])

def render_lic():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding:2rem;"><h1>LIC — Liability for Incurred Claims</h1><p>Outstanding claims, IBNR, ULAE, NPR, and Risk Adjustment</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Fulfilment Cashflows</h3><p>OCR, IBNR (6 methods), ULAE, and NPR calculators.</p></div>', unsafe_allow_html=True)
        if st.button("Fulfilment Cashflows", key="nav_lic_fulfil"): navigate_to('fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Risk Adjustment</h3><p>Mack, Bootstrap, VaR, and Cost of Capital methods.</p></div>', unsafe_allow_html=True)
        if st.button("Risk Adjustment", key="nav_lic_ra"): navigate_to('risk_adjustment', ['Home','LIC','Risk Adjustment']); st.rerun()
    back_button('home', ['Home'])

def render_fulfilment_cashflows():
    show_breadcrumb(); st.markdown("## Fulfilment Cashflows"); st.markdown("Select a calculator:"); st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (t, d, p) in enumerate([("OCR","Outstanding Claims Reserve","ocr_calculator"),("IBNR","Incurred But Not Reported","ibnr_menu"),("ULAE","Unallocated Loss Adjustment Expenses","ulae_calculator"),("NPR","Non-Performance Risk","npr_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_fc_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows',t]); st.rerun()
    back_button('lic', ['Home','LIC'])

def render_ibnr_menu():
    show_breadcrumb(); st.markdown("## IBNR Calculation Methods"); st.markdown("Select a method:"); st.markdown("<br>", unsafe_allow_html=True)
    methods = [("Percentage Approach","Simple percentage of premiums","ibnr_percentage"),("Basic Chain Ladder (BCL)","Traditional CL with inflation & discounting","bcl_calculator"),("Cape Cod","Internally-derived loss ratio","capecod_calculator"),("Bornhuetter-Ferguson (BF)","A-priori ELR with development pattern","bf_calculator"),("Expected Loss Ratio (ELR)","Pure ELR method for IBNR","elr_calculator"),("Average Cost Per Claim (ACPC)","Claims frequency & severity","acpc_calculator")]
    for i in range(0,len(methods),3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(methods):
                n,d,p = methods[i+j]
                with cols[j]:
                    st.markdown(f'<div class="card"><h3>{n}</h3><p>{d}</p></div>', unsafe_allow_html=True)
                    if st.button("Open", key=f"nav_ibnr_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows','IBNR Methods',n]); st.rerun()
    back_button('fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows'])

def render_risk_adjustment():
    show_breadcrumb(); st.markdown("## Risk Adjustment Methods"); st.markdown("Select a methodology:"); st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(n,d,p) in enumerate([("Mack Method","Distribution-free standard error","mack_calculator"),("Bootstrap","England & Verrall (2002)","bootstrap_calculator"),("Value at Risk (VaR)","Percentile-based risk measure","var_calculator"),("Cost of Capital","Solvency II approach","coc_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{n}</h3><p>{d}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_ra_{p}"): navigate_to(p, ['Home','LIC','Risk Adjustment',n]); st.rerun()
    back_button('lic', ['Home','LIC'])

# =============================================================================
#  CALCULATORS — COMPLETE
# =============================================================================

# UPR
def render_upr_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Unearned Premium Reserve (UPR) Calculator</h1><p>Upload CSV or Excel. Map columns. Calculates UPR using 365th, 24th, or 8th method.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    with col1: valuation_date=st.date_input("Valuation Date",value=date(2025,12,31),key="upr_vd")
    with col2: client_name=st.text_input("Client Name",value="Client",key="upr_cn").strip()
    with col3: method=st.selectbox("Method",["365th (exact days)","24th (half-month)","8th (half-quarter)"],key="upr_mt")
    with col4: pass
    valuation_date=pd.to_datetime(valuation_date)
    uploaded_file=st.file_uploader("Choose a file",type=["csv","xlsx","xls"],key="upr_f")
    if uploaded_file is not None:
        try:
            original_filename=uploaded_file.name; base_filename=re.sub(r'\.[^.]*$','',original_filename)
            ext=uploaded_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(uploaded_file,encoding='utf-8')
                except: uploaded_file.seek(0); df=pd.read_csv(uploaded_file,encoding='cp1252')
            else: df=pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            st.markdown("#### Preview"); st.dataframe(df.head()); st.markdown("---")
            st.markdown("### Map Columns")
            all_columns=df.columns.tolist()
            r1,r2=st.columns(2)
            with r1:
                st.markdown('<div class="required-container"><h3>Start_Date</h3><p>Policy start date</p></div>',unsafe_allow_html=True)
                start_date_col=st.selectbox("Start Date",[""]+all_columns,key="upr_sd",label_visibility="collapsed")
                if start_date_col=="": start_date_col=None
            with r2:
                st.markdown('<div class="required-container"><h3>End_Date</h3><p>Policy end date</p></div>',unsafe_allow_html=True)
                end_date_col=st.selectbox("End Date",[""]+all_columns,key="upr_ed",label_visibility="collapsed")
                if end_date_col=="": end_date_col=None
            st.markdown("---")
            st.markdown('<div class="grouping-container"><h3>Grouping Columns</h3></div>',unsafe_allow_html=True)
            grouping_options=[c for c in all_columns if c not in [start_date_col,end_date_col]]
            grouping_cols=st.multiselect("Group by:",options=grouping_options,default=[grouping_options[0]] if grouping_options else [],key="upr_gc")
            if not grouping_cols: st.error("Select at least one grouping column."); st.stop()
            st.markdown("---"); st.markdown("### Select Numeric Columns")
            numeric_columns=[]
            for c in df.columns:
                if c in [start_date_col,end_date_col]+grouping_cols: continue
                try: pd.to_numeric(df[c]); numeric_columns.append(c)
                except: pass
            if not numeric_columns: st.error("No numeric columns."); st.stop()
            selected_value_cols=st.multiselect("Numeric columns:",options=numeric_columns,default=numeric_columns[:min(4,len(numeric_columns))],key="upr_vc")
            if not start_date_col or not end_date_col: st.error("Map all date columns."); st.stop()
            if not selected_value_cols: st.warning("Select at least one numeric column."); st.stop()
            st.markdown("### Data Quality Checks")
            df_check=df.copy(); df_check=df_check.rename(columns={start_date_col:'Start_Date',end_date_col:'End_Date'})
            df_check['Start_Date']=pd.to_datetime(df_check['Start_Date'],errors='coerce')
            df_check['End_Date']=pd.to_datetime(df_check['End_Date'],errors='coerce')
            all_selected=['Start_Date','End_Date']+grouping_cols+selected_value_cols
            has_critical=False
            st.markdown("#### Missing Values")
            missing={}
            for c in all_selected:
                if c in df_check.columns: missing[c]=df_check[c].isna().sum()
            st.dataframe(pd.DataFrame(list(missing.items()),columns=['Column','Missing']),use_container_width=True)
            if sum(missing.values())==0: st.success("No missing values.")
            else: st.warning(f"Total missing: {sum(missing.values())}")
            st.markdown("#### Date Reasonability")
            bad=df_check.dropna(subset=['Start_Date','End_Date']); bad=bad[bad['End_Date']<=bad['Start_Date']]
            if len(bad)>0: has_critical=True; st.error(f"{len(bad)} rows with End_Date <= Start_Date.")
            else: st.success("All dates valid.")
            st.markdown("#### Duplicates")
            dups=df_check[df_check.duplicated()]
            if len(dups)>0: st.warning(f"{len(dups)} duplicates found.")
            else: st.success("No duplicates.")
            st.markdown("---")
            if has_critical: st.error("Critical issues. Fix and re-upload."); st.stop()
            df_processed=df_check.dropna(subset=['Start_Date','End_Date'])
            df_processed=df_processed[df_processed['End_Date']>df_processed['Start_Date']]
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce')
            df_processed["Duration"]=(df_processed["End_Date"]-df_processed["Start_Date"]).dt.days
            df_processed=df_processed[df_processed["Duration"]>0]
            if df_processed.empty: st.error("No valid policies."); st.stop()
            if st.button("Calculate UPR",key="upr_calc",use_container_width=True):
                with st.spinner("Calculating..."):
                    cond=[valuation_date<df_processed["Start_Date"],valuation_date>df_processed["End_Date"],(valuation_date<=df_processed["End_Date"])&(valuation_date>=df_processed["Start_Date"])]
                    if method=="365th (exact days)": t=df_processed["Duration"]; r=(df_processed["End_Date"]-valuation_date).dt.days; ch=[1,0,r/t]
                    elif method=="24th (half-month)": iv=365.25/24; t=df_processed["Duration"]/iv; r=(df_processed["End_Date"]-valuation_date).dt.days/iv; ch=[1,0,r/t]
                    else: iv=365.25/8; t=df_processed["Duration"]/iv; r=(df_processed["End_Date"]-valuation_date).dt.days/iv; ch=[1,0,r/t]
                    df_processed["Unearned"]=np.select(cond,ch,default=np.nan)
                    for c in selected_value_cols: df_processed[f"{c}_UPR"]=df_processed["Unearned"]*df_processed[c]
                    upr_c=[f"{c}_UPR" for c in selected_value_cols]
                    result=df_processed.groupby(grouping_cols)[upr_c].sum().reset_index()
                    result.columns=grouping_cols+[c.replace('_UPR','') for c in upr_c]
                    st.subheader("UPR Results by "+", ".join(grouping_cols))
                    disp=result.copy()
                    for c in disp.columns:
                        if c not in grouping_cols: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                    st.dataframe(disp,use_container_width=True)
                    output=BytesIO()
                    with pd.ExcelWriter(output,engine='openpyxl') as w: result.to_excel(w,index=False,sheet_name='UPR_Results')
                    output.seek(0)
                    sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                    so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
                    st.download_button("Download Excel",data=output,file_name=f"{sc}_{so}_UPR_Results.xlsx",key="upr_dl",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('lrc',['Home','LRC'])

# LOSS COMPONENT
def render_loss_component():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Loss Component Calculator</h1><p>Upload CSV or Excel. Map columns. Calculates Loss Ratio, Commission Ratio, Expense Ratio, Combined Ratio, and Loss Component.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client Name",value="Client",key="lc_cn").strip()
    with col2: pass
    uploaded_file=st.file_uploader("Choose a file",type=["csv","xlsx","xls"],key="lc_f")
    if uploaded_file is not None:
        try:
            ext=uploaded_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(uploaded_file,encoding='utf-8')
                except: uploaded_file.seek(0); df=pd.read_csv(uploaded_file,encoding='cp1252')
            else: df=pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            st.markdown("#### Preview"); st.dataframe(df.head()); st.markdown("---")
            st.markdown("### Map Your Columns")
            all_columns=df.columns.tolist()
            required_fields={
                'Line_of_business':'Line of Business','Gross_Written_Premiums':'Gross Written Premiums',
                'Gross_Attributable_Expenses':'Gross Attributable Expenses','Gross_Commission_Paid':'Gross Commission Paid',
                'Gross_Paid_Claims':'Gross Paid Claims','Gross_Opening_OCR':'Gross Opening OCR',
                'Gross_Closing_OCR':'Gross Closing OCR','Gross_Opening_IBNR':'Gross Opening IBNR',
                'Gross_Closing_IBNR':'Gross Closing IBNR','Gross_Opening_UPR':'Gross Opening UPR',
                'Gross_Closing_UPR':'Gross Closing UPR','Gross_Risk_Adjustment':'Gross Risk Adjustment'
            }
            mapped_columns={}
            field_list=list(required_fields.keys())
            for i in range(0,len(field_list),3):
                cols=st.columns(3)
                for j in range(3):
                    if i+j<len(field_list):
                        field=field_list[i+j]
                        with cols[j]:
                            desc=required_fields[field]
                            st.markdown(f'<div class="required-container"><h3>{field}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
                            mapped_columns[field]=st.selectbox(f"Select {field}",[""]+all_columns,key=f"lc_m_{field}",label_visibility="collapsed")
                            if mapped_columns[field]=="": mapped_columns[field]=None
            st.markdown("---")
            missing=[f for f,c in mapped_columns.items() if c is None]
            if missing: st.error(f"Missing mappings: {', '.join(missing)}"); st.stop()
            df_processed=df.rename(columns=mapped_columns)
            df_processed["Gross_Actual_Incurred_Claims"]=(df_processed["Gross_Paid_Claims"]+df_processed["Gross_Closing_IBNR"]+df_processed["Gross_Closing_OCR"]-df_processed["Gross_Opening_IBNR"]-df_processed["Gross_Opening_OCR"])
            df_processed["Gross_Earned_Premiums"]=(df_processed["Gross_Written_Premiums"]+df_processed["Gross_Opening_UPR"]-df_processed["Gross_Closing_UPR"])
            result=df_processed.groupby('Line_of_business').agg({'Gross_Written_Premiums':'sum','Gross_Earned_Premiums':'sum','Gross_Actual_Incurred_Claims':'sum','Gross_Commission_Paid':'sum','Gross_Attributable_Expenses':'sum','Gross_Risk_Adjustment':'sum','Gross_Closing_IBNR':'sum','Gross_Closing_OCR':'sum','Gross_Closing_UPR':'sum'}).reset_index()
            result['Loss_Ratio']=np.where(result['Gross_Earned_Premiums']!=0,result['Gross_Actual_Incurred_Claims']/result['Gross_Earned_Premiums'],np.nan)
            result['Commission_Ratio']=np.where(result['Gross_Written_Premiums']!=0,result['Gross_Commission_Paid']/result['Gross_Written_Premiums'],np.nan)
            result['Expense_Ratio']=np.where(result['Gross_Written_Premiums']!=0,result['Gross_Attributable_Expenses']/result['Gross_Written_Premiums'],np.nan)
            ra_denom=result['Gross_Closing_IBNR']+result['Gross_Closing_OCR']
            result['Risk_Adjustment_Ratio']=np.where(ra_denom!=0,result['Gross_Risk_Adjustment']/ra_denom,np.nan)
            result['Combined_Ratio']=result['Loss_Ratio']+result['Commission_Ratio']+result['Expense_Ratio']+result['Risk_Adjustment_Ratio']
            result['Loss_Component']=np.maximum(result['Combined_Ratio']-1,0)*result['Gross_Closing_UPR']
            result=result.rename(columns={'Gross_Written_Premiums':'Total_Written_Premiums','Gross_Earned_Premiums':'Total_Earned_Premiums','Gross_Actual_Incurred_Claims':'Total_Incurred_Claims','Gross_Commission_Paid':'Total_Commission_Paid','Gross_Attributable_Expenses':'Total_Expenses','Gross_Risk_Adjustment':'Total_Risk_Adjustment','Gross_Closing_UPR':'Closing_UPR'})
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.subheader("Loss Component Results")
            disp=result.copy()
            for c in disp.columns:
                if c!='Line_of_business': disp[c]=disp[c].apply(lambda x: f"{x:.2%}" if 'Ratio' in c and pd.notna(x) else (f"{x:,.2f}" if pd.notna(x) else "N/A"))
            st.dataframe(disp,use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: result.to_excel(w,index=False,sheet_name='Loss_Component_Results')
            output.seek(0)
            sc="".join(c for c in client_name if c.isalnum() or c in (' ','-','_')).rstrip() or "Client"
            st.download_button("Download Excel",data=output,file_name=f"{sc}_Loss_Component_Results.xlsx",key="lc_dl",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            with st.expander("View Detailed Calculations"): st.dataframe(df_processed,use_container_width=True)
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('lrc',['Home','LRC'])

# OCR
def render_ocr_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Outstanding Claims Reserve (OCR) Calculator</h1><p>Upload CSV or Excel. Select grouping and numeric columns. Calculates outstanding reserves.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client Name",value="Client",key="ocr_cn").strip()
    with col2: pass
    uploaded_file=st.file_uploader("Choose a file",type=["csv","xlsx","xls"],key="ocr_f")
    if uploaded_file is not None:
        try:
            original_filename=uploaded_file.name; base_filename=re.sub(r'\.[^.]*$','',original_filename)
            ext=uploaded_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(uploaded_file,encoding='utf-8')
                except: uploaded_file.seek(0); df=pd.read_csv(uploaded_file,encoding='cp1252')
            else: df=pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            st.markdown("#### Preview"); st.dataframe(df.head()); st.markdown("---")
            all_columns=df.columns.tolist()
            st.markdown('<div class="grouping-container"><h3>Grouping Columns</h3></div>',unsafe_allow_html=True)
            grouping_cols=st.multiselect("Group by:",options=all_columns,default=[all_columns[0]] if all_columns else [],key="ocr_gc")
            if not grouping_cols: st.error("Select at least one grouping column."); st.stop()
            st.markdown("---"); st.markdown("### Select Numeric Columns")
            numeric_columns=df.select_dtypes(include=[np.number]).columns.tolist()
            numeric_columns=[c for c in numeric_columns if c not in grouping_cols]
            if not numeric_columns: st.error("No numeric columns."); st.stop()
            selected_value_cols=st.multiselect("Numeric columns:",options=numeric_columns,default=numeric_columns[:min(5,len(numeric_columns))],key="ocr_vc")
            if not selected_value_cols: st.warning("Select at least one numeric column."); st.stop()
            st.markdown("### Data Quality Checks")
            all_selected=grouping_cols+selected_value_cols; df_original_len=len(df)
            st.markdown("#### 1. Missing Values")
            ms={}
            for c in all_selected:
                if c in df.columns: ms[c]=df[c].isna().sum()
            st.dataframe(pd.DataFrame(list(ms.items()),columns=['Column','Missing']),use_container_width=True)
            if any(v>0 for v in ms.values()):
                st.markdown('<div class="data-check-error"><b>CRITICAL: Missing values found.</b></div>',unsafe_allow_html=True); st.stop()
            else: st.success("No missing values.")
            st.markdown("#### 2. Duplicates")
            dc=df.duplicated().sum()
            if dc>0: df=df.drop_duplicates(); st.success(f"Removed {dc} duplicates. {len(df)} rows remain.")
            else: st.success("No duplicates.")
            st.markdown("#### 3. Non-Numeric Values")
            def cn(series):
                if series.dtype=='object':
                    c=series.astype(str).str.replace(r'[$,]','',regex=True); c=c.str.replace(r',','',regex=False)
                    c=c.str.replace(r'^\((.+)\)$',r'-\1',regex=True).str.strip().replace('',np.nan)
                    return pd.to_numeric(c,errors='coerce')
                return pd.to_numeric(series,errors='coerce')
            ci=[]
            for c in selected_value_cols:
                if c in df.columns:
                    t=cn(df[c]); f=t.isna()&df[c].notna()
                    if f.sum()>0: ci.append(f"Column '{c}': {f.sum()} non-numeric")
            if ci:
                for i in ci: st.write(f"  {i}")
                for c in selected_value_cols: df[c]=cn(df[c]).fillna(0)
                st.success("Converted.")
            else: st.success("All numeric.")
            if dc>0 or ci: st.info("Adjustments applied.")
            else: st.markdown('<div class="data-check-success"><b>All checks passed!</b></div>',unsafe_allow_html=True)
            st.markdown("---")
            df_processed=df[grouping_cols+selected_value_cols].copy()
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce').fillna(0)
            grouped=df_processed.groupby(grouping_cols)[selected_value_cols].sum().reset_index()
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.subheader("Outstanding Reserve Results"); st.markdown(f"**Grouped by:** {', '.join(grouping_cols)}")
            disp=grouped.copy()
            for c in selected_value_cols: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(disp,use_container_width=True)
            st.caption(f"Original: {df_original_len} | Cleaned: {len(df_processed)} | Grouped: {len(grouped)}")
            st.markdown('</div>',unsafe_allow_html=True)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: grouped.to_excel(w,index=False,sheet_name='OCR_Results')
            output.seek(0)
            sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
            so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
            st.download_button("Download Excel",data=output,file_name=f"{sc}_{so}_OCR_Results.xlsx",key="ocr_dl",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

# IBNR PERCENTAGE
def render_ibnr_percentage():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>IBNR Percentage Method Calculator</h1><p>Upload premium data. Map columns, select period, enter IBNR percentage.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-container"><h3>Client Information</h3></div>', unsafe_allow_html=True)
    client_name=st.text_input("Client Name",value="Client",key="ibp_cn",label_visibility="collapsed").strip()
    st.markdown('<div class="section-container"><h3>IBNR Period</h3></div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: from_date=st.date_input("From Date",value=date(2020,1,1),key="ibp_fd",label_visibility="collapsed")
    with c2: to_date=st.date_input("To Date",value=date(2024,12,31),key="ibp_td",label_visibility="collapsed")
    from_date=pd.to_datetime(from_date); to_date=pd.to_datetime(to_date)
    st.info(f"Selected Period: {from_date.date()} to {to_date.date()}")
    st.markdown('<div class="section-container"><h3>IBNR Percentage</h3></div>', unsafe_allow_html=True)
    ibnr_pct=st.number_input("Percentage (%)",min_value=0.0,max_value=100.0,value=10.0,step=0.5,key="ibp_pct",label_visibility="collapsed")/100
    st.caption(f"Selected: {ibnr_pct*100:.2f}%")
    st.markdown('<div class="section-container"><h3>Upload Data File</h3></div>', unsafe_allow_html=True)
    uploaded_file=st.file_uploader("Choose a file",type=["csv","xlsx","xls"],key="ibp_f",label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            original_filename=uploaded_file.name; base_filename=re.sub(r'\.[^.]*$','',original_filename)
            ext=uploaded_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(uploaded_file,encoding='utf-8')
                except: uploaded_file.seek(0); df=pd.read_csv(uploaded_file,encoding='cp1252')
            else: df=pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if 'Unnamed' in c]
            if unnamed: df=df.drop(columns=unnamed)
            st.write("### Preview"); st.dataframe(df.head())
            st.write("### Map Your Columns")
            all_cols=df.columns.tolist()
            c1,c2=st.columns(2)
            with c1: date_col=st.selectbox("Date column",["Select..."]+all_cols,key="ibp_dc")
            with c2: lob_col=st.selectbox("Line of Business column",["Select..."]+all_cols,key="ibp_lc")
            if date_col=="Select..." or lob_col=="Select...": st.warning("Please select both."); st.stop()
            num_cols=[c for c in all_cols if c not in [date_col,lob_col]]
            if not num_cols: st.error("No numeric columns."); st.stop()
            amount_cols=st.multiselect("Amount columns",num_cols,key="ibp_ac")
            if not amount_cols: st.warning("Select at least one."); st.stop()
            st.write("### Data Quality Checks")
            mf=False
            for c in [date_col,lob_col]+amount_cols:
                if df[c].isna().sum()>0: st.error(f"Column '{c}' has missing values."); mf=True
            if mf: st.stop()
            try:
                df[date_col]=pd.to_datetime(df[date_col],errors='coerce')
                if df[date_col].isna().sum()>0: st.error("Could not parse dates."); st.stop()
            except Exception as e: st.error(f"Date error: {e}"); st.stop()
            dc=df.duplicated().sum()
            if dc>0: df=df.drop_duplicates(); st.info(f"Removed {dc} duplicates.")
            mask=(df[date_col]>=from_date)&(df[date_col]<=to_date)
            df_filtered=df[mask].copy()
            if df_filtered.empty: st.error("No data in selected period."); st.stop()
            st.success(f"{len(df_filtered)} records after filtering")
            st.write("### Results")
            premium_summary=df_filtered.groupby(lob_col)[amount_cols].sum().reset_index()
            ibnr_summary=premium_summary.copy()
            for c in amount_cols: ibnr_summary[f"{c}_IBNR"]=ibnr_summary[c]*ibnr_pct
            total_row={lob_col:"TOTAL"}
            for c in amount_cols: total_row[c]=premium_summary[c].sum(); total_row[f"{c}_IBNR"]=total_row[c]*ibnr_pct
            ibnr_summary=pd.concat([ibnr_summary,pd.DataFrame([total_row])],ignore_index=True)
            st.subheader("Premium Summary")
            dp=premium_summary.copy()
            for c in amount_cols: dp[c]=dp[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(dp)
            st.subheader("IBNR Summary")
            di=ibnr_summary.copy()
            for c in di.columns:
                if c!=lob_col: di[c]=di[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(di)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: ibnr_summary.to_excel(w,index=False,sheet_name='IBNR_Summary')
            output.seek(0)
            sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
            so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
            st.download_button("Download IBNR Summary",data=output.getvalue(),file_name=f"{sc}_{so}_IBNR_Summary.xlsx",key="ibp_dl")
        except Exception as e: st.error(f"Error: {str(e)}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

# =============================================================================
#  PLACEHOLDERS — PENDING CALCULATORS
# =============================================================================

def render_bcl_calculator():
    show_breadcrumb(); st.markdown("## Basic Chain Ladder (BCL) IBNR Calculator")
    # ╔══ INSERT BCL CODE HERE ══╗
    st.info("Basic Chain Ladder — Pending implementation")
    # =============================================================================
#  BASIC CHAIN LADDER (BCL) CALCULATOR — COMPLETE
# =============================================================================

def render_bcl_calculator():
    """Basic Chain Ladder IBNR Calculator with Inflation & Discounting."""
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Basic Chain Ladder (BCL) IBNR Calculator</h1><p>Upload claims data. Select period, grain, grouping, and amounts. Choose LDF method with stability diagnostics. Optional inflation adjustment and discounting.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ---- Session state for BCL ----
    if 'bcl_df' not in st.session_state: st.session_state.bcl_df = None
    if 'bcl_factors' not in st.session_state: st.session_state.bcl_factors = None
    if 'bcl_results' not in st.session_state: st.session_state.bcl_results = None
    if 'bcl_cum_inflation' not in st.session_state: st.session_state.bcl_cum_inflation = None
    if 'bcl_per_period' not in st.session_state: st.session_state.bcl_per_period = None

    # ---- Client & Period ----
    col1, col2 = st.columns(2)
    with col1: client_name = st.text_input("Client Name", value="Client", key="bcl_cn").strip()
    with col2: pass

    st.markdown('<div class="section-container"><h3>IBNR Period & Grain</h3></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: from_date = st.date_input("From Date", value=date(2021,1,1), key="bcl_fd")
    with c2: to_date = st.date_input("To Date", value=date(2025,12,31), key="bcl_td")
    with c3: grain = st.selectbox("Grain", ["Yearly","Half-Yearly","Quarterly","Monthly"], key="bcl_gr")
    grain_map = {"Yearly":"Y","Half-Yearly":"H","Quarterly":"Q","Monthly":"M"}
    grain_key = grain_map[grain]
    from_date_dt = pd.to_datetime(from_date); to_date_dt = pd.to_datetime(to_date)
    st.info(f"Period: {from_date} to {to_date} | Grain: {grain}")

    # ---- File Upload ----
    st.markdown('<div class="section-container"><h3>Upload Claims Data</h3></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose claims file", type=["csv","xlsx","xls"], key="bcl_f")
    
    if uploaded_file is not None:
        try:
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext == 'csv':
                try: df = pd.read_csv(uploaded_file, encoding='utf-8')
                except: uploaded_file.seek(0); df = pd.read_csv(uploaded_file, encoding='cp1252')
            else: df = pd.read_excel(uploaded_file)
            unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df = df.drop(columns=unnamed)
            st.markdown("#### Preview"); st.dataframe(df.head())
            
            st.markdown("### Map Columns")
            all_cols = df.columns.tolist()
            c1, c2 = st.columns(2)
            with c1: loss_col = st.selectbox("Loss Date column", [""]+all_cols, key="bcl_lc")
            with c2: report_col = st.selectbox("Report Date column", [""]+all_cols, key="bcl_rc")
            if not loss_col or not report_col: st.warning("Select both date columns."); st.stop()
            
            remaining = [c for c in all_cols if c not in [loss_col, report_col]]
            grouping_cols = st.multiselect("Grouping columns (optional)", remaining, key="bcl_gc")
            
            num_cands = [c for c in df.columns if c not in [loss_col,report_col]+grouping_cols and pd.api.types.is_numeric_dtype(df[c])]
            if not num_cands: st.error("No numeric columns."); st.stop()
            amount_cols = st.multiselect("Claim Amount columns", num_cands, key="bcl_ac")
            if not amount_cols: st.warning("Select at least one amount column."); st.stop()

            # Process data
            df[loss_col] = pd.to_datetime(df[loss_col], errors='coerce')
            df[report_col] = pd.to_datetime(df[report_col], errors='coerce')
            df = df.dropna(subset=[loss_col, report_col])
            df_filtered = df[(df[loss_col]>=from_date_dt)&(df[loss_col]<=to_date_dt)].copy()
            if df_filtered.empty: st.error("No data in selected period."); st.stop()
            st.success(f"{len(df_filtered)} records in period")

            # Calculate periods
            if grain_key == 'Y': n_periods = to_date_dt.year - from_date_dt.year + 1
            elif grain_key == 'M': n_periods = (to_date_dt.year-from_date_dt.year)*12 + (to_date_dt.month-from_date_dt.month) + 1
            elif grain_key == 'Q': n_periods = (to_date_dt.year-from_date_dt.year)*4 + ((to_date_dt.month-1)//3-(from_date_dt.month-1)//3) + 1
            else: n_periods = (to_date_dt.year-from_date_dt.year)*2 + ((to_date_dt.month-1)//6-(from_date_dt.month-1)//6) + 1

            # Discounting & Inflation
            st.markdown("---"); st.markdown("### Options")
            c1, c2 = st.columns(2)
            with c1:
                use_discounting = st.checkbox("Apply Discounting", key="bcl_ud")
                spot_rates = None; flat_rate = None
                if use_discounting:
                    use_curve = st.checkbox("Use Yield Curve", key="bcl_uc")
                    if use_curve:
                        yc_file = st.file_uploader("Yield Curve file (Maturity, Rate%)", type=["csv","xlsx","xls"], key="bcl_yc")
                        if yc_file is not None:
                            yc_ext = yc_file.name.split('.')[-1].lower()
                            yc_df = pd.read_csv(yc_file) if yc_ext=='csv' else pd.read_excel(yc_file)
                            yc_df = yc_df.dropna()
                            if len(yc_df.columns)>=2:
                                maturities = pd.to_numeric(yc_df.iloc[:,0], errors='coerce').values
                                rates = pd.to_numeric(yc_df.iloc[:,1], errors='coerce').values/100
                                ppy = periods_per_year(grain_key)
                                pm = np.arange(1,61)/ppy
                                if len(maturities)>=4: f_int = interpolate.CubicSpline(maturities, rates, extrapolate=True)
                                else: f_int = interpolate.interp1d(maturities, rates, kind='linear', fill_value='extrapolate')
                                spot_rates = np.clip(f_int(pm), 0, 1.0)
                    else: flat_rate = st.number_input("Annual discount rate (%)", 0.0, 50.0, 5.0, key="bcl_fr")/100
            with c2:
                use_inflation = st.checkbox("Apply Inflation Adjustment", key="bcl_ui")
                cum_inflation = None; per_period_rates = None
                if use_inflation:
                    inf_file = st.file_uploader("Inflation file (Period, Rate%)", type=["csv","xlsx","xls"], key="bcl_if")
                    if inf_file is not None:
                        inf_ext = inf_file.name.split('.')[-1].lower()
                        inf_df = pd.read_csv(inf_file) if inf_ext=='csv' else pd.read_excel(inf_file)
                        inf_df = inf_df.dropna()
                        if len(inf_df.columns)>=2:
                            inf_rates = pd.to_numeric(inf_df.iloc[:,1], errors='coerce').fillna(0)/100
                            ppy_tgt = periods_per_year(grain_key)
                            x_inf = np.arange(len(inf_rates))
                            x_tgt = np.arange(int(x_inf[-1])+1) if len(inf_rates)>0 else np.arange(n_periods)
                            if len(inf_rates)>=4: f_int = interpolate.CubicSpline(x_inf, inf_rates, extrapolate=True)
                            else: f_int = interpolate.interp1d(x_inf, inf_rates, kind='linear', fill_value='extrapolate')
                            annual_tgt = np.clip(f_int(x_tgt), -0.5, 2.0)
                            per_period_rates = (1+annual_tgt)**(1/ppy_tgt)-1
                            cum_inflation = np.cumprod(1+per_period_rates)

            # ---- LDF Selection & Calculate ----
            st.markdown("---"); st.markdown("### LDF Selection & Calculation")
            
            # Get groups
            if grouping_cols: groups = df_filtered[grouping_cols].drop_duplicates().to_dict("records")
            else: groups = [{"__all__":"All Data"}]

            if st.button("Run Chain Ladder", key="bcl_run", use_container_width=True):
                all_summary = []; all_detail = []; all_factors = []
                
                for grp in groups:
                    if "__all__" in grp: gdf = df_filtered.copy(); glabel = "All Data"
                    else:
                        mask = pd.Series(True, index=df_filtered.index)
                        for col, val in grp.items(): mask &= (df_filtered[col]==val)
                        gdf = df_filtered[mask].copy(); glabel = " | ".join(str(v) for v in grp.values())
                    
                    for ac in amount_cols:
                        label = f"{glabel} | {ac}"
                        st.markdown(f"**{label}**")
                        
                        # Build triangles
                        gdf["__ap"] = gdf[loss_col].apply(lambda d: (d.year-from_date_dt.year) if grain_key=='Y' else ((d.year-from_date_dt.year)*12+(d.month-from_date_dt.month)))
                        gdf["__dp"] = gdf.apply(lambda r: max(0, min((r[report_col].year-r[loss_col].year) if grain_key=='Y' else ((r[report_col].year-r[loss_col].year)*12+(r[report_col].month-r[loss_col].month)), n_periods-1)), axis=1)
                        gdf = gdf[(gdf["__ap"]>=0)&(gdf["__ap"]<n_periods)]
                        
                        pivot = gdf.pivot_table(index="__ap", columns="__dp", values=ac, aggfunc="sum")
                        for ap in range(n_periods):
                            if ap not in pivot.index: pivot.loc[ap] = np.nan
                        for dp in range(n_periods):
                            if dp not in pivot.columns: pivot[dp] = np.nan
                        inc = pivot.sort_index()[sorted(pivot.columns)].astype(float)
                        
                        obs_mask = pd.DataFrame(False, index=inc.index, columns=inc.columns)
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp < n_periods: obs_mask.loc[ap, dp] = pd.notna(inc.loc[ap, dp])
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp >= n_periods: inc.loc[ap, dp] = np.nan
                        
                        cum = inc.copy()
                        for ap in inc.index:
                            has_obs = any(pd.notna(inc.loc[ap, dp]) for dp in inc.columns if ap+dp<n_periods)
                            if not has_obs: cum.loc[ap]=np.nan; continue
                            running = 0.0
                            for dp in sorted(inc.columns):
                                if ap+dp<n_periods:
                                    v = inc.loc[ap, dp]; running += v if pd.notna(v) else 0.0; cum.loc[ap, dp]=running
                                else: cum.loc[ap, dp]=np.nan
                        
                        cum_filled = cum.fillna(0)
                        
                        # Deflate
                        working_cum = cum_filled
                        if use_inflation and cum_inflation is not None:
                            valuation_idx = n_periods-1
                            if len(cum_inflation)<=valuation_idx: cum_inflation=np.append(cum_inflation,[cum_inflation[-1]]*(valuation_idx-len(cum_inflation)+1))
                            inf_val = cum_inflation[valuation_idx]
                            real_inc = inc.copy().astype(float)
                            for ap in inc.index:
                                for dp in inc.columns:
                                    if ap+dp>=n_periods: continue
                                    val = inc.loc[ap, dp]
                                    if pd.isna(val): continue
                                    t = ap+dp
                                    inf_t = cum_inflation[min(t, len(cum_inflation)-1)]
                                    real_inc.loc[ap, dp] = val*(inf_val/inf_t) if inf_t>0 else val
                            working_cum = real_inc.cumsum(axis=1).fillna(0)
                        
                        # Calculate factors
                        n_ay, n_dp = working_cum.shape
                        vw = []; sa = []
                        for j in range(n_dp-1):
                            num, den = 0.0, 0.0; indiv = []
                            for i in range(n_ay):
                                if i+j+1<n_ay:
                                    c = working_cum.iloc[i,j]; n = working_cum.iloc[i,j+1]
                                    if c>0: num+=n; den+=c; indiv.append(n/c)
                            vw.append(num/den if den>0 else 1.0)
                            sa.append(np.mean(indiv) if indiv else 1.0)
                        
                        # Show LDF comparison
                        ldf_df = pd.DataFrame({"Dev Period":range(1,n_dp),"Vol-Weighted":[round(f,4) for f in vw],"Simple Avg":[round(f,4) for f in sa]})
                        st.dataframe(ldf_df, use_container_width=True)
                        
                        # User selects method
                        method = st.selectbox("Select LDF Method", ["Volume-Weighted","Simple Average"], key=f"bcl_m_{label}")
                        factors = vw if method=="Volume-Weighted" else sa
                        
                        # Project
                        completed = working_cum.copy().astype(float)
                        for i in range(n_ay):
                            last_obs = -1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs<0: continue
                            for j in range(last_obs,n_dp-1):
                                if j<len(factors):
                                    prev = completed.iloc[i,j]
                                    completed.iloc[i,j+1] = prev*factors[j] if prev>0 else 0.0
                        
                        cdfs = []
                        running = 1.0
                        for f in reversed(factors): running*=f; cdfs.insert(0, running)
                        
                        # Results
                        rows = []
                        for i in range(n_ay):
                            last_obs = -1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs<0: continue
                            current = working_cum.iloc[i,last_obs]
                            ultimate = completed.iloc[i,n_dp-1]
                            ibnr = max(ultimate-current,0.0)
                            cdf = cdfs[last_obs] if last_obs<len(cdfs) else 1.0
                            rows.append({"AP":i,"Current":current,"Ultimate":ultimate,"IBNR":ibnr,"CDF":cdf})
                        
                        res_df = pd.DataFrame(rows)
                        res_df["IBNR_Nominal"] = res_df["IBNR"]
                        
                        # Re-inflate
                        if use_inflation and cum_inflation is not None and per_period_rates is not None:
                            valuation_idx = n_periods-1
                            last_rate = per_period_rates[-1] if len(per_period_rates)>0 else 0.0
                            def fci(tf):
                                factor=1.0
                                for k in range(valuation_idx+1,tf+1):
                                    ki=k-valuation_idx-1; r=per_period_rates[ki] if ki<len(per_period_rates) else last_rate; factor*=(1.0+r)
                                return factor
                            nominal_map = {}
                            for i in completed.index:
                                last_obs=-1
                                for j in range(n_dp-1,-1,-1):
                                    if i+j<n_ay and pd.notna(working_cum.iloc[i,j]): last_obs=j; break
                                if last_obs<0: nominal_map[i]=0.0; continue
                                total=0.0; dp_cols=sorted(completed.columns)
                                for idx_dp,dp in enumerate(dp_cols):
                                    if dp<=last_obs: continue
                                    cum_curr=completed.iloc[i,dp]
                                    cum_prev=completed.iloc[i,dp_cols[idx_dp-1]] if idx_dp>0 else 0.0
                                    inc_r=max(cum_curr-cum_prev,0.0)
                                    if inc_r<=0: continue
                                    total+=inc_r*fci(i+dp)
                                nominal_map[i]=total
                            res_df["IBNR_Nominal"] = res_df["AP"].map(lambda ap: nominal_map.get(ap,0.0))
                        
                        nom_total = res_df["IBNR_Nominal"].sum()
                        st.metric("Total IBNR (Nominal)", f"{nom_total:,.2f}")
                        disp = res_df.copy()
                        for c in ["Current","Ultimate","IBNR","IBNR_Nominal"]:
                            if c in disp.columns: disp[c] = disp[c].apply(lambda x: f"{x:,.2f}")
                        st.dataframe(disp, use_container_width=True)
                        
                        all_summary.append({"Group":glabel,"Amount":ac,"IBNR_Nominal":nom_total})
                        all_detail.append(res_df)
                
                if all_summary:
                    st.markdown("### Overall Summary")
                    st.dataframe(pd.DataFrame(all_summary), use_container_width=True)
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as w:
                        pd.DataFrame(all_summary).to_excel(w, index=False, sheet_name='IBNR_Summary')
                        if all_detail: pd.concat(all_detail).to_excel(w, index=False, sheet_name='IBNR_Detail')
                    output.seek(0)
                    sc = re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                    st.download_button("Download Excel", data=output, file_name=f"{sc}_BCL_IBNR_Results.xlsx", key="bcl_dl", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e: st.error(f"Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    # ╚══════════════════════════╝
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_capecod_calculator():
    show_breadcrumb(); st.markdown("## Cape Cod IBNR Calculator")
    st.info("Cape Cod — Pending implementation")
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_bf_calculator():
    show_breadcrumb(); st.markdown("## Bornhuetter-Ferguson (BF) IBNR Calculator")
    st.info("Bornhuetter-Ferguson — Pending implementation")
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_elr_calculator():
    show_breadcrumb(); st.markdown("## Expected Loss Ratio (ELR) IBNR Calculator")
    st.info("Expected Loss Ratio — Pending implementation")
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_acpc_calculator():
    show_breadcrumb(); st.markdown("## Average Cost Per Claim (ACPC) IBNR Calculator")
    st.info("Average Cost Per Claim — Pending implementation")
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_ulae_calculator():
    show_breadcrumb(); st.markdown("## ULAE — Unallocated Loss Adjustment Expenses Calculator")
    st.info("ULAE Calculator — Pending implementation")
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def render_npr_calculator():
    show_breadcrumb(); st.markdown("## NPR — Non-Performance Risk (Reinsurance) Calculator")
    st.info("NPR Calculator — Pending implementation")
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def render_mack_calculator():
    show_breadcrumb(); st.markdown("## Mack Method — Risk Adjustment Calculator")
    st.info("Mack Method — Pending implementation")
    back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_bootstrap_calculator():
    show_breadcrumb(); st.markdown("## Bootstrap — Stochastic Reserving Calculator")
    st.info("Bootstrap — Pending implementation")
    back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_var_calculator():
    show_breadcrumb(); st.markdown("## Value at Risk (VaR) — Risk Adjustment Calculator")
    st.info("Value at Risk — Pending implementation")
    back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_coc_calculator():
    show_breadcrumb(); st.markdown("## Cost of Capital — Risk Adjustment Calculator")
    st.info("Cost of Capital — Pending implementation")
    back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

# =============================================================================
#  MAIN ROUTER
# =============================================================================

page_renderers = {
    'home':render_home,'lrc':render_lrc,'lic':render_lic,
    'fulfilment_cashflows':render_fulfilment_cashflows,
    'ibnr_menu':render_ibnr_menu,'risk_adjustment':render_risk_adjustment,
    'upr_calculator':render_upr_calculator,'loss_component':render_loss_component,
    'ocr_calculator':render_ocr_calculator,'ibnr_percentage':render_ibnr_percentage,
    'bcl_calculator':render_bcl_calculator,'capecod_calculator':render_capecod_calculator,
    'bf_calculator':render_bf_calculator,'elr_calculator':render_elr_calculator,
    'acpc_calculator':render_acpc_calculator,'ulae_calculator':render_ulae_calculator,
    'npr_calculator':render_npr_calculator,'mack_calculator':render_mack_calculator,
    'bootstrap_calculator':render_bootstrap_calculator,'var_calculator':render_var_calculator,
    'coc_calculator':render_coc_calculator,
}

current_page = st.session_state.page
if current_page in page_renderers: page_renderers[current_page]()
else: render_home()

st.markdown('<div class="footer"><p>2026 African Actuarial Consultants. All rights reserved.</p><p style="margin-top:0.5rem;font-size:0.9rem;">IFRS 17 Compliant | Solvency II Ready | Built by AAC</p></div>', unsafe_allow_html=True)
