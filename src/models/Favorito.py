from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, BeforeValidator


class Favorito(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    produtoId: Annotated[str, BeforeValidator(str)] = Field(alias="id_produto")
    nome: str
    imagem: str
    precoEmCentavos: int = Field(ge=0)
