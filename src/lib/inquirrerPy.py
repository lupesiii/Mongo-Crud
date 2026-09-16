from InquirerPy.validator import ValidationError

def verificar_vazio(texto):
    if len(texto.strip()) == 0:
        raise ValidationError(message="Este campo não pode ficar vazio!")
    return True