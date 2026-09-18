from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


class Vendedor(BaseModel):
    id: Annotated[str, BeforeValidator(str)] | None = Field(default=None, alias="_id")
    nome_loja: str
    usuario_id: str
    produtos_cadastrados: list
    vendas: list


class VendedorProduto(BaseModel):
    vendedor_id: str
    nome_loja: str
