from InquirerPy import inquirer
from pydantic import ValidationError as PydanticValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from lib.inquirrerPy import verificarCpf, verificarEmail, verificarVazio
from models.Cpf import Cpf, limparCpf
from models.Endereco import Endereco
from models.Usuario import Usuario

console = Console()

def printarUsuario(nome: str, email: str, favoritos: list): 
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

def getUsuario():
  nome = inquirer.text(message="Digite o nome do usuário: ", validate=verificarVazio).execute()
  sobrenome = inquirer.text(message="Digite o sobrenome do usuário: ", validate=verificarVazio).execute()
  email = inquirer.text(message="Digite o email do usuário: ", validate=verificarEmail).execute()
  senha = inquirer.secret(message="Digite a senha do usuário: ", validate=verificarVazio).execute()
  cpf = inquirer.text(message="Digite o CPF do usuário: ", validate=verificarCpf).execute()
  enderecos = getEnderecos()

  cpf_validado = Cpf(cpf=limparCpf(cpf))
  return Usuario(nome=nome, sobrenome=sobrenome, email=email, senha=senha, cpf=cpf_validado.cpf, favoritos=[], enderecos=enderecos)
  
def getEnderecos():
  enderecos: list[Endereco] = []
  
  while True:
    rua = inquirer.text(message="Rua: ", validate=verificarVazio).execute()
    numero = inquirer.text(message="Número: ", validate=verificarVazio).execute()
    bairro = inquirer.text(message="Bairro: ", validate=verificarVazio).execute()
    cidade = inquirer.text(message="Cidade: ", validate=verificarVazio).execute()
    default = inquirer.confirm(message="Esse é o endereço padrão?").execute()
    
    try:
      novoEndereco = Endereco.model_validate({"rua": rua, "numero": numero, "bairro": bairro, "cidade": cidade, "default": default})
    except PydanticValidationError:
      raise PydanticValidationError("Formato de endereço não suportado")
    
    if novoEndereco.default:
      for i in range(len(enderecos)):
        if not enderecos[i].default: 
          continue
        enderecos[i].default = False
        
    enderecos.append(novoEndereco)
    
    if not inquirer.confirm(message="Deseja adicionar mais um endereço? ").execute():
      return enderecos

def exibirErro(mensagem: str):
  console.print(
      Panel(
          f"[bold red]X {mensagem} [/bold red]",
          title="Erro",
          border_style='red',
          expand=False
      )
  )
