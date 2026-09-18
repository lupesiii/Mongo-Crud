from pydantic import BaseModel, Field, HttpUrl


class Favorito(BaseModel):
    id_produto: str | None = Field(default=None)
    nome: str
    imagem: HttpUrl
    precoEmCentavos: int = Field(ge=0)
