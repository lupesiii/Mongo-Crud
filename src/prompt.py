from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from db.usuario import buscar_todos_usuarios, buscar_usuario, cadastrar_usuario, deletar_usuario, input_enderecos
from lib.inquirrerPy import verificar_vazio, verificar_cpf, verificar_email
from models.Cpf import Cpf, limpar_cpf
from models.Email import Email
from models.Usuario import Usuario

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
                return
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
                nome = inquirer.text(message="Digite o nome do usuário: ", validate=verificar_vazio).execute()
                sobrenome = inquirer.text(message="Digite o sobrenome do usuário: ", validate=verificar_vazio).execute()
                email = inquirer.text(message="Digite o email do usuário: ", validate=verificar_email).execute()
                senha = inquirer.secret(message="Digite a senha do usuário: ", validate=verificar_vazio).execute()
                cpf = inquirer.text(message="Digite o CPF do usuário: ", validate=verificar_cpf).execute()
                enderecos = input_enderecos()
            
                cpf_validado = Cpf(cpf=limpar_cpf(cpf))
                novoUsuario = Usuario(nome=nome, sobrenome=sobrenome, email=email, senha=senha, cpf=cpf_validado.cpf, favoritos=[], enderecos=enderecos)
                cadastrar_usuario(novoUsuario)
            case 2:
                email = inquirer.text(message="Digite o email do usuário: ", validate=verificar_vazio).execute()
                buscar_usuario(email)
            case 3:
                buscar_todos_usuarios()
            case 4:
                print("Menu compras")
            case 5:
                email = inquirer.text(message="Digite o email do usuário: ", validate=verificar_vazio).execute()
                deletar_usuario(email)
            case 6:
                console.clear()
                break
            case _:
                print("Opção inválida");

menu_principal()
    