from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import BaseModel
from .mixins import TimestampMixin


class TipoNotificacao(enum.Enum):
    """Notification type enum."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SISTEMA = "sistema"


class StatusNotificacao(enum.Enum):
    """Notification status enum."""
    PENDENTE = "pendente"
    ENVIADA = "enviada"
    FALHA = "falha"
    CANCELADA = "cancelada"


class PrioridadeNotificacao(enum.Enum):
    """Notification priority enum."""
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class Notificacao(BaseModel, TimestampMixin):
    """Notification model."""
    __tablename__ = "notificacao"

    destinatario_id = Column(Integer, ForeignKey("pessoa.id"), nullable=False)
    tipo = Column(Enum(TipoNotificacao), nullable=False)
    status = Column(
        Enum(StatusNotificacao),
        default=StatusNotificacao.PENDENTE,
        nullable=False
    )
    prioridade = Column(
        Enum(PrioridadeNotificacao),
        default=PrioridadeNotificacao.MEDIA,
        nullable=False
    )
    titulo = Column(String(128), nullable=False)
    mensagem = Column(String(512), nullable=False)
    data_envio = Column(DateTime, nullable=True)
    data_leitura = Column(DateTime, nullable=True)
    tentativas = Column(Integer, default=0)
    erro = Column(String(256), nullable=True)
    
    # Relationships
    destinatario = relationship("Pessoa", back_populates="notificacoes")

    def __repr__(self):
        return (
            f"<Notificacao {self.id} - "
            f"Destinatario {self.destinatario_id}>"
        )


class TemplateNotificacao(BaseModel, TimestampMixin):
    """Notification template model."""
    __tablename__ = "template_notificacao"

    codigo = Column(String(32), nullable=False, unique=True)
    tipo = Column(Enum(TipoNotificacao), nullable=False)
    titulo = Column(String(128), nullable=False)
    corpo = Column(String(1024), nullable=False)
    variaveis = Column(String(256), nullable=True)  # Lista de variáveis separadas por vírgula
    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<TemplateNotificacao {self.id} - {self.codigo}>"


class ConfiguracaoNotificacao(BaseModel, TimestampMixin):
    """Notification configuration model."""
    __tablename__ = "configuracao_notificacao"

    pessoa_id = Column(Integer, ForeignKey("pessoa.id"), nullable=False)
    tipo = Column(Enum(TipoNotificacao), nullable=False)
    ativo = Column(Boolean, default=True)
    preferencia = Column(String(256), nullable=True)  # Configurações específicas do tipo
    
    # Relationships
    pessoa = relationship("Pessoa", back_populates="configuracoes_notificacao")

    def __repr__(self):
        return (
            f"<ConfiguracaoNotificacao {self.id} - "
            f"Pessoa {self.pessoa_id}>"
        ) 