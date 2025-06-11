from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel
from .mixins import TimestampMixin


class TipoEvento(enum.Enum):
    """Event type enum."""
    PALESTRA = "palestra"
    WORKSHOP = "workshop"
    FEIRA = "feira"
    EXPOSICAO = "exposicao"
    CLUBE_LEITURA = "clube_leitura"
    OUTRO = "outro"


class StatusEvento(enum.Enum):
    """Event status enum."""
    AGENDADO = "agendado"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    ADIADO = "adiado"


class Evento(BaseModel, TimestampMixin):
    """Library event model."""
    __tablename__ = "evento"

    titulo = Column(String(128), nullable=False)
    descricao = Column(String(512), nullable=False)
    tipo = Column(Enum(TipoEvento), nullable=False)
    status = Column(
        Enum(StatusEvento),
        default=StatusEvento.AGENDADO,
        nullable=False
    )
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    local = Column(String(128), nullable=False)
    capacidade = Column(Integer, nullable=True)
    vagas_disponiveis = Column(Integer, nullable=True)
    valor_inscricao = Column(String(10), nullable=True)
    responsavel_id = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    publico_alvo = Column(String(256), nullable=True)
    requisitos = Column(String(512), nullable=True)
    material_necessario = Column(String(512), nullable=True)
    certificado = Column(Boolean, default=False)
    
    # Relationships
    responsavel = relationship("Funcionario", back_populates="eventos")
    inscricoes = relationship("InscricaoEvento", back_populates="evento")
    materiais = relationship("MaterialEvento", back_populates="evento")

    def __repr__(self):
        return f"<Evento {self.id} - {self.titulo}>"


class InscricaoEvento(BaseModel, TimestampMixin):
    """Event registration model."""
    __tablename__ = "inscricao_evento"

    evento_id = Column(Integer, ForeignKey("evento.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    data_inscricao = Column(DateTime, default=datetime.utcnow)
    status = Column(String(32), default="confirmada")  # confirmada, cancelada
    presenca = Column(Boolean, default=False)
    certificado_emitido = Column(Boolean, default=False)
    
    # Relationships
    evento = relationship("Evento", back_populates="inscricoes")
    cliente = relationship("Cliente", back_populates="inscricoes_eventos")

    def __repr__(self):
        return (
            f"<InscricaoEvento {self.id} - "
            f"Evento {self.evento_id} - "
            f"Cliente {self.cliente_id}>"
        )


class MaterialEvento(BaseModel, TimestampMixin):
    """Event material model."""
    __tablename__ = "material_evento"

    evento_id = Column(Integer, ForeignKey("evento.id"), nullable=False)
    titulo = Column(String(128), nullable=False)
    descricao = Column(String(512), nullable=True)
    tipo = Column(String(32), nullable=False)  # apresentacao, documento, video
    url = Column(String(256), nullable=True)
    arquivo = Column(String(256), nullable=True)
    
    # Relationships
    evento = relationship("Evento", back_populates="materiais")

    def __repr__(self):
        return (
            f"<MaterialEvento {self.id} - "
            f"Evento {self.evento_id}>"
        ) 