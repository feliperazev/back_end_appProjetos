from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect

from model import Session, Projeto
from schemas import *

info = Info(title="API projetos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
projeto_tag = Tag(name="Projeto", description="Adição, visualização e remoção de projetos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/projeto', tags=[projeto_tag],
          responses={"200": ProjetoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProjetoSchema):
    """Adiciona um novo projeto à base de dados

    Retorna uma representação dos projetos.
    """
    projeto = Projeto(
        codigoProjeto=form.codigoProjeto,
        cliente=form.cliente,
        solicitante=form.solicitante,
        coordenador=form.coordenador,
        horasPrev=form.horasPrev,
        horasAcc=form.horasAcc,
        dataInicio=form.dataInicio,
        dataEntr=form.dataEntr
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionando projeto
        session.add(projeto)
        # efetivando o comando de adição do novo item na tabela
        session.commit()
        return apresenta_projeto(projeto), 200
    except IntegrityError as e:
        # como a duplicidade do código é a provável razão do IntegrityError
        error_msg = "Projeto de mesmo código já salvo na base :/"
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400


@app.get('/projetos', tags=[projeto_tag],
         responses={"200": ListagemProjetosSchema, "404": ErrorSchema})
def get_projetos():
    """Faz busca por todos os Projetos cadastrados

    Retorna um representação da listagem de projetos.
    """

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    projetos = session.query(Projeto).all()

    if not projetos:
        # se não há projetos cadastrados
        return {"projetos": []}, 200
    else:
        # retorna a representação de projeto
        print(projetos)
        return apresenta_projetos(projetos), 200
  
@app.put('/projeto', tags=[projeto_tag],
            responses={"200": ProjetoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_projeto(form: ProjetoSchema):
    """Edita o projeto de acordo com o código informado.

    """    
    projeto = Projeto(
        codigoProjeto=form.codigoProjeto,
        cliente=form.cliente,
        solicitante=form.solicitante,
        coordenador=form.coordenador,
        horasPrev=form.horasPrev,
        horasAcc=form.horasAcc,
        dataInicio=form.dataInicio,
        dataEntr=form.dataEntr
    )

    codigoProjeto = form.codigoProjeto
    
    try:
        # criando conexão com a base
        session = Session()
        
        # editando projeto
        session.query(Projeto).filter(Projeto.codigoProjeto == codigoProjeto).update(
        {"codigoProjeto": projeto.codigoProjeto,
         "cliente": form.cliente,
         "solicitante":form.solicitante,
         "coordenador":form.coordenador,
         "horasPrev":form.horasPrev,
         "horasAcc":form.horasAcc,
         "dataInicio":form.dataInicio,
         "dataEntr":form.dataEntr
         }, synchronize_session="fetch"
        )


        # efetivando o comando de adição do novo item na tabela
        session.commit()
        return apresenta_projeto(projeto), 200
    except IntegrityError as e:
        # como a duplicidade do código é a provável razão do IntegrityError
        error_msg = "Erro de edição :/"
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"message": error_msg}, 400


      

# @app.get('/projeto', tags=[projeto_tag],
#          responses={"200": ProjetoViewSchema, "404": ErrorSchema})
# def get_projeto(query: ProjetoBuscaSchema):
#     """Faz a busca por um Projeto a partir do código

#     Retorna uma representação do projeto.
#     """
#     codigoProjeto = query.codigoProjeto
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     projeto = session.query(Projeto).filter(Projeto.codigoProjeto == codigoProjeto).first()

#     if not projeto:
#         # se o projeto não foi encontrado
#         error_msg = "Projeto não encontrado na base :/"
#         return {"message": error_msg}, 404
#     else:
#         # retorna a representação de produto
#         return apresenta_projeto(projeto), 200


@app.delete('/projeto', tags=[projeto_tag],
            responses={"200": ProjetoDelSchema, "404": ErrorSchema})
def del_projeto(query: ProjetoBuscaSchema):
    """Deleta um Projeto a partir do código informado

    Retorna uma mensagem de confirmação da remoção.
    """
    codigoProjeto = query.codigoProjeto

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Projeto).filter(Projeto.codigoProjeto == codigoProjeto).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"message": "Projeto removido", "codigo": codigoProjeto}
    else:
        # se o projeto não foi encontrado
        error_msg = "Projeto não encontrado na base :/"
        return {"message": error_msg}, 404
