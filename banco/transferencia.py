class Transferencia:

    def __init__(self, conta_origem, conta_destino, valor_transacao):
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor_transacao = valor_transacao

    def executar(self):
        self.conta_origem.sacar(self.valor_transacao)
        self.conta_destino.depositar(self.valor_transacao)