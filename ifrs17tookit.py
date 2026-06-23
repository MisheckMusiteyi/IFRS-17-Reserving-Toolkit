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
import uuid

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
    /* UPR-specific styles */
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
#  BACK BUTTON HELPER (FIXED — unique keys via uuid)
# =============================================================================

def back_button(target_page, target_breadcrumb):
    st.markdown("<br>", unsafe_allow_html=True)
    unique_id = str(uuid.uuid4())[:8]
    if st.button("Back", key=f"back_{target_page}_{unique_id}"):
        navigate_to(target_page, target_breadcrumb)
        st.rerun()

# =============================================================================
#  PAGE RENDERERS — NAVIGATION MENUS
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
        if st.button("Go to LRC Calculators", key="btn_lrc"):
            navigate_to('lrc', ['Home', 'LRC']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>LIC — Liability for Incurred Claims</h3><p>Outstanding claims reserves, IBNR, ULAE, Risk Adjustment, and more.</p><p style="font-size:0.85rem;color:#666;">Fulfilment Cashflows | Risk Adjustment</p></div>', unsafe_allow_html=True)
        if st.button("Go to LIC Calculators", key="btn_lic"):
            navigate_to('lic', ['Home', 'LIC']); st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("Select LRC or LIC above to access the relevant actuarial calculators.")


def render_lrc():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding: 2rem;"><h1>LRC — Liability for Remaining Coverage</h1><p>Unexpired risk reserve and loss component calculations</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>UPR Calculator</h3><p>Unearned Premium Reserve — 365th, 24th, and 8th methods with data quality checks.</p></div>', unsafe_allow_html=True)
        if st.button("Open UPR Calculator", key="btn_upr"):
            navigate_to('upr_calculator', ['Home', 'LRC', 'UPR Calculator']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Loss Component</h3><p>Calculate Loss Ratio, Commission Ratio, Expense Ratio, Combined Ratio, and Loss Component.</p></div>', unsafe_allow_html=True)
        if st.button("Open Loss Component", key="btn_loss_comp"):
            navigate_to('loss_component', ['Home', 'LRC', 'Loss Component']); st.rerun()
    back_button('home', ['Home'])


def render_lic():
    show_breadcrumb()
    st.markdown('<div class="hero" style="padding: 2rem;"><h1>LIC — Liability for Incurred Claims</h1><p>Outstanding claims, IBNR, ULAE, NPR, and Risk Adjustment</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>Fulfilment Cashflows</h3><p>OCR, IBNR (6 methods), ULAE, and NPR calculators.</p></div>', unsafe_allow_html=True)
        if st.button("Fulfilment Cashflows", key="btn_fulfilment"):
            navigate_to('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows']); st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>Risk Adjustment</h3><p>Mack, Bootstrap, VaR, and Cost of Capital methods.</p></div>', unsafe_allow_html=True)
        if st.button("Risk Adjustment", key="btn_ra"):
            navigate_to('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment']); st.rerun()
    back_button('home', ['Home'])


