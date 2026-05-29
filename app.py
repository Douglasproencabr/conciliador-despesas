import streamlit as st
import base64
import os
from datetime import datetime

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="CISS — Conciliador de Despesas",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS personalizado com identidade CISS ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Reset e base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fundo geral */
.stApp {
    background: #0D1117;
    color: #E6EDF3;
}

/* Remove header padrão do Streamlit */
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #161B22; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }

/* ── HEADER ──────────────────────────────────── */
.ciss-header {
    background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
    border: 1px solid #30363D;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
}
.ciss-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #29ABE2, #1A7FB5, #29ABE2);
}
.ciss-header-text h1 {
    margin: 0;
    font-size: 22px;
    font-weight: 700;
    color: #E6EDF3;
    letter-spacing: -0.3px;
}
.ciss-header-text p {
    margin: 4px 0 0;
    font-size: 13px;
    color: #7D8590;
}
.version-pill {
    background: rgba(41,171,226,0.12);
    border: 1px solid rgba(41,171,226,0.35);
    color: #29ABE2;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    margin-left: auto;
    white-space: nowrap;
}

/* ── SECTION LABELS ──────────────────────────── */
.section-label {
    font-size: 10px;
    font-weight: 700;
    color: #484F58;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin: 24px 0 12px;
}

/* ── UPLOAD CARDS ────────────────────────────── */
.upload-card {
    background: #161B22;
    border: 1px dashed #30363D;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.upload-card:hover { border-color: #29ABE2; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: #161B22 !important;
    border: 1px dashed #30363D !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #29ABE2 !important;
}
[data-testid="stFileUploadDropzone"] {
    background: transparent !important;
}
[data-testid="stFileUploadDropzone"] p {
    color: #7D8590 !important;
}

/* ── BOTÃO PRINCIPAL ─────────────────────────── */
.stButton > button {
    background: linear-gradient(90deg, #1A7FB5 0%, #29ABE2 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    letter-spacing: 0.3px;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    box-shadow: 0 0 20px rgba(41,171,226,0.3) !important;
}
.stButton > button:disabled {
    background: #1C2333 !important;
    color: #484F58 !important;
}

/* ── DOWNLOAD BUTTON ─────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: #161B22 !important;
    color: #29ABE2 !important;
    border: 1.5px solid #29ABE2 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 10px !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #29ABE2 !important;
    color: white !important;
}

/* ── METRIC CARDS ────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 16px 0;
}
.metric-card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.mc-green::before  { background: #3FB950; }
.mc-yellow::before { background: #D29922; }
.mc-red::before    { background: #F85149; }
.mc-orange::before { background: #E3B341; }

.metric-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}
.metric-icon { font-size: 18px; }
.metric-num  {
    font-size: 28px;
    font-weight: 700;
    line-height: 1;
}
.mc-green  .metric-num { color: #3FB950; }
.mc-yellow .metric-num { color: #D29922; }
.mc-red    .metric-num { color: #F85149; }
.mc-orange .metric-num { color: #E3B341; }

.metric-label { font-size: 12px; color: #7D8590; margin-bottom: 2px; }
.metric-value { font-size: 11px; color: #484F58; }

/* ── DIVIDER ─────────────────────────────────── */
.ciss-divider {
    border: none;
    border-top: 1px solid #21262D;
    margin: 24px 0;
}

/* ── ALERTA / STATUS ─────────────────────────── */
.