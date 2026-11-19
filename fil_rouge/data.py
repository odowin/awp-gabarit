"""Exo 1 : lire mes parties d'échecs. Environ 25 min.

Question : je joue depuis 2023, je stagne, qu'est-ce que je devrais travailler ?
À produire : un DataFrame propre, prêt pour les figures de l'exo 1 et pour l'appli de l'exo 2.
Les colonnes et leurs pièges sont dans data/echecs/LISEZMOI.md : lisez-le d'abord.
Lancer : uv run python fil_rouge/data.py
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "echecs"


def valider(df: pd.DataFrame) -> pd.DataFrame:
    """Plan B : s'arrêter avec un message clair si le fichier n'a pas la forme attendue.

    Colonnes absentes, colonnes entièrement vides, nombres lus comme du texte,
    identifiant de partie en double, résultat inconnu.
    """
    colonnes = [
        "partie_id", "date_jeu", "cadence", "couleur", "resultat",
        "elo_joueur", "elo_adverse", "ouverture_famille", "gaffes_joueur",
    ]  # fmt: skip
    absentes = [c for c in colonnes if c not in df.columns]
    if absentes:
        raise ValueError(f"Colonnes absentes : {absentes}")
    vides = [c for c in colonnes if df[c].isna().all()]
    if vides:
        raise ValueError(f"Colonnes entièrement vides : {vides}")
    for c in ["elo_joueur", "elo_adverse", "gaffes_joueur"]:
        if not pd.api.types.is_numeric_dtype(df[c]):
            raise ValueError(f"La colonne {c} devrait être numérique, pas du texte")
    if df["partie_id"].duplicated().any():
        raise ValueError("partie_id en double : une ligne doit être une partie")
    inconnus = set(df["resultat"].dropna()) - {"win", "draw", "lose"}
    if inconnus:
        raise ValueError(f"Résultats inconnus : {sorted(inconnus)}")
    return df


def load_data() -> pd.DataFrame:
    """Une ligne par partie (data/echecs/parties.csv), validée.

    Ajoutez : le résultat de mon point de vue en français, un score (1, 0,5 ou 0),
    l'année, l'heure, et l'écart d'Elo avec l'adversaire. Une cadence vide veut dire
    « aucune » : ne la laissez pas disparaître des filtres.
    Les exos suivants lisent ces colonnes, gardez ces noms : date_jeu (en datetime),
    resultat (victoire, nulle, défaite), score, annee, heure (UTC), ecart_elo
    (Elo de l'adversaire moins le mien), cadence.
    """
    df = pd.read_csv(DATA / "parties.csv", parse_dates=["date_jeu"])
    df = valider(df)
    df["score"] = df["resultat"].map({"win": 1, "draw": 0.5, "lose": 0})
    df["resultat"] = df["resultat"].map({"win": "victoire", "draw": "nulle", "lose": "défaite"})
    df["annee"] = df["date_jeu"].dt.year
    df["heure"] = df["date_jeu"].dt.hour
    df["ecart_elo"] = df["elo_adverse"] - df["elo_joueur"]
    df["cadence"] = df["cadence"].fillna("aucune")
    return df


def load_coups() -> pd.DataFrame:
    """Un de mes coups jugés mauvais par ligne (data/echecs/coups_juges.csv)."""
    return pd.read_csv(DATA / "coups_juges.csv")


def familles(df: pd.DataFrame, min_n: int = 30) -> pd.DataFrame:
    """Score moyen par famille d'ouvertures, la pire d'abord.

    Colonnes : famille, n (parties), score, gaffes (par partie).
    Sous min_n parties le chiffre ne dit rien : écartez la famille.
    """
    t = df.groupby("ouverture_famille").agg(
        n=("partie_id", "count"), score=("score", "mean"), gaffes=("gaffes_joueur", "mean")
    )
    t = t[t["n"] >= min_n].reset_index(names="famille")
    return t.sort_values("score").reset_index(drop=True)


if __name__ == "__main__":
    d = load_data()
    print(d.shape)
