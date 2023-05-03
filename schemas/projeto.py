from pydantic import BaseModel
from typing import Optional, List, Union
from model.projeto import Projeto
from datetime import date, datetime


class ProjetoSchema(BaseModel):
    """Define como um novo projeto a ser inserido deve ser representado
    """

    codigoProjeto: str
    cliente: str
    solicitante: str
    coordenador: Optional[str]
    horasPrev: Optional[int]
    horasAcc: Optional[int]
    dataInicio: Optional[date] 
    dataEntr: Optional[date]
    

class ProjetoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Que será feita apenas com base no código do projeto.
    
    """
    codigoProjeto: str

class ListagemProjetosSchema(BaseModel):
    """Define como uma listagem de projetos será retornada.
    
    """
    projetos: List[ProjetoSchema]


def apresenta_projetos(projetos: List[Projeto]):
    """Retorna uma apresentação do projeto seguindo o schema definido em ProjetoViewSchema
    """
    result = []
    for projeto in projetos:
        result.append({
            "codigoProjeto": projeto.codigoProjeto,
            "cliente": projeto.cliente,
            "solicitante": projeto.solicitante,
            "coordenador": projeto.coordenador,
            "horasPrev": projeto.horasPrev,
            "horasAcc": projeto.horasAcc,
            "dataInicio": projeto.dataInicio,
            "dataEntr": projeto.dataEntr,
            "dataInsercao": projeto.dataInsercao
        })

    return {"projetos": result}


class ProjetoViewSchema(BaseModel):
    """Define como um projeto será retornado.
    """

    codigoProjeto: str
    cliente: str
    solicitante: str
    coordenador: Optional[str]
    horasPrev: Optional[float]
    horasAcc: Optional[float]
    dataInicio: Optional[date]
    dataEntr: Optional[date]
    dataInsercao: datetime


class ProjetoDelSchema(BaseModel):
    """Define como dever ser a estrutura do dado retornado após uma requisição de remoção.
    """
    message: str
    codigo_projeto: str

def apresenta_projeto(projeto: Projeto):
    """Retorna uma representação do projeto seguindo o schema definifo em 
       ProjetoViewSchema.
    """
    return {
            "codigoProjeto": projeto.codigoProjeto,
            "cliente": projeto.cliente,
            "solicitante": projeto.solicitante,
            "coordenador": projeto.coordenador,
            "horasPrev": projeto.horasPrev,
            "horasAcc": projeto.horasAcc,
            "dataInicio": projeto.dataInicio,
            "dataEntr": projeto.dataEntr,
            "dataInsercao": projeto.dataInsercao
    }