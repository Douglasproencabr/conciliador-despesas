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
.status-ok {
    background: rgba(63,185,80,0.1);
    border: 1px solid rgba(63,185,80,0.3);
    border-radius: 10px;
    padding: 16px 20px;
    color: #3FB950;
    font-weight: 600;
    font-size: 14px;
    margin: 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.status-error {
    background: rgba(248,81,73,0.1);
    border: 1px solid rgba(248,81,73,0.3);
    border-radius: 10px;
    padding: 16px 20px;
    color: #F85149;
    font-weight: 600;
    font-size: 14px;
    margin: 16px 0;
}

/* ── SPINNER ─────────────────────────────────── */
[data-testid="stSpinner"] { color: #29ABE2 !important; }

/* ── FOOTER ──────────────────────────────────── */
.ciss-footer {
    text-align: center;
    font-size: 11px;
    color: #30363D;
    margin-top: 32px;
    padding-top: 20px;
    border-top: 1px solid #21262D;
}

/* Oculta label vazio dos uploaders */
[data-testid="stFileUploader"] label { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Logo em base64 ──────────────────────────────────────────────────────────
def logo_b64():
    logo_path = os.path.join(os.path.dirname(__file__), "logo_ciss.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# ── HEADER ──────────────────────────────────────────────────────────────────
logo = logo_b64()
logo_html = f'<img src="data:image/png;base64,{logo}" style="height:50px; filter: brightness(0) invert(1);" />' if logo else '<span style="font-size:28px;font-weight:900;color:#29ABE2;">CiSS</span>'

st.markdown(f"""
<div class="ciss-header">
    {logo_html}
    <div style="width:1px;height:40px;background:#30363D;margin:0 4px;"></div>
    <div class="ciss-header-text">
        <h1>Conciliador de Despesas</h1>
        <p>Paytrack &nbsp;×&nbsp; Fatura Bradesco Corporativo</p>
    </div>
    <span class="version-pill">v2.0</span>
</div>
""", unsafe_allow_html=True)


# ── UPLOAD DOS ARQUIVOS ──────────────────────────────────────────────────────
st.markdown('<div class="section-label">📂 Arquivos de entrada</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**📊 Fatura do Cartão**")
    st.caption("Extrato Excel exportado pelo banco")
    excel_file = st.file_uploader("excel", type=["xlsx", "xls"], label_visibility="collapsed", key="excel")

with col2:
    st.markdown("**📄 Relatório Paytrack**")
    st.caption("PDF gerado pelo aplicativo Paytrack")
    pdf_file = st.file_uploader("pdf", type=["pdf"], label_visibility="collapsed", key="pdf")


# ── STATUS DOS ARQUIVOS ──────────────────────────────────────────────────────
files_ok = excel_file is not None and pdf_file is not None

if excel_file:
    st.success(f"✓ Fatura: **{excel_file.name}** ({excel_file.size/1024:.1f} KB)")
if pdf_file:
    st.success(f"✓ Relatório: **{pdf_file.name}** ({pdf_file.size/1024:.1f} KB)")


# ── BOTÃO CONCILIAR ──────────────────────────────────────────────────────────
st.markdown('<div class="ciss-divider"></div>', unsafe_allow_html=True)

iniciar = st.button(
    "⚡  Iniciar Conciliação",
    disabled=not files_ok,
    use_container_width=True,
)

if not files_ok:
    st.markdown(
        '<p style="text-align:center;color:#484F58;font-size:12px;margin-top:8px;">'
        'Selecione os dois arquivos para habilitar a conciliação</p>',
        unsafe_allow_html=True,
    )


# ── PROCESSAMENTO ────────────────────────────────────────────────────────────
if iniciar and files_ok:
    try:
        with st.spinner("Processando conciliação..."):
            from services.conciliador import processar_conciliacao
            excel_bytes_out, resumo = processar_conciliacao(
                excel_file.read(),
                pdf_file.read(),
            )

        # Guarda no session_state para não reprocessar no re-render
        st.session_state["resultado"]    = excel_bytes_out
        st.session_state["resumo"]       = resumo
        st.session_state["nome_arquivo"] = (
            f"conciliacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

    except Exception as e:
        st.markdown(
            f'<div class="status-error">❌ Erro: {e}</div>',
            unsafe_allow_html=True,
        )


# ── RESULTADO ────────────────────────────────────────────────────────────────
if "resultado" in st.session_state:
    resumo = st.session_state["resumo"]

    st.markdown('<div class="ciss-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📊 Resultado da conciliação</div>', unsafe_allow_html=True)

    # Badges 2×2
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card mc-green">
            <div class="metric-top">
                <span class="metric-icon">✅</span>
                <span class="metric-num">{resumo['conciliados']}</span>
            </div>
            <div class="metric-label">Conciliados</div>
            <div class="metric-value">R$ {resumo['valor_conciliado']:,.2f}</div>
        </div>
        <div class="metric-card mc-yellow">
            <div class="metric-top">
                <span class="metric-icon">⚠️</span>
                <span class="metric-num">{resumo['divergentes']}</span>
            </div>
            <div class="metric-label">Divergentes</div>
            <div class="metric-value">R$ {resumo['valor_divergente']:,.2f}</div>
        </div>
        <div class="metric-card mc-red">
            <div class="metric-top">
                <span class="metric-icon">❌</span>
                <span class="metric-num">{resumo['nao_encontrados']}</span>
            </div>
            <div class="metric-label">Não encontr. na Fatura</div>
            <div class="metric-value">R$ {resumo['valor_nao_encontrado']:,.2f}</div>
        </div>
        <div class="metric-card mc-orange">
            <div class="metric-top">
                <span class="metric-icon">❗</span>
                <span class="metric-num">{resumo['nao_lancados']}</span>
            </div>
            <div class="metric-label">Não lançados no Paytrack</div>
            <div class="metric-value">R$ {resumo['valor_nao_lancado']:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botão de download
    st.download_button(
        label="⬇️  Baixar Relatório Excel",
        data=st.session_state["resultado"],
        file_name=st.session_state["nome_arquivo"],
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="ciss-footer">CISS Consultoria em Informática, Serviços e Software S/A</div>',
    unsafe_allow_html=True,
)
