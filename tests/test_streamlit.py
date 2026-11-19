from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "fil_rouge" / "app_streamlit.py"


def lancer():
    return AppTest.from_file(str(APP), default_timeout=30).run()


def metriques(at):
    return {m.label: m.value for m in at.metric}


def test_lancement_par_defaut():
    at = lancer()
    assert not at.exception
    assert metriques(at) == {"Parties": "2774", "Score": "51.0 %", "Gaffes par partie": "2.34"}


def test_couleur_noirs():
    at = lancer()
    at.radio(key="couleur").set_value("noirs").run()
    assert not at.exception
    assert metriques(at) == {"Parties": "1397", "Score": "49.1 %", "Gaffes par partie": "2.31"}


def test_aucune_cadence_affiche_un_avertissement():
    at = lancer()
    at.multiselect(key="cadence").set_value([]).run()
    assert len(at.warning) == 1
    assert len(at.metric) == 0


def test_periode_incomplete_affiche_un_avertissement():
    at = lancer()
    premiere_date = at.date_input(key="periode").value[0]
    at.date_input(key="periode").set_value(premiere_date).run()
    assert len(at.warning) == 1
    assert len(at.metric) == 0
