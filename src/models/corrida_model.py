from pydantic import BaseModel, field_validator


class Passageiro(BaseModel):
    nome: str
    telefone: str


class Motorista(BaseModel):
    nome: str
    nota: float


class Corrida(BaseModel):
    id_corrida: str
    passageiro: Passageiro
    motorista: Motorista
    origem: str
    destino: str
    valor_corrida: float
    forma_pagamento: str

    @field_validator("forma_pagamento")
    @classmethod
    def normalize_pagamento(cls, v: str) -> str:
        return v.strip()
