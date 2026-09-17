from pydantic import BaseModel

class Endereco(BaseModel):
    rua: str
    numero: str
    bairro: str
    cidade: str
    default: bool