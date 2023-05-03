from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.projeto import Projeto


db_path = "database/"
# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # Então cria o diretório
    os.makedirs(db_path)

# URL de acesso ao banco
db_url = 'sqlite:///%s/data_base.sqlite3' %db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(engine)


# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
