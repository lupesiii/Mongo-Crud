from models.Cpf import Cpf
from models.Endereco import Endereco
from models.Favorito import Favorito
from pydantic import BaseModel, EmailStr


class Usuario(BaseModel):
  nome: str
  sobrenome: str
  email: EmailStr
  senha: str
  cpf: Cpf
  favoritos: list[Favorito]
  enderecos: list[Endereco]