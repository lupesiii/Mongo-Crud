from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from cli import (
    exibirErro,
    promptLogin,
    getUsuarioUpdate,
    promptUsuario,
    selecionarProduto,
)
from db.produto import buscarTodosProdutos
from db.transactions import deletarUsuarioTransaction
from db.usuario import (
    buscarTodosUsuarios,
    buscarUsuario,
    cadastrarUsuario,
    deletarUsuario,
    loginUsuario,
    atualizarUsuario,
    adicionarFavotito,
)
from lib.inquirrerPy import verificarEmail, verificarVazio
from lib.rich import console
from rich.panel import Panel
from models.ErroException import ErroException
from session import sessao


def menuUsuario():
    while True:
        console.print(
            Panel.fit(
                "Opções Usuário",
                border_style="cyan",
            )
        )

        opcao = inquirer.select(  # pyright: ignore[reportPrivateImportUsage]
            message="Escolha a ação desejada: ",
            choices=[
                Choice(2, name="Buscar usuário por email"),
                Choice(3, name="Buscar todos os usuários"),
                Choice(7, name="Adicionar produto ao favoritos"),
                Choice(4, name="Atualizar usuário"),
                Choice(5, name="Remover usuário"),
                Choice(6, name="Voltar"),
            ],
        ).execute()

        match opcao:
            case 2:
                email = inquirer.text(  # pyright: ignore[reportPrivateImportUsage]
                    message="Digite o email do usuário: ", validate=verificarEmail
                ).execute()
                try:
                    buscarUsuario(email)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 3:
                try:
                    buscarTodosUsuarios()
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 4:
                try:
                    usuarioAtual = sessao.usuarioAtual()
                    usuarioUpdate = getUsuarioUpdate(usuarioAtual)
                    atualizarUsuario(usuarioUpdate, usuarioAtual.id)
                except (ErroException, RuntimeError) as e:
                    mensagem = e.mensagem if isinstance(e, ErroException) else str(e)
                    exibirErro(mensagem)
            case 7:
                email, senha = promptLogin()
                try:
                    loginUsuario(email, senha)
                    produtos = buscarTodosProdutos(False)
                    produtosSelecionados = selecionarProduto(produtos)
                    adicionarFavotito(produtosSelecionados, email)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 5:
                email, senha = promptLogin()
                try:
                    loginUsuario(email, senha)
                    deletarUsuarioTransaction(email)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 6:
                console.clear()
                break
            case _:
                exibirErro("Opção inválida")
