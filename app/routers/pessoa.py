from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models.pessoa import Pessoa, Funcionario, Cliente
from routers.base import BaseRouter


# Schemas
class PessoaBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: datetime
    email: str
    telefone: str
    endereco: str
    tipo: str


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(PessoaBase):
    nome: str | None = None
    cpf: str | None = None
    data_nascimento: datetime | None = None
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None
    tipo: str | None = None
    ativo: bool | None = None


class PessoaResponse(PessoaBase):
    id: int
    ativo: bool
    data_cadastro: datetime

    class Config:
        orm_mode = True


# Router
class PessoaRouter(BaseRouter[Pessoa, PessoaCreate, PessoaUpdate, PessoaResponse]):
    def __init__(self):
        super().__init__(
            model=Pessoa,
            create_schema=PessoaCreate,
            update_schema=PessoaUpdate,
            response_schema=PessoaResponse,
            prefix="/pessoas",
            tags=["pessoas"]
        )
        self._setup_custom_routes()

    def _setup_custom_routes(self):
        """Setup custom routes for Pessoa."""
        
        @self.router.get("/buscar/cpf/{cpf}", response_model=PessoaResponse)
        async def buscar_por_cpf(
            cpf: str,
            db: Session = Depends(get_db)
        ):
            """Buscar pessoa por CPF."""
            pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
            if not pessoa:
                raise HTTPException(
                    status_code=404,
                    detail=f"Pessoa com CPF {cpf} não encontrada"
                )
            return pessoa

        @self.router.get("/buscar/nome", response_model=List[PessoaResponse])
        async def buscar_por_nome(
            nome: str = Query(..., min_length=3),
            db: Session = Depends(get_db)
        ):
            """Buscar pessoas por nome."""
            pessoas = db.query(Pessoa).filter(
                Pessoa.nome.ilike(f"%{nome}%")
            ).all()
            return pessoas

        @self.router.get("/funcionarios", response_model=List[PessoaResponse])
        async def listar_funcionarios(
            db: Session = Depends(get_db)
        ):
            """Listar todos os funcionários."""
            return db.query(Pessoa).filter(
                Pessoa.tipo == "funcionario"
            ).all()

        @self.router.get("/clientes", response_model=List[PessoaResponse])
        async def listar_clientes(
            db: Session = Depends(get_db)
        ):
            """Listar todos os clientes."""
            return db.query(Pessoa).filter(
                Pessoa.tipo == "cliente"
            ).all()

        @self.router.post("/{pessoa_id}/desativar")
        async def desativar_pessoa(
            pessoa_id: int,
            db: Session = Depends(get_db)
        ):
            """Desativar uma pessoa."""
            pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
            if not pessoa:
                raise HTTPException(
                    status_code=404,
                    detail=f"Pessoa com id {pessoa_id} não encontrada"
                )
            
            pessoa.ativo = False
            db.commit()
            return {"message": "Pessoa desativada com sucesso"}


# Router instance
pessoa_router = PessoaRouter().get_router() 