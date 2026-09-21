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


def existeRegistro(identificador: str, collection: Collection, query: dict):
    identificador = identificador.strip()

    if not identificador:
        raise ErroException("Valor nulo não é aceito")

    try:
        exists = list(collection.find(query))
    except BaseException as e:
        raise ErroException("Erro ao verificar se registro existe")

    if len(exists) > 0:
        return True
    return False


def cadastrarProduto(produto: Produto, session):
    produtoDados = produto.model_dump(by_alias=True)
    produtoDados["_id"] = ObjectId(produtoDados["_id"]) if produtoDados.get("_id") else ObjectId()

    try:
        db.produtos.insert_one(produtoDados, session=session)
    except BaseException:
        raise ErroException("Erro ao criar registro do produto")


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


def buscarProdutoPorId(produtoId: str):
    produtoId = produtoId.strip()
 
    if not produtoId:
        raise ErroException("Valor nulo é inválido")
 
    try:
        produto = db.produtos.find_one({"_id": ObjectId(produtoId)})
    except Exception:
        raise ErroException("Erro ao recuperar produto")
 
    if not produto:
        raise ErroException("Produto não encontrado")
 
    try:
        produto = Produto.model_validate(produto)
    except ValidationError:
        raise ErroException("Erro ao converter produto")
 
    return produto


def buscarProdutosParaCompra(nome: str):
    nome = nome.strip()
    if not nome:
        raise ErroException("Valor nulo não é permitido")
 
    try:
        produtos = list(
            db.produtos.find({"nome": {"$regex": re.compile(nome, re.IGNORECASE)}})
        )
    except BaseException:
        raise ErroException("Não foi possivel verificar se produto existe")
 
    produtosValidados: list[Produto] = []
    for produto in produtos:
        try:
            produtosValidados.append(Produto.model_validate(produto))
        except Exception:
            continue
 
    if len(produtosValidados) == 0:
        raise ErroException("Nenhum produto disponível em estoque foi encontrado")
 
    return produtosValidados


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


def atualizarProduto(produtoUpdate: ProdutoUpdate, produtoId: str, session):
    try:
        produtoUpdate = ProdutoUpdate.model_validate(produtoUpdate)
    except ValidationError:
        raise ErroException("Formato de produto não suportado")
 
    produtoUpdateDump = produtoUpdate.model_dump(exclude_unset=True, exclude_none=True)
 
    if not produtoUpdateDump:
        raise ErroException("Nenhum campo para atualizar foi informado")
 
    exists = existeRegistro(produtoId, db.produtos, {"_id": ObjectId(produtoId)})
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

    exists = existeRegistro(produtoId, db.produtos, {"_id": ObjectId(produtoId)})
    if not exists:
        raise ErroException("Produto não existente")

    try:
        resultado = db.produtos.delete_one({"_id": ObjectId(produtoId)}, session=session)

        if resultado.deleted_count == 0:
            raise ErroException("Produto não encontrado")

    except BaseException as e:
        print(e)
        raise ErroException("Erro ao deletar produto")
