from fastapi.testclient import TestClient
from src import app
import pytest

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client