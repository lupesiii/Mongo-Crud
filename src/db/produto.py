import re

from pydantic import ValidationError
from rich.panel import Panel

from cli import printarProduto
from lib.mongoConnection import db
from models.ErroException import ErroException
from models.Produto import Produto
from lib.rich import console


def cadastrarProduto(produto: Produto):
    try:
        produto = Produto.model_validate(produto)
    except ValidationError:
        raise ErroException("Formato de usuário não suportado")

    try:
        db.produtos.insert_one(produto.model_dump(exclude={"id"}))
    except BaseException:
        raise ErroException("Erro ao criar registro do produto")

    console.print(
        Panel(
            f"[bold green]✓ Produto {produto.nome} cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def buscarProdutos(nome: str):
    nome = nome.strip()
    if not nome:
        raise ErroException("Valor nulo não é permitido")
    try:
        produtos = list(
            db.produtos.find({"nome": {"$regex": re.compile(nome, re.IGNORECASE)}})
        )
    except BaseException:
        raise ErroException("Não foi possivel verificar se produto existe")

    if len(produtos) == 0:
        raise ErroException("Nenhum produto encontrado")

    for produto in produtos:
        try:
            produto = Produto.model_validate(produto)
        except BaseException as e:
            continue
        printarProduto(produto)


def buscarTodosProdutos():
    try:
        produtos = list(db.produtos.find().sort("nome"))
    except BaseException:
        raise ErroException("Não foi possível recuperar os produtos")

    if len(produtos) == 0:
        raise ErroException("Nenhum produto encontrado")

    for produto in produtos:
        try:
            produto = Produto.model_validate(produto)
        except BaseException as e:
            continue
        printarProduto(produto)
