from fastapi import status, HTTPException
import json

import pytest

BASE_URL = "/books"


def test_create_get_book(test_client, test_book_payload):
    response = test_client.post(f"{BASE_URL}/", content=json.dumps(test_book_payload))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Python Testing with pytest"

    book_id = response.json()["id"]

    response = test_client.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(book_id)
    assert response.json()["title"] == "Python Testing with pytest"

def test_create_book_with_invalid_payload(test_client):
    invalid_payload = {
        "title": "Python Testing with pytest",
        "author": "Brian Okken",
        # Missing required fields
    }
    response = test_client.post(f"{BASE_URL}/", content=json.dumps(invalid_payload))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_get_book_not_found(test_client):
    # Assuming a book with ID '123e4567-e89b-12d3-a456-426614174000' does not exist
    response = test_client.get(f"{BASE_URL}/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Book not found"


def test_get_all_books(test_client):
    response = test_client.get(f"{BASE_URL}/")
    assert response.status_code == status.HTTP_200_OK


def test_get_all_public_books(test_client):
    response = test_client.get(f"{BASE_URL}/", params={"status": "PUBLIC"})
    assert response.status_code == status.HTTP_200_OK


def test_get_all_private_books(test_client):
    response = test_client.get(f"{BASE_URL}/", params={"status": "PRIVATE"})
    assert response.status_code == status.HTTP_200_OK

def test_get_books_with_invalid_status(test_client):
    # Assuming 'INVALID_STATUS' is not a valid status
    response = test_client.get(f"{BASE_URL}/", params={"status": "INVALID_STATUS"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Input should be 'PUBLIC' or 'PRIVATE'"


def test_create_update_book(test_client, test_book_payload, test_book_update_payload):
    # Create a book first
    response = test_client.post(f"{BASE_URL}/", content=json.dumps(test_book_payload))
    book_id = response.json()["id"]

    # Update the book
    response = test_client.put(
        f"{BASE_URL}/{book_id}", content=json.dumps(test_book_update_payload)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Python Testing with pytest"


def test_update_book_not_found(test_client, test_book_update_payload):
    # Assuming a book with ID '123e4567-e89b-12d3-a456-426614174000' does not exist
    response = test_client.put(
        f"{BASE_URL}/123e4567-e89b-12d3-a456-426614174000",
        content=json.dumps(test_book_update_payload),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Book not found"


def test_update_book_with_invalid_payload(test_client, test_book_payload):
    # Create a book first
    response = test_client.post(f"{BASE_URL}/", content=json.dumps(test_book_payload))
    book_id = response.json()["id"]

    # Update the book with invalid payload
    invalid_payload = {
        "title": "Updated Python Testing with pytest",
        "author": "Brian Okken",
        # Missing required fields
    }
    response = test_client.put(
        f"{BASE_URL}/{book_id}", content=json.dumps(invalid_payload)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Field required"
    

def test_create_delete_book(test_client, test_book_payload):
    response = test_client.post(f"{BASE_URL}/", content=json.dumps(test_book_payload))
    book_id = response.json()["id"]
    response = test_client.delete(f"{BASE_URL}/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the book is really deleted
    response = test_client.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Book not found"


def test_delete_book_not_found(test_client):
    # Assuming a book with ID '123e4567-e89b-12d3-a456-426614174000' does not exist
    response = test_client.delete(f"{BASE_URL}/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"]
        == "Book with uuid 123e4567-e89b-12d3-a456-426614174000 not found."
    )
