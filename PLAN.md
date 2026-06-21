# PLAN.md — Market Predictor

## Overview

Eight phases, each self-contained and runnable. Complete each phase before
starting the next — each builds on the previous.

---

## Phase 1 — Project Scaffold (Day 1)

**Goal:** Runnable skeleton with no real data yet.

Tasks:
- [ ] Create folder structure as described in SPEC.md §8
- [ ] `requirements.txt` with pinned versions
- [ ] `config/settings.yaml` with defaults
- [ ] `data/watchlist.json` with 5 seed stocks (RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ITC.NS)
- [ ] `dashboard.py` — Streamlit skeleton with five pages: Home, Screener, Detail, Watchlist, Themes
- [ ] Confirm `streamlit run dashboard.py` opens at localhost:8501 without errors

Deliverables: empty dashboard with navigation sidebar, no real data.

---

## Phase 2 — Price & Fundamental Data Layer (Days 2–3)

**Goal:** Fetch and cache price + fundamental data for the watchlist.

Tasks:
- [ ] `src/data/fetcher.py` — `fetch_price_history(symbol, days)` using `yfinance`
- [ ] `src/data/fetcher.py` — `fetch_sensex(period)` using `^BSESN` ticker
- [ ] `src/data/cache.py` — `get_cached(key, ttl_hours)` / `save_cache(key, data)` using Parquet
- [ ] `src/data/fundamentals.py` — `fetch_fundamentals(symbol)` parsing yfinance `.info`
  dict (PE, EPS, D/E, promoter holding); fall back to Screener.in scrape if key missing
- [ ] `scripts/refresh.py` skeleton — refreshes prices + fundamentals; news added in Phase 4
- [ ] Smoke test: run `python scripts/refresh.py` for 5 seed stocks without error

Deliverables: `data/cache/prices/` and `data/cache/fundamentals/` populated;
Home page shows real Sensex chart.

---

## Phase 3 — Signals Engine (Days 4–5)

**Goal:** Compute all technical and fundamental signal scores.

Tasks:
- [ ] `src/signals/technical.py` — `compute_technical(df)` returning dict with:
  - `rsi_14`, `rsi_score`
  - `macd_line`, `macd_signal`, `macd_score`
  - `bb_upper`, `bb_lower`, `bb_score`
  - `volume_ratio`, `volume_score`
  - `momentum_10d`, `momentum_score`
- [ ] `src/signals/fundamental.py` — `compute_fundamental(info)` returning:
  - `pe`, `pe_score`
  - `eps_growth`, `eps_growth_score`
  - `debt_equity`, `debt_score`
  - `promoter_holding`, `promoter_score`
  - `return_52w`, `momentum_52w_score`
- [ ] All score functions return float in [0.0, 1.0]
- [ ] Manual validation: run signals for RELIANCE.NS, inspect values

Deliverables: signal dict for each watchlist stock computed and cached.

---

## Phase 4 — News & Thematic Engine (Days 6–7)

**Goal:** Fetch latest internet news per stock, classify each headline as good/bad
for investors, extract active investment themes, and compute a `news_sentiment_score`.

Tasks:
- [ ] `src/news/fetcher.py` — `fetch_news(symbol, company_name) -> list[Article]`
  - Primary: Google News RSS (`https://news.google.com/rss/search?q={company}+NSE+stock`)
    via `feedparser`; no API key, free
  - Secondary: NewsAPI.org if `NEWS_API_KEY` set in `.env`; falls back to RSS
  - Each `Article`: `{ title, source, published_at, url }`
  - Cache result to `data/cache/news/{symbol}_news.json`, TTL 2 hours
- [ ] `src/news/sentiment.py` — `classify_headline(text) -> "positive"|"negative"|"neutral"`
  - Pure keyword matching (no API calls, always free, runs on every refresh)
  - Positive keywords: beat, profit, expansion, order win, acquisition, upgrade,
    buyback, dividend, record, capex, growth, partnership, launch, outperform, debt free
  - Negative keywords: loss, probe, fraud, layoff, default, downgrade, penalty,
    fine, lawsuit, slump, write-off, margin pressure, recall, resignation, miss
  - Returns classification + keyword(s) matched
- [ ] `src/news/themes.py` — `extract_themes(articles, sector) -> list[ThemeTag]`
  - `ThemeTag`: `{ id, label, direction: "tailwind"|"headwind", reason }`
  - Match each article against 18-theme taxonomy from SPEC.md §5.3
  - Direction is determined by (theme, sector) mapping in taxonomy table
  - Deduplicate: if same theme seen in 2+ articles, merge into one tag
- [ ] `src/news/news_score.py` — `news_sentiment_score(articles) -> float`
  - `mean(score_per_headline)` where good sign → 1.0, bad sign → 0.0, neutral → 0.5
  - Returns 0.5 if `articles` is empty (neutral; do not penalise no-news stocks)
- [ ] Update `scripts/refresh.py` to also call `fetch_news()` for each watchlist stock
- [ ] Smoke test: run refresh, inspect `data/cache/news/TCS.NS_news.json` for 7 articles

Deliverables:
- `data/cache/news/` populated
- `news_sentiment_score` available for scorer
- `ThemeTag` list available for UI

---

## Phase 5 — Scoring Model (Day 8)

**Goal:** Turn all six signal scores into short-term and long-term scores.

