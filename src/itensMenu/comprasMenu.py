from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.panel import Panel
from cli import (
    exibirErro,
    getCompra,
    getCompraUpdate,
    selecionarEnderecoEntrega,
    selecionarProduto,
)
from db.compras import (
    atualizarCompra,
    buscarCompra,
    buscarComprasPorUsuario,
    buscarTodasCompras,
)
from db.produto import buscarProdutosParaCompra
from db.transactions import cadastrarCompraTransaction, deletarCompraTransaction
from db.usuario import buscarUsuario, buscarUsuarioId, loginUsuario
from lib.inquirrerPy import verificarEmail, verificarVazio
from lib.rich import console
from models.ErroException import ErroException


def menuCompras():
    while True:
        console.print(
            Panel.fit(
                "Opções Compras",
                border_style="cyan",
            )
        )

        opcao = inquirer.select(
            message="Escolha a ação desejada: ",
            choices=[
                Choice(1, name="Cadastrar Compra"),
                Choice(2, name="Buscar compra por id"),
                Choice(3, name="Buscar compras de um usuário"),
                Choice(4, name="Buscar todas as compras"),
                Choice(5, name="Atualizar compra"),
                Choice(6, name="Remover compra"),
                Choice(7, name="Voltar"),
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
                    usuario = buscarUsuario(email, False)

                    nomeProduto = inquirer.text(
                        message="Que produto deseja comprar: ", validate=verificarVazio
                    ).execute()
                    produtos = buscarProdutosParaCompra(nomeProduto)
                    produto = selecionarProduto(produtos)

                    enderecoEntregaId = selecionarEnderecoEntrega(usuario.enderecos)

                    compra = getCompra(usuarioId, usuario.nome, produto, enderecoEntregaId)
                    cadastrarCompraTransaction(compra)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 2:
                compraId = inquirer.text(
                    message="Digite o id da compra: ", validate=verificarVazio
                ).execute()
                try:
                    buscarCompra(compraId)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 3:
                email = inquirer.text(
                    message="Digite o email do usuário: ", validate=verificarEmail
                ).execute()
                try:
                    usuarioId = buscarUsuarioId(email)
                    buscarComprasPorUsuario(usuarioId)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 4:
                try:
                    buscarTodasCompras()
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 5:
                email = inquirer.text(
                    message="Digite o email do usuário: ", validate=verificarEmail
                ).execute()
                senha = inquirer.text(
                    message="Digite a senha do usuário: ", validate=verificarVazio
                ).execute()
                compraId = inquirer.text(
                    message="Digite o id da compra: ", validate=verificarVazio
                ).execute()

                try:
                    loginUsuario(email, senha)
                    usuario = buscarUsuario(email, False)
                    compra = buscarCompra(compraId, False)
                    compraUpdate = getCompraUpdate(compra, usuario.enderecos)
                    atualizarCompra(compraUpdate, compraId)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 6:
                email = inquirer.text(
                    message="Digite o email do usuário: ", validate=verificarEmail
                ).execute()
                senha = inquirer.text(
                    message="Digite a senha do usuário: ", validate=verificarVazio
                ).execute()
                compraId = inquirer.text(
                    message="Digite o id da compra: ", validate=verificarVazio
                ).execute()

                try:
                    loginUsuario(email, senha)
                    deletarCompraTransaction(compraId)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 7:
                console.clear()
                break
            case _:
                exibirErro("Opção inválida")