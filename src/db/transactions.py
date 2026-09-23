from db.usuario import deletarUsuario
from models.Vendedor import Vendedor
from models.Produto import Produto, ProdutoUpdate
from lib.mongoConnection import db
from db.vendedor import (
    deletarVendedor,
    removerProdutoCadastrado,
    cadastrarProdutoCadastrado,
    atualizarProdutoCadastrado,
)
from models.ErroException import ErroException
from db.produto import (
    deletarProduto,
    cadastrarProduto,
    atualizarProduto,
    existeRegistro,
)
from db.compras import cadastrarCompra, deletarCompra
from lib.rich import console
from rich.panel import Panel
from pydantic import ValidationError
from models.Compra import Compra
from bson import ObjectId


def deletarUsuarioTransaction(email: str):
    with db.client.start_session() as session:
        try:
            with session.start_transaction():
                exists = existeRegistro(
                    identificador=email,
                    collection=db.vendedores,
                    query={"email": email},
                )

                deletarUsuario(email, session)
                if exists:
                    deletarVendedor(email, session)
        except Exception as e:
            print(e)
            raise ErroException("Erro ao deletar usuário")

    console.print(
        Panel(
            f"[bold green]✓ Usuário deletado com sucesso![/bold green]",
            title="Delete",
            border_style="green",
        )
    )


def cadastrarProdutoTransaction(vendedor: Vendedor, produto: Produto):
    try:
        vendedor = Vendedor.model_validate(vendedor)
        produto = Produto.model_validate(produto)
    except ValidationError as e:
        raise ErroException("Formato dos dados inválido")

    with db.client.start_session() as session:
        try:
            with session.start_transaction():
                cadastrarProduto(produto, session)
                cadastrarProdutoCadastrado(vendedor, produto, session)

        except Exception as e:
            raise ErroException("Erro ao cadastrar produto")

    console.print(
        Panel(
            "[bold green]✓ Produto cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def deletarProdutoTransaction(vendedor: Vendedor, produtoId: str):
    try:
        vendedor = Vendedor.model_validate(vendedor)
    except ValidationError as e:
        raise ErroException("Formato dos dados inválido")

    with db.client.start_session() as session:
        try:
            with session.start_transaction():
                deletarProduto(produtoId, session)
                removerProdutoCadastrado(vendedor, produtoId, session)

        except Exception as e:
            raise ErroException(e)

    console.print(
        Panel(
            f"[bold green]✓ Produto deletado com sucesso![/bold green]",
            title="Delete",
            border_style="green",
        )
    )


def atualizarProdutoTransaction(
    vendedor: Vendedor, produtoId: str, produtoUpdate: ProdutoUpdate
) -> None:
    try:
        vendedor = Vendedor.model_validate(vendedor)
        produtoUpdate = ProdutoUpdate.model_validate(produtoUpdate)
    except ValidationError:
        raise ErroException("Formato dos dados inválido")

    produtoUpdateDump = produtoUpdate.model_dump(exclude_unset=True, exclude_none=True)

    with db.client.start_session() as session:
        try:
            with session.start_transaction():
                atualizarProduto(produtoUpdate, produtoId, session)
                atualizarProdutoCadastrado(
                    vendedor, produtoId, produtoUpdateDump, session
                )

        except ErroException:
            raise
        except Exception as e:
            raise ErroException("Erro ao atualizar produto")

    console.print(
        Panel(
            "[bold green]✓ Produto atualizado com sucesso![/bold green]",
            title="Update",
            border_style="green",
        )
    )


def cadastrarCompraTransaction(compra: Compra):
    try:
        compra = Compra.model_validate(compra)
    except ValidationError:
        raise ErroException("Formato de compra não suportado")

    with db.client.start_session() as session:
        try:
            with session.start_transaction():
                resultado = db.produtos.update_one(
                    {"_id": ObjectId(compra.produtoId), "estoque": {"$gt": 0}},
                    {"$inc": {"estoque": -1}},
                    session=session,
                )

                if resultado.matched_count == 0:
                    raise ErroException("Produto sem estoque disponível")

                cadastrarCompra(compra, session)

        except ErroException:
            raise
        except Exception as e:
            print(e)
            raise ErroException("Erro ao cadastrar compra")

    console.print(
        Panel(
            "[bold green]✓ Compra realizada com sucesso![/bold green]",
            title="Compra",
            border_style="green",
        )
    )


def deletarCompraTransaction(compraId: str):
    with db.client.start_session() as session:
        try:
            with session.start_transaction():
                compra = db.compras.find_one(
                    {"_id": ObjectId(compraId)}, session=session
                )

                if not compra:
                    raise ErroException("Compra não encontrada")

                deletarCompra(compraId, session)

                db.produtos.update_one(
                    {"_id": ObjectId(compra["id_produto"])},
                    {"$inc": {"estoque": 1}},
                    session=session,
                )

        except ErroException:
            raise
        except Exception as e:
            print(e)
            raise ErroException("Erro ao remover compra")

    console.print(
        Panel(
            "[bold green]✓ Compra removida com sucesso![/bold green]",
            title="Delete",
            border_style="green",
        )
    )
