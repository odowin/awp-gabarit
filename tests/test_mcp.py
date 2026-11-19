"""Tests du serveur MCP : outils exposés et schémas envoyés au client LLM."""

import asyncio

import mcp_server


def outils():
    return {t.name: t for t in asyncio.run(mcp_server.mcp.list_tools())}


def test_outils_exposes():
    assert {"pire_ouvertures", "proba_victoire"} <= set(outils())


def test_cadence_limitee_aux_valeurs_permises():
    schema = outils()["pire_ouvertures"].inputSchema
    assert schema["properties"]["cadence"]["enum"] == ["bullet", "blitz", "rapid"]


def test_descriptions_non_vides():
    for outil in outils().values():
        assert outil.description and outil.description.strip()
