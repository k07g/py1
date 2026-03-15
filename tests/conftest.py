import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_book():
    return {
        "id": "test-id-1234",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "published_year": 2008,
        "genre": "Programming",
        "description": "A handbook of agile software craftsmanship.",
        "created_at": "2024-01-01T00:00:00+00:00",
        "updated_at": "2024-01-01T00:00:00+00:00",
    }
