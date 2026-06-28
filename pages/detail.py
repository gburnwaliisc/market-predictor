import json

import plotly.graph_objects as go
import streamlit as st

from src.ai.claude_client import _api_key, ask_claude
from src.data.fetcher import fetch_price_history
from src.data.fundamentals import fetch_fundamentals
from src.model.scorer import (feature_vector_long, feature_vector_short,
                               load_config, score)
from src.news.fetcher import fetch_news
from src.news.sentiment import classify_articles, news_sentiment_score
from src.news.themes import extract_themes
from src.signals.fundamental import compute_fundamental
from src.signals.technical import compute_technical
from src.ui.styles import (PLOTLY_DARK, page_header, score_badge, score_bar,
                            section, theme_chip)


def _load_watchlist():
    wl = st.session_state.get("watchlist")
    if wl is None:
        with open("data/watchlist.json") as f:
            wl = json.load(f)
        st.session_state["watchlist"] = wl
    return wl


# ── Stock selector ────────────────────────────────────────────────────────────
page_header("Stock Detail", "Deep-dive analysis with signals, news, and AI reasoning")

watchlist = _load_watchlist()
options = {f"{s['name']}  ({s['symbol']})": s for s in watchlist}

sel_col, _ = st.columns([2, 2])
with sel_col:
    selected = st.selectbox("Select stock", list(options.keys()), label_visibility="collapsed")

if not selected:
    st.stop()

stock  = options[selected]
sym    = stock["symbol"]
name   = stock["name"]
sector = stock.get("sector", "")

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner(f"Loading {name}…"):
    df     = fetch_price_history(sym)
    info   = fetch_fundamentals(sym)
    raw    = fetch_news(sym, name)
    arts   = classify_articles(raw)
    ns     = news_sentiment_score(arts)
    themes = extract_themes(arts, sector)
    tech   = compute_technical(df)
    fund   = compute_fundamental(info)

cfg      = load_config()
st_score = score(feature_vector_short(tech, ns), cfg["short_term"]["weights"])
lt_score = score(feature_vector_long(fund, ns),  cfg["long_term"]["weights"])

price = info.get("price") or (float(df["Close"].iloc[-1]) if not df.empty else None)
chg   = info.get("day_change_pct")

# ── Hero card ─────────────────────────────────────────────────────────────────
sym_short  = sym.replace(".NS", "").replace(".BO", "")
price_str  = f"₹{price:,.2f}" if price else "—"
is_up      = (chg or 0) >= 0
chg_cls    = "mp-hero-up" if is_up else "mp-hero-down"
chg_str    = f'{"▲" if is_up else "▼"} {abs(chg):.2f}%' if chg is not None else ""
sector_tag = f'<span class="mp-chip-neu" style="font-size:0.75rem">{sector}</span>' if sector else ""

st_badge = score_badge(st_score)
lt_badge = score_badge(lt_score)

