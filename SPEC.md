# SPEC.md — Market Predictor

## 1. Purpose

A local-only Python dashboard that tracks the BSE Sensex and a configurable
watchlist of Indian stocks, computes technical, fundamental, and news-sentiment
signals, scores each stock for short-term and long-term investment potential,
surfaces active investment themes per stock, and optionally explains top picks
using Claude AI. Runs entirely on the user's machine — zero hosting cost.

---

## 2. Scope

| In scope | Out of scope |
|---|---|
| BSE / NSE stocks and Sensex | US / international markets |
| Local Streamlit UI | Cloud deployment |
| Historical + EOD price data | Real-time tick data |
| Technical + fundamental signals | Options / derivatives analysis |
| Short-term (1–4 weeks) and long-term (3–12 months) scores | Intraday trading signals |
| Latest internet news + good/bad sign classification | Paid news subscriptions |
| Thematic flavor tags per stock (tailwind / headwind) | Sentiment from social media |
| Claude AI reasoning (optional, pay-per-click) | Automated buy/sell execution |

---

## 3. User Flows

### 3.1 Dashboard Home
- Shows Sensex index chart (1D / 1W / 1M / 6M / 1Y toggle).
- Summary strip: Sensex value, day change %, 52-week high/low.
- Market breadth: number of watchlist stocks above 50-day MA.
- **Market Themes panel**: top 5 active macro/sector themes across the watchlist,
  each tagged Tailwind or Headwind with a count of affected stocks.

### 3.2 Stock Screener
- Table of all watchlist stocks with columns:
  - Symbol, Sector, Current Price, Day Change %
  - Short-Term Score (0–100), Long-Term Score (0–100)
  - RSI, MACD signal, 50-day MA trend
  - PE Ratio, Debt-to-Equity, Promoter Holding %
  - **News Sentiment** — icon badge: green thumbs-up (net positive), red
    thumbs-down (net negative), or dash (neutral / no recent news)
  - **Top Theme** — single most relevant theme tag for the stock
- Sortable by any column. Filter by sector, score range, sentiment.
- Score badge colour: ≥70 green, 40–69 amber, <40 red.

### 3.3 Stock Detail Page
- Price chart with selectable overlays: SMA 20/50/200, Bollinger Bands.
- Technical signal panel: RSI gauge, MACD histogram, volume bars.
- Fundamental panel: PE, EPS growth, debt-to-equity, promoter holding trend.
- Short-term and long-term score breakdown (feature bar chart, including news
  sentiment weight).
- **News Feed panel**: latest 7 headlines for the company, each tagged:
  - Good sign (green) — headline implies price-positive event
  - Bad sign (red) — headline implies price-negative event
  - Neutral (grey) — informational, no clear directional signal
  - Headline text, source name, and publication time shown.
- **Thematic Analysis panel**: active investment themes for this stock,
  each with direction (Tailwind ↑ / Headwind ↓) and a one-line reason.
- "Ask Claude" button — sends signals, scores, and top news to Claude Haiku,
  returns buy/hold/sell reasoning in plain English. Triggered manually, not on
  load. Cost note shown: "~₹0.15".

### 3.4 Watchlist Management
- Add / remove stocks by BSE/NSE symbol.
- Stored in `data/watchlist.json` (plain file, no database).
- Sector tag editable per stock.

### 3.5 Data Refresh
- Manual "Refresh Data" button in sidebar pulls latest prices, fundamentals,
  and news headlines.
- Automatic refresh: Windows Task Scheduler runs `scripts/refresh.py` at
  08:30 IST daily (market open) and 16:30 IST (market close).
- Last-refreshed timestamp shown in sidebar.

---

## 4. Scoring Model

### 4.1 Short-Term Score (1–4 week horizon)

Six-feature vector. `news_sentiment_score` starts with weight 0 until the user
enables it via the sidebar slider.

| Feature | Derivation |
|---|---|
| `rsi_score` | RSI 14-day: oversold (<30) → 1.0, overbought (>70) → 0.0, else linear |
| `macd_score` | MACD crossover signal: bullish → 1.0, bearish → 0.0 |
| `bb_score` | Price vs Bollinger Bands: near lower band → 1.0, near upper → 0.0 |
| `volume_score` | 5-day volume vs 20-day avg: >1.5× → 1.0 (breakout signal) |
| `momentum_score` | 10-day price return: normalised against watchlist peers |
| `news_sentiment_score` | Fraction of recent headlines classified positive minus negative, clamped [0, 1] |

`short_term_score = round(sigmoid(dot(features, weights) + bias) * 100)`

