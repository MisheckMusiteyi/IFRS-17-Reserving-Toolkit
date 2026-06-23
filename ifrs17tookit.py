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

# Must be the first Streamlit command
st.set_page_config(
    page_title="AAC Actuarial Toolkit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
#  CUSTOM CSS — AAC THEME: Light Blue (#4A90D9), Black (#000000), White (#FFFFFF)
# =============================================================================

st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Calisto MT', 'Georgia', serif;
        font-size: 11pt;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        font-family: 'Calisto MT', 'Georgia', serif !important;
    }
    .header {
        background-color: #000000;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 3px solid #4A90D9;
    }
    .header .logo {
        color: #4A90D9;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .nav-links a {
        color: #FFFFFF;
        margin-left: 2rem;
        text-decoration: none;
        font-weight: 500;
    }
    .nav-links a:hover { color: #4A90D9; }
    .hero {
        background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
        color: #FFFFFF;
        padding: 3rem 2rem;
        text-align: center;
        border-bottom: 3px solid #4A90D9;
    }
    .hero h1 { color: #4A90D9; font-size: 2.8rem; margin-bottom: 0.5rem; }
    .hero p { font-size: 1.2rem; max-width: 800px; margin: 0 auto; }
    .card {
        background-color: #F9F9F9;
        border: 1px solid #4A90D9;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        text-align: center;
        transition: transform 0.2s;
    }
    .card:hover { transform: translateY(-3px); }
    .card h3 { color: #4A90D9; margin-top: 0; }
    .footer {
        background-color: #000000;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem;
        border-top: 3px solid #4A90D9;
        margin-top: 3rem;
    }
    .footer a { color: #4A90D9; }
    .stButton > button {
        background-color: #4A90D9 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        font-family: 'Calisto MT', 'Georgia', serif !important;
    }
    .stButton > button:hover {
        background-color: #357ABD !important;
        color: #FFFFFF !important;
    }
    .section-container {
        background-color: #F9F9F9;
        border: 2px solid #4A90D9;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .section-container h3 {
        color: #4A90D9;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .breadcrumb {
        background-color: #F0F0F0;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 3px solid #4A90D9;
    }
    .breadcrumb span { color: #4A90D9; font-weight: bold; }
    .stFileUploader {
        border: 2px dashed #4A90D9 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    .data-check-info { background-color: #E3F2FD; border: 2px solid #4A90D9; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .data-check-warning { background-color: #FFF3E0; border: 2px solid #FF9800; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .data-check-error { background-color: #FFEBEE; border: 2px solid #F44336; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .data-check-success { background-color: #E8F5E9; border: 2px solid #4CAF50; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
    .dataframe { border: 1px solid #4A90D9 !important; border-radius: 8px !important; overflow: hidden !important; }
    .stSelectbox [data-baseweb="select"], .stMultiSelect [data-baseweb="select"] {
        border: 1px solid #4A90D9 !important;
        border-radius: 4px !important;
    }
    .required-container {
        background-color: #F9F9F9; border: 2px solid #4A90D9;
        border-radius: 10px; padding: 1rem; text-align: center;
        min-height: 120px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .required-container h3 { color: #4A90D9; font-size: 1.2rem; font-weight: bold; }
    .required-container p { color: #666666; font-size: 0.85rem; }
    .grouping-container {
        background-color: #F9F9F9; border: 2px solid #4A90D9;
        border-radius: 10px; padding: 1rem; margin-bottom: 1rem;
    }
    .grouping-container h3 { color: #4A90D9; font-size: 1.2rem; font-weight: bold; }
    .main-container { max-width: 1400px; margin: 2rem auto; padding: 0 2rem; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
#  SESSION STATE FOR NAVIGATION
# =============================================================================

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'breadcrumb' not in st.session_state:
    st.session_state.breadcrumb = ['Home']

# =============================================================================
#  NAVIGATION FUNCTIONS
# =============================================================================

def navigate_to(page, breadcrumb_label=None):
    st.session_state.page = page
    if breadcrumb_label:
        st.session_state.breadcrumb = breadcrumb_label

def go_home():
    st.session_state.page = 'home'
    st.session_state.breadcrumb = ['Home']

# =============================================================================
#  HEADER
# =============================================================================

st.markdown("""
<div class="header">
    <div class="logo">AAC Actuarial Toolkit</div>
    <div class="nav-links">
        <a href="javascript:void(0)" onclick="window.location.reload()">Home</a>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
#  BREADCRUMB DISPLAY
# =============================================================================

def show_breadcrumb():
    if len(st.session_state.breadcrumb) > 1 or st.session_state.breadcrumb[0] != 'Home':
        breadcrumb_html = " > ".join(
            [f"<span>{b}</span>" for b in st.session_state.breadcrumb]
        )
        st.markdown(f'<div class="breadcrumb">{breadcrumb_html}</div>', unsafe_allow_html=True)

# =============================================================================
#  BACK BUTTON — Uses stable key based on current page + target
# =============================================================================

def back_button(target_page, target_breadcrumb):
    st.markdown("<br>", unsafe_allow_html=True)
    # Key is based on the CURRENT page going back to a specific TARGET
    current = st.session_state.page
    if st.button("Back", key=f"back_{current}_to_{target_page}"):
        navigate_to(target_page, target_breadcrumb)
        st.rerun()

# =============================================================================
#  PAGE RENDERERS — NAVIGATION MENUS (Static keys for nav buttons)
# =============================================================================

def render_home():
    st.markdown("""
    <div class="hero">
        <h1>African Actuarial Consultants</h1>
        <p>Comprehensive Actuarial Reserving Toolkit — IFRS 17 Compliant</p>
        <p style="margin-top: 1rem; font-size: 1rem;">Liability for Remaining Coverage (LRC) | Liability for Incurred Claims (LIC)</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>LRC — Liability for Remaining Coverage</h3><p>Unexpired risk reserve calculations for premium liabilities.</p><p style="font-size:0.85rem;color:#666;">UPR Calculator | Loss Component</p></div>', unsafe_allow_html=True)
        if st.button("Go to LRC Calculators", key="nav_home_lrc"):
            navigate_to('lrc', ['Home', 'LRC']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>LIC — Liability for Incurred Claims</h3><p>Outstanding claims reserves, IBNR, ULAE, Risk Adjustment, and more.</p><p style="font-size:0.85rem;color:#666;">Fulfilment Cashflows | Risk Adjustment</p></div>', unsafe_allow_html=True)
        if st.button("Go to LIC Calculators", key="nav_home_lic"):
            navigate_to('lic', ['Home', 'LIC']); st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("Select LRC or LIC above to access the relevant actuarial calculators.")


def render_lrc():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding: 2rem;"><h1>LRC — Liability for Remaining Coverage</h1><p>Unexpired risk reserve and loss component calculations</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>UPR Calculator</h3><p>Unearned Premium Reserve — 365th, 24th, and 8th methods with data quality checks.</p></div>', unsafe_allow_html=True)
        if st.button("Open UPR Calculator", key="nav_lrc_upr"):
            navigate_to('upr_calculator', ['Home', 'LRC', 'UPR Calculator']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Loss Component</h3><p>Calculate Loss Ratio, Commission Ratio, Expense Ratio, Combined Ratio, and Loss Component.</p></div>', unsafe_allow_html=True)
        if st.button("Open Loss Component", key="nav_lrc_loss"):
            navigate_to('loss_component', ['Home', 'LRC', 'Loss Component']); st.rerun()
    back_button('home', ['Home'])


def render_lic():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding: 2rem;"><h1>LIC — Liability for Incurred Claims</h1><p>Outstanding claims, IBNR, ULAE, NPR, and Risk Adjustment</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Fulfilment Cashflows</h3><p>OCR, IBNR (6 methods), ULAE, and NPR calculators.</p></div>', unsafe_allow_html=True)
        if st.button("Fulfilment Cashflows", key="nav_lic_fulfil"):
            navigate_to('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Risk Adjustment</h3><p>Mack, Bootstrap, VaR, and Cost of Capital methods.</p></div>', unsafe_allow_html=True)
        if st.button("Risk Adjustment", key="nav_lic_ra"):
            navigate_to('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment']); st.rerun()
    back_button('home', ['Home'])


def render_fulfilment_cashflows():
    show_breadcrumb()
    st.markdown("## Fulfilment Cashflows")
    st.markdown("Select a calculator from the options below:")
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
    items = [
        ("OCR", "Outstanding Claims Reserve", "ocr_calculator"),
        ("IBNR", "Incurred But Not Reported", "ibnr_menu"),
        ("ULAE", "Unallocated Loss Adjustment Expenses", "ulae_calculator"),
        ("NPR", "Non-Performance Risk", "npr_calculator"),
    ]
    for i, (title, desc, page) in enumerate(items):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_fc_{page}"):
                navigate_to(page, ['Home', 'LIC', 'Fulfilment Cashflows', title]); st.rerun()
    back_button('lic', ['Home', 'LIC'])


def render_ibnr_menu():
    show_breadcrumb()
    st.markdown("## IBNR Calculation Methods")
    st.markdown("Select an IBNR estimation method:")
    st.markdown("<br>", unsafe_allow_html=True)
    methods = [
        ("Percentage Approach", "Simple percentage of premiums", "ibnr_percentage"),
        ("Basic Chain Ladder (BCL)", "Traditional CL with inflation & discounting", "bcl_calculator"),
        ("Cape Cod", "Internally-derived loss ratio", "capecod_calculator"),
        ("Bornhuetter-Ferguson (BF)", "A-priori ELR with development pattern", "bf_calculator"),
        ("Expected Loss Ratio (ELR)", "Pure ELR method for IBNR", "elr_calculator"),
        ("Average Cost Per Claim (ACPC)", "Claims frequency & severity approach", "acpc_calculator"),
    ]
    for i in range(0, len(methods), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(methods):
                name, desc, page = methods[idx]
                with cols[j]:
                    st.markdown(f'<div class="card"><h3>{name}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
                    if st.button("Open", key=f"nav_ibnr_{page}"):
                        navigate_to(page, ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods', name]); st.rerun()
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])


def render_risk_adjustment():
    show_breadcrumb()
    st.markdown("## Risk Adjustment Methods")
    st.markdown("Select a risk adjustment methodology:")
    st.markdown("<br>", unsafe_allow_html=True)
    methods = [
        ("Mack Method", "Distribution-free standard error of Chain Ladder", "mack_calculator"),
        ("Bootstrap", "England & Verrall (2002) stochastic reserving", "bootstrap_calculator"),
        ("Value at Risk (VaR)", "Percentile-based risk measure", "var_calculator"),
        ("Cost of Capital", "Solvency II cost of capital approach", "coc_calculator"),
    ]
    cols = st.columns(4)
    for i, (name, desc, page) in enumerate(methods):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{name}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"nav_ra_{page}"):
                navigate_to(page, ['Home', 'LIC', 'Risk Adjustment', name]); st.rerun()
    back_button('lic', ['Home', 'LIC'])


# =============================================================================
#  UPR CALCULATOR — COMPLETE
# =============================================================================

def render_upr_calculator():
    show_breadcrumb()
    st.markdown('<div class="hero"><h1>Unearned Premium Reserve (UPR) Calculator</h1><p>Upload CSV or Excel Data file. Map the columns to the required fields below. The app calculates UPR-equivalent reserves grouped by the selected columns (e.g., Line of Business, Currency) using the chosen method (365th, 24th, or 8th).</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: valuation_date = st.date_input("Valuation Date", value=date(2025, 12, 31), key="upr_val_date")
    with col2: client_name = st.text_input("Client Name (for file name)", value="Client", key="upr_client").strip()
    with col3: method = st.selectbox("UPR Calculation Method", ["365th (exact days)", "24th (half-month)", "8th (half-quarter)"], key="upr_method")
    with col4: pass
    valuation_date = pd.to_datetime(valuation_date)
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"], key="upr_file")

    if uploaded_file is not None:
        try:
            original_filename = uploaded_file.name
            base_filename = re.sub(r'\.[^.]*$', '', original_filename)
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext == 'csv':
                try: df = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError: uploaded_file.seek(0); df = pd.read_csv(uploaded_file, encoding='cp1252')
            else: df = pd.read_excel(uploaded_file)
            unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df = df.drop(columns=unnamed)
            st.markdown("#### Preview of uploaded data"); st.dataframe(df.head()); st.markdown("---")
            st.markdown("### Map Your Columns to Required Fields")
            all_columns = df.columns.tolist()
            req_col1, req_col2 = st.columns(2)
            with req_col1:
                st.markdown('<div class="required-container"><h3>Start_Date</h3><p>The date when the policy starts</p></div>', unsafe_allow_html=True)
                start_date_col = st.selectbox("Start Date column", options=[""] + all_columns, key="upr_start", label_visibility="collapsed")
                if start_date_col == "": start_date_col = None
            with req_col2:
                st.markdown('<div class="required-container"><h3>End_Date</h3><p>The date when the policy ends</p></div>', unsafe_allow_html=True)
                end_date_col = st.selectbox("End Date column", options=[""] + all_columns, key="upr_end", label_visibility="collapsed")
                if end_date_col == "": end_date_col = None
            st.markdown("---")
            st.markdown('<div class="grouping-container"><h3>Grouping Columns</h3><p>Select columns to group by (e.g., Line_of_Business).</p></div>', unsafe_allow_html=True)
            grouping_options = [col for col in all_columns if col not in [start_date_col, end_date_col]]
            grouping_cols = st.multiselect("Group by (at least one):", options=grouping_options, default=[grouping_options[0]] if grouping_options else [], key="upr_group")
            if not grouping_cols: st.error("Select at least one grouping column."); st.stop()
            st.markdown("---"); st.markdown("### Select Numeric Columns")
            numeric_columns = []
            for col in df.columns:
                if col in [start_date_col, end_date_col] + grouping_cols: continue
                try: pd.to_numeric(df[col]); numeric_columns.append(col)
                except: pass
            if not numeric_columns: st.error("No numeric columns found."); st.stop()
            selected_value_cols = st.multiselect("Numeric columns:", options=numeric_columns, default=numeric_columns[:min(4, len(numeric_columns))], key="upr_vals")
            if not start_date_col or not end_date_col: st.error("Map all required date columns."); st.stop()
            if not selected_value_cols: st.warning("Select at least one numeric column."); st.stop()

            st.markdown("### Data Quality Checks")
            df_check = df.copy()
            df_check = df_check.rename(columns={start_date_col: 'Start_Date', end_date_col: 'End_Date'})
            df_check['Start_Date'] = pd.to_datetime(df_check['Start_Date'], errors='coerce')
            df_check['End_Date'] = pd.to_datetime(df_check['End_Date'], errors='coerce')
            all_selected = ['Start_Date', 'End_Date'] + grouping_cols + selected_value_cols
            has_critical = False

            st.markdown("#### Missing Values")
            missing = {}
            for col in all_selected:
                if col in df_check.columns: missing[col] = df_check[col].isna().sum()
            st.dataframe(pd.DataFrame(list(missing.items()), columns=['Column', 'Missing']), use_container_width=True)
            if sum(missing.values()) == 0: st.success("No missing values.")
            else: st.warning(f"Total missing: {sum(missing.values())}")

            st.markdown("#### Date Reasonability")
            bad_dates = df_check.dropna(subset=['Start_Date', 'End_Date'])
            bad_dates = bad_dates[bad_dates['End_Date'] <= bad_dates['Start_Date']]
            if len(bad_dates) > 0: has_critical = True; st.error(f"{len(bad_dates)} rows with End_Date <= Start_Date.")
            else: st.success("All dates valid.")

            st.markdown("#### Duplicates")
            dups = df_check[df_check.duplicated()]
            if len(dups) > 0: st.warning(f"{len(dups)} duplicate rows found.")
            else: st.success("No duplicates.")

            st.markdown("---")
            if has_critical: st.error("Cannot proceed with critical issues."); st.stop()

            df_processed = df_check.dropna(subset=['Start_Date', 'End_Date'])
            df_processed = df_processed[df_processed['End_Date'] > df_processed['Start_Date']]
            for col in selected_value_cols: df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
            df_processed["Duration"] = (df_processed["End_Date"] - df_processed["Start_Date"]).dt.days
            df_processed = df_processed[df_processed["Duration"] > 0]
            if df_processed.empty: st.error("No valid policies."); st.stop()

            if st.button("Calculate UPR", key="upr_calc_btn", use_container_width=True):
                with st.spinner("Calculating..."):
                    conditions = [valuation_date < df_processed["Start_Date"], valuation_date > df_processed["End_Date"], (valuation_date <= df_processed["End_Date"]) & (valuation_date >= df_processed["Start_Date"])]
                    if method == "365th (exact days)": total = df_processed["Duration"]; remaining = (df_processed["End_Date"] - valuation_date).dt.days; choices = [1, 0, remaining / total]
                    elif method == "24th (half-month)": iv = 365.25/24; total = df_processed["Duration"]/iv; remaining = (df_processed["End_Date"]-valuation_date).dt.days/iv; choices = [1, 0, remaining/total]
                    else: iv = 365.25/8; total = df_processed["Duration"]/iv; remaining = (df_processed["End_Date"]-valuation_date).dt.days/iv; choices = [1, 0, remaining/total]
                    df_processed["Unearned"] = np.select(conditions, choices, default=np.nan)
                    for col in selected_value_cols: df_processed[f"{col}_UPR"] = df_processed["Unearned"] * df_processed[col]
                    upr_cols = [f"{c}_UPR" for c in selected_value_cols]
                    result = df_processed.groupby(grouping_cols)[upr_cols].sum().reset_index()
                    result.columns = grouping_cols + [c.replace('_UPR', '') for c in upr_cols]
                    st.subheader("UPR Results by " + ", ".join(grouping_cols))
                    disp = result.copy()
                    for c in disp.columns:
                        if c not in grouping_cols: disp[c] = disp[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                    st.dataframe(disp, use_container_width=True)
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as w: result.to_excel(w, index=False, sheet_name='UPR_Results')
                    output.seek(0)
                    sc = re.sub(r'[\\/*?:"<>|]', "", client_name).strip() or "Client"
                    so = re.sub(r'[\\/*?:"<>|]', "", base_filename).strip() or "Data"
                    st.download_button("Download Excel", data=output, file_name=f"{sc}_{so}_UPR_Results.xlsx", key="upr_dl", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
    back_button('lrc', ['Home', 'LRC'])


# =============================================================================
#  PLACEHOLDER CALCULATORS
# =============================================================================

def render_loss_component():
    show_breadcrumb(); st.markdown("## Loss Component Calculator")
    # ╔══ INSERT LOSS COMPONENT CODE HERE ══╗
    st.info("Loss Component Calculator — Pending implementation")
    # ╚══════════════════════════════════════╝
    back_button('lrc', ['Home', 'LRC'])

def render_ocr_calculator():
    show_breadcrumb(); st.markdown("## OCR — Outstanding Claims Reserve Calculator")
    # ╔══ INSERT OCR CODE HERE ══╗
    st.info("OCR Calculator — Pending implementation")
    # ╚═══════════════════════════╝
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])

def render_ibnr_percentage():
    show_breadcrumb(); st.markdown("## IBNR Percentage Method Calculator")
    st.info("IBNR Percentage Method — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])

def render_bcl_calculator():
    show_breadcrumb(); st.markdown("## Basic Chain Ladder (BCL) IBNR Calculator")
    st.info("Basic Chain Ladder — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])

def render_capecod_calculator():
    show_breadcrumb(); st.markdown("## Cape Cod IBNR Calculator")
    st.info("Cape Cod — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])

def render_bf_calculator():
    show_breadcrumb(); st.markdown("## Bornhuetter-Ferguson (BF) IBNR Calculator")
    st.info("Bornhuetter-Ferguson — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])

def render_elr_calculator():
    show_breadcrumb(); st.markdown("## Expected Loss Ratio (ELR) IBNR Calculator")
    st.info("Expected Loss Ratio — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])

def render_acpc_calculator():
    show_breadcrumb(); st.markdown("## Average Cost Per Claim (ACPC) IBNR Calculator")
    st.info("Average Cost Per Claim — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])

def render_ulae_calculator():
    show_breadcrumb(); st.markdown("## ULAE — Unallocated Loss Adjustment Expenses Calculator")
    st.info("ULAE Calculator — Pending implementation")
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])

def render_npr_calculator():
    show_breadcrumb(); st.markdown("## NPR — Non-Performance Risk (Reinsurance) Calculator")
    st.info("NPR Calculator — Pending implementation")
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])

def render_mack_calculator():
    show_breadcrumb(); st.markdown("## Mack Method — Risk Adjustment Calculator")
    st.info("Mack Method — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])

def render_bootstrap_calculator():
    show_breadcrumb(); st.markdown("## Bootstrap — Stochastic Reserving Calculator")
    st.info("Bootstrap — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])

def render_var_calculator():
    show_breadcrumb(); st.markdown("## Value at Risk (VaR) — Risk Adjustment Calculator")
    st.info("Value at Risk — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])

def render_coc_calculator():
    show_breadcrumb(); st.markdown("## Cost of Capital — Risk Adjustment Calculator")
    st.info("Cost of Capital — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])


# =============================================================================
#  MAIN ROUTER
# =============================================================================

page_renderers = {
    'home': render_home, 'lrc': render_lrc, 'lic': render_lic,
    'fulfilment_cashflows': render_fulfilment_cashflows,
    'ibnr_menu': render_ibnr_menu, 'risk_adjustment': render_risk_adjustment,
    'upr_calculator': render_upr_calculator, 'loss_component': render_loss_component,
    'ocr_calculator': render_ocr_calculator, 'ibnr_percentage': render_ibnr_percentage,
    'bcl_calculator': render_bcl_calculator, 'capecod_calculator': render_capecod_calculator,
    'bf_calculator': render_bf_calculator, 'elr_calculator': render_elr_calculator,
    'acpc_calculator': render_acpc_calculator, 'ulae_calculator': render_ulae_calculator,
    'npr_calculator': render_npr_calculator, 'mack_calculator': render_mack_calculator,
    'bootstrap_calculator': render_bootstrap_calculator, 'var_calculator': render_var_calculator,
    'coc_calculator': render_coc_calculator,
}

current_page = st.session_state.page
if current_page in page_renderers:
    page_renderers[current_page]()
else:
    render_home()

# =============================================================================
#  FOOTER
# =============================================================================

st.markdown("""
<div class="footer">
    <p>2026 African Actuarial Consultants. All rights reserved.</p>
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">IFRS 17 Compliant | Solvency II Ready | Built by AAC</p>
</div>
""", unsafe_allow_html=True)
