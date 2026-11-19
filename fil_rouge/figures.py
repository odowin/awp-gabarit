"""Figures Plotly de l'exo 1, réutilisées par les applis des exos suivants.

Chaque fonction reçoit des données et renvoie une figure dont le titre dit ce qu'elle montre.
"""

import plotly.express as px
import plotly.graph_objects as go

BLEU = "#0072B2"  # Okabe-Ito, lisible pour les daltoniens


def pct(x: float) -> str:
    """0.361 -> '36,1 %' (virgule française)."""
    return f"{x * 100:.1f} %".replace(".", ",")


def sans_donnee() -> go.Figure:
    """Figure vide, pour quand un filtre ne laisse rien."""
    return go.Figure(layout_title_text="Aucune donnée pour ce filtre")


def fig_familles(table):
    """Barres horizontales du score par famille (table de familles()), la pire en haut."""
    if table.empty:
        return sans_donnee()
    table = table.sort_values("score")
    pire = table.iloc[0]
    fig = px.bar(
        table,
        x="score",
        y="famille",
        orientation="h",
        text="score",
        hover_data={"n": True, "score": ":.1%"},
        title=f"{pire['famille']} : {pct(pire['score'])} de score en {int(pire['n'])} parties, "
        "ma pire famille",
    )
    fig.update_traces(marker_color=BLEU, texttemplate="%{x:.1%}")
    fig.update_xaxes(tickformat=".0%", title="Score moyen")
    fig.update_yaxes(autorange="reversed", title="")  # la première ligne (la pire) en haut
    return fig


def fig_phases(coups):
    """Nombre de gaffes par phase de la partie : ouverture, milieu, finale."""
    gaffes = coups[coups["jugement"] == "blunder"]
    if gaffes.empty:
        return sans_donnee()
    noms = {"opening": "ouverture", "middlegame": "milieu", "endgame": "finale"}
    t = gaffes["phase"].map(noms).value_counts().reindex(list(noms.values()), fill_value=0)
    t = t.rename_axis("phase").reset_index(name="gaffes")
    top = t.loc[t["gaffes"].idxmax()]
    part = pct(top["gaffes"] / t["gaffes"].sum())
    fig = px.bar(
        t,
        x="phase",
        y="gaffes",
        text="gaffes",
        title=f"{part} de mes gaffes tombent en {top['phase']} ({top['gaffes']} sur "
        f"{t['gaffes'].sum()})",
    )
    fig.update_traces(marker_color=BLEU)
    fig.update_xaxes(title="Phase de la partie")
    fig.update_yaxes(title="Gaffes")
    return fig


def fig_heures(df, min_n: int = 30):
    """Score par heure UTC, pour les heures avec au moins min_n parties."""
    t = df.groupby("heure").agg(n=("score", "count"), score=("score", "mean")).reset_index()
    t = t[t["n"] >= min_n]
    if t.empty:
        return sans_donnee()
    haut = t.loc[t["score"].idxmax()]
    bas = t.loc[t["score"].idxmin()]
    fig = px.bar(
        t,
        x="heure",
        y="score",
        text="score",
        hover_data={"n": True, "score": ":.1%"},
        title=f"Meilleur score à {int(haut['heure'])} h UTC ({pct(haut['score'])}), "
        f"pire à {int(bas['heure'])} h UTC ({pct(bas['score'])})",
    )
    fig.update_traces(marker_color=BLEU, texttemplate="%{y:.0%}")
    fig.update_xaxes(title="Heure de la partie (UTC)", dtick=1)
    fig.update_yaxes(tickformat=".0%", title="Score moyen")
    return fig
