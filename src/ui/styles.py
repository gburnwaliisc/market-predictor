"""
Global design system — dark professional theme.
Call inject_css() once at the top of every page.
"""

import streamlit as st

# ── Plotly layout defaults ────────────────────────────────────────────────────
PLOTLY_DARK = dict(
    paper_bgcolor="#161b22",
    plot_bgcolor="#161b22",
    font=dict(family="Inter, sans-serif", size=12, color="#8b949e"),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02,
        xanchor="left", x=0, font=dict(size=11),
        bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
    ),
    xaxis=dict(
        showgrid=False, showline=True, linecolor="#30363d",
        tickfont=dict(size=11, color="#8b949e"),
        rangeslider_visible=False,
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#21262d", showline=False,
        tickfont=dict(size=11, color="#8b949e"),
        tickformat=",.0f",
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="#1c2333", bordercolor="#30363d",
        font_size=12, font_color="#f0f6fc",
    ),
    margin=dict(l=0, r=0, t=10, b=0),
)

# ── Master CSS ────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

/* ─── Base ──────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background: #0d1117 !important;
    color: #f0f6fc !important;
}

/* ─── Hide Streamlit chrome ─────────────────────────────────── */
#MainMenu              { visibility: hidden !important; }
footer                 { visibility: hidden !important; }
header                 { visibility: hidden !important; }
.stDeployButton        { display: none !important; }
[data-testid="stToolbar"]   { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ─── Layout ────────────────────────────────────────────────── */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1440px !important;
}

