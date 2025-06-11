from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from models.livro import (
    Livro, Exemplar, Emprestimo, LivroDanificado,
    LivroNaoDevolvido, StatusLivro, TipoDano
)
from business_rules.biblioteca import BibliotecaRules


class BibliotecaService:
    def __init__(self, db: Session):
        self.db = db
        self.rules = BibliotecaRules

    def emprestar_livro(
        self, exemplar_id: int, usuario_id: int
    ) -> Tuple[bool, str, Optional[Emprestimo]]:
        """Realiza o empréstimo de um livro."""
        # Verifica disponibilidade do exemplar
        if not self.rules.verificar_disponibilidade_exemplar(
            self.db, exemplar_id
        ):
            return False, "Exemplar não disponível", None

        # Verifica limite de empréstimos do usuário
        if not self.rules.verificar_limite_emprestimos(
            self.db, usuario_id
        ):
            return False, "Limite de empréstimos atingido", None

        # Cria o empréstimo
        emprestimo = Emprestimo(
            exemplar_id=exemplar_id,
            usuario_id=usuario_id,
            data_emprestimo=datetime.utcnow(),
            data_devolucao_prevista=self.rules.calcular_data_devolucao(),
            status=StatusLivro.EMPRESTADO
        )

        # Atualiza status do exemplar
        exemplar = self.db.query(Exemplar).filter(
            Exemplar.id == exemplar_id
        ).first()
        exemplar.disponivel = False

        self.db.add(emprestimo)
        self.db.commit()
        return True, "Empréstimo realizado com sucesso", emprestimo

    def devolver_livro(
        self, emprestimo_id: int
    ) -> Tuple[bool, str, Optional[float]]:
        """Realiza a devolução de um livro."""
        emprestimo = self.db.query(Emprestimo).filter(
            Emprestimo.id == emprestimo_id
        ).first()

        if not emprestimo:
            return False, "Empréstimo não encontrado", None

        if emprestimo.status != StatusLivro.EMPRESTADO:
            return False, "Empréstimo não está ativo", None

        # Calcula multa se houver atraso
        multa = self.rules.calcular_multa(
            emprestimo.data_devolucao_prevista
        )

        # Atualiza status
        emprestimo.status = StatusLivro.DISPONIVEL
        emprestimo.data_devolucao_real = datetime.utcnow()
        emprestimo.exemplar.disponivel = True

        self.db.commit()
        return True, "Devolução realizada com sucesso", multa

    def renovar_emprestimo(
        self, emprestimo_id: int
    ) -> Tuple[bool, str]:
        """Renova um empréstimo."""
        pode_renovar, mensagem = self.rules.verificar_renovacao(
            self.db, emprestimo_id
        )
        
        if not pode_renovar:
            return False, mensagem

        emprestimo = self.db.query(Emprestimo).filter(
            Emprestimo.id == emprestimo_id
        ).first()

        emprestimo.data_devolucao_prevista = self.rules.calcular_data_devolucao()
        emprestimo.numero_renovacoes += 1

        self.db.commit()
        return True, "Renovação realizada com sucesso"

    def registrar_dano(
        self,
        exemplar_id: int,
        tipo_dano: TipoDano,
        descricao: str,
        custo_reparo: Optional[float] = None
    ) -> Tuple[bool, str, Optional[LivroDanificado]]:
        """Registra dano em um exemplar."""
        try:
            dano = self.rules.registrar_dano(
                self.db,
                exemplar_id,
                tipo_dano,
                descricao,
                custo_reparo
            )
            return True, "Dano registrado com sucesso", dano
        except ValueError as e:
            return False, str(e), None

    def registrar_nao_devolucao(
        self, emprestimo_id: int
    ) -> Tuple[bool, str, Optional[LivroNaoDevolvido]]:
        """Registra não devolução de um livro."""
        try:
            nao_devolvido = self.rules.registrar_nao_devolucao(
                self.db,
                emprestimo_id
            )
            return True, "Não devolução registrada com sucesso", nao_devolvido
        except ValueError as e:
            return False, str(e), None

    def listar_emprestimos_ativos(
        self, usuario_id: Optional[int] = None
    ) -> List[Emprestimo]:
        """Lista empréstimos ativos."""
        query = self.db.query(Emprestimo).filter(
            Emprestimo.status == StatusLivro.EMPRESTADO
        )
        
        if usuario_id:
            query = query.filter(Emprestimo.usuario_id == usuario_id)
            
        return query.all()

    def listar_livros_danificados(
        self, reparavel: Optional[bool] = None
    ) -> List[LivroDanificado]:
        """Lista livros danificados."""
        query = self.db.query(LivroDanificado)
        
        if reparavel is not None:
            query = query.filter(LivroDanificado.reparavel == reparavel)
            
        return query.all()

    def listar_livros_nao_devolvidos(
        self, status: Optional[str] = None
    ) -> List[LivroNaoDevolvido]:
        """Lista livros não devolvidos."""
        query = self.db.query(LivroNaoDevolvido)
        
        if status:
            query = query.filter(LivroNaoDevolvido.status == status)
            
        return query.all() 