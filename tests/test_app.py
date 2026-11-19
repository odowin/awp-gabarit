import pandas as pd
import pytest

import data

PARTIES = ["partie_id", "date_jeu", "resultat", "cadence", "couleur", "elo_joueur", "elo_adverse"]


def test_csv_des_parties_se_lisent():
    df = pd.read_csv(data.DATA / "parties.csv")
    assert len(df) > 1000
    assert set(PARTIES) <= set(df.columns)
    assert df["partie_id"].is_unique


def test_csv_des_coups_juges_se_lisent():
    coups = pd.read_csv(data.DATA / "coups_juges.csv")
    assert {"partie_id", "coup", "jugement", "phase"} <= set(coups.columns)


def test_load_data_une_ligne_par_partie():
    df = data.load_data()
    assert df["partie_id"].is_unique
    assert df["score"].isin([0, 0.5, 1]).all()


def test_familles_pire_en_premier():
    f = data.familles(data.load_data(), 30)
    assert f["score"].is_monotonic_increasing


def test_valider_refuse_un_fichier_mal_forme():
    df = pd.read_csv(data.DATA / "parties.csv")
    with pytest.raises(ValueError):
        data.valider(df.drop(columns=["cadence"]))
    with pytest.raises(ValueError):
        data.valider(pd.concat([df, df.head(1)]))
    with pytest.raises(ValueError):
        data.valider(df.assign(resultat="gagné"))
