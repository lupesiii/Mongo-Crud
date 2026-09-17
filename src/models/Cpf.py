from pydantic import BaseModel, model_validator

def limpar_cpf(cpf):
  return ''.join(filter(str.isdigit, cpf))
class Cpf(BaseModel):
  cpf: str
  
  @model_validator(mode='before')
  def limpar(cls, values):
    if isinstance(values, dict):
      values['cpf'] = ''.join(filter(str.isdigit, values['cpf']))
    else:
      values = {"cpf": ''.join(filter(str.isdigit, values))}
    return values

  @model_validator(mode='after')
  def verificar(self):
    if len(self.cpf) != 11:
      raise ValueError('CPF deve possuir 11 dígitos')

    if not self.verificar_digito(9):
        raise ValueError('Primeiro dígito verificador inválido')

    if not self.verificar_digito(10):
        raise ValueError('Segundo dígito verificador inválido')

    return self
  
  def verificar_digito(self, posicao: int):
    qnt_digitos = posicao
    pesos = posicao + 1
    
    soma = sum(int(self.cpf[i]) * (pesos - i) for i in range(qnt_digitos))
    
    resto = soma % 11
    digito = 0 if resto < 2 else 11 - resto
    
    return digito == int(self.cpf[posicao])
