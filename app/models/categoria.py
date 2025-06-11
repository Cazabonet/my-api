from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel
from .mixins import TimestampMixin


# Association tables
livro_categoria = Table(
    'livro_categoria',
    BaseModel.metadata,
    Column(
        'livro_id',
        Integer,
        ForeignKey('livro.id'),
        primary_key=True
    ),
    Column(
        'categoria_id',
        Integer,
        ForeignKey('categoria.id'),
        primary_key=True
    )
)

livro_tag = Table(
    'livro_tag',
    BaseModel.metadata,
    Column(
        'livro_id',
        Integer,
        ForeignKey('livro.id'),
        primary_key=True
    ),
    Column(
        'tag_id',
        Integer,
        ForeignKey('tag.id'),
        primary_key=True
    )
)


class Categoria(BaseModel, TimestampMixin):
    """Book category model."""
    __tablename__ = "categoria"

    nome = Column(String(64), nullable=False, unique=True)
    descricao = Column(String(256), nullable=True)
    codigo = Column(String(10), nullable=False, unique=True)  # Código de classificação
    categoria_pai_id = Column(Integer, ForeignKey('categoria.id'), nullable=True)
    
    # Relationships
    livros = relationship(
        "Livro",
        secondary=livro_categoria,
        back_populates="categorias"
    )
    subcategorias = relationship(
        "Categoria",
        backref="categoria_pai",
        remote_side=[id]
    )

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Tag(BaseModel, TimestampMixin):
    """Book tag model."""
    __tablename__ = "tag"

    nome = Column(String(32), nullable=False, unique=True)
    descricao = Column(String(128), nullable=True)
    cor = Column(String(7), nullable=True)  # Código hexadecimal da cor
    
    # Relationships
    livros = relationship(
        "Livro",
        secondary=livro_tag,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.nome}>"


class Classificacao(BaseModel, TimestampMixin):
    """Book classification model (CDD, CDU, etc)."""
    __tablename__ = "classificacao"

    codigo = Column(String(10), nullable=False, unique=True)
    descricao = Column(String(256), nullable=False)
    tipo = Column(String(32), nullable=False)  # CDD, CDU, etc
    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=True)
    
    # Relationships
    categoria = relationship("Categoria", backref="classificacoes")
    livros = relationship("Livro", back_populates="classificacao")

    def __repr__(self):
        return f"<Classificacao {self.codigo}>" 