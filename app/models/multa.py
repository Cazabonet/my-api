from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel
from .mixins import TimestampMixin


class StatusMulta(enum.Enum):
    """Fine status enum."""
    PENDENTE = "pendente"
    PAGA = "paga"
    CANCELADA = "cancelada"
    PARCELADA = "parcelada"


class StatusPagamento(enum.Enum):
    """Payment status enum."""
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    ESTORNADO = "estornado"


class MetodoPagamento(enum.Enum):
    """Payment method enum."""
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    BOLETO = "boleto"
    TRANSFERENCIA = "transferencia"


class Multa(BaseModel, TimestampMixin):
    """Fine model."""
    __tablename__ = "multa"

    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    emprestimo_id = Column(Integer, ForeignKey("emprestimo.id"), nullable=False)
    valor = Column(Float, nullable=False)
    data_geracao = Column(DateTime, default=datetime.utcnow)
    data_vencimento = Column(DateTime, nullable=False)
    status = Column(
        Enum(StatusMulta),
        default=StatusMulta.PENDENTE,
        nullable=False
    )
    motivo = Column(String(256), nullable=False)
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    cliente = relationship("Cliente", back_populates="multas")
    emprestimo = relationship("Emprestimo", back_populates="multa")
    pagamentos = relationship("Pagamento", back_populates="multa")

    def __repr__(self):
        return (
            f"<Multa {self.id} - "
            f"Cliente {self.cliente_id}>"
        )


class Pagamento(BaseModel, TimestampMixin):
    """Payment model."""
    __tablename__ = "pagamento"

    multa_id = Column(Integer, ForeignKey("multa.id"), nullable=False)
    valor = Column(Float, nullable=False)
    data_pagamento = Column(DateTime, default=datetime.utcnow)
    metodo = Column(Enum(MetodoPagamento), nullable=False)
    status = Column(
        Enum(StatusPagamento),
        default=StatusPagamento.PENDENTE,
        nullable=False
    )
    comprovante = Column(String(256), nullable=True)
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    multa = relationship("Multa", back_populates="pagamentos")

    def __repr__(self):
        return (
            f"<Pagamento {self.id} - "
            f"Multa {self.multa_id}>"
        )


class Parcela(BaseModel, TimestampMixin):
    """Payment installment model."""
    __tablename__ = "parcela"

    multa_id = Column(Integer, ForeignKey("multa.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    data_vencimento = Column(DateTime, nullable=False)
    status = Column(
        Enum(StatusPagamento),
        default=StatusPagamento.PENDENTE,
        nullable=False
    )
    
    # Relationships
    multa = relationship("Multa", back_populates="parcelas")
    pagamento = relationship("Pagamento", back_populates="parcela")

    def __repr__(self):
        return (
            f"<Parcela {self.id} - "
            f"Multa {self.multa_id} - "
            f"Parcela {self.numero}>"
        ) 