/* ─── Sidebar ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div { color: #c9d1d9 !important; }

section[data-testid="stSidebar"] label {
    color: #8b949e !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f0f6fc !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #21262d !important;
    margin: 0.75rem 0 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: #1f6feb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    width: 100% !important;
    padding: 0.5rem 1rem !important;
    transition: background 0.15s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #388bfd !important;
}
[data-testid="stSidebarNav"] {
    padding-top: 0.25rem !important;
}
[data-testid="stSidebarNav"] a {
    color: #8b949e !important;
    border-radius: 6px !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    transition: all 0.12s !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: #21262d !important;
    color: #f0f6fc !important;
}
[data-testid="stSidebarNav"] [aria-selected="true"] {
    background: #1f6feb !important;
    color: #fff !important;
    font-weight: 600 !important;
}

/* ─── Tabs ──────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background: transparent !important;
    border-bottom: 2px solid #21262d !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #8b949e !important;
    padding: 0.65rem 1.25rem !important;
    border: none !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    transition: color 0.12s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #c9d1d9 !important; }
.stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom-color: #58a6ff !important;
    font-weight: 600 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.25rem !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ─── Buttons ───────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.1rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: #238636 !important;
    border: 1px solid #2ea043 !important;
    color: #fff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2ea043 !important;
    box-shadow: 0 0 0 3px rgba(46,160,67,0.25) !important;
}
.stButton > button[kind="secondary"] {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #30363d !important;
    border-color: #8b949e !important;
}

/* ─── Inputs ────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #f0f6fc !important;
    font-size: 0.875rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
}
.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {
    border-color: #58a6ff !important;
}

/* ─── Native Metrics ────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    color: #8b949e !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #f0f6fc !important;
    font-feature-settings: "tnum" !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"] { font-size: 0.82rem !important; font-weight: 600 !important; }

/* ─── DataFrames ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ─── Alerts ────────────────────────────────────────────────── */
.stAlert { border-radius: 8px !important; border: 1px solid !important; }
[data-testid="stNotification"] { background: #1c2333 !important; border-color: #30363d !important; }
.stSuccess {
    background: rgba(35,134,54,0.12) !important;
    border-color: #238636 !important;
    color: #56d364 !important;
}
.stError {
    background: rgba(248,81,73,0.12) !important;
    border-color: #da3633 !important;
    color: #f85149 !important;
}
.stWarning {
    background: rgba(187,128,9,0.15) !important;
    border-color: #bb8009 !important;
    color: #e3b341 !important;
}
.stInfo {
    background: rgba(31,111,235,0.12) !important;
    border-color: #1f6feb !important;
    color: #58a6ff !important;
}

/* ─── Progress bar ──────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
    border-radius: 99px !important;
}
.stProgress > div > div {
    background: #21262d !important;
    border-radius: 99px !important;
}

/* ─── Expander ──────────────────────────────────────────────── */
details { border: 1px solid #21262d !important; border-radius: 8px !important; }
details summary {
    background: #161b22 !important;
    border-radius: 8px !important;
    color: #c9d1d9 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.75rem 1rem !important;
}

/* ─── Divider ───────────────────────────────────────────────── */
hr { border-color: #21262d !important; }

/* ─── Spinner ───────────────────────────────────────────────── */
.stSpinner > div { border-top-color: #58a6ff !important; }

/* ─── Slider ────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    background: #1f6feb !important; color: #fff !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #58a6ff !important;
}

/* ═══════════════════════════════════════════════════════════════
   Custom Component Classes
═══════════════════════════════════════════════════════════════ */

/* ─── Page Header ───────────────────────────────────────────── */
.mp-page-header {
    padding: 0.25rem 0 1.25rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.5rem;
}
.mp-page-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f0f6fc;
    letter-spacing: -0.02em;
    margin: 0 0 0.2rem;
}
.mp-page-subtitle {
    font-size: 0.8rem;
    color: #8b949e;
    margin: 0;
}

/* ─── Section Header ────────────────────────────────────────── */
.mp-section {
    font-size: 0.7rem;
    font-weight: 700;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #21262d;
    margin: 1.5rem 0 1rem;
}

/* ─── Card ──────────────────────────────────────────────────── */
.mp-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
}
.mp-card-sm {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.75rem 1rem;
}

/* ─── Metric Card ───────────────────────────────────────────── */
.mp-metric { display: flex; flex-direction: column; gap: 0.2rem; }
.mp-metric-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.09em;
}
.mp-metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f0f6fc;
    font-feature-settings: "tnum";
    line-height: 1.15;
}
.mp-metric-value-sm {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f0f6fc;
    font-feature-settings: "tnum";
}
.mp-metric-up   { font-size: 0.8rem; font-weight: 600; color: #3fb950; }
.mp-metric-down { font-size: 0.8rem; font-weight: 600; color: #f85149; }
.mp-metric-neu  { font-size: 0.8rem; font-weight: 600; color: #8b949e; }

/* ─── Score Badges ──────────────────────────────────────────── */
.mp-score-green {
    display: inline-flex; align-items: center; justify-content: center;
    background: rgba(63,185,80,0.15); color: #3fb950;
    font-weight: 700; font-size: 0.85rem;
    padding: 0.2rem 0.65rem; border-radius: 999px;
    min-width: 2.5rem; font-feature-settings: "tnum";
    border: 1px solid rgba(63,185,80,0.3);
}
.mp-score-amber {
    display: inline-flex; align-items: center; justify-content: center;
    background: rgba(187,128,9,0.15); color: #e3b341;
    font-weight: 700; font-size: 0.85rem;
    padding: 0.2rem 0.65rem; border-radius: 999px;
    min-width: 2.5rem; font-feature-settings: "tnum";
    border: 1px solid rgba(187,128,9,0.3);
}
.mp-score-red {
    display: inline-flex; align-items: center; justify-content: center;
    background: rgba(248,81,73,0.15); color: #f85149;
    font-weight: 700; font-size: 0.85rem;
    padding: 0.2rem 0.65rem; border-radius: 999px;
    min-width: 2.5rem; font-feature-settings: "tnum";
    border: 1px solid rgba(248,81,73,0.3);
}

/* ─── News Badges ───────────────────────────────────────────── */
.mp-news-good {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(63,185,80,0.12); color: #3fb950;
    font-size: 0.72rem; font-weight: 700;
    padding: 0.2rem 0.6rem; border-radius: 999px;
    border: 1px solid rgba(63,185,80,0.25); white-space: nowrap;
}
.mp-news-bad {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(248,81,73,0.12); color: #f85149;
    font-size: 0.72rem; font-weight: 700;
    padding: 0.2rem 0.6rem; border-radius: 999px;
    border: 1px solid rgba(248,81,73,0.25); white-space: nowrap;
}
.mp-news-neu {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: rgba(139,148,158,0.1); color: #8b949e;
    font-size: 0.72rem; font-weight: 700;
    padding: 0.2rem 0.6rem; border-radius: 999px;
    border: 1px solid #30363d; white-space: nowrap;
}

/* ─── Theme Chips ───────────────────────────────────────────── */
.mp-chip-tail {
    display: inline-flex; align-items: center; gap: 0.25rem;
    background: rgba(63,185,80,0.12); color: #3fb950;
    font-size: 0.72rem; font-weight: 600;
    padding: 0.2rem 0.65rem; border-radius: 999px;
    margin: 0.15rem; white-space: nowrap;
    border: 1px solid rgba(63,185,80,0.25);
}
.mp-chip-head {
    display: inline-flex; align-items: center; gap: 0.25rem;
    background: rgba(248,81,73,0.12); color: #f85149;
    font-size: 0.72rem; font-weight: 600;
    padding: 0.2rem 0.65rem; border-radius: 999px;
    margin: 0.15rem; white-space: nowrap;
    border: 1px solid rgba(248,81,73,0.25);
}
.mp-chip-neu {
    display: inline-flex; align-items: center; gap: 0.25rem;
    background: rgba(139,148,158,0.1); color: #8b949e;
    font-size: 0.72rem; font-weight: 600;
    padding: 0.2rem 0.65rem; border-radius: 999px;
    margin: 0.15rem; white-space: nowrap;
    border: 1px solid #30363d;
}

/* ─── News Feed Items ───────────────────────────────────────── */
.mp-news-item {
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 0.875rem 1rem; margin-bottom: 0.5rem;
    display: flex; align-items: flex-start; gap: 0.85rem;
    transition: border-color 0.12s, background 0.12s;
}
.mp-news-item:hover { border-color: #58a6ff; background: #1c2333; }
.mp-news-dot {
    width: 9px; height: 9px; border-radius: 50%;
    flex-shrink: 0; margin-top: 0.35rem;
}
.mp-dot-pos { background: #3fb950; }
.mp-dot-neg { background: #f85149; }
.mp-dot-neu { background: #8b949e; }
.mp-news-body { flex: 1; min-width: 0; }
.mp-news-title {
    font-size: 0.875rem; font-weight: 600; color: #c9d1d9;
    line-height: 1.45; margin: 0 0 0.25rem; overflow: hidden;
    text-overflow: ellipsis; white-space: normal;
}
.mp-news-meta { font-size: 0.72rem; color: #8b949e; margin: 0; }

/* ─── Hero Stock Card ───────────────────────────────────────── */
.mp-hero {
    background: linear-gradient(135deg, #0d1117 0%, #1c2333 100%);
    border: 1px solid #30363d; border-radius: 12px;
    padding: 1.5rem 1.75rem; margin-bottom: 1.25rem;
}
.mp-hero-name { font-size: 0.8rem; font-weight: 700; color: #8b949e; letter-spacing: 0.06em; text-transform: uppercase; margin: 0 0 0.35rem; }
.mp-hero-row { display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; }
.mp-hero-price { font-size: 2.4rem; font-weight: 700; color: #f0f6fc; letter-spacing: -0.03em; font-feature-settings: "tnum"; line-height: 1; margin: 0; }
.mp-hero-up   { font-size: 1rem; font-weight: 600; color: #3fb950; }
.mp-hero-down { font-size: 1rem; font-weight: 600; color: #f85149; }
.mp-hero-scores { display: flex; gap: 0.75rem; margin-top: 0.9rem; flex-wrap: wrap; }
.mp-hero-score-label { font-size: 0.68rem; font-weight: 700; color: #8b949e; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 0.25rem; }

/* ─── Signal Row ────────────────────────────────────────────── */
.mp-sig-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.6rem 0; border-bottom: 1px solid #21262d;
}
.mp-sig-row:last-child { border-bottom: none; }
.mp-sig-name { font-size: 0.8rem; color: #8b949e; font-weight: 500; }
.mp-sig-val  { font-size: 0.875rem; font-weight: 700; color: #f0f6fc; font-feature-settings: "tnum"; }
.mp-sig-bar-outer { background: #21262d; border-radius: 99px; height: 5px; width: 80px; flex-shrink: 0; }
.mp-sig-bar-inner { height: 100%; border-radius: 99px; }

/* ─── Watchlist Items ───────────────────────────────────────── */
.mp-wl-item {
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 0.825rem 1.1rem; margin-bottom: 0.4rem;
    display: flex; align-items: center; gap: 0.875rem;
    transition: border-color 0.12s;
}
.mp-wl-item:hover { border-color: #58a6ff; }
.mp-wl-sym {
    font-size: 0.75rem; font-weight: 700; color: #58a6ff;
    background: rgba(31,111,235,0.12); padding: 0.2rem 0.6rem;
    border-radius: 4px; min-width: 5.5rem; text-align: center;
    font-feature-settings: "tnum"; border: 1px solid rgba(31,111,235,0.2);
}
.mp-wl-name { flex: 1; font-size: 0.88rem; font-weight: 600; color: #c9d1d9; }
.mp-wl-sector {
    font-size: 0.72rem; color: #8b949e; background: #21262d;
    padding: 0.15rem 0.5rem; border-radius: 4px;
    border: 1px solid #30363d;
}

/* ─── Index Strip ───────────────────────────────────────────── */
.mp-index-strip {
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    padding: 0.875rem 1.25rem; display: flex;
    align-items: center; gap: 2.5rem; margin-bottom: 1.25rem;
    flex-wrap: wrap;
}
.mp-index-block { display: flex; flex-direction: column; gap: 0.15rem; }
.mp-index-label {
    font-size: 0.65rem; font-weight: 700; color: #8b949e;
    text-transform: uppercase; letter-spacing: 0.1em;
}
.mp-index-val {
    font-size: 1.25rem; font-weight: 700; color: #f0f6fc;
    font-feature-settings: "tnum"; line-height: 1;
}
.mp-index-up   { font-size: 0.8rem; font-weight: 600; color: #3fb950; }
.mp-index-down { font-size: 0.8rem; font-weight: 600; color: #f85149; }
.mp-index-divider {
    width: 1px; height: 2.5rem; background: #30363d; flex-shrink: 0;
}

/* ─── Breadth Bar ───────────────────────────────────────────── */
.mp-breadth-outer {
    background: #21262d; border-radius: 99px; height: 8px;
    margin: 0.5rem 0; overflow: hidden;
}
.mp-breadth-inner {
    height: 100%; background: linear-gradient(90deg, #238636, #3fb950);
    border-radius: 99px;
}

/* ─── Custom HTML Table (Screener) ─────────────────────────── */
.mp-table-wrap {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    overflow: auto; margin-top: 0.75rem;
}
.mp-table {
    width: 100%; border-collapse: collapse;
    font-size: 0.84rem; font-family: 'Inter', sans-serif;
}
.mp-table th {
    background: #0d1117; color: #8b949e;
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    padding: 0.75rem 0.9rem; text-align: left;
    border-bottom: 2px solid #21262d; white-space: nowrap;
    position: sticky; top: 0; z-index: 1;
}
.mp-table th:nth-child(n+5) { text-align: center; }
.mp-table td {
    padding: 0.7rem 0.9rem; border-bottom: 1px solid #21262d;
    color: #c9d1d9; vertical-align: middle; white-space: nowrap;
}
.mp-table td:nth-child(n+5) { text-align: center; }
.mp-table tr:last-child td { border-bottom: none; }
.mp-table tr:hover td { background: #1c2333; }
.mp-table .t-sym {
    font-weight: 700; color: #58a6ff; font-size: 0.82rem;
    font-feature-settings: "tnum";
}
.mp-table .t-name { color: #c9d1d9; font-weight: 500; max-width: 180px; overflow: hidden; text-overflow: ellipsis; }
.mp-table .t-sector {
    font-size: 0.68rem; color: #8b949e; background: #21262d;
    padding: 0.1rem 0.4rem; border-radius: 3px;
    border: 1px solid #30363d;
}
.mp-table .t-price { font-weight: 600; font-feature-settings: "tnum"; color: #f0f6fc; }
.mp-table .t-up   { color: #3fb950; font-weight: 600; font-feature-settings: "tnum"; }
.mp-table .t-down { color: #f85149; font-weight: 600; font-feature-settings: "tnum"; }
.mp-table .t-rsi-ob { color: #f85149; font-weight: 700; font-feature-settings: "tnum"; }
.mp-table .t-rsi-os { color: #3fb950; font-weight: 700; font-feature-settings: "tnum"; }
.mp-table .t-rsi-n  { color: #e3b341; font-weight: 600; font-feature-settings: "tnum"; }
.mp-table .t-bull {
    color: #3fb950; background: rgba(63,185,80,0.12);
    padding: 0.15rem 0.5rem; border-radius: 4px;
    font-size: 0.72rem; font-weight: 700;
    border: 1px solid rgba(63,185,80,0.25);
}
.mp-table .t-bear {
    color: #f85149; background: rgba(248,81,73,0.12);
    padding: 0.15rem 0.5rem; border-radius: 4px;
    font-size: 0.72rem; font-weight: 700;
    border: 1px solid rgba(248,81,73,0.25);
}

/* ─── Theme Panel Cards ─────────────────────────────────────── */
.mp-theme-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 0.875rem 1.1rem; margin-bottom: 0.5rem;
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
}
.mp-theme-card:hover { border-color: #58a6ff; }
.mp-theme-title { font-size: 0.875rem; font-weight: 600; color: #c9d1d9; margin: 0 0 0.15rem; }
.mp-theme-count { font-size: 0.72rem; color: #8b949e; }
.mp-theme-dir-tail {
    font-size: 0.72rem; font-weight: 700; color: #3fb950;
    background: rgba(63,185,80,0.12); padding: 0.25rem 0.75rem;
    border-radius: 999px; border: 1px solid rgba(63,185,80,0.3);
    white-space: nowrap;
}
.mp-theme-dir-head {
    font-size: 0.72rem; font-weight: 700; color: #f85149;
    background: rgba(248,81,73,0.12); padding: 0.25rem 0.75rem;
    border-radius: 999px; border: 1px solid rgba(248,81,73,0.3);
    white-space: nowrap;
}
.mp-theme-dir-neu {
    font-size: 0.72rem; font-weight: 700; color: #8b949e;
    background: rgba(139,148,158,0.1); padding: 0.25rem 0.75rem;
    border-radius: 999px; border: 1px solid #30363d;
    white-space: nowrap;
}

/* ─── Sidebar Brand ─────────────────────────────────────────── */
.mp-brand {
    font-size: 1.05rem; font-weight: 700; color: #f0f6fc !important;
    letter-spacing: -0.01em;
}
.mp-brand-accent { color: #58a6ff !important; }
.mp-brand-tag {
    font-size: 0.65rem; font-weight: 600; color: #8b949e !important;
    text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.1rem;
    display: block;
}

/* ─── Filter Bar ────────────────────────────────────────────── */
.mp-filter-bar {
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 0.75rem 1rem; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
}

/* ─── Add Stock Form ────────────────────────────────────────── */
.mp-form-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    padding: 1.25rem 1.5rem; margin-top: 1rem;
}
.mp-form-title {
    font-size: 0.75rem; font-weight: 700; color: #8b949e;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin: 0 0 1rem; padding-bottom: 0.6rem;
    border-bottom: 1px solid #21262d;
}

/* ─── Score Bar ─────────────────────────────────────────────── */
.mp-bar-wrap { margin-bottom: 0.5rem; }
.mp-bar-label {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.3rem;
}
.mp-bar-name { font-size: 0.78rem; color: #8b949e; font-weight: 500; }
.mp-bar-val  { font-size: 0.78rem; font-weight: 700; color: #f0f6fc; font-feature-settings: "tnum"; }
.mp-bar-outer { background: #21262d; border-radius: 99px; height: 6px; }
.mp-bar-inner { height: 100%; border-radius: 99px; }

/* ─── Last-refresh tag ──────────────────────────────────────── */
.mp-refresh-tag {
    font-size: 0.68rem; color: #8b949e; font-style: italic;
}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


# ── HTML component helpers ────────────────────────────────────────────────────

def score_badge(val: int) -> str:
    if val >= 70:
        return f'<span class="mp-score-green">{val}</span>'
    elif val >= 40:
        return f'<span class="mp-score-amber">{val}</span>'
    return f'<span class="mp-score-red">{val}</span>'


def news_badge(articles: list) -> str:
    if not articles:
        return '<span class="mp-news-neu">— No news</span>'
    pos   = sum(1 for a in articles if a.get("sentiment") == "positive")
    neg   = sum(1 for a in articles if a.get("sentiment") == "negative")
    total = len(articles)
    ratio = pos / total if total else 0
    if ratio >= 0.6:
        return '<span class="mp-news-good">▲ Good sign</span>'
    if total > 0 and neg / total >= 0.6:
        return '<span class="mp-news-bad">▼ Bad sign</span>'
    return '<span class="mp-news-neu">─ Neutral</span>'


def theme_chip(label: str, direction: str) -> str:
    if direction == "tailwind":
        return f'<span class="mp-chip-tail">↑ {label}</span>'
    elif direction == "headwind":
        return f'<span class="mp-chip-head">↓ {label}</span>'
    return f'<span class="mp-chip-neu">{label}</span>'


def section(title: str) -> None:
    st.markdown(f'<div class="mp-section">{title}</div>', unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="mp-page-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="mp-page-header">'
        f'<h1 class="mp-page-title">{title}</h1>{sub}'
        f'</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, delta: str = "", delta_dir: str = "neu") -> str:
    delta_cls = {"up": "mp-metric-up", "down": "mp-metric-down"}.get(delta_dir, "mp-metric-neu")
    delta_html = f'<span class="{delta_cls}">{delta}</span>' if delta else ""
    return (
        f'<div class="mp-card mp-metric">'
        f'<span class="mp-metric-label">{label}</span>'
        f'<span class="mp-metric-value">{value}</span>'
        f'{delta_html}'
        f'</div>'
    )


def score_bar(name: str, value: float, color: str = "#58a6ff") -> str:
    pct = round(value * 100)
    return (
        f'<div class="mp-bar-wrap">'
        f'<div class="mp-bar-label">'
        f'<span class="mp-bar-name">{name}</span>'
        f'<span class="mp-bar-val">{pct}</span>'
        f'</div>'
        f'<div class="mp-bar-outer">'
        f'<div class="mp-bar-inner" style="width:{pct}%;background:{color}"></div>'
        f'</div></div>'
    )


def rsi_class(rsi) -> str:
    try:
        v = float(rsi)
        if v > 70: return "t-rsi-ob"
        if v < 30: return "t-rsi-os"
    except (TypeError, ValueError):
        pass
    return "t-rsi-n"
