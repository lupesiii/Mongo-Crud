from InquirerPy.validator import ValidationError
from models.Cpf import Cpf
from models.Email import Email
from pydantic import ValidationError as PydanticValidationError


def verificarVazio(texto):
    if len(texto.strip()) == 0:
        raise ValidationError(message="Este campo não pode ficar vazio!")
    return True


def verificarCpf(cpf):
    verificarVazio(cpf)

    try:
        CPF = Cpf(cpf=cpf)
    except PydanticValidationError:
        raise ValidationError(message="Este CPF não está válido!")

    is_valid = CPF.verificar()
    if not is_valid:
        raise ValidationError(message="Este CPF não está válido!")

    return True


def verificarEmail(email):
    verificarVazio(email)

    try:
        Email(email=email)
    except PydanticValidationError:
        raise ValidationError(message="Este Email não está válido!")
    return True


def verificarDecimal(valor):
    try:
        valor = float(valor)
    except ValueError:
        raise ValidationError(message="Este campo deve ser numérico!")

    if valor < 0:
        raise ValidationError(message="Este campo não pode ser negativo!")

    if "." in str(valor) and len(str(valor).split(".")[1]) > 2:
        raise ValidationError(message="São permitidas apenas 2 casas decimais")

    return True


def verificarInteiro(valor):
    try:
        valor = int(valor)
    except BaseException:
        raise ValidationError(message="Este campo deve ser numérico!")

    if valor < 0:
        raise ValidationError(message="Este campo não pode ser negativo!")

    if "." in str(valor) and len(str(valor).split(".")[1]) > 2:
        raise ValidationError(message="São permitidas apenas 2 casas decimais")

    return True


def transformarEmCentavos(valor):
    if "." in str(valor):
        partes = valor.split(".")
        valor = "".join(partes)

    return int(valor)
