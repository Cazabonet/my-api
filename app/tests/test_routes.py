import pytest
from fastapi import status
from app.core.constants import BookStatus, LoanStatus, ReservationStatus


def test_create_pessoa(client):
    """Test creating a person."""
    response = client.post(
        "/api/v1/pessoas/",
        json={
            "nome": "John Doe",
            "email": "john@example.com",
            "senha": "password123",
            "admin": False
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert data["data"]["nome"] == "John Doe"
    assert data["data"]["email"] == "john@example.com"
    assert data["data"]["admin"] is False


def test_create_livro(client):
    """Test creating a book."""
    response = client.post(
        "/api/v1/livros/",
        json={
            "titulo": "Test Book",
            "autor": "Test Author",
            "isbn": "1234567890",
            "quantidade": 5
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert data["data"]["titulo"] == "Test Book"
    assert data["data"]["autor"] == "Test Author"
    assert data["data"]["isbn"] == "1234567890"
    assert data["data"]["quantidade"] == 5


def test_create_emprestimo(client, test_user, test_book):
    """Test creating a loan."""
    response = client.post(
        "/api/v1/emprestimos/",
        json={
            "pessoa_id": test_user.id,
            "livro_id": test_book.id
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert data["data"]["pessoa_id"] == test_user.id
    assert data["data"]["livro_id"] == test_book.id
    assert data["data"]["status"] == LoanStatus.ACTIVE


def test_create_reserva(client, test_user, test_book):
    """Test creating a reservation."""
    response = client.post(
        "/api/v1/reservas/",
        json={
            "pessoa_id": test_user.id,
            "livro_id": test_book.id
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert data["data"]["pessoa_id"] == test_user.id
    assert data["data"]["livro_id"] == test_book.id
    assert data["data"]["status"] == ReservationStatus.PENDING


def test_get_pessoa(client, test_user):
    """Test getting a person."""
    response = client.get(f"/api/v1/pessoas/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == test_user.id
    assert data["data"]["nome"] == test_user.nome
    assert data["data"]["email"] == test_user.email


def test_get_livro(client, test_book):
    """Test getting a book."""
    response = client.get(f"/api/v1/livros/{test_book.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == test_book.id
    assert data["data"]["titulo"] == test_book.titulo
    assert data["data"]["autor"] == test_book.autor


def test_update_pessoa(client, test_user):
    """Test updating a person."""
    response = client.put(
        f"/api/v1/pessoas/{test_user.id}",
        json={
            "nome": "Updated Name",
            "email": test_user.email,
            "senha": test_user.senha,
            "admin": test_user.admin
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["data"]["nome"] == "Updated Name"


def test_update_livro(client, test_book):
    """Test updating a book."""
    response = client.put(
        f"/api/v1/livros/{test_book.id}",
        json={
            "titulo": "Updated Title",
            "autor": test_book.autor,
            "isbn": test_book.isbn,
            "quantidade": test_book.quantidade
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["data"]["titulo"] == "Updated Title"


def test_delete_pessoa(client, test_user):
    """Test deleting a person."""
    response = client.delete(f"/api/v1/pessoas/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    
    # Verify deletion
    response = client.get(f"/api/v1/pessoas/{test_user.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_livro(client, test_book):
    """Test deleting a book."""
    response = client.delete(f"/api/v1/livros/{test_book.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    
    # Verify deletion
    response = client.get(f"/api/v1/livros/{test_book.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND 