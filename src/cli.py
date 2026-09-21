from InquirerPy import inquirer
from pydantic import ValidationError as PydanticValidationError
from rich.console import Group
from datetime import datetime
from lib.rich import console
from InquirerPy.base.control import Choice
from rich.panel import Panel
from rich.table import Table
from lib.inquirrerPy import (
    transformarEmCentavos,
    transformarEmReais,
    verificarCpf,
    verificarDecimal,
    verificarEmail,
    verificarInteiro,
    verificarVazio,
)
from models.Cpf import Cpf, limparCpf
from models.Endereco import Endereco
from models.Produto import Produto, ProdutoUpdate
from models.Usuario import Usuario, UsuarioUpdate
from models.Vendedor import VendedorProduto, ProdutosCadastrados
from models.Favorito import Favorito
from models.Compra import Compra, CompraUpdate
from bson import ObjectId
from models.ErroException import ErroException


def printarUsuario(usuario: Usuario):
    if len(usuario.favoritos) > 0:
        tabelaFavoritos = Table(
            title="[bold yellow]⭐ Favoritos[/bold yellow]",
            border_style="cyan",
            show_lines=True,
        )
        tabelaFavoritos.add_column("N°", justify="center", style="dim")
        tabelaFavoritos.add_column("Produto", style="bold white")
        tabelaFavoritos.add_column("Preço", justify="right", style="green")

        for fav in usuario.favoritos:
            tabelaFavoritos.add_row(
                fav.produtoId,
                fav.nome,
                f"R$ {int(fav.precoEmCentavos) / 100:.2f}",
            )

    if len(usuario.enderecos) > 0:
        tabelaEnderecos = Table(
            title="[bold orange3]🛣️ Endereços[/bold orange3]",
            border_style="cyan",
            show_lines=True,
        )

        tabelaEnderecos.add_column("Endereço", justify="center", style="bold white")
        tabelaEnderecos.add_column("Cidade", justify="center", style="white")
        tabelaEnderecos.add_column("Default", justify="center", style="dim")

        for end in usuario.enderecos:
            enderecoCompleto = "".join([end.rua, " ", end.numero, ",", end.bairro])
            tabelaEnderecos.add_row(enderecoCompleto, end.cidade, str(end.default))

    content = Group(
        tabelaFavoritos if len(usuario.favoritos) > 0 else "Nenhum favorito adicionado",
        tabelaEnderecos if len(usuario.enderecos) > 0 else "Nenhum endereço adicionado",
    )

    console.print(
        Panel(
            content,
            title=f"[bold cyan]👤 {usuario.nome}[/bold cyan]",
            subtitle=f"[italic]{usuario.email}[/italic]",
            border_style="blue",
            padding=(1, 1),
            expand=False,
        )
    )


def printarVendedor(nomeLoja: str, produtosCadastrados: ProdutosCadastrados):
    if len(produtosCadastrados) > 0:
        tabelaCadastrados = Table(
            title="[bold yellow]🛒 Produtos[/bold yellow]",
            border_style="cyan",
            show_lines=True,
        )

        tabelaCadastrados.add_column("N°", justify="center", style="dim")
        tabelaCadastrados.add_column("Produto", style="bold white")
        tabelaCadastrados.add_column("Preço", justify="right", style="green")

        for produto in produtosCadastrados:
            tabelaCadastrados.add_row(
                produto.produtoId,
                produto.nome,
                f"R$ {int(produto.precoEmCentavos) / 100:.2f}",
            )

    console.print(
        Panel(
            (
                tabelaCadastrados
                if len(produtosCadastrados) > 0
                else "Nenhum produto cadastrado"
            ),
            title=f"[bold cyan]👤 {nomeLoja}[/bold cyan]",
            border_style="blue",
            padding=(1, 1),
            expand=False,
        )
    )


