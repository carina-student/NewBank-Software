from banco.conta import ContaBancaria, SaldoInsuficienteException
import pytest

def test_criar_conta_com_saldo_inicial():
    conta = ContaBancaria(saldo_inicial=100)
    assert conta.getSaldo() == 100

def test_depositar_valor_positivo():
    """Deve aumentar o saldo quando depositar valor positivo"""
    conta = ContaBancaria(saldo_inicial=100)
    conta.depositar(50)
    assert conta.getSaldo() == 150

def test_depositar_valor_negativo_deve_lancar_excecao():
    """Deve lançar exceção ao tentar depositar valor negativo"""
    conta = ContaBancaria(saldo_inicial=100)
    with pytest.raises(ValueError):
        conta.depositar(-50)

def test_depositar_zero_deve_lancar_excecao():
    """Deve lançar exceção ao tentar depositar zero"""
    conta = ContaBancaria(saldo_inicial=100)
    with pytest.raises(ValueError):
        conta.depositar(0)

def test_sacar_valor_positivo_com_saldo_suficiente():
    """Deve diminuir o saldo quando sacar valor positivo com saldo suficiente"""
    conta = ContaBancaria(saldo_inicial=100)
    conta.sacar(30)
    assert conta.getSaldo() == 70

def test_sacar_valor_negativo_deve_lancar_excecao():
    """Deve lançar exceção ao tentar sacar valor negativo"""
    conta = ContaBancaria(saldo_inicial=100)
    with pytest.raises(ValueError):
        conta.sacar(-50)

def test_sacar_zero_deve_lancar_excecao():
    """Deve lançar exceção ao tentar sacar zero"""
    conta = ContaBancaria(saldo_inicial=100)
    with pytest.raises(ValueError):
        conta.sacar(0)

def test_sacar_com_saldo_insuficiente_deve_lancar_excecao():
    """Deve lançar exceção ao tentar sacar valor maior que o saldo"""
    conta = ContaBancaria(saldo_inicial=100)
    with pytest.raises(SaldoInsuficienteException):
        conta.sacar(150)

def test_get_saldo_deve_retornar_saldo_atual():
    """Deve retornar o saldo atual da conta"""
    conta = ContaBancaria(saldo_inicial=100)
    conta.depositar(50)
    conta.sacar(30)
    assert conta.getSaldo() == 120
