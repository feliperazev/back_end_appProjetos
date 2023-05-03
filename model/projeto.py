from sqlalchemy import Column, String, Integer, DateTime, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from typing import Union

from model import Base

class Projeto(Base):
    __tablename__ = 'projeto'

    id = Column("pk_projeto", Integer, primary_key=True)
    codigoProjeto = Column(String, unique = True)
    cliente = Column(String)
    solicitante = Column(String)
    coordenador = Column(String)
    horasPrev = Column(Float)
    horasAcc = Column(Float)
    dataInicio = Column(Date, default=date.today())
    dataEntr = Column(Date)
    dataInsercao =  Column(DateTime, default=datetime.now())

    
    def __init__(self, codigoProjeto, cliente, solicitante, coordenador, horasPrev, horasAcc, dataInicio, dataEntr):
        """
        Cria um projeto

        Arguments:
        codigoProjeto = Série de letras que identificam um projeto de acordo com cliente;
        cliente = Empresa compradora do projeto;
        solicitante = Responsável técnico do cliente;
        coordenador = Coordenador interno do projeto;
        HorasPrev = Horas previstas totais de execução do projeto;
        HorasAcc = Horas acumuladas totais de execução do projeto;
        dataInicio = Data de criação do projeto e início das atividades;
        dataEntr = Data de entrega do projeto;
        dataInsercao = Data de registro na base;
        """
        self.codigoProjeto = codigoProjeto
        self.cliente = cliente
        self.solicitante = solicitante
        self.coordenador = coordenador
        self.horasPrev = horasPrev
        self.horasAcc = horasAcc
        # se não for informada, será o data exata da inserção no banco
        if dataInicio:
            self.dataInicio = dataInicio
        self.dataEntr = dataEntr
        
        
