import pandas as pd
import numpy as np


def compute_technical(df: pd.DataFrame) -> dict:
    if df is None or df.empty or len(df) < 26:
        return _neutral()

    close = df["Close"].dropna().astype(float)
    volume = df["Volume"].dropna().astype(float)

    signals = {}

    # RSI (14)
    rsi = _rsi(close, 14)
    signals["rsi_14"] = round(rsi, 1)
    if rsi < 30:
        signals["rsi_score"] = 1.0
    elif rsi > 70:
        signals["rsi_score"] = 0.0
    else:
        signals["rsi_score"] = round(1.0 - (rsi - 30) / 40.0, 3)

    # MACD (12, 26, 9)
    macd_line, signal_line = _macd(close)
    signals["macd_line"] = round(macd_line, 4)
    signals["macd_signal_line"] = round(signal_line, 4)
    signals["macd_score"] = 1.0 if macd_line > signal_line else 0.0

    # Bollinger Bands (20, 2)
    bb_upper, bb_lower = _bollinger(close)
    price = float(close.iloc[-1])
    bb_range = bb_upper - bb_lower
    if bb_range > 0:
        bb_score = 1.0 - (price - bb_lower) / bb_range
    else:
        bb_score = 0.5
    signals["bb_upper"] = round(bb_upper, 2)
    signals["bb_lower"] = round(bb_lower, 2)
    signals["bb_score"] = round(max(0.0, min(1.0, bb_score)), 3)

    # Volume (5d vs 20d average)
    vol_5 = float(volume.iloc[-5:].mean()) if len(volume) >= 5 else float(volume.mean())
    vol_20 = float(volume.iloc[-20:].mean()) if len(volume) >= 20 else float(volume.mean())
    ratio = vol_5 / vol_20 if vol_20 > 0 else 1.0
    signals["volume_ratio"] = round(ratio, 2)
    signals["volume_score"] = round(max(0.0, min(1.0, (ratio - 0.5) / 1.0)), 3)

    # Momentum (10-day return)
    if len(close) >= 11:
        mom = float((close.iloc[-1] / close.iloc[-11]) - 1)
    else:
        mom = 0.0
    signals["momentum_10d"] = round(mom * 100, 2)
    # +10% → 1.0, -10% → 0.0
    signals["momentum_score"] = round(max(0.0, min(1.0, (mom + 0.10) / 0.20)), 3)

    return signals


def _rsi(close: pd.Series, period: int) -> float:
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    val = rsi.dropna()
    return float(val.iloc[-1]) if not val.empty else 50.0


def _macd(close: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal, adjust=False).mean()
    return float(macd.iloc[-1]), float(sig.iloc[-1])


def _bollinger(close: pd.Series, period=20, std=2):
    sma = close.rolling(period).mean()
    sigma = close.rolling(period).std()
    return float((sma + std * sigma).iloc[-1]), float((sma - std * sigma).iloc[-1])


def _neutral() -> dict:
    return {
        "rsi_14": 50.0, "rsi_score": 0.5,
        "macd_line": 0.0, "macd_signal_line": 0.0, "macd_score": 0.5,
        "bb_upper": 0.0, "bb_lower": 0.0, "bb_score": 0.5,
        "volume_ratio": 1.0, "volume_score": 0.5,
        "momentum_10d": 0.0, "momentum_score": 0.5,
    }
