from models.Cpf import Cpf
from models.Endereco import Endereco
from models.Favorito import Favorito


class Usuario:
  nome: str
  sobrenome: str
  email: str
  senha: str
  cpf: Cpf
  favoritos: list[Favorito]
  enderecos: list[Endereco]