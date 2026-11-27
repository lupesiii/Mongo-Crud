from models.Usuario import Usuario


class Sessao:
    def __init__(self) -> None:
        self.usuario: Usuario | None = None

    def entrar(self, usuario: Usuario) -> None:
        self.usuario = usuario

    def sair(self) -> None:
        self.usuario = None

    def usuarioAtual(self) -> Usuario:
        if self.usuario is None:
            raise RuntimeError("Nenhum usuário autenticado")

        return self.usuario

    def estaAutenticada(self) -> bool:
        return self.usuario is not None


sessao = Sessao()
