from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from cli import exibirErro, promptLogin, promptUsuario
from db.usuario import cadastrarUsuario, loginUsuario
from itensMenu.comprasMenu import menuCompras
from itensMenu.produtoMenu import menuProduto
from itensMenu.usuarioMenu import menuUsuario
from itensMenu.vendedorMenu import menuVendedor
from lib.rich import console
from rich.panel import Panel

from models.ErroException import ErroException
from session import sessao


def menuPrincipal():
    while True:
        console.print(
            Panel.fit(
                "Mongo Crud",
                border_style="cyan",
            )
        )

        opcaoEntrada = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
            message="Selecione uma das opções: ",
            choices=[
                Choice(1, name="Cadastrar"),
                Choice(2, name="Logar"),
            ],
        ).execute()

        match opcaoEntrada:
            case 1:
                novoUsuario = promptUsuario()
                try:
                    cadastrarUsuario(novoUsuario)
                    sessao.entrar(novoUsuario)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 2:
                try:
                    email, senha = promptLogin()
                    sessao.entrar(loginUsuario(email=email, senha=senha))
                except ErroException as e:
                    exibirErro(e.mensagem)

        if not sessao.estaAutenticada():
            raise ErroException("Usuario não atribuido")

        opcao = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
            message="Escolha a coleção desejada: ",
            choices=[
                Choice(1, name="Usuário"),
                Choice(2, name="Vendedor"),
                Choice(3, name="Produto"),
                Choice(4, name="Compras"),
                Choice(5, name="Sair"),
            ],
        ).execute()

        match opcao:
            case 1:
                menuUsuario()

            case 2:
                menuVendedor()

            case 3:
                menuProduto()

            case 4:
                menuCompras()

            case 5:
                break
            case _:
                exibirErro("Opção inválida")


try:
    menuPrincipal()
except KeyboardInterrupt:
    exibirErro("Forçando interrupção do sistema")
