class Endereco:
    def __init__(
        self,
        rua: str,
        numero: str,
        bairro: str,
        cidade: str,
        default: bool
    ):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.default = default