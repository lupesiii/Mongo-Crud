from pydantic import BaseModel, HttpUrl
class Favorito(BaseModel):
    id_produto: str
    nome: str
    imagem: HttpUrl
    precoEmCentavos: int 
