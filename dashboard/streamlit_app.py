import os
import sys
from pathlib import Path

import streamlit as st
import runpy

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PAGES_DIR = ROOT / "pages"

st.set_page_config(page_title="Finance Dashboard", layout="wide",page_icon="💵")

st.sidebar.title("Navigation for devs...❤️")
page_files = sorted([p for p in PAGES_DIR.iterdir() if p.suffix == ".py"])
page_names = [p.name for p in page_files]

choice = st.sidebar.selectbox("Select page", page_names)

selected_path = PAGES_DIR / choice

try:
    ns = runpy.run_path(str(selected_path), run_name=choice)
    show = ns.get("show")
    if callable(show):
        show()
    else:
        st.error(f"Page {choice} does not expose a `show()` function.")
except Exception as e:
    st.exception(e)
