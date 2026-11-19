"""Exo 4 : la même appli en Dash, avec un drill-down. Environ 25 min.

Question : quelles ouvertures coûtent des points, et dans quelles parties ?
À produire : un curseur (parties minimum) et le graphique des familles ; un clic sur une barre
liste les parties, un clic sur une partie liste les coups jugés mauvais, dans deux AG Grid.
Lancer : uv run python fil_rouge/app_dash.py   (http://127.0.0.1:8050)
"""

import dash_ag_grid as dag
from dash import Dash, Input, Output, callback, dcc, html

from data import familles, load_coups, load_data
from figures import fig_familles

df = load_data()  # lus une seule fois, au démarrage
coups = load_coups()

app = Dash(__name__, title="Mes parties d'échecs")
server = app.server  # Dash tourne sur Flask

# réglages AG Grid communs (AGENTS.md)
GRILLE = {"columnSize": "responsiveSizeToFit", "defaultColDef": {"filter": True, "sortable": True}}
OPTIONS = {
    "theme": "themeBalham",
    "animateRows": True,
    "pagination": True,
    "paginationPageSize": 10,
}

COLS_PARTIES = [
    "partie_id",
    "date_jeu",
    "cadence",
    "couleur",
    "resultat",
    "elo_adverse",
    "gaffes_joueur",
]
COLS_COUPS = ["numero_coup", "coup", "meilleur_coup", "phase", "jugement"]

app.layout = html.Div(
    [
        html.H2("Quelles ouvertures me coûtent des points ? Cliquez une barre"),
        dcc.Slider(30, 60, 10, value=30, id="n-min"),
        dcc.Graph(id="familles"),
        html.H3("Parties de la famille"),
        html.P("Cliquez une partie pour voir ses coups jugés."),
        dag.AgGrid(
            id="parties",
            columnDefs=[{"field": c} for c in COLS_PARTIES],
            dashGridOptions={
                **OPTIONS,
                "rowSelection": {"mode": "singleRow", "enableClickSelection": True},
            },
            **GRILLE,
        ),
        html.H3("Coups jugés de la partie"),
        dag.AgGrid(
            id="coups",
            columnDefs=[{"field": c} for c in COLS_COUPS],
            dashGridOptions=OPTIONS,
            **GRILLE,
        ),
    ]
)


def en_records(table):
    """Lignes prêtes pour AG Grid : les NaN deviennent None (JSON valide)."""
    return table.astype(object).where(table.notna(), None).to_dict("records")


@callback(Output("familles", "figure"), Input("n-min", "value"))
def maj_familles(n_min):
    return fig_familles(familles(df, n_min))


@callback(Output("parties", "rowData"), Input("familles", "clickData"))
def parties(click):
    if not click:
        return []
    famille = click["points"][0]["y"]
    lignes = df[df["ouverture_famille"] == famille].sort_values("date_jeu", ascending=False)
    lignes = lignes.assign(date_jeu=lignes["date_jeu"].astype(str))
    return en_records(lignes[COLS_PARTIES])


@callback(Output("coups", "rowData"), Input("parties", "selectedRows"))
def detail(rows):
    if not rows:
        return []
    lignes = coups[coups["partie_id"] == rows[0]["partie_id"]]
    return en_records(lignes[COLS_COUPS])


if __name__ == "__main__":
    # debug=True : bouton « Callbacks » en bas à droite, le graphe des callbacks
    app.run(debug=True, port=8050)
