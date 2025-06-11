import pytest
from datetime import datetime, timedelta
from app.models.pessoa import Pessoa
from app.models.livro import Livro, Exemplar
from app.models.emprestimo import Emprestimo
from app.models.reserva import Reserva
from app.core.constants import BookStatus, LoanStatus, ReservationStatus


def test_create_pessoa(db):
    """Test creating a person."""
    pessoa = Pessoa(
        nome="John Doe",
        email="john@example.com",
        senha="password123",
        admin=False,
        ativo=True
    )
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    
    assert pessoa.id is not None
    assert pessoa.nome == "John Doe"
    assert pessoa.email == "john@example.com"
    assert pessoa.admin is False
    assert pessoa.ativo is True


def test_create_livro(db):
    """Test creating a book."""
    livro = Livro(
        titulo="Test Book",
        autor="Test Author",
        isbn="1234567890",
        quantidade=5
    )
    db.add(livro)
    db.commit()
    db.refresh(livro)
    
    assert livro.id is not None
    assert livro.titulo == "Test Book"
    assert livro.autor == "Test Author"
    assert livro.isbn == "1234567890"
    assert livro.quantidade == 5


def test_create_exemplar(db, test_book):
    """Test creating a book copy."""
    exemplar = Exemplar(
        livro_id=test_book.id,
        codigo="EX001",
        status=BookStatus.AVAILABLE
    )
    db.add(exemplar)
    db.commit()
    db.refresh(exemplar)
    
    assert exemplar.id is not None
    assert exemplar.livro_id == test_book.id
    assert exemplar.codigo == "EX001"
    assert exemplar.status == BookStatus.AVAILABLE


def test_create_emprestimo(db, test_user, test_book):
    """Test creating a loan."""
    data_emprestimo = datetime.now()
    data_devolucao = data_emprestimo + timedelta(days=15)
    
    emprestimo = Emprestimo(
        pessoa_id=test_user.id,
        livro_id=test_book.id,
        data_emprestimo=data_emprestimo,
        data_devolucao=data_devolucao,
        status=LoanStatus.ACTIVE
    )
    db.add(emprestimo)
    db.commit()
    db.refresh(emprestimo)
    
    assert emprestimo.id is not None
    assert emprestimo.pessoa_id == test_user.id
    assert emprestimo.livro_id == test_book.id
    assert emprestimo.data_emprestimo == data_emprestimo
    assert emprestimo.data_devolucao == data_devolucao
    assert emprestimo.status == LoanStatus.ACTIVE


def test_create_reserva(db, test_user, test_book):
    """Test creating a reservation."""
    data_reserva = datetime.now()
    data_expiracao = data_reserva + timedelta(days=7)
    
    reserva = Reserva(
        pessoa_id=test_user.id,
        livro_id=test_book.id,
        data_reserva=data_reserva,
        data_expiracao=data_expiracao,
        status=ReservationStatus.PENDING
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    
    assert reserva.id is not None
    assert reserva.pessoa_id == test_user.id
    assert reserva.livro_id == test_book.id
    assert reserva.data_reserva == data_reserva
    assert reserva.data_expiracao == data_expiracao
    assert reserva.status == ReservationStatus.PENDING 