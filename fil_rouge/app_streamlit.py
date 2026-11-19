"""Exo 2 : l'appli Streamlit du fil rouge. Environ 1 h.

Question : l'appli que ce joueur ouvrirait chaque semaine pour savoir quoi travailler.
À produire : une barre latérale (cadence, période, couleur), trois st.metric, deux figures
en colonnes. Le titre de la page dit la question, pas « Dashboard ».
Colonnes utilisées : cadence (dont « aucune »), date_jeu (datetime), couleur (white ou black),
score, gaffes_joueur. Si votre load_data() ne les donne pas ainsi, corrigez-la.
Lancer : uv run streamlit run fil_rouge/app_streamlit.py --server.address 127.0.0.1
"""

import plotly.express as px  # noqa: F401
import streamlit as st

from data import load_coups, load_data  # noqa: F401

st.set_page_config(page_title="Mes parties d'échecs", layout="wide")
print("relance")  # regardez le terminal à chaque clic

# TODO 1. Charger les données une seule fois (@st.cache_data)
# TODO 2. Le titre, puis la barre latérale : widgets avec key=
# TODO 3. Filtrer, et un message clair si aucune partie ne reste (st.warning puis st.stop).
#         La période n'a qu'une date tant que la seconde n'est pas choisie : len(periode) != 2 -> st.stop()
# TODO 4. Trois st.metric : parties, score, gaffes par partie
# TODO 5. Deux figures côte à côte (st.columns) : les figures 1 et 2 de l'exo 1 (familles d'ouvertures,
#         phase des gaffes), recopiées ici et calculées sur les parties filtrées
#         (pour les gaffes : coups[coups["partie_id"].isin(vue["partie_id"])])
