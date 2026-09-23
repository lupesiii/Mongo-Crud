from cli import printarUsuario
from models.ErroException import ErroException
from models.Usuario import Usuario, UsuarioUpdate
from lib.mongoConnection import db
from rich.panel import Panel
from pydantic import ValidationError
from lib.rich import console
from bson import ObjectId


def existeUsuario(email: str):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo não é aceito")

    try:
        exists = list(db.usuarios.find({"email": email}))
    except BaseException:
        raise ErroException("Erro ao verificar se usuário existe")

    if len(exists) > 0:
        return True
    return False


def buscarUsuario(email: str, allow_Print=True):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo é inválido")

    try:
        user = db.usuarios.find_one({"email": email})
    except BaseException:
        raise ErroException("Erro ao recuperar usuário")

    if not user:
        console.print(
            Panel.fit(
                "Nenhum usuário encontrado",
                border_style="red",
            )
        )
        return

    try:
        user = Usuario.model_validate(user)
    except BaseException as e:
        print(e)
        raise ErroException("Erro ao converter usuário")

    if allow_Print:
        printarUsuario(user)

    return user


def buscarUsuarioId(email: str):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo não é permitido")

    try:
        user = db.usuarios.find_one({"email": email})
    except BaseException:
        raise ErroException("Erro ao recuperar usuário")

    if not user:
        raise ErroException("Usuário não encontrado")

    return str(user.get("_id"))


def buscarTodosUsuarios():
    try:
        usuarios = list(db.usuarios.find().sort("nome"))
    except BaseException:
        raise ErroException("Erro ao buscar usuários")

    if len(usuarios) == 0:
        console.print(
            Panel.fit(
                "Nenhum usuário encontrado",
                border_style="red",
            )
        )

    for user in usuarios:
        try:
            user = Usuario.model_validate(user)
        except BaseException as e:
            continue

        printarUsuario(user)


def cadastrarUsuario(user: Usuario):
    try:
        user = Usuario.model_validate(user)
    except ValidationError:
        raise ErroException("Formato de usuário não suportado")

    exists = existeUsuario(user.email)
    if exists:
        raise ErroException("Usuário já existe")

    user_dump = user.model_dump()
    user_dump = {
        key: value["cpf"] if key == "cpf" else value for key, value in user_dump.items()
    }
    try:
        db.usuarios.insert_one(user_dump)
    except BaseException as e:
        print(e)
        raise ErroException("Erro ao criar registro do usuário")

    console.print(
        Panel(
            f"[bold green]✓ Usuário {user.nome} cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def updateUsuario(usuario: UsuarioUpdate, usuarioId: str):
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
        resultado = db.usuarios.update_one(
            {"_id": ObjectId(usuarioId)},
            {
                "$set": usuarioUpdateDump,
                "$pull": {
                    "favoritos": {"id_produto": {"$in": favoritosIds}},
                    "enderecos": {"id": {"$in": enderecosIds}},
                },
            },
        )
    except Exception as e:
        print(e)
        raise ErroException("Erro ao atualizar usuário")

    console.print(
        Panel(
            f"[bold green]✓ Usuario {usuario.nome} atualizado![/bold green]",
            title="Update",
            border_style="green",
        )
    )


def deletarUsuario(email, session):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo é inválido")

    exists = existeUsuario(email)
    if not exists:
        raise ErroException("Usuário não existente")

    try:
        db.usuarios.delete_one({"email": email}, session=session)
    except BaseException:
        raise ErroException("Usuário não foi deletado")


def loginUsuario(email: str, senha: str):
    email = email.strip()
    senha = senha.strip()

    if not email or not senha:
        raise ErroException("Valores nulos não são permitidos")

    try:
        usuario = db.usuarios.find_one({"email": email, "senha": senha})
    except BaseException:
        raise ErroException("Erro ao recuperar usuário")

    if not usuario:
        raise ErroException("Email ou senha inválido")

    return str(usuario.get("_id"))
