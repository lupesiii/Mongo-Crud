from cli import printarUsuario
from db.produto import existeProduto
from models.ErroException import ErroException
from models.Favorito import Favorito
from models.Produto import Produto
from models.Usuario import Usuario, UsuarioUpdate
from lib.mongoConnection import db
from rich.panel import Panel
from pydantic import ValidationError
from lib.rich import console
from pymongo.client_session import ClientSession
from bson import ObjectId


def loginUsuario(email: str, senha: str):
    email = email.strip()
    senha = senha.strip()
    if not email or not senha:
        raise ErroException("Valores nulos não são permitidos")

    try:
        usuarioEncontrado = db.usuarios.find_one({"email": email, "senha": senha})
        if not usuarioEncontrado:
            raise ErroException("Email ou senha inválido")

        usuario = Usuario.model_validate(usuarioEncontrado)
    except ErroException:
        raise
    except ValidationError:
        raise ErroException("Erro ao converter usuário")
    except Exception:
        raise ErroException("Erro ao recuperar usuário")

    return usuario


def existeUsuario(email: str):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo não é aceito")

    try:
        usuarioEncontrado = db.usuarios.find({"email": email})
        if usuarioEncontrado is None:
            return False
        return True
    except Exception:
        raise ErroException("Erro ao verificar se usuário existe")


def buscarUsuario(email: str, allow_Print=True):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo é inválido")

    try:
        usuarioEncontrado = db.usuarios.find_one({"email": email})
        if not usuarioEncontrado:
            raise ErroException("Usuário não encontrado")

        usuario = Usuario.model_validate(usuarioEncontrado)
    except ErroException:
        raise
    except ValidationError:
        raise ErroException("Erro ao converter usuário")
    except Exception:
        raise ErroException("Erro ao recuperar usuário")

    if allow_Print:
        printarUsuario(usuario)
    return usuario


def buscarUsuarioId(email: str):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo não é permitido")

    try:
        usuarioEncontrado = db.usuarios.find_one({"email": email})
        if usuarioEncontrado is None:
            raise ErroException("Usuário não encontrado")

        usuario = Usuario.model_validate(usuarioEncontrado)
    except ErroException:
        raise
    except ValidationError:
        raise ErroException("Erro ao converter usuário")
    except Exception:
        raise ErroException("Erro ao recuperar usuário")

    return usuario.id


def buscarTodosUsuarios():
    try:
        usuariosEncontrados = db.usuarios.find().sort("nome")
        if usuariosEncontrados is None:
            console.print(
                Panel.fit(
                    "Nenhum usuário encontrado",
                    border_style="red",
                )
            )
    except Exception:
        raise ErroException("Erro ao buscar usuários")

    for usuario in usuariosEncontrados:
        try:
            usuario = Usuario.model_validate(usuario)
            printarUsuario(usuario)
        except ValidationError:
            continue


def cadastrarUsuario(usuario: Usuario):
    try:
        usuario = Usuario.model_validate(usuario)
    except ValidationError:
        raise ErroException("Formato de usuário não suportado")

    usuarioExiste = existeUsuario(usuario.email)
    if usuarioExiste:
        raise ErroException("Usuário já existe")

    usuario_dump = usuario.model_dump()
    usuario_dump = {
        key: value["cpf"] if key == "cpf" else value
        for key, value in usuario_dump.items()
    }

    try:
        db.usuarios.insert_one(usuario_dump)
    except Exception:
        raise ErroException("Erro ao criar registro do usuário")

    console.print(
        Panel(
            f"[bold green]✓ Usuário {usuario.nome} cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def atualizarUsuario(usuario: UsuarioUpdate, usuarioId: str):
    try:
        usuarioUpdate = UsuarioUpdate.model_validate(usuario)
    except ValidationError:
        raise ErroException("Formato de usuário não suportado")

    usuarioUpdateDump = usuarioUpdate.model_dump(
        exclude={"favoritos", "enderecos"}, exclude_unset=True, exclude_none=True
    )

    favoritosIds = []
    if usuario.favoritos:
        favoritosIds = usuario.favoritos

    enderecosIds = []
    if usuario.enderecos:
        enderecosIds = usuario.enderecos

    if not usuarioUpdateDump and not usuario.favoritos and not usuario.enderecos:
        raise ErroException("Nenhum campo para atualizar foi informado")

    try:
        usuarioAtualizado = db.usuarios.update_one(
            {"_id": ObjectId(usuarioId)},
            {
                "$set": usuarioUpdateDump,
                "$pull": {
                    "favoritos": {"id_produto": {"$in": favoritosIds}},
                    "enderecos": {"id": {"$in": enderecosIds}},
                },
            },
        )

        if usuarioAtualizado.modified_count == 0:
            raise ErroException("Nenhum usuário modificado")

    except ErroException:
        raise
    except Exception:
        raise ErroException("Erro ao atualizar usuário")

    console.print(
        Panel(
            f"[bold green]✓ Usuario {usuario.nome} atualizado![/bold green]",
            title="Update",
            border_style="green",
        )
    )


def deletarUsuario(email, session: ClientSession):
    email = email.strip()
    if not email:
        raise ErroException("Valor nulo é inválido")

    usuarioExiste = existeUsuario(email)
    if not usuarioExiste:
        raise ErroException("Usuário não existente")

    try:
        db.usuarios.delete_one({"email": email}, session=session)
    except Exception:
        raise ErroException("Usuário não foi deletado")


def adicionarFavotito(vetorProdutos: list[Produto], email: str):
    email = email.strip()
    if not email:
        raise ErroException("Valor nulo é inválido")

    usuarioExiste = existeUsuario(email)
    if not usuarioExiste:
        raise ErroException("Usuário não existe")

    favoritos: list[Favorito] = []
    for produto in vetorProdutos:
        produtoExiste = existeProduto(produto.id)

        if not produtoExiste:
            raise ErroException("Produto não existe")

        try:
            favoritos.append(
                Favorito(
                    id_produto=produto.id,
                    nome=produto.nome,
                    imagem=produto.imagem,
                    precoEmCentavos=produto.precoEmCentavos,
                )
            )
        except ValidationError:
            continue

    try:
        usuarioAtualizado = db.usuarios.update_one(
            {"email": email},
            {
                "$addToSet": {
                    "favoritos": {"$each": favoritos},
                },
            },
        )

        if usuarioAtualizado.modified_count == 0:
            raise ErroException("Nenhum usuário encontrado")

    except ErroException:
        raise
    except Exception:
        raise ErroException("Erro ao adicionar favoritos ao usuário")

    console.print(
        Panel(
            f"[bold green]✓ Produtos adicionados ao favoritos![/bold green]",
            title="Update",
            border_style="green",
        )
    )
