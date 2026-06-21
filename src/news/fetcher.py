import socket
from urllib.parse import quote_plus

import feedparser
import streamlit as st
import yaml

with open("config/settings.yaml") as _f:
    _cfg = yaml.safe_load(_f)

_TTL = _cfg["cache"]["ttl_news_seconds"]
_N = _cfg["news"]["headlines_per_stock"]


@st.cache_data(ttl=_TTL, show_spinner=False)
def fetch_news(symbol: str, company_name: str) -> list[dict]:
    articles = _google_rss(company_name)
    if not articles:
        ticker = symbol.replace(".NS", "").replace(".BO", "")
        articles = _google_rss(ticker)
    return articles[:_N]


def _google_rss(query: str) -> list[dict]:
    url = (
        "https://news.google.com/rss/search"
        f"?q={quote_plus(query + ' stock NSE')}"
        "&hl=en-IN&gl=IN&ceid=IN:en"
    )
    try:
        socket.setdefaulttimeout(6)
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries[:12]:
            source = ""
            if hasattr(entry, "source") and isinstance(entry.source, dict):
                source = entry.source.get("title", "")
            results.append({
                "title":        entry.get("title", ""),
                "source":       source or "Google News",
                "published_at": entry.get("published", entry.get("updated", "")),
                "url":          entry.get("link", ""),
                "sentiment":    "neutral",
                "matched_keywords": [],
            })
        return results
    except Exception:
        return []
