from bson import ObjectId
from pydantic import ValidationError
from rich.panel import Panel
from cli import printarCompra
from lib.mongoConnection import db
from lib.rich import console
from models.Compra import Compra, CompraUpdate
from models.ErroException import ErroException


def existeCompra(compraId: str):
    compraId = compraId.strip()
    if not compraId:
        raise ErroException("Valor nulo não é aceito")

    try:
        compraEncontrada = db.compras.find_one({"_id": ObjectId(compraId)})
        if compraEncontrada is None:
            return False
        return True
    except Exception:
        raise ErroException("Erro ao verificar se compra existe")


def buscarCompra(compraId: str, allow_print=True):
    compraId = compraId.strip()
    if not compraId:
        raise ErroException("Valor nulo é inválido")

    try:
        compraEncontrada = db.compras.find_one({"_id": ObjectId(compraId)})
        if compraEncontrada is None:
            raise ErroException("Compra não encontrada")

        compra = Compra.model_validate(compraEncontrada)
    except ErroException:
        raise
    except ValidationError:
        raise ErroException("Erro ao converter compra")
    except Exception:
        raise ErroException("Erro ao recuperar compra")

    if allow_print:
        printarCompra(compra)
    return compra


def buscarComprasPorUsuario(usuarioId: str):
    usuarioId = usuarioId.strip()
    if not usuarioId:
        raise ErroException("Valor nulo não é permitido")

    try:
        comprasEncontradas = db.compras.find({"id_usuario": usuarioId}).sort(
            "data_compra"
        )
        if comprasEncontradas is None:
            raise ErroException("Nenhuma compra encontrada")
    except ErroException:
        raise
    except Exception:
        raise ErroException("Erro ao buscar compras do usuário")

    for compra in comprasEncontradas:
        try:
            compra = Compra.model_validate(compra)
            printarCompra(compra)
        except ValidationError:
            continue


def buscarTodasCompras():
    try:
        comprasEncontradas = db.compras.find().sort("data_compra")
        if comprasEncontradas is None:
            raise ErroException("Nenhuma compra encontrada")
    except Exception:
        raise ErroException("Erro ao buscar compras")

    for compra in comprasEncontradas:
        try:
            compra = Compra.model_validate(compra)
            printarCompra(compra)
        except ValidationError:
            continue


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


def atualizarCompra(compraUpdate: CompraUpdate, compraId: str):
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
