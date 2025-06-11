from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel
from .mixins import TimestampMixin


class Avaliacao(BaseModel, TimestampMixin):
    """Book rating model."""
    __tablename__ = "avaliacao"

    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    nota = Column(Integer, nullable=False)  # 1-5
    comentario = Column(String(512), nullable=True)
    data_avaliacao = Column(DateTime, default=datetime.utcnow)
    status = Column(String(32), default="ativo")  # ativo, moderado, removido
    
    # Relationships
    livro = relationship("Livro", back_populates="avaliacoes")
    cliente = relationship("Cliente", back_populates="avaliacoes")
    respostas = relationship(
        "RespostaAvaliacao",
        back_populates="avaliacao"
    )

    def __repr__(self):
        return f"<Avaliacao {self.id} - Livro {self.livro_id}>"


class RespostaAvaliacao(BaseModel, TimestampMixin):
    """Rating response model."""
    __tablename__ = "resposta_avaliacao"

    avaliacao_id = Column(Integer, ForeignKey("avaliacao.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionario.id"), nullable=False)
    resposta = Column(String(512), nullable=False)
    data_resposta = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    avaliacao = relationship("Avaliacao", back_populates="respostas")
    funcionario = relationship(
        "Funcionario",
        back_populates="respostas_avaliacoes"
    )

    def __repr__(self):
        return (
            f"<RespostaAvaliacao {self.id} - "
            f"Avaliacao {self.avaliacao_id}>"
        )


class DenunciaAvaliacao(BaseModel, TimestampMixin):
    """Rating report model."""
    __tablename__ = "denuncia_avaliacao"

    avaliacao_id = Column(Integer, ForeignKey("avaliacao.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    motivo = Column(String(256), nullable=False)
    descricao = Column(String(512), nullable=True)
    status = Column(String(32), default="pendente")  # pendente, analisada, rejeitada
    
    # Relationships
    avaliacao = relationship("Avaliacao")
    cliente = relationship("Cliente", back_populates="denuncias")

    def __repr__(self):
        return (
            f"<DenunciaAvaliacao {self.id} - "
            f"Avaliacao {self.avaliacao_id}>"
        ) 