Default weights: `[0.2, 0.2, 0.2, 0.2, 0.2, 0.0]` (news disabled; user can
raise the 6th weight to incorporate sentiment).

### 4.2 Long-Term Score (3–12 month horizon)

| Feature | Derivation |
|---|---|
| `pe_score` | PE vs sector median: below median → 1.0, above 2× median → 0.0 |
| `eps_growth_score` | YoY EPS growth: >20% → 1.0, negative → 0.0 |
| `debt_score` | D/E ratio: <0.3 → 1.0, >2.0 → 0.0, else linear |
| `promoter_score` | Promoter holding: >60% → 1.0, <30% → 0.0 |
| `momentum_52w_score` | 52-week return vs Sensex: outperformance normalised |
| `news_sentiment_score` | Same as short-term (shared computation, same cache) |

Default weights: `[0.2, 0.2, 0.2, 0.2, 0.2, 0.0]`

### 4.3 Weights

Initial weights: equal (0.2 each for first 5, 0.0 for news), bias 0. User can
tune all six weights via sidebar sliders. Weights saved to
`data/model_config.json`.

---

## 5. News & Thematic Analysis

### 5.1 News Fetching

Primary source (no API key required):
- **Google News RSS** via `feedparser` — query: `{company_name} stock NSE` — returns
  fresh headlines typically within 2–4 hours.

Secondary source (optional, 100 req/day free):
- **NewsAPI.org** — set `NEWS_API_KEY` in `.env` to enable; falls back to RSS if
  key missing.

Cache: `data/cache/news/{symbol}_news.json`, TTL 2 hours.

### 5.2 Sentiment Classification

Each headline is classified without calling any external API:

1. Tokenise headline to lowercase words.
2. Match against positive keyword list: `beat`, `profit`, `expansion`, `order win`,
   `acquisition`, `upgrade`, `buyback`, `dividend`, `record`, `capex`, `growth`,
   `partnership`, `launch`, `outperform`, `debt free`.
3. Match against negative keyword list: `loss`, `probe`, `fraud`, `layoff`,
   `default`, `downgrade`, `penalty`, `fine`, `lawsuit`, `slump`, `write-off`,
   `margin pressure`, `recall`, `resignation`, `miss`.
4. If positive > negative → **Good sign** (1). If negative > positive → **Bad sign**
   (0). Else → **Neutral** (0.5).

`news_sentiment_score = mean(score_per_headline)` across last 7 headlines.

Claude Haiku is NOT used for headline classification (that runs silently on
refresh). It is only used for the on-demand "Ask Claude" narrative.

### 5.3 Thematic Taxonomy

Predefined themes. Each theme has a keyword match list for headlines and a
default direction per sector.

| Theme ID | Label | Tailwind sectors | Headwind sectors |
|---|---|---|---|
| `rbi_rate_cut` | RBI Rate Cut | Banking, Realty, Auto | — |
| `rbi_rate_hike` | RBI Rate Hike | — | Banking (NIMs), Realty |
| `inr_depreciation` | INR Weakening | IT (export earners) | Oil & Gas (importers) |
| `fii_buying` | FII Inflow | Broad market | — |
| `fii_selling` | FII Outflow | — | Broad market |
| `pli_scheme` | PLI / Govt Scheme | Manufacturing, Defence | — |
| `ai_tech` | AI & Digitization | IT, Tech | — |
| `ev_transition` | EV Transition | Auto, Battery | Traditional Auto OEM |
| `green_energy` | Green / Renewables | Power, Infra | Coal |
| `commodity_cycle` | Commodity Supercycle | Metals, Mining | Manufacturing |
| `domestic_consumption` | Domestic Consumption | FMCG, Retail | — |
| `credit_growth` | Banking Credit Growth | Banking, NBFC | — |
| `npa_concern` | NPA / Credit Risk | — | Banking, NBFC |
| `capex_expansion` | Capex Expansion | Capital Goods, Cement | — |
| `margin_pressure` | Margin Pressure | — | FMCG, Auto |
| `regulatory_risk` | Regulatory Headwinds | — | Pharma, Telecom |
| `promoter_buying` | Promoter Buying | Company-specific | — |
| `order_book_growth` | Order Book Growth | Infra, Defence | — |

Each theme is tagged per-stock based on:
a. Keywords found in recent headlines.
b. Whether the stock's sector is a tailwind or headwind sector for that theme.

---

## 6. Data Sources

