from datetime import datetime, timedelta

from unittest.mock import MagicMock, patch, AsyncMock
import pytest

from src.database.models import User
from src.services.auth import auth_service
from src.conf import messages


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]

cdate = datetime.now() - timedelta(days=5)
print("birthdate: " + cdate.date().strftime("%Y-%m-%d"))

CONTACT = {
    "first_name": "Flora",
    "last_name": "Florian",
    "email": "flora@example.com",
    "phone": "+1(250)234-5678",
    "birthdate": cdate.date().strftime("%Y-%m-%d")
}

def test_create_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.post(
            "/api/contacts",
            json=CONTACT,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == CONTACT["first_name"]
        assert data["last_name"] == CONTACT["last_name"]
        assert data["email"] == CONTACT["email"]
        assert data["phone"] == CONTACT["phone"]
        assert data["birthdate"] == CONTACT["birthdate"]
        assert "id" in data


def test_get_contacts(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["first_name"] == CONTACT["first_name"]
        assert data[0]["last_name"] == CONTACT["last_name"]
        assert data[0]["email"] == CONTACT["email"]
        assert data[0]["phone"] == CONTACT["phone"]
        assert data[0]["birthdate"] == CONTACT["birthdate"]


def test_get_contacts_mask(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts/?search_mask=%or%",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["first_name"] == CONTACT["first_name"]
        assert data[0]["last_name"] == CONTACT["last_name"]
        assert data[0]["email"] == CONTACT["email"]
        assert data[0]["phone"] == CONTACT["phone"]
        assert data[0]["birthdate"] == CONTACT["birthdate"]


def test_get_contacts_mask_notfound(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts/?search_mask=%fff%",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert len(data) == 0


def test_get_contacts_birthday_notfound(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts/birthday",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert len(data) == 0


def test_get_contact(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts/1",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == CONTACT["first_name"]
        assert data["last_name"] == CONTACT["last_name"]
        assert data["email"] == CONTACT["email"]
        assert data["phone"] == CONTACT["phone"]
        assert data["birthdate"] == CONTACT["birthdate"]


def test_get_contact_notfound(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts/2",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.NOT_FOUND


def test_update_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        cdate = datetime.now() + timedelta(days=5)
        print("birthdate: " + cdate.date().strftime("%Y-%m-%d"))
        CONTACT["birthdate"] = cdate.date().strftime("%Y-%m-%d")

        response = client.put(
            "/api/contacts/1",
            json=CONTACT,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == CONTACT["first_name"]
        assert data["last_name"] == CONTACT["last_name"]
        assert data["email"] == CONTACT["email"]
        assert data["phone"] == CONTACT["phone"]
        assert data["birthdate"] == CONTACT["birthdate"]
        assert "id" in data


def test_update_contact_notfound(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.put(
            "/api/contacts/2",
            json=CONTACT,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.NOT_FOUND


def test_get_contacts_birthday(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.get("/api/contacts/birthday",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["first_name"] == CONTACT["first_name"]
        assert data[0]["last_name"] == CONTACT["last_name"]
        assert data[0]["email"] == CONTACT["email"]
        assert data[0]["phone"] == CONTACT["phone"]
        assert data[0]["birthdate"] == CONTACT["birthdate"]


def test_delete_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204, response.text


def test_repeat_delete_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.depends.RateLimiter', AsyncMock())

        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == messages.NOT_FOUND
