from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
import auth # Importa o módulo de autenticação

from fastapi.middleware.cors import CORSMiddleware


import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
# Cria a aplicação FastAPI
app = FastAPI(title="API Bancária", description="Sistema de transferências e contas")
# Configuração de CORS para permitir que o frontend converse com a API
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["*"], # Permite acesso de qualquer origem (ideal apenas para testes locais)
    # Permite acesso apenas do frontend hospedado no Vercel
    allow_origins=["http://digital-banking-simulation-innrpdjes-001986josevaldos-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API do Banco! Acesse http://127.0.0.1:8000/docs para testar as rotas.",
            "instruções": "Entre com login e senha para criar uma conta, consultar saldo e realizar transferências."}

# Dependência do FastAPI: Abre e fecha a conexão com o banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota: Criar usuário e Conta Bancária simultaneamente
@app.post("/usuarios/", response_model=schemas.UserResponse, status_code=201)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se já existe usuário com esse nome
    usuario_existente = db.query(models.User).filter(models.User.nome == user.nome).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")

    # 1. Cria o Usuário
    senha_criptografada = auth.gerar_hash_senha(user.senha)
    novo_usuario = models.User(nome=user.nome, senha_hash=senha_criptografada)
    db.add(novo_usuario)
    
    # 2. Cria a Conta Bancária automaticamente atrelada ao nome com saldo zero
    nova_conta = models.Conta(nome_titular=user.nome, saldo=0.00)
    db.add(nova_conta)
    
    # 3. Salva tudo no banco de dados
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


# Rota: Login (verificar usuário e retornar dados da conta)
@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Valida o usuário e a senha
    usuario = db.query(models.User).filter(models.User.nome == user.nome).first()
    if not usuario or not auth.verificar_senha(user.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    
    # Busca a conta bancária criada para este usuário
    conta = db.query(models.Conta).filter(models.Conta.nome_titular == usuario.nome).first()
    
    # Retorna o id da conta e o saldo para o frontend exibir
    return {
        "mensagem": f"Bem-vindo, {usuario.nome}!",
        "conta_id": conta.id if conta else None,
        "saldo": conta.saldo if conta else 0.00
    }


# Rota 1: Criar uma nova conta
@app.post("/contas/", status_code=201)
def criar_conta(conta: schemas.ContaCreate, db: Session = Depends(get_db)):
    nova_conta = models.Conta(nome_titular=conta.nome_titular, saldo=conta.saldo)
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)
    return {"id": nova_conta.id, "nome_titular": nova_conta.nome_titular, "saldo": nova_conta.saldo}

# Rota 2: Consultar saldo de uma conta
@app.get("/contas/{conta_id}/saldo")
def ver_saldo(conta_id: int, db: Session = Depends(get_db)):
    conta = db.query(models.Conta).filter(models.Conta.id == conta_id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"conta_id": conta.id, "nome_titular": conta.nome_titular, "saldo": conta.saldo}

# Rota 3: O coração do sistema - Transferência com ACID e Lock
@app.post("/transferencias/")
def realizar_transferencia(transacao: schemas.TransacaoCreate, db: Session = Depends(get_db)):
    # Validações iniciais
    if transacao.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor da transferência deve ser maior que zero")
    if transacao.conta_origem_id == transacao.conta_destino_id:
        raise HTTPException(status_code=400, detail="Contas de origem e destino não podem ser iguais")

    try:
        # 1. Busca as contas usando with_for_update() -> Isso aplica um LOCK no banco.
        # Nenhuma outra transação pode alterar estas contas até que esta finalize.
        conta_origem = db.query(models.Conta).filter(models.Conta.id == transacao.conta_origem_id).with_for_update().first()
        conta_destino = db.query(models.Conta).filter(models.Conta.id == transacao.conta_destino_id).with_for_update().first()

        # 2. Valida se as contas existem e se há saldo
        if not conta_origem:
            raise HTTPException(status_code=404, detail="Conta de origem não encontrada")
        if not conta_destino:
            raise HTTPException(status_code=404, detail="Conta de destino não encontrada")
        if conta_origem.saldo < transacao.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

        # 3. Realiza a matemática (tira de um, bota no outro)
        conta_origem.saldo -= transacao.valor
        conta_destino.saldo += transacao.valor

        # 4. Cria o histórico (extrato)
        nova_transacao = models.Transacao(
            conta_origem_id=transacao.conta_origem_id,
            conta_destino_id=transacao.conta_destino_id,
            valor=transacao.valor,
            status="CONCLUIDA"
        )
        db.add(nova_transacao)

        # 5. Salva TUDO de uma vez (Se der erro antes daqui, NADA é salvo)
        db.commit()
        return {"mensagem": "Transferência realizada com sucesso", "valor": transacao.valor}

    except HTTPException:
        # Se for um erro que nós mesmos criamos (como saldo insuficiente), repassamos ele
        db.rollback()
        raise
    except Exception as e:
        # Se der qualquer erro inesperado (ex: banco de dados caiu), desfaz tudo
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao processar a transferência")