from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel
from .mixins import TimestampMixin


class StatusReserva(enum.Enum):
    """Reservation status enum."""
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluida"
    EXPIRADA = "expirada"


class Reserva(BaseModel, TimestampMixin):
    """Book reservation model."""
    __tablename__ = "reserva"

    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    data_reserva = Column(DateTime, default=datetime.utcnow)
    data_limite = Column(DateTime, nullable=False)
    data_notificacao = Column(DateTime, nullable=True)
    status = Column(
        Enum(StatusReserva),
        default=StatusReserva.PENDENTE,
        nullable=False
    )
    prioridade = Column(Integer, default=1)  # 1-5, onde 5 é a maior prioridade
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    livro = relationship("Livro", back_populates="reservas")
    cliente = relationship("Cliente", back_populates="reservas")
    notificacoes = relationship(
        "NotificacaoReserva",
        back_populates="reserva"
    )

    def __repr__(self):
        return (
            f"<Reserva {self.id} - "
            f"Livro {self.livro_id} - "
            f"Cliente {self.cliente_id}>"
        )


class NotificacaoReserva(BaseModel, TimestampMixin):
    """Reservation notification model."""
    __tablename__ = "notificacao_reserva"

    reserva_id = Column(Integer, ForeignKey("reserva.id"), nullable=False)
    tipo = Column(String(32), nullable=False)  # email, sms, push
    mensagem = Column(String(512), nullable=False)
    data_envio = Column(DateTime, default=datetime.utcnow)
    status = Column(String(32), default="pendente")  # pendente, enviada, falha
    
    # Relationships
    reserva = relationship("Reserva", back_populates="notificacoes")

    def __repr__(self):
        return (
            f"<NotificacaoReserva {self.id} - "
            f"Reserva {self.reserva_id}>"
        ) 