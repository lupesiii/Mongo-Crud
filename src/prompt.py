from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from db.usuario import buscar_usuario
from lib.inquirrerPy import verificar_vazio

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
                print("Opção inválida");

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
                print("Menu Usuario")
            case 2:
                email = inquirer.text(message="Digite o email do usuário: ", validate=verificar_vazio).execute()
                buscar_usuario(email)
            case 3:
                print("Menu produto")
            case 4:
                print("Menu compras")
            case 5:
                print("ede")
            case 6:
                console.clear()
                menu_principal()
            case _:
                print("Opção inválida");

menu_principal()
    