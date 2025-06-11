from repositories import empresa_repository
from models.empresa import Empresa

def criar_empresa(db, empresa_data):
    # Regra de negócio: impedir duplicidade de CNPJ
    if empresa_repository.get_by_cnpj(db, empresa_data.cnpj):
        raise ValueError("Empresa com este CNPJ já existe")

    nova_empresa = Empresa(**empresa_data.dict())
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa
