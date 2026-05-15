from datetime import datetime
from banco.extrato import CategoriaTransacao, Extrato, Transacao


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
     