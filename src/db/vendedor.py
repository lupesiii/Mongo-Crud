from pydantic import ValidationError
from rich.panel import Panel

from cli import printarVendedor
from db.usuario import existeUsuario
from lib.rich import console
from lib.mongoConnection import db
from models.ErroException import ErroException
from models.Vendedor import Vendedor


def existeVendedor(usuarioId: str):
    usuarioId = usuarioId.strip()

    if not usuarioId:
        raise ErroException("Valor nulo não é permitido")

    try:
        exists = list(db.vendedores.find({"usuario_id": usuarioId}))
    except BaseException:
        raise ErroException("Erro ao verificar se vendedor existe")

    if len(exists) > 0:
        return True
    return False


def buscarVendedor(email: str, allow_print=True):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo não é permitido")

    exists = existeUsuario(email)
    if not exists:
        raise ErroException("Usuário não existente")

    try:
        usuario = dict(db.usuarios.find_one({"email": email}))
        vendedor = db.vendedores.find_one({"usuario_id": str(usuario.get("_id"))})
    except BaseException:
        raise ErroException("Não foi possivel verificar se vendedor existe")

    if not vendedor:
        raise ErroException("Vendedor não encontrado")

    vendedor = dict(vendedor)

    if allow_print:
        printarVendedor(vendedor["nome_loja"], vendedor["produtos_cadastrados"])

    return vendedor


def buscarTodosVendedores():
    try:
        vendedores = list(db.vendedores.find().sort("nome_loja"))
    except BaseException:
        raise ErroException("Erro ao buscar vendedores")

    if len(vendedores) == 0:
        console.print(
            Panel.fit(
                "Nenhum vendedor encontrado",
                border_style="red",
            )
        )

    for vendedor in vendedores:
        printarVendedor(vendedor["nome_loja"], vendedor["produtos_cadastrados"])


def cadastrarVendedor(vendedor: Vendedor):
    try:
        vendedor = Vendedor.model_validate(vendedor)
    except ValidationError:
        raise ErroException("Formato de vendedor não suportado")

    exists = existeVendedor(vendedor.usuario_id)
    if exists:
        raise ErroException("Usuário já possui cadastro de vendedor")

    try:
        db.vendedores.insert_one(vendedor.model_dump())
    except BaseException as e:
        print(e)
        raise ErroException("Erro ao criar registro do usuário")

    console.print(
        Panel(
            f"[bold green]✓ Vendedor {vendedor.nome_loja} cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def deletarVendedor(email: str):
    vendedor = buscarVendedor(email, False)

    try:
        db.vendedores.delete_one({"_id": vendedor["_id"]})
        console.print(
            Panel(
                f"[bold green]✓ Vendedor deletado com sucesso![/bold green]",
                title="Delete",
                border_style="green",
            )
        )
    except BaseException:
        raise ErroException("Vendedor não foi deletado")
