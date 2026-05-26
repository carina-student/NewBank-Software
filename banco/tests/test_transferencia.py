import pytest

from banco.conta import ContaBancaria
from banco.transferencia import Transferencia


class TestTransferencia:

    def test_deve_transferir_valor_quando_saldo_for_suficiente(self):

        conta_origem = ContaBancaria(1000.0, "001")
        conta_destino = ContaBancaria(500.0, "002")

        transferencia = Transferencia(
            conta_origem,
            conta_destino,
            300.0
        )

        transferencia.executar()

        assert conta_origem.getSaldo() == 700.0
        assert conta_destino.getSaldo() == 800.0
    
    def test_deve_lancar_excecao_quando_saldo_for_insuficiente(self):

        conta_origem = ContaBancaria(100.0, "001")
        conta_destino = ContaBancaria(500.0, "002")

        transferencia = Transferencia(
            conta_origem,
            conta_destino,
            1000.0
        )

        with pytest.raises(Exception):
            transferencia.executar()

    def test_nao_deve_permitir_transferencia_para_mesma_conta(self):

        conta = ContaBancaria(1000.0, "001")

        transferencia = Transferencia(
            conta,
            conta,
            100.0
        )

        with pytest.raises(ValueError):
            transferencia.executar()

    def test_nao_deve_permitir_valor_negativo(self):

        conta_origem = ContaBancaria(1000.0, "001")
        conta_destino = ContaBancaria(500.0, "002")

        transferencia = Transferencia(
            conta_origem,
            conta_destino,
            -50.0
        )

        with pytest.raises(ValueError):
            transferencia.executar()