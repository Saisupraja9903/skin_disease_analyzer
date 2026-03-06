import sys
import os
import pytest

# make sure the `backend` package (which uses bare `services` imports) is
# on sys.path.  We append the absolute path to the backend folder itself.
base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base, "backend"))

try:
    from fastapi.testclient import TestClient
except ImportError:
    pytest.skip("fastapi or httpx not installed", allow_module_level=True)

from backend.routes.diagnosis_routes import router
from fastapi import FastAPI

# mount router onto a temporary app for testing
app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_upload_endpoint_slices_to_eight(monkeypatch):
    class DummyResponse:
        status_code = 200
        def json(self):
            # return more than eight predictions, backend should slice
            return {"predictions": [["A", 0.1]] * 12}
        def raise_for_status(self):
            pass

    def dummy_post(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("requests.post", dummy_post)

    response = client.post("/upload", files={"file": ("x.png", b"data", "image/png")})
    assert response.status_code == 200
    body = response.json()
    assert "questions" in body
    assert len(body["questions"]) >= 0  # questions may be empty but no error
    assert len(body.get("predictions", [])) <= 8
    assert len(body.get("predictions", [])) == 8
