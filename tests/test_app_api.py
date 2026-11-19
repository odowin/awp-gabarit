from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).parent.parent / "fil_rouge" / "app_api.py"


def test_api_arretee_message_lisible(monkeypatch):
    monkeypatch.setenv("AWP_API_URL", "http://127.0.0.1:9")
    at = AppTest.from_file(str(APP)).run()
    assert not at.exception
    assert len(at.error) == 1
    assert "ne répond pas" in at.error[0].value
