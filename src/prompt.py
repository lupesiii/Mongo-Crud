from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from cli import exibirErro, getUsuario
from db.usuario import buscarTodosUsuarios, buscarUsuario, cadastrarUsuario, deletarUsuario
from lib.inquirrerPy import verificarEmail, verificarVazio
from models.ErroException import ErroException

console = Console()

def menu_principal():
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
                menu_usuario()
                
            case 2:
                print("Menu vendedor")
                        
            case 3:
                print("Menu produto")
                        
            case 4:
                print("Menu compras")
                        
            case 5:
                break
            case _:
                exibirErro("Opção inválida")

def menu_usuario():
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
                print("Menu compras")
            case 5:
                email = inquirer.text(message="Digite o email do usuário: ", validate=verificarVazio).execute()
                try:    
                    deletarUsuario(email)
                except ErroException as e:
                    exibirErro(e.mensagem)
            case 6:
                console.clear()
                break
            case _:
                exibirErro("Opção inválida")

try:
    menu_principal()
except KeyboardInterrupt:
    exibirErro("Forçando interrupção do sistema")
    