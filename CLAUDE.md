# CLAUDE.md — Market Predictor

Guidance for Claude Code working in this project.

---

## Project Purpose

Local Python dashboard for tracking BSE Sensex and scoring Indian stocks for
short-term (1–4 week) and long-term (3–12 month) investment. Also fetches
latest internet news per stock, classifies headlines as good/bad sign for
investors, and surfaces active investment themes (e.g. "RBI Rate Cut Tailwind",
"Margin Pressure Headwind"). Runs on Windows 11, zero hosting cost.

Full spec in SPEC.md. Phased build plan in PLAN.md.

---

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py

# Refresh all data (prices + fundamentals + news)
python scripts/refresh.py

# Set up Windows Task Scheduler (run as admin)
python scripts/setup_scheduler.py
```

---

## Architecture

```
dashboard.py         — Streamlit entry point, page router
config/settings.yaml — all user config (edit this, not code)
data/                — watchlist.json, model_config.json, cache/
scripts/             — standalone scripts for Task Scheduler
src/
  data/              — fetcher.py, fundamentals.py, cache.py
  signals/           — technical.py, fundamental.py
  news/              — fetcher.py, sentiment.py, themes.py, news_score.py
  model/             — scorer.py (sigmoid + dot product, 6 features)
  ai/                — claude_client.py (optional AI reasoning)
  ui/                — one file per Streamlit page + components.py
