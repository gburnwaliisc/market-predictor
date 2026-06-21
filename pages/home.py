import json

import plotly.graph_objects as go
import streamlit as st

from src.data.fetcher import fetch_sensex
from src.news.fetcher import fetch_news
from src.news.sentiment import classify_articles
from src.news.themes import extract_themes

PERIOD_MAP = {"1D": "1d", "1W": "5d", "1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y"}


@st.cache_data(ttl=3600, show_spinner=False)
def _watchlist():
    with open("data/watchlist.json") as f:
        return json.load(f)


st.title("Market Predictor")
st.caption("Sensex tracker + Indian stock investment scorer")

# Sensex chart
col_title, col_period = st.columns([4, 1])
col_title.subheader("Sensex (BSE)")
period_label = col_period.selectbox(
    "Period", list(PERIOD_MAP.keys()), index=4, label_visibility="collapsed"
)

with st.spinner("Loading Sensex..."):
    df = fetch_sensex(PERIOD_MAP[period_label])

if df is not None and not df.empty:
    latest = float(df["Close"].iloc[-1])
    prev = float(df["Close"].iloc[-2]) if len(df) > 1 else latest
    chg = latest - prev
    chg_pct = (chg / prev * 100) if prev else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sensex", f"₹{latest:,.0f}", f"{chg:+,.0f} ({chg_pct:+.2f}%)")
    c2.metric("Period High", f"₹{df['Close'].max():,.0f}")
    c3.metric("Period Low",  f"₹{df['Close'].min():,.0f}")
    c4.metric("Points",      f"{len(df)}")

    line_color = "#16a34a" if chg >= 0 else "#dc2626"
    fig = go.Figure(go.Scatter(
        x=df.index, y=df["Close"], mode="lines",
        line=dict(color=line_color, width=2),
        fill="tozeroy",
        fillcolor=f"rgba({'22,163,74' if chg >= 0 else '220,38,38'},0.06)",
        hovertemplate="₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        plot_bgcolor="white", paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Could not fetch Sensex data. Check your internet connection.")

st.divider()

# Market Themes
st.subheader("Active Market Themes")
st.caption("Aggregated from latest news across your watchlist")

watchlist = _watchlist()
tally: dict[tuple, int] = {}

with st.spinner("Scanning news for themes..."):
    for stock in watchlist:
        raw = fetch_news(stock["symbol"], stock["name"])
        articles = classify_articles(raw)
        themes = extract_themes(articles, stock.get("sector", ""))
        for t in themes:
            key = (t["id"], t["label"], t["direction"])
            tally[key] = tally.get(key, 0) + 1

if tally:
    top5 = sorted(tally.items(), key=lambda x: -x[1])[:5]
    for (tid, label, direction), count in top5:
        icon = "🟢" if direction == "tailwind" else ("🔴" if direction == "headwind" else "⚪")
        arrow = "↑" if direction == "tailwind" else ("↓" if direction == "headwind" else "")
        st.markdown(f"{icon} **{label}** {arrow} — active in news for **{count}** stock(s)")
else:
    st.info("No strong market themes detected in recent headlines.")
