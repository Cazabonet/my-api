from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
import enum
from datetime import datetime
from .base import BaseModel
from .mixins import TimestampMixin, SoftDeleteMixin, ValidationMixin


class TipoPessoa(enum.Enum):
    FUNCIONARIO = "funcionario"
    CLIENTE = "cliente"


class Pessoa(BaseModel, TimestampMixin, SoftDeleteMixin, ValidationMixin):
    """Base model for all people in the system."""
    __tablename__ = "pessoa"

    nome = Column(String(128), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    data_nascimento = Column(DateTime, nullable=False)
    email = Column(String(64), nullable=False)
    telefone = Column(String(11), nullable=False)
    endereco = Column(String(256), nullable=False)
    tipo = Column(Enum(TipoPessoa), nullable=False)
    ativo = Column(Boolean, default=True)
    
    # Relationships
    funcionario = relationship("Funcionario", back_populates="pessoa", uselist=False)
    cliente = relationship("Cliente", back_populates="pessoa", uselist=False)

    @validates('cpf')
    def validate_cpf(self, key, cpf):
        if not self.validate_cpf(cpf):
            raise ValueError("CPF inválido")
        return cpf

    @validates('email')
    def validate_email(self, key, email):
        if not self.validate_email(email):
            raise ValueError("Email inválido")
        return email

    @validates('telefone')
    def validate_telefone(self, key, telefone):
        if not self.validate_phone(telefone):
            raise ValueError("Telefone inválido")
        return telefone

    @hybrid_property
    def idade(self):
        """Calculate person's age."""
        today = datetime.utcnow()
        return (
            today.year - self.data_nascimento.year -
            ((today.month, today.day) <
             (self.data_nascimento.month, self.data_nascimento.day))
        )


class Funcionario(BaseModel, TimestampMixin):
    """Employee model."""
    __tablename__ = "funcionario"

    pessoa_id = Column(Integer, ForeignKey("pessoa.id"), nullable=False)
    cargo = Column(String(64), nullable=False)
    data_contratacao = Column(DateTime, nullable=False)
    salario = Column(String(10), nullable=False)
    matricula = Column(String(10), nullable=False, unique=True)
    
    # Relationships
    pessoa = relationship("Pessoa", back_populates="funcionario")
    emprestimos_processados = relationship("Emprestimo", back_populates="funcionario")

    @hybrid_property
    def tempo_servico(self):
        """Calculate employee's service time."""
        return (datetime.utcnow() - self.data_contratacao).days // 365


class Cliente(BaseModel, TimestampMixin, SoftDeleteMixin):
    """Client model."""
    __tablename__ = "cliente"

    pessoa_id = Column(Integer, ForeignKey("pessoa.id"), nullable=False)
    numero_cartao = Column(String(10), nullable=False, unique=True)
    data_adesao = Column(DateTime, default=datetime.utcnow)
    limite_emprestimos = Column(Integer, default=3)
    status = Column(String(32), default="ativo")
    
    # Relationships
    pessoa = relationship("Pessoa", back_populates="cliente")
    emprestimos = relationship("Emprestimo", back_populates="cliente")

    @hybrid_property
    def tempo_adesao(self):
        """Calculate client's membership time."""
        return (datetime.utcnow() - self.data_adesao).days

    def pode_emprestar(self):
        """Check if client can borrow books."""
        return (
            self.status == "ativo" and
            not self.is_deleted and
            len(self.emprestimos) < self.limite_emprestimos
        ) 