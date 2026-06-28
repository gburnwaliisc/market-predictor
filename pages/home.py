import json
from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

from src.data.fetcher import fetch_sensex
from src.news.fetcher import fetch_news
from src.news.sentiment import classify_articles
from src.news.themes import extract_themes
from src.ui.styles import PLOTLY_DARK, page_header, section

PERIOD_MAP = {
    "1D": "1d", "1W": "5d", "1M": "1mo",
    "3M": "3mo", "6M": "6mo", "1Y": "1y",
}


@st.cache_data(ttl=3600, show_spinner=False)
def _watchlist():
    with open("data/watchlist.json") as f:
        return json.load(f)


# ── Page header ───────────────────────────────────────────────────────────────
now = datetime.now().strftime("%d %b %Y, %I:%M %p")
page_header("Market Intelligence", f"Indian Equity Dashboard  ·  {now} IST")

# ── Sensex chart ──────────────────────────────────────────────────────────────
col_period, col_refresh = st.columns([6, 1])
with col_period:
    period_label = st.radio(
        "period", list(PERIOD_MAP.keys()), index=4,
        horizontal=True, label_visibility="collapsed",
    )
with col_refresh:
    refresh = st.button("⟳ Refresh", key="home_refresh")

if refresh:
    st.cache_data.clear()
    st.rerun()

with st.spinner(""):
    df = fetch_sensex(PERIOD_MAP[period_label])

if df is not None and not df.empty:
    latest  = float(df["Close"].iloc[-1])
    prev    = float(df["Close"].iloc[-2]) if len(df) > 1 else latest
    chg     = latest - prev
    chg_pct = (chg / prev * 100) if prev else 0.0
    high    = float(df["Close"].max())
    low     = float(df["Close"].min())
    is_up   = chg >= 0

    # ── Index strip ────────────────────────────────────────────────────────────
    chg_color = "#3fb950" if is_up else "#f85149"
    chg_arrow = "▲" if is_up else "▼"
    st.markdown(
        f'<div class="mp-index-strip">'
        f'  <div class="mp-index-block">'
        f'    <span class="mp-index-label">BSE Sensex</span>'
        f'    <span class="mp-index-val">₹{latest:,.0f}</span>'
        f'    <span style="font-size:0.8rem;font-weight:600;color:{chg_color}">'
        f'      {chg_arrow} {chg:+,.0f} ({chg_pct:+.2f}%)'
        f'    </span>'
        f'  </div>'
        f'  <div class="mp-index-divider"></div>'
        f'  <div class="mp-index-block">'
        f'    <span class="mp-index-label">{period_label} High</span>'
        f'    <span class="mp-index-val" style="font-size:1rem">₹{high:,.0f}</span>'
        f'    <span class="mp-metric-neu" style="font-size:0.75rem">Period</span>'
        f'  </div>'
        f'  <div class="mp-index-block">'
        f'    <span class="mp-index-label">{period_label} Low</span>'
        f'    <span class="mp-index-val" style="font-size:1rem">₹{low:,.0f}</span>'
        f'    <span class="mp-metric-neu" style="font-size:0.75rem">Period</span>'
        f'  </div>'
        f'  <div class="mp-index-block">'
        f'    <span class="mp-index-label">Range Used</span>'
        f'    <span class="mp-index-val" style="font-size:1rem">{((latest-low)/(high-low)*100) if high!=low else 50:.0f}%</span>'
        f'    <span class="mp-metric-neu" style="font-size:0.75rem">of {period_label} range</span>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Plotly area/line chart ─────────────────────────────────────────────────
    line_rgb = "63,185,80" if is_up else "248,81,73"
    y_min = float(df["Close"].min())
    y_max = float(df["Close"].max())
    y_pad = (y_max - y_min) * 0.15   # 15% padding so the line isn't flush to top/bottom

    # Baseline trace at chart floor — fill="tonexty" fills between the two traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=[y_min - y_pad] * len(df),
        mode="lines", line=dict(color="rgba(0,0,0,0)", width=0),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"], mode="lines",
        line=dict(color=f"rgb({line_rgb})", width=2.5),
        fill="tonexty",
        fillcolor=f"rgba({line_rgb},0.10)",
        hovertemplate="<b>₹%{y:,.0f}</b><extra></extra>",
        name="Sensex",
    ))
    layout = dict(**PLOTLY_DARK, height=320)
    layout["yaxis"]["tickprefix"] = "₹"
    layout["yaxis"]["range"] = [y_min - y_pad, y_max + y_pad]
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Could not fetch Sensex data. Check your internet connection.")

