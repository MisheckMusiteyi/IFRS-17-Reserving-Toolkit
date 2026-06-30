# -*- coding: utf-8 -*-
# =============================================================================
#  NEXT VANTAGE — COMPREHENSIVE ACTUARIAL TOOLKIT
#  Premium Redesign: Deep Navy + Electric Blue + Frosted Glass
#  Login gate + full IFRS 17 calculations (unchanged)
#  Run:  streamlit run app.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date, datetime
import re
from scipy import interpolate

st.set_page_config(
    page_title="Next Vantage Actuarial Toolkit",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⬡"
)

# =============================================================================
#  CREDENTIALS  (extend this dict or swap with DB lookup)
# =============================================================================

USERS = {
    "admin@nextvantage.com": {"password": "NV2026!", "name": "Administrator", "role": "Admin"},
    "actuary@nextvantage.com": {"password": "Actuary1", "name": "Actuarial User", "role": "Actuary"},
    "demo@nextvantage.com": {"password": "demo", "name": "Demo User", "role": "Viewer"},
}

# =============================================================================
#  DESIGN SYSTEM CSS
# =============================================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #0A0E1A;
    color: #F1F5F9;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
.stApp { background-color: #0A0E1A; }

/* ── Sidebar redesign ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1321 0%, #0A0E1A 100%) !important;
    border-right: 1px solid rgba(37, 99, 235, 0.25) !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] .block-container { padding: 1rem 0.75rem; }

/* ── Main content area ── */
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.nv-topbar {
    background: rgba(13, 19, 33, 0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(37, 99, 235, 0.3);
    padding: 0 2rem;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.nv-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.15rem;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.02em;
}
.nv-logo .hex { color: #2563EB; font-size: 1.4rem; }
.nv-logo span { color: #38BDF8; }
.nv-user-pill {
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(37, 99, 235, 0.4);
    border-radius: 50px;
    padding: 6px 16px;
    font-size: 0.82rem;
    color: #94A3B8;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nv-user-pill strong { color: #38BDF8; font-weight: 600; }

/* ── LOGIN SCREEN ── */
.login-wrap {
    min-height: 100vh;
    background: #0A0E1A;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    padding: 2rem;
}
.login-mesh {
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 20%, rgba(37,99,235,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 80% 80%, rgba(56,189,248,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 60% 30%, rgba(37,99,235,0.08) 0%, transparent 50%);
    pointer-events: none;
}
.login-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(37,99,235,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37,99,235,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
}
.login-card {
    position: relative;
    background: rgba(28, 35, 51, 0.85);
    backdrop-filter: blur(32px);
    -webkit-backdrop-filter: blur(32px);
    border: 1px solid rgba(37, 99, 235, 0.35);
    border-radius: 20px;
    padding: 2.5rem 2.5rem 2rem;
    width: 100%;
    max-width: 420px;
    box-shadow:
        0 0 0 1px rgba(37,99,235,0.1),
        0 32px 64px rgba(0,0,0,0.5),
        0 0 80px rgba(37,99,235,0.08);
}
.login-badge {
    display: inline-block;
    background: rgba(37,99,235,0.15);
    border: 1px solid rgba(37,99,235,0.4);
    border-radius: 50px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #38BDF8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.login-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.04em;
    line-height: 1.15;
    margin-bottom: 0.4rem;
}
.login-title span { color: #2563EB; }
.login-sub {
    font-size: 0.85rem;
    color: #64748B;
    margin-bottom: 1.8rem;
    line-height: 1.55;
}
.login-divider {
    height: 1px;
    background: rgba(37,99,235,0.18);
    margin: 1.5rem 0;
}
.login-error {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #F87171;
    margin-bottom: 1rem;
}
.demo-hint {
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.78rem;
    color: #64748B;
    margin-top: 1rem;
    line-height: 1.6;
}
.demo-hint code {
    color: #38BDF8;
    background: rgba(56,189,248,0.1);
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
}

/* ── HERO ── */
.nv-hero {
    background: linear-gradient(135deg, rgba(37,99,235,0.12) 0%, rgba(10,14,26,0) 60%);
    border-bottom: 1px solid rgba(37,99,235,0.2);
    padding: 2rem 2.5rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.nv-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(37,99,235,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.nv-hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nv-hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 2px;
    background: #2563EB;
    border-radius: 2px;
}
.nv-hero h1 {
    font-size: 1.85rem;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.04em;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.nv-hero h1 span { color: #38BDF8; }
.nv-hero p {
    font-size: 0.9rem;
    color: #64748B;
    max-width: 640px;
    line-height: 1.6;
}

/* ── BREADCRUMB ── */
.nv-breadcrumb {
    padding: 0.6rem 2.5rem;
    font-size: 0.78rem;
    color: #475569;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(13,19,33,0.5);
}
.nv-breadcrumb span { color: #38BDF8; font-weight: 500; }
.nv-breadcrumb .sep { color: #1E293B; }

/* ── CARDS ── */
.nv-card {
    background: rgba(28, 35, 51, 0.6);
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 14px;
    padding: 1.5rem;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    cursor: pointer;
    text-align: center;
    margin-bottom: 0;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(8px);
}
.nv-card:hover {
    border-color: rgba(37,99,235,0.55);
    box-shadow: 0 8px 32px rgba(37,99,235,0.15), 0 0 0 1px rgba(37,99,235,0.2);
    transform: translateY(-2px);
}
.nv-card-icon {
    width: 40px; height: 40px;
    background: rgba(37,99,235,0.15);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    margin: 0 auto 0.8rem;
    border: 1px solid rgba(37,99,235,0.25);
}
.nv-card h3 {
    font-size: 0.95rem;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 0.35rem;
    letter-spacing: -0.02em;
}
.nv-card p {
    font-size: 0.78rem;
    color: #64748B;
    line-height: 1.5;
}

/* ── SECTION CONTAINER ── */
.nv-section {
    background: rgba(28, 35, 51, 0.45);
    border: 1px solid rgba(37, 99, 235, 0.18);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 0 2.5rem 1.25rem;
    backdrop-filter: blur(8px);
}
.nv-section h3 {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #38BDF8;
    margin-bottom: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.nv-section h3::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 14px;
    background: linear-gradient(180deg, #2563EB, #38BDF8);
    border-radius: 2px;
}

/* ── METADATA TABLE ── */
.nv-meta {
    background: rgba(37,99,235,0.05);
    border: 1px solid rgba(37,99,235,0.15);
    border-radius: 10px;
    padding: 0.9rem 1.25rem;
    font-size: 0.8rem;
    color: #64748B;
    margin: 0 2.5rem 1.25rem;
}
.nv-meta table { width: 100%; border-collapse: collapse; }
.nv-meta td { padding: 3px 12px 3px 0; }
.nv-meta td:first-child { color: #475569; font-weight: 500; width: 120px; }
.nv-meta td:last-child { color: #94A3B8; font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; }

/* ── RUN ID CHIP ── */
.nv-runid {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #2563EB;
    background: rgba(37,99,235,0.1);
    border: 1px solid rgba(37,99,235,0.25);
    border-radius: 4px;
    padding: 2px 8px;
    letter-spacing: 0.04em;
}

/* ── STAT CHIPS ── */
.nv-stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin: 0 2.5rem 1.25rem; }
.nv-stat {
    background: rgba(28,35,51,0.7);
    border: 1px solid rgba(37,99,235,0.2);
    border-radius: 10px;
    padding: 0.75rem 1.1rem;
    min-width: 140px;
    flex: 1;
}
.nv-stat-label { font-size: 0.7rem; font-weight: 500; color: #475569; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.nv-stat-value { font-size: 1.25rem; font-weight: 700; color: #F1F5F9; font-family: 'JetBrains Mono', monospace; letter-spacing: -0.02em; }
.nv-stat-value.blue { color: #38BDF8; }

/* ── SUCCESS / INFO / ERROR ALERTS ── */
.nv-alert {
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.82rem;
    margin: 0 2.5rem 0.75rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.nv-alert.success { background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.25); color: #4ADE80; }
.nv-alert.info    { background: rgba(56,189,248,0.07); border: 1px solid rgba(56,189,248,0.2);  color: #38BDF8; }
.nv-alert.warn    { background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.25); color: #FCD34D; }

/* ── PAGE PADDING ── */
.nv-main { padding: 0 0 3rem 0; }
.nv-padded { padding: 0 2.5rem; }

/* ── FOOTER ── */
.nv-footer {
    background: rgba(13,19,33,0.9);
    border-top: 1px solid rgba(37,99,235,0.15);
    text-align: center;
    padding: 1.25rem;
    font-size: 0.75rem;
    color: #1E293B;
    letter-spacing: 0.04em;
    margin-top: 3rem;
}
.nv-footer span { color: #2563EB; }

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stButton > button {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: -0.01em !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB, #38BDF8) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Back button variant */
.back-btn .stButton > button {
    background: rgba(30,41,59,0.8) !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    color: #94A3B8 !important;
    box-shadow: none !important;
    width: auto !important;
    font-size: 0.8rem !important;
}
.back-btn .stButton > button:hover {
    background: rgba(37,99,235,0.15) !important;
    color: #F1F5F9 !important;
    box-shadow: none !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextInput > div > div > input:focus {
    background: rgba(13,19,33,0.8) !important;
    border: 1px solid rgba(37,99,235,0.3) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 0.8rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(37,99,235,0.7) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(13,19,33,0.8) !important;
    border: 1px solid rgba(37,99,235,0.3) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-size: 0.85rem !important;
}

.stDateInput > div > div > input {
    background: rgba(13,19,33,0.8) !important;
    border: 1px solid rgba(37,99,235,0.3) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-size: 0.85rem !important;
}

.stNumberInput > div > div > input {
    background: rgba(13,19,33,0.8) !important;
    border: 1px solid rgba(37,99,235,0.3) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-size: 0.85rem !important;
}

/* Checkbox */
.stCheckbox > label { color: #94A3B8 !important; font-size: 0.85rem !important; }

/* Labels */
.stTextInput > label, .stSelectbox > label, .stNumberInput > label,
.stDateInput > label, .stMultiSelect > label, .stFileUploader > label {
    color: #64748B !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    font-family: 'Inter', sans-serif !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(37,99,235,0.2) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
.stDataFrame { background: rgba(13,19,33,0.6) !important; }

/* File uploader */
.stFileUploader > div {
    border: 2px dashed rgba(37,99,235,0.3) !important;
    border-radius: 10px !important;
    background: rgba(13,19,33,0.5) !important;
    padding: 1rem !important;
}
.stFileUploader > div:hover { border-color: rgba(37,99,235,0.6) !important; }

/* Info / success / warning boxes */
.stAlert { border-radius: 8px !important; border-left-width: 3px !important; font-size: 0.82rem !important; }

/* Spinner */
.stSpinner > div { border-top-color: #2563EB !important; }

/* Columns gap */
[data-testid="column"] { padding: 0 0.4rem !important; }

/* Sidebar items */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(37,99,235,0.1) !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    color: #94A3B8 !important;
    box-shadow: none !important;
    font-size: 0.82rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(37,99,235,0.2) !important;
    color: #F1F5F9 !important;
}

/* Download button */
.stDownloadButton > button {
    background: rgba(34,197,94,0.12) !important;
    border: 1px solid rgba(34,197,94,0.35) !important;
    color: #4ADE80 !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(34,197,94,0.2) !important;
    box-shadow: none !important;
}

/* HR */
hr { border-color: rgba(37,99,235,0.15) !important; }

/* Subheader */
h2, h3 { color: #F1F5F9 !important; letter-spacing: -0.02em !important; font-family: 'Inter', sans-serif !important; }
h2 { font-size: 1.2rem !important; font-weight: 700 !important; }
h3 { font-size: 1rem !important; font-weight: 600 !important; }
h4 { color: #94A3B8 !important; font-size: 0.85rem !important; font-weight: 600 !important; font-family: 'Inter', sans-serif !important; }

/* Markdown text */
.stMarkdown p { color: #94A3B8; font-size: 0.85rem; line-height: 1.6; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# =============================================================================
#  SESSION STATE
# =============================================================================

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'user_role' not in st.session_state: st.session_state.user_role = ""
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'breadcrumb' not in st.session_state: st.session_state.breadcrumb = ['Home']
if 'report_metadata' not in st.session_state: st.session_state.report_metadata = {}
if 'fv_results' not in st.session_state: st.session_state.fv_results = {}
if 'login_error' not in st.session_state: st.session_state.login_error = ""

# =============================================================================
#  LOGIN PAGE
# =============================================================================

def render_login():
    st.markdown("""
    <div class="login-wrap">
        <div class="login-mesh"></div>
        <div class="login-grid"></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    with col_m:
        st.markdown("""
        <div class="login-card">
            <div class="login-badge">⬡ IFRS 17 Compliant Platform</div>
            <div class="login-title">Next <span>Vantage</span></div>
            <div class="login-sub">Actuarial reserving toolkit for modern insurance operations. Secure access required.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown(f'<div class="login-error">⚠ {st.session_state.login_error}</div>', unsafe_allow_html=True)

        email = st.text_input("Email address", placeholder="you@company.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign in to Next Vantage", key="login_btn", use_container_width=True):
            email_clean = email.strip().lower()
            if email_clean in USERS and USERS[email_clean]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.user_name = USERS[email_clean]["name"]
                st.session_state.user_email = email_clean
                st.session_state.user_role = USERS[email_clean]["role"]
                st.session_state.login_error = ""
                st.rerun()
            else:
                st.session_state.login_error = "Invalid email or password. Please try again."
                st.rerun()

        st.markdown("""
        <div class="demo-hint">
            <strong style="color:#38BDF8;">Demo credentials</strong><br>
            Email: <code>demo@nextvantage.com</code><br>
            Password: <code>demo</code>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
#  TOPBAR
# =============================================================================

def render_topbar():
    st.markdown(f"""
    <div class="nv-topbar">
        <div class="nv-logo"><span class="hex">⬡</span> Next<span>Vantage</span></div>
        <div class="nv-user-pill">
            ● &nbsp; Signed in as &nbsp;<strong>{st.session_state.user_name}</strong>
            &nbsp;·&nbsp; {st.session_state.user_role}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
#  SIDEBAR
# =============================================================================

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.5rem 0 1rem; border-bottom: 1px solid rgba(37,99,235,0.2); margin-bottom: 1rem;">
            <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:0.75rem;">Navigation</div>
        </div>
        """, unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Home", "home", ['Home']),
            ("◈", "Full IFRS 17 Valuation", "full_valuation", ['Home', 'Full Valuation']),
            ("◻", "LRC Calculators", "lrc", ['Home', 'Individual Calculators', 'LRC']),
            ("◼", "LIC Calculators", "lic", ['Home', 'LIC']),
        ]
        for icon, label, pg, bc in nav_items:
            if st.button(f"{icon}  {label}", key=f"sb_{pg}", use_container_width=True):
                navigate_to(pg, bc); st.rerun()

        st.markdown("""
        <div style="height:1px; background:rgba(37,99,235,0.15); margin: 1rem 0;"></div>
        <div style="font-size:0.7rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:0.75rem;">Session</div>
        """, unsafe_allow_html=True)

        if st.button("⏻  Sign out", key="sb_signout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        st.markdown("""
        <div style="position:absolute; bottom:1.5rem; left:0.75rem; right:0.75rem; font-size:0.68rem; color:#1E293B; text-align:center; line-height:1.6;">
            Next Vantage v3.9.29.3<br>IFRS 17 Compliant Engine
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
#  NAVIGATION HELPERS
# =============================================================================

def navigate_to(page, breadcrumb_label=None):
    st.session_state.page = page
    if breadcrumb_label: st.session_state.breadcrumb = breadcrumb_label

def show_breadcrumb():
    if st.session_state.breadcrumb:
        parts = []
        for i, b in enumerate(st.session_state.breadcrumb):
            if i == len(st.session_state.breadcrumb) - 1:
                parts.append(f'<span>{b}</span>')
            else:
                parts.append(f'<span style="color:#475569">{b}</span>')
        bc = ' <span class="sep">›</span> '.join(parts)
        st.markdown(f'<div class="nv-breadcrumb">{bc}</div>', unsafe_allow_html=True)

def back_button(target_page, target_breadcrumb):
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    st.markdown('<div class="back-btn nv-padded">', unsafe_allow_html=True)
    current = st.session_state.page
    if st.button("← Back", key=f"back_{current}_to_{target_page}"):
        navigate_to(target_page, target_breadcrumb); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def map_columns(df, required_fields, file_label):
    all_cols = df.columns.tolist()
    mapped = {}
    st.markdown(f'<div style="font-size:0.78rem;font-weight:600;color:#64748B;letter-spacing:0.04em;text-transform:uppercase;margin:0.5rem 0 0.4rem;">Map columns — {file_label}</div>', unsafe_allow_html=True)
    cols_per_row = min(4, len(required_fields))
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
#  HOME PAGE
# =============================================================================

def render_home():
    st.markdown("""
    <div class="nv-hero">
        <div class="nv-hero-eyebrow">Actuarial Reserving Platform</div>
        <h1>Insurance Liability Intelligence<br><span>at your fingertips</span></h1>
        <p>Production-grade IFRS 17 reserving engine covering UPR, OCR, IBNR, ULAE, Risk Adjustment, and Income Statement generation across multiple lines of business.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
        <div class="nv-card">
            <div class="nv-card-icon">◈</div>
            <h3>Full IFRS 17 Valuation</h3>
            <p>End-to-end valuation with Income Statement and per-LOB Liability Rollforward. Upload data, map columns, download report.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Full Valuation", key="nav_home_full"): navigate_to('full_valuation', ['Home', 'Full Valuation']); st.rerun()

    with col2:
        st.markdown("""
        <div class="nv-card">
            <div class="nv-card-icon">◻</div>
            <h3>Individual Calculators</h3>
            <p>Standalone LRC tools — UPR calculator with 365th, 24th and 8th methods, plus Loss Component analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Calculators", key="nav_home_calc"): navigate_to('lrc', ['Home', 'Individual Calculators', 'LRC']); st.rerun()

    with col3:
        st.markdown("""
        <div class="nv-card">
            <div class="nv-card-icon">◼</div>
            <h3>LIC — Incurred Claims</h3>
            <p>Fulfilment Cashflows, IBNR methods (BCL, BF, Cape Cod, ACPC) and Risk Adjustment via bootstrap.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open LIC", key="nav_home_lic"): navigate_to('lic', ['Home', 'LIC']); st.rerun()

    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 0 2.5rem;">
        <div style="background:rgba(28,35,51,0.4);border:1px solid rgba(37,99,235,0.15);border-radius:12px;padding:1.25rem 1.5rem;display:flex;align-items:center;gap:1rem;">
            <div style="width:8px;height:8px;background:#4ADE80;border-radius:50%;box-shadow:0 0 8px rgba(74,222,128,0.5);flex-shrink:0;"></div>
            <div style="font-size:0.82rem;color:#64748B;line-height:1.6;">
                Engine operational &nbsp;·&nbsp; IFRS 17 PAA methodology &nbsp;·&nbsp; Bootstrap RA @ 90th percentile &nbsp;·&nbsp; BCL chain-ladder &nbsp;·&nbsp; Multi-LOB rollforward export
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
#  FULL VALUATION  — PLACEHOLDER (replaced by patch step)
# =============================================================================
def render_full_valuation():
    show_breadcrumb()
    st.markdown("""
    <div class="nv-hero">
        <div class="nv-hero-eyebrow">IFRS 17 · PAA Measurement Model</div>
        <h1>Full <span>IFRS 17</span> Valuation</h1>
        <p>Complete valuation with Income Statement and Liability Rollforward per Line of Business. Upload data files, configure parameters, and export a structured Excel report.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nv-main">', unsafe_allow_html=True)

    # ---- REPORT METADATA ----
    st.markdown('<div class="nv-section"><h3>Report Metadata</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: report_created_by = st.text_input("Created By", value="", key="fv_cb")
    with c2: report_version = st.text_input("Version", value="3.9.29.3", key="fv_ver")
    with c3: report_client = st.text_input("Client Name", value="", key="fv_client")
    with c4: report_date = st.date_input("Valuation Date", value=date.today(), key="fv_vd")
    st.markdown('</div>', unsafe_allow_html=True)

    run_id = f"DN{hash(str(datetime.now())):x}"[:40]
    st.markdown(f"""
    <div class="nv-meta">
    <table>
    <tr><td>Created</td><td class="nv-runid">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
    <tr><td>By</td><td>{report_created_by or '—'}</td></tr>
    <tr><td>Version</td><td>{report_version}</td></tr>
    <tr><td>Run ID</td><td class="nv-runid">{run_id}</td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.report_metadata = {
        'created_by': report_created_by, 'version': report_version,
        'client': report_client, 'valuation_date': str(report_date),
        'run_id': run_id, 'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # ---- VALUATION MODE SELECTOR ----
    st.markdown('<div class="nv-section"><h3>Valuation Mode</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)

    valuation_mode = st.radio(
        "Select Valuation Mode",
        options=["Simplified UPR (IFRS 4)", "Full IFRS 17 LRC (PAA)"],
        index=0,
        key="fv_mode"
    )

    if valuation_mode == "Full IFRS 17 LRC (PAA)":
        st.markdown(
            '<div class="nv-alert info">◈ Full IFRS 17 LRC Mode enabled. '
            'You will upload data sections and configure accounting policy toggles. '
            'This mode is fully independent of the Simplified UPR mode and of the LIC '
            '(OCR/IBNR/ULAE/RA) calculations on this page.</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    #  BRANCH: SIMPLIFIED UPR (IFRS 4) — UNCHANGED FROM ORIGINAL
    # =========================================================================
    if valuation_mode == "Simplified UPR (IFRS 4)":
        _render_simplified_upr_branch(report_date, report_client)
        st.markdown('</div>', unsafe_allow_html=True)
        back_button('home', ['Home'])
        return

    # =========================================================================
    #  BRANCH: FULL IFRS 17 LRC (PAA) — NEW
    # =========================================================================
    _render_full_ifrs17_lrc_branch(report_date, report_client)

    st.markdown('</div>', unsafe_allow_html=True)
    back_button('home', ['Home'])


# =============================================================================
#  BRANCH 1 — SIMPLIFIED UPR (IFRS 4)  [UNCHANGED LOGIC, EXTRACTED TO FUNCTION]
# =============================================================================

def _render_simplified_upr_branch(report_date, report_client):
    """
    This is the ORIGINAL Full Valuation logic, completely unchanged.
    Includes UPR, OCR, IBNR (BCL), ULAE, RA (Bootstrap @90%), and the
    Income Statement. Extracted into its own function so it can be called
    cleanly from the mode selector without touching its internals.
    """
    val_date = pd.to_datetime(report_date)
    from_dt = pd.to_datetime('2020-01-01')
    to_dt = pd.to_datetime('2025-12-31')
    n_periods_bcl = to_dt.year - from_dt.year + 1

    # ---- SELECT RESERVES ----
    st.markdown('<div class="nv-section"><h3>Reserves to Calculate</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: calc_upr = st.checkbox("UPR (LRC)", value=True, key="fv_upr")
    with c2: calc_ocr = st.checkbox("OCR (LIC)", value=True, key="fv_ocr")
    with c3: calc_ibnr = st.checkbox("IBNR — BCL", value=True, key="fv_ibnr")
    with c4: calc_ulae = st.checkbox("ULAE (LIC)", value=True, key="fv_ulae")
    with c5: calc_ra = st.checkbox("RA — Bootstrap @90%", value=True, key="fv_ra")
    with c6: calc_npr = st.checkbox("NPR", value=False, key="fv_npr")
    selected = [x for x, b in [("UPR",calc_upr),("OCR",calc_ocr),("IBNR",calc_ibnr),("ULAE",calc_ulae),("RA",calc_ra),("NPR",calc_npr)] if b]
    if selected:
        st.markdown(f'<div style="font-size:0.78rem;color:#475569;padding:0.4rem 0;">Selected: <span style="color:#38BDF8;font-weight:500;">{" · ".join(selected)}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- DATA FILES ----
    st.markdown('<div class="nv-section"><h3>Data Files & Column Mapping</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)

    upr_data = None; ocr_data = None; claims_data = None
    apportionment_data = None; cashflow_data = None; opening_data = None

    if calc_upr:
        st.markdown("#### UPR Data — Premium Register")
        upr_file = st.file_uploader("Upload UPR file (CSV or Excel)", type=["csv","xlsx","xls"], key="fv_upr_f")
        if upr_file is not None:
            try:
                upr_df = pd.read_csv(upr_file) if upr_file.name.endswith('.csv') else pd.read_excel(upr_file)
                upr_df.columns = upr_df.columns.astype(str).str.strip()
                st.dataframe(upr_df.head(3), use_container_width=True)
                upr_map = map_columns(upr_df, ['Start_Date','End_Date','Line_of_Business','Gross_Written_Premium'], 'UPR')
                upr_data = upr_df.rename(columns=upr_map)
                st.markdown('<div class="nv-alert success">✓ UPR columns mapped</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")

    if calc_ocr:
        st.markdown("#### OCR Data — Case Estimates")
        ocr_file = st.file_uploader("Upload OCR file", type=["csv","xlsx","xls"], key="fv_ocr_f")
        if ocr_file is not None:
            try:
                ocr_df = pd.read_csv(ocr_file) if ocr_file.name.endswith('.csv') else pd.read_excel(ocr_file)
                ocr_df.columns = ocr_df.columns.astype(str).str.strip()
                st.dataframe(ocr_df.head(3), use_container_width=True)
                ocr_map = map_columns(ocr_df, ['Line_of_Business','Case_Reserve'], 'OCR')
                ocr_data = ocr_df.rename(columns=ocr_map)
                st.markdown('<div class="nv-alert success">✓ OCR columns mapped</div>', unsafe_allow_html=True)
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
                st.markdown('<div class="nv-alert success">✓ Claims columns mapped</div>', unsafe_allow_html=True)
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
                st.markdown('<div class="nv-alert success">✓ Apportionment columns mapped</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")

    st.markdown("#### Cash Flow Data — Income Statement")
    cf_file = st.file_uploader("Upload Cash Flow file", type=["csv","xlsx","xls"], key="fv_cf")
    if cf_file is not None:
        try:
            cf_df = pd.read_csv(cf_file) if cf_file.name.endswith('.csv') else pd.read_excel(cf_file)
            cf_df.columns = cf_df.columns.astype(str).str.strip()
            st.dataframe(cf_df.head(3), use_container_width=True)
            cf_map = map_columns(cf_df, ['Portfolio','Premiums_Received','Paid_Claims_Gross','Acquisition_Costs','Maintenance_Expenses'], 'CashFlow')
            cashflow_data = cf_df.rename(columns=cf_map)
            st.markdown('<div class="nv-alert success">✓ Cash flow columns mapped</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="nv-alert success">✓ Opening balances mapped</div>', unsafe_allow_html=True)
        except Exception as e: st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---- PARAMETERS ----
    st.markdown('<div class="nv-section"><h3>Parameters</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- RUN BUTTON ----
    st.markdown('<div class="nv-padded"><br>', unsafe_allow_html=True)
    run_clicked = st.button("⬡  Run Full IFRS 17 Valuation", key="fv_run", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if run_clicked:
        if not selected:
            st.markdown('<div class="nv-alert warn">⚠ Select at least one reserve type before running.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Running IFRS 17 valuation engine..."):
                results = {}

                portfolios = []
                if upr_data is not None and 'Line_of_Business' in upr_data.columns:
                    portfolios = sorted(upr_data['Line_of_Business'].dropna().unique().tolist())
                elif ocr_data is not None and 'Line_of_Business' in ocr_data.columns:
                    portfolios = sorted(ocr_data['Line_of_Business'].dropna().unique().tolist())
                elif claims_data is not None and 'Line_of_Business' in claims_data.columns:
                    portfolios = sorted(claims_data['Line_of_Business'].dropna().unique().tolist())
                else:
                    portfolios = ["Motor","Property","Health","Engineering","Liability"]

                st.markdown(f'<div class="nv-alert info">◈ Portfolios detected: <strong>{" · ".join(portfolios)}</strong></div>', unsafe_allow_html=True)

                # UPR
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
                    st.markdown(f'<div class="nv-alert success">✓ UPR calculated: <strong>{upr_result["Closing_UPR"].sum():,.2f}</strong></div>', unsafe_allow_html=True)

                # OCR
                if calc_ocr and ocr_data is not None:
                    df_ocr = ocr_data.copy()
                    df_ocr['Reserve'] = pd.to_numeric(df_ocr['Case_Reserve'], errors='coerce')
                    ocr_result = df_ocr.groupby('Line_of_Business')['Reserve'].sum().reset_index()
                    ocr_result.columns = ['Portfolio','Closing_OCR']
                    results['OCR'] = ocr_result
                    st.markdown(f'<div class="nv-alert success">✓ OCR calculated: <strong>{ocr_result["Closing_OCR"].sum():,.2f}</strong></div>', unsafe_allow_html=True)

                # IBNR (BCL)
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
                        if len(lob_data)==0: ibnr_rows.append({'Portfolio':lob,'Closing_IBNR':0}); continue
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
                    st.markdown(f'<div class="nv-alert success">✓ IBNR calculated: <strong>{ibnr_result["Closing_IBNR"].sum():,.2f}</strong></div>', unsafe_allow_html=True)

                # ULAE
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
                    st.markdown(f'<div class="nv-alert success">✓ ULAE calculated: <strong>{reserves_df["Closing_ULAE"].sum():,.2f}</strong></div>', unsafe_allow_html=True)

                # RA Bootstrap @90%
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
                        if len(lob_data)==0: ra_rows.append({'Portfolio':lob,'Closing_RA':0}); continue
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
                    st.markdown(f'<div class="nv-alert success">✓ RA (Bootstrap @90%) calculated: <strong>{ra_result["Closing_RA"].sum():,.2f}</strong></div>', unsafe_allow_html=True)

                # ---- RESULTS DISPLAY ----
                st.markdown("""
                <div style="padding:1.5rem 2.5rem 0.5rem;">
                    <div style="height:1px;background:rgba(37,99,235,0.2);margin-bottom:1.5rem;"></div>
                    <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#2563EB;margin-bottom:0.5rem;">Valuation Output</div>
                    <div style="font-size:1.35rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.03em;margin-bottom:1.5rem;">IFRS 17 Results</div>
                </div>
                """, unsafe_allow_html=True)

                closing_reserves = {}
                for p in portfolios:
                    closing_reserves[p] = {
                        'UPR': results['UPR'][results['UPR']['Portfolio']==p]['Closing_UPR'].sum() if 'UPR' in results else 0,
                        'OCR': results['OCR'][results['OCR']['Portfolio']==p]['Closing_OCR'].sum() if 'OCR' in results else 0,
                        'IBNR': results['IBNR'][results['IBNR']['Portfolio']==p]['Closing_IBNR'].sum() if 'IBNR' in results else 0,
                        'ULAE': results['ULAE'][results['ULAE']['Portfolio']==p]['Closing_ULAE'].sum() if 'ULAE' in results else 0,
                        'RA': results['RA'][results['RA']['Portfolio']==p]['Closing_RA'].sum() if 'RA' in results else 0,
                    }

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

                st.markdown('<div class="nv-padded">', unsafe_allow_html=True)
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
                    if key != 'Portfolio': total_row[key] = sum(r.get(key, 0) for r in summary_rows)
                summary_rows.append(total_row)
                summary_df = pd.DataFrame(summary_rows)
                disp_summary = summary_df.copy()
                for c in disp_summary.columns:
                    if c != 'Portfolio': disp_summary[c] = disp_summary[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "-")
                st.dataframe(disp_summary, use_container_width=True, hide_index=True)

                ins_rev = {}
                for p in portfolios:
                    op_upr = op_reserves.get(p, {}).get('UPR', 0)
                    cl_upr = closing_reserves.get(p, {}).get('UPR', 0)
                    prem_rec = cf_reserves.get(p, {}).get('Premiums_Received', 0)
                    ins_rev[p] = op_upr + prem_rec - cl_upr

                st.subheader("Liability Rollforward — by Line of Business")
                for p in portfolios:
                    op = op_reserves.get(p, {}); cl = closing_reserves.get(p, {}); cf = cf_reserves.get(p, {})
                    op_upr=op.get('UPR',0); cl_upr=cl.get('UPR',0)
                    op_ocr=op.get('OCR',0); cl_ocr=cl.get('OCR',0)
                    op_ibnr=op.get('IBNR',0); cl_ibnr=cl.get('IBNR',0)
                    op_ulae=op.get('ULAE',0); cl_ulae=cl.get('ULAE',0)
                    op_ra=op.get('RA',0); cl_ra=cl.get('RA',0)
                    prem_rec=cf.get('Premiums_Received',0); paid=cf.get('Paid_Claims',0)
                    acq=cf.get('Acquisition_Costs',0); maint=cf.get('Maintenance_Expenses',0)
                    ir=ins_rev.get(p,0)
                    incurred=paid+cl_ocr+cl_ibnr-op_ocr-op_ibnr
                    op_icf=op_ocr+op_ibnr+op_ulae; cl_icf=cl_ocr+cl_ibnr+cl_ulae
                    op_icl=op_upr+op_icf+op_ra; cl_icl=cl_upr+cl_icf+cl_ra
                    st.markdown(f'<div style="font-size:0.8rem;font-weight:600;color:#38BDF8;margin:0.75rem 0 0.35rem;">◈ {p}</div>', unsafe_allow_html=True)
                    roll_data = {
                        "Line Item": ["Opening Balance","Premiums Received","Insurance Revenue","Incurred Claims","Paid Claims","Acquisition Costs","ULAE","Maintenance Expenses","Change in RA","Closing Balance"],
                        "LRC (UPR)": [f"{op_upr:,.2f}",f"{prem_rec:,.2f}",f"{-ir:,.2f}","-","-","-","-","-","-",f"{cl_upr:,.2f}"],
                        "LIC (FCF)": [f"{op_icf:,.2f}","-","-",f"{incurred:,.2f}",f"{-paid:,.2f}","-",f"{cl_ulae:,.2f}",f"{-maint:,.2f}","-",f"{cl_icf:,.2f}"],
                        "LIC (RA)": [f"{op_ra:,.2f}","-","-","-","-","-","-","-",f"{cl_ra-op_ra:,.2f}",f"{cl_ra:,.2f}"],
                        "ICL": [f"{op_icl:,.2f}",f"{prem_rec:,.2f}",f"{-ir:,.2f}",f"{incurred:,.2f}",f"{-paid:,.2f}",f"{-acq:,.2f}",f"{cl_ulae:,.2f}",f"{-maint:,.2f}",f"{cl_ra-op_ra:,.2f}",f"{cl_icl:,.2f}"]
                    }
                    st.dataframe(pd.DataFrame(roll_data), use_container_width=True, hide_index=True)

                st.subheader("Consolidated Liability Rollforward")
                T = lambda d: sum(v for v in d.values())
                tot_op_upr=T({p:op_reserves.get(p,{}).get('UPR',0) for p in portfolios}); tot_cl_upr=T({p:closing_reserves.get(p,{}).get('UPR',0) for p in portfolios})
                tot_op_ocr=T({p:op_reserves.get(p,{}).get('OCR',0) for p in portfolios}); tot_cl_ocr=T({p:closing_reserves.get(p,{}).get('OCR',0) for p in portfolios})
                tot_op_ibnr=T({p:op_reserves.get(p,{}).get('IBNR',0) for p in portfolios}); tot_cl_ibnr=T({p:closing_reserves.get(p,{}).get('IBNR',0) for p in portfolios})
                tot_op_ulae=T({p:op_reserves.get(p,{}).get('ULAE',0) for p in portfolios}); tot_cl_ulae=T({p:closing_reserves.get(p,{}).get('ULAE',0) for p in portfolios})
                tot_op_ra=T({p:op_reserves.get(p,{}).get('RA',0) for p in portfolios}); tot_cl_ra=T({p:closing_reserves.get(p,{}).get('RA',0) for p in portfolios})
                tot_prem=T({p:cf_reserves.get(p,{}).get('Premiums_Received',0) for p in portfolios})
                tot_paid=T({p:cf_reserves.get(p,{}).get('Paid_Claims',0) for p in portfolios})
                tot_acq=T({p:cf_reserves.get(p,{}).get('Acquisition_Costs',0) for p in portfolios})
                tot_maint=T({p:cf_reserves.get(p,{}).get('Maintenance_Expenses',0) for p in portfolios})
                tot_ir=tot_op_upr+tot_prem-tot_cl_upr
                tot_incurred=tot_paid+tot_cl_ocr+tot_cl_ibnr-tot_op_ocr-tot_op_ibnr
                tot_op_icf=tot_op_ocr+tot_op_ibnr+tot_op_ulae; tot_cl_icf=tot_cl_ocr+tot_cl_ibnr+tot_cl_ulae
                tot_op_icl=tot_op_upr+tot_op_icf+tot_op_ra; tot_cl_icl=tot_cl_upr+tot_cl_icf+tot_cl_ra
                consol_data = {
                    "Line Item": ["Opening Balance","Premiums Received","Insurance Revenue","Incurred Claims","Paid Claims","Acquisition Costs","ULAE","Maintenance Expenses","Change in RA","Closing Balance"],
                    "LRC (UPR)": [f"{tot_op_upr:,.2f}",f"{tot_prem:,.2f}",f"{-tot_ir:,.2f}","-","-","-","-","-","-",f"{tot_cl_upr:,.2f}"],
                    "LIC (FCF)": [f"{tot_op_icf:,.2f}","-","-",f"{tot_incurred:,.2f}",f"{-tot_paid:,.2f}","-",f"{tot_cl_ulae:,.2f}",f"{-tot_maint:,.2f}","-",f"{tot_cl_icf:,.2f}"],
                    "LIC (RA)": [f"{tot_op_ra:,.2f}","-","-","-","-","-","-","-",f"{tot_cl_ra-tot_op_ra:,.2f}",f"{tot_cl_ra:,.2f}"],
                    "ICL": [f"{tot_op_icl:,.2f}",f"{tot_prem:,.2f}",f"{-tot_ir:,.2f}",f"{tot_incurred:,.2f}",f"{-tot_paid:,.2f}",f"{-tot_acq:,.2f}",f"{tot_cl_ulae:,.2f}",f"{-tot_maint:,.2f}",f"{tot_cl_ra-tot_op_ra:,.2f}",f"{tot_cl_icl:,.2f}"]
                }
                st.dataframe(pd.DataFrame(consol_data), use_container_width=True, hide_index=True)

                st.subheader("IFRS 17 Income Statement")
                income_data = {
                    "Line Item": ["Insurance revenue","Insurance service expenses","  Incurred claims","  Acquisition costs","  ULAE","  Maintenance expenses","Insurance service result","Insurance Finance Result","Profit before tax"],
                    "Amount": [f"{tot_ir:,.2f}",f"{(tot_incurred+tot_acq+tot_cl_ulae+tot_maint):,.2f}",f"{tot_incurred:,.2f}",f"{tot_acq:,.2f}",f"{tot_cl_ulae:,.2f}",f"{tot_maint:,.2f}",f"{tot_ir-tot_incurred-tot_acq-tot_cl_ulae-tot_maint:,.2f}","0.00",f"{tot_ir-tot_incurred-tot_acq-tot_cl_ulae-tot_maint:,.2f}"]
                }
                st.dataframe(pd.DataFrame(income_data), use_container_width=True, hide_index=True)

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
                    for p in portfolios:
                        op=op_reserves.get(p,{}); cl=closing_reserves.get(p,{}); cf=cf_reserves.get(p,{})
                        op_upr=op.get('UPR',0); cl_upr=cl.get('UPR',0)
                        op_ocr=op.get('OCR',0); cl_ocr=cl.get('OCR',0)
                        op_ibnr=op.get('IBNR',0); cl_ibnr=cl.get('IBNR',0)
                        op_ulae=op.get('ULAE',0); cl_ulae=cl.get('ULAE',0)
                        op_ra=op.get('RA',0); cl_ra=cl.get('RA',0)
                        prem_rec=cf.get('Premiums_Received',0); paid=cf.get('Paid_Claims',0)
                        acq=cf.get('Acquisition_Costs',0); maint=cf.get('Maintenance_Expenses',0)
                        ir=ins_rev.get(p,0); incurred=paid+cl_ocr+cl_ibnr-op_ocr-op_ibnr
                        op_icf=op_ocr+op_ibnr+op_ulae; cl_icf=cl_ocr+cl_ibnr+cl_ulae
                        op_icl=op_upr+op_icf+op_ra; cl_icl=cl_upr+cl_icf+cl_ra
                        pr_data = {
                            "Line Item": ["Opening Balance","Premiums Received","Insurance Revenue","Incurred Claims","Paid Claims","Acquisition Costs","ULAE","Maintenance Expenses","Change in RA","Closing Balance"],
                            "LRC (UPR)": [op_upr,prem_rec,-ir,0,0,0,0,0,0,cl_upr],
                            "LIC (FCF)": [op_icf,0,0,incurred,-paid,0,cl_ulae,-maint,0,cl_icf],
                            "LIC (RA)": [op_ra,0,0,0,0,0,0,0,cl_ra-op_ra,cl_ra],
                            "ICL": [op_icl,prem_rec,-ir,incurred,-paid,-acq,cl_ulae,-maint,cl_ra-op_ra,cl_icl]
                        }
                        safe_name = re.sub(r'[\\/*?:\[\]]', '', p)[:28]
                        pd.DataFrame(pr_data).to_excel(w, index=False, sheet_name=f'RW_{safe_name}')
                output.seek(0)
                sc = re.sub(r'[\\/*?:"<>|]',"",report_client).strip() or "Client"
                st.download_button("⬇  Download IFRS 17 Report (.xlsx)", data=output, file_name=f"{sc}_IFRS17_Report_{report_date}.xlsx", key="fv_dl")
                st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
#  BRANCH 2 — FULL IFRS 17 LRC (PAA)  [NEW, FULLY INDEPENDENT]
# =============================================================================

def _render_full_ifrs17_lrc_branch(report_date, report_client):
    """
    Full IFRS 17 LRC (PAA) Mode.

    Independent of the Simplified UPR branch and of LIC (OCR/IBNR/ULAE/RA).
    No shared state, no cross-calls.

    Methodology (confirmed):
      - Insurance Revenue driven by Allocated Premium method (B126(a)),
        computed per-policy then aggregated to group level.
      - UPR roll-forward identity computed SEPARATELY, purely for the
        UPR_Comparison output sheet (transition bridge / audit cross-check).
      - IACF Amortisation tied to the SAME allocation_factor as Revenue (B125).
      - Loss Component onerous test uses the ratio-based methodology from
        the existing Loss Component Calculator:
            Combined Ratio = Loss Ratio + Commission Ratio + Expense Ratio + RA Ratio
            Loss Component = Expected Future Premiums x Max(0, Combined Ratio - 1)
        All ratios sourced from UPLOADED DATA ONLY (no Bootstrap RA call).
      - Financing Adjustment = Opening LRC (excl. Loss) x Locked-in Spot Rate.
      - Closing LRC = Opening LRC + Premiums Received - Insurance Revenue
                      - IACF Paid + IACF Amortised + Financing Adjustment
                      - Investment Components Paid - Loss Reversals + New Losses
    """
    val_date = pd.to_datetime(report_date)
    ifrs17_data = {}

    # ---- CONFIGURATION TOGGLES ----
    st.markdown('<div class="nv-section"><h3>IFRS 17 Configuration Toggles</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        iacf_toggle = st.selectbox("IACF Treatment", ["Expense Immediately", "Capitalize & Amortize"], key="cfg_iacf")
    with c2:
        discount_toggle = st.selectbox("Discounting", ["No Discounting", "Apply Discounting"], key="cfg_discount")
    with c3:
        invest_toggle = st.selectbox("Investment Components", ["No", "Yes"], key="cfg_invest")
    with c4:
        revenue_toggle = st.selectbox("Revenue Method", ["Passage of Time", "Emergence of Risk"], key="cfg_revenue")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- DATA FILES ----
    st.markdown('<div class="nv-section"><h3>Data Files & Column Mapping</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded">', unsafe_allow_html=True)

    # Section 1: Opening Balances
    st.markdown("#### Section 1: Opening Balances")
    ob_file = st.file_uploader("Upload Opening Balances (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_ob")
    if ob_file is not None:
        try:
            ob_df = pd.read_csv(ob_file) if ob_file.name.endswith('.csv') else pd.read_excel(ob_file)
            ob_df.columns = ob_df.columns.astype(str).str.strip()
            st.dataframe(ob_df.head(3), use_container_width=True)
            ob_map = map_columns(ob_df, ['Group','Opening_LRC_Excl_Loss','Opening_Loss_Component'], 'OpeningBalances')
            ob_df = ob_df.rename(columns=ob_map)
            ob_df['Opening_LRC_Excl_Loss'] = pd.to_numeric(ob_df['Opening_LRC_Excl_Loss'], errors='coerce').fillna(0)
            ob_df['Opening_Loss_Component'] = pd.to_numeric(ob_df['Opening_Loss_Component'], errors='coerce').fillna(0)
            ifrs17_data['opening_balances'] = ob_df
            st.markdown('<div class="nv-alert success">✓ Opening balances mapped</div>', unsafe_allow_html=True)
        except Exception as e: st.error(f"Error: {e}")

    # Section 2: Cashflows
    st.markdown("#### Section 2: Cashflows")
    cf_file = st.file_uploader("Upload Cashflows (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_cf")
    if cf_file is not None:
        try:
            cf_df = pd.read_csv(cf_file) if cf_file.name.endswith('.csv') else pd.read_excel(cf_file)
            cf_df.columns = cf_df.columns.astype(str).str.strip()
            st.dataframe(cf_df.head(3), use_container_width=True)
            cf_map = map_columns(cf_df, ['Group','Premiums_Received','IACF_Paid','Investment_Components_Paid'], 'Cashflows')
            cf_df = cf_df.rename(columns=cf_map)
            cf_df['Premiums_Received'] = pd.to_numeric(cf_df['Premiums_Received'], errors='coerce').fillna(0)
            cf_df['IACF_Paid'] = pd.to_numeric(cf_df['IACF_Paid'], errors='coerce').fillna(0)
            cf_df['Investment_Components_Paid'] = pd.to_numeric(cf_df['Investment_Components_Paid'], errors='coerce').fillna(0)
            ifrs17_data['cashflows'] = cf_df
            st.markdown('<div class="nv-alert success">✓ Cashflows mapped</div>', unsafe_allow_html=True)
        except Exception as e: st.error(f"Error: {e}")

    # Section 3: Policy Data
    st.markdown("#### Section 3: Policy Data")
    pdf_file = st.file_uploader("Upload Premium Schedule (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_pd")
    if pdf_file is not None:
        try:
            pol_df = pd.read_csv(pdf_file) if pdf_file.name.endswith('.csv') else pd.read_excel(pdf_file)
            pol_df.columns = pol_df.columns.astype(str).str.strip()
            st.dataframe(pol_df.head(3), use_container_width=True)
            pol_map = map_columns(pol_df, ['Group','Start_Date','End_Date','Written_Premium'], 'PolicyData')
            pol_df = pol_df.rename(columns=pol_map)
            pol_df['Start_Date'] = pd.to_datetime(pol_df['Start_Date'], errors='coerce')
            pol_df['End_Date'] = pd.to_datetime(pol_df['End_Date'], errors='coerce')
            pol_df['Written_Premium'] = pd.to_numeric(pol_df['Written_Premium'], errors='coerce').fillna(0)
            pol_df = pol_df.dropna(subset=['Start_Date','End_Date'])
            pol_df = pol_df[pol_df['End_Date'] > pol_df['Start_Date']]
            ifrs17_data['policy_data'] = pol_df
            st.markdown('<div class="nv-alert success">✓ Policy data mapped</div>', unsafe_allow_html=True)
        except Exception as e: st.error(f"Error: {e}")

    # Section 3b: Investment Components (only if toggle = Yes)
    if invest_toggle == "Yes":
        st.markdown("#### Section 3b: Investment Components")
        ic_file = st.file_uploader("Upload Investment Components by Group (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_ic")
        if ic_file is not None:
            try:
                ic_df = pd.read_csv(ic_file) if ic_file.name.endswith('.csv') else pd.read_excel(ic_file)
                ic_df.columns = ic_df.columns.astype(str).str.strip()
                st.dataframe(ic_df.head(3), use_container_width=True)
                ic_map = map_columns(ic_df, ['Group','Total_Investment_Components'], 'InvestmentComponents')
                ic_df = ic_df.rename(columns=ic_map)
                ic_df['Total_Investment_Components'] = pd.to_numeric(ic_df['Total_Investment_Components'], errors='coerce').fillna(0)
                ifrs17_data['investment_components'] = ic_df
                st.markdown('<div class="nv-alert success">✓ Investment Components mapped</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")

    # Section 4: Loss Component Data — RATIO-BASED METHODOLOGY (uploaded data only)
    st.markdown("#### Section 4: Loss Component Data (Ratio-Based)")
    st.markdown(
        '<div class="nv-alert info">◈ Uses the same methodology as the standalone Loss Component '
        'Calculator: Combined Ratio = Loss Ratio + Commission Ratio + Expense Ratio + RA Ratio. '
        'All ratios are sourced from this uploaded file only — no Bootstrap RA call is made.</div>',
        unsafe_allow_html=True
    )
    lc_file = st.file_uploader("Upload Loss Component Data (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_lc")
    if lc_file is not None:
        try:
            lc_df = pd.read_csv(lc_file) if lc_file.name.endswith('.csv') else pd.read_excel(lc_file)
            lc_df.columns = lc_df.columns.astype(str).str.strip()
            st.dataframe(lc_df.head(3), use_container_width=True)
            lc_map = map_columns(
                lc_df,
                ['Group', 'Expected_Future_Premiums', 'Loss_Ratio', 'Commission_Ratio',
                 'Expense_Ratio', 'RA_Ratio'],
                'LossComponent'
            )
            lc_df = lc_df.rename(columns=lc_map)
            for col in ['Expected_Future_Premiums', 'Loss_Ratio', 'Commission_Ratio',
                       'Expense_Ratio', 'RA_Ratio']:
                lc_df[col] = pd.to_numeric(lc_df[col], errors='coerce').fillna(0)
            ifrs17_data['loss_component'] = lc_df
            st.markdown('<div class="nv-alert success">✓ Loss Component data mapped</div>', unsafe_allow_html=True)
        except Exception as e: st.error(f"Error: {e}")

    # Section 5: Discounting Data (Yield Curve)
    if discount_toggle == "Apply Discounting":
        st.markdown("#### Section 5: Discounting Data (Yield Curve)")
        yc_file = st.file_uploader("Upload Yield Curve (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_yc")
        if yc_file is not None:
            try:
                yc_df = pd.read_csv(yc_file) if yc_file.name.endswith('.csv') else pd.read_excel(yc_file)
                yc_df.columns = yc_df.columns.astype(str).str.strip()
                st.dataframe(yc_df.head(3), use_container_width=True)
                yc_map = map_columns(yc_df, ['Duration_Years','Spot_Rate'], 'YieldCurve')
                yc_df = yc_df.rename(columns=yc_map)
                yc_df['Duration_Years'] = pd.to_numeric(yc_df['Duration_Years'], errors='coerce')
                yc_df['Spot_Rate'] = pd.to_numeric(yc_df['Spot_Rate'], errors='coerce')
                yc_df = yc_df.dropna().sort_values('Duration_Years')
                ifrs17_data['yield_curve'] = yc_df
                st.markdown('<div class="nv-alert success">✓ Yield Curve mapped</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")

    # Section 6: Revenue Recognition Data (Claims Curve)
    if revenue_toggle == "Emergence of Risk":
        st.markdown("#### Section 6: Revenue Recognition Data (Claims Curve)")
        rc_file = st.file_uploader("Upload Claims Emergence Curve (CSV/Excel)", type=["csv","xlsx","xls"], key="ifrs17_rc")
        if rc_file is not None:
            try:
                rc_df = pd.read_csv(rc_file) if rc_file.name.endswith('.csv') else pd.read_excel(rc_file)
                rc_df.columns = rc_df.columns.astype(str).str.strip()
                st.dataframe(rc_df.head(3), use_container_width=True)
                rc_map = map_columns(rc_df, ['Period','Percentage'], 'ClaimsCurve')
                rc_df = rc_df.rename(columns=rc_map)
                rc_df['Percentage'] = pd.to_numeric(rc_df['Percentage'], errors='coerce').fillna(0)
                ifrs17_data['claims_curve'] = rc_df
                st.markdown('<div class="nv-alert success">✓ Claims Curve mapped</div>', unsafe_allow_html=True)
            except Exception as e: st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---- RUN BUTTON ----
    st.markdown('<div class="nv-padded"><br>', unsafe_allow_html=True)
    run_clicked = st.button("⬡  Run Full IFRS 17 LRC Valuation", key="ifrs17_run", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if not run_clicked:
        return

    if 'policy_data' not in ifrs17_data or ifrs17_data['policy_data'].empty:
        st.markdown('<div class="nv-alert warn">⚠ Please upload Policy Data (Section 3) before running.</div>', unsafe_allow_html=True)
        return

    with st.spinner("Running Full IFRS 17 LRC engine..."):
        policy_df = ifrs17_data['policy_data'].copy()
        portfolios = sorted(policy_df['Group'].dropna().unique().tolist())
        st.markdown(f'<div class="nv-alert info">◈ Groups detected: <strong>{" · ".join(portfolios)}</strong></div>', unsafe_allow_html=True)

        # Per-policy day counts (used for both Allocated Premium and UPR comparison)
        policy_df['Policy_Days'] = (policy_df['End_Date'] - policy_df['Start_Date']).dt.days
        policy_df = policy_df[policy_df['Policy_Days'] > 0]
        policy_df['Passed_Days'] = (val_date - policy_df['Start_Date']).dt.days
        policy_df['Passed_Days'] = np.clip(policy_df['Passed_Days'], 0, policy_df['Policy_Days'])
        policy_df['Remaining_Days'] = policy_df['Policy_Days'] - policy_df['Passed_Days']

        # UPR snapshot (used ONLY for the comparison sheet, not the LRC driver)
        policy_df['UPR'] = policy_df['Written_Premium'] * (policy_df['Remaining_Days'] / policy_df['Policy_Days'])

        lrc_results = {}

        for group in portfolios:
            group_policies = policy_df[policy_df['Group'] == group].copy()
            if group_policies.empty:
                continue

            group_cf = (ifrs17_data['cashflows'][ifrs17_data['cashflows']['Group'] == group]
                       if 'cashflows' in ifrs17_data else pd.DataFrame())
            group_ob = (ifrs17_data['opening_balances'][ifrs17_data['opening_balances']['Group'] == group]
                       if 'opening_balances' in ifrs17_data else pd.DataFrame())
            group_lc = (ifrs17_data['loss_component'][ifrs17_data['loss_component']['Group'] == group]
                       if 'loss_component' in ifrs17_data else pd.DataFrame())
            group_ic = (ifrs17_data['investment_components'][ifrs17_data['investment_components']['Group'] == group]
                       if 'investment_components' in ifrs17_data else pd.DataFrame())

            # --- 1. Opening Balances ---
            opening_lrc_excl_loss = float(group_ob['Opening_LRC_Excl_Loss'].values[0]) if not group_ob.empty else 0.0
            opening_loss_component = float(group_ob['Opening_Loss_Component'].values[0]) if not group_ob.empty else 0.0

            # --- 2. Cashflows ---
            premiums_received = float(group_cf['Premiums_Received'].values[0]) if not group_cf.empty else 0.0
            iacf_paid_raw = float(group_cf['IACF_Paid'].values[0]) if not group_cf.empty else 0.0
            investment_components_paid = float(group_cf['Investment_Components_Paid'].values[0]) if not group_cf.empty else 0.0
            iacf_paid = iacf_paid_raw if iacf_toggle == "Capitalize & Amortize" else 0.0

            # --- 3. Weighted Average Duration (for locked-in discount rate lookup) ---
            group_policies['Duration_Years'] = group_policies['Policy_Days'] / 365.25
            total_wp = group_policies['Written_Premium'].sum()
            weighted_duration = (
                np.average(group_policies['Duration_Years'], weights=group_policies['Written_Premium'])
                if total_wp > 0 else 0.0
            )
            locked_in_years = max(1, int(np.ceil(weighted_duration))) if weighted_duration > 0 else 1

            # --- 4. Allocation Factor & Insurance Revenue (CORRECTED — per-policy aggregation) ---
            total_written_premium = total_wp
            total_policy_days = group_policies['Policy_Days'].sum()
            total_passed_days = group_policies['Passed_Days'].sum()

            if revenue_toggle == "Passage of Time":
                allocation_factor = (total_passed_days / total_policy_days) if total_policy_days > 0 else 0.0
                allocated_premium = total_written_premium * allocation_factor
            else:  # Emergence of Risk
                claims_curve = ifrs17_data.get('claims_curve')
                allocation_factor = (
                    float(claims_curve['Percentage'].sum())
                    if claims_curve is not None and not claims_curve.empty else 0.0
                )
                allocated_premium = total_written_premium * allocation_factor

            # Investment components allocated using the same allocation factor
            total_investment_components = (
                float(group_ic['Total_Investment_Components'].values[0])
                if not group_ic.empty else 0.0
            )
            allocated_investment_components = total_investment_components * allocation_factor

            # --- 5. Financing Adjustment (computed before Revenue since Revenue includes it) ---
            locked_in_rate = 0.0
            if discount_toggle == "Apply Discounting":
                yield_curve = ifrs17_data.get('yield_curve')
                if yield_curve is not None and not yield_curve.empty:
                    yc_years = yield_curve['Duration_Years'].values
                    yc_rates = yield_curve['Spot_Rate'].values
                    if locked_in_years in yc_years:
                        locked_in_rate = float(yc_rates[np.where(yc_years == locked_in_years)[0][0]])
                    elif len(yc_years) >= 2:
                        locked_in_rate = float(np.interp(locked_in_years, yc_years, yc_rates))
                    elif len(yc_years) == 1:
                        locked_in_rate = float(yc_rates[0])
            financing_adjustment = opening_lrc_excl_loss * locked_in_rate

            # --- 6. Insurance Revenue (Allocated Premium method, IFRS 17.B126(a)) ---
            insurance_revenue = (allocated_premium - allocated_investment_components) + financing_adjustment

            # --- 7. IACF Amortisation — SAME allocation_factor as Revenue (B125) ---
            iacf_amortized = (iacf_paid * allocation_factor) if iacf_toggle == "Capitalize & Amortize" else 0.0

            # --- 8. Loss Component — RATIO-BASED METHODOLOGY (uploaded data only) ---
            if not group_lc.empty:
                expected_future_premiums = float(group_lc['Expected_Future_Premiums'].values[0])
                loss_ratio       = float(group_lc['Loss_Ratio'].values[0])
                commission_ratio = float(group_lc['Commission_Ratio'].values[0])
                expense_ratio    = float(group_lc['Expense_Ratio'].values[0])
                ra_ratio         = float(group_lc['RA_Ratio'].values[0])

                combined_ratio = loss_ratio + commission_ratio + expense_ratio + ra_ratio
                closing_loss_component = expected_future_premiums * max(0.0, combined_ratio - 1.0)
            else:
                expected_future_premiums = 0.0
                loss_ratio = commission_ratio = expense_ratio = ra_ratio = 0.0
                combined_ratio = 0.0
                closing_loss_component = 0.0

            # Implicit Loss Reversals / New Losses (snapshot reconciliation)
            loss_reversals = min(opening_loss_component, max(allocated_premium, 0.0))
            new_losses_arising = closing_loss_component - opening_loss_component + loss_reversals

            # --- 9. Closing LRC (excl. Loss Component) ---
            closing_lrc_excl_loss = (
                opening_lrc_excl_loss
                + premiums_received
                - insurance_revenue
                - iacf_paid
                + iacf_amortized
                + financing_adjustment
                - investment_components_paid
            )
            total_closing_lrc = closing_lrc_excl_loss + closing_loss_component

            # --- 10. Audit Check ---
            audit_diff = abs(total_closing_lrc - (closing_lrc_excl_loss + closing_loss_component))
            audit_pass = audit_diff <= 0.01

            # --- 11. UPR Comparison (separate calculation, NOT the LRC driver) ---
            upr_snapshot = float(group_policies['UPR'].sum())
            upr_diff_abs = total_closing_lrc - upr_snapshot
            upr_diff_pct = (upr_diff_abs / upr_snapshot * 100) if upr_snapshot != 0 else 0.0

            lrc_results[group] = {
                'Opening_LRC_Excl_Loss': opening_lrc_excl_loss,
                'Opening_Loss_Component': opening_loss_component,
                'Premiums_Received': premiums_received,
                'Allocated_Premium': allocated_premium,
                'Allocated_Investment_Components': allocated_investment_components,
                'Insurance_Revenue': insurance_revenue,
                'IACF_Paid': iacf_paid,
                'IACF_Amortized': iacf_amortized,
                'Financing_Adjustment': financing_adjustment,
                'Locked_In_Rate': locked_in_rate,
                'Locked_In_Years': locked_in_years,
                'Investment_Components_Paid': investment_components_paid,
                'Loss_Ratio': loss_ratio,
                'Commission_Ratio': commission_ratio,
                'Expense_Ratio': expense_ratio,
                'RA_Ratio': ra_ratio,
                'Combined_Ratio': combined_ratio,
                'Expected_Future_Premiums': expected_future_premiums,
                'Loss_Reversals': loss_reversals,
                'New_Losses_Arising': new_losses_arising,
                'Closing_LRC_Excl_Loss': closing_lrc_excl_loss,
                'Closing_Loss_Component': closing_loss_component,
                'Total_Closing_LRC': total_closing_lrc,
                'Audit_Diff': audit_diff,
                'Audit_Pass': audit_pass,
                'UPR_Snapshot': upr_snapshot,
                'UPR_Diff_Abs': upr_diff_abs,
                'UPR_Diff_Pct': upr_diff_pct,
            }

        st.markdown(f'<div class="nv-alert success">✓ Full IFRS 17 LRC calculated for {len(lrc_results)} group(s)</div>', unsafe_allow_html=True)

        # ---- AUDIT WARNING ----
        failed_groups = [g for g, d in lrc_results.items() if not d['Audit_Pass']]
        if failed_groups:
            st.markdown(
                f'<div class="nv-alert warn">⚠ Audit check FAILED for: {", ".join(failed_groups)}. '
                f'Reconciliation difference exceeds tolerance (0.01).</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="nv-alert success">✓ Audit check passed for all groups (LRC mathematically locked).</div>', unsafe_allow_html=True)

        # ---- RESULTS DISPLAY ----
        st.markdown("""
        <div style="padding:1.5rem 2.5rem 0.5rem;">
            <div style="height:1px;background:rgba(37,99,235,0.2);margin-bottom:1.5rem;"></div>
            <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#2563EB;margin-bottom:0.5rem;">Valuation Output</div>
            <div style="font-size:1.35rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.03em;margin-bottom:1.5rem;">IFRS 17 LRC Results</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nv-padded">', unsafe_allow_html=True)

        # 1. LRC Summary
        st.subheader("LRC Summary by Group")
        summary_rows = []
        for group, data in lrc_results.items():
            summary_rows.append({
                'Group': group,
                'LRC (excl. Loss Component)': data['Closing_LRC_Excl_Loss'],
                'Loss Component': data['Closing_Loss_Component'],
                'Total LRC': data['Total_Closing_LRC'],
                'Audit': '✓ Pass' if data['Audit_Pass'] else '✗ Fail',
            })
        summary_df = pd.DataFrame(summary_rows)
        disp_summary = summary_df.copy()
        for c in disp_summary.columns:
            if c not in ('Group', 'Audit'):
                disp_summary[c] = disp_summary[c].apply(lambda x: f"{x:,.2f}")
        st.dataframe(disp_summary, use_container_width=True, hide_index=True)

        # 2. Loss Component Ratio Breakdown
        st.subheader("Loss Component — Ratio Breakdown")
        ratio_rows = []
        for group, data in lrc_results.items():
            ratio_rows.append({
                'Group': group,
                'Loss Ratio': data['Loss_Ratio'],
                'Commission Ratio': data['Commission_Ratio'],
                'Expense Ratio': data['Expense_Ratio'],
                'RA Ratio': data['RA_Ratio'],
                'Combined Ratio': data['Combined_Ratio'],
                'Expected Future Premiums': data['Expected_Future_Premiums'],
                'Loss Component': data['Closing_Loss_Component'],
            })
        ratio_df = pd.DataFrame(ratio_rows)
        disp_ratio = ratio_df.copy()
        for c in ['Loss Ratio', 'Commission Ratio', 'Expense Ratio', 'RA Ratio', 'Combined Ratio']:
            disp_ratio[c] = disp_ratio[c].apply(lambda x: f"{x:.2%}")
        for c in ['Expected Future Premiums', 'Loss Component']:
            disp_ratio[c] = disp_ratio[c].apply(lambda x: f"{x:,.2f}")
        st.dataframe(disp_ratio, use_container_width=True, hide_index=True)

        # 3. LRC Rollforward Per Group
        st.subheader("LRC Rollforward — by Group")
        for group, data in lrc_results.items():
            st.markdown(f'<div style="font-size:0.8rem;font-weight:600;color:#38BDF8;margin:0.75rem 0 0.35rem;">◈ {group}</div>', unsafe_allow_html=True)
            roll_data = {
                "Line Item": [
                    "Opening LRC (excl. Loss)", "Opening Loss Component", "Premiums Received",
                    "Insurance Revenue", "IACF Paid", "IACF Amortized",
                    "Financing Adjustment", "Investment Components Paid",
                    "Loss Reversals", "New Losses Arising",
                    "Closing LRC (excl. Loss)", "Closing Loss Component", "Total Closing LRC"
                ],
                "Amount": [
                    f"{data['Opening_LRC_Excl_Loss']:,.2f}",
                    f"{data['Opening_Loss_Component']:,.2f}",
                    f"{data['Premiums_Received']:,.2f}",
                    f"{-data['Insurance_Revenue']:,.2f}",
                    f"{-data['IACF_Paid']:,.2f}",
                    f"{data['IACF_Amortized']:,.2f}",
                    f"{data['Financing_Adjustment']:,.2f}",
                    f"{-data['Investment_Components_Paid']:,.2f}",
                    f"{-data['Loss_Reversals']:,.2f}",
                    f"{data['New_Losses_Arising']:,.2f}",
                    f"{data['Closing_LRC_Excl_Loss']:,.2f}",
                    f"{data['Closing_Loss_Component']:,.2f}",
                    f"{data['Total_Closing_LRC']:,.2f}"
                ]
            }
            st.dataframe(pd.DataFrame(roll_data), use_container_width=True, hide_index=True)

        # 4. UPR Comparison (IFRS 4 vs IFRS 17) — bridge/cross-check sheet
        st.subheader("UPR Comparison (IFRS 4 vs IFRS 17 LRC)")
        st.markdown(
            '<div class="nv-alert info">◈ This is a transition bridge for client reference. '
            'The UPR snapshot is NOT used to drive the LRC calculation above — it is computed '
            'independently from the same policy data for comparison purposes only.</div>',
            unsafe_allow_html=True
        )
        comparison_rows = []
        for group, data in lrc_results.items():
            comparison_rows.append({
                'Group': group,
                'UPR (IFRS 4)': data['UPR_Snapshot'],
                'Total LRC (IFRS 17)': data['Total_Closing_LRC'],
                'Difference ($)': data['UPR_Diff_Abs'],
                'Difference (%)': f"{data['UPR_Diff_Pct']:.2f}%"
            })
        comparison_df = pd.DataFrame(comparison_rows)
        disp_comp = comparison_df.copy()
        for c in disp_comp.columns:
            if c not in ('Group', 'Difference (%)'):
                disp_comp[c] = disp_comp[c].apply(lambda x: f"{x:,.2f}")
        st.dataframe(disp_comp, use_container_width=True, hide_index=True)

        # 5. Consolidated Rollforward
        st.subheader("Consolidated LRC Rollforward")
        agg = lambda key: sum(d[key] for d in lrc_results.values())
        consol_data = {
            "Line Item": [
                "Opening LRC (excl. Loss)", "Opening Loss Component", "Premiums Received",
                "Insurance Revenue", "IACF Paid", "IACF Amortized",
                "Financing Adjustment", "Investment Components Paid",
                "Loss Reversals", "New Losses Arising",
                "Closing LRC (excl. Loss)", "Closing Loss Component", "Total Closing LRC"
            ],
            "Amount": [
                f"{agg('Opening_LRC_Excl_Loss'):,.2f}", f"{agg('Opening_Loss_Component'):,.2f}",
                f"{agg('Premiums_Received'):,.2f}", f"{-agg('Insurance_Revenue'):,.2f}",
                f"{-agg('IACF_Paid'):,.2f}", f"{agg('IACF_Amortized'):,.2f}",
                f"{agg('Financing_Adjustment'):,.2f}", f"{-agg('Investment_Components_Paid'):,.2f}",
                f"{-agg('Loss_Reversals'):,.2f}", f"{agg('New_Losses_Arising'):,.2f}",
                f"{agg('Closing_LRC_Excl_Loss'):,.2f}", f"{agg('Closing_Loss_Component'):,.2f}",
                f"{agg('Total_Closing_LRC'):,.2f}"
            ]
        }
        st.dataframe(pd.DataFrame(consol_data), use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)

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
                {"Field":"Mode","Value":"Full IFRS 17 LRC (PAA)"},
                {"Field":"IACF Treatment","Value":iacf_toggle},
                {"Field":"Discounting","Value":discount_toggle},
                {"Field":"Investment Components","Value":invest_toggle},
                {"Field":"Revenue Method","Value":revenue_toggle},
            ])
            meta_df.to_excel(w, index=False, sheet_name='Report_Metadata')

            summary_df.to_excel(w, index=False, sheet_name='LRC_Summary')
            ratio_df.to_excel(w, index=False, sheet_name='Loss_Component_Ratios')
            comparison_df.to_excel(w, index=False, sheet_name='UPR_Comparison')
            pd.DataFrame(consol_data).to_excel(w, index=False, sheet_name='LRC_Rollforward_Total')

            for group, data in lrc_results.items():
                roll_data_export = {
                    "Line Item": [
                        "Opening LRC (excl. Loss)", "Opening Loss Component", "Premiums Received",
                        "Insurance Revenue", "IACF Paid", "IACF Amortized",
                        "Financing Adjustment", "Investment Components Paid",
                        "Loss Reversals", "New Losses Arising",
                        "Closing LRC (excl. Loss)", "Closing Loss Component", "Total Closing LRC"
                    ],
                    "Amount": [
                        data['Opening_LRC_Excl_Loss'], data['Opening_Loss_Component'],
                        data['Premiums_Received'], -data['Insurance_Revenue'],
                        -data['IACF_Paid'], data['IACF_Amortized'],
                        data['Financing_Adjustment'], -data['Investment_Components_Paid'],
                        -data['Loss_Reversals'], data['New_Losses_Arising'],
                        data['Closing_LRC_Excl_Loss'], data['Closing_Loss_Component'],
                        data['Total_Closing_LRC']
                    ]
                }
                safe_name = re.sub(r'[\\/*?:\[\]]', '', group)[:28]
                pd.DataFrame(roll_data_export).to_excel(w, index=False, sheet_name=f'LRC_RW_{safe_name}')

        output.seek(0)
        sc = re.sub(r'[\\/*?:"<>|]', "", report_client).strip() or "Client"
        st.download_button(
            "⬇  Download IFRS 17 LRC Report (.xlsx)",
            data=output,
            file_name=f"{sc}_IFRS17_LRC_Report_{report_date}.xlsx",
            key="ifrs17_dl"
        )

# =============================================================================
#  REMAINING PAGES (structure preserved, UI upgraded)
# =============================================================================

def render_lrc():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">Liability for Remaining Coverage</div><h1>Individual <span>LRC</span> Calculators</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="nv-card"><div class="nv-card-icon">◻</div><h3>UPR Calculator</h3><p>Pro-rata unearned premium calculation via 365th, 24th or 8th methods with group-by and multi-column support.</p></div>', unsafe_allow_html=True)
        if st.button("Open UPR Calculator", key="nav_lrc_upr"): navigate_to('upr_calculator', ['Home','Individual Calculators','UPR Calculator']); st.rerun()
    with col2:
        st.markdown('<div class="nv-card"><div class="nv-card-icon">◼</div><h3>Loss Component</h3><p>Onerous contract identification and loss component recognition under IFRS 17 PAA.</p></div>', unsafe_allow_html=True)
        if st.button("Open Loss Component", key="nav_lrc_loss"): navigate_to('loss_component', ['Home','Individual Calculators','Loss Component']); st.rerun()
    back_button('home', ['Home'])

def render_lic():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">Liability for Incurred Claims</div><h1>LIC <span>Calculators</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="nv-card"><div class="nv-card-icon">◈</div><h3>Fulfilment Cashflows</h3><p>OCR, IBNR (multiple methods), ULAE and NPR calculation with full chain-ladder engine.</p></div>', unsafe_allow_html=True)
        if st.button("Open FCF", key="nav_lic_fulfil"): navigate_to('fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows']); st.rerun()
    with col2:
        st.markdown('<div class="nv-card"><div class="nv-card-icon">◈</div><h3>Risk Adjustment</h3><p>Bootstrap, Mack, VaR and Cost of Capital approaches for IFRS 17 risk margin quantification.</p></div>', unsafe_allow_html=True)
        if st.button("Open RA", key="nav_lic_ra"): navigate_to('risk_adjustment', ['Home','LIC','Risk Adjustment']); st.rerun()
    back_button('home', ['Home'])

def render_fulfilment_cashflows():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">LIC · Fulfilment Cashflows</div><h1>FCF <span>Modules</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    items = [("◻","OCR","Case reserve aggregation","ocr_calculator"),("◈","IBNR","Chain-ladder methods","ibnr_menu"),("◼","ULAE","Unallocated LAE","ulae_calculator"),("⬡","NPR","Notified pending reserves","npr_calculator")]
    for i,(icon,t,d,p) in enumerate(items):
        with cols[i]:
            st.markdown(f'<div class="nv-card"><div class="nv-card-icon">{icon}</div><h3>{t}</h3><p>{d}</p></div>', unsafe_allow_html=True)
            if st.button(f"Open {t}", key=f"nav_fc_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows',t]); st.rerun()
    back_button('lic', ['Home','LIC'])

def render_ibnr_menu():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">LIC · IBNR</div><h1>IBNR <span>Methods</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    methods = [("Percentage","ibnr_percentage"),("BCL","bcl_calculator"),("Cape Cod","capecod_calculator"),("Bornhuetter-Ferguson","bf_calculator"),("ELR","elr_calculator"),("ACPC","acpc_calculator")]
    for i in range(0,len(methods),3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(methods):
                n,p = methods[i+j]
                with cols[j]:
                    st.markdown(f'<div class="nv-card"><div class="nv-card-icon">◈</div><h3>{n}</h3></div>', unsafe_allow_html=True)
                    if st.button(f"Open {n}", key=f"nav_ibnr_{p}"): navigate_to(p, ['Home','LIC','Fulfilment Cashflows','IBNR Methods',n]); st.rerun()
    back_button('fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows'])

def render_risk_adjustment():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">LIC · Risk Adjustment</div><h1>RA <span>Methods</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(n,p) in enumerate([("Mack","mack_calculator"),("Bootstrap","bootstrap_calculator"),("VaR","var_calculator"),("Cost of Capital","coc_calculator")]):
        with cols[i]:
            st.markdown(f'<div class="nv-card"><div class="nv-card-icon">◈</div><h3>{n}</h3></div>', unsafe_allow_html=True)
            if st.button(f"Open {n}", key=f"nav_ra_{p}"): navigate_to(p, ['Home','LIC','Risk Adjustment',n]); st.rerun()
    back_button('lic', ['Home','LIC'])

def render_upr_calculator():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">LRC · UPR</div><h1>UPR <span>Calculator</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    with col1: valuation_date=st.date_input("Valuation Date",value=date(2025,12,31),key="upr_vd")
    with col2: client_name=st.text_input("Client",value="Client",key="upr_cn").strip()
    with col3: method=st.selectbox("Method",["365th","24th","8th"],key="upr_mt")
    with col4: pass
    valuation_date=pd.to_datetime(valuation_date)
    uploaded_file=st.file_uploader("Upload premium register (CSV or Excel)",type=["csv","xlsx","xls"],key="upr_f")
    if uploaded_file is not None:
        try:
            original_filename=uploaded_file.name; base_filename=re.sub(r'\.[^.]*$','',original_filename)
            ext=uploaded_file.name.split('.')[-1].lower()
            df=pd.read_csv(uploaded_file) if ext=='csv' else pd.read_excel(uploaded_file)
            unnamed=[c for c in df.columns if c.startswith('Unnamed:')]
            if unnamed: df=df.drop(columns=unnamed)
            all_columns=df.columns.tolist()
            r1,r2=st.columns(2)
            with r1: start_date_col=st.selectbox("Start Date Column",[""]+all_columns,key="upr_sd")
            with r2: end_date_col=st.selectbox("End Date Column",[""]+all_columns,key="upr_ed")
            if not start_date_col or not end_date_col: st.stop()
            grouping_options=[c for c in all_columns if c not in [start_date_col,end_date_col]]
            grouping_cols=st.multiselect("Group by:",options=grouping_options,default=[grouping_options[0]] if grouping_options else [],key="upr_gc")
            if not grouping_cols: st.stop()
            numeric_columns=[c for c in df.columns if c not in [start_date_col,end_date_col]+grouping_cols and pd.api.types.is_numeric_dtype(df[c])]
            selected_value_cols=st.multiselect("Numeric columns:",options=numeric_columns,default=numeric_columns[:min(4,len(numeric_columns))],key="upr_vc")
            if not selected_value_cols: st.stop()
            df_check=df.rename(columns={start_date_col:'Start_Date',end_date_col:'End_Date'})
            df_check['Start_Date']=pd.to_datetime(df_check['Start_Date'],errors='coerce')
            df_check['End_Date']=pd.to_datetime(df_check['End_Date'],errors='coerce')
            bad=df_check.dropna(subset=['Start_Date','End_Date']); bad=bad[bad['End_Date']<=bad['Start_Date']]
            if len(bad)>0: st.error(f"{len(bad)} rows have End_Date ≤ Start_Date."); st.stop()
            df_processed=df_check.dropna(subset=['Start_Date','End_Date']); df_processed=df_processed[df_processed['End_Date']>df_processed['Start_Date']]
            for c in selected_value_cols: df_processed[c]=pd.to_numeric(df_processed[c],errors='coerce')
            df_processed["Duration"]=(df_processed["End_Date"]-df_processed["Start_Date"]).dt.days
            df_processed=df_processed[df_processed["Duration"]>0]
            if df_processed.empty: st.error("No valid policies after date filtering."); st.stop()
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
                st.download_button("⬇  Download UPR Results",data=output,file_name=f"{sc}_{so}_UPR.xlsx",key="upr_dl")
        except Exception as e: st.error(f"Error: {e}")
    back_button('lrc',['Home','Individual Calculators'])

def render_ocr_calculator():
    show_breadcrumb()
    st.markdown('<div class="nv-hero"><div class="nv-hero-eyebrow">LIC · OCR</div><h1>OCR <span>Calculator</span></h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="nv-padded"><br></div>', unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1: client_name=st.text_input("Client",value="Client",key="ocr_cn").strip()
    uploaded_file=st.file_uploader("Upload case estimates file",type=["csv","xlsx","xls"],key="ocr_f")
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
            selected_value_cols=st.multiselect("Numeric columns:",options=numeric_columns,default=numeric_columns[:min(5,len(numeric_columns))],key="ocr_vc")
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
            st.download_button("⬇  Download OCR Results",data=output,file_name=f"{sc}_{so}_OCR.xlsx",key="ocr_dl")
        except Exception as e: st.error(f"Error: {e}")
    back_button('fulfilment_cashflows',['Home','LIC','Fulfilment Cashflows'])

def _coming_soon(title, back_pg, back_bc):
    show_breadcrumb()
    st.markdown(f'<div class="nv-hero"><div class="nv-hero-eyebrow">Module</div><h1>{title}</h1></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:2.5rem;text-align:center;">
        <div style="display:inline-flex;flex-direction:column;align-items:center;gap:1rem;background:rgba(28,35,51,0.5);border:1px solid rgba(37,99,235,0.2);border-radius:14px;padding:2.5rem 3rem;">
            <div style="font-size:2rem;">⬡</div>
            <div style="font-size:0.95rem;font-weight:600;color:#F1F5F9;">Module available for individual use</div>
            <div style="font-size:0.8rem;color:#475569;">This calculator is enabled in the standalone configuration.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    back_button(back_pg, back_bc)

def render_loss_component(): _coming_soon("Loss Component", 'lrc', ['Home','Individual Calculators'])
def render_ibnr_percentage(): _coming_soon("IBNR Percentage", 'ibnr_menu', ['Home','LIC','Fulfilment Cashflows','IBNR Methods'])
def render_bcl_calculator(): _coming_soon("BCL Chain-Ladder", 'ibnr_menu', ['Home','LIC','Fulfilment Cashflows','IBNR Methods'])
def render_capecod_calculator(): _coming_soon("Cape Cod", 'ibnr_menu', ['Home','LIC','Fulfilment Cashflows','IBNR Methods'])
def render_bf_calculator(): _coming_soon("Bornhuetter-Ferguson", 'ibnr_menu', ['Home','LIC','Fulfilment Cashflows','IBNR Methods'])
def render_elr_calculator(): _coming_soon("ELR", 'ibnr_menu', ['Home','LIC','Fulfilment Cashflows','IBNR Methods'])
def render_acpc_calculator(): _coming_soon("ACPC", 'ibnr_menu', ['Home','LIC','Fulfilment Cashflows','IBNR Methods'])
def render_ulae_calculator(): _coming_soon("ULAE", 'fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows'])
def render_npr_calculator(): _coming_soon("NPR", 'fulfilment_cashflows', ['Home','LIC','Fulfilment Cashflows'])
def render_mack_calculator(): _coming_soon("Mack RA", 'risk_adjustment', ['Home','LIC','Risk Adjustment'])
def render_bootstrap_calculator(): _coming_soon("Bootstrap RA", 'risk_adjustment', ['Home','LIC','Risk Adjustment'])
def render_var_calculator(): _coming_soon("VaR RA", 'risk_adjustment', ['Home','LIC','Risk Adjustment'])
def render_coc_calculator(): _coming_soon("Cost of Capital RA", 'risk_adjustment', ['Home','LIC','Risk Adjustment'])

# =============================================================================
#  MAIN ROUTER
# =============================================================================

page_renderers = {
    'home': render_home, 'full_valuation': render_full_valuation,
    'lrc': render_lrc, 'lic': render_lic,
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

# =============================================================================
#  APP ENTRY — gate on auth
# =============================================================================

if not st.session_state.authenticated:
    render_login()
else:
    render_topbar()
    render_sidebar()
    current_page = st.session_state.page
    if current_page in page_renderers:
        page_renderers[current_page]()
    else:
        render_home()
    st.markdown('<div class="nv-footer">© 2026 <span>Next Vantage</span>. All rights reserved. &nbsp;·&nbsp; IFRS 17 PAA Engine v3.9.29.3</div>', unsafe_allow_html=True)
