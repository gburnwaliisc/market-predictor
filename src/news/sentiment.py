_POSITIVE = [
    "beat", "profit", "expansion", "order win", "acquisition", "upgrade",
    "buyback", "dividend", "record", "capex", "growth", "partnership",
    "launch", "outperform", "debt free", "surge", "rally", "gains",
    "strong", "bullish", "upgraded", "revenue rise", "raises guidance",
]

_NEGATIVE = [
    "loss", "probe", "fraud", "layoff", "default", "downgrade", "penalty",
    "fine", "lawsuit", "slump", "write-off", "margin pressure", "recall",
    "resignation", "miss", "weak", "decline", "falls", "crash", "bearish",
    "npa", "warning", "cut guidance", "debt concern", "regulatory action",
]


def classify_headline(title: str) -> tuple[str, list[str]]:
    text = title.lower()
    pos = [kw for kw in _POSITIVE if kw in text]
    neg = [kw for kw in _NEGATIVE if kw in text]
    if len(pos) > len(neg):
        return "positive", pos
    if len(neg) > len(pos):
        return "negative", neg
    return "neutral", []


def classify_articles(articles: list[dict]) -> list[dict]:
    result = []
    for a in articles:
        sentiment, keywords = classify_headline(a.get("title", ""))
        result.append({**a, "sentiment": sentiment, "matched_keywords": keywords})
    return result


def news_sentiment_score(articles: list[dict]) -> float:
    if not articles:
        return 0.5
    scores = [
        1.0 if a.get("sentiment") == "positive"
        else (0.0 if a.get("sentiment") == "negative" else 0.5)
        for a in articles
    ]
    return round(sum(scores) / len(scores), 3)