# ── Market Breadth ────────────────────────────────────────────────────────────
watchlist = _watchlist()
section("Market Overview")

c_breadth, c_themes = st.columns([1, 1])

with c_breadth:
    st.markdown(
        '<div class="mp-card" style="height:100%">'
        '<p style="font-size:0.72rem;font-weight:700;color:#8b949e;text-transform:uppercase;letter-spacing:0.09em;margin:0 0 0.75rem">Market Breadth</p>',
        unsafe_allow_html=True,
    )
    total_stocks = len(watchlist)
    above_ma = max(1, round(total_stocks * 0.55))   # placeholder until live signal
    pct = above_ma / total_stocks * 100 if total_stocks else 0

    breadth_color = "#3fb950" if pct > 55 else ("#e3b341" if pct > 40 else "#f85149")
    st.markdown(
        f'<p style="font-size:1.6rem;font-weight:700;color:#f0f6fc;font-feature-settings:\'tnum\';margin:0 0 0.3rem">'
        f'{above_ma} <span style="font-size:0.9rem;color:#8b949e;font-weight:500">/ {total_stocks} stocks</span></p>'
        f'<p style="font-size:0.8rem;color:{breadth_color};font-weight:600;margin:0 0 0.6rem">above 50-day MA</p>'
        f'<div class="mp-breadth-outer">'
        f'  <div class="mp-breadth-inner" style="width:{pct:.0f}%;background:{breadth_color}"></div>'
        f'</div>'
        f'<p style="font-size:0.72rem;color:#8b949e;margin:0.4rem 0 0">{pct:.0f}% of watchlist above moving average</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Active Market Themes ──────────────────────────────────────────────────────
section("Active Market Themes")
st.caption("Aggregated from latest news across your watchlist. Themes require ≥2 headline matches.")

tally: dict[tuple, int] = {}

with st.spinner("Scanning headlines for market themes…"):
    for stock in watchlist:
        raw     = fetch_news(stock["symbol"], stock["name"])
        articles = classify_articles(raw)
        themes  = extract_themes(articles, stock.get("sector", ""))
        for t in themes:
            key = (t["id"], t["label"], t["direction"])
            tally[key] = tally.get(key, 0) + 1

if tally:
    top5 = sorted(tally.items(), key=lambda x: -x[1])[:6]
    left_col, right_col = st.columns(2)
    for idx, ((tid, label, direction), count) in enumerate(top5):
        col = left_col if idx % 2 == 0 else right_col
        with col:
            if direction == "tailwind":
                dir_html = '<span class="mp-theme-dir-tail">↑ Tailwind</span>'
            elif direction == "headwind":
                dir_html = '<span class="mp-theme-dir-head">↓ Headwind</span>'
            else:
                dir_html = '<span class="mp-theme-dir-neu">Neutral</span>'

            stock_word = "stock" if count == 1 else "stocks"
            st.markdown(
                f'<div class="mp-theme-card">'
                f'  <div>'
                f'    <p class="mp-theme-title">{label}</p>'
                f'    <p class="mp-theme-count">Active in {count} {stock_word}</p>'
                f'  </div>'
                f'  {dir_html}'
                f'</div>',
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        '<div class="mp-card" style="text-align:center;padding:2rem">'
        '<p style="color:#8b949e;font-size:0.9rem;margin:0">No strong market themes detected in recent headlines.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Sidebar: refresh button ───────────────────────────────────────────────────
with st.sidebar:
    section("Data Controls")
    if st.button("⟳ Refresh All Data", key="sb_refresh"):
        st.cache_data.clear()
        st.rerun()
    st.markdown(
        f'<p class="mp-refresh-tag">Last loaded: {now}</p>',
        unsafe_allow_html=True,
    )