def printarProduto(produto: Produto):
    tabela = Table(
        border_style="cyan",
        show_lines=True,
    )

    tabela.add_column("Nome", style="bold yellow", justify="left")
    tabela.add_column("Descrição", style="bold white", justify="left")
    tabela.add_column("Preço", style="bold white", justify="left")
    tabela.add_column("Estoque", style="bold white", justify="center")

    vendedor = produto.vendedor

    corEstoque = (
        "green" if produto.estoque > 5 else "yellow" if produto.estoque > 0 else "red"
    )
    tabela.add_row(
        produto.nome,
        produto.descricao,
        f"[green]R$ {int(produto.precoEmCentavos) / 100:.2f}[/green]",
        f"[{corEstoque}] {produto.estoque} [/{corEstoque}]",
    )

    console.print(
        Panel(
            tabela,
            title=f"[bold cyan]🛍️ {vendedor.nome_loja}[/bold cyan]",
            border_style="blue",
            padding=(1, 1),
            expand=False,
        )
    )


def printarCompra(compra: Compra):
    tabela = Table(
        border_style="cyan",
        show_lines=True,
    )
 
    tabela.add_column("Produto", style="bold white", justify="left")
    tabela.add_column("Preço", style="green", justify="right")
    tabela.add_column("Data da compra", style="white", justify="center")
    tabela.add_column("Loja", style="white", justify="center")
 
    tabela.add_row(
        compra.nomeProduto,
        f"R$ {int(compra.precoEmCentavos) / 100:.2f}",
        compra.dataCompra,
        compra.nomeLoja,
    )
 
    console.print(
        Panel(
            tabela,
            title=f"[bold cyan]🧾 Compra de {compra.nomeUsuario}[/bold cyan]",
            subtitle=f"[italic]{compra.id}[/italic]",
            border_style="blue",
            padding=(1, 1),
            expand=False,
        )
    )    


def getUsuario():
    nome = inquirer.text(
        message="Digite o nome do usuário: ", validate=verificarVazio
    ).execute()
    sobrenome = inquirer.text(
        message="Digite o sobrenome do usuário: ", validate=verificarVazio
    ).execute()
    email = inquirer.text(
        message="Digite o email do usuário: ", validate=verificarEmail
    ).execute()
    senha = inquirer.secret(
        message="Digite a senha do usuário: ", validate=verificarVazio
    ).execute()
    cpf = inquirer.text(
        message="Digite o CPF do usuário: ", validate=verificarCpf
    ).execute()
    enderecos = getEnderecos()

    cpf_validado = Cpf(cpf=limparCpf(cpf))
    return Usuario(
        nome=nome.strip(),
        sobrenome=sobrenome.strip(),
        email=email.strip(),
        senha=senha.strip(),
        cpf=cpf_validado.cpf,
        favoritos=[],
        enderecos=enderecos,
    )


def getProduto(vendedorProduto: VendedorProduto):
    nome = inquirer.text(
        message="Digite o nome do produto: ", validate=verificarVazio
    ).execute()
    descricao = inquirer.text(
        message="Digite a descrição do produto: ", validate=verificarVazio
    ).execute()
    precoEmCentavos = inquirer.text(
        message="Digite o preco do produto em centavos: ",
        validate=verificarDecimal,
        transformer=transformarEmReais
    ).execute()
    estoque = inquirer.text(
        message="Digite a quantidade do estoque: ", validate=verificarInteiro
    ).execute()
    imagem = inquirer.text(
        message="Digite a url da imagem do produto: ", validate=verificarVazio
    ).execute()

    return Produto(
        id=ObjectId(),
        nome=nome.strip(),
        descricao=descricao.strip(),
        precoEmCentavos=transformarEmCentavos(precoEmCentavos),
        estoque=estoque,
        imagem=imagem.strip(),
        vendedor=vendedorProduto,
    )


def getEnderecos():
    enderecos: list[Endereco] = []

    while True:
        rua = inquirer.text(message="Rua: ", validate=verificarVazio).execute()
        numero = inquirer.text(message="Número: ", validate=verificarVazio).execute()
        bairro = inquirer.text(message="Bairro: ", validate=verificarVazio).execute()
        cidade = inquirer.text(message="Cidade: ", validate=verificarVazio).execute()
        default = inquirer.confirm(message="Esse é o endereço padrão?").execute()

        try:
            novoEndereco = Endereco.model_validate(
                {
                    "id": str(ObjectId()),
                    "rua": rua.strip(),
                    "numero": numero.strip(),
                    "bairro": bairro.strip(),
                    "cidade": cidade.strip(),
                    "default": default,
                }
            )
        except PydanticValidationError:
            raise PydanticValidationError("Formato de endereço não suportado")

        if novoEndereco.default:
            for i in range(len(enderecos)):
                if not enderecos[i].default:
                    continue
                enderecos[i].default = False

        enderecos.append(novoEndereco)

        if not inquirer.confirm(
            message="Deseja adicionar mais um endereço? "
        ).execute():
            return enderecos


