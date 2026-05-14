class SaldoInsuficienteException(Exception):
    """Exceção lançada quando o saldo é insuficiente para uma operação"""
    pass


class ContaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial

    def depositar(self, valor):
        """Adiciona valor ao saldo da conta
        
        Args:
            valor: Valor a depositar (deve ser positivo)
            
        Raises:
            ValueError: Se o valor for negativo ou zero
        """
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo")
        self.saldo += valor

    def sacar(self, valor):
        """Remove valor do saldo da conta
        
        Args:
            valor: Valor a sacar
            
        Raises:
            ValueError: Se o valor for negativo ou zero
            SaldoInsuficienteException: Se o saldo for insuficiente
        """
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo")
        if valor > self.saldo:
            raise SaldoInsuficienteException("Saldo insuficiente para este saque")
        self.saldo -= valor

    def getSaldo(self):
        """Retorna o saldo atual da conta"""
        return self.saldo
