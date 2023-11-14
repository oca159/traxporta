import json
from datetime import datetime
import pytest

from fastapi.testclient import TestClient

from domain.repositories.url import UrlRepository
from infrastructure.db.models.url import Url

from main import app


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def url_repository_mock(mocker):
    return mocker.Mock(spec=UrlRepository)


def test_get_urls(client, url_repository_mock):
    # Arrange
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    url_repository_mock.get_urls.return_value = [
        Url(
            id=1,
            original="https://www.google.com.mx/maps",
            shortcode="https://s.com/gm",
            created_at=now,
            updated_at=now
        ),
        Url(
            id=2,
            original="https://www.facebook.com",
            shortcode="https://s.com/f",
            created_at=now,
            updated_at=now
        ),
    ]

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.get("/urls")

    # Assert
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "original": "https://www.google.com.mx/maps",
            "shortcode": "https://s.com/gm",
            "created_at": now_str,
            "updated_at": now_str,
        },
        {
            "id": 2,
            "original": "https://www.facebook.com",
            "shortcode": "https://s.com/f",
            "created_at": now_str,
            "updated_at": now_str,
        },
    ]


def test_get_url_by_id(client, url_repository_mock):
    # Arrange
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    url_repository_mock.get_url_by_id.return_value = Url(
        id=1,
        original="https://www.google.com.mx/maps",
        shortcode="https://s.com/gm",
        created_at=now,
        updated_at=now
    )

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.get("/urls/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "original": "https://www.google.com.mx/maps",
        "shortcode": "https://s.com/gm",
        "created_at": now_str,
        "updated_at": now_str,
    }


def test_get_url_by_shortcode(client, url_repository_mock):
    # Arrange
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    url_repository_mock.get_url_by_shortcode.return_value = Url(
        id=1,
        original="https://www.google.com.mx/maps",
        shortcode="https://s.com/gm",
        created_at=now,
        updated_at=now
    )

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.get("/urls", params={"shortcode": "https://s.com/gm"})

    # Assert
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "original": "https://www.google.com.mx/maps",
            "shortcode": "https://s.com/gm",
            "created_at": now_str,
            "updated_at": now_str,
        }
    ]


def test_create_url(client, url_repository_mock):
    # Arrange
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    url_repository_mock.create_url.return_value = Url(
        id=1,
        original="https://www.google.com.mx/maps",
        shortcode="https://s.com/gm",
        created_at=now,
        updated_at=now
    )

    with app.container.url_repository.override(url_repository_mock):
        response = client.post("/urls", json={"original": "https://www.google.com.mx/maps"})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "original": "https://www.google.com.mx/maps",
        "shortcode": "https://s.com/gm",
        "created_at": now_str,
        "updated_at": now_str,
    }


def test_update_url(client, url_repository_mock):
    # Arrange
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    url_repository_mock.get_url_by_id.return_value = Url(
        id=1,
        original="https://www.google.com.mx/maps",
        shortcode="https://s.com/gm",
        created_at=now,
        updated_at=now
    )
    url_repository_mock.update_url.return_value = Url(
        id=1,
        original="https://www.facebook.com",
        shortcode="https://s.com/f",
        created_at=now,
        updated_at=now
    )

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.patch("/urls/1",
                                json={"id": 1, "original": "https://www.facebook.com", "shortcode": "https://s.com/f"})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "original": "https://www.facebook.com",
        "shortcode": "https://s.com/f",
        "created_at": now_str,
        "updated_at": now_str,
    }


def test_delete_url(client, url_repository_mock):
    # Arrange
    url_repository_mock.delete_url.return_value = None

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.delete("/urls/1")

    # Assert
    assert response.status_code == 204

