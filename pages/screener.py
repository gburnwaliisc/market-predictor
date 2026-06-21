import json

import pandas as pd
import streamlit as st

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


def _news_badge(articles: list[dict]) -> str:
    if not articles:
        return "–"
    pos = sum(1 for a in articles if a.get("sentiment") == "positive")
    neg = sum(1 for a in articles if a.get("sentiment") == "negative")
    if pos >= 3 and pos > neg:
        return "👍 Good"
    if neg >= 3 and neg > pos:
        return "👎 Bad"
    return "– Neutral"


st.title("Stock Screener")

# Weight sliders in sidebar
cfg = load_config()
st.sidebar.header("Score Weights")

st.sidebar.subheader("Short-Term")
short_labels = ["RSI", "MACD", "Bollinger", "Volume", "Momentum 10d", "News"]
short_weights = [
    st.sidebar.slider(lbl, 0.0, 1.0, float(cfg["short_term"]["weights"][i]), 0.05, key=f"sw{i}")
    for i, lbl in enumerate(short_labels)
]

st.sidebar.subheader("Long-Term")
long_labels = ["P/E", "EPS Growth", "Debt/Equity", "Promoter", "52W Momentum", "News"]
long_weights = [
    st.sidebar.slider(lbl, 0.0, 1.0, float(cfg["long_term"]["weights"][i]), 0.05, key=f"lw{i}")
    for i, lbl in enumerate(long_labels)
]

watchlist = _load_watchlist()
rows = []
bar = st.progress(0, text="Loading stocks…")

for i, stock in enumerate(watchlist):
    sym, name, sector = stock["symbol"], stock["name"], stock.get("sector", "")

    df   = fetch_price_history(sym)
    info = fetch_fundamentals(sym)
    raw  = fetch_news(sym, name)
    arts = classify_articles(raw)
    ns   = news_sentiment_score(arts)
    themes = extract_themes(arts, sector)

    tech = compute_technical(df)
    fund = compute_fundamental(info)

    st_score = score(feature_vector_short(tech, ns), short_weights)
    lt_score = score(feature_vector_long(fund, ns), long_weights)

    price = info.get("price") or (float(df["Close"].iloc[-1]) if not df.empty else None)
    chg   = info.get("day_change_pct")
    top_t = themes[0] if themes else None

    rows.append({
        "Symbol":    sym.replace(".NS", "").replace(".BO", ""),
        "Name":      name,
        "Sector":    sector,
        "Price (₹)": round(price, 1) if price else None,
        "Day Chg%":  round(chg, 2) if chg else None,
        "ST Score":  st_score,
        "LT Score":  lt_score,
        "RSI":       tech.get("rsi_14"),
        "MACD":      "Bull" if tech.get("macd_score", 0.5) > 0.5 else "Bear",
        "News":      _news_badge(arts),
        "Top Theme": (
            ("↑ " if top_t["direction"] == "tailwind" else "↓ " if top_t["direction"] == "headwind" else "")
            + top_t["label"]
            if top_t else "—"
        ),
    })
    bar.progress((i + 1) / len(watchlist), text=f"Loaded {name}")

bar.empty()

df_table = pd.DataFrame(rows)
st.dataframe(
    df_table,
    use_container_width=True,
    column_config={
        "ST Score": st.column_config.ProgressColumn("ST Score", min_value=0, max_value=100, format="%d"),
        "LT Score": st.column_config.ProgressColumn("LT Score", min_value=0, max_value=100, format="%d"),
        "Price (₹)": st.column_config.NumberColumn("Price (₹)", format="₹%.1f"),
        "Day Chg%":  st.column_config.NumberColumn("Day Chg%",  format="%.2f%%"),
    },
    hide_index=True,
)
