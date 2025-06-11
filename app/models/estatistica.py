from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Enum, Float, JSON, Boolean
)
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel
from .mixins import TimestampMixin


class TipoEstatistica(enum.Enum):
    """Statistics type enum."""
    EMPRESTIMOS = "emprestimos"
    DEVOLUCOES = "devolucoes"
    MULTAS = "multas"
    RESERVAS = "reservas"
    EVENTOS = "eventos"
    USUARIOS = "usuarios"
    LIVROS = "livros"
    FINANCEIRO = "financeiro"


class PeriodoEstatistica(enum.Enum):
    """Statistics period enum."""
    DIARIO = "diario"
    SEMANAL = "semanal"
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    ANUAL = "anual"


class Estatistica(BaseModel, TimestampMixin):
    """Statistics model."""
    __tablename__ = "estatistica"

    tipo = Column(Enum(TipoEstatistica), nullable=False)
    periodo = Column(Enum(PeriodoEstatistica), nullable=False)
    data_referencia = Column(DateTime, nullable=False)
    valor = Column(Float, nullable=False)
    detalhes = Column(JSON, nullable=True)
    gerado_por = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    
    # Relationships
    funcionario = relationship("Funcionario", back_populates="estatisticas")

    def __repr__(self):
        return (
            f"<Estatistica {self.id} - "
            f"{self.tipo.value} - "
            f"{self.periodo.value}>"
        )


class Relatorio(BaseModel, TimestampMixin):
    """Report model."""
    __tablename__ = "relatorio"

    titulo = Column(String(128), nullable=False)
    tipo = Column(String(32), nullable=False)
    periodo_inicio = Column(DateTime, nullable=False)
    periodo_fim = Column(DateTime, nullable=False)
    parametros = Column(JSON, nullable=True)
    resultado = Column(JSON, nullable=True)
    gerado_por = Column(
        Integer, ForeignKey("funcionario.id"), nullable=False
    )
    status = Column(String(32), default="pendente")
    
    # Relationships
    funcionario = relationship("Funcionario", back_populates="relatorios")

    def __repr__(self):
        return f"<Relatorio {self.id} - {self.titulo}>"


class Dashboard(BaseModel, TimestampMixin):
    """Dashboard model."""
    __tablename__ = "dashboard"

    titulo = Column(String(128), nullable=False)
    descricao = Column(String(512), nullable=True)
    configuracao = Column(JSON, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_por = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    
    # Relationships
    funcionario = relationship("Funcionario", back_populates="dashboards")

    def __repr__(self):
        return f"<Dashboard {self.id} - {self.titulo}>" 