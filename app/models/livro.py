from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime


class StatusLivro(enum.Enum):
    RECEBIDO = "recebido"
    PERDIDO = "perdido"
    EMPRESTADO = "emprestado"
    DISPONIVEL = "disponivel"
    DANIFICADO = "danificado"
    NAO_DEVOLVIDO = "nao_devolvido"


class MotivoPerda(enum.Enum):
    NAO_DEVOLVIDO = "nao_devolvido"
    DANIFICADO = "danificado"
    ROUBO = "roubo"
    EXTRAVIO = "extravio"
    OUTRO = "outro"


class TipoDano(enum.Enum):
    FOLHAS_RASGADAS = "folhas_rasgadas"
    CAPA_DANIFICADA = "capa_danificada"
    PAGINAS_MANCHADAS = "paginas_manchadas"
    ENCADERNACAO = "encadernacao"
    OUTRO = "outro"


class Livro(Base):
    __tablename__ = "livro"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(128), nullable=False)
    autor = Column(String(128), nullable=False)
    isbn = Column(String(13), nullable=True)
    editora = Column(String(128), nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    descricao = Column(String(512), nullable=True)
    
    # Relationships
    exemplares = relationship("Exemplar", back_populates="livro")
    historico = relationship("HistoricoLivro", back_populates="livro")
    livros_danificados = relationship("LivroDanificado", back_populates="livro")
    livros_nao_devolvidos = relationship("LivroNaoDevolvido", back_populates="livro")


class Exemplar(Base):
    __tablename__ = "exemplar"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    numero_exemplar = Column(Integer, nullable=False)
    disponivel = Column(Boolean, default=True)
    localizacao = Column(String(64), nullable=True)
    
    # Relationships
    livro = relationship("Livro", back_populates="exemplares")
    emprestimos = relationship("Emprestimo", back_populates="exemplar")
    exemplares_danificados = relationship("LivroDanificado", back_populates="exemplar")
    exemplares_nao_devolvidos = relationship("LivroNaoDevolvido", back_populates="exemplar")


class HistoricoLivro(Base):
    __tablename__ = "historico_livro"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    data_evento = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo_evento = Column(Enum(StatusLivro), nullable=False)
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    livro = relationship("Livro", back_populates="historico")


class Emprestimo(Base):
    __tablename__ = "emprestimo"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    exemplar_id = Column(Integer, ForeignKey("exemplar.id"), nullable=False)
    data_emprestimo = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_devolucao_prevista = Column(DateTime, nullable=False)
    data_devolucao_real = Column(DateTime, nullable=True)
    status = Column(Enum(StatusLivro), default=StatusLivro.EMPRESTADO, nullable=False)
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    exemplar = relationship("Exemplar", back_populates="emprestimos")


class LivroDanificado(Base):
    __tablename__ = "livro_danificado"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    exemplar_id = Column(Integer, ForeignKey("exemplar.id"), nullable=False)
    data_dano = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo_dano = Column(Enum(TipoDano), nullable=False)
    descricao_dano = Column(String(512), nullable=False)
    custo_reparo = Column(Float, nullable=True)
    reparavel = Column(Boolean, default=True)
    data_reparo = Column(DateTime, nullable=True)
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    livro = relationship("Livro", back_populates="livros_danificados")
    exemplar = relationship("Exemplar", back_populates="exemplares_danificados")


class LivroNaoDevolvido(Base):
    __tablename__ = "livro_nao_devolvido"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey("livro.id"), nullable=False)
    exemplar_id = Column(Integer, ForeignKey("exemplar.id"), nullable=False)
    emprestimo_id = Column(Integer, ForeignKey("emprestimo.id"), nullable=False)
    data_vencimento = Column(DateTime, nullable=False)
    data_notificacao = Column(DateTime, nullable=True)
    multa = Column(Float, nullable=True)
    status = Column(String(32), default="pendente", nullable=False)
    observacao = Column(String(512), nullable=True)
    
    # Relationships
    livro = relationship("Livro", back_populates="livros_nao_devolvidos")
    exemplar = relationship("Exemplar", back_populates="exemplares_nao_devolvidos")
    emprestimo = relationship("Emprestimo") 