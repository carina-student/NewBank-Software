
from datetime import datetime
from enum import Enum

class Extrato:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def getTransacoes(self):
        return self.transacoes


class CategoriaTransacao(Enum):
    DEPOSITO = "deposito"
    ENVIO = "envio"

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

    def exibir_resumo(self):
        print(f"Valor: R$ {self.valor}")
        print(f"Categoria: {self.categoria.value}")
        print(f"Data: {self.data_operacao}")

        if self.categoria == CategoriaTransacao.DEPOSITO:
            print(f"Responsável: {self.responsavel}")