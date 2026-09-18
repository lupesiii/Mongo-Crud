from pydantic import BaseModel, Field


class Endereco(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    rua: str
    numero: str
    bairro: str
    cidade: str
    default: bool