def render_fulfilment_cashflows():
    show_breadcrumb()
    st.markdown("## Fulfilment Cashflows")
    st.markdown("Select a calculator from the options below:")
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
    calculators = [
        ("OCR", "Outstanding Claims Reserve", "ocr_calculator", "OCR Calculator"),
        ("IBNR", "Incurred But Not Reported", "ibnr_menu", "IBNR Methods"),
        ("ULAE", "Unallocated Loss Adjustment Expenses", "ulae_calculator", "ULAE Calculator"),
        ("NPR", "Non-Performance Risk", "npr_calculator", "NPR Calculator"),
    ]
    for i, (title, desc, page, breadcrumb) in enumerate(calculators):
        with cols[i]:
            st.markdown(f'<div class="card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button("Open", key=f"btn_{page}"):
                navigate_to(page, ['Home', 'LIC', 'Fulfilment Cashflows', breadcrumb]); st.rerun()
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
                    if st.button("Open", key=f"btn_{page}"):
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
            if st.button("Open", key=f"btn_{page}"):
                navigate_to(page, ['Home', 'LIC', 'Risk Adjustment', name]); st.rerun()
    back_button('lic', ['Home', 'LIC'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║                    CALCULATOR IMPLEMENTATIONS                            ║
#  ║  COMPLETED: UPR Calculator                                              ║
#  ║  TODO: All other calculators — replace placeholder with full code        ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================


# =============================================================================
#  UPR CALCULATOR — COMPLETE
# =============================================================================

def render_upr_calculator():
    """UPR Calculator — Unearned Premium Reserve. FULLY IMPLEMENTED."""
    show_breadcrumb()

    st.markdown("""
    <div class="hero">
        <h1>Unearned Premium Reserve (UPR) Calculator</h1>
        <p>Upload CSV or Excel Data file. Map the columns to the required fields below. The app calculates UPR-equivalent reserves grouped by the selected columns (e.g., Line of Business, Currency) using the chosen method (365th, 24th, or 8th).</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        valuation_date = st.date_input("Valuation Date", value=date(2025, 12, 31))
    with col2:
        client_name = st.text_input("Client Name (for file name)", value="Client").strip()
    with col3:
        method = st.selectbox("UPR Calculation Method", ["365th (exact days)", "24th (half-month)", "8th (half-quarter)"])
    with col4:
        pass

    valuation_date = pd.to_datetime(valuation_date)
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        try:
            original_filename = uploaded_file.name
            base_filename = re.sub(r'\.[^.]*$', '', original_filename)

            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension == 'csv':
                try: df = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0); df = pd.read_csv(uploaded_file, encoding='cp1252')
                    st.info("File read with Windows-1252 encoding.")
            else:
                df = pd.read_excel(uploaded_file)

            unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed:
                df = df.drop(columns=unnamed)
                st.info(f"Dropped {len(unnamed)} unnamed column(s).")

            st.markdown("#### Preview of uploaded data")
            st.dataframe(df.head())
            st.markdown("---")

            st.markdown("### Map Your Columns to Required Fields")
            all_columns = df.columns.tolist()

            req_col1, req_col2 = st.columns(2)
            with req_col1:
                st.markdown('<div class="required-container"><h3>Start_Date</h3><p>The date when the policy starts (origin period)</p></div>', unsafe_allow_html=True)
                start_date_col = st.selectbox("Select your Start Date column", options=[""] + all_columns, key="start_date", label_visibility="collapsed")
                if start_date_col == "": start_date_col = None
            with req_col2:
                st.markdown('<div class="required-container"><h3>End_Date</h3><p>The date when the policy ends (development period)</p></div>', unsafe_allow_html=True)
                end_date_col = st.selectbox("Select your End Date column", options=[""] + all_columns, key="end_date", label_visibility="collapsed")
                if end_date_col == "": end_date_col = None

            st.markdown("---")
            st.markdown('<div class="grouping-container"><h3>Grouping Columns</h3><p>Select the columns you want to group by (e.g., Line_of_Business, Currency). Results will be aggregated by these columns.</p></div>', unsafe_allow_html=True)
            grouping_options = [col for col in all_columns if col not in [start_date_col, end_date_col]]
            grouping_cols = st.multiselect("Choose columns to group results by (at least one required):", options=grouping_options, default=[grouping_options[0]] if grouping_options else [])
            if not grouping_cols: st.error("Please select at least one grouping column."); st.stop()

            st.markdown("---")
            st.markdown("### Select Numeric Columns for UPR Calculation")
            numeric_columns = []
            for col in df.columns:
                if col in [start_date_col, end_date_col] + grouping_cols: continue
                try: pd.to_numeric(df[col]); numeric_columns.append(col)
                except (ValueError, TypeError): pass
            numeric_columns = list(set(numeric_columns + [col for col in df.select_dtypes(include=[np.number]).columns.tolist() if col not in numeric_columns]))
            if not numeric_columns: st.error("No numeric columns found."); st.stop()
            selected_value_cols = st.multiselect("Choose the numeric columns you want to convert to UPR:", options=numeric_columns, default=numeric_columns[:min(4, len(numeric_columns))] if numeric_columns else [])
            if not start_date_col or not end_date_col: st.error("Please map all required date columns."); st.stop()
            if not selected_value_cols: st.warning("Please select at least one numeric column."); st.stop()

            # DATA QUALITY CHECKS
            st.markdown("### Data Quality Checks")
            df_check = df.copy()
            df_check = df_check.rename(columns={start_date_col: 'Start_Date', end_date_col: 'End_Date'})
            df_check['Start_Date'] = pd.to_datetime(df_check['Start_Date'], errors='coerce')
            df_check['End_Date'] = pd.to_datetime(df_check['End_Date'], errors='coerce')
            all_selected_cols = ['Start_Date', 'End_Date'] + grouping_cols + selected_value_cols
            has_critical_errors = False; error_messages = []; warning_messages = []

            st.markdown("#### 1. Missing Values Check")
            missing_summary = {}
            for col in all_selected_cols:
                if col in df_check.columns:
                    mc = df_check[col].isna().sum(); missing_summary[col] = mc
                    if mc > 0: warning_messages.append(f"Column '{col}' has {mc} missing value(s).")
            st.dataframe(pd.DataFrame(list(missing_summary.items()), columns=['Column', 'Missing Values']), use_container_width=True)
            if sum(missing_summary.values()) == 0: st.success("No missing values found.")
            else: st.warning(f"Total missing values: {sum(missing_summary.values())}")

            st.markdown("#### 2. Date Reasonability Check")
            invalid_dates = df_check.dropna(subset=['Start_Date', 'End_Date'])
            invalid_dates = invalid_dates[invalid_dates['End_Date'] <= invalid_dates['Start_Date']]
            if len(invalid_dates) > 0:
                has_critical_errors = True; error_messages.append(f"Found {len(invalid_dates)} row(s) where End_Date is not after Start_Date.")
                st.error(f"{len(invalid_dates)} row(s) have End_Date <= Start_Date.")
            else: st.success("All valid dates have End_Date after Start_Date.")

            st.markdown("#### 3. Duplicate Entry Check")
            dup_rows = df_check[df_check.duplicated()]
            if len(dup_rows) > 0: warning_messages.append(f"Found {len(dup_rows)} exact duplicate row(s)."); st.warning(f"{len(dup_rows)} exact duplicate row(s) found.")
            else: st.success("No exact duplicate rows found.")

            st.markdown("#### Data Quality Summary")
            if error_messages:
                st.markdown('<div class="data-check-error"><b>Critical Issues Found:</b>', unsafe_allow_html=True)
                for e in error_messages: st.write(f"  {e}")
                st.markdown('</div>', unsafe_allow_html=True)
            if warning_messages:
                st.markdown('<div class="data-check-warning"><b>Warnings:</b>', unsafe_allow_html=True)
                for w in warning_messages: st.write(f"  {w}")
                st.markdown('</div>', unsafe_allow_html=True)
            if not error_messages and not warning_messages:
                st.markdown('<div class="data-check-success"><b>All data quality checks passed!</b></div>', unsafe_allow_html=True)
            st.markdown("---")

            if has_critical_errors: st.error("Calculation cannot proceed due to critical data issues."); st.stop()

            df_processed = df_check.dropna(subset=['Start_Date', 'End_Date'])
            df_processed = df_processed[df_processed['End_Date'] > df_processed['Start_Date']]
            for col in selected_value_cols:
                if col in df_processed.columns: df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
            df_processed["Duration"] = (df_processed["End_Date"] - df_processed["Start_Date"]).dt.days
            df_processed = df_processed[df_processed["Duration"] > 0]
            if df_processed.empty: st.error("No valid policies remaining."); st.stop()

            if st.button("Calculate UPR", use_container_width=True):
                with st.spinner("Calculating UPR..."):
                    conditions = [
                        valuation_date < df_processed["Start_Date"],
                        valuation_date > df_processed["End_Date"],
                        (valuation_date <= df_processed["End_Date"]) & (valuation_date >= df_processed["Start_Date"])
                    ]
                    if method == "365th (exact days)":
                        total = df_processed["Duration"]; remaining = (df_processed["End_Date"] - valuation_date).dt.days
                        choices = [1, 0, remaining / total]
                    elif method == "24th (half-month)":
                        interval_days = 365.25 / 24
                        total = df_processed["Duration"] / interval_days; remaining = (df_processed["End_Date"] - valuation_date).dt.days / interval_days
                        choices = [1, 0, remaining / total]
                    else:
                        interval_days = 365.25 / 8
                        total = df_processed["Duration"] / interval_days; remaining = (df_processed["End_Date"] - valuation_date).dt.days / interval_days
                        choices = [1, 0, remaining / total]

                    df_processed["Unearned_portion"] = np.select(conditions, choices, default=np.nan)
                    for col in selected_value_cols:
                        df_processed[f"{col}_UPR"] = df_processed["Unearned_portion"] * df_processed[col]

                    upr_columns = [f"{col}_UPR" for col in selected_value_cols]
                    result = df_processed.groupby(grouping_cols)[upr_columns].sum().reset_index()
                    result.columns = grouping_cols + [col.replace('_UPR', '') for col in upr_columns]

                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.subheader("UPR Results by " + ", ".join(grouping_cols))
                    display_result = result.copy()
                    for col in display_result.columns:
                        if col not in grouping_cols: display_result[col] = display_result[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                    st.dataframe(display_result, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result.to_excel(writer, index=False, sheet_name='UPR_Results')
                    output.seek(0)
                    safe_client = re.sub(r'[\\/*?:"<>|]', "", client_name).strip() or "Client"
                    safe_original = re.sub(r'[\\/*?:"<>|]', "", base_filename).strip() or "Data"
                    st.download_button("Download results as Excel", data=output, file_name=f"{safe_client}_{safe_original}_UPR_Results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    back_button('lrc', ['Home', 'LRC'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  LOSS COMPONENT CALCULATOR — INSERT CODE BELOW                          ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_loss_component():
    """Loss Component Calculator."""
    show_breadcrumb()
    st.markdown("## Loss Component Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR LOSS COMPONENT CALCULATOR CODE HERE                    ║
    # ║  Replace this entire function body with your Streamlit code         ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Loss Component Calculator — Pending implementation")
    back_button('lrc', ['Home', 'LRC'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  OCR CALCULATOR — INSERT CODE BELOW                                     ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_ocr_calculator():
    """OCR Calculator."""
    show_breadcrumb()
    st.markdown("## OCR — Outstanding Claims Reserve Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR OCR CALCULATOR CODE HERE                               ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("OCR Calculator — Pending implementation")
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  IBNR PERCENTAGE METHOD — INSERT CODE BELOW                             ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_ibnr_percentage():
    """IBNR Percentage Method."""
    show_breadcrumb()
    st.markdown("## IBNR Percentage Method Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR IBNR PERCENTAGE METHOD CODE HERE                       ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("IBNR Percentage Method — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  BASIC CHAIN LADDER (BCL) — INSERT CODE BELOW                           ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_bcl_calculator():
    """Basic Chain Ladder Calculator."""
    show_breadcrumb()
    st.markdown("## Basic Chain Ladder (BCL) IBNR Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR BCL CALCULATOR CODE HERE                               ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Basic Chain Ladder — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  CAPE COD — INSERT CODE BELOW                                           ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_capecod_calculator():
    """Cape Cod Calculator."""
    show_breadcrumb()
    st.markdown("## Cape Cod IBNR Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR CAPE COD CALCULATOR CODE HERE                          ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Cape Cod — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  BORNHUETTER-FERGUSON (BF) — INSERT CODE BELOW                          ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_bf_calculator():
    """Bornhuetter-Ferguson Calculator."""
    show_breadcrumb()
    st.markdown("## Bornhuetter-Ferguson (BF) IBNR Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR BF CALCULATOR CODE HERE                                ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Bornhuetter-Ferguson — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  EXPECTED LOSS RATIO (ELR) — INSERT CODE BELOW                          ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_elr_calculator():
    """Expected Loss Ratio Calculator."""
    show_breadcrumb()
    st.markdown("## Expected Loss Ratio (ELR) IBNR Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR ELR CALCULATOR CODE HERE                               ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Expected Loss Ratio — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  AVERAGE COST PER CLAIM (ACPC) — INSERT CODE BELOW                      ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_acpc_calculator():
    """Average Cost Per Claim Calculator."""
    show_breadcrumb()
    st.markdown("## Average Cost Per Claim (ACPC) IBNR Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR ACPC CALCULATOR CODE HERE                              ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Average Cost Per Claim — Pending implementation")
    back_button('ibnr_menu', ['Home', 'LIC', 'Fulfilment Cashflows', 'IBNR Methods'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  ULAE CALCULATOR — INSERT CODE BELOW                                    ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_ulae_calculator():
    """ULAE Calculator."""
    show_breadcrumb()
    st.markdown("## ULAE — Unallocated Loss Adjustment Expenses Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR ULAE CALCULATOR CODE HERE                              ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("ULAE Calculator — Pending implementation")
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  NPR CALCULATOR — INSERT CODE BELOW                                     ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_npr_calculator():
    """NPR Calculator."""
    show_breadcrumb()
    st.markdown("## NPR — Non-Performance Risk (Reinsurance) Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR NPR CALCULATOR CODE HERE                               ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("NPR Calculator — Pending implementation")
    back_button('fulfilment_cashflows', ['Home', 'LIC', 'Fulfilment Cashflows'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  MACK METHOD — INSERT CODE BELOW                                        ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_mack_calculator():
    """Mack Method Calculator."""
    show_breadcrumb()
    st.markdown("## Mack Method — Risk Adjustment Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR MACK METHOD CODE HERE                                  ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Mack Method — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  BOOTSTRAP — INSERT CODE BELOW                                          ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_bootstrap_calculator():
    """Bootstrap Calculator."""
    show_breadcrumb()
    st.markdown("## Bootstrap — Stochastic Reserving Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR BOOTSTRAP CALCULATOR CODE HERE                         ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Bootstrap — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  VALUE AT RISK (VaR) — INSERT CODE BELOW                                ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_var_calculator():
    """Value at Risk Calculator."""
    show_breadcrumb()
    st.markdown("## Value at Risk (VaR) — Risk Adjustment Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR VAR CALCULATOR CODE HERE                               ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Value at Risk — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])


# =============================================================================
#  ╔══════════════════════════════════════════════════════════════════════════╗
#  ║  COST OF CAPITAL — INSERT CODE BELOW                                    ║
#  ╚══════════════════════════════════════════════════════════════════════════╝
# =============================================================================

def render_coc_calculator():
    """Cost of Capital Calculator."""
    show_breadcrumb()
    st.markdown("## Cost of Capital — Risk Adjustment Calculator")

    # ╔══════════════════════════════════════════════════════════════════════╗
    # ║  INSERT YOUR COST OF CAPITAL CODE HERE                              ║
    # ╚══════════════════════════════════════════════════════════════════════╝

    st.info("Cost of Capital — Pending implementation")
    back_button('risk_adjustment', ['Home', 'LIC', 'Risk Adjustment'])


# =============================================================================
#  MAIN ROUTER — Maps page names to renderer functions
# =============================================================================

page_renderers = {
    # Navigation menus
    'home': render_home,
    'lrc': render_lrc,
    'lic': render_lic,
    'fulfilment_cashflows': render_fulfilment_cashflows,
    'ibnr_menu': render_ibnr_menu,
    'risk_adjustment': render_risk_adjustment,

    # LRC Calculators
    'upr_calculator': render_upr_calculator,        # COMPLETE
    'loss_component': render_loss_component,         # PENDING

    # Fulfilment Cashflows Calculators
    'ocr_calculator': render_ocr_calculator,         # PENDING
    'ibnr_percentage': render_ibnr_percentage,       # PENDING
    'bcl_calculator': render_bcl_calculator,         # PENDING
    'capecod_calculator': render_capecod_calculator, # PENDING
    'bf_calculator': render_bf_calculator,           # PENDING
    'elr_calculator': render_elr_calculator,         # PENDING
    'acpc_calculator': render_acpc_calculator,       # PENDING
    'ulae_calculator': render_ulae_calculator,       # PENDING
    'npr_calculator': render_npr_calculator,         # PENDING

    # Risk Adjustment Calculators
    'mack_calculator': render_mack_calculator,       # PENDING
    'bootstrap_calculator': render_bootstrap_calculator, # PENDING
    'var_calculator': render_var_calculator,         # PENDING
    'coc_calculator': render_coc_calculator,         # PENDING
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
