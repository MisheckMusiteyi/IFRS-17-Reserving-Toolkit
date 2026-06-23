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
from scipy import interpolate

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
    .card { background-color: #F9F9F9; border: 1px solid #4A90D9; border-radius: 8px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1.5rem; text-align: center; }
    .card h3 { color: #4A90D9; margin-top: 0; }
    .footer { background-color: #000000; color: #FFFFFF; text-align: center; padding: 1.5rem; border-top: 3px solid #4A90D9; margin-top: 3rem; }
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
    .required-container { background-color: #F9F9F9; border: 2px solid #4A90D9; border-radius: 10px; padding: 1rem; text-align: center; min-height: 120px; margin-bottom: 1rem; }
    .required-container h3 { color: #4A90D9; font-size: 1.2rem; font-weight: bold; }
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
    st.markdown('<div class="hero"><h1>African Actuarial Consultants</h1><p>Comprehensive Actuarial Reserving Toolkit — IFRS 17 Compliant</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>LRC — Liability for Remaining Coverage</h3><p>UPR Calculator | Loss Component</p></div>', unsafe_allow_html=True)
        if st.button("Go to LRC", key="nav_home_lrc"): navigate_to('lrc', ['Home','LRC']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>LIC — Liability for Incurred Claims</h3><p>Fulfilment Cashflows | Risk Adjustment</p></div>', unsafe_allow_html=True)
        if st.button("Go to LIC", key="nav_home_lic"): navigate_to('lic', ['Home','LIC']); st.rerun()

def render_lrc():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding:2rem;"><h1>LRC — Liability for Remaining Coverage</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>UPR Calculator</h3></div>', unsafe_allow_html=True)
        if st.button("Open", key="nav_lrc_upr"): navigate_to('upr_calculator', ['Home','LRC','UPR Calculator']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Loss Component</h3></div>', unsafe_allow_html=True)
        if st.button("Open", key="nav_lrc_loss"): navigate_to('loss_component', ['Home','LRC','Loss Component']); st.rerun()
    back_button('home', ['Home'])

def render_lic():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding:2rem;"><h1>LIC — Liability for Incurred Claims</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Fulfilment Cashflows</h3></div>', unsafe_allow_html=True)
        if st.button("Open", key="nav_lic_fulfil"): navigate_to('fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Risk Adjustment</h3></div>', unsafe_allow_html=True)
        if st.button("Open", key="nav_lic_ra"): navigate_to('risk_adjustment', ['Home','LIC','Risk Adjustment']); st.rerun()
    back_button('home', ['Home'])

def render_fulfilment_cashflows():
    show_breadcrumb(); st.markdown("## Fulfilment Cashflows")
    cols = st.columns(4)
    for i, (t, d, p) in enumerate([("OCR","Outstanding Claims Reserve","ocr_calculator"),("IBNR","Incurred But Not Reported","ibnr_menu"),("ULAE","Unallocated Loss Adjustment Expenses","ulae_calculator"),("NPR","Non-Performance Risk","npr_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_fc_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows',t]); st.rerun()
    back_button('lic', ['Home','LIC'])

def render_ibnr_menu():
    show_breadcrumb(); st.markdown("## IBNR Calculation Methods")
    methods = [("Percentage Approach","ibnr_percentage"),("Basic Chain Ladder","bcl_calculator"),("Cape Cod","capecod_calculator"),("Bornhuetter-Ferguson","bf_calculator"),("Expected Loss Ratio","elr_calculator"),("Average Cost Per Claim","acpc_calculator")]
    for i in range(0,len(methods),3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(methods):
                n,p = methods[i+j]
                with cols[j]:
                    st.markdown(f'<div class="card"><h3>{n}</h3></div>', unsafe_allow_html=True)
                    if st.button("Open", key=f"nav_ibnr_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows','IBNR Methods',n]); st.rerun()
    back_button('fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows'])

def render_risk_adjustment():
    show_breadcrumb(); st.markdown("## Risk Adjustment Methods")
    cols = st.columns(4)
    for i,(n,d,p) in enumerate([("Mack Method","","mack_calculator"),("Bootstrap","","bootstrap_calculator"),("Value at Risk","","var_calculator"),("Cost of Capital","","coc_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{n}</h3></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_ra_{p}"): navigate_to(p, ['Home','LIC','Risk Adjustment',n]); st.rerun()
    back_button('lic', ['Home','LIC'])

# =============================================================================
#  UPR CALCULATOR
# =============================================================================

def render_upr_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>UPR Calculator</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    with col1: valuation_date=st.date_input("Valuation Date",value=date(2025,12,31),key="upr_vd")
    with col2: client_name=st.text_input("Client Name",value="Client",key="upr_cn").strip()
    with col3: method=st.selectbox("Method",["365th","24th","8th"],key="upr_mt")
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
            st.dataframe(df.head())
            all_columns=df.columns.tolist()
            r1,r2=st.columns(2)
            with r1: start_date_col=st.selectbox("Start Date",[""]+all_columns,key="upr_sd",label_visibility="collapsed")
            with r2: end_date_col=st.selectbox("End Date",[""]+all_columns,key="upr_ed",label_visibility="collapsed")
            if not start_date_col or not end_date_col: st.error("Select date columns."); st.stop()
            grouping_options=[c for c in all_columns if c not in [start_date_col,end_date_col]]
            grouping_cols=st.multiselect("Group by:",options=grouping_options,default=[grouping_options[0]] if grouping_options else [],key="upr_gc")
            if not grouping_cols: st.error("Select grouping column."); st.stop()
            numeric_columns=[]
            for c in df.columns:
                if c in [start_date_col,end_date_col]+grouping_cols: continue
                try: pd.to_numeric(df[c]); numeric_columns.append(c)
                except: pass
            selected_value_cols=st.multiselect("Numeric columns:",options=numeric_columns,default=numeric_columns[:min(4,len(numeric_columns))],key="upr_vc")
            if not selected_value_cols: st.warning("Select numeric column."); st.stop()
            df_check=df.copy(); df_check=df_check.rename(columns={start_date_col:'Start_Date',end_date_col:'End_Date'})
            df_check['Start_Date']=pd.to_datetime(df_check['Start_Date'],errors='coerce')
            df_check['End_Date']=pd.to_datetime(df_check['End_Date'],errors='coerce')
            bad=df_check.dropna(subset=['Start_Date','End_Date']); bad=bad[bad['End_Date']<=bad['Start_Date']]
            if len(bad)>0: st.error(f"{len(bad)} rows with End_Date <= Start_Date."); st.stop()
            df_processed=df_check.dropna(subset=['Start_Date','End_Date'])
            df_processed=df_processed[df_processed['End_Date']>df_processed['Start_Date']]
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce')
            df_processed["Duration"]=(df_processed["End_Date"]-df_processed["Start_Date"]).dt.days
            df_processed=df_processed[df_processed["Duration"]>0]
            if df_processed.empty: st.error("No valid policies."); st.stop()
            if st.button("Calculate UPR",key="upr_calc",use_container_width=True):
                with st.spinner("Calculating..."):
                    cond=[valuation_date<df_processed["Start_Date"],valuation_date>df_processed["End_Date"],(valuation_date<=df_processed["End_Date"])&(valuation_date>=df_processed["Start_Date"])]
                    if method=="365th": t=df_processed["Duration"]; r=(df_processed["End_Date"]-valuation_date).dt.days; ch=[1,0,r/t]
                    elif method=="24th": iv=365.25/24; t=df_processed["Duration"]/iv; r=(df_processed["End_Date"]-valuation_date).dt.days/iv; ch=[1,0,r/t]
                    else: iv=365.25/8; t=df_processed["Duration"]/iv; r=(df_processed["End_Date"]-valuation_date).dt.days/iv; ch=[1,0,r/t]
                    df_processed["Unearned"]=np.select(cond,ch,default=np.nan)
                    for c in selected_value_cols: df_processed[f"{c}_UPR"]=df_processed["Unearned"]*df_processed[c]
                    upr_c=[f"{c}_UPR" for c in selected_value_cols]
                    result=df_processed.groupby(grouping_cols)[upr_c].sum().reset_index()
                    result.columns=grouping_cols+[c.replace('_UPR','') for c in upr_c]
                    st.subheader("UPR Results")
                    disp=result.copy()
                    for c in disp.columns:
                        if c not in grouping_cols: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                    st.dataframe(disp,use_container_width=True)
                    output=BytesIO()
                    with pd.ExcelWriter(output,engine='openpyxl') as w: result.to_excel(w,index=False,sheet_name='UPR_Results')
                    output.seek(0)
                    sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                    so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
                    st.download_button("Download Excel",data=output,file_name=f"{sc}_{so}_UPR_Results.xlsx",key="upr_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('lrc',['Home','LRC'])

# =============================================================================
#  LOSS COMPONENT
# =============================================================================

def render_loss_component():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Loss Component Calculator</h1></div>', unsafe_allow_html=True)
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
            st.dataframe(df.head())
            all_columns=df.columns.tolist()
            required_fields={'Line_of_business':'LOB','Gross_Written_Premiums':'GWP','Gross_Attributable_Expenses':'Expenses','Gross_Commission_Paid':'Commission','Gross_Paid_Claims':'Paid Claims','Gross_Opening_OCR':'Open OCR','Gross_Closing_OCR':'Close OCR','Gross_Opening_IBNR':'Open IBNR','Gross_Closing_IBNR':'Close IBNR','Gross_Opening_UPR':'Open UPR','Gross_Closing_UPR':'Close UPR','Gross_Risk_Adjustment':'RA'}
            mapped_columns={}
            field_list=list(required_fields.keys())
            for i in range(0,len(field_list),3):
                cols=st.columns(3)
                for j in range(3):
                    if i+j<len(field_list):
                        field=field_list[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="required-container"><h3>{field}</h3></div>',unsafe_allow_html=True)
                            mapped_columns[field]=st.selectbox(f"Select",[""]+all_columns,key=f"lc_m_{field}",label_visibility="collapsed")
                            if mapped_columns[field]=="": mapped_columns[field]=None
            missing=[f for f,c in mapped_columns.items() if c is None]
            if missing: st.error(f"Missing: {', '.join(missing)}"); st.stop()
            df_processed=df.rename(columns=mapped_columns)
            df_processed["Incurred_Claims"]=(df_processed["Gross_Paid_Claims"]+df_processed["Gross_Closing_IBNR"]+df_processed["Gross_Closing_OCR"]-df_processed["Gross_Opening_IBNR"]-df_processed["Gross_Opening_OCR"])
            df_processed["Earned_Premiums"]=(df_processed["Gross_Written_Premiums"]+df_processed["Gross_Opening_UPR"]-df_processed["Gross_Closing_UPR"])
            result=df_processed.groupby('Line_of_business').agg({'Gross_Written_Premiums':'sum','Earned_Premiums':'sum','Incurred_Claims':'sum','Gross_Commission_Paid':'sum','Gross_Attributable_Expenses':'sum','Gross_Risk_Adjustment':'sum','Gross_Closing_IBNR':'sum','Gross_Closing_OCR':'sum','Gross_Closing_UPR':'sum'}).reset_index()
            result['Loss_Ratio']=np.where(result['Earned_Premiums']!=0,result['Incurred_Claims']/result['Earned_Premiums'],np.nan)
            result['Commission_Ratio']=np.where(result['Gross_Written_Premiums']!=0,result['Gross_Commission_Paid']/result['Gross_Written_Premiums'],np.nan)
            result['Expense_Ratio']=np.where(result['Gross_Written_Premiums']!=0,result['Gross_Attributable_Expenses']/result['Gross_Written_Premiums'],np.nan)
            ra_denom=result['Gross_Closing_IBNR']+result['Gross_Closing_OCR']
            result['RA_Ratio']=np.where(ra_denom!=0,result['Gross_Risk_Adjustment']/ra_denom,np.nan)
            result['Combined_Ratio']=result['Loss_Ratio']+result['Commission_Ratio']+result['Expense_Ratio']+result['RA_Ratio']
            result['Loss_Component']=np.maximum(result['Combined_Ratio']-1,0)*result['Gross_Closing_UPR']
            st.subheader("Results")
            disp=result.copy()
            for c in disp.columns:
                if c!='Line_of_business': disp[c]=disp[c].apply(lambda x: f"{x:.2%}" if 'Ratio' in c and pd.notna(x) else (f"{x:,.2f}" if pd.notna(x) else "N/A"))
            st.dataframe(disp,use_container_width=True)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: result.to_excel(w,index=False,sheet_name='Loss_Component')
            output.seek(0)
            sc="".join(c for c in client_name if c.isalnum() or c in (' ','-','_')).rstrip() or "Client"
            st.download_button("Download Excel",data=output,file_name=f"{sc}_Loss_Component.xlsx",key="lc_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('lrc',['Home','LRC'])

# =============================================================================
#  OCR
# =============================================================================

def render_ocr_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>OCR Calculator</h1></div>', unsafe_allow_html=True)
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
            st.dataframe(df.head())
            all_columns=df.columns.tolist()
            grouping_cols=st.multiselect("Group by:",options=all_columns,default=[all_columns[0]] if all_columns else [],key="ocr_gc")
            if not grouping_cols: st.error("Select grouping column."); st.stop()
            numeric_columns=df.select_dtypes(include=[np.number]).columns.tolist()
            numeric_columns=[c for c in numeric_columns if c not in grouping_cols]
            selected_value_cols=st.multiselect("Numeric columns:",options=numeric_columns,default=numeric_columns[:min(5,len(numeric_columns))],key="ocr_vc")
            if not selected_value_cols: st.warning("Select numeric column."); st.stop()
            df_processed=df[grouping_cols+selected_value_cols].copy()
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce').fillna(0)
            grouped=df_processed.groupby(grouping_cols)[selected_value_cols].sum().reset_index()
            st.subheader("Results")
            disp=grouped.copy()
            for c in selected_value_cols: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(disp,use_container_width=True)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: grouped.to_excel(w,index=False,sheet_name='OCR_Results')
            output.seek(0)
            sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
            so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
            st.download_button("Download Excel",data=output,file_name=f"{sc}_{so}_OCR_Results.xlsx",key="ocr_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

# =============================================================================
#  IBNR PERCENTAGE
# =============================================================================

def render_ibnr_percentage():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>IBNR Percentage Method</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    client_name=st.text_input("Client Name",value="Client",key="ibp_cn",label_visibility="collapsed").strip()
    c1,c2=st.columns(2)
    with c1: from_date=st.date_input("From",value=date(2020,1,1),key="ibp_fd",label_visibility="collapsed")
    with c2: to_date=st.date_input("To",value=date(2024,12,31),key="ibp_td",label_visibility="collapsed")
    from_date=pd.to_datetime(from_date); to_date=pd.to_datetime(to_date)
    ibnr_pct=st.number_input("IBNR %",0.0,100.0,10.0,0.5,key="ibp_pct",label_visibility="collapsed")/100
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
            all_cols=df.columns.tolist()
            c1,c2=st.columns(2)
            with c1: date_col=st.selectbox("Date",["Select..."]+all_cols,key="ibp_dc")
            with c2: lob_col=st.selectbox("LOB",["Select..."]+all_cols,key="ibp_lc")
            if date_col=="Select..." or lob_col=="Select...": st.warning("Select both."); st.stop()
            num_cols=[c for c in all_cols if c not in [date_col,lob_col]]
            amount_cols=st.multiselect("Amounts",num_cols,key="ibp_ac")
            if not amount_cols: st.warning("Select amount."); st.stop()
            df[date_col]=pd.to_datetime(df[date_col],errors='coerce')
            mask=(df[date_col]>=from_date)&(df[date_col]<=to_date)
            df_filtered=df[mask].copy()
            if df_filtered.empty: st.error("No data."); st.stop()
            premium_summary=df_filtered.groupby(lob_col)[amount_cols].sum().reset_index()
            ibnr_summary=premium_summary.copy()
            for c in amount_cols: ibnr_summary[f"{c}_IBNR"]=ibnr_summary[c]*ibnr_pct
            total_row={lob_col:"TOTAL"}
            for c in amount_cols: total_row[c]=premium_summary[c].sum(); total_row[f"{c}_IBNR"]=total_row[c]*ibnr_pct
            ibnr_summary=pd.concat([ibnr_summary,pd.DataFrame([total_row])],ignore_index=True)
            st.subheader("IBNR Summary")
            di=ibnr_summary.copy()
            for c in di.columns:
                if c!=lob_col: di[c]=di[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(di)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: ibnr_summary.to_excel(w,index=False,sheet_name='IBNR')
            output.seek(0)
            sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
            so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
            st.download_button("Download",data=output.getvalue(),file_name=f"{sc}_{so}_IBNR.xlsx",key="ibp_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

# =============================================================================
#  BCL
# =============================================================================

def render_bcl_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Basic Chain Ladder (BCL)</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client",value="Client",key="bcl_cn").strip()
    with col2: pass
    c1,c2,c3=st.columns(3)
    with c1: from_date=st.date_input("From",value=date(2021,1,1),key="bcl_fd")
    with c2: to_date=st.date_input("To",value=date(2025,12,31),key="bcl_td")
    with c3: grain=st.selectbox("Grain",["Yearly","Half-Yearly","Quarterly","Monthly"],key="bcl_gr")
    grain_map={"Yearly":"Y","Half-Yearly":"H","Quarterly":"Q","Monthly":"M"}
    grain_key=grain_map[grain]
    from_date_dt=pd.to_datetime(from_date); to_date_dt=pd.to_datetime(to_date)
    uploaded_file=st.file_uploader("Claims file",type=["csv","xlsx","xls"],key="bcl_f")
    if uploaded_file is not None:
        try:
            ext=uploaded_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(uploaded_file,encoding='utf-8')
                except: uploaded_file.seek(0); df=pd.read_csv(uploaded_file,encoding='cp1252')
            else: df=pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            all_cols=df.columns.tolist()
            c1,c2=st.columns(2)
            with c1: loss_col=st.selectbox("Loss Date",[""]+all_cols,key="bcl_lc")
            with c2: report_col=st.selectbox("Report Date",[""]+all_cols,key="bcl_rc")
            if not loss_col or not report_col: st.stop()
            remaining=[c for c in all_cols if c not in [loss_col,report_col]]
            grouping_cols=st.multiselect("Grouping",remaining,key="bcl_gc")
            num_cands=[c for c in df.columns if c not in [loss_col,report_col]+grouping_cols and pd.api.types.is_numeric_dtype(df[c])]
            amount_cols=st.multiselect("Amounts",num_cands,key="bcl_ac")
            if not amount_cols: st.stop()
            df[loss_col]=pd.to_datetime(df[loss_col],errors='coerce')
            df[report_col]=pd.to_datetime(df[report_col],errors='coerce')
            df=df.dropna(subset=[loss_col,report_col])
            df_filtered=df[(df[loss_col]>=from_date_dt)&(df[loss_col]<=to_date_dt)].copy()
            if df_filtered.empty: st.error("No data."); st.stop()
            if grain_key=='Y': n_periods=to_date_dt.year-from_date_dt.year+1
            elif grain_key=='M': n_periods=(to_date_dt.year-from_date_dt.year)*12+(to_date_dt.month-from_date_dt.month)+1
            elif grain_key=='Q': n_periods=(to_date_dt.year-from_date_dt.year)*4+((to_date_dt.month-1)//3-(from_date_dt.month-1)//3)+1
            else: n_periods=(to_date_dt.year-from_date_dt.year)*2+((to_date_dt.month-1)//6-(from_date_dt.month-1)//6)+1
            if grouping_cols: groups=df_filtered[grouping_cols].drop_duplicates().to_dict("records")
            else: groups=[{"__all__":"All"}]
            if st.button("Run BCL",key="bcl_run",use_container_width=True):
                all_summary=[]
                for grp in groups:
                    if "__all__" in grp: gdf=df_filtered.copy(); glabel="All"
                    else:
                        mask=pd.Series(True,index=df_filtered.index)
                        for col,val in grp.items(): mask&=(df_filtered[col]==val)
                        gdf=df_filtered[mask].copy(); glabel=" | ".join(str(v) for v in grp.values())
                    for ac in amount_cols:
                        gdf["__ap"]=gdf[loss_col].apply(lambda d: (d.year-from_date_dt.year) if grain_key=='Y' else ((d.year-from_date_dt.year)*12+(d.month-from_date_dt.month)))
                        gdf["__dp"]=gdf.apply(lambda r: max(0,min((r[report_col].year-r[loss_col].year) if grain_key=='Y' else ((r[report_col].year-r[loss_col].year)*12+(r[report_col].month-r[loss_col].month)),n_periods-1)),axis=1)
                        gdf=gdf[(gdf["__ap"]>=0)&(gdf["__ap"]<n_periods)]
                        pivot=gdf.pivot_table(index="__ap",columns="__dp",values=ac,aggfunc="sum")
                        for ap in range(n_periods):
                            if ap not in pivot.index: pivot.loc[ap]=np.nan
                        for dp in range(n_periods):
                            if dp not in pivot.columns: pivot[dp]=np.nan
                        inc=pivot.sort_index()[sorted(pivot.columns)].astype(float)
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp>=n_periods: inc.loc[ap,dp]=np.nan
                        cum=inc.copy()
                        for ap in inc.index:
                            has_obs=any(pd.notna(inc.loc[ap,dp]) for dp in inc.columns if ap+dp<n_periods)
                            if not has_obs: cum.loc[ap]=np.nan; continue
                            running=0.0
                            for dp in sorted(inc.columns):
                                if ap+dp<n_periods: v=inc.loc[ap,dp]; running+=v if pd.notna(v) else 0.0; cum.loc[ap,dp]=running
                                else: cum.loc[ap,dp]=np.nan
                        wc=cum.fillna(0)
                        n_ay,n_dp=wc.shape
                        factors=[]
                        for j in range(n_dp-1):
                            num,den=0.0,0.0
                            for i in range(n_ay):
                                if i+j+1<n_ay:
                                    c=wc.iloc[i,j]; n=wc.iloc[i,j+1]
                                    if c>0: num+=n; den+=c
                            factors.append(num/den if den>0 else 1.0)
                        completed=wc.copy().astype(float)
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs<0: continue
                            for j in range(last_obs,n_dp-1):
                                if j<len(factors):
                                    prev=completed.iloc[i,j]; completed.iloc[i,j+1]=prev*factors[j] if prev>0 else 0.0
                        ibnr_total=0.0
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs>=0:
                                current=wc.iloc[i,last_obs]; ultimate=completed.iloc[i,n_dp-1]
                                ibnr_total+=max(ultimate-current,0.0)
                        all_summary.append({"Group":glabel,"Amount":ac,"IBNR":ibnr_total})
                if all_summary:
                    st.dataframe(pd.DataFrame(all_summary),use_container_width=True)
                    output=BytesIO()
                    with pd.ExcelWriter(output,engine='openpyxl') as w: pd.DataFrame(all_summary).to_excel(w,index=False)
                    output.seek(0)
                    sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                    st.download_button("Download",data=output,file_name=f"{sc}_BCL.xlsx",key="bcl_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

# =============================================================================
#  CAPE COD
# =============================================================================

def render_capecod_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Cape Cod IBNR Calculator</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client",value="Client",key="cc_cn").strip()
    with col2: pass
    c1,c2,c3=st.columns(3)
    with c1: from_date=st.date_input("From",value=date(2021,1,1),key="cc_fd")
    with c2: to_date=st.date_input("To",value=date(2025,12,31),key="cc_td")
    with c3: grain=st.selectbox("Grain",["Yearly","Half-Yearly","Quarterly","Monthly"],key="cc_gr")
    grain_map={"Yearly":"Y","Half-Yearly":"H","Quarterly":"Q","Monthly":"M"}
    grain_key=grain_map[grain]
    from_date_dt=pd.to_datetime(from_date); to_date_dt=pd.to_datetime(to_date)
    claims_file=st.file_uploader("Claims file",type=["csv","xlsx","xls"],key="cc_cf")
    if claims_file is not None:
        try:
            ext=claims_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(claims_file,encoding='utf-8')
                except: claims_file.seek(0); df=pd.read_csv(claims_file,encoding='cp1252')
            else: df=pd.read_excel(claims_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            all_cols=df.columns.tolist()
            c1,c2=st.columns(2)
            with c1: loss_col=st.selectbox("Loss Date",[""]+all_cols,key="cc_lc")
            with c2: report_col=st.selectbox("Report Date",[""]+all_cols,key="cc_rc")
            if not loss_col or not report_col: st.stop()
            remaining=[c for c in all_cols if c not in [loss_col,report_col]]
            grouping_cols=st.multiselect("Grouping",remaining,key="cc_gc")
            num_cands=[c for c in df.columns if c not in [loss_col,report_col]+grouping_cols and pd.api.types.is_numeric_dtype(df[c])]
            amount_cols=st.multiselect("Amounts",num_cands,key="cc_ac")
            if not amount_cols: st.stop()
            df[loss_col]=pd.to_datetime(df[loss_col],errors='coerce')
            df[report_col]=pd.to_datetime(df[report_col],errors='coerce')
            df=df.dropna(subset=[loss_col,report_col])
            df_filtered=df[(df[loss_col]>=from_date_dt)&(df[loss_col]<=to_date_dt)].copy()
            if df_filtered.empty: st.error("No data."); st.stop()
            if grain_key=='Y': n_periods=to_date_dt.year-from_date_dt.year+1
            elif grain_key=='M': n_periods=(to_date_dt.year-from_date_dt.year)*12+(to_date_dt.month-from_date_dt.month)+1
            elif grain_key=='Q': n_periods=(to_date_dt.year-from_date_dt.year)*4+((to_date_dt.month-1)//3-(from_date_dt.month-1)//3)+1
            else: n_periods=(to_date_dt.year-from_date_dt.year)*2+((to_date_dt.month-1)//6-(from_date_dt.month-1)//6)+1
            if grouping_cols: unique_groups=sorted(df_filtered[grouping_cols[0]].unique())
            else: unique_groups=["All"]
            st.markdown("**Premium Data**")
            premium_file=st.file_uploader("Premium file",type=["csv","xlsx","xls"],key="cc_pf")
            premiums_dict={}
            if premium_file is not None:
                prem_ext=premium_file.name.split('.')[-1].lower()
                prem_df=pd.read_csv(premium_file) if prem_ext=='csv' else pd.read_excel(premium_file)
                prem_df.columns=prem_df.columns.astype(str).str.strip()
                prem_cols=prem_df.columns.tolist()
                pc=st.columns(min(3,len(unique_groups)))
                for i,g in enumerate(unique_groups):
                    with pc[i%3]:
                        sc=st.selectbox(f"Premium {g}",prem_cols,key=f"cc_pm_{g}")
                        if len(prem_df)==n_periods: premiums_dict[g]=pd.to_numeric(prem_df[sc],errors='coerce').fillna(0).tolist()
            if st.button("Run Cape Cod",key="cc_run",use_container_width=True) and all(len(v)>0 for v in premiums_dict.values()):
                if grouping_cols: groups=df_filtered[grouping_cols].drop_duplicates().to_dict("records")
                else: groups=[{"__all__":"All"}]
                all_summary=[]
                for grp in groups:
                    if "__all__" in grp: gdf=df_filtered.copy(); glabel="All"
                    else:
                        mask=pd.Series(True,index=df_filtered.index)
                        for col,val in grp.items(): mask&=(df_filtered[col]==val)
                        gdf=df_filtered[mask].copy(); glabel=" | ".join(str(v) for v in grp.values())
                    for ac in amount_cols:
                        gdf["__ap"]=gdf[loss_col].apply(lambda d: (d.year-from_date_dt.year) if grain_key=='Y' else ((d.year-from_date_dt.year)*12+(d.month-from_date_dt.month)))
                        gdf["__dp"]=gdf.apply(lambda r: max(0,min((r[report_col].year-r[loss_col].year) if grain_key=='Y' else ((r[report_col].year-r[loss_col].year)*12+(r[report_col].month-r[loss_col].month)),n_periods-1)),axis=1)
                        gdf=gdf[(gdf["__ap"]>=0)&(gdf["__ap"]<n_periods)]
                        pivot=gdf.pivot_table(index="__ap",columns="__dp",values=ac,aggfunc="sum")
                        for ap in range(n_periods):
                            if ap not in pivot.index: pivot.loc[ap]=np.nan
                        for dp in range(n_periods):
                            if dp not in pivot.columns: pivot[dp]=np.nan
                        inc=pivot.sort_index()[sorted(pivot.columns)].astype(float)
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp>=n_periods: inc.loc[ap,dp]=np.nan
                        cum=inc.copy()
                        for ap in inc.index:
                            has_obs=any(pd.notna(inc.loc[ap,dp]) for dp in inc.columns if ap+dp<n_periods)
                            if not has_obs: cum.loc[ap]=np.nan; continue
                            running=0.0
                            for dp in sorted(inc.columns):
                                if ap+dp<n_periods: v=inc.loc[ap,dp]; running+=v if pd.notna(v) else 0.0; cum.loc[ap,dp]=running
                                else: cum.loc[ap,dp]=np.nan
                        wc=cum.fillna(0)
                        n_ay,n_dp=wc.shape
                        factors=[]
                        for j in range(n_dp-1):
                            num,den=0.0,0.0
                            for i in range(n_ay):
                                if i+j+1<n_ay:
                                    c=wc.iloc[i,j]; n=wc.iloc[i,j+1]
                                    if c>0: num+=n; den+=c
                            factors.append(num/den if den>0 else 1.0)
                        cdfs=[]; running=1.0
                        for f in reversed(factors): running*=f; cdfs.insert(0,running)
                        pct_dev=[1/c if c>0 else 1.0 for c in cdfs]
                        gk=glabel.split(" | ")[0] if " | " in glabel else glabel
                        prems=premiums_dict.get(gk,premiums_dict.get("All",[0]*n_periods))
                        dev_cl=[]; used_up=[]
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs==-1: dev_cl.append(0); used_up.append(0); continue
                            cur=wc.iloc[i,last_obs]
                            pdv=pct_dev[last_obs] if last_obs<len(pct_dev) else 1.0
                            dev_cl.append(cur); used_up.append(prems[i]*pdv)
                        td=sum(dev_cl); tu=sum(used_up)
                        cc_lr=td/tu if tu>0 else 0
                        cc_ibnr=0.0
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs>=0:
                                pdv=pct_dev[last_obs] if last_obs<len(pct_dev) else 1.0
                                cc_ibnr+=prems[i]*cc_lr*(1-pdv)
                        all_summary.append({"Group":glabel,"Amount":ac,"CC_LR":cc_lr,"CC_IBNR":cc_ibnr})
                if all_summary:
                    st.dataframe(pd.DataFrame(all_summary),use_container_width=True)
                    output=BytesIO()
                    with pd.ExcelWriter(output,engine='openpyxl') as w: pd.DataFrame(all_summary).to_excel(w,index=False)
                    output.seek(0)
                    sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                    st.download_button("Download",data=output,file_name=f"{sc}_CapeCod.xlsx",key="cc_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

# =============================================================================
#  BF
# =============================================================================

def render_bf_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Bornhuetter-Ferguson (BF)</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client",value="Client",key="bf_cn").strip()
    with col2: pass
    c1,c2,c3=st.columns(3)
    with c1: from_date=st.date_input("From",value=date(2021,1,1),key="bf_fd")
    with c2: to_date=st.date_input("To",value=date(2025,12,31),key="bf_td")
    with c3: grain=st.selectbox("Grain",["Yearly","Half-Yearly","Quarterly","Monthly"],key="bf_gr")
    grain_map={"Yearly":"Y","Half-Yearly":"H","Quarterly":"Q","Monthly":"M"}
    grain_key=grain_map[grain]
    from_date_dt=pd.to_datetime(from_date); to_date_dt=pd.to_datetime(to_date)
    claims_file=st.file_uploader("Claims",type=["csv","xlsx","xls"],key="bf_cf")
    if claims_file is not None:
        try:
            ext=claims_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df=pd.read_csv(claims_file,encoding='utf-8')
                except: claims_file.seek(0); df=pd.read_csv(claims_file,encoding='cp1252')
            else: df=pd.read_excel(claims_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            all_cols=df.columns.tolist()
            c1,c2=st.columns(2)
            with c1: loss_col=st.selectbox("Loss Date",[""]+all_cols,key="bf_lc")
            with c2: report_col=st.selectbox("Report Date",[""]+all_cols,key="bf_rc")
            if not loss_col or not report_col: st.stop()
            remaining=[c for c in all_cols if c not in [loss_col,report_col]]
            grouping_cols=st.multiselect("Grouping",remaining,key="bf_gc")
            num_cands=[c for c in df.columns if c not in [loss_col,report_col]+grouping_cols and pd.api.types.is_numeric_dtype(df[c])]
            amount_cols=st.multiselect("Amounts",num_cands,key="bf_ac")
            if not amount_cols: st.stop()
            df[loss_col]=pd.to_datetime(df[loss_col],errors='coerce')
            df[report_col]=pd.to_datetime(df[report_col],errors='coerce')
            df=df.dropna(subset=[loss_col,report_col])
            df_filtered=df[(df[loss_col]>=from_date_dt)&(df[loss_col]<=to_date_dt)].copy()
            if df_filtered.empty: st.error("No data."); st.stop()
            if grain_key=='Y': n_periods=to_date_dt.year-from_date_dt.year+1
            elif grain_key=='M': n_periods=(to_date_dt.year-from_date_dt.year)*12+(to_date_dt.month-from_date_dt.month)+1
            elif grain_key=='Q': n_periods=(to_date_dt.year-from_date_dt.year)*4+((to_date_dt.month-1)//3-(from_date_dt.month-1)//3)+1
            else: n_periods=(to_date_dt.year-from_date_dt.year)*2+((to_date_dt.month-1)//6-(from_date_dt.month-1)//6)+1
            if grouping_cols: unique_groups=sorted(df_filtered[grouping_cols[0]].unique())
            else: unique_groups=["All"]
            st.markdown("**ELR per Group**")
            elr_dict={}
            ec=st.columns(min(3,len(unique_groups)))
            for i,g in enumerate(unique_groups):
                with ec[i%3]: elr_dict[g]=st.number_input(f"ELR {g} %",0.0,200.0,70.0,1.0,key=f"bf_elr_{g}")/100
            premium_file=st.file_uploader("Premium",type=["csv","xlsx","xls"],key="bf_pf")
            premiums_dict={}
            if premium_file is not None:
                prem_ext=premium_file.name.split('.')[-1].lower()
                prem_df=pd.read_csv(premium_file) if prem_ext=='csv' else pd.read_excel(premium_file)
                prem_df.columns=prem_df.columns.astype(str).str.strip()
                prem_cols=prem_df.columns.tolist()
                pc=st.columns(min(3,len(unique_groups)))
                for i,g in enumerate(unique_groups):
                    with pc[i%3]:
                        sc=st.selectbox(f"Premium {g}",prem_cols,key=f"bf_pm_{g}")
                        if len(prem_df)==n_periods: premiums_dict[g]=pd.to_numeric(prem_df[sc],errors='coerce').fillna(0).tolist()
            if st.button("Run BF",key="bf_run",use_container_width=True) and all(len(v)>0 for v in premiums_dict.values()):
                if grouping_cols: groups=df_filtered[grouping_cols].drop_duplicates().to_dict("records")
                else: groups=[{"__all__":"All"}]
                all_summary=[]
                for grp in groups:
                    if "__all__" in grp: gdf=df_filtered.copy(); glabel="All"
                    else:
                        mask=pd.Series(True,index=df_filtered.index)
                        for col,val in grp.items(): mask&=(df_filtered[col]==val)
                        gdf=df_filtered[mask].copy(); glabel=" | ".join(str(v) for v in grp.values())
                    for ac in amount_cols:
                        gdf["__ap"]=gdf[loss_col].apply(lambda d: (d.year-from_date_dt.year) if grain_key=='Y' else ((d.year-from_date_dt.year)*12+(d.month-from_date_dt.month)))
                        gdf["__dp"]=gdf.apply(lambda r: max(0,min((r[report_col].year-r[loss_col].year) if grain_key=='Y' else ((r[report_col].year-r[loss_col].year)*12+(r[report_col].month-r[loss_col].month)),n_periods-1)),axis=1)
                        gdf=gdf[(gdf["__ap"]>=0)&(gdf["__ap"]<n_periods)]
                        pivot=gdf.pivot_table(index="__ap",columns="__dp",values=ac,aggfunc="sum")
                        for ap in range(n_periods):
                            if ap not in pivot.index: pivot.loc[ap]=np.nan
                        for dp in range(n_periods):
                            if dp not in pivot.columns: pivot[dp]=np.nan
                        inc=pivot.sort_index()[sorted(pivot.columns)].astype(float)
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp>=n_periods: inc.loc[ap,dp]=np.nan
                        cum=inc.copy()
                        for ap in inc.index:
                            has_obs=any(pd.notna(inc.loc[ap,dp]) for dp in inc.columns if ap+dp<n_periods)
                            if not has_obs: cum.loc[ap]=np.nan; continue
                            running=0.0
                            for dp in sorted(inc.columns):
                                if ap+dp<n_periods: v=inc.loc[ap,dp]; running+=v if pd.notna(v) else 0.0; cum.loc[ap,dp]=running
                                else: cum.loc[ap,dp]=np.nan
                        wc=cum.fillna(0)
                        n_ay,n_dp=wc.shape
                        factors=[]
                        for j in range(n_dp-1):
                            num,den=0.0,0.0
                            for i in range(n_ay):
                                if i+j+1<n_ay:
                                    c=wc.iloc[i,j]; n=wc.iloc[i,j+1]
                                    if c>0: num+=n; den+=c
                            factors.append(num/den if den>0 else 1.0)
                        cdfs=[]; running=1.0
                        for f in reversed(factors): running*=f; cdfs.insert(0,running)
                        pct_unpaid=[1-(1/c) if c>0 else 0 for c in cdfs]
                        gk=glabel.split(" | ")[0] if " | " in glabel else glabel
                        gelr=elr_dict.get(gk,elr_dict.get("All",0.7))
                        prems=premiums_dict.get(gk,premiums_dict.get("All",[0]*n_periods))
                        bf_ibnr=0.0
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs>=0:
                                eu=prems[i]*gelr
                                if last_obs<len(pct_unpaid): bf_ibnr+=eu*pct_unpaid[last_obs]
                        all_summary.append({"Group":glabel,"Amount":ac,"ELR":gelr,"BF_IBNR":bf_ibnr})
                if all_summary:
                    st.dataframe(pd.DataFrame(all_summary),use_container_width=True)
                    output=BytesIO()
                    with pd.ExcelWriter(output,engine='openpyxl') as w: pd.DataFrame(all_summary).to_excel(w,index=False)
                    output.seek(0)
                    sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                    st.download_button("Download",data=output,file_name=f"{sc}_BF.xlsx",key="bf_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

# =============================================================================
#  ULAE — COMPLETE
# =============================================================================

def render_ulae_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>ULAE Calculator</h1><p>ULAE = ULAE_Ratio x (50% x OCR + IBNR)</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client",value="Client",key="ulae_cn").strip()
    with col2: pass
    data_format=st.radio("Reserves format:",["Detailed (OCR+IBNR)","Summary (Total)"],key="ulae_df")
    is_detailed=data_format.startswith("Detailed")
    reserves_file=st.file_uploader("Reserves file",type=["csv","xlsx","xls"],key="ulae_rf")
    if reserves_file is not None:
        try:
            ext=reserves_file.name.split('.')[-1].lower()
            if ext=='csv':
                try: df_res=pd.read_csv(reserves_file,encoding='utf-8')
                except: reserves_file.seek(0); df_res=pd.read_csv(reserves_file,encoding='cp1252')
            else: df_res=pd.read_excel(reserves_file)
            unnamed=[c for c in df_res.columns if c.startswith('Unnamed:')]
            if unnamed: df_res=df_res.drop(columns=unnamed)
            all_cols=df_res.columns.tolist()
            portfolio_col=st.selectbox("Portfolio",[""]+all_cols,key="ulae_pc")
            if not portfolio_col: st.stop()
            df_res=df_res.rename(columns={portfolio_col:"Portfolio"})
            if is_detailed:
                c1,c2=st.columns(2)
                with c1: ocr_col=st.selectbox("OCR",[""]+[c for c in all_cols if c!=portfolio_col],key="ulae_oc")
                with c2: ibnr_col=st.selectbox("IBNR",[""]+[c for c in all_cols if c!=portfolio_col],key="ulae_ic")
                if not ocr_col or not ibnr_col: st.stop()
                df_res=df_res.rename(columns={ocr_col:"OCR",ibnr_col:"IBNR"})
                df_res["OCR"]=pd.to_numeric(df_res["OCR"],errors='coerce').fillna(0)
                df_res["IBNR"]=pd.to_numeric(df_res["IBNR"],errors='coerce').fillna(0)
                df_res["Total"]=df_res["OCR"]+df_res["IBNR"]
            else:
                total_col=st.selectbox("Total",[""]+[c for c in all_cols if c!=portfolio_col],key="ulae_tc")
                if not total_col: st.stop()
                df_res=df_res.rename(columns={total_col:"Total"})
                df_res["Total"]=pd.to_numeric(df_res["Total"],errors='coerce').fillna(0)
                df_res["OCR"]=np.nan; df_res["IBNR"]=np.nan
            portfolios=df_res["Portfolio"].dropna().unique().tolist()
            basis=st.radio("Basis:",["Per Portfolio","Aggregated"],key="ulae_bs")
            apportionment_df=None
            if basis.startswith("Aggregated"):
                app_file=st.file_uploader("Apportionment file",type=["csv","xlsx","xls"],key="ulae_af")
                if app_file is not None:
                    app_ext=app_file.name.split('.')[-1].lower()
                    app_df=pd.read_csv(app_file) if app_ext=='csv' else pd.read_excel(app_file)
                    app_cols=app_df.columns.tolist()
                    c1,c2=st.columns(2)
                    with c1: apc=st.selectbox("Portfolio",[""]+app_cols,key="ulae_apc")
                    with c2: aac=st.selectbox("Amount",[""]+app_cols,key="ulae_aac")
                    if apc and aac:
                        app_df=app_df.rename(columns={apc:"Portfolio",aac:"Amount"})
                        app_df["Amount"]=pd.to_numeric(app_df["Amount"],errors='coerce').fillna(0)
                        ta=app_df["Amount"].sum()
                        app_df["Pct"]=app_df["Amount"]/ta if ta>0 else 0
                        apportionment_df=app_df
            ratio_method=st.radio("Ratio:",["Overall","Per Portfolio","From File"],key="ulae_rm")
            ulae_ratios={}
            if ratio_method=="Overall":
                op=st.number_input("ULAE %",0.0,100.0,5.0,0.5,key="ulae_op")/100
                ulae_ratios={p:op for p in portfolios}
            elif ratio_method=="Per Portfolio":
                ec=st.columns(min(3,len(portfolios)))
                for i,p in enumerate(portfolios):
                    with ec[i%3]: ulae_ratios[p]=st.number_input(f"{p} %",0.0,100.0,5.0,0.5,key=f"ulae_r_{p}")/100
            else:
                rf=st.file_uploader("Ratio file",type=["csv","xlsx","xls"],key="ulae_rf2")
                if rf is not None:
                    rext=rf.name.split('.')[-1].lower()
                    rdf=pd.read_csv(rf) if rext=='csv' else pd.read_excel(rf)
                    rcols=rdf.columns.tolist()
                    c1,c2=st.columns(2)
                    with c1: rpc=st.selectbox("Portfolio",[""]+rcols,key="ulae_rpc")
                    with c2: rrc=st.selectbox("Ratio",[""]+rcols,key="ulae_rrc")
                    if rpc and rrc:
                        rdf=rdf.rename(columns={rpc:"Portfolio",rrc:"Ratio"})
                        rdf["Ratio"]=pd.to_numeric(rdf["Ratio"],errors='coerce')/100
                        ulae_ratios=dict(zip(rdf["Portfolio"],rdf["Ratio"]))
                        for p in portfolios:
                            if p not in ulae_ratios: ulae_ratios[p]=0.0
            if st.button("Calculate ULAE",key="ulae_run",use_container_width=True) and ulae_ratios:
                results=df_res.copy()
                results["ULAE_Ratio"]=results["Portfolio"].map(ulae_ratios).fillna(0)
                if is_detailed: results["ULAE_Base"]=0.5*results["OCR"]+results["IBNR"]
                else: results["ULAE_Base"]=results["Total"]
                if basis.startswith("Aggregated") and apportionment_df is not None:
                    or_val=list(ulae_ratios.values())[0]
                    tb=results["ULAE_Base"].sum()
                    tulae=tb*or_val
                    results=results.merge(apportionment_df[["Portfolio","Pct"]],on="Portfolio",how="left")
                    results["Pct"]=results["Pct"].fillna(0)
                    results["ULAE"]=tulae*results["Pct"]
                else: results["ULAE"]=results["ULAE_Ratio"]*results["ULAE_Base"]
                st.subheader("ULAE Results")
                disp=results[["Portfolio","OCR","IBNR","Total","ULAE_Ratio","ULAE_Base","ULAE"]].copy()
                for c in disp.columns:
                    if c=="Portfolio": continue
                    if "Ratio" in c: disp[c]=disp[c].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
                    else: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                st.dataframe(disp,use_container_width=True)
                st.metric("Total ULAE",f"{results['ULAE'].sum():,.2f}")
                output=BytesIO()
                with pd.ExcelWriter(output,engine='openpyxl') as w: results.to_excel(w,index=False)
                output.seek(0)
                sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                st.download_button("Download",data=output,file_name=f"{sc}_ULAE.xlsx",key="ulae_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

# =============================================================================
#  PLACEHOLDERS
# =============================================================================

def render_elr_calculator():
    show_breadcrumb(); st.markdown("## ELR"); st.info("Pending"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_acpc_calculator():
    show_breadcrumb(); st.markdown("## ACPC"); st.info("Pending"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_npr_calculator():
    show_breadcrumb(); st.markdown("## NPR"); st.info("Pending"); back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def render_mack_calculator():
    show_breadcrumb(); st.markdown("## Mack"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_bootstrap_calculator():
    show_breadcrumb(); st.markdown("## Bootstrap"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_var_calculator():
    show_breadcrumb(); st.markdown("## VaR"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_coc_calculator():
    show_breadcrumb(); st.markdown("## Cost of Capital"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

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

st.markdown('<div class="footer"><p>2026 African Actuarial Consultants. All rights reserved.</p></div>', unsafe_allow_html=True)
