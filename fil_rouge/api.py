"""Exo 5 : le service FastAPI. Environ 45 min.

Question : mes parties derrière une API que n'importe quel client peut appeler (votre appli, puis l'agent de l'exo 6).
À produire : GET /ouvertures et GET /parties, paramètres validés (une cadence inconnue renvoie 422, pas une liste vide).
Ensuite : app_api.py, ou votre appli de l'exo 2 ou de l'exo 4, appelle cette API au lieu de lire les CSV.
Bonus : POST /predict avec le modèle fourni (fil_rouge/model.joblib, déjà entraîné), puis client.py.
Lancer : uv run uvicorn api:app --app-dir fil_rouge --host 127.0.0.1 --port 8000 --reload
Documentation interactive : http://127.0.0.1:8000/docs
"""

from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from data import familles, load_data

app = FastAPI(title="Mes parties d'échecs", version="1.0")

df = load_data()  # chargé une seule fois, au démarrage
model = joblib.load(Path(__file__).parent / "model.joblib")

Cadence = Literal["bullet", "blitz", "rapid"]


class Partie(BaseModel):
    couleur: Literal["white", "black"]
    cadence: Cadence
    ecart_elo: float = Field(ge=-1000, le=1000)
    heure: int = Field(ge=0, le=23)


@app.get("/ouvertures")
def ouvertures(cadence: Cadence | None = None, min_n: int = Query(30, ge=1)):
    """Familles d'ouvertures, la pire d'abord (score moyen)."""
    vue = df if cadence is None else df[df["cadence"] == cadence]
    return familles(vue, min_n).to_dict("records")


@app.get("/parties")
def parties(
    cadence: Cadence | None = None,
    couleur: Literal["white", "black"] | None = None,
    limit: int = Query(10, ge=1, le=500),
):
    """Les parties les plus récentes d'abord, filtrables par cadence et couleur."""
    vue = df
    if cadence is not None:
        vue = vue[vue["cadence"] == cadence]
    if couleur is not None:
        vue = vue[vue["couleur"] == couleur]
    colonnes = [
        "partie_id", "date_jeu", "cadence", "couleur", "resultat",
        "ouverture_famille", "elo_joueur", "elo_adverse",
        "gaffes_joueur", "precision_joueur",
    ]  # fmt: skip
    vue = vue.sort_values("date_jeu", ascending=False).head(limit)[colonnes].copy()
    vue["date_jeu"] = vue["date_jeu"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    # JSON ne sait pas écrire NaN : on le remplace par None (null)
    vue = vue.astype(object).where(vue.notna(), None)
    return vue.to_dict("records")


@app.post("/predict")
def predict(partie: Partie):
    """Probabilité de victoire d'une partie, d'après le modèle entraîné."""
    X = pd.DataFrame([partie.model_dump()])
    return {"proba_victoire": float(model.predict_proba(X)[0, 1])}  # colonne 1 = True
