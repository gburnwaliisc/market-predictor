import yfinance as yf
import pandas as pd
import streamlit as st
import yaml

with open("config/settings.yaml") as _f:
    _cfg = yaml.safe_load(_f)

_TTL_PRICES = _cfg["cache"]["ttl_prices_seconds"]
_HISTORY_DAYS = _cfg["data"]["price_history_days"]


@st.cache_data(ttl=_TTL_PRICES, show_spinner=False)
def fetch_price_history(symbol: str) -> pd.DataFrame:
    try:
        df = yf.Ticker(symbol).history(period=f"{_HISTORY_DAYS}d")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=_TTL_PRICES, show_spinner=False)
def fetch_sensex(period: str = "1y") -> pd.DataFrame:
    try:
        df = yf.Ticker("^BSESN").history(period=period)
        return df
    except Exception:
        return pd.DataFrame()
