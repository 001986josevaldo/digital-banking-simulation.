from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)


class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    nome_titular = Column(String, nullable=False)
    
    # Em bancos, usamos Numeric para dinheiro para evitar erros de arredondamento do tipo Float
    saldo = Column(Numeric(precision=10, scale=2), default=0.00) 

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Chaves estrangeiras que ligam a transação às contas de origem e destino
    conta_origem_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    conta_destino_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    
    valor = Column(Numeric(precision=10, scale=2), nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="CONCLUIDA") # PENDENTE, CONCLUIDA, FALHOU

    # Relacionamentos (opcional, mas ajuda o SQLAlchemy a buscar os dados das contas facilmente)
    conta_origem = relationship("Conta", foreign_keys=[conta_origem_id])
    conta_destino = relationship("Conta", foreign_keys=[conta_destino_id])