def compute_fundamental(info: dict) -> dict:
    signals = {}

    # P/E score vs broad market median (~25)
    pe = info.get("pe")
    if pe and pe > 0:
        median = 25.0
        if pe < median:
            pe_score = 1.0
        elif pe > 2 * median:
            pe_score = 0.0
        else:
            pe_score = 1.0 - (pe - median) / median
        signals["pe"] = round(pe, 1)
        signals["pe_score"] = round(max(0.0, min(1.0, pe_score)), 3)
    else:
        signals["pe"] = None
        signals["pe_score"] = 0.5

    # EPS growth (trailing → forward)
    eps = info.get("eps")
    eps_fwd = info.get("eps_forward")
    if eps and eps_fwd and abs(eps) > 0.001:
        growth = (eps_fwd - eps) / abs(eps)
        signals["eps_growth"] = round(growth * 100, 1)
        if growth > 0.20:
            signals["eps_growth_score"] = 1.0
        elif growth < 0:
            signals["eps_growth_score"] = 0.0
        else:
            signals["eps_growth_score"] = round(growth / 0.20, 3)
    else:
        signals["eps_growth"] = None
        signals["eps_growth_score"] = 0.5

    # Debt / Equity (yfinance returns as percentage, e.g. 50 means D/E 0.5)
    de = info.get("debt_equity")
    if de is not None and de >= 0:
        de_ratio = de / 100.0
        if de_ratio < 0.3:
            de_score = 1.0
        elif de_ratio > 2.0:
            de_score = 0.0
        else:
            de_score = 1.0 - (de_ratio - 0.3) / 1.7
        signals["debt_equity"] = round(de_ratio, 2)
        signals["debt_score"] = round(max(0.0, min(1.0, de_score)), 3)
    else:
        signals["debt_equity"] = None
        signals["debt_score"] = 0.5

    # Promoter holding — not available via yfinance; default neutral
    signals["promoter_holding"] = None
    signals["promoter_score"] = 0.5

    # 52-week momentum vs Sensex — approximated; computed neutral for now
    signals["momentum_52w_score"] = 0.5

    return signals
