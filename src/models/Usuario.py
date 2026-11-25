from models.Cpf import Cpf
from models.Endereco import Endereco
from models.Favorito import Favorito
from pydantic import BaseModel, ConfigDict, EmailStr, BeforeValidator, Field
from typing import Annotated, Optional


class Usuario(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")
    nome: str
    sobrenome: str
    email: EmailStr
    senha: str
    cpf: Cpf
    favoritos: list[Favorito]
    enderecos: list[Endereco]


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    cpf: Optional[Cpf] = None
    favoritos: Optional[list[str]] = []
    enderecos: Optional[list[str]] = []
