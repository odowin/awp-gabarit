"""Exo 1 : trois figures. Environ 25 min.

Question : où ce joueur perd-il des points ?
À produire : trois figures Plotly dont le titre dit ce qu'elles montrent.
Lancer : uv run python fil_rouge/01_figures.py
"""

from data import familles, load_coups, load_data
from figures import fig_familles, fig_heures, fig_phases

df, coups = load_data(), load_coups()
print(df.shape, coups.shape)

# 1. Le score par famille d'ouvertures, la pire en haut
fig_familles(familles(df)).show()

# 2. La phase de la partie où tombent ses gaffes : ouverture, milieu, finale
fig_phases(coups).show()

# 3. Le score selon l'heure de la partie (heures UTC, au moins 30 parties par heure)
fig_heures(df).show()
