from database import engine, Base
import models # Importante importar os modelos para que o Base os conheça

def inicializar_banco():
    print("Criando o banco de dados e as tabelas...")
    # Este comando lê tudo o que herda de 'Base' e cria no banco de dados
    Base.metadata.create_all(bind=engine)
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    inicializar_banco()