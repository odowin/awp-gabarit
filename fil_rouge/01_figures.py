"""Exo 1 : trois figures. Environ 25 min.

Question : où ce joueur perd-il des points ?
À produire : trois figures Plotly dont le titre dit ce qu'elles montrent.
Lancer : uv run python fil_rouge/01_figures.py
"""

import plotly.express as px  # noqa: F401

from data import familles, load_coups, load_data  # noqa: F401

df, coups = load_data(), load_coups()
print(df.shape, coups.shape)

# 1. Le score par famille d'ouvertures, la pire en haut (px.bar, familles(df))

# 2. La phase de la partie où tombent ses gaffes : ouverture, milieu, finale (coups)

# 3. Le score selon l'heure de la partie (heures UTC, au moins 30 parties par heure)
