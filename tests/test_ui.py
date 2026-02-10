from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page_serves_ui():
    response = client.get("/")

    assert response.status_code == 200
    assert "AI QA Workflow Assistant" in response.text
    assert "Create Session" in response.text
