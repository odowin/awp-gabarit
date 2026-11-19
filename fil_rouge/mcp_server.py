"""Exo 6 : votre propre serveur MCP. Environ 20 min.

Question : un LLM doit pouvoir interroger mes parties.
À produire : un serveur FastMCP de deux ou trois outils au-dessus de votre API (api.py doit
tourner). Le LLM choisit un outil d'après son nom, sa docstring et ses arguments : soignez-les.
Lancer : uv run python fil_rouge/mcp_server.py   (stdio : c'est le client LLM qui le lance,
voir contexte/README.md pour le brancher). Lancé à la main, il n'affiche rien et attend un
client : c'est normal. Pour tester : npx @modelcontextprotocol/inspector uv run python fil_rouge/mcp_server.py
"""

import os
from typing import Literal

import requests
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

API = os.environ.get("AWP_API_URL", "http://127.0.0.1:8000")
# Deux transports. stdio (par défaut) : le client LLM lance ce script lui-même, sur la même machine.
# MCP_TRANSPORT=http : un serveur HTTP sur /mcp, pour un client qui ne lance pas le script (un client
# dans le cloud, via un hébergeur ou un tunnel). En local : 127.0.0.1:8001 (l'API est sur 8000), pas
# ouvert à la salle. Sur un hébergeur qui fixe $PORT (Render, Cloud Run) : 0.0.0.0:$PORT.
HTTP = os.environ.get("MCP_TRANSPORT") == "http"
HOTE = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
# En local, FastMCP refuse un nom d'hôte autre que 127.0.0.1 ou localhost (protection contre le DNS
# rebinding). Derrière un tunnel (MCP_TUNNEL=1), l'hôte est celui du tunnel : on lève la protection,
# le serveur est de toute façon public tant que le tunnel tourne.
TUNNEL = os.environ.get("MCP_TUNNEL") == "1"
SECU = TransportSecuritySettings(enable_dns_rebinding_protection=False) if TUNNEL else None
mcp = FastMCP(
    "echecs", host=HOTE, port=int(os.environ.get("PORT", "8001")), transport_security=SECU
)

Cadence = Literal["bullet", "blitz", "rapid"]


def appeler_api(chemin, params=None, corps=None):
    """Appelle l'API (GET si pas de corps, POST sinon) et lève une erreur si la réponse n'est pas un succès."""
    if corps is None:
        r = requests.get(f"{API}{chemin}", params=params, timeout=10)
    else:
        r = requests.post(f"{API}{chemin}", json=corps, timeout=10)
    r.raise_for_status()
    return r.json()


@mcp.tool()
def pire_ouvertures(cadence: Cadence = "blitz", n: int = 5) -> list[dict]:
    """Mes familles d'ouvertures, de la moins bonne à la meilleure, pour une cadence.

    Pour chaque famille : famille, n (nombre de parties), score (score moyen, de 0 à 1) et
    gaffes (gaffes par partie). Seules les familles jouées au moins 30 fois sont comptées.
    """
    return appeler_api("/ouvertures", {"cadence": cadence, "min_n": 30})[:n]


@mcp.tool()
def proba_victoire(
    couleur: Literal["white", "black"], cadence: Cadence, ecart_elo: float, heure: int
) -> dict:
    """Probabilité que je gagne une partie, d'après une régression logistique.

    couleur : "white" (blancs) ou "black" (noirs).
    ecart_elo : Elo de l'adversaire moins mon Elo (positif si l'adversaire est plus fort).
    heure : heure UTC de la partie, de 0 à 23.
    Attention : ce modèle fait à peine mieux que le hasard, la probabilité n'est qu'indicative.
    """
    corps = {"couleur": couleur, "cadence": cadence, "ecart_elo": ecart_elo, "heure": heure}
    return appeler_api("/predict", corps=corps)


if __name__ == "__main__":
    # Derrière un tunnel : MCP_TUNNEL=1 MCP_TRANSPORT=http uv run python …, puis npx localtunnel --port 8001
    mcp.run(transport="streamable-http" if HTTP else "stdio")
