from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator

from models.Vendedor import VendedorProduto


class Produto(BaseModel):
    id: Annotated[str, BeforeValidator(str)] | None = Field(default=None, alias="_id")
    nome: str
    descricao: str
    precoEmCentavos: int = Field(ge=0)
    estoque: int = Field(ge=0)
    imagem: str
    vendedor: VendedorProduto
