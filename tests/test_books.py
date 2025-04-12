import json
from fastapi import status
from src.data import books

BASE_URL = '/books'

def test_get_all_books(test_client):
    response = test_client.get(f"{BASE_URL}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 8

def test_get_public_books(test_client):
    response = test_client.get(f"{BASE_URL}/",params={"status":"PUBLIC"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 4


def test_get_private_books(test_client):
    response = test_client.get(f"{BASE_URL}/",params={"status":"PRIVATE"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 4

def test_get_books_with_invalid_status(test_client):
    response = test_client.get(f"{BASE_URL}/",params={"status":"UNKNOWN"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == "Input should be 'PUBLIC' or 'PRIVATE'"

def test_create_post(test_client):
    test_create_data = {
        "title": "Mastering Async Python",
        "author": "Sophie Carter",
        "description": "A comprehensive guide to asynchronous programming in Python, with a focus on FastAPI and real-world applications.",
        "level": "Intermediate to Advanced",
        "date_published": "2024-03-15",
        "status": "PRIVATE"
    }

    response = test_client.post(f"{BASE_URL}/",content=json.dumps(test_create_data))

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == "Mastering Async Python"

def test_get_book(test_client):
    post_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    response = test_client.get(f"{BASE_URL}/{post_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == post_id

def test_get_book_not_found(test_client):
    post_id = "f47ac10b-58cc-4372-a567-0e02b2c3d473"
    response = test_client.get(f"{BASE_URL}/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update(test_client):
    post_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"

    updated_data = {
        "author": "Sophie Doe",
        "description": "A comprehensive guide to asynchronous programming in Python, with a focus on FastAPI and real-world applications.",
        "title": "Mastering Async Python",
        "level": "Intermediate to Advanced",
        "date_published": "2024-03-15",
        "status": "PRIVATE"
    }
    response = test_client.put(f"{BASE_URL}/{post_id}", content=json.dumps(updated_data))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['author'] == "Sophie Doe"

def test_update_for_non_existent_book(test_client):
    post_id = "f47ac10b-58cc-4372-a567-0e02b2c3d478"

    updated_data = {
        "author": "Sophie Doe",
        "description": "A comprehensive guide to asynchronous programming in Python, with a focus on FastAPI and real-world applications.",
        "title": "Mastering Async Python",
        "level": "Intermediate to Advanced",
        "date_published": "2024-03-15",
        "status": "PRIVATE"
    }
    response = test_client.put(f"{BASE_URL}/{post_id}", content=json.dumps(updated_data))

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_book_for_non_existent_book(test_client):
    post_id = "f47ac10b-58cc-4372-a567-0e02b2c3d478"

    response = test_client.delete(f"{BASE_URL}/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
