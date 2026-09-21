from pydantic import BaseModel, Field


class Favorito(BaseModel):
    produtoId: str | None = Field(default=None, alias="id_produto")
    nome: str
    imagem: str
    precoEmCentavos: int = Field(ge=0)