```

### Data flow

```
refresh.py / sidebar button
  → src/data/fetcher.py (yfinance)         → cache/prices/*.parquet
  → src/data/fundamentals.py               → cache/fundamentals/*.json
  → src/news/fetcher.py (Google RSS/NewsAPI) → cache/news/*.json

dashboard.py (on page load)
  → cache.py (reads cache, serves stale if needed)
  → technical.py / fundamental.py          → signals dict
  → src/news/sentiment.py                  → per-headline classification
  → src/news/themes.py                     → ThemeTag list
  → src/news/news_score.py                 → news_sentiment_score float
  → scorer.py                              → short_term_score, long_term_score
  → ui/*.py                                → Streamlit render
```

---

## Key Conventions

### Config first
All thresholds (RSI overbought level, BB window, score weights, news keywords)
live in `config/settings.yaml` or `data/model_config.json`. Never hardcode
magic numbers in source files.

### Score functions return [0.0, 1.0]
Every individual feature scorer (`rsi_score`, `pe_score`, `news_sentiment_score`,
etc.) must return a float in [0.0, 1.0]. The final score is scaled to [0, 100]
in `scorer.py`. Return 0.5 for any signal that cannot be computed (neutral).

### Cache before network
Always check cache first. If cache exists and is within TTL, return cached data.
Never make a network call when fresh cached data is available. Serve stale data
with a warning banner rather than failing.

Cache TTLs: prices 4 h, fundamentals 24 h, news 2 h.

### News sentiment is keyword-only, always free
`src/news/sentiment.py` must use only keyword matching — no API call, no ML
model, no Claude. This runs on every refresh (automatic) and must have zero
marginal cost. Claude is called only on explicit user click.

### Claude is opt-in and news-aware
The "Ask Claude" button fires only on explicit click. The prompt must include
the top 3 positive and top 3 negative headlines, plus the active theme tags,
so the reasoning reflects current news. Guard every call with
`settings.claude.enabled` and `ANTHROPIC_API_KEY` presence check.

### No database
All persistence is flat files: JSON for watchlist/config/news, Parquet for
price cache. Never introduce SQLite or any other database.

### Watchlist format
`data/watchlist.json` structure:
```json
[
  { "symbol": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy" },
  { "symbol": "TCS.NS",      "name": "Tata Consultancy Services", "sector": "IT" }
]
```
The `.NS` suffix is required for NSE symbols in yfinance and for Google News
RSS queries. BSE symbols use `.BO`.

---

## News Module Conventions

### Article structure
```python
@dataclass
class Article:
    title: str
    source: str
    published_at: str   # ISO 8601
    url: str
    sentiment: str      # "positive" | "negative" | "neutral" (filled by sentiment.py)
    matched_keywords: list[str]
```

### ThemeTag structure
```python
@dataclass
class ThemeTag:
    id: str             # e.g. "rbi_rate_cut"
    label: str          # e.g. "RBI Rate Cut"
    direction: str      # "tailwind" | "headwind"
    reason: str         # one sentence, e.g. "Lower borrowing cost benefits banking NIM"
```

### Theme taxonomy
The 18 themes and their (sector → direction) mappings are defined in
`config/settings.yaml` under `themes:`, not hardcoded in `themes.py`.
`themes.py` reads the taxonomy from config at startup.

### Google News RSS URL template
```python
RSS_URL = "https://news.google.com/rss/search?q={company}+NSE+stock&hl=en-IN&gl=IN&ceid=IN:en"
```
Use `urllib.parse.quote(company_name)` for the query. Set a 5-second timeout
on the feedparser fetch. On timeout, return cached articles if available.

### Good sign / bad sign display rules
- ≥60% of headlines positive → green thumbs-up badge ("Good sign")
- ≥60% of headlines negative → red thumbs-down badge ("Bad sign")
- Between 40–60% → grey dash badge ("Neutral")
- No headlines → grey dash badge ("No recent news")

---

## Environment Variables

Create `.env` in the project root (never commit this file):

```
ANTHROPIC_API_KEY=your_anthropic_key_here
NEWS_API_KEY=your_newsapi_key_here   # optional — RSS works without this
```

Load with `python-dotenv` at dashboard startup before any SDK import.
If `ANTHROPIC_API_KEY` is missing, hide the "Ask Claude" button silently.
If `NEWS_API_KEY` is missing, fall back to Google News RSS without warning.

---

## Adding a New Signal

1. Implement `new_signal_score(df_or_info) -> float` in the appropriate signals
   file. Must return [0.0, 1.0].
2. Add to the relevant `feature_vector_*()` in `scorer.py`.
3. Add a default weight (0.0 initially) to `config/settings.yaml`.
4. Add a slider in the sidebar weight panel.

## Adding a New Theme

1. Add a new entry to the `themes:` list in `config/settings.yaml` with:
   `id`, `label`, `keywords` (list), `tailwind_sectors` (list), `headwind_sectors` (list).
2. No code changes needed — `themes.py` reads the taxonomy dynamically.

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| `yfinance` returns empty DataFrame for delisted stocks | Check `df.empty`; return neutral scores (0.5) |
| `.info` dict keys vary by symbol | Always use `.get(key, None)` with fallback |
| Parquet write fails on Windows if file is open | Use temp file + atomic rename |
| Streamlit re-runs on every widget change | Cache expensive fetches with `@st.cache_data(ttl=3600)` |
| `ANTHROPIC_API_KEY` not loaded | Call `load_dotenv()` before `import anthropic` |
| NSE symbols need `.NS`, BSE need `.BO` | Enforce in `watchlist.py` add-stock validation |
| Google News RSS returns no results for small caps | Fall back to generic `{symbol} BSE` query |
| feedparser blocks > 5 s | Set `socket.setdefaulttimeout(5)` before each RSS fetch |
| NewsAPI returns 426 (rate limit) | Catch `HTTPError` and silently fall back to RSS |
| Theme matches too many stocks | Require ≥2 headlines to confirm a theme; single mention is noise |

---

## File Naming

- Signal scorer functions: `{name}_score` (e.g. `rsi_score`, `news_sentiment_score`)
- Cache keys: `{symbol}_{type}` (e.g. `RELIANCE.NS_prices`, `TCS.NS_news`)
- Streamlit page files: one per page (`home.py`, `screener.py`, `detail.py`, `watchlist.py`)
- Theme IDs: snake_case, matches `id` field in `config/settings.yaml`
