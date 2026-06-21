import json
import os

import plotly.graph_objects as go
import streamlit as st

from src.ai.claude_client import ask_claude, _api_key
from src.data.fetcher import fetch_price_history
from src.data.fundamentals import fetch_fundamentals
from src.model.scorer import (feature_vector_long, feature_vector_short,
                               load_config, score)
from src.news.fetcher import fetch_news
from src.news.sentiment import classify_articles, news_sentiment_score
from src.news.themes import extract_themes
from src.signals.fundamental import compute_fundamental
from src.signals.technical import compute_technical


def _load_watchlist():
    wl = st.session_state.get("watchlist")
    if wl is None:
        with open("data/watchlist.json") as f:
            wl = json.load(f)
        st.session_state["watchlist"] = wl
    return wl


st.title("Stock Detail")

watchlist = _load_watchlist()
options = {f"{s['name']}  ({s['symbol']})": s for s in watchlist}
selected = st.selectbox("Select stock", list(options.keys()))
if not selected:
    st.stop()

stock  = options[selected]
sym    = stock["symbol"]
name   = stock["name"]
sector = stock.get("sector", "")

with st.spinner(f"Loading {name}…"):
    df      = fetch_price_history(sym)
    info    = fetch_fundamentals(sym)
    raw     = fetch_news(sym, name)
    arts    = classify_articles(raw)
    ns      = news_sentiment_score(arts)
    themes  = extract_themes(arts, sector)
    tech    = compute_technical(df)
    fund    = compute_fundamental(info)

cfg      = load_config()
st_score = score(feature_vector_short(tech, ns), cfg["short_term"]["weights"])
lt_score = score(feature_vector_long(fund, ns),  cfg["long_term"]["weights"])

# Header metrics
price = info.get("price") or (float(df["Close"].iloc[-1]) if not df.empty else None)
chg   = info.get("day_change_pct")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Price",            f"₹{price:,.1f}" if price else "—", f"{chg:+.2f}%" if chg else None)
c2.metric("ST Score (1–4W)",  st_score)
c3.metric("LT Score (3–12M)", lt_score)
c4.metric("Sector",           sector or "—")

# Price chart
st.subheader("Price Chart")
overlays = st.multiselect(
    "Overlays", ["SMA 20", "SMA 50", "SMA 200", "Bollinger Bands"],
    default=["SMA 50"],
)

if not df.empty:
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name="Price",
    ))
    close = df["Close"]
    if "SMA 20" in overlays:
        fig.add_trace(go.Scatter(x=df.index, y=close.rolling(20).mean(),  name="SMA 20",  line=dict(color="#3b82f6", width=1)))
    if "SMA 50" in overlays:
        fig.add_trace(go.Scatter(x=df.index, y=close.rolling(50).mean(),  name="SMA 50",  line=dict(color="#f97316", width=1)))
    if "SMA 200" in overlays:
        fig.add_trace(go.Scatter(x=df.index, y=close.rolling(200).mean(), name="SMA 200", line=dict(color="#a855f7", width=1)))
    if "Bollinger Bands" in overlays:
        sma = close.rolling(20).mean()
        std = close.rolling(20).std()
        fig.add_trace(go.Scatter(x=df.index, y=sma + 2*std, name="BB Upper", line=dict(color="#94a3b8", dash="dash"), showlegend=False))
        fig.add_trace(go.Scatter(x=df.index, y=sma - 2*std, name="BB Lower", line=dict(color="#94a3b8", dash="dash"),
                                 fill="tonexty", fillcolor="rgba(148,163,184,0.08)"))
    fig.update_layout(
        height=420, xaxis_rangeslider_visible=False,
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

# Technical signals
st.subheader("Technical Signals")
t1, t2, t3, t4 = st.columns(4)
t1.metric("RSI (14)",          tech.get("rsi_14", "—"))
t2.metric("MACD",              "Bullish" if tech.get("macd_score", 0.5) > 0.5 else "Bearish")
t3.metric("Volume ratio",      tech.get("volume_ratio", "—"))
t4.metric("10d momentum",      f"{tech.get('momentum_10d', 0):+.2f}%")

# Fundamental panel
st.subheader("Fundamentals")
f1, f2, f3, f4 = st.columns(4)
f1.metric("P/E",          fund.get("pe") or "—")
f2.metric("EPS growth",   f"{fund.get('eps_growth', 0) or 0:+.1f}%" if fund.get("eps_growth") is not None else "—")
f3.metric("D/E ratio",    fund.get("debt_equity") or "—")
f4.metric("52W High",     f"₹{info.get('week_52_high'):,.0f}" if info.get("week_52_high") else "—")

st.divider()

# News Feed
st.subheader("Latest News")
if arts:
    for a in arts:
        s = a.get("sentiment", "neutral")
        icon  = "🟢" if s == "positive" else ("🔴" if s == "negative" else "⚪")
        label = "Good sign" if s == "positive" else ("Bad sign" if s == "negative" else "Neutral")
        kws   = ", ".join(a.get("matched_keywords", [])[:2])
        nc1, nc2 = st.columns([6, 1])
        nc1.markdown(f"**{a['title']}**")
        nc1.caption(f"{a.get('source', '')}  ·  {a.get('published_at', '')[:16]}")
        nc2.markdown(f"{icon} {label}")
        if kws:
            nc2.caption(kws)
        st.divider()
else:
    st.info("No recent news found for this stock.")

# Thematic Analysis
st.subheader("Thematic Analysis")
if themes:
    for t in themes:
        if t["direction"] == "tailwind":
            st.success(f"↑ **{t['label']}** (Tailwind) — {t['reason']}")
        elif t["direction"] == "headwind":
            st.error(f"↓ **{t['label']}** (Headwind) — {t['reason']}")
        else:
            st.info(f"**{t['label']}** — {t['reason']}")
else:
    st.info("No strong investment themes detected in recent headlines.")

st.divider()

# Ask Claude
st.subheader("AI Analysis")
has_key = bool(_api_key())
if not has_key:
    st.info("Set `ANTHROPIC_API_KEY` in Streamlit secrets to enable AI reasoning.")
else:
    if st.button("Ask Claude  (~₹0.15)", type="primary"):
        with st.spinner("Asking Claude Haiku…"):
            pos_h = [a["title"] for a in arts if a.get("sentiment") == "positive"][:3]
            neg_h = [a["title"] for a in arts if a.get("sentiment") == "negative"][:3]
            reasoning = ask_claude(
                symbol=sym, name=name, sector=sector,
                tech=tech, fund=fund,
                st_score=st_score, lt_score=lt_score,
                positive_headlines=pos_h, negative_headlines=neg_h,
                themes=themes,
            )
        st.markdown(reasoning)
