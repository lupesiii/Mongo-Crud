from pydantic import ValidationError
from rich.panel import Panel
from cli import printarVendedor
from db.usuario import existeUsuario
from lib.rich import console
from lib.mongoConnection import db
from models.ErroException import ErroException
from models.Vendedor import Vendedor, ProdutosCadastrados
from models.Produto import Produto
from bson import ObjectId
from pymongo.client_session import ClientSession


def existeVendedor(usuarioId: str):
    usuarioId = usuarioId.strip()

    if not usuarioId:
        raise ErroException("Valor nulo não é permitido")

    try:
        vendedorEncontrado = db.vendedores.find({"usuario_id": usuarioId})
        if vendedorEncontrado is None:
            return False
        return True
    except Exception:
        raise ErroException("Erro ao verificar se vendedor existe")


def buscarVendedor(email: str, allow_print=True):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo não é permitido")

    try:
        usuarioEncontrado = db.usuarios.find_one({"email": email})
        if usuarioEncontrado is None:
            raise ErroException("Usuário não existente")

        usuario = dict(usuarioEncontrado)
        vendedor = db.vendedores.find_one({"usuario_id": str(usuario.get("_id"))})

        if not vendedor:
            raise ErroException("Vendedor não encontrado")

        vendedor = Vendedor.model_validate(vendedor)
    except ErroException:
        raise
    except ValidationError:
        raise ErroException("Erro ao converter vendedor")
    except Exception:
        raise ErroException("Não foi possivel verificar se vendedor existe")

    if allow_print:
        printarVendedor(vendedor.nomeLoja, vendedor.produtosCadastrados)
    return vendedor


def buscarTodosVendedores():
    try:
        vendedoresEncontrados = db.vendedores.find().sort("nome_loja")
    except Exception:
        raise ErroException("Erro ao buscar vendedores")

    vendedores: list[Vendedor] = []
    for vendedor in vendedoresEncontrados:
        try:
            vendedores.append(Vendedor.model_validate(vendedor))
        except ValidationError:
            continue

    if len(vendedores) <= 0:
        console.print(
            Panel.fit(
                "Nenhum vendedor encontrado",
                border_style="red",
            )
        )
    for vendedor in vendedores:
        printarVendedor(vendedor.nomeLoja, vendedor.produtosCadastrados)


def cadastrarVendedor(vendedor: Vendedor):
    try:
        vendedor = Vendedor.model_validate(vendedor)
    except ValidationError:
        raise ErroException("Formato de vendedor não suportado")

    exists = existeVendedor(vendedor.usuarioId)
    if exists:
        raise ErroException("Usuário já possui cadastro de vendedor")

    try:
        db.vendedores.insert_one(vendedor.model_dump(by_alias=True, exclude_none=True))
    except BaseException as e:
        print(e)
        raise ErroException("Erro ao criar registro do usuário")

    console.print(
        Panel(
            f"[bold green]✓ Vendedor {vendedor.nomeLoja} cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def atualizarVendedor(vendedorId: str, nomeLoja: str):
    vendedorId = vendedorId.strip()
    nomeLoja = nomeLoja.strip()

    if not vendedorId or not nomeLoja:
        raise ErroException("Valores nulos não são permitidos")

    try:
        resultado = db.vendedores.update_one(
            {"_id": ObjectId(vendedorId)},
            {"$set": {"nome_loja": nomeLoja}},
        )
    except Exception as e:
        raise ErroException("Não foi possível atualizar o vendedor")

    if resultado.matched_count == 0:
        raise ErroException("Vendedor não encontrado")

    console.print(
        Panel(
            f"[bold green]✓ Vendedor atualizado com sucesso![/bold green]",
            title="Update",
            border_style="green",
        )
    )


def deletarVendedor(email: str, session: ClientSession | None):
    vendedor = buscarVendedor(email, False)
    try:
        vendedorDeletado = db.vendedores.delete_one(
            {"_id": ObjectId(vendedor.id)}, session=session if session else None
        )
    except Exception:
        raise ErroException("Vendedor não foi deletado")

    if vendedorDeletado.deleted_count == 0:
        raise ErroException("Vendedor não encontrado")

    console.print(
        Panel(
            f"[bold green]✓ Vendedor deletado com sucesso![/bold green]",
            title="Delete",
            border_style="green",
        )
    )


def cadastrarProdutoCadastrado(vendedor: Vendedor, produto: Produto, session):
    try:
        resultado = db.vendedores.update_one(
            {"_id": ObjectId(vendedor.id)},
            {
                "$push": {
                    "produtos_cadastrados": {
                        "id_produto": produto.id,
                        "nome": produto.nome,
                        "precoEmCentavos": produto.precoEmCentavos,
                    }
                }
            },
            session=session,
        )
    except Exception as e:
        raise ErroException("Não foi possível cadastrar produto")

    if resultado.matched_count == 0:
        raise ErroException("Vendedor não encontrado")


def atualizarProdutoCadastrado(
    vendedor: Vendedor, produtoId: str, produtoUpdateDump: dict, session
):
    camposAtualizados = {}

    if "nome" in produtoUpdateDump:
        camposAtualizados["produtos_cadastrados.$.nome"] = produtoUpdateDump["nome"]
    if "precoEmCentavos" in produtoUpdateDump:
        camposAtualizados["produtos_cadastrados.$.precoEmCentavos"] = produtoUpdateDump[
            "precoEmCentavos"
        ]

    if not camposAtualizados:
        return

    try:
        resultado = db.vendedores.update_one(
            {
                "_id": ObjectId(vendedor.id),
                "produtos_cadastrados.id_produto": produtoId,
            },
            {"$set": camposAtualizados},
            session=session,
        )
    except Exception:
        raise ErroException("Erro ao atualizar produto cadastrado do vendedor")

    if resultado.matched_count == 0:
        raise ErroException("Vendedor não encontrado")


def removerProdutoCadastrado(vendedor: Vendedor, produtoId: str, session):
    try:
        resultado = db.vendedores.update_one(
            {"_id": ObjectId(vendedor.id)},
            {"$pull": {"produtos_cadastrados": {"id_produto": produtoId}}},
            session=session,
        )
    except Exception:
        raise ErroException("Erro ao remover produto do vendedor")

    if resultado.matched_count == 0:
        raise ErroException("Vendedor não encontrado")
