from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from cli import exibirErro
from itensMenu.comprasMenu import menuCompras
from itensMenu.produtoMenu import menuProduto
from itensMenu.usuarioMenu import menuUsuario
from itensMenu.vendedorMenu import menuVendedor
from lib.rich import console
from rich.panel import Panel


def menuPrincipal():
    while True:
        console.print(
            Panel.fit(
                "Mongo Crud",
                border_style="cyan",
            )
        )

        opcao = inquirer.select(
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
