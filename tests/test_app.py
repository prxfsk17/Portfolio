import pytest

from main import app
from modules.morse import MorseConverter


@pytest.fixture
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    return app.test_client()


def test_home_page(client):
    assert client.get("/").status_code == 200


def test_portfolio_page_lists_projects(client):
    response = client.get("/portfolio")
    assert response.status_code == 200
    assert b"Morse" in response.data


def test_project_page(client):
    assert client.get("/project/morse").status_code == 200


def test_unknown_project_returns_404(client):
    assert client.get("/project/does-not-exist").status_code == 404


def test_contact_page(client):
    assert client.get("/contact").status_code == 200


def test_f1_demo_home(client):
    assert client.get("/demo/api-website/").status_code == 200


def test_morse_encode():
    assert MorseConverter("cipher").operate("SOS").strip() == "... --- ..."


def test_morse_decode():
    assert MorseConverter("decipher").operate("... --- ...").strip() == "SOS"