Tasks:
- [ ] `src/model/scorer.py` — `sigmoid(x)`, `feature_vector_short(signals)`,
  `feature_vector_long(signals)`, `score(features, weights, bias) -> int`
  - Both feature vectors include `news_sentiment_score` as 6th element
- [ ] `src/model/scorer.py` — `load_config()` reads weights/bias from
  `data/model_config.json`; falls back to `[0.2, 0.2, 0.2, 0.2, 0.2, 0.0]` if missing
- [ ] `src/model/scorer.py` — `score_all(watchlist) -> list[StockScore]`
- [ ] Sidebar slider panel with 6 sliders (one per feature); writes to config on change
- [ ] Screener table shows both scores with colour badges + news sentiment icon

Deliverables: Screener page fully functional with all signals and news badge.

---

## Phase 6 — UI Polish + Detail Page (Days 9–10)

**Goal:** Full detail page, news feed panel, thematic analysis, and polished home.

Tasks:
- [ ] `src/ui/home.py` — Sensex chart, summary strip, market breadth counter,
  **Market Themes panel** (top 5 themes across watchlist, tailwind/headwind count)
- [ ] `src/ui/detail.py` — price chart with overlays, signal panels, score breakdown,
  **News Feed panel** (7 headlines, each with good/bad/neutral badge, source, time),
  **Thematic Analysis panel** (theme chips with ↑↓ direction and one-line reason)
- [ ] `src/ui/screener.py` — news sentiment badge column, top-theme column
- [ ] `src/ui/watchlist.py` — add/remove stocks, edit sector, persist to JSON
- [ ] `src/ui/components.py` — `score_badge()`, `news_badge()`, `theme_chip()`,
  `metric_card()`, `stale_data_banner()`
- [ ] Stale data banner + last-refreshed timestamp in sidebar footer

Deliverables: All pages complete and usable end-to-end.

---

## Phase 7 — Claude AI Integration (Day 11)

**Goal:** Optional "Ask Claude" reasoning on the detail page, now augmented with
news and themes context.

Tasks:
- [ ] `src/ai/claude_client.py` — `ask_claude(symbol, signals, scores, fundamentals,
  top_headlines, themes) -> str`
  - Prompt includes: stock name, key signals, short/long scores, top 3 positive/negative
    headlines, active theme tags
  - Ask: buy/hold/sell recommendation with 2–3 sentence reasoning referencing news
- [ ] Button in detail page: "Ask Claude (costs ~₹0.15)"
- [ ] Response shown in expander below Thematic Analysis panel
- [ ] If `ANTHROPIC_API_KEY` not set or `claude.enabled: false`, hide button gracefully
- [ ] `.env.example` with `ANTHROPIC_API_KEY` and `NEWS_API_KEY` placeholders

Deliverables: Claude reasoning incorporates live news context; cost note visible.

---

## Phase 8 — Task Scheduler Setup (Day 12)

**Goal:** Automated daily refresh on Windows without user action.

Tasks:
- [ ] `scripts/setup_scheduler.py` — creates two Windows Task Scheduler tasks:
  - `MarketPredictor-Open` — runs `refresh.py` daily at 08:30 IST
  - `MarketPredictor-Close` — runs `refresh.py` daily at 16:30 IST
- [ ] `scripts/refresh.py` — writes `data/last_refresh.txt` with ISO timestamp after run
- [ ] Dashboard reads `last_refresh.txt`, shows "Last refreshed: X min ago" in sidebar
- [ ] README section: how to run `setup_scheduler.py` and verify in Task Scheduler UI

Deliverables: Refresh runs automatically; news + prices + fundamentals all updated.

---

## Dependencies (requirements.txt)

```
streamlit>=1.35
yfinance>=0.2
pandas>=2.0
numpy>=1.26
pandas-ta>=0.3
plotly>=5.22
requests>=2.31
beautifulsoup4>=4.12
feedparser>=6.0         # Google News RSS parsing
newsapi-python>=0.2.7   # NewsAPI.org optional secondary source
anthropic>=0.28
python-dotenv>=1.0
pyarrow>=16.0           # Parquet cache
pyyaml>=6.0
```

---

## Key Decisions

| Decision | Choice | Reason |
|---|---|---|
| UI framework | Streamlit | Fastest local dashboard, no JS required |
| Price data | yfinance | Free, no API key, reliable for BSE/NSE |
| Fundamentals | yfinance `.info` + Screener.in fallback | `.info` covers PE/EPS; Screener for promoter holding |
| News primary | Google News RSS via feedparser | No API key, no rate limit, always fresh |
| News secondary | NewsAPI.org (optional) | Better keyword search; 100 req/day free |
| Sentiment | Keyword matching (no ML, no API) | Zero cost, fast, explainable, runs on every refresh |
| Claude role | On-demand narrative only, not classification | Keeps AI cost to user-triggered clicks only |
| Theme taxonomy | 18 predefined themes, keyword-matched | Interpretable; no training data needed |
| Cache format | Parquet for prices, JSON for news/fundamentals | Compact + pandas-native for prices; JSON readable for inspection |
| Chart library | Plotly (via `st.plotly_chart`) | Interactive zoom/pan, candlestick support |
| Scheduling | Windows Task Scheduler via schtasks | No third-party daemon, built into Windows 11 |
