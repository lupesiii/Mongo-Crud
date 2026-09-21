from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated


class Endereco(BaseModel):
    id: str
    rua: str
    numero: str
    bairro: str
    cidade: str
    default: bool