st.markdown(
    f'<div class="mp-hero">'
    f'  <p class="mp-hero-name">{sym_short}  ·  {sector}</p>'
    f'  <div class="mp-hero-row">'
    f'    <span class="mp-hero-price">{price_str}</span>'
    f'    <span class="{chg_cls}">{chg_str}</span>'
    f'  </div>'
    f'  <div class="mp-hero-scores">'
    f'    <div>'
    f'      <span class="mp-hero-score-label">Short-Term (1–4W)</span>'
    f'      {st_badge}'
    f'    </div>'
    f'    <div>'
    f'      <span class="mp-hero-score-label">Long-Term (3–12M)</span>'
    f'      {lt_badge}'
    f'    </div>'
    f'  </div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_chart, tab_signals, tab_fund, tab_news, tab_ai = st.tabs([
    "📈 Chart", "⚡ Signals", "📋 Fundamentals", "📰 News", "🤖 AI Analysis",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHART
# ════════════════════════════════════════════════════════════════════════════════
with tab_chart:
    overlay_col, _ = st.columns([3, 1])
    with overlay_col:
        overlays = st.multiselect(
            "Overlays",
            ["SMA 20", "SMA 50", "SMA 200", "Bollinger Bands"],
            default=["SMA 50"],
        )

    if not df.empty:
        close = df["Close"]
        fig = go.Figure()

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=close, name="Price",
            increasing_line_color="#3fb950", decreasing_line_color="#f85149",
            increasing_fillcolor="rgba(63,185,80,0.8)",
            decreasing_fillcolor="rgba(248,81,73,0.8)",
        ))

        sma_styles = {
            "SMA 20":  ("#58a6ff", 1.5),
            "SMA 50":  ("#e3b341", 1.5),
            "SMA 200": ("#bc8cff", 1.5),
        }
        for name_key, (clr, w) in sma_styles.items():
            if name_key in overlays:
                window = int(name_key.split()[1])
                fig.add_trace(go.Scatter(
                    x=df.index, y=close.rolling(window).mean(),
                    name=name_key, line=dict(color=clr, width=w),
                    hovertemplate=f"{name_key}: ₹%{{y:,.0f}}<extra></extra>",
                ))

        if "Bollinger Bands" in overlays:
            sma = close.rolling(20).mean()
            std = close.rolling(20).std()
            fig.add_trace(go.Scatter(
                x=df.index, y=sma + 2*std, name="BB Upper",
                line=dict(color="#8b949e", dash="dash", width=1),
                showlegend=False,
                hovertemplate="BB Upper: ₹%{y:,.0f}<extra></extra>",
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=sma - 2*std, name="BB Lower",
                line=dict(color="#8b949e", dash="dash", width=1),
                fill="tonexty", fillcolor="rgba(139,148,158,0.07)",
                showlegend=False,
                hovertemplate="BB Lower: ₹%{y:,.0f}<extra></extra>",
            ))

        layout = dict(**PLOTLY_DARK, height=440)
        layout["xaxis"]["rangeslider_visible"] = False
        layout["yaxis"]["tickprefix"] = "₹"
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)

        # Volume sub-chart
        vol_colors = [
            "rgba(63,185,80,0.6)" if float(df["Close"].iloc[i]) >= float(df["Open"].iloc[i])
            else "rgba(248,81,73,0.6)"
            for i in range(len(df))
        ]
        fig_vol = go.Figure(go.Bar(
            x=df.index, y=df["Volume"], marker_color=vol_colors,
            name="Volume",
            hovertemplate="%{y:,.0f}<extra></extra>",
        ))
        vol_layout = dict(**PLOTLY_DARK, height=110)
        vol_layout["margin"] = dict(l=0, r=0, t=5, b=0)
        vol_layout["yaxis"]["tickformat"] = ",.0s"
        vol_layout["showlegend"] = False
        fig_vol.update_layout(**vol_layout)
        st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.info("No price data available for this symbol.")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — SIGNALS
