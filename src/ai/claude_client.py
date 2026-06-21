import os


def _api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        return ""


def ask_claude(
    symbol: str,
    name: str,
    sector: str,
    tech: dict,
    fund: dict,
    st_score: int,
    lt_score: int,
    positive_headlines: list[str],
    negative_headlines: list[str],
    themes: list[dict],
) -> str:
    api_key = _api_key()
    if not api_key:
        return "No ANTHROPIC_API_KEY configured. Add it to .env (local) or Streamlit secrets (cloud)."

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        return f"Could not initialise Anthropic client: {e}"

    theme_txt = "\n".join(
        f"- {t['label']} ({t['direction']}): {t['reason']}" for t in themes[:5]
    ) or "No strong themes detected."

    pos_txt = "\n".join(f"- {h}" for h in positive_headlines) or "None"
    neg_txt = "\n".join(f"- {h}" for h in negative_headlines) or "None"

    prompt = f"""You are a concise equity analyst specialising in Indian stocks listed on NSE/BSE.

Stock: {name} ({symbol}) | Sector: {sector}
Short-term score (1–4 weeks): {st_score}/100
Long-term score (3–12 months): {lt_score}/100

Technical signals:
- RSI (14): {tech.get('rsi_14')} | MACD: {'Bullish' if tech.get('macd_score', 0.5) > 0.5 else 'Bearish'}
- Volume ratio (5d/20d): {tech.get('volume_ratio')} | 10d momentum: {tech.get('momentum_10d')}%

Fundamental signals:
- P/E: {fund.get('pe')} | EPS growth: {fund.get('eps_growth')}% | D/E ratio: {fund.get('debt_equity')}

Positive recent headlines:
{pos_txt}

Negative recent headlines:
{neg_txt}

Active investment themes:
{theme_txt}

In 3–4 sentences give a clear buy / hold / sell view for both the short-term (1–4 weeks) and long-term (3–12 months) horizon. Cite the most important signal or news item in your reasoning. Be direct and specific."""

    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
    except Exception as e:
        return f"Claude API error: {e}"
