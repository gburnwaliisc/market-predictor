import json

import streamlit as st

from src.ui.styles import page_header, section


def _load():
    with open("data/watchlist.json") as f:
        return json.load(f)


if "watchlist" not in st.session_state:
    st.session_state["watchlist"] = _load()

wl = st.session_state["watchlist"]

# ── Page header ───────────────────────────────────────────────────────────────
page_header("Watchlist Manager", "Add, remove, or reorder your tracked stocks")

# ── Stats strip ───────────────────────────────────────────────────────────────
sectors = {}
for s in wl:
    sec = s.get("sector", "Other")
    sectors[sec] = sectors.get(sec, 0) + 1

top_sector = max(sectors, key=sectors.get) if sectors else "—"

s1, s2, s3 = st.columns(3)
s1.metric("Total Stocks", len(wl))
s2.metric("Sectors Covered", len(sectors))
s3.metric("Largest Sector", top_sector, f"{sectors.get(top_sector, 0)} stocks")

# ── Current watchlist ─────────────────────────────────────────────────────────
section(f"Current Watchlist  ·  {len(wl)} stocks")

to_remove = None
if wl:
    for i, stock in enumerate(wl):
        col_info, col_btn = st.columns([10, 1])
        with col_info:
            sym_short = stock["symbol"].replace(".NS", "").replace(".BO", "")
            exchange  = "NSE" if stock["symbol"].endswith(".NS") else ("BSE" if stock["symbol"].endswith(".BO") else "")
            exch_html = (
                f'<span style="font-size:0.65rem;color:#8b949e;background:#21262d;'
                f'padding:0.1rem 0.35rem;border-radius:3px;margin-left:0.3rem">{exchange}</span>'
                if exchange else ""
            )
            st.markdown(
                f'<div class="mp-wl-item">'
                f'  <span class="mp-wl-sym">{sym_short}</span>'
                f'  {exch_html}'
                f'  <span class="mp-wl-name">{stock["name"]}</span>'
                f'  <span class="mp-wl-sector">{stock.get("sector", "—")}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            st.markdown('<div style="margin-top:0.1rem">', unsafe_allow_html=True)
            if st.button("✕", key=f"rm_{i}", help=f"Remove {stock['name']}"):
                to_remove = i
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="mp-card" style="text-align:center;padding:2rem">'
        '<p style="color:#8b949e;font-size:0.9rem;margin:0">Your watchlist is empty. Add stocks below.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

if to_remove is not None:
    removed = wl.pop(to_remove)
    st.session_state["watchlist"] = wl
    st.toast(f"Removed {removed['name']} from watchlist", icon="✓")
    st.rerun()

# ── Add stock form ────────────────────────────────────────────────────────────
section("Add a Stock")
st.markdown(
    '<div class="mp-form-card">'
    '<p class="mp-form-title">Enter stock details</p>',
    unsafe_allow_html=True,
)

with st.form("add_stock", clear_on_submit=True):
    a1, a2, a3 = st.columns(3)
    new_sym    = a1.text_input("NSE / BSE Symbol", placeholder="WIPRO.NS",
                               help="Use .NS for NSE, .BO for BSE")
    new_name   = a2.text_input("Company Name", placeholder="Wipro Limited")
    new_sector = a3.text_input("Sector", placeholder="IT")

    submitted = st.form_submit_button("＋ Add to Watchlist", type="primary")
    if submitted:
        if new_sym and new_name:
            sym_upper = new_sym.upper().strip()
            if not (sym_upper.endswith(".NS") or sym_upper.endswith(".BO")):
                st.warning("Symbol must end with .NS (NSE) or .BO (BSE). Example: WIPRO.NS")
            elif any(s["symbol"] == sym_upper for s in wl):
                st.warning(f"{sym_upper} is already in your watchlist.")
            else:
                entry = {
                    "symbol": sym_upper,
                    "name":   new_name.strip(),
                    "sector": new_sector.strip(),
                }
                wl.append(entry)
                st.session_state["watchlist"] = wl
                st.toast(f"Added {new_name} ({sym_upper})", icon="✓")
                st.rerun()
        else:
            st.warning("Symbol and Company Name are required.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Persist / Download ────────────────────────────────────────────────────────
section("Persist Changes")
st.markdown(
    '<div class="mp-card">'
    '<p style="font-size:0.85rem;color:#c9d1d9;margin:0 0 0.75rem">'
    'Changes are saved in session memory. Download the updated file and replace '
    '<code style="background:#21262d;padding:0.1rem 0.4rem;border-radius:4px;color:#58a6ff">'
    'data/watchlist.json</code> to make them permanent.'
    '</p>',
    unsafe_allow_html=True,
)
st.download_button(
    label="⬇ Download watchlist.json",
    data=json.dumps(wl, indent=2, ensure_ascii=False),
    file_name="watchlist.json",
    mime="application/json",
    type="primary",
)
st.markdown('</div>', unsafe_allow_html=True)
