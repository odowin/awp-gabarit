import api
import pytest
from fastapi.testclient import TestClient

client = TestClient(api.app)


def test_ouvertures_blitz():
    r = client.get("/ouvertures", params={"cadence": "blitz"})
    assert r.status_code == 200
    premiere = r.json()[0]
    assert premiere["famille"] == "Hungarian Opening"
    assert premiere["n"] == 34
    assert premiere["score"] == pytest.approx(0.324, abs=1e-3)
    assert premiere["gaffes"] == pytest.approx(2.647, abs=1e-3)


def test_ouvertures_parametres_invalides():
    assert client.get("/ouvertures", params={"cadence": "rapide"}).status_code == 422
    assert client.get("/ouvertures", params={"min_n": 0}).status_code == 422


def test_parties_recentes_d_abord():
    r = client.get("/parties", params={"limit": 10})
    assert r.status_code == 200
    dates = [p["date_jeu"] for p in r.json()]
    assert len(dates) == 10
    assert dates == sorted(dates, reverse=True)


def test_parties_limit_invalide():
    assert client.get("/parties", params={"limit": 0}).status_code == 422
    assert client.get("/parties", params={"limit": 501}).status_code == 422


def test_parties_couleur():
    r = client.get("/parties", params={"couleur": "black", "limit": 50})
    assert {p["couleur"] for p in r.json()} == {"black"}


def test_predict():
    corps = {"couleur": "white", "cadence": "blitz", "ecart_elo": 50, "heure": 20}
    r = client.post("/predict", json=corps)
    assert r.status_code == 200
    assert 0 <= r.json()["proba_victoire"] <= 1


def test_predict_heure_invalide():
    corps = {"couleur": "white", "cadence": "blitz", "ecart_elo": 50, "heure": 24}
    assert client.post("/predict", json=corps).status_code == 422
