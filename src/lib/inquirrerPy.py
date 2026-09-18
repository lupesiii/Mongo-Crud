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
