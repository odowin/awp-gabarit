import app_dash


def test_parties_d_une_famille():
    lignes = app_dash.parties({"points": [{"y": "French Defense"}]})
    assert len(lignes) > 30


def test_coups_d_une_partie():
    assert "d3" in [c["coup"] for c in app_dash.detail([{"partie_id": "P0001"}])]


def test_sans_clic_rien_a_afficher():
    assert app_dash.parties(None) == []
    assert app_dash.detail(None) == []


def test_pire_famille_en_haut():
    fig = app_dash.maj_familles(30)
    assert fig.data[0].y[0] == "Hungarian Opening"
