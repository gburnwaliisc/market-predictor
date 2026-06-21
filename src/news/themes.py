_THEMES = [
    {
        "id": "rbi_rate_cut",
        "label": "RBI Rate Cut",
        "keywords": ["rate cut", "repo rate cut", "rbi cuts", "monetary easing", "rate reduction"],
        "tailwind": ["Banking", "Realty", "Auto", "NBFC"],
        "headwind": [],
    },
    {
        "id": "rbi_rate_hike",
        "label": "RBI Rate Hike",
        "keywords": ["rate hike", "repo rate hike", "rbi raises", "rate increase", "monetary tightening"],
        "tailwind": [],
        "headwind": ["Banking", "Realty", "Auto", "NBFC"],
    },
    {
        "id": "inr_depreciation",
        "label": "INR Weakening",
        "keywords": ["rupee falls", "inr weakens", "rupee depreciation", "dollar gains", "currency pressure"],
        "tailwind": ["IT"],
        "headwind": ["Energy", "Oil & Gas"],
    },
    {
        "id": "fii_buying",
        "label": "FII Inflow",
        "keywords": ["fii buying", "foreign inflow", "fpi inflow", "foreign investors buy", "overseas buying"],
        "tailwind": ["Banking", "IT", "Energy", "FMCG"],
        "headwind": [],
    },
    {
        "id": "fii_selling",
        "label": "FII Outflow",
        "keywords": ["fii selling", "foreign outflow", "fpi outflow", "foreign investors sell"],
        "tailwind": [],
        "headwind": ["Banking", "IT", "Energy", "FMCG"],
    },
    {
        "id": "pli_scheme",
        "label": "PLI / Govt Scheme",
        "keywords": ["pli scheme", "production linked", "government incentive", "make in india", "govt subsidy"],
        "tailwind": ["Manufacturing", "Defence", "Pharma", "Auto"],
        "headwind": [],
    },
    {
        "id": "ai_tech",
        "label": "AI & Digitization",
        "keywords": ["artificial intelligence", "ai deal", "digital transformation", "cloud deal", "generative ai", "ai contract"],
        "tailwind": ["IT"],
        "headwind": [],
    },
    {
        "id": "ev_transition",
        "label": "EV Transition",
        "keywords": ["electric vehicle", "ev launch", "ev sales", "battery", "ev adoption"],
        "tailwind": ["Auto"],
        "headwind": [],
    },
    {
        "id": "commodity_cycle",
        "label": "Commodity Supercycle",
        "keywords": ["commodity rally", "steel prices", "metal prices", "copper surge", "iron ore rise"],
        "tailwind": ["Metals", "Mining"],
        "headwind": ["Manufacturing", "Auto"],
    },
    {
        "id": "domestic_consumption",
        "label": "Domestic Consumption",
        "keywords": ["consumption boost", "rural demand", "urban spending", "fmcg growth", "retail sales rise"],
        "tailwind": ["FMCG", "Retail", "Auto"],
        "headwind": [],
    },
    {
        "id": "credit_growth",
        "label": "Banking Credit Growth",
        "keywords": ["credit growth", "loan growth", "banking credit", "retail loans", "msme credit"],
        "tailwind": ["Banking", "NBFC"],
        "headwind": [],
    },
    {
        "id": "npa_concern",
        "label": "NPA / Credit Risk",
        "keywords": ["npa rises", "bad loans", "stressed assets", "credit default", "loan npa"],
        "tailwind": [],
        "headwind": ["Banking", "NBFC"],
    },
    {
        "id": "margin_pressure",
        "label": "Margin Pressure",
        "keywords": ["margin pressure", "margin decline", "cost pressure", "input cost rise", "profitability hit"],
        "tailwind": [],
        "headwind": ["FMCG", "Auto", "Manufacturing"],
    },
    {
        "id": "regulatory_risk",
        "label": "Regulatory Headwinds",
        "keywords": ["sebi notice", "regulatory action", "penalty imposed", "cci probe", "compliance issue"],
        "tailwind": [],
        "headwind": ["Pharma", "Telecom", "Banking"],
    },
    {
        "id": "order_book_growth",
        "label": "Order Book Growth",
        "keywords": ["order win", "new orders", "contract win", "order book", "wins contract"],
        "tailwind": ["Capital Goods", "Defence", "IT"],
        "headwind": [],
    },
    {
        "id": "capex_expansion",
        "label": "Capex Expansion",
        "keywords": ["capex", "capacity expansion", "new plant", "greenfield project", "investment plan"],
        "tailwind": ["Capital Goods", "Cement", "Energy"],
        "headwind": [],
    },
    {
        "id": "green_energy",
        "label": "Green / Renewables",
        "keywords": ["renewable energy", "solar project", "green energy", "wind power", "clean energy"],
        "tailwind": ["Energy"],
        "headwind": [],
    },
    {
        "id": "promoter_activity",
        "label": "Promoter Activity",
        "keywords": ["promoter buying", "insider buying", "promoter stake", "promoter increases"],
        "tailwind": ["Banking", "IT", "Energy", "FMCG", "Auto"],
        "headwind": [],
    },
]


def extract_themes(articles: list[dict], sector: str) -> list[dict]:
    hit_count: dict[str, int] = {}
    for a in articles:
        text = a.get("title", "").lower()
        for theme in _THEMES:
            if any(kw in text for kw in theme["keywords"]):
                hit_count[theme["id"]] = hit_count.get(theme["id"], 0) + 1

    result = []
    for theme in _THEMES:
        if hit_count.get(theme["id"], 0) < 1:
            continue
        if sector in theme["tailwind"]:
            direction, reason = "tailwind", f"{theme['label']} is positive for {sector} stocks"
        elif sector in theme["headwind"]:
            direction, reason = "headwind", f"{theme['label']} is a risk for {sector} stocks"
        else:
            direction, reason = "neutral", f"{theme['label']} active — monitor impact on {sector}"
        result.append({
            "id":        theme["id"],
            "label":     theme["label"],
            "direction": direction,
            "reason":    reason,
            "hits":      hit_count[theme["id"]],
        })

    order = {"tailwind": 0, "headwind": 1, "neutral": 2}
    result.sort(key=lambda x: (order[x["direction"]], -x["hits"]))
    return result