# ════════════════════════════════════════════════════════════════════════════════
with tab_signals:
    sig_left, sig_right = st.columns(2)

    rsi_val  = tech.get("rsi_14")
    macd_s   = tech.get("macd_score", 0.5)
    vol_r    = tech.get("volume_ratio")
    mom_10d  = tech.get("momentum_10d", 0)

    with sig_left:
        section("Short-Term Signals")
        fv = feature_vector_short(tech, ns)
        labels = ["RSI", "MACD", "Bollinger", "Volume", "Momentum 10d", "News Sentiment"]
        colors = ["#58a6ff", "#3fb950", "#e3b341", "#bc8cff", "#f0883e", "#58d9f9"]
        bars_html = "".join(score_bar(labels[i], fv[i], colors[i]) for i in range(len(fv)))
        st.markdown(f'<div class="mp-card">{bars_html}</div>', unsafe_allow_html=True)

    with sig_right:
        section("Long-Term Signals")
        fv_lt = feature_vector_long(fund, ns)
        labels_lt = ["P/E vs Sector", "EPS Growth", "Debt/Equity", "Promoter Holding", "52W Momentum", "News Sentiment"]
        colors_lt = ["#58a6ff", "#3fb950", "#e3b341", "#bc8cff", "#f0883e", "#58d9f9"]
        bars_html_lt = "".join(score_bar(labels_lt[i], fv_lt[i], colors_lt[i]) for i in range(len(fv_lt)))
        st.markdown(f'<div class="mp-card">{bars_html_lt}</div>', unsafe_allow_html=True)

    section("Technical Readings")
    m1, m2, m3, m4 = st.columns(4)
    rsi_color = "#f85149" if (rsi_val or 50) > 70 else ("#3fb950" if (rsi_val or 50) < 30 else "#e3b341")
    m1.metric("RSI (14-day)", f"{rsi_val:.1f}" if rsi_val else "—")
    m2.metric("MACD", "Bullish" if macd_s > 0.5 else "Bearish",
              "↑ Above signal" if macd_s > 0.5 else "↓ Below signal")
    m3.metric("Volume vs 20d Avg", f"{vol_r:.2f}×" if vol_r else "—",
              "High volume" if (vol_r or 0) > 1.5 else "Normal")
    m4.metric("10-day Momentum", f"{mom_10d:+.2f}%" if mom_10d else "—")

    # RSI gauge
    if rsi_val is not None:
        section("RSI Gauge")
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(rsi_val),
            gauge=dict(
                axis=dict(range=[0, 100], tickwidth=1, tickcolor="#8b949e", tickfont=dict(color="#8b949e")),
                bar=dict(color=rsi_color, thickness=0.3),
                bgcolor="#21262d",
                steps=[
                    dict(range=[0, 30],  color="rgba(63,185,80,0.15)"),
                    dict(range=[30, 70], color="rgba(139,148,158,0.08)"),
                    dict(range=[70, 100], color="rgba(248,81,73,0.15)"),
                ],
                threshold=dict(line=dict(color="#8b949e", width=2), thickness=0.75, value=50),
            ),
            number=dict(suffix="", font=dict(size=32, color="#f0f6fc")),
        ))
        gauge.update_layout(
            height=200, margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#161b22", font=dict(color="#8b949e"),
        )
        g_col, _ = st.columns([1, 2])
        with g_col:
            st.plotly_chart(gauge, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — FUNDAMENTALS
# ════════════════════════════════════════════════════════════════════════════════
with tab_fund:
    section("Valuation & Growth")
    f1, f2, f3, f4 = st.columns(4)
    pe_val    = fund.get("pe")
    eps_val   = fund.get("eps_growth")
    de_val    = fund.get("debt_equity")
    prom_val  = info.get("promoter_holding")
    w52h      = info.get("week_52_high")
    w52l      = info.get("week_52_low")

    f1.metric("P/E Ratio",       f"{pe_val:.1f}" if pe_val else "—",
              "vs sector median")
    f2.metric("EPS Growth (YoY)", f"{eps_val:+.1f}%" if eps_val is not None else "—")
    f3.metric("Debt / Equity",    f"{de_val:.2f}" if de_val else "—",
              "Conservative" if de_val and de_val < 0.5 else ("Moderate" if de_val and de_val < 1.5 else "High"))
    f4.metric("Promoter Holding", f"{prom_val:.1f}%" if prom_val else "—")

    section("52-Week Range")
    if price and w52l and w52h and w52h != w52l:
        pos_pct = (price - w52l) / (w52h - w52l) * 100
        bar_color = "#3fb950" if pos_pct > 60 else ("#e3b341" if pos_pct > 35 else "#f85149")
        st.markdown(
            f'<div class="mp-card">'
            f'  <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem">'
            f'    <span style="font-size:0.8rem;color:#8b949e;font-weight:600">52W Low<br>'
            f'      <span style="color:#f0f6fc;font-size:0.95rem;font-feature-settings:\'tnum\'">₹{w52l:,.0f}</span>'
            f'    </span>'
            f'    <span style="font-size:0.8rem;color:#8b949e;font-weight:600;text-align:center">Current<br>'
            f'      <span style="color:#f0f6fc;font-size:0.95rem;font-weight:700;font-feature-settings:\'tnum\'">₹{price:,.2f}</span>'
            f'    </span>'
            f'    <span style="font-size:0.8rem;color:#8b949e;font-weight:600;text-align:right">52W High<br>'
            f'      <span style="color:#f0f6fc;font-size:0.95rem;font-feature-settings:\'tnum\'">₹{w52h:,.0f}</span>'
            f'    </span>'
            f'  </div>'
            f'  <div class="mp-breadth-outer">'
            f'    <div class="mp-breadth-inner" style="width:{pos_pct:.1f}%;background:{bar_color}"></div>'
            f'  </div>'
            f'  <p style="font-size:0.72rem;color:#8b949e;margin:0.4rem 0 0">Price is at {pos_pct:.1f}% of 52-week range</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — NEWS
# ════════════════════════════════════════════════════════════════════════════════
with tab_news:
    if arts:
        pos_count = sum(1 for a in arts if a.get("sentiment") == "positive")
        neg_count = sum(1 for a in arts if a.get("sentiment") == "negative")
        neu_count = len(arts) - pos_count - neg_count

        n1, n2, n3, n4 = st.columns(4)
        n1.metric("Headlines",  len(arts))
        n2.metric("Positive",   pos_count)
        n3.metric("Negative",   neg_count)
        n4.metric("Neutral",    neu_count)

        section("Recent Headlines")

        for a in arts:
            s     = a.get("sentiment", "neutral")
            dot   = "mp-dot-pos" if s == "positive" else ("mp-dot-neg" if s == "negative" else "mp-dot-neu")
            label = "Good sign" if s == "positive" else ("Bad sign" if s == "negative" else "Neutral")
            badge = (
                f'<span class="mp-news-good">{label}</span>' if s == "positive" else
                f'<span class="mp-news-bad">{label}</span>' if s == "negative" else
                f'<span class="mp-news-neu">{label}</span>'
            )
            kws   = ", ".join(a.get("matched_keywords", [])[:3])
            kw_html = f'<span style="color:#8b949e;font-size:0.68rem"> · {kws}</span>' if kws else ""
            src   = a.get("source", "")
            pub   = a.get("published_at", "")[:16].replace("T", "  ")

            st.markdown(
                f'<div class="mp-news-item">'
                f'  <div class="mp-news-dot {dot}"></div>'
                f'  <div class="mp-news-body">'
                f'    <p class="mp-news-title">{a["title"]}</p>'
                f'    <p class="mp-news-meta">{src}  ·  {pub}{kw_html}</p>'
                f'  </div>'
                f'  {badge}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Thematic Analysis
        if themes:
            section("Investment Themes")
            chips = "".join(theme_chip(t["label"], t["direction"]) for t in themes)
            st.markdown(
                f'<div class="mp-card" style="margin-bottom:0.75rem">'
                f'  <div style="margin-bottom:0.75rem">{chips}</div>',
                unsafe_allow_html=True,
            )
            for t in themes:
                d = t.get("direction", "")
                color = "#3fb950" if d == "tailwind" else ("#f85149" if d == "headwind" else "#8b949e")
                arrow = "↑" if d == "tailwind" else ("↓" if d == "headwind" else "→")
                st.markdown(
                    f'<p style="font-size:0.84rem;color:#c9d1d9;margin:0.4rem 0">'
                    f'  <span style="color:{color};font-weight:700">{arrow} {t["label"]}</span>'
                    f'  <span style="color:#8b949e"> — {t.get("reason", "")}</span>'
                    f'</p>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="mp-card" style="text-align:center;padding:2rem">'
            '<p style="color:#8b949e;font-size:0.9rem;margin:0">No recent news found for this stock.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — AI ANALYSIS
# ════════════════════════════════════════════════════════════════════════════════
with tab_ai:
    has_key = bool(_api_key())

    st.markdown(
        '<div class="mp-card" style="margin-bottom:1rem">'
        '<p class="mp-section" style="margin-top:0">About AI Analysis</p>'
        '<p style="font-size:0.85rem;color:#c9d1d9;margin:0 0 0.5rem">'
        'Claude analyses the technical signals, fundamental metrics, and the latest news '
        'headlines to produce a plain-English investment brief with outlook, key strengths, '
        'risks, and the next catalyst to watch.'
        '</p>'
        '<p style="font-size:0.75rem;color:#8b949e;margin:0">'
        'Estimated cost: <strong style="color:#e3b341">~₹0.15 per query</strong> · '
        'Claude Haiku · Not called automatically.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not has_key:
        st.markdown(
            '<div class="mp-card" style="border-color:#30363d;text-align:center;padding:1.5rem">'
            '<p style="color:#8b949e;font-size:0.875rem;margin:0">'
            'Set <code style="background:#21262d;padding:0.1rem 0.4rem;border-radius:4px;color:#58a6ff">'
            'ANTHROPIC_API_KEY</code> in <code style="background:#21262d;padding:0.1rem 0.4rem;border-radius:4px;color:#58a6ff">'
            '.env</code> to enable AI reasoning.'
            '</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        if st.button("Ask Claude  ·  ~₹0.15", type="primary", key="ask_claude_btn"):
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
            st.markdown(
                f'<div class="mp-card" style="margin-top:0.75rem">'
                f'<p class="mp-section" style="margin-top:0">Claude\'s Analysis</p>'
                f'<div style="font-size:0.875rem;color:#c9d1d9;line-height:1.7">'
                + reasoning.replace("\n", "<br>")
                + '</div></div>',
                unsafe_allow_html=True,
            )
