from pydantic import BaseModel, field_validator
from decimal import Decimal

class UserCreate(BaseModel):
    nome: str
    senha: str

    @field_validator("senha")
    @classmethod
    def valida_tamanho_senha(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Senha muito longa (máximo 72 bytes)")
        return v

class UserResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True  # ou orm_mode = True, se estiver usando Pydantic v1


# Schema para quando o usuário for criar uma conta
class ContaCreate(BaseModel):
    nome_titular: str
    saldo: Decimal

# Schema para validar a requisição de transferência
class TransacaoCreate(BaseModel):
    conta_origem_id: int
    conta_destino_id: int
    valor: Decimal