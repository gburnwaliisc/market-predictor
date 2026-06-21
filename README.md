# Market Predictor

Local dashboard for tracking the BSE Sensex and scoring Indian stocks for
short-term and long-term investment potential. Runs entirely on your Windows
machine — no cloud hosting, no ongoing cost.

---

## What it does

- Sensex index chart with period toggle (1D / 1W / 1M / 6M / 1Y)
- Watchlist screener table with short-term and long-term scores (0–100)
- Technical signals: RSI, MACD, Bollinger Bands, volume breakout, momentum
- Fundamental signals: PE ratio, EPS growth, debt-to-equity, promoter holding
- **Latest internet news per stock** — fetches fresh headlines from Google News
  RSS and classifies each as a **Good sign** (green) or **Bad sign** (red) for
  the investor, with a net sentiment badge in the screener table
- **Thematic flavor** — identifies which macro and sector investment themes are
  currently active for each stock (e.g. "RBI Rate Cut — Tailwind ↑",
  "Margin Pressure — Headwind ↓", "AI & Digitization — Tailwind ↑") drawn from
  an 18-theme taxonomy; a Market Themes panel on the home page shows the top
  themes across your whole watchlist
- Stock detail page with interactive price chart, signal breakdown, news feed,
  and thematic analysis panel
- Optional "Ask Claude" button for AI buy/hold/sell reasoning that incorporates
  current news and themes (~₹0.15 per click)
- Automatic daily refresh via Windows Task Scheduler

---

## Requirements

- Windows 11
- Python 3.11 or higher
- Internet connection for data and news refresh

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your watchlist

Edit `data/watchlist.json` to add/remove stocks. Use `.NS` suffix for NSE
symbols (e.g. `RELIANCE.NS`) and `.BO` for BSE symbols.

### 3. (Optional) Enable NewsAPI for richer news search

By default the dashboard fetches news from **Google News RSS** — no API key
required. For better keyword search coverage, get a free key from
newsapi.org (100 requests/day) and add it to `.env`:

```
NEWS_API_KEY=your_newsapi_key_here
```

### 4. (Optional) Enable Claude AI reasoning

```
ANTHROPIC_API_KEY=your_key_here
```

Then set `claude.enabled: true` in `config/settings.yaml`. Without this, the
"Ask Claude" button is hidden and no API costs are incurred. News headline
classification (good sign / bad sign) always uses keyword matching and is
always free — Claude is only for the on-demand narrative.

### 5. Run the dashboard

```bash
streamlit run dashboard.py
```

Opens at http://localhost:8501.

### 6. (Optional) Set up automatic daily refresh

Run once as administrator to register Task Scheduler tasks:

```bash
python scripts/setup_scheduler.py
```

This creates two tasks:
- `MarketPredictor-Open` — refreshes prices, fundamentals, and news at 08:30 IST
- `MarketPredictor-Close` — second refresh at 16:30 IST (post-market)

To remove the tasks: `schtasks /delete /tn MarketPredictor-Open /f`

---

## Manual data refresh

```bash
python scripts/refresh.py
```

Or click the "Refresh Data" button in the dashboard sidebar.

---

## How news works

On every refresh, the dashboard fetches the latest 7 headlines for each stock
from Google News RSS. Each headline is classified using keyword matching:

- **Good sign** — headline contains words like *profit*, *expansion*, *order win*,
  *acquisition*, *dividend*, *upgrade*, *record*
- **Bad sign** — headline contains words like *loss*, *fraud*, *probe*, *layoff*,
  *default*, *penalty*, *downgrade*, *write-off*
- **Neutral** — informational, no clear directional signal

No AI model or API call is used for this — it is instant and free. The net
sentiment across all 7 headlines feeds into an optional 6th feature in the
scoring model (disabled by default; enable via the sidebar weight slider).

The **Thematic Analysis** panel goes further: it identifies which of 18
predefined macro/sector themes are active based on the headlines and the
stock's sector. Each theme is tagged as a tailwind or headwind.

---

## Tuning the scores

Open the sidebar and expand "Score Weights". Six sliders control how much
each signal contributes to short-term and long-term scores (the 6th slider
is news sentiment, 0 by default). Changes save to `data/model_config.json`.

---

## Data sources

| Data | Source | Cost |
|---|---|---|
| Price history, Sensex | Yahoo Finance (`yfinance`) | Free |
| Fundamentals (PE, EPS, D/E) | Yahoo Finance `.info` + Screener.in | Free |
| Promoter holding | Screener.in | Free |
| News headlines | Google News RSS (`feedparser`) | Free, no key |
| News headlines (enhanced) | NewsAPI.org (optional) | Free with key, 100/day |
| AI reasoning | Anthropic Claude Haiku | ~₹0.15 per click |

---

## Project structure

See SPEC.md for the full product specification.
See PLAN.md for the phased build plan.
See CLAUDE.md for development conventions.

---

## Disclaimer

This tool is for personal research and informational purposes only. It does
not constitute financial advice. Past signals and news sentiment do not
guarantee future returns. Always do your own research before making investment
decisions.
