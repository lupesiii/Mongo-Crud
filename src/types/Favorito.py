class Favorito:
    def __init__(
        self,
        id_produto: str,
        nome: str,
        imagem: str,
        precoEmCentavos: int
    ):
        self.id_produto = id_produto
        self.nome = nome
        self.imagem = imagem
        self.precoEmCentavos = precoEmCentavos