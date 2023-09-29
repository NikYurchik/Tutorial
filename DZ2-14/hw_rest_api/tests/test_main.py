from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_read_main(monkeypatch):
    monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
    monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
    monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
    monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

    response = client.get("/")
    assert response.status_code == 200