| Data type | Source | Method | Cost |
|---|---|---|---|
| Price history + EOD | Yahoo Finance | `yfinance` Python lib | Free |
| Live Sensex | Yahoo Finance (`^BSESN`) | `yfinance` | Free |
| NSE live quotes | NSE India | `nselib` or direct HTTP | Free |
| Fundamentals (PE, EPS, D/E) | Yahoo Finance `.info` + Screener.in | Parse / scrape | Free |
| News headlines | Google News RSS | `feedparser` | Free, no key |
| News headlines (enhanced) | NewsAPI.org | REST API, 100 req/day | Free with key |
| AI reasoning | Anthropic Claude Haiku | REST API, pay-per-use | ~₹0.15/query |

All fetched data cached in `data/cache/` as Parquet / JSON files.

| Cache type | TTL |
|---|---|
| Price data | 4 hours |
| Fundamentals | 24 hours |
| News headlines | 2 hours |

---

## 7. Configuration

All user-facing config in `config/settings.yaml`:

```yaml
watchlist_file: data/watchlist.json
cache_dir: data/cache/
model_config: data/model_config.json

data:
  price_history_days: 365
  cache_ttl_prices_hours: 4
  cache_ttl_fundamentals_hours: 24
  cache_ttl_news_hours: 2

news:
  enabled: true
  primary_source: google_rss   # google_rss | newsapi
  headlines_per_stock: 7
  positive_threshold: 0.6      # net positive fraction for "Good sign" badge
  negative_threshold: 0.4      # net negative fraction for "Bad sign" badge

scoring:
  short_term:
    weights: [0.2, 0.2, 0.2, 0.2, 0.2, 0.0]   # 6th = news_sentiment
    bias: 0.0
  long_term:
    weights: [0.2, 0.2, 0.2, 0.2, 0.2, 0.0]
    bias: 0.0

claude:
  enabled: true          # set false to disable AI tab entirely
  model: claude-haiku-4-5-20251001
  max_tokens: 400        # slightly more to include news context

display:
  default_period: "6M"   # chart default
  top_n_picks: 5         # stocks shown in "Top Picks" summary
  themes_on_home: 5      # top N themes shown in Market Themes panel
```

---

## 8. File Layout

```
market-predictor/
  config/
    settings.yaml          — master config
  data/
    watchlist.json         — user's stock watchlist
    model_config.json      — tuned weights/bias
    cache/
      prices/              — {symbol}_prices.parquet
      fundamentals/        — {symbol}_fundamentals.json
      news/                — {symbol}_news.json
  scripts/
    refresh.py             — standalone data refresh (run by Task Scheduler)
    setup_scheduler.py     — registers Task Scheduler tasks
  src/
    data/
      fetcher.py           — yfinance + NSE fetch functions
      fundamentals.py      — Screener.in / yfinance.info parser
      cache.py             — cache read/write with TTL
    signals/
      technical.py         — RSI, MACD, Bollinger, volume, momentum
      fundamental.py       — PE score, EPS growth, D/E, promoter
    news/
      fetcher.py           — fetch_news(symbol, company_name) → list[Article]
      sentiment.py         — classify_headline(text) → "positive"|"negative"|"neutral"
      themes.py            — extract_themes(articles, sector) → list[ThemeTag]
      news_score.py        — news_sentiment_score(articles) → float [0.0, 1.0]
    model/
      scorer.py            — sigmoid, dot, score(), feature_vector()
    ai/
      claude_client.py     — Anthropic SDK wrapper, prompt builder
    ui/
      home.py              — Streamlit home page + Market Themes panel
      screener.py          — Streamlit screener table
      detail.py            — Streamlit stock detail + News Feed + Thematic Analysis
      watchlist.py         — Streamlit watchlist manager
      components.py        — shared score_badge(), theme_chip(), news_badge()
  dashboard.py             — Streamlit entry point
  requirements.txt
  .env.example
  SPEC.md
  PLAN.md
  CLAUDE.md
  README.md
```

---

## 9. Non-Functional Requirements

| Concern | Requirement |
|---|---|
| Startup time | Dashboard loads in < 5 s on cold start |
| Data refresh | Full watchlist refresh (30 stocks, prices + news) completes in < 90 s |
| News fetch | Per-stock news fetch completes in < 3 s (RSS is fast) |
| Cache | Stale data served when network unavailable; banner shown |
| API cost | Claude called only on explicit user click, never on page load or refresh |
| Sentiment | Headline classification uses keyword matching only — no API calls |
| Privacy | No data sent to any server except yfinance/NSE/Screener/NewsAPI/Anthropic |
| Portability | Runs on Windows 11 with Python 3.11+, no Docker required |
