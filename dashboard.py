import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Market Predictor — Indian Equity Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui.styles import inject_css
inject_css()

# ── Sidebar branding (visible on every page) ──────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p class="mp-brand">Market<span class="mp-brand-accent">Predictor</span></p>'
        '<span class="mp-brand-tag">Indian Equity Intelligence</span>',
        unsafe_allow_html=True,
    )
    st.divider()

pg = st.navigation([
    st.Page("pages/home.py",      title="Home",         icon="🏠", default=True),
    st.Page("pages/screener.py",  title="Screener",     icon="📊"),
    st.Page("pages/detail.py",    title="Stock Detail", icon="🔍"),
    st.Page("pages/watchlist.py", title="Watchlist",    icon="⭐"),
])
pg.run()
