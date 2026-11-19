"""Exo 2 : l'appli Streamlit du fil rouge. Environ 1 h.

Question : l'appli que ce joueur ouvrirait chaque semaine pour savoir quoi travailler.
À produire : une barre latérale (cadence, période, couleur), trois st.metric, deux figures
en colonnes. Le titre de la page dit la question, pas « Dashboard ».
Colonnes utilisées : cadence (dont « aucune »), date_jeu (datetime), couleur (white ou black),
score, gaffes_joueur. Si votre load_data() ne les donne pas ainsi, corrigez-la.
Lancer : uv run streamlit run fil_rouge/app_streamlit.py --server.address 127.0.0.1
"""

import streamlit as st

from data import familles, load_coups, load_data
from figures import fig_familles, fig_phases

st.set_page_config(page_title="Mes parties d'échecs", layout="wide")
print("relance")  # regardez le terminal à chaque clic


@st.cache_data
def donnees():
    return load_data(), load_coups()


df, coups = donnees()

st.title("Je stagne aux échecs : qu'est-ce que je dois travailler ?")

with st.sidebar:
    cadences = st.multiselect(
        "Cadence", sorted(df["cadence"].unique()), default=["blitz"], key="cadence"
    )
    debut, fin = df["date_jeu"].min().date(), df["date_jeu"].max().date()
    periode = st.date_input("Période", value=(debut, fin), key="periode")
    couleur = st.radio("Couleur", ["toutes", "blancs", "noirs"], horizontal=True, key="couleur")
    n_min = st.slider("Parties minimum par ouverture", 30, 60, 30, step=10, key="n_min")

# La période n'a qu'une date tant que la seconde n'est pas choisie
if len(periode) != 2:
    st.warning("Choisissez la seconde date de la période.")
    st.stop()

vue = df[df["cadence"].isin(cadences)]
vue = vue[vue["date_jeu"].dt.date.between(periode[0], periode[1])]
if couleur != "toutes":
    vue = vue[vue["couleur"] == {"blancs": "white", "noirs": "black"}[couleur]]
if vue.empty:
    st.warning("Aucune partie ne correspond à ces filtres.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Parties", len(vue))
c2.metric("Score", f"{100 * vue['score'].mean():.1f} %")
c3.metric("Gaffes par partie", f"{vue['gaffes_joueur'].mean():.2f}")

g1, g2 = st.columns(2)
with g1:
    event = st.plotly_chart(
        fig_familles(familles(vue, n_min)),
        on_select="rerun",
        selection_mode="points",
        key="familles",
        alt="Barres du score moyen par famille d'ouvertures, la pire en haut.",
    )
with g2:
    st.plotly_chart(
        fig_phases(coups[coups["partie_id"].isin(vue["partie_id"])]),
        alt="Nombre de gaffes par phase de la partie : ouverture, milieu, finale.",
    )

# Bonus : cliquer sur une barre liste les parties de cette famille
points = event.selection.points
if points:
    famille = points[0]["y"]  # barres horizontales : le nom est sur l'axe y
    st.subheader(f"Parties jouées avec {famille}")
    colonnes = ["partie_id", "date_jeu", "cadence", "couleur", "resultat", "elo_adverse"]
    parties = vue[vue["ouverture_famille"] == famille]
    st.dataframe(
        parties.sort_values("date_jeu", ascending=False)[colonnes + ["gaffes_joueur"]],
        hide_index=True,
    )
