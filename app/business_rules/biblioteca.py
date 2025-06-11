from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from models.livro import (
    Livro, Exemplar, Emprestimo, LivroDanificado, 
    LivroNaoDevolvido, StatusLivro, TipoDano
)


class BibliotecaRules:
    # Constants
    DIAS_EMPRESTIMO = 15
    DIAS_RENOVACAO = 15
    MAX_RENOVACOES = 2
    MULTA_POR_DIA = 1.0
    MAX_LIVROS_EMPRESTADOS = 3

    @staticmethod
    def calcular_data_devolucao() -> datetime:
        """Calculate the expected return date based on business rules."""
        return datetime.utcnow() + timedelta(days=BibliotecaRules.DIAS_EMPRESTIMO)

    @staticmethod
    def calcular_multa(data_vencimento: datetime) -> float:
        """Calculate the fine amount for late returns."""
        dias_atraso = (datetime.utcnow() - data_vencimento).days
        if dias_atraso <= 0:
            return 0.0
        return dias_atraso * BibliotecaRules.MULTA_POR_DIA

    @staticmethod
    def verificar_disponibilidade_exemplar(
        db: Session, exemplar_id: int
    ) -> bool:
        """Check if a book copy is available for loan."""
        exemplar = db.query(Exemplar).filter(Exemplar.id == exemplar_id).first()
        if not exemplar:
            return False
        return exemplar.disponivel

    @staticmethod
    def verificar_limite_emprestimos(
        db: Session, usuario_id: int
    ) -> bool:
        """Check if user has reached the maximum number of active loans."""
        emprestimos_ativos = db.query(Emprestimo).filter(
            Emprestimo.usuario_id == usuario_id,
            Emprestimo.status == StatusLivro.EMPRESTADO
        ).count()
        return emprestimos_ativos < BibliotecaRules.MAX_LIVROS_EMPRESTADOS

    @staticmethod
    def verificar_renovacao(
        db: Session, emprestimo_id: int
    ) -> tuple[bool, str]:
        """Check if a loan can be renewed."""
        emprestimo = db.query(Emprestimo).filter(
            Emprestimo.id == emprestimo_id
        ).first()
        
        if not emprestimo:
            return False, "Empréstimo não encontrado"
            
        if emprestimo.numero_renovacoes >= BibliotecaRules.MAX_RENOVACOES:
            return False, "Número máximo de renovações atingido"
            
        if emprestimo.status != StatusLivro.EMPRESTADO:
            return False, "Empréstimo não está ativo"
            
        return True, "Renovação permitida"

    @staticmethod
    def registrar_dano(
        db: Session,
        exemplar_id: int,
        tipo_dano: TipoDano,
        descricao: str,
        custo_reparo: Optional[float] = None
    ) -> LivroDanificado:
        """Register a new book damage."""
        exemplar = db.query(Exemplar).filter(Exemplar.id == exemplar_id).first()
        if not exemplar:
            raise ValueError("Exemplar não encontrado")

        dano = LivroDanificado(
            livro_id=exemplar.livro_id,
            exemplar_id=exemplar_id,
            tipo_dano=tipo_dano,
            descricao_dano=descricao,
            custo_reparo=custo_reparo
        )
        
        exemplar.disponivel = False
        db.add(dano)
        db.commit()
        return dano

    @staticmethod
    def registrar_nao_devolucao(
        db: Session,
        emprestimo_id: int
    ) -> LivroNaoDevolvido:
        """Register a non-returned book."""
        emprestimo = db.query(Emprestimo).filter(
            Emprestimo.id == emprestimo_id
        ).first()
        
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado")
            
        if emprestimo.status != StatusLivro.EMPRESTADO:
            raise ValueError("Empréstimo não está ativo")

        nao_devolvido = LivroNaoDevolvido(
            livro_id=emprestimo.exemplar.livro_id,
            exemplar_id=emprestimo.exemplar_id,
            emprestimo_id=emprestimo_id,
            data_vencimento=emprestimo.data_devolucao_prevista,
            multa=BibliotecaRules.calcular_multa(
                emprestimo.data_devolucao_prevista
            )
        )
        
        emprestimo.status = StatusLivro.NAO_DEVOLVIDO
        emprestimo.exemplar.disponivel = False
        db.add(nao_devolvido)
        db.commit()
        return nao_devolvido 