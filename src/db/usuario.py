from models import Usuario
from mongoConnection import db
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from models.Cpf import Cpf
from models.Endereco import Endereco
from models.Favorito import Favorito
from InquirerPy import inquirer
from lib.inquirrerPy import verificar_vazio

console = Console()

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
  
  user = db.usuario.find_one({"email": email})
  
  if not user:
    console.print(
      Panel.fit(
        "Nenhum usuário encontrado",
        border_style="red",
      )
    )
    return
  
  user = dict(user)
  printar_usuario(user["nome"], user["email"], user["favoritos"])

def printar_usuario(nome: str, email: str, favoritos: list): 
  if len(favoritos) > 0:
    tabela = Table(
        title="[bold yellow]⭐ Favoritos[/bold yellow]",
        border_style="cyan",
        show_lines=True,
    )
    tabela.add_column("N°", justify="center", style="dim")
    tabela.add_column("Produto", style="bold white")
    tabela.add_column("Preço", justify="right", style="green")
  

    for fav in favoritos:
      tabela.add_row(
          fav["id_produto"],
          fav["nome"],
          f"R$ {fav['precoEmCentavos']:.2f}",
      )
  console.print(
      Panel(
          tabela if len(favoritos) > 0 else "Nenhum favorito adicionado",
          title=f"[bold cyan]👤 {nome}[/bold cyan]",
          subtitle=f"[italic]{email}[/italic]",
          border_style="blue",
          padding=(1, 1),
          expand=False
      )
  )

def cadastrar_usuario(user: Usuario):
    print()
  
def input_enderecos():
  enderecos: list[Endereco] = []
  
  while True:
    rua = inquirer.text(message="Rua: ", validate=verificar_vazio).execute()
    numero = inquirer.text(message="Número: ", validate=verificar_vazio).execute()
    bairro = inquirer.text(message="Bairro: ", validate=verificar_vazio).execute()
    cidade = inquirer.text(message="Cidade: ", validate=verificar_vazio).execute()
    default = inquirer.confirm(message="Esse é o endereço padrão?").execute()
    
    novoEndereco = Endereco(rua=rua, numero=numero, bairro=bairro, cidade=cidade, default=default)
    
    if novoEndereco.default:
      for i in range(len(enderecos)):
        if not enderecos[i].default: 
          continue
        enderecos[i].default = False
        
    enderecos.append(novoEndereco)
    
    if not inquirer.confirm(message="Deseja adicionar mais um endereço? ").execute():
      print(enderecos)
      break