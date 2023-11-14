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
    url_repository_mock.get_urls.return_value = [
        Url(id=1, name="osvaldo", url_number="123", balance=100),
        Url(id=2, name="ana", url_number="567", balance=50),
    ]

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.get("/urls")

    # Assert
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "osvaldo", "url_number": "123", "balance": 100},
        {"id": 2, "name": "ana", "url_number": "567", "balance": 50},
    ]


def test_get_url(client, url_repository_mock):
    # Arrange
    url_repository_mock.get_url_by_id.return_value = Url(id=1, name="osvaldo", url_number="123",
                                                                     balance=100)

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.get("/urls/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "osvaldo", "url_number": "123", "balance": 100}


def test_get_url_balance(client, url_repository_mock):
    # Arrange
    url_repository_mock.get_url_by_id.return_value = Url(id=1, name="osvaldo", url_number="123",
                                                                     balance=100)

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.get("/urls/1/balance")

    # Assert
    assert response.status_code == 200
    assert response.json() == 100


def test_create_url(client, url_repository_mock):
    # Arrange
    url_repository_mock.create_url.return_value = Url(id=1, name="osvaldo", url_number="123",
                                                                     balance=100)
    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.post("/urls", json={"name": "osvaldo", "url_number": "123", "balance": 100})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "osvaldo", "url_number": "123", "balance": 100}


def test_update_url(client, url_repository_mock):
    # Arrange
    url_repository_mock.get_url_by_id.return_value = Url(id=1, name="osvaldo", url_number="123",
                                                                     balance=100)
    url_repository_mock.update_url.return_value = Url(id=1, name="osvaldo", url_number="456",
                                                                  balance=100)

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.patch("/urls/1",
                                json={"id": 1, "name": "osvaldo", "url_number": "456", "balance": 100})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "osvaldo", "url_number": "456", "balance": 100}


def test_delete_url(client, url_repository_mock):
    # Arrange
    url_repository_mock.delete_url.return_value = None

    # Act
    with app.container.url_repository.override(url_repository_mock):
        response = client.delete("/urls/1")

    # Assert
    assert response.status_code == 204