def getUsuarioUpdate(usuario: Usuario):
    print("Dados em branco serão considerados sem alteração")
    nome = inquirer.text(message=f"Nome ({usuario.nome}): ").execute()
    sobrenome = inquirer.text(message=f"Sobrenome ({usuario.sobrenome}): ").execute()
    email = inquirer.text(message=f"Email ({usuario.email}): ").execute()
    senha = inquirer.secret(message="Nova senha (deixe em branco para não alterar): ").execute()
    cpf = inquirer.text(message=f"CPF ({usuario.cpf}): ").execute()
    favoritosParaRemover = selecionarFavoritos(usuario.favoritos)
    enderecosParaRemover = selecionarEnderecos(usuario.enderecos)    

    dados = {
        "nome": nome,
        "sobrenome": sobrenome,
        "email": email,
        "senha": senha,
        "cpf": cpf,
        "favoritos": favoritosParaRemover,
        "enderecos": enderecosParaRemover

    }

    if dados is None:
        raise ErroException("Coleta de dados cancelada pelo usuário")

    dadosPreenchidos = {
        chave: valor.strip() if type(valor) is str else valor for chave, valor in dados.items() if valor
    }

    try:
        usuarioUpdate = UsuarioUpdate.model_validate(dadosPreenchidos)
    except Exception as e:
        print(e)
        raise ErroException("Erro ao transformar os dados")

    return usuarioUpdate


def getVendedorUpdate(nomeLoja: str):
    print("Dados em branco serão considerados sem alteração")
    nomeLoja = inquirer.text(message=f"Nome da Loja ({nomeLoja}): ").execute()

    if not nomeLoja:
        raise ErroException("Coleta de dados cancelada pelo usuário")

    return nomeLoja.strip()


def getProdutoUpdate(produto: Produto):
    print("Dados em branco serão considerados sem alteração")
 
    nome = inquirer.text(message=f"Nome ({produto.nome}): ").execute()
    descricao = inquirer.text(message=f"Descrição ({produto.descricao}): ").execute()
    precoEmCentavos = inquirer.text(
        message=f"Preço (R$ {int(produto.precoEmCentavos) / 100:.2f}), "
        "deixe em branco para não alterar: "
    ).execute()
    estoque = inquirer.text(
        message=f"Estoque ({produto.estoque}), deixe em branco para não alterar: "
    ).execute()
    imagem = inquirer.text(message=f"Imagem ({produto.imagem}): ").execute()
 
    try:
        dados = {
            "nome": nome,
            "descricao": descricao,
            "precoEmCentavos": (
                transformarEmCentavos(precoEmCentavos) if precoEmCentavos else None
            ),
            "estoque": int(estoque) if estoque else None,
            "imagem": imagem,
        }
    except Exception:
        raise ErroException("Preço ou estoque informado em formato inválido")
 
    dadosPreenchidos = {
        chave: valor.strip() if type(valor) is str else valor for chave, valor in dados.items() if valor is not None
    }
 
    if not dadosPreenchidos:
        raise ErroException("Nenhum campo para atualizar foi informado")
 
    try:
        produtoUpdate = ProdutoUpdate.model_validate(dadosPreenchidos)
    except Exception as e:
        print(e)
        raise ErroException("Erro ao transformar os dados")
 
    return produtoUpdate


def selecionarFavoritos(favoritos: list[Favorito]):
    if len(favoritos) == 0:
        return []

    opcoes = [
        Choice(value=fav.produtoId, name=fav.nome)
        for fav in favoritos
    ]

    favoritosSelecionados = inquirer.checkbox(
        message="Selecione os favoritos que deseja remover (Tab):",
        choices=opcoes,
    ).execute()

    return favoritosSelecionados


def selecionarEnderecos(enderecos: list[Endereco]):
    if len(enderecos) == 0:
        return []

    opcoes = [
        Choice(value=end.id, name="".join([end.rua, " ", end.numero, ",", end.bairro]))
        for end in enderecos
    ]

    enderecosSelecionados = inquirer.checkbox(
        message="Selecione os enderecos que deseja remover (Tab):",
        choices=opcoes,
    ).execute()

    return enderecosSelecionados


