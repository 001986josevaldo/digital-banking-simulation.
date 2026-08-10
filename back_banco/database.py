from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define onde o banco de dados será salvo (neste caso, um arquivo chamado banco.db)
#SQLALCHEMY_DATABASE_URL = "sqlite:///./banco.db"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres.tkobjirhdgpnawtxsrno:bancoSimulador@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

# O engine é o motor que gerencia a conexão com o banco
"""engine = create_engine(
    # check_same_thread é necessário apenas para o SQLite
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)"""
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# A SessionLocal é o que usaremos para fazer queries (buscar, salvar, atualizar)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A classe Base será herdada por todos os nossos modelos (tabelas)
Base = declarative_base()