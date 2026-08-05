import bcrypt

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return hash_bytes.decode("utf-8")

def verificar_senha(senha_texto: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha_texto.encode("utf-8"), senha_hash.encode("utf-8"))
