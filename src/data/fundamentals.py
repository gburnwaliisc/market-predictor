import yfinance as yf
import streamlit as st
import yaml

with open("config/settings.yaml") as _f:
    _cfg = yaml.safe_load(_f)

_TTL = _cfg["cache"]["ttl_fundamentals_seconds"]


@st.cache_data(ttl=_TTL, show_spinner=False)
def fetch_fundamentals(symbol: str) -> dict:
    try:
        info = yf.Ticker(symbol).info
        return {
            "pe":           info.get("trailingPE"),
            "forward_pe":   info.get("forwardPE"),
            "eps":          info.get("trailingEps"),
            "eps_forward":  info.get("forwardEps"),
            "debt_equity":  info.get("debtToEquity"),
            "market_cap":   info.get("marketCap"),
            "sector":       info.get("sector", ""),
            "industry":     info.get("industry", ""),
            "name":         info.get("longName", symbol),
            "price":        info.get("currentPrice") or info.get("regularMarketPrice"),
            "prev_close":   info.get("previousClose"),
            "day_change_pct": info.get("regularMarketChangePercent"),
            "week_52_high": info.get("fiftyTwoWeekHigh"),
            "week_52_low":  info.get("fiftyTwoWeekLow"),
            "dividend_yield": info.get("dividendYield"),
            "beta":         info.get("beta"),
        }
    except Exception:
        return {}
