from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from cli import exibirErro, getUsuario, getLogin, getUsuarioUpdate
from db.transactions import deletarUsuarioTransaction
from db.usuario import buscarTodosUsuarios, buscarUsuario, cadastrarUsuario, deletarUsuario, loginUsuario, updateUsuario
from lib.inquirrerPy import verificarEmail, verificarVazio
from lib.rich import console
from rich.panel import Panel
from models.ErroException import ErroException


def menuUsuario():
  while True:
    console.print(
      Panel.fit(
          "Opções Usuário",
          border_style="cyan",
      )
    )

    opcao = inquirer.select(
    message="Escolha a ação desejada: ",
    choices=[
        Choice(1, name="Cadastrar usuário"),
        Choice(2, name="Buscar usuário por email"),
        Choice(3, name="Buscar todos os usuários"),
        Choice(4, name="Atualizar usuário"),
        Choice(5, name="Remover usuário"),
        Choice(6, name="Voltar"),
    ],
    ).execute()

    match opcao:
      case 1:
        novoUsuario = getUsuario()
        try:    
            cadastrarUsuario(novoUsuario)
        except ErroException as e:
            exibirErro(e.mensagem)
      case 2:
        email = inquirer.text(message="Digite o email do usuário: ", validate=verificarEmail).execute()
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
        email, senha = getLogin()
        try:
          usuarioId = loginUsuario(email, senha)
          usuario = buscarUsuario(email, False)
          usuarioUpdate = getUsuarioUpdate(usuario)
          updateUsuario(usuarioUpdate, usuarioId)
        except ErroException as e:
          exibirErro(e.mensagem)
      case 5:
        email, senha = getLogin()
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
