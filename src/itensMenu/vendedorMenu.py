from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from db.usuario import loginUsuario
from db.vendedor import (
    buscarTodosVendedores,
    buscarVendedor,
    cadastrarVendedor,
    deletarVendedor,
    atualizarVendedor,
)
from lib.rich import console
from rich.panel import Panel
from cli import exibirErro, getLogin, getVendedorUpdate
from lib.inquirrerPy import verificarEmail, verificarVazio
from models.ErroException import ErroException
from models.Vendedor import Vendedor
from bson import ObjectId


def menuVendedor():
    while True:
        console.print(
            Panel.fit(
                "Opções Vendedor",
                border_style="cyan",
            )
        )

        opcao = inquirer.select(
            message="Escolha a ação desejada: ",
            choices=[
                Choice(1, name="Cadastrar Vendedor"),
                Choice(2, name="Buscar vendedor por email"),
                Choice(3, name="Buscar todos os vendedores"),
                Choice(4, name="Atualizar vendedor"),
                Choice(5, name="Remover vendedor"),
                Choice(6, name="Voltar"),
            ],
        ).execute()

        match opcao:
            case 1:
                email, senha = getLogin()
                try:
                    usuarioId = loginUsuario(email, senha)
                    nomeLoja = inquirer.text(
                        message="Digite o nome da loja: ", validate=verificarVazio
                    ).execute()

                    vendedor = Vendedor(
                        nomeLoja=nomeLoja,
                        usuarioId=usuarioId,
                        produtosCadastrados=[],
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
                email, senha = getLogin()
                try:
                    loginUsuario(email, senha)
                    vendedor = buscarVendedor(email, False)
                    nomeLoja = getVendedorUpdate(vendedor.nomeLoja)
                    atualizarVendedor(vendedor.id, nomeLoja)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 5:
                email, senha = getLogin()
                try:
                    loginUsuario(email, senha)
                    deletarVendedor(email, None)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 6:
                console.clear()
                break
            case _:
                exibirErro("Opção inválida")
