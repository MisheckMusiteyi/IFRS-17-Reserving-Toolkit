# -*- coding: utf-8 -*-
# =============================================================================
#  NEXT VANTAGE — COMPREHENSIVE ACTUARIAL TOOLKIT
#  Main App with Multi-Page Navigation
#  Theme: Light Blue (#4A90D9), Black, White
#  Run:  streamlit run app.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date, datetime
import re
from scipy import interpolate

st.set_page_config(page_title="Next Vantage Actuarial Toolkit", layout="wide", initial_sidebar_state="expanded")

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
    .dataframe { border: 1px solid #4A90D9 !important; border-radius: 8px !important; overflow: hidden !important; }
    .stSelectbox [data-baseweb="select"], .stMultiSelect [data-baseweb="select"] { border: 1px solid #4A90D9 !important; border-radius: 4px !important; }
    .required-container { background-color: #F9F9F9; border: 2px solid #4A90D9; border-radius: 10px; padding: 1rem; text-align: center; min-height: 120px; margin-bottom: 1rem; }
    .required-container h3 { color: #4A90D9; font-size: 1.2rem; font-weight: bold; }
    .main-container { max-width: 1400px; margin: 2rem auto; padding: 0 2rem; }
    .report-meta { background-color: #F0F4F8; border: 2px solid #4A90D9; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; font-size: 0.85rem; }
    .report-meta td { padding: 2px 8px; }
    .rollforward-table { font-size: 0.85rem; }
    .rollforward-table th { background-color: #4A90D9; color: #FFFFFF; padding: 6px; text-align: center; }
    .rollforward-table td { padding: 4px 8px; border: 1px solid #ddd; }
    .rollforward-table .lob-header { background-color: #E3F2FD; font-weight: bold; }
    .rollforward-table .total-row { background-color: #000000; color: #FFFFFF; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
#  SESSION STATE & NAVIGATION
# =============================================================================

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'breadcrumb' not in st.session_state: st.session_state.breadcrumb = ['Home']
if 'report_metadata' not in st.session_state: st.session_state.report_metadata = {}
if 'fv_results' not in st.session_state: st.session_state.fv_results = {}

def navigate_to(page, breadcrumb_label=None):
    st.session_state.page = page
    if breadcrumb_label: st.session_state.breadcrumb = breadcrumb_label

def go_home():
    st.session_state.page = 'home'; st.session_state.breadcrumb = ['Home']

st.markdown('<div class="header"><div class="logo">Next Vantage Actuarial Toolkit</div><div class="nav-links"><a href="javascript:void(0)" onclick="window.location.reload()">Home</a></div></div>', unsafe_allow_html=True)

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
#  HELPER: Map columns for uploaded files
# =============================================================================

def map_columns(df, required_fields, file_label):
    """Interactive column mapping for uploaded data files."""
    all_cols = df.columns.tolist()
    mapped = {}
    st.markdown(f"**Map columns for {file_label}:**")
    cols_per_row = min(3, len(required_fields))
    for i in range(0, len(required_fields), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(required_fields):
                field = required_fields[idx]
                with row_cols[j]:
                    default_val = field if field in all_cols else (all_cols[idx] if idx < len(all_cols) else "")
                    default_idx = all_cols.index(default_val) if default_val in all_cols else 0
                    mapped[field] = st.selectbox(f"{field}", all_cols, index=default_idx, key=f"fv_map_{file_label}_{field}")
    return mapped

# =============================================================================
#  NAVIGATION MENUS
# =============================================================================

def render_home():
    st.markdown('<div class="hero"><h1>Next Vantage</h1><p>Comprehensive Actuarial Reserving Toolkit — IFRS 17 Compliant</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><h3>Full IFRS 17 Valuation</h3><p>Complete valuation with Income Statement & Liability Rollforward per LOB</p></div>', unsafe_allow_html=True)
        if st.button("Full Valuation", key="nav_home_full"): navigate_to('full_valuation', ['Home','Full Valuation']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Individual Calculators</h3><p>LRC | LIC | Risk Adjustment — standalone tools</p></div>', unsafe_allow_html=True)
        if st.button("Go to Calculators", key="nav_home_calc"): navigate_to('lrc', ['Home','Individual Calculators','LRC']); st.rerun()
    with col3:
        st.markdown('<div class="card"><h3>LIC — Liability for Incurred Claims</h3><p>Fulfilment Cashflows | Risk Adjustment</p></div>', unsafe_allow_html=True)
        if st.button("Go to LIC", key="nav_home_lic"): navigate_to('lic', ['Home','LIC']); st.rerun()

def render_full_valuation():
    """Full IFRS 17 Valuation Mode with per-LOB rollforwards."""
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Full IFRS 17 Valuation</h1><p>Complete valuation with Income Statement & Liability Rollforward per Line of Business</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # ---- REPORT METADATA ----
    st.markdown('<div class="section-container"><h3>Report Metadata</h3></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: report_created_by = st.text_input("Created By", value="", key="fv_cb")
    with c2: report_version = st.text_input("Version", value="3.9.29.3", key="fv_ver")
    with c3: report_client = st.text_input("Client Name", value="", key="fv_client")
    with c4: report_date = st.date_input("Valuation Date", value=date.today(), key="fv_vd")
    
    run_id = f"DN{hash(str(datetime.now())):x}"[:40]
    st.markdown(f"""
    <div class="report-meta">
    <table>
    <tr><td><b>Creation:</b></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
    <tr><td><b>Created By:</b></td><td>{report_created_by or '(not set)'}</td></tr>
    <tr><td><b>Version:</b></td><td>{report_version}</td></tr>
    <tr><td><b>Run ID:</b></td><td style="font-size:0.75rem;">{run_id}</td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.report_metadata = {
        'created_by': report_created_by, 'version': report_version,
        'client': report_client, 'valuation_date': str(report_date),
        'run_id': run_id, 'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # ---- SELECT RESERVES ----
    st.markdown('<div class="section-container"><h3>Select Reserves to Calculate</h3></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: calc_upr = st.checkbox("UPR (LRC)", value=True, key="fv_upr")
    with c2: calc_ocr = st.checkbox("OCR (LIC)", value=True, key="fv_ocr")
    with c3: calc_ibnr = st.checkbox("IBNR - BCL (LIC)", value=True, key="fv_ibnr")
    with c4: calc_ulae = st.checkbox("ULAE (LIC)", value=True, key="fv_ulae")
    
    c1, c2 = st.columns(2)
    with c1: calc_ra = st.checkbox("RA - Bootstrap @90%", value=True, key="fv_ra")
    with c2: calc_npr = st.checkbox("NPR", value=False, key="fv_npr")
    
    selected = []
    if calc_upr: selected.append("UPR")
    if calc_ocr: selected.append("OCR")
    if calc_ibnr: selected.append("IBNR")
    if calc_ulae: selected.append("ULAE")
    if calc_ra: selected.append("RA")
    if calc_npr: selected.append("NPR")
    st.info(f"Selected: {', '.join(selected) if selected else 'None'}")
    
    # ---- DATA FILES WITH COLUMN MAPPING ----
    st.markdown('<div class="section-container"><h3>Upload Data Files & Map Columns</h3></div>', unsafe_allow_html=True)
    
    upr_data = None; ocr_data = None; claims_data = None
    apportionment_data = None; cashflow_data = None; opening_data = None
    
    if calc_upr:
        st.markdown("#### UPR Data (Premium Register)")
        upr_file = st.file_uploader("Upload UPR file", type=["csv","xlsx","xls"], key="fv_upr_f")
        if upr_file is not None:
            try:
                upr_df = pd.read_csv(upr_file) if upr_file.name.endswith('.csv') else pd.read_excel(upr_file)
                upr_df.columns = upr_df.columns.astype(str).str.strip()
                st.dataframe(upr_df.head(3), use_container_width=True)
                upr_map = map_columns(upr_df, ['Start_Date','End_Date','Line_of_Business','Gross_Written_Premium'], 'UPR')
                upr_data = upr_df.rename(columns=upr_map)
                st.success("UPR columns mapped.")
            except Exception as e: st.error(f"Error: {e}")
    
    if calc_ocr:
        st.markdown("#### OCR Data (Case Estimates)")
        ocr_file = st.file_uploader("Upload OCR file", type=["csv","xlsx","xls"], key="fv_ocr_f")
        if ocr_file is not None:
            try:
                ocr_df = pd.read_csv(ocr_file) if ocr_file.name.endswith('.csv') else pd.read_excel(ocr_file)
                ocr_df.columns = ocr_df.columns.astype(str).str.strip()
                st.dataframe(ocr_df.head(3), use_container_width=True)
                ocr_map = map_columns(ocr_df, ['Line_of_Business','Case_Reserve'], 'OCR')
                ocr_data = ocr_df.rename(columns=ocr_map)
                st.success("OCR columns mapped.")
            except Exception as e: st.error(f"Error: {e}")
    
    if calc_ibnr or calc_ra:
        st.markdown("#### Claims Triangle Data")
        claims_file = st.file_uploader("Upload Claims file", type=["csv","xlsx","xls"], key="fv_cl_f")
        if claims_file is not None:
            try:
                cl_df = pd.read_csv(claims_file) if claims_file.name.endswith('.csv') else pd.read_excel(claims_file)
                cl_df.columns = cl_df.columns.astype(str).str.strip()
                st.dataframe(cl_df.head(3), use_container_width=True)
                cl_map = map_columns(cl_df, ['Loss_Date','Report_Date','Claim_Amount','Line_of_Business'], 'Claims')
                claims_data = cl_df.rename(columns=cl_map)
                st.success("Claims columns mapped.")
            except Exception as e: st.error(f"Error: {e}")
    
    if calc_ulae:
        st.markdown("#### ULAE Apportionment Key")
        app_file = st.file_uploader("Upload Apportionment file", type=["csv","xlsx","xls"], key="fv_ap_f")
        if app_file is not None:
            try:
                app_df = pd.read_csv(app_file) if app_file.name.endswith('.csv') else pd.read_excel(app_file)
                app_df.columns = app_df.columns.astype(str).str.strip()
                st.dataframe(app_df.head(3), use_container_width=True)
                app_map = map_columns(app_df, ['Portfolio','Premiums_Received'], 'Apportionment')
                apportionment_data = app_df.rename(columns=app_map)
                st.success("Apportionment columns mapped.")
            except Exception as e: st.error(f"Error: {e}")
    
    st.markdown("#### Cash Flow Data (for Income Statement)")
    cf_file = st.file_uploader("Upload Cash Flow file", type=["csv","xlsx","xls"], key="fv_cf")
    if cf_file is not None:
        try:
            cf_df = pd.read_csv(cf_file) if cf_file.name.endswith('.csv') else pd.read_excel(cf_file)
            cf_df.columns = cf_df.columns.astype(str).str.strip()
            st.dataframe(cf_df.head(3), use_container_width=True)
            cf_map = map_columns(cf_df, ['Portfolio','Premiums_Received','Paid_Claims_Gross','Acquisition_Costs','Maintenance_Expenses'], 'CashFlow')
            cashflow_data = cf_df.rename(columns=cf_map)
            st.success("Cash flow columns mapped.")
        except Exception as e: st.error(f"Error: {e}")
    
    st.markdown("#### Opening Balances")
    op_file = st.file_uploader("Upload Opening Balances file", type=["csv","xlsx","xls"], key="fv_ob")
    if op_file is not None:
        try:
            op_df = pd.read_csv(op_file) if op_file.name.endswith('.csv') else pd.read_excel(op_file)
            op_df.columns = op_df.columns.astype(str).str.strip()
            st.dataframe(op_df.head(3), use_container_width=True)
            op_map = map_columns(op_df, ['Portfolio','Opening_LRC_UPR','Opening_LIC_OCR','Opening_LIC_IBNR','Opening_LIC_ULAE','Opening_LIC_RA'], 'OpeningBal')
            opening_data = op_df.rename(columns=op_map)
            st.success("Opening balance columns mapped.")
        except Exception as e: st.error(f"Error: {e}")
    
    # ---- PARAMETERS ----
    st.markdown('<div class="section-container"><h3>Parameters</h3></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if calc_ulae: ulae_ratio = st.number_input("ULAE Ratio (%)", 0.0, 20.0, 5.0, 0.5, key="fv_ur") / 100
        else: ulae_ratio = 0.05
    with c2:
        if calc_ibnr: ibnr_grain = st.selectbox("IBNR Grain", ["Yearly","Half-Yearly","Quarterly","Monthly"], key="fv_ig")
        else: ibnr_grain = "Yearly"
    with c3:
        if calc_ra: ra_iters = st.number_input("Bootstrap Iterations", 100, 5000, 1000, 100, key="fv_ri")
        else: ra_iters = 1000
    
    # ---- CALCULATE ----
    if st.button("Run Full IFRS 17 Valuation", key="fv_run", use_container_width=True):
        if not selected:
            st.warning("Select at least one reserve.")
        else:
            with st.spinner("Running full IFRS 17 valuation..."):
                results = {}
                val_date = pd.to_datetime(report_date)
                from_dt = pd.to_datetime('2020-01-01')
                to_dt = pd.to_datetime('2025-12-31')
                n_periods_bcl = to_dt.year - from_dt.year + 1
                
                # Determine portfolios
                portfolios = []
                if upr_data is not None and 'Line_of_Business' in upr_data.columns:
                    portfolios = sorted(upr_data['Line_of_Business'].dropna().unique().tolist())
                elif ocr_data is not None and 'Line_of_Business' in ocr_data.columns:
                    portfolios = sorted(ocr_data['Line_of_Business'].dropna().unique().tolist())
                elif claims_data is not None and 'Line_of_Business' in claims_data.columns:
                    portfolios = sorted(claims_data['Line_of_Business'].dropna().unique().tolist())
                else:
                    portfolios = ["Motor","Property","Health","Engineering","Liability"]
                
                st.info(f"Portfolios detected: {', '.join(portfolios)}")
                
                # ---- UPR ----
                if calc_upr and upr_data is not None:
                    df_upr = upr_data.copy()
                    df_upr['Start_Date'] = pd.to_datetime(df_upr['Start_Date'], errors='coerce')
                    df_upr['End_Date'] = pd.to_datetime(df_upr['End_Date'], errors='coerce')
                    df_upr['Premium'] = pd.to_numeric(df_upr['Gross_Written_Premium'], errors='coerce')
                    df_upr = df_upr.dropna(subset=['Start_Date','End_Date'])
                    df_upr = df_upr[df_upr['End_Date'] > df_upr['Start_Date']]
                    df_upr['Duration'] = (df_upr['End_Date'] - df_upr['Start_Date']).dt.days
                    df_upr['Remaining'] = (df_upr['End_Date'] - val_date).dt.days
                    df_upr['Unearned'] = np.where(val_date < df_upr['Start_Date'], 1,
                        np.where(val_date > df_upr['End_Date'], 0,
                        np.clip(df_upr['Remaining'] / df_upr['Duration'], 0, 1)))
                    df_upr['UPR'] = df_upr['Unearned'] * df_upr['Premium']
                    upr_result = df_upr.groupby('Line_of_Business')['UPR'].sum().reset_index()
                    upr_result.columns = ['Portfolio','Closing_UPR']
                    results['UPR'] = upr_result
                    st.success(f"UPR calculated: {upr_result['Closing_UPR'].sum():,.2f}")
                
                # ---- OCR ----
                if calc_ocr and ocr_data is not None:
                    df_ocr = ocr_data.copy()
                    df_ocr['Reserve'] = pd.to_numeric(df_ocr['Case_Reserve'], errors='coerce')
                    ocr_result = df_ocr.groupby('Line_of_Business')['Reserve'].sum().reset_index()
                    ocr_result.columns = ['Portfolio','Closing_OCR']
                    results['OCR'] = ocr_result
                    st.success(f"OCR calculated: {ocr_result['Closing_OCR'].sum():,.2f}")
                
                # ---- IBNR (BCL) ----
                if calc_ibnr and claims_data is not None:
                    df_cl = claims_data.copy()
                    df_cl['Loss_Date'] = pd.to_datetime(df_cl['Loss_Date'], errors='coerce')
                    df_cl['Report_Date'] = pd.to_datetime(df_cl['Report_Date'], errors='coerce')
                    df_cl['Amount'] = pd.to_numeric(df_cl['Claim_Amount'], errors='coerce')
                    df_cl = df_cl.dropna(subset=['Loss_Date','Report_Date'])
                    df_cl = df_cl[(df_cl['Loss_Date']>=from_dt)&(df_cl['Loss_Date']<=to_dt)]
                    
                    ibnr_rows = []
                    for lob in portfolios:
                        lob_data = df_cl[df_cl['Line_of_Business']==lob].copy()
                        if len(lob_data)==0:
                            ibnr_rows.append({'Portfolio':lob,'Closing_IBNR':0})
                            continue
                        lob_data['AP'] = lob_data['Loss_Date'].apply(lambda d: d.year - from_dt.year)
                        lob_data['DP'] = lob_data.apply(lambda r: max(0, min(r['Report_Date'].year - r['Loss_Date'].year, n_periods_bcl-1)), axis=1)
                        pivot = lob_data.pivot_table(index='AP', columns='DP', values='Amount', aggfunc='sum')
                        for ap in range(n_periods_bcl):
                            if ap not in pivot.index: pivot.loc[ap] = np.nan
                        for dp in range(n_periods_bcl):
                            if dp not in pivot.columns: pivot[dp] = np.nan
                        inc = pivot.sort_index()[sorted(pivot.columns)].astype(float)
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp >= n_periods_bcl: inc.loc[ap, dp] = np.nan
                        cum = inc.copy()
                        for ap in inc.index:
                            has_obs = any(pd.notna(inc.loc[ap, dp]) for dp in inc.columns if ap+dp<n_periods_bcl)
                            if not has_obs: continue
                            running = 0.0
                            for dp in sorted(inc.columns):
                                if ap+dp<n_periods_bcl:
                                    v = inc.loc[ap, dp]; running += v if pd.notna(v) else 0.0; cum.loc[ap, dp] = running
                        wc = cum.fillna(0)
                        n_ay, n_dp = wc.shape
                        factors = []
                        for j in range(n_dp-1):
                            num, den = 0.0, 0.0
                            for i in range(n_ay):
                                if i+j+1<n_ay:
                                    c = wc.iloc[i,j]; n = wc.iloc[i,j+1]
                                    if c>0: num+=n; den+=c
                            factors.append(num/den if den>0 else 1.0)
                        completed = wc.copy().astype(float)
                        for i in range(n_ay):
                            last_obs = -1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs<0: continue
                            for j in range(last_obs, n_dp-1):
                                if j<len(factors):
                                    prev = completed.iloc[i,j]; completed.iloc[i,j+1] = prev*factors[j] if prev>0 else 0.0
                        ibnr_total = 0.0
                        for i in range(n_ay):
                            last_obs = -1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs>=0:
                                cur = wc.iloc[i,last_obs]; ult = completed.iloc[i,n_dp-1]
                                ibnr_total += max(ult-cur, 0.0)
                        ibnr_rows.append({'Portfolio':lob,'Closing_IBNR':ibnr_total})
                    ibnr_result = pd.DataFrame(ibnr_rows)
                    results['IBNR'] = ibnr_result
                    st.success(f"IBNR calculated: {ibnr_result['Closing_IBNR'].sum():,.2f}")
                
                # ---- ULAE (auto from OCR + IBNR) ----
                if calc_ulae and 'OCR' in results and 'IBNR' in results:
                    reserves_df = results['OCR'].merge(results['IBNR'], on='Portfolio', how='outer').fillna(0)
                    reserves_df['ULAE_Base'] = 0.5 * reserves_df['Closing_OCR'] + reserves_df['Closing_IBNR']
                    
                    if apportionment_data is not None:
                        app_df = apportionment_data.copy()
                        app_df['Amount'] = pd.to_numeric(app_df['Premiums_Received'], errors='coerce')
                        total_amt = app_df['Amount'].sum()
                        app_df['Pct'] = app_df['Amount'] / total_amt if total_amt > 0 else 0
                        total_base = reserves_df['ULAE_Base'].sum()
                        total_ulae = total_base * ulae_ratio
                        reserves_df = reserves_df.merge(app_df[['Portfolio','Pct']], on='Portfolio', how='left')
                        reserves_df['Pct'] = reserves_df['Pct'].fillna(1.0/len(reserves_df))
                        reserves_df['Closing_ULAE'] = total_ulae * reserves_df['Pct']
                    else:
                        reserves_df['Closing_ULAE'] = reserves_df['ULAE_Base'] * ulae_ratio
                    
                    results['ULAE'] = reserves_df[['Portfolio','Closing_ULAE']]
                    st.success(f"ULAE calculated: {reserves_df['Closing_ULAE'].sum():,.2f}")
                
                # ---- RA (Bootstrap @ 90%) ----
                if calc_ra and claims_data is not None:
                    df_cl = claims_data.copy()
                    df_cl['Loss_Date'] = pd.to_datetime(df_cl['Loss_Date'], errors='coerce')
                    df_cl['Report_Date'] = pd.to_datetime(df_cl['Report_Date'], errors='coerce')
                    df_cl['Amount'] = pd.to_numeric(df_cl['Claim_Amount'], errors='coerce')
                    df_cl = df_cl.dropna(subset=['Loss_Date','Report_Date'])
                    df_cl = df_cl[(df_cl['Loss_Date']>=from_dt)&(df_cl['Loss_Date']<=to_dt)]
                    
                    ra_rows = []
                    for lob in portfolios:
                        lob_data = df_cl[df_cl['Line_of_Business']==lob].copy()
                        if len(lob_data)==0:
                            ra_rows.append({'Portfolio':lob,'Closing_RA':0})
                            continue
                        lob_data['AP'] = lob_data['Loss_Date'].apply(lambda d: d.year - from_dt.year)
                        lob_data['DP'] = lob_data.apply(lambda r: max(0, min(r['Report_Date'].year - r['Loss_Date'].year, n_periods_bcl-1)), axis=1)
                        pivot = lob_data.pivot_table(index='AP', columns='DP', values='Amount', aggfunc='sum')
                        for ap in range(n_periods_bcl):
                            if ap not in pivot.index: pivot.loc[ap] = np.nan
                        for dp in range(n_periods_bcl):
                            if dp not in pivot.columns: pivot[dp] = np.nan
                        inc = pivot.sort_index()[sorted(pivot.columns)].astype(float)
                        obs_mask = pd.DataFrame(False, index=inc.index, columns=inc.columns)
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp < n_periods_bcl: obs_mask.loc[ap, dp] = pd.notna(inc.loc[ap, dp])
                        for ap in inc.index:
                            for dp in inc.columns:
                                if ap+dp >= n_periods_bcl: inc.loc[ap, dp] = np.nan
                        cum = inc.copy()
                        for ap in inc.index:
                            has_obs = any(pd.notna(inc.loc[ap, dp]) for dp in inc.columns if ap+dp<n_periods_bcl)
                            if not has_obs: continue
                            running = 0.0
                            for dp in sorted(inc.columns):
                                if ap+dp<n_periods_bcl:
                                    v = inc.loc[ap, dp]; running += v if pd.notna(v) else 0.0; cum.loc[ap, dp] = running
                        wc = cum.fillna(0)
                        n_ay, n_dp = wc.shape
                        factors = []
                        for j in range(n_dp-1):
                            num, den = 0.0, 0.0
                            for i in range(n_ay):
                                if i+j+1<n_ay:
                                    c = wc.iloc[i,j]; n = wc.iloc[i,j+1]
                                    if c>0: num+=n; den+=c
                            factors.append(num/den if den>0 else 1.0)
                        completed_det = wc.copy().astype(float)
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs<0: continue
                            for j in range(last_obs,n_dp-1):
                                if j<len(factors):
                                    prev=completed_det.iloc[i,j]; completed_det.iloc[i,j+1]=prev*factors[j] if prev>0 else 0.0
                        fitted_inc = completed_det.copy()
                        for i in range(n_ay):
                            for j in range(n_dp-1,0,-1): fitted_inc.iloc[i,j] = completed_det.iloc[i,j] - completed_det.iloc[i,j-1]
                        residuals_list = []
                        for i in range(n_ay):
                            for j in range(n_dp):
                                if i+j<n_ay and obs_mask.iloc[i,j]:
                                    actual = (wc.iloc[i,j]-wc.iloc[i,j-1]) if j>0 else wc.iloc[i,j]
                                    fitted = fitted_inc.iloc[i,j]
                                    resid = (actual-fitted)/np.sqrt(abs(fitted)) if fitted>0 else 0.0
                                    residuals_list.append(resid)
                        residuals = np.array(residuals_list)
                        n_obs = len(residuals); phi = max(np.sum(residuals**2)/max(n_obs-n_dp+1,1), 0.01)
                        ibnr_samples = []
                        for iteration in range(min(ra_iters, 200)):
                            sampled = np.random.choice(residuals, size=n_obs, replace=True)
                            pseudo_inc = fitted_inc.copy().astype(float); idx = 0
                            for i in range(n_ay):
                                for j in range(n_dp):
                                    if i+j<n_ay and obs_mask.iloc[i,j]:
                                        fv = fitted_inc.iloc[i,j]
                                        pv = fv + sampled[idx]*np.sqrt(max(abs(fv),0.001))
                                        pseudo_inc.iloc[i,j] = max(pv,0.0); idx += 1
                            pseudo_cum = pseudo_inc.cumsum(axis=1)
                            pf = []
                            for j in range(n_dp-1):
                                num, den = 0.0, 0.0
                                for i in range(n_ay):
                                    if i+j+1<n_ay:
                                        c = pseudo_cum.iloc[i,j]; n = pseudo_cum.iloc[i,j+1]
                                        if c>0: num+=n; den+=c
                                pf.append(num/den if den>0 else 1.0)
                            pc = pseudo_cum.copy().astype(float)
                            for i in range(n_ay):
                                last_obs=-1
                                for j in range(n_dp-1,-1,-1):
                                    if i+j<n_ay: last_obs=j; break
                                if last_obs<0: continue
                                for j in range(last_obs,n_dp-1):
                                    if j<len(pf):
                                        prev=pc.iloc[i,j]; pc.iloc[i,j+1]=prev*pf[j] if prev>0 else 0.0
                            if phi>1e-10:
                                proc_inc = pc.copy()
                                for i in range(n_ay):
                                    for j in range(n_dp-1,0,-1): proc_inc.iloc[i,j] = pc.iloc[i,j] - pc.iloc[i,j-1]
                                for i in range(n_ay):
                                    for j in range(n_dp):
                                        is_future = (i+j>=n_ay) or (not obs_mask.iloc[i,j])
                                        if is_future:
                                            mv = proc_inc.iloc[i,j]
                                            if pd.notna(mv) and mv>0: proc_inc.iloc[i,j] = max(np.random.gamma(mv/phi, phi), 0.0)
                                            else: proc_inc.iloc[i,j] = 0.0
                                pc = proc_inc.copy()
                                for i in range(n_ay):
                                    running=0.0
                                    for j in range(n_dp):
                                        v=proc_inc.iloc[i,j]; running+=v if pd.notna(v) and v>0 else 0.0; pc.iloc[i,j]=running
                            ibnr_val = 0.0
                            for i in range(n_ay):
                                last_obs=-1
                                for j in range(n_dp-1,-1,-1):
                                    if i+j<n_ay and obs_mask.iloc[i,j]: last_obs=j; break
                                if last_obs>=0:
                                    cur = pseudo_cum.iloc[i,last_obs]; ult = pc.iloc[i,n_dp-1]
                                    ibnr_val += max(ult-cur,0.0)
                            ibnr_samples.append(ibnr_val)
                        ibnr_arr = np.array(ibnr_samples)
                        cl_ibnr = 0.0
                        for i in range(n_ay):
                            last_obs=-1
                            for j in range(n_dp-1,-1,-1):
                                if i+j<n_ay: last_obs=j; break
                            if last_obs>=0:
                                cur=wc.iloc[i,last_obs]; ult=completed_det.iloc[i,n_dp-1]
                                cl_ibnr += max(ult-cur,0.0)
                        ra_90 = max(np.percentile(ibnr_arr, 90) - cl_ibnr, 0.0)
                        ra_rows.append({'Portfolio':lob,'Closing_RA':ra_90})
                    ra_result = pd.DataFrame(ra_rows)
                    results['RA'] = ra_result
                    st.success(f"RA (Bootstrap @90%) calculated: {ra_result['Closing_RA'].sum():,.2f}")
                
                # ---- BUILD OUTPUT TABLES ----
                st.markdown("---")
                st.markdown("## IFRS 17 Valuation Results")
                
                # Build per-portfolio closing reserves
                closing_reserves = {}
                for p in portfolios:
                    closing_reserves[p] = {
                        'UPR': results['UPR'][results['UPR']['Portfolio']==p]['Closing_UPR'].sum() if 'UPR' in results else 0,
                        'OCR': results['OCR'][results['OCR']['Portfolio']==p]['Closing_OCR'].sum() if 'OCR' in results else 0,
                        'IBNR': results['IBNR'][results['IBNR']['Portfolio']==p]['Closing_IBNR'].sum() if 'IBNR' in results else 0,
                        'ULAE': results['ULAE'][results['ULAE']['Portfolio']==p]['Closing_ULAE'].sum() if 'ULAE' in results else 0,
                        'RA': results['RA'][results['RA']['Portfolio']==p]['Closing_RA'].sum() if 'RA' in results else 0,
                    }
                
                # Opening balances per portfolio
                op_reserves = {}
                if opening_data is not None:
                    for _, row in opening_data.iterrows():
                        p = str(row['Portfolio'])
                        op_reserves[p] = {
                            'UPR': abs(pd.to_numeric(row.get('Opening_LRC_UPR',0), errors='coerce') or 0),
                            'OCR': pd.to_numeric(row.get('Opening_LIC_OCR',0), errors='coerce') or 0,
                            'IBNR': pd.to_numeric(row.get('Opening_LIC_IBNR',0), errors='coerce') or 0,
                            'ULAE': pd.to_numeric(row.get('Opening_LIC_ULAE',0), errors='coerce') or 0,
                            'RA': pd.to_numeric(row.get('Opening_LIC_RA',0), errors='coerce') or 0,
                        }
                
                # Cash flows per portfolio
                cf_reserves = {}
                if cashflow_data is not None:
                    for _, row in cashflow_data.iterrows():
                        p = str(row['Portfolio'])
                        cf_reserves[p] = {
                            'Premiums_Received': pd.to_numeric(row.get('Premiums_Received',0), errors='coerce') or 0,
                            'Paid_Claims': pd.to_numeric(row.get('Paid_Claims_Gross',0), errors='coerce') or 0,
                            'Acquisition_Costs': pd.to_numeric(row.get('Acquisition_Costs',0), errors='coerce') or 0,
                            'Maintenance_Expenses': pd.to_numeric(row.get('Maintenance_Expenses',0), errors='coerce') or 0,
                        }
                
                # ---- LIABILITY SUMMARY ----
                st.subheader("Liability Summary by Portfolio")
                summary_rows = []
                for p in portfolios:
                    cl = closing_reserves.get(p, {})
                    row = {'Portfolio': p}
                    row['UPR (LRC)'] = cl.get('UPR', 0)
                    row['OCR (LIC)'] = cl.get('OCR', 0)
                    row['IBNR (LIC)'] = cl.get('IBNR', 0)
                    row['ULAE (LIC)'] = cl.get('ULAE', 0)
                    row['RA (LIC)'] = cl.get('RA', 0)
                    row['Total LRC'] = row['UPR (LRC)']
                    row['Total LIC'] = row['OCR (LIC)'] + row['IBNR (LIC)'] + row['ULAE (LIC)'] + row['RA (LIC)']
                    row['ICL'] = row['Total LRC'] + row['Total LIC']
                    summary_rows.append(row)
                
                total_row = {'Portfolio': 'TOTAL'}
                for key in summary_rows[0].keys():
                    if key != 'Portfolio':
                        total_row[key] = sum(r.get(key, 0) for r in summary_rows)
                summary_rows.append(total_row)
                summary_df = pd.DataFrame(summary_rows)
                disp_summary = summary_df.copy()
                for c in disp_summary.columns:
                    if c != 'Portfolio':
                        disp_summary[c] = disp_summary[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "-")
                st.dataframe(disp_summary, use_container_width=True, hide_index=True)
                
                # ---- PER-PORTFOLIO ROLLFORWARDS ----
                st.subheader("Liability Rollforward — by Line of Business")
                
                # Calculate insurance revenue per portfolio
                ins_rev = {}
                for p in portfolios:
                    op_upr = op_reserves.get(p, {}).get('UPR', 0)
                    cl_upr = closing_reserves.get(p, {}).get('UPR', 0)
                    prem_rec = cf_reserves.get(p, {}).get('Premiums_Received', 0)
                    ins_rev[p] = op_upr + prem_rec - cl_upr
                
                for p in portfolios:
                    op = op_reserves.get(p, {})
                    cl = closing_reserves.get(p, {})
                    cf = cf_reserves.get(p, {})
                    
                    op_upr = op.get('UPR', 0)
                    cl_upr = cl.get('UPR', 0)
                    op_ocr = op.get('OCR', 0)
                    cl_ocr = cl.get('OCR', 0)
                    op_ibnr = op.get('IBNR', 0)
                    cl_ibnr = cl.get('IBNR', 0)
                    op_ulae = op.get('ULAE', 0)
                    cl_ulae = cl.get('ULAE', 0)
                    op_ra = op.get('RA', 0)
                    cl_ra = cl.get('RA', 0)
                    
                    prem_rec = cf.get('Premiums_Received', 0)
                    paid = cf.get('Paid_Claims', 0)
                    acq = cf.get('Acquisition_Costs', 0)
                    maint = cf.get('Maintenance_Expenses', 0)
                    
                    ir = ins_rev.get(p, 0)
                    incurred = paid + cl_ocr + cl_ibnr - op_ocr - op_ibnr
                    
                    op_icf = op_ocr + op_ibnr + op_ulae
                    cl_icf = cl_ocr + cl_ibnr + cl_ulae
                    op_icl = op_upr + op_icf + op_ra
                    cl_icl = cl_upr + cl_icf + cl_ra
                    
                    st.markdown(f"**{p}**")
                    roll_data = {
                        "Line Item": [
                            "Opening Balance", "Premiums Received", "Insurance Revenue",
                            "Incurred Claims", "Paid Claims", "Acquisition Costs",
                            "ULAE", "Maintenance Expenses", "Change in RA", "Closing Balance"
                        ],
                        "LRC (UPR)": [
                            f"{op_upr:,.2f}", f"{prem_rec:,.2f}", f"{-ir:,.2f}",
                            "-", "-", "-", "-", "-", "-", f"{cl_upr:,.2f}"
                        ],
                        "LIC (FCF)": [
                            f"{op_icf:,.2f}", "-", "-",
                            f"{incurred:,.2f}", f"{-paid:,.2f}", "-",
                            f"{cl_ulae:,.2f}", f"{-maint:,.2f}", "-", f"{cl_icf:,.2f}"
                        ],
                        "LIC (RA)": [
                            f"{op_ra:,.2f}", "-", "-", "-", "-", "-", "-", "-",
                            f"{cl_ra - op_ra:,.2f}", f"{cl_ra:,.2f}"
                        ],
                        "ICL": [
                            f"{op_icl:,.2f}", f"{prem_rec:,.2f}", f"{-ir:,.2f}",
                            f"{incurred:,.2f}", f"{-paid:,.2f}", f"{-acq:,.2f}",
                            f"{cl_ulae:,.2f}", f"{-maint:,.2f}",
                            f"{cl_ra - op_ra:,.2f}", f"{cl_icl:,.2f}"
                        ]
                    }
                    st.dataframe(pd.DataFrame(roll_data), use_container_width=True, hide_index=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                
                # ---- CONSOLIDATED ROLLFORWARD ----
                st.subheader("Consolidated Liability Rollforward")
                T = lambda d: sum(v for v in d.values())
                tot_op_upr = T({p: op_reserves.get(p,{}).get('UPR',0) for p in portfolios})
                tot_cl_upr = T({p: closing_reserves.get(p,{}).get('UPR',0) for p in portfolios})
                tot_op_ocr = T({p: op_reserves.get(p,{}).get('OCR',0) for p in portfolios})
                tot_cl_ocr = T({p: closing_reserves.get(p,{}).get('OCR',0) for p in portfolios})
                tot_op_ibnr = T({p: op_reserves.get(p,{}).get('IBNR',0) for p in portfolios})
                tot_cl_ibnr = T({p: closing_reserves.get(p,{}).get('IBNR',0) for p in portfolios})
                tot_op_ulae = T({p: op_reserves.get(p,{}).get('ULAE',0) for p in portfolios})
                tot_cl_ulae = T({p: closing_reserves.get(p,{}).get('ULAE',0) for p in portfolios})
                tot_op_ra = T({p: op_reserves.get(p,{}).get('RA',0) for p in portfolios})
                tot_cl_ra = T({p: closing_reserves.get(p,{}).get('RA',0) for p in portfolios})
                tot_prem = T({p: cf_reserves.get(p,{}).get('Premiums_Received',0) for p in portfolios})
                tot_paid = T({p: cf_reserves.get(p,{}).get('Paid_Claims',0) for p in portfolios})
                tot_acq = T({p: cf_reserves.get(p,{}).get('Acquisition_Costs',0) for p in portfolios})
                tot_maint = T({p: cf_reserves.get(p,{}).get('Maintenance_Expenses',0) for p in portfolios})
                
                tot_ir = tot_op_upr + tot_prem - tot_cl_upr
                tot_incurred = tot_paid + tot_cl_ocr + tot_cl_ibnr - tot_op_ocr - tot_op_ibnr
                tot_op_icf = tot_op_ocr + tot_op_ibnr + tot_op_ulae
                tot_cl_icf = tot_cl_ocr + tot_cl_ibnr + tot_cl_ulae
                tot_op_icl = tot_op_upr + tot_op_icf + tot_op_ra
                tot_cl_icl = tot_cl_upr + tot_cl_icf + tot_cl_ra
                
                consol_data = {
                    "Line Item": [
                        "Opening Balance", "Premiums Received", "Insurance Revenue",
                        "Incurred Claims", "Paid Claims", "Acquisition Costs",
                        "ULAE", "Maintenance Expenses", "Change in RA", "Closing Balance"
                    ],
                    "LRC (UPR)": [
                        f"{tot_op_upr:,.2f}", f"{tot_prem:,.2f}", f"{-tot_ir:,.2f}",
                        "-", "-", "-", "-", "-", "-", f"{tot_cl_upr:,.2f}"
                    ],
                    "LIC (FCF)": [
                        f"{tot_op_icf:,.2f}", "-", "-",
                        f"{tot_incurred:,.2f}", f"{-tot_paid:,.2f}", "-",
                        f"{tot_cl_ulae:,.2f}", f"{-tot_maint:,.2f}", "-", f"{tot_cl_icf:,.2f}"
                    ],
                    "LIC (RA)": [
                        f"{tot_op_ra:,.2f}", "-", "-", "-", "-", "-", "-", "-",
                        f"{tot_cl_ra - tot_op_ra:,.2f}", f"{tot_cl_ra:,.2f}"
                    ],
                    "ICL": [
                        f"{tot_op_icl:,.2f}", f"{tot_prem:,.2f}", f"{-tot_ir:,.2f}",
                        f"{tot_incurred:,.2f}", f"{-tot_paid:,.2f}", f"{-tot_acq:,.2f}",
                        f"{tot_cl_ulae:,.2f}", f"{-tot_maint:,.2f}",
                        f"{tot_cl_ra - tot_op_ra:,.2f}", f"{tot_cl_icl:,.2f}"
                    ]
                }
                st.dataframe(pd.DataFrame(consol_data), use_container_width=True, hide_index=True)
                
                # ---- INCOME STATEMENT ----
                st.subheader("IFRS 17 Income Statement")
                income_data = {
                    "Line Item": [
                        "Insurance revenue", "Insurance service expenses",
                        "  Incurred claims", "  Acquisition costs", "  ULAE",
                        "  Maintenance expenses", "Insurance service result",
                        "Insurance Finance Result", "Profit before tax"
                    ],
                    "Amount": [
                        f"{tot_ir:,.2f}",
                        f"{(tot_incurred + tot_acq + tot_cl_ulae + tot_maint):,.2f}",
                        f"{tot_incurred:,.2f}", f"{tot_acq:,.2f}",
                        f"{tot_cl_ulae:,.2f}", f"{tot_maint:,.2f}",
                        f"{tot_ir - tot_incurred - tot_acq - tot_cl_ulae - tot_maint:,.2f}",
                        "0.00",
                        f"{tot_ir - tot_incurred - tot_acq - tot_cl_ulae - tot_maint:,.2f}"
                    ]
                }
                st.dataframe(pd.DataFrame(income_data), use_container_width=True, hide_index=True)
                
                # ---- EXPORT ----
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as w:
                    meta_df = pd.DataFrame([
                        {"Field":"Creation","Value":st.session_state.report_metadata.get('creation_time','')},
                        {"Field":"Created By","Value":st.session_state.report_metadata.get('created_by','')},
                        {"Field":"Version","Value":st.session_state.report_metadata.get('version','')},
                        {"Field":"Run ID","Value":st.session_state.report_metadata.get('run_id','')},
                        {"Field":"Client","Value":st.session_state.report_metadata.get('client','')},
                        {"Field":"Valuation Date","Value":st.session_state.report_metadata.get('valuation_date','')},
                    ])
                    meta_df.to_excel(w, index=False, sheet_name='Report_Metadata')
                    summary_df.to_excel(w, index=False, sheet_name='Liability_Summary')
                    pd.DataFrame(income_data).to_excel(w, index=False, sheet_name='Income_Statement')
                    pd.DataFrame(consol_data).to_excel(w, index=False, sheet_name='Consolidated_Rollforward')
                    
                    # Per-portfolio rollforwards
                    for p in portfolios:
                        op = op_reserves.get(p, {})
                        cl = closing_reserves.get(p, {})
                        cf = cf_reserves.get(p, {})
                        
                        op_upr = op.get('UPR', 0); cl_upr = cl.get('UPR', 0)
                        op_ocr = op.get('OCR', 0); cl_ocr = cl.get('OCR', 0)
                        op_ibnr = op.get('IBNR', 0); cl_ibnr = cl.get('IBNR', 0)
                        op_ulae = op.get('ULAE', 0); cl_ulae = cl.get('ULAE', 0)
                        op_ra = op.get('RA', 0); cl_ra = cl.get('RA', 0)
                        
                        prem_rec = cf.get('Premiums_Received', 0)
                        paid = cf.get('Paid_Claims', 0)
                        acq = cf.get('Acquisition_Costs', 0)
                        maint = cf.get('Maintenance_Expenses', 0)
                        
                        ir = ins_rev.get(p, 0)
                        incurred = paid + cl_ocr + cl_ibnr - op_ocr - op_ibnr
                        op_icf = op_ocr + op_ibnr + op_ulae
                        cl_icf = cl_ocr + cl_ibnr + cl_ulae
                        op_icl = op_upr + op_icf + op_ra
                        cl_icl = cl_upr + cl_icf + cl_ra
                        
                        pr_data = {
                            "Line Item": [
                                "Opening Balance", "Premiums Received", "Insurance Revenue",
                                "Incurred Claims", "Paid Claims", "Acquisition Costs",
                                "ULAE", "Maintenance Expenses", "Change in RA", "Closing Balance"
                            ],
                            "LRC (UPR)": [op_upr, prem_rec, -ir, 0, 0, 0, 0, 0, 0, cl_upr],
                            "LIC (FCF)": [op_icf, 0, 0, incurred, -paid, 0, cl_ulae, -maint, 0, cl_icf],
                            "LIC (RA)": [op_ra, 0, 0, 0, 0, 0, 0, 0, cl_ra-op_ra, cl_ra],
                            "ICL": [op_icl, prem_rec, -ir, incurred, -paid, -acq, cl_ulae, -maint, cl_ra-op_ra, cl_icl]
                        }
                        safe_name = re.sub(r'[\\/*?:\[\]]', '', p)[:28]
                        pd.DataFrame(pr_data).to_excel(w, index=False, sheet_name=f'RW_{safe_name}')
                
                output.seek(0)
                sc = re.sub(r'[\\/*?:"<>|]',"",report_client).strip() or "Client"
                st.download_button("Download IFRS 17 Report", data=output, file_name=f"{sc}_IFRS17_Report_{report_date}.xlsx", key="fv_dl")
    
    st.markdown('</div>', unsafe_allow_html=True)
    back_button('home', ['Home'])

# =============================================================================
#  ALL OTHER RENDER FUNCTIONS (LRC, LIC, Individual Calculators)
#  Same as previous code — included for completeness
# =============================================================================

def render_lrc():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding:2rem;"><h1>Individual Calculators — LRC</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>UPR Calculator</h3></div>', unsafe_allow_html=True)
        if st.button("Open", key="nav_lrc_upr"): navigate_to('upr_calculator', ['Home','Individual Calculators','UPR Calculator']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Loss Component</h3></div>', unsafe_allow_html=True)
        if st.button("Open", key="nav_lrc_loss"): navigate_to('loss_component', ['Home','Individual Calculators','Loss Component']); st.rerun()
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
    for i, (t, d, p) in enumerate([("OCR","","ocr_calculator"),("IBNR","","ibnr_menu"),("ULAE","","ulae_calculator"),("NPR","","npr_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{t}</h3></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_fc_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows',t]); st.rerun()
    back_button('lic', ['Home','LIC'])

def render_ibnr_menu():
    show_breadcrumb(); st.markdown("## IBNR Methods")
    methods = [("Percentage","ibnr_percentage"),("BCL","bcl_calculator"),("Cape Cod","capecod_calculator"),("BF","bf_calculator"),("ELR","elr_calculator"),("ACPC","acpc_calculator")]
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
    show_breadcrumb(); st.markdown("## Risk Adjustment")
    cols = st.columns(4)
    for i,(n,d,p) in enumerate([("Mack","","mack_calculator"),("Bootstrap","","bootstrap_calculator"),("VaR","","var_calculator"),("Cost of Capital","","coc_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{n}</h3></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_ra_{p}"): navigate_to(p, ['Home','LIC','Risk Adjustment',n]); st.rerun()
    back_button('lic', ['Home','LIC'])

def render_upr_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>UPR Calculator</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    with col1: valuation_date=st.date_input("Valuation Date",value=date(2025,12,31),key="upr_vd")
    with col2: client_name=st.text_input("Client",value="Client",key="upr_cn").strip()
    with col3: method=st.selectbox("Method",["365th","24th","8th"],key="upr_mt")
    with col4: pass
    valuation_date=pd.to_datetime(valuation_date)
    uploaded_file=st.file_uploader("Choose a file",type=["csv","xlsx","xls"],key="upr_f")
    if uploaded_file is not None:
        try:
            original_filename=uploaded_file.name; base_filename=re.sub(r'\.[^.]*$','',original_filename)
            ext=uploaded_file.name.split('.')[-1].lower()
            df=pd.read_csv(uploaded_file) if ext=='csv' else pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            all_columns=df.columns.tolist()
            r1,r2=st.columns(2)
            with r1: start_date_col=st.selectbox("Start Date",[""]+all_columns,key="upr_sd",label_visibility="collapsed")
            with r2: end_date_col=st.selectbox("End Date",[""]+all_columns,key="upr_ed",label_visibility="collapsed")
            if not start_date_col or not end_date_col: st.stop()
            grouping_options=[c for c in all_columns if c not in [start_date_col,end_date_col]]
            grouping_cols=st.multiselect("Group by:",options=grouping_options,default=[grouping_options[0]] if grouping_options else [],key="upr_gc")
            if not grouping_cols: st.stop()
            numeric_columns=[c for c in df.columns if c not in [start_date_col,end_date_col]+grouping_cols and pd.api.types.is_numeric_dtype(df[c])]
            selected_value_cols=st.multiselect("Numeric:",options=numeric_columns,default=numeric_columns[:min(4,len(numeric_columns))],key="upr_vc")
            if not selected_value_cols: st.stop()
            df_check=df.rename(columns={start_date_col:'Start_Date',end_date_col:'End_Date'})
            df_check['Start_Date']=pd.to_datetime(df_check['Start_Date'],errors='coerce')
            df_check['End_Date']=pd.to_datetime(df_check['End_Date'],errors='coerce')
            bad=df_check.dropna(subset=['Start_Date','End_Date']); bad=bad[bad['End_Date']<=bad['Start_Date']]
            if len(bad)>0: st.error(f"{len(bad)} rows End_Date <= Start_Date."); st.stop()
            df_processed=df_check.dropna(subset=['Start_Date','End_Date']); df_processed=df_processed[df_processed['End_Date']>df_processed['Start_Date']]
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce')
            df_processed["Duration"]=(df_processed["End_Date"]-df_processed["Start_Date"]).dt.days
            df_processed=df_processed[df_processed["Duration"]>0]
            if df_processed.empty: st.error("No valid policies."); st.stop()
            if st.button("Calculate UPR",key="upr_calc",use_container_width=True):
                cond=[valuation_date<df_processed["Start_Date"],valuation_date>df_processed["End_Date"],(valuation_date<=df_processed["End_Date"])&(valuation_date>=df_processed["Start_Date"])]
                if method=="365th": t=df_processed["Duration"]; r=(df_processed["End_Date"]-valuation_date).dt.days; ch=[1,0,r/t]
                elif method=="24th": iv=365.25/24; t=df_processed["Duration"]/iv; r=(df_processed["End_Date"]-valuation_date).dt.days/iv; ch=[1,0,r/t]
                else: iv=365.25/8; t=df_processed["Duration"]/iv; r=(df_processed["End_Date"]-valuation_date).dt.days/iv; ch=[1,0,r/t]
                df_processed["Unearned"]=np.select(cond,ch,default=np.nan)
                for c in selected_value_cols: df_processed[f"{c}_UPR"]=df_processed["Unearned"]*df_processed[c]
                upr_c=[f"{c}_UPR" for c in selected_value_cols]
                result=df_processed.groupby(grouping_cols)[upr_c].sum().reset_index()
                result.columns=grouping_cols+[c.replace('_UPR','') for c in upr_c]
                disp=result.copy()
                for c in disp.columns:
                    if c not in grouping_cols: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                st.dataframe(disp,use_container_width=True)
                output=BytesIO()
                with pd.ExcelWriter(output,engine='openpyxl') as w: result.to_excel(w,index=False)
                output.seek(0)
                sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
                so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
                st.download_button("Download",data=output,file_name=f"{sc}_{so}_UPR.xlsx",key="upr_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('lrc',['Home','Individual Calculators'])

def render_loss_component():
    show_breadcrumb(); st.markdown("## Loss Component"); st.info("Available for individual use"); back_button('lrc',['Home','Individual Calculators'])

def render_ocr_calculator():
    show_breadcrumb(); st.markdown('<div class="hero"><h1>OCR Calculator</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client",value="Client",key="ocr_cn").strip()
    with col2: pass
    uploaded_file=st.file_uploader("Choose a file",type=["csv","xlsx","xls"],key="ocr_f")
    if uploaded_file is not None:
        try:
            original_filename=uploaded_file.name; base_filename=re.sub(r'\.[^.]*$','',original_filename)
            ext=uploaded_file.name.split('.')[-1].lower()
            df=pd.read_csv(uploaded_file) if ext=='csv' else pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            all_columns=df.columns.tolist()
            grouping_cols=st.multiselect("Group by:",options=all_columns,default=[all_columns[0]] if all_columns else [],key="ocr_gc")
            if not grouping_cols: st.stop()
            numeric_columns=[c for c in df.select_dtypes(include=[np.number]).columns if c not in grouping_cols]
            selected_value_cols=st.multiselect("Numeric:",options=numeric_columns,default=numeric_columns[:min(5,len(numeric_columns))],key="ocr_vc")
            if not selected_value_cols: st.stop()
            df_processed=df[grouping_cols+selected_value_cols].copy()
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce').fillna(0)
            grouped=df_processed.groupby(grouping_cols)[selected_value_cols].sum().reset_index()
            disp=grouped.copy()
            for c in selected_value_cols: disp[c]=disp[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(disp,use_container_width=True)
            output=BytesIO()
            with pd.ExcelWriter(output,engine='openpyxl') as w: grouped.to_excel(w,index=False)
            output.seek(0)
            sc=re.sub(r'[\\/*?:"<>|]',"",client_name).strip() or "Client"
            so=re.sub(r'[\\/*?:"<>|]',"",base_filename).strip() or "Data"
            st.download_button("Download",data=output,file_name=f"{sc}_{so}_OCR.xlsx",key="ocr_dl")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>',unsafe_allow_html=True)
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def render_ibnr_percentage():
    show_breadcrumb(); st.markdown("## IBNR Percentage"); st.info("Available for individual use"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_bcl_calculator():
    show_breadcrumb(); st.markdown("## BCL"); st.info("Available for individual use"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_capecod_calculator():
    show_breadcrumb(); st.markdown("## Cape Cod"); st.info("Available for individual use"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_bf_calculator():
    show_breadcrumb(); st.markdown("## BF"); st.info("Available for individual use"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_elr_calculator():
    show_breadcrumb(); st.markdown("## ELR"); st.info("Pending"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_acpc_calculator():
    show_breadcrumb(); st.markdown("## ACPC"); st.info("Pending"); back_button('ibnr_menu',['Home','LIC','Fulfilment Cashflows','IBNR Methods'])

def render_ulae_calculator():
    show_breadcrumb(); st.markdown("## ULAE"); st.info("Available for individual use"); back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def render_npr_calculator():
    show_breadcrumb(); st.markdown("## NPR"); st.info("Available for individual use"); back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def render_mack_calculator():
    show_breadcrumb(); st.markdown("## Mack"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_bootstrap_calculator():
    show_breadcrumb(); st.markdown("## Bootstrap"); st.info("Available for individual use"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_var_calculator():
    show_breadcrumb(); st.markdown("## VaR"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

def render_coc_calculator():
    show_breadcrumb(); st.markdown("## Cost of Capital"); st.info("Pending"); back_button('risk_adjustment',['Home','LIC','Risk Adjustment'])

# =============================================================================
#  MAIN ROUTER
# =============================================================================

page_renderers = {
    'home':render_home, 'full_valuation':render_full_valuation,
    'lrc':render_lrc,'lic':render_lic,
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

st.markdown('<div class="footer"><p>2026 Next Vantage. All rights reserved.</p></div>', unsafe_allow_html=True)
