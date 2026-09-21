from bson import ObjectId
from pydantic import ValidationError
from rich.panel import Panel
from cli import printarCompra
from db.produto import existeRegistro
from lib.mongoConnection import db
from lib.rich import console
from models.Compra import Compra, CompraUpdate
from models.ErroException import ErroException


def existeCompra(compraId: str):
    return existeRegistro(compraId, db.compras, {"_id": ObjectId(compraId)})


def cadastrarCompra(compra: Compra, session=None):
    try:
        compra = Compra.model_validate(compra)
    except ValidationError:
        raise ErroException("Formato de compra não suportado")

    compraDados = compra.model_dump(by_alias=True, exclude={"id"})

    try:
        db.compras.insert_one(compraDados, session=session)
    except BaseException:
        raise ErroException("Erro ao criar registro da compra")


def buscarCompra(compraId: str, allow_print=True):
    compraId = compraId.strip()

    if not compraId:
        raise ErroException("Valor nulo é inválido")

    try:
        compra = db.compras.find_one({"_id": ObjectId(compraId)})
    except Exception:
        raise ErroException("Erro ao recuperar compra")

    if not compra:
        raise ErroException("Compra não encontrada")

    try:
        compra = Compra.model_validate(compra)
    except ValidationError:
        raise ErroException("Erro ao converter compra")

    if allow_print:
        printarCompra(compra)

    return compra


def buscarComprasPorUsuario(usuarioId: str):
    usuarioId = usuarioId.strip()

    if not usuarioId:
        raise ErroException("Valor nulo não é permitido")

    try:
        compras = list(db.compras.find({"id_usuario": usuarioId}).sort("data_compra"))
    except Exception:
        raise ErroException("Erro ao buscar compras do usuário")

    if len(compras) == 0:
        raise ErroException("Nenhuma compra encontrada")

    for compra in compras:
        try:
            compra = Compra.model_validate(compra)
        except BaseException:
            continue
        printarCompra(compra)


def buscarTodasCompras():
    try:
        compras = list(db.compras.find().sort("data_compra"))
    except Exception:
        raise ErroException("Erro ao buscar compras")

    if len(compras) == 0:
        raise ErroException("Nenhuma compra encontrada")

    for compra in compras:
        try:
            compra = Compra.model_validate(compra)
        except BaseException:
            continue
        printarCompra(compra)


def atualizarCompra(compraUpdate: CompraUpdate, compraId: str):
    try:
        compraUpdate = CompraUpdate.model_validate(compraUpdate)
    except ValidationError:
        raise ErroException("Formato de compra não suportado")

    compraUpdateDump = compraUpdate.model_dump(
        by_alias=True, exclude_unset=True, exclude_none=True
    )

    if not compraUpdateDump:
        raise ErroException("Nenhum campo para atualizar foi informado")

    exists = existeCompra(compraId)
    if not exists:
        raise ErroException("Compra não existente")

    try:
        db.compras.update_one(
            {"_id": ObjectId(compraId)},
            {"$set": compraUpdateDump},
        )
    except Exception:
        raise ErroException("Erro ao atualizar compra")

    console.print(
        Panel(
            "[bold green]✓ Compra atualizada com sucesso![/bold green]",
            title="Update",
            border_style="green",
        )
    )


def deletarCompra(compraId: str, session=None):
    compraId = compraId.strip()

    if not compraId:
        raise ErroException("Valor nulo é inválido")

    exists = existeCompra(compraId)
    if not exists:
        raise ErroException("Compra não existente")

    try:
        resultado = db.compras.delete_one({"_id": ObjectId(compraId)}, session=session)

        if resultado.deleted_count == 0:
            raise ErroException("Compra não encontrada")
    except Exception:
        raise ErroException("Erro ao deletar compra")