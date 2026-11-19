"""Exo 5, suite : l'appli ne lit plus les CSV, elle demande à l'API.

Lancez api.py d'abord.
Lancer : uv run streamlit run fil_rouge/app_api.py --server.address 127.0.0.1
"""

import os

import pandas as pd
import requests
import streamlit as st

from figures import fig_familles

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Mes parties d'échecs", layout="wide")
st.title("Quelles ouvertures me coûtent des points ?")


def appeler(chemin, **params):
    r = requests.get(f"{API}{chemin}", params=params, timeout=10)
    r.raise_for_status()
    return pd.DataFrame(r.json())


cadence = st.sidebar.selectbox("Cadence", ["blitz", "rapid", "bullet"], key="cadence")
n_min = st.sidebar.slider("Parties minimum par ouverture", 30, 60, step=10, key="n_min")

try:
    ouvertures = appeler("/ouvertures", cadence=cadence, min_n=n_min)
    parties = appeler("/parties", cadence=cadence, limit=10)
except requests.RequestException:
    st.error(f"L'API ne répond pas sur {API}. Lancez uvicorn, puis rechargez la page.")
    st.stop()

st.plotly_chart(fig_familles(ouvertures))
st.dataframe(parties)
