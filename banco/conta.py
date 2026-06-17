import math


class SaldoInsuficienteException(Exception):
    """Exceção lançada quando o saldo é insuficiente para uma operação"""
    pass


class ContaBancaria:
    def __init__(self, saldo_inicial=0, numero_conta=None):
        self._validar_valor(saldo_inicial, permitir_zero=True)
        self.saldo = saldo_inicial
        self.numero_conta = numero_conta

    def depositar(self, valor):
        """Adiciona valor ao saldo da conta
        
        Args:
            valor: Valor a depositar (deve ser positivo)
            
        Raises:
            ValueError: Se o valor for negativo ou zero
        """
        self._validar_valor(valor)
        self.saldo += valor

    def sacar(self, valor):
        """Remove valor do saldo da conta
        
        Args:
            valor: Valor a sacar
            
        Raises:
            ValueError: Se o valor for negativo ou zero
            SaldoInsuficienteException: Se o saldo for insuficiente
        """
        self._validar_valor(valor)
        if valor > self.saldo:
            raise SaldoInsuficienteException("Saldo insuficiente para este saque")
        self.saldo -= valor

    @staticmethod
    def _validar_valor(valor, permitir_zero=False):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("O valor deve ser numérico")
        if not math.isfinite(valor):
            raise ValueError("O valor deve ser finito")
        if valor < 0 or (valor == 0 and not permitir_zero):
            raise ValueError("O valor deve ser positivo")

    def getSaldo(self):
        """Retorna o saldo atual da conta"""
        return self.saldo

    def getNumeroConta(self):
        """Retorna o número da conta"""
        return self.numero_conta
