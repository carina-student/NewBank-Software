from datetime import datetime
from banco.extrato import CategoriaTransacao, Extrato, Transacao
import pytest


def test_adicionar_transacao_registra_uma_transacao():
    # Arrange — criar transação extrato
    extrato = Extrato()

    transacao = Transacao(
        valor=150.21,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Maria"
    )

    # act - Adicionando extrato na transacao
    extrato.adicionar_transacao(transacao=transacao)

    # assert - Testando se foi adicionado uma transacao ao extrato
    assert len(extrato.getTransacoes())== 1

def test_adicionar_transacao_com_valor_none_deve_lancar_excecao():
    extrato = Extrato()

    transacaoComValorNone = Transacao(
        valor=None,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Maria"
    )

    with pytest.raises(ValueError):
        extrato.adicionar_transacao(transacao=transacaoComValorNone)

def test_adicionar_transacao_com_valor_diferente_de_decimal_deve_lancar_excecao():
    extrato = Extrato()

    transacaoComValorString = Transacao(
        valor="teste",
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Humberto"
    )

    with pytest.raises(ValueError):
        extrato.adicionar_transacao(transacao=transacaoComValorString)

def test_adicionar_transacao_com_valor_negativo_deve_lancar_excecao():
    extrato = Extrato()

    transacaoComValorNegativo= Transacao(
        valor=-200,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Arnaldo"
    )

    with pytest.raises(ValueError):
        extrato.adicionar_transacao(transacao=transacaoComValorNegativo)

def test_adicionar_transacao_com_valor_zerado_deve_lancar_excecao():
    extrato = Extrato()

    transacaoComValorNegativo = Transacao(
        valor=0,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Arnaldo"
    )

    with pytest.raises(ValueError):
        extrato.adicionar_transacao(transacao=transacaoComValorNegativo)


def test_adicionar_transacao_com_categoria_invalida_deve_lancar_excecao():
    extrato = Extrato()
    transacao = Transacao(
        valor=100,
        categoria="invalida",
        data_operacao=datetime.now(),
    )

    with pytest.raises(ValueError):
        extrato.adicionar_transacao(transacao)


def test_get_transacao_deve_retornar_transacoes_atuais():
    extrato = Extrato()

    transacao = Transacao(
        valor=150.21,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Maria"
    )

    transacao2 = Transacao(
        valor=100,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Maria"
    )

    transacao3 = Transacao(
        valor=30.3,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Maria"
    )

    extrato.adicionar_transacao(transacao=transacao)
    extrato.adicionar_transacao(transacao=transacao2)
    extrato.adicionar_transacao(transacao=transacao3)

    assert len(extrato.getTransacoes())== 3


def test_emitir_extrato_deve_vir_vazio():
    extrato = Extrato()

    assert len(extrato.getTransacoes()) == 0

def test_calcular_entradas_em_extrato_com_entradas():
    extrato = Extrato()

    transacao = Transacao(
        valor=50,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Bispo codex"
    )

    transacao2 = Transacao(
        valor=20,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Bispo codex"
    )

    transacao3 = Transacao(
        valor=100,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Bispo codex"
    )

    extrato.adicionar_transacao(transacao=transacao)
    extrato.adicionar_transacao(transacao=transacao2)
    extrato.adicionar_transacao(transacao=transacao3)

    assert extrato.calcularTotalEntradas() == 170


def test_calcular_entradas_em_extrato_vazio():
    extrato = Extrato()
    assert extrato.calcularTotalEntradas() == 0


def test_calcular_entradas_em_extrato_com_entradas_e_saidas():
    extrato = Extrato()

    transacao = Transacao(
        valor=50,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Evandro Java"
    )

    transacao2 = Transacao(
        valor=20,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Evandro Java"
    )

    transacao3 = Transacao(
        valor=100,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Alberto Python"
    )

    transacao4 = Transacao(
        valor=100,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Alberto Python"
    )

    transacao5 = Transacao(
        valor=20,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Alberto Python"
    )

    extrato.adicionar_transacao(transacao=transacao)
    extrato.adicionar_transacao(transacao=transacao2)
    extrato.adicionar_transacao(transacao=transacao3)
    extrato.adicionar_transacao(transacao=transacao4)
    extrato.adicionar_transacao(transacao=transacao5)

    assert extrato.calcularTotalEntradas() == 170



def test_calcular_total_saidas_em_extrato_com_saidas():
    extrato = Extrato()

    transacao = Transacao(
        valor=100,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    transacao2 = Transacao(
        valor=300,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    transacao3 = Transacao(
        valor=20,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    extrato.adicionar_transacao(transacao=transacao)
    extrato.adicionar_transacao(transacao=transacao2)
    extrato.adicionar_transacao(transacao=transacao3)

    assert extrato.calcularTotalSaidas() == 420


def test_calcular_total_saidas_em_extrato_vazio():
    extrato = Extrato()
    assert extrato.calcularTotalSaidas() == 0


def test_calcular_total_saidas_em_extrato_com_entradas_e_saidas():
    extrato = Extrato()

    transacao = Transacao(
        valor=30,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    transacao2 = Transacao(
        valor=5,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    transacao3 = Transacao(
        valor=50,
        categoria=CategoriaTransacao.DEPOSITO,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    transacao4 = Transacao(
        valor=20,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    transacao5 = Transacao(
        valor=10,
        categoria=CategoriaTransacao.SAQUE,
        data_operacao=datetime.now(),
        responsavel="Pedro Spring"
    )

    extrato.adicionar_transacao(transacao=transacao)
    extrato.adicionar_transacao(transacao=transacao2)
    extrato.adicionar_transacao(transacao=transacao3)
    extrato.adicionar_transacao(transacao=transacao4)
    extrato.adicionar_transacao(transacao=transacao5)

    assert extrato.calcularTotalSaidas() == 30
