import json

import streamlit as st


def _load():
    with open("data/watchlist.json") as f:
        return json.load(f)


if "watchlist" not in st.session_state:
    st.session_state["watchlist"] = _load()

wl = st.session_state["watchlist"]

st.title("Watchlist")
st.caption(
    "Manage your stock watchlist. Changes persist within this session. "
    "Download the updated JSON and replace `data/watchlist.json` in the repo to make them permanent."
)

# Current list
st.subheader("Current Watchlist")
to_remove = None
for i, stock in enumerate(wl):
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    c1.write(f"**{stock['name']}**")
    c2.write(stock["symbol"])
    c3.write(stock.get("sector", "—"))
    if c4.button("Remove", key=f"rm_{i}"):
        to_remove = i

if to_remove is not None:
    wl.pop(to_remove)
    st.session_state["watchlist"] = wl
    st.rerun()

st.divider()

# Add stock
st.subheader("Add Stock")
with st.form("add_stock", clear_on_submit=True):
    a1, a2, a3 = st.columns(3)
    new_sym    = a1.text_input("Symbol", placeholder="WIPRO.NS")
    new_name   = a2.text_input("Company Name", placeholder="Wipro")
    new_sector = a3.text_input("Sector", placeholder="IT")
    if st.form_submit_button("Add to Watchlist"):
        if new_sym and new_name:
            entry = {
                "symbol": new_sym.upper().strip(),
                "name":   new_name.strip(),
                "sector": new_sector.strip(),
            }
            wl.append(entry)
            st.session_state["watchlist"] = wl
            st.success(f"Added {new_name} ({new_sym.upper()})")
            st.rerun()
        else:
            st.warning("Symbol and Company Name are required.")

st.divider()

# Download
st.subheader("Persist Changes")
st.caption("Download and commit this file to make your watchlist changes permanent.")
st.download_button(
    label="Download watchlist.json",
    data=json.dumps(wl, indent=2),
    file_name="watchlist.json",
    mime="application/json",
)
