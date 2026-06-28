import json

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
from src.ui.styles import (news_badge, page_header, rsi_class, score_badge,
                            section, theme_chip)


def _load_watchlist():
    wl = st.session_state.get("watchlist")
    if wl is None:
        with open("data/watchlist.json") as f:
            wl = json.load(f)
        st.session_state["watchlist"] = wl
    return wl


# ── Sidebar: weight panel ─────────────────────────────────────────────────────
cfg = load_config()
with st.sidebar:
    section("Short-Term Weights")
    short_labels = ["RSI", "MACD", "Bollinger", "Volume", "Momentum 10d", "News"]
    short_weights = [
        st.slider(lbl, 0.0, 1.0, float(cfg["short_term"]["weights"][i]), 0.05, key=f"sw{i}")
        for i, lbl in enumerate(short_labels)
    ]

    section("Long-Term Weights")
    long_labels = ["P/E", "EPS Growth", "Debt/Equity", "Promoter", "52W Momentum", "News"]
    long_weights = [
        st.slider(lbl, 0.0, 1.0, float(cfg["long_term"]["weights"][i]), 0.05, key=f"lw{i}")
        for i, lbl in enumerate(long_labels)
    ]

    st.divider()
    if st.button("⟳ Refresh Data", key="sc_refresh"):
        st.cache_data.clear()
        st.rerun()


# ── Page header ───────────────────────────────────────────────────────────────
page_header("Stock Screener", "All watchlist stocks ranked by signal strength")

# ── Load & compute ────────────────────────────────────────────────────────────
watchlist = _load_watchlist()
rows = []
progress = st.progress(0, text="Initialising…")

for i, stock in enumerate(watchlist):
    sym, name, sector = stock["symbol"], stock["name"], stock.get("sector", "")
    progress.progress((i + 1) / len(watchlist), text=f"Loading {name}…")

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
        "_sym":    sym,
        "_name":   name,
        "_sector": sector,
        "_price":  price,
        "_chg":    chg,
        "_st":     st_score,
        "_lt":     lt_score,
        "_rsi":    tech.get("rsi_14"),
        "_macd":   tech.get("macd_score", 0.5),
        "_arts":   arts,
        "_theme":  top_t,
    })

progress.empty()

# ── Filters ───────────────────────────────────────────────────────────────────
all_sectors = sorted({r["_sector"] for r in rows if r["_sector"]})
sentiments  = ["All", "Good sign", "Bad sign", "Neutral"]

f1, f2, f3, f4 = st.columns([2, 2, 2, 2])
with f1:
    sel_sector = st.selectbox("Sector", ["All"] + all_sectors, label_visibility="visible")
with f2:
    sel_sentiment = st.selectbox("News Sentiment", sentiments, label_visibility="visible")
with f3:
    min_st = st.slider("Min ST Score", 0, 100, 0, 5)
with f4:
    sort_by = st.selectbox("Sort by", ["ST Score ↓", "LT Score ↓", "Price ↑", "Day Change ↑", "Day Change ↓"], label_visibility="visible")

# ── Apply filters ─────────────────────────────────────────────────────────────
def _sentiment_label(arts):
    if not arts:
        return "Neutral"
    pos   = sum(1 for a in arts if a.get("sentiment") == "positive")
    neg   = sum(1 for a in arts if a.get("sentiment") == "negative")
    total = len(arts)
    ratio = pos / total if total else 0
    if ratio >= 0.6:
        return "Good sign"
    if total > 0 and neg / total >= 0.6:
        return "Bad sign"
    return "Neutral"

filtered = [r for r in rows if r["_st"] >= min_st]
if sel_sector != "All":
    filtered = [r for r in filtered if r["_sector"] == sel_sector]
if sel_sentiment != "All":
    filtered = [r for r in filtered if _sentiment_label(r["_arts"]) == sel_sentiment]

sort_key = {
    "ST Score ↓":    lambda r: -r["_st"],
    "LT Score ↓":    lambda r: -r["_lt"],
    "Price ↑":       lambda r: r["_price"] or 0,
    "Day Change ↑":  lambda r: r["_chg"] or 0,
    "Day Change ↓":  lambda r: -(r["_chg"] or 0),
}[sort_by]
filtered.sort(key=sort_key)

# ── Results summary ───────────────────────────────────────────────────────────
section(f"{len(filtered)} stocks  ·  {sort_by}")

# ── HTML Table ────────────────────────────────────────────────────────────────
def _chg_html(chg):
    if chg is None:
        return '<td class="t-rsi-n">—</td>'
    cls = "t-up" if chg >= 0 else "t-down"
    arrow = "▲" if chg >= 0 else "▼"
    return f'<td class="{cls}">{arrow} {chg:+.2f}%</td>'

def _macd_html(macd_score):
    if macd_score > 0.5:
        return '<td><span class="t-bull">▲ Bull</span></td>'
    return '<td><span class="t-bear">▼ Bear</span></td>'

def _theme_html(top_t):
    if not top_t:
        return '<td style="color:#484f58">—</td>'
    return f'<td>{theme_chip(top_t["label"], top_t["direction"])}</td>'

rows_html = ""
for r in filtered:
    sym_short = r["_sym"].replace(".NS", "").replace(".BO", "")
    price_str = f'₹{r["_price"]:,.1f}' if r["_price"] else "—"
    rsi_val   = f'{r["_rsi"]:.1f}' if r["_rsi"] is not None else "—"
    rsi_cls   = rsi_class(r["_rsi"])

    rows_html += (
        f'<tr>'
        f'<td><span class="t-sym">{sym_short}</span></td>'
        f'<td class="t-name">{r["_name"]}</td>'
        f'<td><span class="t-sector">{r["_sector"] or "—"}</span></td>'
        f'<td class="t-price">{price_str}</td>'
        + _chg_html(r["_chg"])
        + f'<td>{score_badge(r["_st"])}</td>'
        + f'<td>{score_badge(r["_lt"])}</td>'
        + f'<td class="{rsi_cls}">{rsi_val}</td>'
        + _macd_html(r["_macd"])
        + f'<td>{news_badge(r["_arts"])}</td>'
        + _theme_html(r["_theme"])
        + '</tr>'
    )

table_html = f"""
<div class="mp-table-wrap">
<table class="mp-table">
  <thead><tr>
    <th>Symbol</th>
    <th>Company</th>
    <th>Sector</th>
    <th>Price</th>
    <th>Day Chg</th>
    <th>ST Score</th>
    <th>LT Score</th>
    <th>RSI</th>
    <th>MACD</th>
    <th>News</th>
    <th>Top Theme</th>
  </tr></thead>
  <tbody>{rows_html}</tbody>
</table>
</div>
"""

if filtered:
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="mp-card" style="text-align:center;padding:2rem">'
        '<p style="color:#8b949e;font-size:0.9rem;margin:0">No stocks match the current filters.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<p style="font-size:0.7rem;color:#484f58;margin-top:0.6rem">'
    'RSI: <span style="color:#f85149">red</span> = overbought (>70) &nbsp;|&nbsp; '
    '<span style="color:#3fb950">green</span> = oversold (<30) &nbsp;|&nbsp; '
    '<span style="color:#e3b341">amber</span> = neutral. '
    'Scores are 0–100 weighted sigmoid; weights adjustable in sidebar.'
    '</p>',
    unsafe_allow_html=True,
)
