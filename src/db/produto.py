import re
from pydantic import ValidationError
from rich.panel import Panel
from pymongo.collection import Collection
from cli import printarProduto
from lib.mongoConnection import db
from models.ErroException import ErroException
from models.Produto import Produto, ProdutoUpdate
from models.Vendedor import Vendedor
from lib.rich import console
from bson import ObjectId


def existeProduto(produtoId: str):
    produtoId = produtoId.strip()
    if not produtoId:
        raise ErroException("Valor nulo não é aceito")

    try:
        produtoEncontrado = db.produtos.find({"_id": ObjectId(produtoId)})
        if produtoEncontrado is None:
            return False
        return True
    except Exception:
        raise ErroException("Erro ao verificar se produto existe")


def buscarProdutos(nome: str):
    nome = nome.strip()
    if not nome:
        raise ErroException("Valor nulo não é permitido")

    try:
        produtosEncontrados = db.produtos.find(
            {"nome": {"$regex": re.compile(nome, re.IGNORECASE)}}
        )
        if produtosEncontrados is None:
            raise ErroException("Nenhum produto encontrado")
    except ErroException:
        raise
    except Exception:
        raise ErroException("Não foi possivel verificar se produto existe")

    for produto in produtosEncontrados:
        try:
            produto = Produto.model_validate(produto)
            printarProduto(produto)
        except Exception as e:
            continue


def buscarProdutoPorId(produtoId: str):
    produtoId = produtoId.strip()
    if not produtoId:
        raise ErroException("Valor nulo é inválido")

    try:
        produtoEncontrado = db.produtos.find_one({"_id": ObjectId(produtoId)})
        if produtoEncontrado is None:
            raise ErroException("Produto não encontrado")

        produto = Produto.model_validate(produtoEncontrado)
    except ErroException:
        raise
    except ValidationError:
        raise ErroException("Erro ao converter produto")
    except Exception:
        raise ErroException("Erro ao recuperar produto")

    return produto


def buscarProdutosParaCompra(nome: str):
    nome = nome.strip()
    if not nome:
        raise ErroException("Valor nulo não é permitido")

    try:
        produtosEncontrados = db.produtos.find(
            {"nome": {"$regex": re.compile(nome, re.IGNORECASE)}}
        )
        if produtosEncontrados is None:
            raise ErroException("Nenhum produto encontrado")
    except ErroException:
        raise
    except Exception:
        raise ErroException("Não foi possivel verificar se produto existe")

    produtos: list[Produto] = []
    for produto in produtosEncontrados:
        try:
            produtos.append(Produto.model_validate(produto))
        except Exception:
            continue

    if len(produtos) == 0:
        raise ErroException("Nenhum produto disponível em estoque foi encontrado")
    return produtos


def buscarTodosProdutos(allowPrint=True):
    try:
        produtosEncontrados = db.produtos.find().sort("nome")
        if produtosEncontrados is None:
            raise ErroException("Nenhum produto encontrado")
    except ErroException:
        raise
    except Exception:
        raise ErroException("Não foi possivel verificar se produto existe")

    produtos: list[Produto] = []
    for produto in produtosEncontrados:
        try:
            produto = Produto.model_validate(produto)
            produtos.append(produto)
            if allowPrint:
                printarProduto(produto)
        except Exception as e:
            continue
    return produtos


def cadastrarProduto(produto: Produto, session):
    produtoDados = produto.model_dump(by_alias=True)
    produtoDados["_id"] = (
        ObjectId(produtoDados["_id"]) if produtoDados.get("_id") else ObjectId()
    )

    try:
        db.produtos.insert_one(produtoDados, session=session)
    except Exception:
        raise ErroException("Erro ao criar registro do produto")


def atualizarProduto(produtoUpdate: ProdutoUpdate, produtoId: str, session):
    try:
        produtoUpdate = ProdutoUpdate.model_validate(produtoUpdate)
    except ValidationError:
        raise ErroException("Formato de produto não suportado")

    produtoUpdateDump = produtoUpdate.model_dump(exclude_unset=True, exclude_none=True)

    if not produtoUpdateDump:
        raise ErroException("Nenhum campo para atualizar foi informado")

    exists = existeProduto(produtoId)
    if not exists:
        raise ErroException("Produto não existente")

    try:
        db.produtos.update_one(
            {"_id": ObjectId(produtoId)},
            {"$set": produtoUpdateDump},
            session=session,
        )
    except Exception:
        raise ErroException("Erro ao atualizar produto")


def deletarProduto(produtoId: str, session):
    produtoId = produtoId.strip()

    if not produtoId:
        raise ErroException("Valor nulo é inválido")

    exists = existeProduto(produtoId)
    if not exists:
        raise ErroException("Produto não existente")

    try:
        resultado = db.produtos.delete_one(
            {"_id": ObjectId(produtoId)}, session=session
        )

        if resultado.deleted_count == 0:
            raise ErroException("Produto não encontrado")

    except Exception as e:
        print(e)
        raise ErroException("Erro ao deletar produto")
