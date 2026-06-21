import math
import json
import yaml
from pathlib import Path

with open("config/settings.yaml") as _f:
    _DEFAULT = yaml.safe_load(_f)["scoring"]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-500.0, min(500.0, x))))


def load_config() -> dict:
    p = Path("data/model_config.json")
    if p.exists():
        try:
            with open(p) as f:
                return json.load(f)
        except Exception:
            pass
    return _DEFAULT


def feature_vector_short(tech: dict, news_score: float) -> list[float]:
    return [
        float(tech.get("rsi_score", 0.5)),
        float(tech.get("macd_score", 0.5)),
        float(tech.get("bb_score", 0.5)),
        float(tech.get("volume_score", 0.5)),
        float(tech.get("momentum_score", 0.5)),
        float(news_score),
    ]


def feature_vector_long(fund: dict, news_score: float) -> list[float]:
    return [
        float(fund.get("pe_score", 0.5)),
        float(fund.get("eps_growth_score", 0.5)),
        float(fund.get("debt_score", 0.5)),
        float(fund.get("promoter_score", 0.5)),
        float(fund.get("momentum_52w_score", 0.5)),
        float(news_score),
    ]


def score(features: list[float], weights: list[float], bias: float = 0.0) -> int:
    dot = sum(f * w for f, w in zip(features, weights))
    return round(sigmoid(dot + bias) * 100)
