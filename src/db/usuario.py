from cli import printarUsuario
from models.ErroException import ErroException
from models.Usuario import Usuario
from lib.mongoConnection import db
from rich.panel import Panel
from pydantic import ValidationError
from lib.rich import console


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

    if allow_Print:
        try:
            user = Usuario.model_validate(user)
        except BaseException as e:
            raise ErroException("Erro ao converter usuário")

        printarUsuario(user)
    return user


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
    except BaseException:
        raise ErroException("Erro ao criar registro do usuário")

    console.print(
        Panel(
            f"[bold green]✓ Usuário {user.nome} cadastrado com sucesso![/bold green]",
            title="Cadastro",
            border_style="green",
        )
    )


def deletarUsuario(email):
    email = email.strip()

    if not email:
        raise ErroException("Valor nulo é inválido")

    exists = existeUsuario(email)
    if not exists:
        raise ErroException("Usuário não existente")

    try:
        db.usuarios.delete_one({"email": email})
        console.print(
            Panel(
                f"[bold green]✓ Usuário deletado com sucesso![/bold green]",
                title="Delete",
                border_style="green",
            )
        )
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

    console.print(
        Panel(
            f"[bold green]✓ Usuario {usuario.get("nome")} logado![/bold green]",
            title="Login",
            border_style="green",
        )
    )

    return str(usuario.get("_id"))
