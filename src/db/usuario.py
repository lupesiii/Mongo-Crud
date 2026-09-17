from cli import printarUsuario
from models.ErroException import ErroException
from models.Usuario import Usuario
from lib.mongoConnection import db
from rich.console import Console
from rich.panel import Panel
from pydantic import ValidationError

console = Console()

def existeUsuario(email: str):
  email = email.strip()
  
  if not email:
    raise ErroException("Valor nulo não é aceito")

  try:
    exist = list(db.usuario.find({"email": email}))
  except Exception:
    raise ErroException("Erro ao verificar se usuário existe")
  
  if len(exist) > 0:
    return True
  return False

def buscarUsuario(email: str):
  email = email.strip()
  
  if not email:  
    raise ErroException("Valor nulo é inválido")
  
  try:
    user = db.usuario.find_one({"email": email})
  except Exception:
    raise ErroException("Erro ao recuperar usuário")
  
  if not user:
    console.print(
      Panel.fit(
        "Nenhum usuário encontrado",
        border_style="red",
      )
    )
    return
  
  user = dict(user)
  printarUsuario(user["nome"], user["email"], user["favoritos"])

def buscarTodosUsuarios():
  try:
    usuarios = list(db.usuario.find().sort("nome"))
  except Exception:
    raise ErroException("Erro ao verificar se usuário existe")
  
  if len(usuarios) == 0:
    console.print(
      Panel.fit(
        "Nenhum usuário encontrado",
        border_style="red",
      )
    )
  
  for user in usuarios:
    printarUsuario(user["nome"], user["email"], user["favoritos"])

def cadastrarUsuario(user: Usuario):
  try:
    user = Usuario.model_validate(user)
  except ValidationError:
    raise ErroException("Formato de usuário não suportado")
  
  exists = existeUsuario(user.email)
  if exists:
    raise ErroException("Usuário já existe")
  
  user_dump = user.model_dump()
  user_dump = {key: value['cpf'] if key == "cpf" else value for key, value in user_dump.items()}

  try:
    db.usuario.insert_one(user_dump)
  except Exception:
    raise ErroException("Erro ao criar registro do usuário")
  
  console.print(
    Panel(
      f"[bold green]✓ Usuário {user.nome} cadastrado com sucesso![/bold green]",
      title="Cadastro",
      border_style="green"
    )
  )
  
def deletarUsuario(email):
  email = email.strip()
  
  if not email:
    raise ErroException("Valor nulo é inválido") 
  
  exists = existeUsuario(email)
  if not exists:
    raise ErroException("Usuário não existente")
  
  try:
    db.usuario.delete_one({"email": email})
    console.print(
      Panel(
        f"[bold green]✓ Usuário deletado com sucesso![/bold green]",
        title="Delete",
        border_style="green"
      )
    )
  except Exception:
    raise ErroException("Usuário não foi deletado")
    