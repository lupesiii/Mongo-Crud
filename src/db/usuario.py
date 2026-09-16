from mongoConnection import db
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from types.Cpf import Cpf
from types.Endereco import Endereco
from types.Favorito import Favorito
from InquirerPy import inquirer
from lib.inquirrerPy import verificar_vazio

console = Console()

class Usuario:
  nome: str
  sobrenome: str
  email: str
  senha: str
  cpf: Cpf
  favoritos: list[Favorito]
  enderecos: list[Endereco]
  

def existe_usuario(email: str):
  email = email.strip()
  
  if not email:
    return False

  exist = list(db.usuario.find({"email": email}))
  
  if len(exist) > 0:
    return True
  return False

def buscar_usuario(email: str):
  email = email.strip()
  
  if not email:  
    raise ValueError("Valor nulo é inválido")
  
  user = dict(db.usuario.find_one({"email": email}))
  
  if len(user) == 0:  
    print("Nenhum usuário encontrado")
    return
  
  tabela = Table(
      title="[bold yellow]⭐ Favoritos[/bold yellow]",
      border_style="cyan",
      show_lines=True,
  )

  tabela.add_column("Nº", justify="center", style="dim")
  tabela.add_column("Produto", style="bold white")
  tabela.add_column("Preço", justify="right", style="green")

  print(user["favoritos"])

  for fav in user["favoritos"]:
      tabela.add_row(
          fav["id_produto"],
          fav["nome"],
          f"R$ {fav['precoEmCentavos']:.2f}",
      )

  console.print(
      Panel(
          tabela,
          title=f"[bold cyan]👤 {user['nome']}[/bold cyan]",
          subtitle=f"[italic]{user['email']}[/italic]",
          border_style="blue",
          padding=(1, 1),
          expand=False
      )
  )
  
# def cadastrar_usuario(user: Usuario):
  
def input_enderecos():
  enderecos: list[Endereco] = []
  
  while True:
    rua = inquirer.text(message="Rua: ", validate=verificar_vazio).execute()
    numero = inquirer.text(message="Número: ", validate=verificar_vazio).execute()
    bairro = inquirer.text(message="Bairro: ", validate=verificar_vazio).execute()
    cidade = inquirer.text(message="Cidade: ", validate=verificar_vazio).execute()
    default = inquirer.confirm(message="Esse é o endereço padrão?").execute()

    enderecos = list(filter(lambda end: end["default"], enderecos))
    print(enderecos)
    
    endereco = Endereco(rua=rua, numero=numero, bairro=bairro, cidade=cidade, default=default)
    enderecos.append(endereco)
    
    if not inquirer.confirm(message="Deseja adicionar mais um endereço? ").execute():
      break
input_enderecos()