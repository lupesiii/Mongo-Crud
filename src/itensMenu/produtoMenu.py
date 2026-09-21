from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from db.produto import cadastrarProduto, buscarProdutos, buscarTodosProdutos, buscarProdutoPorId
from db.transactions import atualizarProdutoTransaction, deletarProdutoTransaction, cadastrarProdutoTransaction
from db.usuario import loginUsuario
from db.vendedor import buscarVendedor, removerProdutoCadastrado
from lib.rich import console
from rich.panel import Panel
from cli import exibirErro, getLogin, getProduto, getProdutoUpdate, printarProdutosCadastrados
from lib.inquirrerPy import verificarEmail, verificarVazio
from models.ErroException import ErroException
from models.Vendedor import Vendedor, VendedorProduto


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
                Choice(2, name="Buscar produtos"),
                Choice(3, name="Buscar todos os produtos"),
                Choice(4, name="Atualizar produto"),
                Choice(5, name="Remover produto"),
                Choice(6, name="Voltar"),
            ],
        ).execute()

        match opcao:
            case 1:
                email, senha = getLogin()
                try:
                    loginUsuario(email, senha)
                    vendedor = buscarVendedor(email, False)
                    vendedorProduto = VendedorProduto(
                        vendedor_id=vendedor.id, nome_loja=vendedor.nomeLoja
                    )
                    produto = getProduto(vendedorProduto)
                    cadastrarProdutoTransaction(vendedor, produto)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 2:
                nome = inquirer.text(
                    message="Que produto deseja encontrar:", validate=verificarVazio
                ).execute()
                try:
                    buscarProdutos(nome)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 3:
                try:
                    buscarTodosProdutos()
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 4:
                email, senha = getLogin()
 
                try:
                    loginUsuario(email, senha)
                    vendedor = buscarVendedor(email, False)
                    produtoId = printarProdutosCadastrados(vendedor.produtosCadastrados)
                    produto = buscarProdutoPorId(produtoId)
                    produtoUpdate = getProdutoUpdate(produto)
                    atualizarProdutoTransaction(vendedor, produtoId, produtoUpdate)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 5:
                email, senha = getLogin()

                try:
                    loginUsuario(email, senha)
                    vendedor = buscarVendedor(email, False)
                    produtoId = printarProdutosCadastrados(vendedor.produtosCadastrados)
                    deletarProdutoTransaction(vendedor, produtoId)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 6:
                console.clear()
                break
            case _:
                exibirErro("Opção inválida")
