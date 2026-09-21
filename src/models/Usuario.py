from models.Cpf import Cpf
from models.Endereco import Endereco
from models.Favorito import Favorito
from pydantic import BaseModel, EmailStr
from typing import Optional


class Usuario(BaseModel):
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