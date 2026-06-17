class Transferencia:

    def __init__(self, conta_origem, conta_destino, valor_transacao):
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor_transacao = valor_transacao

    def executar(self):

        self._validar_contas()
        self._validar_valor()

        self.conta_origem.sacar(self.valor_transacao)
        self.conta_destino.depositar(self.valor_transacao)

    def _validar_contas(self):

        if self.conta_origem == self.conta_destino:
            raise ValueError(
                "Conta origem e destino não podem ser iguais"
            )

    def _validar_valor(self):

        if isinstance(self.valor_transacao, bool) or not isinstance(
            self.valor_transacao, (int, float)
        ):
            raise ValueError("Valor da transferência deve ser numérico")

        if self.valor_transacao <= 0:
            raise ValueError(
                "Valor da transferência deve ser positivo"
            )
