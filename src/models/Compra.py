from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


class Compra(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Annotated[str, BeforeValidator(str)] | None = Field(default=None, alias="_id")
    produtoId: str = Field(alias="id_produto")
    usuarioId: str = Field(alias="id_usuario")
    dataCompra: str = Field(alias="data_compra")
    enderecoEntregaId: str = Field(alias="id_endereco_entrega")
    nomeProduto: str = Field(alias="nome_produto")
    precoEmCentavos: int = Field(ge=0)
    nomeUsuario: str = Field(alias="nome_usuario")
    nomeLoja: str = Field(alias="nome_loja")


class CompraUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dataCompra: Optional[str] = Field(default=None, alias="data_compra")
    enderecoEntregaId: Optional[str] = Field(
        default=None, alias="id_endereco_entrega"
    )