from banco.conta import ContaBancaria

def test_criar_conta_com_saldo_inicial():
    conta = ContaBancaria(saldo_inicial=100)
    assert conta.saldo == 100