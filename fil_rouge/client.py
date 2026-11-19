"""Bonus de l'exo 5 : une appli Streamlit « et si ? » qui appelle POST /predict.

Lancez api.py d'abord.
Lancer : uv run streamlit run fil_rouge/client.py --server.address 127.0.0.1
"""

import os

import requests
import streamlit as st

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")

st.title("Et si je jouais plus tard, ou avec les noirs ?")

with st.form("simulation"):
    couleur = st.radio(
        "Couleur",
        ["white", "black"],
        format_func=lambda c: "blancs" if c == "white" else "noirs",
    )
    cadence = st.selectbox("Cadence", ["blitz", "rapid", "bullet"])
    ecart = st.number_input("Elo de l'adversaire moins le mien", -400.0, 400.0, 0.0)
    heure = st.slider("Heure (UTC)", 0, 23, 20)
    envoye = st.form_submit_button("Estimer")

if envoye:
    corps = {"couleur": couleur, "cadence": cadence, "ecart_elo": ecart, "heure": heure}
    try:
        r = requests.post(f"{API}/predict", json=corps, timeout=10)
    except requests.RequestException:
        st.error(f"L'API ne répond pas sur {API}. Lancez uvicorn, puis rechargez la page.")
    else:
        if r.ok:
            st.metric("Chances de victoire", f"{r.json()['proba_victoire']:.0%}")
        else:
            st.error(f"L'API refuse la requête ({r.status_code}) : {r.json().get('detail')}")
