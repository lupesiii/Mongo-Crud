from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from db.usuario import loginUsuario
from db.vendedor import (
    buscarTodosVendedores,
    buscarVendedor,
    cadastrarVendedor,
    deletarVendedor,
)
from lib.rich import console
from rich.panel import Panel
from cli import exibirErro
from lib.inquirrerPy import verificarEmail, verificarVazio
from models.ErroException import ErroException
from models.Vendedor import Vendedor


def menuProduto():
    while True:
        console.print(
            Panel.fit(
                "Opções Produto",
                border_style="cyan",
            )
        )

        opcao = inquirer.select(
            message="Escolha a ação desejada: ",
            choices=[
                Choice(1, name="Cadastrar Produto"),
                Choice(2, name="Buscar produto por id"),
                Choice(3, name="Buscar todos os produtos"),
                Choice(4, name="Atualizar produto"),
                Choice(5, name="Remover produto"),
                Choice(6, name="Voltar"),
            ],
        ).execute()

        match opcao:
            case 1:
                email = inquirer.text(
                    message="Digite o email do usuário: ", validate=verificarEmail
                ).execute()
                senha = inquirer.text(
                    message="Digite a senha do usuário: ", validate=verificarVazio
                ).execute()

                try:
                    usuarioId = loginUsuario(email, senha)
                    nomeLoja = inquirer.text(
                        message="Digite o nome da loja: ", validate=verificarVazio
                    ).execute()

                    vendedor = Vendedor(
                        nome_loja=nomeLoja,
                        usuario_id=usuarioId,
                        produtos_cadastrados=[],
                        vendas=[],
                    )
                    cadastrarVendedor(vendedor)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 2:
                email = inquirer.text(
                    message="Digite o email do vendedor: ", validate=verificarEmail
                ).execute()
                try:
                    buscarVendedor(email)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 3:
                try:
                    buscarTodosVendedores()
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 4:
                print("Menu compras")
            case 5:
                email = inquirer.text(
                    message="Digite o email do usuário: ", validate=verificarVazio
                ).execute()
                try:
                    deletarVendedor(email)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 6:
                console.clear()
                break
            case _:
                exibirErro("Opção inválida")
