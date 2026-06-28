# SPEC.md — Market Predictor
**Version:** 2.0  |  **Author:** Ghanshyam  |  **Last Updated:** 2026-06-28

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [User Personas](#2-user-personas)
3. [Scope & Boundaries](#3-scope--boundaries)
4. [Feature Catalogue](#4-feature-catalogue)
5. [User Flows](#5-user-flows)
6. [Scoring Model](#6-scoring-model)
7. [News & Thematic Intelligence](#7-news--thematic-intelligence)
8. [Advanced Analytics](#8-advanced-analytics)
9. [Alert & Notification System](#9-alert--notification-system)
10. [AI Integration](#10-ai-integration)
11. [Data Sources & Pipeline](#11-data-sources--pipeline)
12. [Configuration Reference](#12-configuration-reference)
13. [File Layout](#13-file-layout)
14. [Non-Functional Requirements](#14-non-functional-requirements)
15. [Glossary](#15-glossary)

---

## 1. Executive Summary

**Market Predictor** is a local-first, zero-hosting-cost investment intelligence
dashboard for Indian equity markets. It combines quantitative technical and
fundamental signals, real-time news sentiment, thematic macro analysis, and
optional Claude AI reasoning into a single unified interface — with the
sophistication of institutional-grade tools but the simplicity of a local Python
app.

**Core value proposition:**

| Capability | What it does |
|---|---|
| Multi-signal scoring | Blends 12 technical + fundamental + news signals into a single 0–100 score per horizon |
| Thematic intelligence | Tags each stock with active macro/sector tailwinds and headwinds from today's news |
| AI narrative | One-click Claude explanation of why a stock ranks where it does |
| Smart alerts | Windows toast notifications when scores cross thresholds or a target price is hit |
| Backtesting | Replay the scoring model on historical data to validate signal quality |
| Portfolio analytics | Portfolio-level P&L, heat map, sector concentration, and drawdown tracking |
| Macro pulse | India-specific macro dashboard: RBI rates, inflation, FII/DII flows, PMI |

Runs entirely on Windows 11 — no server, no Docker, no cloud bill.

---

## 2. User Personas

### Persona A — Active Retail Investor
- Monitors 20–50 stocks across BSE/NSE.
- Checks the dashboard at market open (09:15 IST) and after close (15:45 IST).
- Needs: screener, sentiment, score change alerts, detail view with chart overlays.

### Persona B — Long-Term Portfolio Builder
- Holds 10–15 high-conviction positions.
- Reviews weekly, cares about fundamentals and themes.
- Needs: long-term score, peer comparison, portfolio analytics, AI digest.

### Persona C — Theme-Driven Investor
- Bets on macro cycles (EV, green energy, AI, rate cuts).
- Needs: Market Themes panel, thematic heatmap, sector rotation radar.

---

## 3. Scope & Boundaries

| In Scope | Out of Scope |
|---|---|
| BSE / NSE equities and Sensex / Nifty 50 index | US / international markets |
| Local Streamlit UI (Windows 11) | Cloud hosting or multi-user deployment |
| EOD + delayed intraday price data | Real-time tick-by-tick data (<15 min) |
| Technical, fundamental, and news sentiment signals | Options / derivatives pricing |
| Short-term (1–4 week) and long-term (3–12 month) scores | Algorithmic execution or order routing |
| Keyword-based headline sentiment classification | ML / LLM-based per-headline inference |
| Claude AI on-demand narrative (pay-per-click) | Automated portfolio rebalancing |
| Backtesting on historical price + signal data | Live paper trading simulation |
| Smart Windows toast notifications | Email / SMS / push (mobile) |
| Portfolio cost basis and P&L tracking | Tax computation or FIFO lot accounting |
| India macro dashboard (rates, inflation, PMI) | Global macro data |

---

## 4. Feature Catalogue

Features are prioritised P0 (MVP), P1 (next sprint), P2 (future).

| # | Feature | Priority | Description |
|---|---|---|---|
| F-01 | Sensex / Nifty Dashboard | P0 | Live index chart with timeframe toggle and summary strip |
| F-02 | Stock Screener Table | P0 | Sortable, filterable table with scores, signals, and news badge |
| F-03 | Stock Detail Page | P0 | Chart overlays, RSI/MACD gauges, score breakdown, news feed |
| F-04 | Watchlist Manager | P0 | Add/remove stocks; edit sector tag; import from CSV |
| F-05 | Short-Term Score | P0 | 6-feature weighted sigmoid score (1–4 week horizon) |
| F-06 | Long-Term Score | P0 | 6-feature weighted sigmoid score (3–12 month horizon) |
| F-07 | News Sentiment Classification | P0 | Keyword-only per-headline classification; no API cost |
| F-08 | Market Themes Panel | P0 | Top 5 active macro/sector themes across watchlist |
| F-09 | Per-Stock Thematic Tags | P0 | Tailwind / Headwind chips on screener and detail page |
| F-10 | Ask Claude (AI Reasoning) | P0 | On-demand narrative with news context; manual trigger only |
| F-11 | Data Refresh (Manual + Scheduled) | P0 | Sidebar button + Windows Task Scheduler at 08:30 / 16:30 IST |
| F-12 | Score Alert System | P1 | Toast notification when short/long score crosses user threshold |
| F-13 | Price Alert | P1 | Toast notification when price crosses user-set target or stop |
| F-14 | Portfolio Heat Map | P1 | Grid of stocks colour-coded by score and day change |
| F-15 | Portfolio P&L Tracker | P1 | Track purchase price, quantity, unrealised P&L per position |
| F-16 | Peer Comparison | P1 | Side-by-side metrics and score breakdown for up to 4 stocks |
| F-17 | Sector Rotation Radar | P1 | Radar/spider chart of sector-average scores to spot rotation |
| F-18 | Score History Chart | P1 | Plot how a stock's short/long score evolved over the last 30 days |
| F-19 | Earnings Calendar | P1 | Upcoming Q results with estimated EPS and surprise % on announcement |
| F-20 | FII / DII Activity Panel | P1 | Net buying/selling by FII and DII from NSE bulk deal data |
| F-21 | Pattern Detection | P2 | Detect candlestick patterns (Doji, Engulfing, Hammer) on price chart |
| F-22 | Chart Pattern Recognition | P2 | Detect chart formations: Double Bottom, Head & Shoulders, Cup & Handle |
| F-23 | Backtesting Engine | P2 | Replay scoring model on historical data; report precision/recall |
| F-24 | AI Weekly Digest | P2 | Scheduled Claude-generated weekly brief on top picks and themes |
| F-25 | Export to Excel | P2 | Download screener table as `.xlsx` with formatted cells |
| F-26 | Promoter Pledge Tracker | P2 | Alert when promoter pledge % increases above threshold |
| F-27 | India Macro Pulse Panel | P2 | RBI repo rate, CPI, IIP, PMI, USD/INR displayed on home page |
| F-28 | Bulk Compare Overlay | P2 | Overlay price returns of multiple stocks on one normalised chart |
| F-29 | Watchlist CSV Import | P1 | Import stocks from a CSV file (symbol, name, sector columns) |
| F-30 | Dark / Light Mode | P1 | Toggle via sidebar; saved to `config/settings.yaml` |

---

## 5. User Flows

### 5.1 Dashboard Home (F-01, F-08, F-14, F-20, F-27)

```
┌─────────────────────────────────────────────────────────┐
│  SENSEX  79,240  ▲ +142 (+0.18%)   52W H: 85,978  L: 71,234  │
│  Nifty 50  24,012  ▲ +38            Last refresh: 09:47 IST  │
├──────────────┬──────────────────────────────────────────┤
│  Index Chart │  TIMEFRAME  1D  1W  1M  6M  1Y  3Y       │
│  (line/OHLC) │  Overlay: Volume  SMA50  SMA200           │
├──────────────┴──────────────────────────────────────────┤
│  Market Breadth  ■■■■■■■■░░  18 / 30 above 50d MA       │
├───────────────────────────┬─────────────────────────────┤
│  TOP THEMES (today)       │  FII/DII NET FLOW (₹ Cr)   │
│  🟢 RBI Rate Cut · 8 stks │  FII  -1,240   DII +2,890   │
│  🟢 PLI Scheme  · 5 stks  │  Net:  +1,650   (bullish)   │
│  🔴 Margin Pres · 6 stks  │                             │
│  🟢 EV Transit  · 4 stks  │  MACRO PULSE                │
│  🔴 NPA Concern · 3 stks  │  Repo:  6.25%  CPI: 4.8%   │
├───────────────────────────┘  USD/INR: ₹83.2  PMI: 58.4 │
│  PORTFOLIO HEAT MAP (colour = score; brightness = day%) │
│  [TCS 82] [HDFC 71] [RELIANCE 65] [INFY 78] [SBI 44]   │
└─────────────────────────────────────────────────────────┘
```

- Sensex and Nifty 50 summary strip with day change and 52-week range.
- Interactive index chart with 1D / 1W / 1M / 6M / 1Y / 3Y toggle; volume bars and SMA overlays.
- **Market Breadth bar**: fraction of watchlist stocks above their 50-day MA.
- **Top Themes panel** (F-08): top 5 macro/sector themes active today, with tailwind/headwind colour and affected stock count. Clicking a theme filters the screener.
- **FII/DII Activity strip** (F-20): net flow in ₹ crore from latest NSE bulk deal data.
- **India Macro Pulse** (F-27): key numbers in a compact card: RBI repo rate, CPI YoY, IIP, PMI, USD/INR.
- **Portfolio Heat Map** (F-14): tile grid of watchlist stocks; colour encodes score (green/amber/red), brightness encodes day change %; hover shows price and score tooltip.

### 5.2 Stock Screener (F-02, F-09, F-29, F-30)

- Full-width table of all watchlist stocks. Default sort: short-term score descending.
- Columns:

| Column | Notes |
|---|---|
| Symbol / Name | Clickable → Stock Detail page |
| Sector | Filterable |
| Price | INR, delayed or EOD |
| Day Change % | Colour-coded green/red |
| Short-Term Score | Badge: ≥70 green, 40–69 amber, <40 red |
| Long-Term Score | Same badge logic |
| Score Δ (7d) | Change in short-term score over 7 days — shows momentum of the model |
| RSI | Number + micro-gauge |
| MACD Signal | ▲ Bullish / ▼ Bearish / ─ Neutral |
| 52W Rank | Price position between 52W low and high, 0–100% |
| PE Ratio | Versus sector median shown as "+12%" or "−8%" |
| Promoter % | With Δ since last quarter |
| News Sentiment | Green / Red / Grey badge |
| Top Theme | Single most relevant theme chip |
| Alert | Bell icon if any alert set |

- **Filter bar**: sector multi-select, score range slider, sentiment filter, theme filter.
- **Column group toggles**: Technical / Fundamental / News / Scores — hide/show groups.
- **Score Δ column** is a differentiating feature — shows whether signal strength is improving or decaying.
- **Import CSV button** (F-29): upload a CSV with `symbol,name,sector` columns to bulk-add to watchlist.

### 5.3 Stock Detail Page (F-03, F-16, F-18, F-21, F-22)

```
┌─ RELIANCE INDUSTRIES (RELIANCE.NS)  ₹2,847  ▲+1.2%  ─────────┐
│  Short Score: 78 ████████░░  Long Score: 65 ██████░░░░         │
│  Sectors: Energy  |  Theme: 🟢 PLI Scheme  🔴 Margin Pressure   │
├─────────────────────────────────────────────────────────────────┤
│  PRICE CHART  [1D][1W][1M][3M][6M][1Y]  [OHLC ▾]              │
│  Overlays: SMA20 SMA50 SMA200  BB  VWAP  Fibonacci              │
│  Patterns detected: 🕯️ Bullish Engulfing (2d ago)               │
├──────────────┬──────────────────────────────────────────────────┤
│  TECHNICALS  │  FUNDAMENTALS                                    │
│  RSI 14: 42  │  PE: 24.1  (Sector: 28.3  ▼ Cheaper)           │
│  ░░░░░█░░░   │  EPS Growth (YoY): +18.4%                       │
│  MACD: ▲ Bull│  Debt / Equity: 0.41                            │
│  BB: near low│  Promoter Holding: 50.3%  (Δ +0.2% QoQ)        │
│  Volume: 1.8×│  Pledge %: 2.1%  (no change)                   │
│  Momentum:+4%│  Return on Equity: 12.8%                        │
├──────────────┴──────────────────────────────────────────────────┤
│  SCORE BREAKDOWN                                                 │
│  Short-term:  rsi ████ macd ████ bb ███ vol ████ mom ███ news ░ │
│  Long-term:   pe  ████ eps ████ d/e ███ promo ████ 52w ███ news░│
│  Score History (30d): ▁▂▄▅▅▆▇▇█ (improving trend)             │
├─────────────────────────────────────────────────────────────────┤
│  PEER COMPARISON  [vs Sector Average] [vs ONGC] [vs BPCL] [+]  │
│  Metric      RELIANCE   Sector Avg   ONGC    BPCL               │
│  ST Score       78         61          55      49               │
│  PE             24.1       28.3        8.4     12.1             │
│  EPS Growth    +18.4%     +8.1%       +3.2%   -1.1%            │
├─────────────────────────────────────────────────────────────────┤
│  NEWS FEED (last 7 headlines, 2h ago)                           │
│  🟢 Reliance Jio wins 5G spectrum ... (ET, 2h ago)              │
│  🔴 SEBI probe into related-party ... (Mint, 6h ago)            │
│  ⚪ Reliance AGM scheduled for ... (BSE filing, 1d ago)         │
│  Net sentiment: 🟢 Good sign (4 positive / 7 headlines)         │
├─────────────────────────────────────────────────────────────────┤
│  SET ALERTS    [Price ▾ 2700 ▾ below]  [Score ▾ 60 ▾ drops]   │
│  Ask Claude ▶  (~₹0.15)  [last answer: 3h ago — show cached]   │
└─────────────────────────────────────────────────────────────────┘
```

- Price chart with candlestick / OHLC / line toggle.
- Overlay selector: SMA 20 / 50 / 200, Bollinger Bands, VWAP, Fibonacci retracement levels.
- **Pattern detection badge** (F-21/F-22): if a known candlestick or chart pattern is detected, a chip is shown above the chart with the pattern name and days since signal.
- Technical panel: RSI gauge (colour zones), MACD histogram, volume bars coloured by direction, 10-day momentum.
- Fundamental panel: PE vs sector median (delta shown), EPS growth, D/E, promoter holding with QoQ delta, promoter pledge %, ROE.
- Score breakdown horizontal bars for all 6 features per horizon, showing relative contribution.
- **Score History chart** (F-18): 30-day sparkline of short-term and long-term scores — shows whether conviction is building or fading.
- **Peer Comparison table** (F-16): compares up to 4 stocks side-by-side. User can add/remove peers. Columns highlight the best value in each row.
- News Feed: 7 most recent headlines with Good/Bad/Neutral badges, source, timestamp. Summary badge at bottom.
- Thematic Analysis: all active themes for this stock with direction chip and one-line reason.
- **Alert setter** (F-12 / F-13): dropdowns to set a price alert (above/below a price) or score alert (drops below / rises above a level).
- Ask Claude button (F-10) with estimated cost; shows cached answer if available within 3 hours.

### 5.4 Sector Rotation Radar (F-17)

- Radar / spider chart with one spoke per sector (IT, Banking, Energy, FMCG, Auto, Pharma, Infra, etc.).
- Each spoke value = average short-term score of watchlist stocks in that sector.
- Two overlaid polygons: current week vs 4 weeks ago — rotation visible as shape change.
- Clicking a sector spoke filters screener to that sector.

### 5.5 Backtesting Engine (F-23)

- User selects: date range, which score (short-term / long-term), buy threshold (e.g. score > 70), hold period.
- Engine replays historical prices and recomputes signals for each day.
- Output: precision (fraction of high-score picks that outperformed Sensex), recall, Sharpe-like ratio, equity curve chart.
- Results shown in a results panel; saved to `data/backtest_results/`.

### 5.6 Watchlist Manager (F-04, F-29)

- Add stock: search by name or BSE/NSE symbol; sector tag auto-suggested from Yahoo Finance sector.
- Remove stock with one-click confirmation.
- Bulk import via CSV (F-29): drag-and-drop or file picker; validates `.NS` / `.BO` suffix.
- Reorder watchlist by drag-and-drop.
- Multiple named watchlists (e.g. "Portfolio", "Watchlist", "High Conviction") — stored as separate JSON files.

### 5.7 Portfolio P&L Tracker (F-15)

- User enters purchase price and quantity per holding.
- Dashboard shows: cost basis, current value, unrealised P&L (₹ and %), XIRR (approximate annualised return).
- Aggregate portfolio view: total invested, current value, overall return %, sector allocation pie.
- Stored in `data/portfolio.json`.

### 5.8 Earnings Calendar (F-19)

- Table of upcoming Q results for watchlist stocks within the next 30 days.
- Columns: company, expected date, estimated EPS (from Yahoo Finance consensus), previous EPS, expected YoY change.
- After announcement: actual EPS shown with surprise % and good/bad badge.
- Source: Yahoo Finance calendar data via `yfinance`.

### 5.9 AI Weekly Digest (F-24)

- Triggered via sidebar button or Windows Task Scheduler (Sunday 07:00 IST).
- Sends aggregate data to Claude: top 5 short-term picks, top 5 long-term picks, active themes, macro pulse.
- Returns a structured 400-word brief: market context, top picks with reasoning, themes to watch.
- Saved to `data/digests/YYYY-MM-DD.md`; viewable in a "Digest" tab.
- Cost estimate shown: ~₹0.40 per digest.

### 5.10 Data Refresh (F-11)

- Sidebar "Refresh Data" button with spinner. Runs prices → fundamentals → news in parallel threads.
- Task Scheduler: 08:30 IST (pre-market), 16:30 IST (post-close).
- Last-refreshed timestamps shown per data type (prices, fundamentals, news).
- Progress bar with per-stock status during manual refresh.

---

## 6. Scoring Model

### 6.1 Short-Term Score (1–4 week horizon)

Six-feature vector, all features return [0.0, 1.0]. `news_sentiment_score` weight
defaults to 0 until user enables it via sidebar slider.

| Feature | Derivation | Signal direction |
|---|---|---|
| `rsi_score` | RSI 14-day: <30 → 1.0, >70 → 0.0, else linear interpolation | Oversold = buy signal |
| `macd_score` | MACD line vs signal line: bullish crossover → 1.0, bearish → 0.0 | Momentum direction |
| `bb_score` | Price vs Bollinger Bands (20,2): near lower band → 1.0, near upper → 0.0 | Mean reversion |
| `volume_score` | 5-day volume vs 20-day avg: >1.5× → 1.0, <0.5× → 0.0 | Breakout conviction |
| `momentum_score` | 10-day price return normalised against watchlist peers (percentile rank) | Relative momentum |
| `news_sentiment_score` | Positive headline fraction minus negative, clamped [0, 1]; weight=0 by default | News flow |

```
short_term_score = round(sigmoid(dot(features, weights) + bias) × 100)
```

Default weights: `[0.2, 0.2, 0.2, 0.2, 0.2, 0.0]`

### 6.2 Long-Term Score (3–12 month horizon)

| Feature | Derivation | Signal direction |
|---|---|---|
| `pe_score` | PE vs sector median: <50% median → 1.0, >2× median → 0.0, else linear | Value |
| `eps_growth_score` | YoY EPS growth: >20% → 1.0, negative → 0.0, else linear | Earnings quality |
| `debt_score` | D/E ratio: <0.3 → 1.0, >2.0 → 0.0, else linear | Balance sheet safety |
| `promoter_score` | Promoter holding: >60% → 1.0, <30% → 0.0; adjusted down if pledge >15% | Insider alignment |
| `momentum_52w_score` | 52-week return vs Sensex return: outperformance percentile | Relative strength |
| `news_sentiment_score` | Same computation and cache as short-term | News flow |

Default weights: `[0.2, 0.2, 0.2, 0.2, 0.2, 0.0]`

### 6.3 Extended Signals (P1 — additional features that can be added to the vector)

| Signal | Derivation | Horizon |
|---|---|---|
| `roe_score` | Return on Equity: >20% → 1.0, <5% → 0.0 | Long-term |
| `revenue_growth_score` | YoY revenue growth: >15% → 1.0, negative → 0.0 | Long-term |
| `52w_high_proximity_score` | Price within 10% of 52W high → 0.0 (stretched); near 52W low → 1.0 | Short-term |
| `fii_flow_score` | Net FII buying in sector: positive → 1.0, selling → 0.0 | Short-term |
| `earnings_surprise_score` | Last quarter EPS surprise: beat >10% → 1.0, miss >10% → 0.0 | Both |

Each extended signal starts at weight 0.0. User enables via sidebar slider.

### 6.4 Score Change (Score Δ)

Every time scores are computed, they are appended to `data/cache/score_history/{symbol}.json`
with a timestamp. The screener's "Score Δ (7d)" column shows the 7-day change in short-term
score. Score history powers the Score History chart on the detail page.

### 6.5 Weights & Calibration

- All weights stored in `data/model_config.json`.
- User tunes weights via sidebar sliders; saved automatically.
- Weights auto-normalise to sum to 1 across non-zero features (shown in sidebar).
- "Reset to defaults" button restores factory weights.
- Backtesting engine (F-23) can report which weight configuration would have maximised
  precision on historical picks.

---

## 7. News & Thematic Intelligence

### 7.1 News Fetching

**Primary source (no API key):**
- Google News RSS via `feedparser` — query: `{company_name} NSE stock`
- Returns fresh headlines typically within 2–4 hours.
- RSS URL template:
  ```python
  RSS_URL = "https://news.google.com/rss/search?q={company}+NSE+stock&hl=en-IN&gl=IN&ceid=IN:en"
  ```
- Fallback query if <2 results: `{symbol} BSE` (for small-caps with low coverage).
- 5-second socket timeout per fetch; stale cache served on timeout.

**Secondary source (optional, 100 req/day free tier):**
- NewsAPI.org: set `NEWS_API_KEY` in `.env`; falls back to RSS silently if key missing.
- Catches 426 rate-limit errors and falls back gracefully.

Cache: `data/cache/news/{symbol}_news.json`, TTL 2 hours.

### 7.2 Article Data Model

```python
@dataclass
class Article:
    title: str
    source: str
    published_at: str        # ISO 8601
    url: str
    sentiment: str           # "positive" | "negative" | "neutral"
    matched_keywords: list[str]
    relevance_score: float   # 0.0–1.0: how closely the headline relates to this stock
```

### 7.3 Sentiment Classification

Entirely keyword-based. No API cost. Runs on every refresh.

1. Lowercase and tokenise the headline.
2. Negate: if `not`, `no`, `without` precedes a word within 2 tokens, flip polarity.
3. Match positive keywords: `beat`, `profit`, `expansion`, `order win`, `acquisition`,
   `upgrade`, `buyback`, `dividend`, `record`, `capex`, `growth`, `partnership`, `launch`,
   `outperform`, `debt free`, `turnaround`, `new high`, `market share`, `approval`,
   `export growth`, `strong demand`.
4. Match negative keywords: `loss`, `probe`, `fraud`, `layoff`, `default`, `downgrade`,
   `penalty`, `fine`, `lawsuit`, `slump`, `write-off`, `margin pressure`, `recall`,
   `resignation`, `miss`, `decline`, `ban`, `seizure`, `pledge`, `NPA`, `slowdown`,
   `under pressure`, `warned`.
5. Score per headline: positive > negative → 1 (Good sign), negative > positive → 0 (Bad sign), else 0.5 (Neutral).
6. `news_sentiment_score = mean(score_per_headline)` over last 7 headlines.

**Display badge rules:**

| Condition | Badge | Colour |
|---|---|---|
| ≥60% headlines positive | Good sign | Green thumbs-up |
| ≥60% headlines negative | Bad sign | Red thumbs-down |
| 40–60% mix | Neutral | Grey dash |
| 0 headlines available | No recent news | Grey dash |

### 7.4 Thematic Taxonomy

Taxonomy of 18 themes, all defined in `config/settings.yaml`. `themes.py` reads
dynamically — adding a new theme requires only a YAML edit, no code change.
A theme is tagged on a stock only if ≥2 headlines match its keywords (single mention
is noise).

| Theme ID | Label | Tailwind Sectors | Headwind Sectors |
|---|---|---|---|
| `rbi_rate_cut` | RBI Rate Cut | Banking, Realty, Auto | — |
| `rbi_rate_hike` | RBI Rate Hike | — | Banking (NIMs), Realty |
| `inr_depreciation` | INR Weakening | IT (export earners) | Oil & Gas, Aviation |
| `inr_appreciation` | INR Strengthening | Oil & Gas, Aviation | IT |
| `fii_buying` | FII Inflow | Broad market | — |
| `fii_selling` | FII Outflow | — | Broad market |
| `pli_scheme` | PLI / Govt Scheme | Manufacturing, Defence, Electronics | — |
| `ai_tech` | AI & Digitization | IT, Tech, SaaS | — |
| `ev_transition` | EV Transition | Auto EV, Battery, Charging Infra | Traditional Auto OEM |
| `green_energy` | Green / Renewables | Power, Infra, Solar | Coal, Thermal |
| `commodity_cycle` | Commodity Supercycle | Metals, Mining | Manufacturing |
| `domestic_consumption` | Domestic Consumption | FMCG, Retail, QSR | — |
| `credit_growth` | Banking Credit Growth | Banking, NBFC | — |
| `npa_concern` | NPA / Credit Risk | — | Banking, NBFC |
| `capex_expansion` | Capex Expansion | Capital Goods, Cement, Steel | — |
| `margin_pressure` | Margin Pressure | — | FMCG, Auto, Paints |
| `regulatory_risk` | Regulatory Headwinds | — | Pharma, Telecom, NBFC |
| `promoter_buying` | Promoter Buying | Company-specific | — |
| `order_book_growth` | Order Book Growth | Infra, Defence, Railway | — |
| `china_competition` | China Import Threat | — | Steel, Chemicals, Solar |

### 7.5 ThemeTag Data Model

```python
@dataclass
class ThemeTag:
    id: str             # e.g. "rbi_rate_cut"
    label: str          # e.g. "RBI Rate Cut"
    direction: str      # "tailwind" | "headwind"
    reason: str         # one sentence explaining why this stock is affected
    headline_count: int # number of supporting headlines (min 2 to show)
    confidence: float   # 0.0–1.0: fraction of theme keywords matched
```

---

## 8. Advanced Analytics

### 8.1 Portfolio Heat Map (F-14)

- Tile grid of watchlist stocks, 5 tiles per row.
- Tile colour: green (score ≥70), amber (40–69), red (<40).
- Tile brightness: proportional to absolute day-change % — brighter = bigger move.
- Tile size (optional): proportional to portfolio position size if P&L tracker enabled.
- Hover tooltip: price, day change %, short-term score, long-term score, top theme.
- Click tile → navigates to Stock Detail page.

### 8.2 Sector Rotation Radar (F-17)

- Sectors: IT, Banking, Energy, FMCG, Auto, Pharma, Infra, Metals, Realty, Telecom.
- Each spoke = average short-term score of stocks in that sector within the watchlist.
- Two overlaid polygons: current week (solid) vs 4 weeks prior (dashed) — rotation
  visible as shape deformation.
- Interpretation guide beneath chart: "Areas expanding → momentum building; contracting → cooling."

### 8.3 Score History Chart (F-18)

- Per-stock. X-axis = last 30 trading days. Y-axis = score (0–100).
- Two lines: short-term score (blue) and long-term score (orange).
- Annotations: major news events or earnings dates shown as vertical markers.
- Stored as JSON: `data/cache/score_history/{symbol}.json`.
- Computed and appended on every refresh; never overwritten.

### 8.4 Peer Comparison (F-16)

- Accessible from Stock Detail page via "+ Add Peer" button.
- Up to 4 stocks side by side.
- Rows: Current Price, Day Change %, Short Score, Long Score, RSI, PE, EPS Growth, D/E,
  Promoter %, 52W Return, News Sentiment.
- Best-in-row value highlighted with a subtle background.
- Normalised return chart: all selected stocks rebased to 100 from a user-selected start date.

### 8.5 Backtesting Engine (F-23)

- User inputs: date range (min 90 days), score type, buy threshold (default 70), hold period (default 14 days).
- Engine:
  1. For each trading day in range, recompute signals using data available at that date (point-in-time correctness).
  2. If score > threshold: mark as "buy signal".
  3. Measure return over hold period vs Sensex return.
- Metrics output:
  - Hit rate: % of buy signals that outperformed Sensex.
  - Avg alpha: avg outperformance when hit.
  - Max drawdown during holds.
  - Equity curve if ₹1 lakh deployed equally on each signal.
- Results saved to `data/backtest_results/{run_id}.json`.

### 8.6 Pattern Detection (F-21/F-22)

**Candlestick patterns** detected on the last 5 candles:

| Pattern | Signal |
|---|---|
| Doji | Indecision — watch for breakout |
| Bullish Engulfing | Reversal — strong buy signal |
| Bearish Engulfing | Reversal — sell signal |
| Hammer / Inverted Hammer | Potential bottom |
| Shooting Star | Potential top |
| Morning Star / Evening Star | 3-candle reversal |

**Chart patterns** detected over rolling 60-day window:

| Pattern | Detection method |
|---|---|
| Double Bottom | Two local minima within 3% of each other, neckline breakout |
| Double Top | Two local maxima within 3% of each other, neckline break |
| Head & Shoulders | Three peaks with middle highest, neckline drawn |
| Cup & Handle | U-shaped recovery with shallow pullback |
| Breakout above 52W high | Price closes above prior 52W high |

Pattern detection is heuristic (price-based), not ML-based. Zero cost. Shown as badges
on the detail chart and as a column (optional) in the screener.

---

## 9. Alert & Notification System

### 9.1 Alert Types

| Alert Type | Trigger | Delivery |
|---|---|---|
| Price Alert (above) | Price > user-set target | Windows toast |
| Price Alert (below) | Price < user-set stop-loss | Windows toast |
| Score Rise Alert | Short/long score rises above threshold (e.g. 70) | Windows toast |
| Score Drop Alert | Short/long score drops below threshold (e.g. 40) | Windows toast |
| Theme Alert | A new theme tag appears on a watchlist stock | Windows toast |
| Promoter Pledge Alert | Promoter pledge % increases by >5% in a quarter | Windows toast |
| Earnings Alert | Upcoming earnings within 3 days | Windows toast |

### 9.2 Delivery Mechanism

- `winotify` library for Windows 10/11 native toast notifications.
- `scripts/alert_checker.py` is registered with Task Scheduler to run at 09:00, 12:00, 16:30 IST daily.
- Alerts stored in `data/alerts.json`; each alert has an `active: true/false` flag.
- Alert history log in `data/alert_log.json`.

### 9.3 Alert Management UI

- Alerts panel accessible from Stock Detail page and sidebar.
- List of active alerts with status (pending / triggered / dismissed).
- Toggle, edit, or delete individual alerts.

---

## 10. AI Integration

### 10.1 Ask Claude (On-Demand Narrative)

- Triggered only by explicit user click on the "Ask Claude" button.
- Never called on page load, auto-refresh, or scheduled tasks (except Weekly Digest).
- Guard: button hidden if `ANTHROPIC_API_KEY` is absent or `settings.claude.enabled: false`.

**Prompt includes:**
- Stock name, sector, current price, day change.
- Short-term score with all 6 feature values and weights.
- Long-term score with all 6 feature values and weights.
- Top 3 positive and top 3 negative recent headlines (titles only).
- Active theme tags with directions and reasons.
- User's current weight configuration (so the narrative reflects their model).

**Output format (structured):**
```
OUTLOOK: Buy / Hold / Sell  (one word)
HORIZON: Short-term | Long-term | Both

KEY STRENGTHS (2–3 bullets)
KEY RISKS (1–2 bullets)

WHAT TO WATCH (1 sentence — next catalyst or risk event)
```

- Model: `claude-haiku-4-5-20251001` (fast, cheap). Max tokens: 450.
- Cache: answer stored in `data/cache/claude/{symbol}_reasoning.json` with timestamp.
- If cached answer is <3 hours old, show it with "Cached answer (Xh ago)" label without
  making a new API call.
- Cost note displayed on button: "~₹0.15/query".

### 10.2 AI Weekly Digest (F-24)

- Scheduled: Sunday 07:00 IST via Task Scheduler or via sidebar "Generate Digest" button.
- Input to Claude: top 5 short-term picks with scores and top themes, top 5 long-term picks,
  market breadth number, FII/DII net flow, macro pulse figures, top 3 macro themes.
- Output: 400-word structured brief saved as Markdown in `data/digests/YYYY-MM-DD.md`.
- Viewable in a "Digest" tab on the home page. Previous digests browsable.
- Estimated cost: ~₹0.40 per digest.
- Model: `claude-sonnet-4-6` for digest (higher quality than Haiku for long-form).

### 10.3 API Cost Controls

- Daily spend cap configurable in `settings.yaml` (`claude.daily_budget_inr`).
- Spend tracker in `data/claude_usage.json`; resets at midnight IST.
- If daily budget exceeded, "Ask Claude" button greyed out with "Daily budget reached" tooltip.

---

## 11. Data Sources & Pipeline

### 11.1 Sources

| Data Type | Source | Method | Cost |
|---|---|---|---|
| Price history (EOD, 1Y) | Yahoo Finance | `yfinance` Python lib | Free |
| Live / delayed Sensex & Nifty | Yahoo Finance (`^BSESN`, `^NSEI`) | `yfinance` | Free |
| Intraday price (delayed 15 min) | NSE India | `nselib` or direct HTTP | Free |
| Fundamentals (PE, EPS, D/E, promoter) | Yahoo Finance `.info` | `yfinance` | Free |
| Earnings calendar | Yahoo Finance | `yfinance` | Free |
| FII / DII bulk deals | NSE India bulk deal CSV | HTTP download | Free |
| News headlines (primary) | Google News RSS | `feedparser` | Free, no key |
| News headlines (enhanced) | NewsAPI.org | REST API, 100 req/day free | Free with key |
| India Macro (CPI, IIP) | RBI / MOSPI public data | HTTP + JSON parse | Free |
| USD/INR rate | Yahoo Finance (`INR=X`) | `yfinance` | Free |
| Earnings surprise (historical) | Yahoo Finance | `yfinance` | Free |
| AI narrative & digest | Anthropic Claude | REST API | Pay-per-use |

### 11.2 Data Flow

```
refresh.py / sidebar "Refresh" button
  ├── src/data/fetcher.py (yfinance)          → cache/prices/{symbol}_prices.parquet
  ├── src/data/fundamentals.py                → cache/fundamentals/{symbol}_fundamentals.json
  ├── src/data/nse_flows.py (FII/DII)         → cache/fii_dii.json
  ├── src/data/macro.py (RBI, CPI, INR)       → cache/macro.json
  ├── src/data/earnings_calendar.py           → cache/earnings_calendar.json
  └── src/news/fetcher.py (RSS / NewsAPI)     → cache/news/{symbol}_news.json

dashboard.py (on page load)
  ├── cache.py (TTL checks, serves stale with banner if needed)
  ├── technical.py / fundamental.py           → signals dict
  ├── src/news/sentiment.py                   → per-headline classification
  ├── src/news/themes.py                      → list[ThemeTag]
  ├── src/news/news_score.py                  → news_sentiment_score float
  ├── scorer.py                               → short_term_score, long_term_score
  ├── score_history.py                        → append to cache/score_history/
  ├── alert_checker.py                        → check & fire Windows toasts
  └── ui/*.py                                 → Streamlit render

scripts/alert_checker.py (Task Scheduler, 3×/day)
  └── reads scores + alerts.json → fires winotify toast if triggered

scripts/weekly_digest.py (Task Scheduler, Sunday 07:00 IST)
  └── builds prompt → calls Claude Sonnet → saves data/digests/YYYY-MM-DD.md
```

### 11.3 Cache

All fetched data cached in `data/cache/` as Parquet (prices) or JSON (all others).

| Cache type | TTL | Location |
|---|---|---|
| Price data | 4 hours | `cache/prices/{symbol}_prices.parquet` |
| Fundamentals | 24 hours | `cache/fundamentals/{symbol}_fundamentals.json` |
| News headlines | 2 hours | `cache/news/{symbol}_news.json` |
| Score history | Never expires (append-only) | `cache/score_history/{symbol}.json` |
| FII / DII flows | 4 hours | `cache/fii_dii.json` |
| Macro pulse | 12 hours | `cache/macro.json` |
| Earnings calendar | 24 hours | `cache/earnings_calendar.json` |
| Claude answers | 3 hours | `cache/claude/{symbol}_reasoning.json` |

Stale data is served with a yellow warning banner. The app never crashes on cache miss.
Parquet writes use temp file + atomic rename to prevent corruption on Windows file lock.

---

## 12. Configuration Reference

`config/settings.yaml` — all user-facing settings:

```yaml
watchlist_file: data/watchlist.json
cache_dir: data/cache/
model_config: data/model_config.json
portfolio_file: data/portfolio.json
alerts_file: data/alerts.json

data:
  price_history_days: 365
  cache_ttl_prices_hours: 4
  cache_ttl_fundamentals_hours: 24
  cache_ttl_news_hours: 2
  cache_ttl_macro_hours: 12
  fii_dii_source_url: "https://www.nseindia.com/api/bulkdeals"

news:
  enabled: true
  primary_source: google_rss      # google_rss | newsapi
  headlines_per_stock: 7
  min_headlines_for_theme: 2      # minimum headline matches to confirm a theme
  positive_threshold: 0.6         # ≥60% positive → "Good sign"
  negative_threshold: 0.4         # ≤40% positive → "Bad sign"

scoring:
  short_term:
    weights: [0.2, 0.2, 0.2, 0.2, 0.2, 0.0]   # [rsi, macd, bb, volume, momentum, news]
    bias: 0.0
  long_term:
    weights: [0.2, 0.2, 0.2, 0.2, 0.2, 0.0]   # [pe, eps_growth, debt, promoter, momentum_52w, news]
    bias: 0.0
  score_history_days_retained: 90               # purge entries older than this

claude:
  enabled: true
  model_ask: claude-haiku-4-5-20251001          # for Ask Claude button
  model_digest: claude-sonnet-4-6               # for weekly digest
  max_tokens_ask: 450
  max_tokens_digest: 1000
  daily_budget_inr: 20.0                        # hard cap; 0 = unlimited
  cache_ttl_hours: 3                            # reuse cached answer within this window

alerts:
  enabled: true
  check_times_ist: ["09:00", "12:00", "16:30"]
  default_score_drop_threshold: 40
  default_score_rise_threshold: 70

display:
  theme: light                  # light | dark
  default_chart_period: "6M"
  top_n_picks: 5
  themes_on_home: 5
  heatmap_tiles_per_row: 5
  show_peer_comparison: true
  show_score_history: true
  show_pattern_detection: true

backtesting:
  default_buy_threshold: 70
  default_hold_days: 14
  results_dir: data/backtest_results/
```

---

## 13. File Layout

```
market-predictor/
  config/
    settings.yaml               — master config (edit this, not code)
  data/
    watchlist.json              — primary watchlist
    watchlist_highconv.json     — second named watchlist (example)
    model_config.json           — user-tuned weights and bias
    portfolio.json              — position cost basis and quantity
    alerts.json                 — active alert definitions
    alert_log.json              — fired alert history
    claude_usage.json           — daily API spend tracker
    digests/
      YYYY-MM-DD.md             — AI weekly digest files
    backtest_results/
      {run_id}.json             — backtesting output
    cache/
      prices/                   — {symbol}_prices.parquet
      fundamentals/             — {symbol}_fundamentals.json
      news/                     — {symbol}_news.json
      score_history/            — {symbol}_score_history.json
      claude/                   — {symbol}_reasoning.json
      fii_dii.json
      macro.json
      earnings_calendar.json
  scripts/
    refresh.py                  — full data refresh (Task Scheduler)
    alert_checker.py            — alert evaluation and toast dispatch
    weekly_digest.py            — AI digest generator
    setup_scheduler.py          — registers all Task Scheduler tasks
  src/
    data/
      fetcher.py                — yfinance price + fundamentals
      fundamentals.py           — .info parser with .get() fallbacks
      nse_flows.py              — FII/DII bulk deal fetch
      macro.py                  — RBI rate, CPI, PMI, USD/INR
      earnings_calendar.py      — upcoming earnings from yfinance
      cache.py                  — cache read/write with TTL
    signals/
      technical.py              — rsi_score, macd_score, bb_score, volume_score, momentum_score
      fundamental.py            — pe_score, eps_growth_score, debt_score, promoter_score, roe_score
      patterns.py               — candlestick and chart pattern detection
    news/
      fetcher.py                — fetch_news(symbol, company_name) → list[Article]
      sentiment.py              — classify_headline(text) → "positive"|"negative"|"neutral"
      themes.py                 — extract_themes(articles, sector) → list[ThemeTag]
      news_score.py             — news_sentiment_score(articles) → float [0.0, 1.0]
    model/
      scorer.py                 — sigmoid, dot, score(), feature_vector_*()
      score_history.py          — append and read score history JSON
    analytics/
      backtester.py             — BacktestEngine: run(), report()
      portfolio.py              — P&L, XIRR computation
      sector_radar.py           — sector average score computation
      peer_comparison.py        — side-by-side metrics builder
    alerts/
      manager.py                — load/save/check alerts
      notifier.py               — winotify dispatch
    ai/
      claude_client.py          — Anthropic SDK wrapper, prompt builder
      digest.py                 — weekly digest prompt + formatter
    ui/
      home.py                   — Sensex, heat map, themes, macro, FII/DII
      screener.py               — sortable/filterable stock table
      detail.py                 — chart, signals, scores, news, peer compare
      watchlist.py              — add/remove/import stocks
      portfolio.py              — P&L tracker
      backtesting.py            — backtesting UI
      digest.py                 — weekly digest viewer
      components.py             — score_badge(), theme_chip(), news_badge(), alert_bell()
  dashboard.py                  — Streamlit entry point, page router
  requirements.txt
  .env.example
  runtime.txt                   — python-3.11
  SPEC.md
  PLAN.md
  CLAUDE.md
  README.md
```

---

## 14. Non-Functional Requirements

| Concern | Requirement |
|---|---|
| Startup time | Dashboard loads in <5 s on cold start (cached data) |
| Data refresh | Full refresh for 30 stocks (prices + news + fundamentals) completes in <90 s |
| News fetch | Per-stock news fetch completes in <3 s (RSS fast path) |
| Cache resilience | Stale data served with yellow banner when network unavailable; app never crashes |
| API cost discipline | Claude called only on explicit user click or scheduled digest — never on load |
| Sentiment cost | Headline classification uses keyword matching only — zero API cost |
| Alert latency | Score/price alerts checked within 15 minutes of trigger condition being met |
| Privacy | No data sent externally except to: Yahoo Finance, NSE, NewsAPI, Google RSS, Anthropic |
| Portability | Runs on Windows 11, Python 3.11+, no Docker, no admin rights for runtime |
| File safety | Parquet writes use atomic rename; JSON writes use temp file to prevent corruption |
| Pattern detection | False-positive rate for candlestick patterns <30% on backtested lookback data |
| Backtesting correctness | Point-in-time data only — no forward-looking bias; lookback price data anchored to date |

---

## 15. Glossary

| Term | Definition |
|---|---|
| **Signal** | A scalar value in [0.0, 1.0] derived from price, fundamental, or news data |
| **Score** | Weighted sigmoid combination of signals, scaled to [0, 100] |
| **Score Δ** | Change in score over a rolling 7-day window; positive means signal improving |
| **ThemeTag** | A macro or sector theme currently active on a stock, tagged tailwind or headwind |
| **Tailwind** | A macro theme that is expected to benefit the stock's sector |
| **Headwind** | A macro theme that is expected to pressure the stock's sector |
| **Good sign** | ≥60% of recent headlines are classified positive |
| **Bad sign** | ≥60% of recent headlines are classified negative |
| **EOD** | End-of-day price data (closing price, volume, OHLC) |
| **FII** | Foreign Institutional Investor — tracked via NSE bulk deal data |
| **DII** | Domestic Institutional Investor — banks, MFs, insurance companies |
| **52W Rank** | (Current Price − 52W Low) / (52W High − 52W Low) × 100; 0% = at 52W low |
| **Promoter** | Indian term for founding/controlling shareholders; high % indicates insider confidence |
| **Pledge %** | Fraction of promoter shares pledged as collateral — high pledge is a risk signal |
| **XIRR** | Extended Internal Rate of Return — annualised return accounting for irregular cash flows |
| **Alpha** | Return in excess of Sensex benchmark over the same period |
| **Hit rate** | In backtesting, fraction of buy signals that generated positive alpha |
| **Point-in-time** | Using only data that was available at a historical date — avoids look-ahead bias |
| **Toast** | Windows native notification bubble shown in the system tray area |
