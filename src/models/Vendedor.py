from pydantic import BaseModel


class Vendedor(BaseModel):
    nome_loja: str
    usuario_id: str
    produtos_cadastrados: list
    vendas: list
