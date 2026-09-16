class Cpf:
  def __init__(self, cpf: str):
    self.cpf = self.limpar(cpf)
    
  @staticmethod
  def limpar(cpf: str):
    return ''.join(filter(str.isdigit, cpf))

  def verificar(self):
    if len(self.cpf) != 11:
      return False
    
    if self.verificar_digito(9) and self.verificar_digito(10):
      return True
    return False
  
  def verificar_digito(self, posicao: int):
    qnt_digitos = posicao
    pesos = posicao + 1
    
    soma = sum(int(self.cpf[i]) * (pesos - i) for i in range(qnt_digitos))
    
    resto = soma % 11
    digito = 0 if resto < 2 else 11 - resto
    
    return digito == int(self.cpf[posicao])
