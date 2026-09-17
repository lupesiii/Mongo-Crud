from models.Usuario import Usuario
from mongoConnection import db
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from models.Endereco import Endereco
from InquirerPy import inquirer
from lib.inquirrerPy import verificar_vazio
from pydantic import ValidationError

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

def buscar_todos_usuarios():
  usuarios = list(db.usuario.find().sort("nome"))
  
  if len(usuarios) == 0:
    console.print(
      Panel.fit(
        "Nenhum usuário encontrado",
        border_style="red",
      )
    )
  
  for user in usuarios:
    printar_usuario(user["nome"], user["email"], user["favoritos"])

def cadastrar_usuario(user: Usuario):
  try:
    user = Usuario.model_validate(user)
  except ValidationError:
    raise ValidationError("Formato de usuário não suportado")
  
  exists = existe_usuario(user.email)
  if exists:
    raise ValueError("Usuário já existente")
  
  user_dump = user.model_dump()
  user_dump = {key: value['cpf'] if key == "cpf" else value for key, value in user_dump.items()}

  db.usuario.insert_one(user_dump)
  
  console.print(
    Panel(
      f"[bold green]✓ Usuário {user.nome} cadastrado com sucesso![/bold green]",
      title="Cadastro",
      border_style="green"
    )
  )
  
def input_enderecos():
  enderecos: list[Endereco] = []
  
  while True:
    rua = inquirer.text(message="Rua: ", validate=verificar_vazio).execute()
    numero = inquirer.text(message="Número: ", validate=verificar_vazio).execute()
    bairro = inquirer.text(message="Bairro: ", validate=verificar_vazio).execute()
    cidade = inquirer.text(message="Cidade: ", validate=verificar_vazio).execute()
    default = inquirer.confirm(message="Esse é o endereço padrão?").execute()
    
    try:
      novoEndereco = Endereco.model_validate({"rua": rua, "numero": numero, "bairro": bairro, "cidade": cidade, "default": default})
    except ValidationError:
      raise ValidationError("Formato de endereço não suportado")
    
    if novoEndereco.default:
      for i in range(len(enderecos)):
        if not enderecos[i].default: 
          continue
        enderecos[i].default = False
        
    enderecos.append(novoEndereco)
    
    if not inquirer.confirm(message="Deseja adicionar mais um endereço? ").execute():
      return enderecos

def deletar_usuario(email):
  email = email.strip()
  
  if not email:
    raise ValueError("Valor nulo é inválido") 
  
  exists = existe_usuario(email)
  if not exists:
    raise ValueError("Usuário não existente")
  
  try:
    db.usuario.delete_one({"email": email})
    console.print(
      Panel(
        f"[bold green]✓ Usuário deletado com sucesso![/bold green]",
        title="Delete",
        border_style="green"
      )
    )
  except Exception as erro:
    console.print(
      Panel(
        f"[bold red]✓ Usuário não deletado[/bold red]",
        title="Delete",
        border_style="red"
      )
    )
    print(erro)
  

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
