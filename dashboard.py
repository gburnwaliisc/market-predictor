import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Market Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation([
    st.Page("pages/home.py",      title="Home",         icon="🏠", default=True),
    st.Page("pages/screener.py",  title="Screener",     icon="📊"),
    st.Page("pages/detail.py",    title="Stock Detail", icon="🔍"),
    st.Page("pages/watchlist.py", title="Watchlist",    icon="⭐"),
])
pg.run()