def selecionarProdutosCadastrados(produtosCadastrados: list[ProdutosCadastrados]):
    if len(produtosCadastrados) == 0:
        return []

    opcoes = [
        Choice(value=pod.produtoId, name=pod.nome)
        for pod in produtosCadastrados
    ]

    produtosCadastradosSelecionados = inquirer.checkbox(
        message="Selecione os enderecos que deseja remover (Tab):",
        choices=opcoes,
    ).execute()

    return produtosCadastradosSelecionados

def selecionarProduto(produtos: list[Produto]):
    produto = inquirer.select(
        message="Selecione o produto desejado: ",
        choices=[
            Choice(
                value=p,
                name=f"{p.nome} - R$ {int(p.precoEmCentavos) / 100:.2f} "
                f"({p.vendedor.nome_loja}) - estoque: {p.estoque}",
            )
            for p in produtos
        ],
    ).execute()
 
    return produto


def selecionarEnderecoEntrega(enderecos: list[Endereco]):
    if len(enderecos) == 0:
        raise ErroException("Usuário não possui endereços cadastrados")
 
    opcoes = [
        Choice(
            value=end.id,
            name="".join([end.rua, " ", end.numero, ", ", end.bairro, " - ", end.cidade])
            + (" (padrão)" if end.default else ""),
        )
        for end in enderecos
    ]
 
    enderecoId = inquirer.select(
        message="Selecione o endereço de entrega: ",
        choices=opcoes,
    ).execute()
 
    return enderecoId
 
 
def getCompra(usuarioId: str, nomeUsuario: str, produto: Produto, enderecoEntregaId: str):
    dataCompra = datetime.now().strftime("%d-%m-%Y")
 
    return Compra(
        produtoId=produto.id,
        usuarioId=usuarioId,
        dataCompra=dataCompra,
        enderecoEntregaId=enderecoEntregaId,
        nomeProduto=produto.nome,
        precoEmCentavos=produto.precoEmCentavos,
        nomeUsuario=nomeUsuario,
        nomeLoja=produto.vendedor.nome_loja,
    )
 
 
def getCompraUpdate(compra: Compra, enderecos: list[Endereco]):
    print("Dados em branco serão considerados sem alteração")
 
    alterarEndereco = inquirer.confirm(
        message="Deseja alterar o endereço de entrega?" ).execute()
 
    novoEnderecoId = None
    if alterarEndereco:
        novoEnderecoId = selecionarEnderecoEntrega(enderecos)
 
    novaData = inquirer.text(
        message=f"Nova data da compra mm-dd-aaaa ({compra.dataCompra}), "
        "deixe em branco para não alterar: "
    ).execute()
 
    dados = {
        "id_endereco_entrega": novoEnderecoId,
        "data_compra": novaData if novaData else None,
    }
 
    dadosPreenchidos = {chave: valor for chave, valor in dados.items() if valor}
 
    if not dadosPreenchidos:
        raise ErroException("Nenhum campo para atualizar foi informado")
 
    try:
        compraUpdate = CompraUpdate.model_validate(dadosPreenchidos)
    except Exception:
        raise ErroException("Erro ao transformar os dados")
 
    return compraUpdate

def printarProdutosCadastrados(produtosCadastrados: list[ProdutosCadastrados]):
    if len(produtosCadastrados) == 0:
        raise ErroException("Nenhum produto cadastrado")

    produtoId = inquirer.select(
        message="Escolha o produto que desejada remover: ",
        choices=[Choice(produto.produtoId, name=produto.nome) for produto in produtosCadastrados]
    ).execute()

    return produtoId


def getLogin():
    console.print(
        Panel(
            "[bold cyan]🔑 Login[/bold cyan]",
            border_style="blue",
            padding=(0, 1),
            expand=False,
        )
    )

    email = inquirer.text(
        message="Digite o email do usuário: ", validate=verificarEmail
    ).execute()
    senha = inquirer.secret(
        message="Digite a senha do usuário: ", validate=verificarVazio
    ).execute()

    return [email, senha]


def exibirErro(mensagem: str):
    console.print(
        Panel(
            f"[bold red]X {mensagem} [/bold red]",
            title="Erro",
            border_style="red",
            expand=False,
        )
    )
