
from datetime import datetime
from enum import Enum

class Extrato:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):

        if not isinstance(transacao.valor, (int, float)):
            raise ValueError("O valor da transação deve ser numérico")
        
        if transacao.valor <= 0:
            raise ValueError("O valor da transação deve ser positivo")

        self.transacoes.append(transacao)

    def getTransacoes(self):
        return self.transacoes
    
    def calcularTotalEntradas(self):
        return sum(
            transacao.valor 
            for transacao in self.transacoes
            if transacao.categoria == CategoriaTransacao.DEPOSITO
        )

    def calcularTotalSaidas(self):
        return sum(
            transacao.valor 
            for transacao in self.transacoes
            if transacao.categoria == CategoriaTransacao.SAQUE
        )



class CategoriaTransacao(Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"

class Transacao:

    def __init__(
        self,
        valor: float,
        categoria: CategoriaTransacao,
        data_operacao: datetime,
        responsavel: str = None
    ):
        self.valor = valor
        self.categoria = categoria
        self.data_operacao = data_operacao
        self.responsavel = responsavel