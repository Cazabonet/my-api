import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import get_settings
from app.database import Base, get_db
from app.main import app

settings = get_settings()

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db):
    """Create test user."""
    from app.models.pessoa import Pessoa
    
    user = Pessoa(
        nome="Test User",
        email="test@example.com",
        senha="test123",
        admin=True,
        ativo=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_book(db):
    """Create test book."""
    from app.models.livro import Livro
    
    book = Livro(
        titulo="Test Book",
        autor="Test Author",
        isbn="1234567890",
        quantidade=5
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@pytest.fixture(scope="function")
def test_loan(db, test_user, test_book):
    """Create test loan."""
    from app.models.emprestimo import Emprestimo
    from datetime import datetime, timedelta
    
    loan = Emprestimo(
        pessoa_id=test_user.id,
        livro_id=test_book.id,
        data_emprestimo=datetime.now(),
        data_devolucao=datetime.now() + timedelta(days=15),
        status="active"
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan 