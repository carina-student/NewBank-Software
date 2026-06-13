import pytest
from banco.juros import CalculadoraJuros


def test_calcular_juros_simples():
    calc = CalculadoraJuros(taxa=0.1)
    # 1000 * (1 + 0.1 * 2) = 1200
    assert calc.calcularJurosSimples(1000, 2) == pytest.approx(1200)


def test_calcular_juros_simples_com_taxa_zero():
    calc = CalculadoraJuros(taxa=0.0)
    assert calc.calcularJurosSimples(500, 5) == pytest.approx(500)


def test_calcular_juros_compostos():
    calc = CalculadoraJuros(taxa=0.1)
    # 1000 * (1.1) ** 2 = 1210
    assert calc.calcularJurosCompostos(1000, 2) == pytest.approx(1210)


def test_calcular_juros_compostos_com_taxa_zero():
    calc = CalculadoraJuros(taxa=0.0)
    assert calc.calcularJurosCompostos(500, 5) == pytest.approx(500)


def test_get_taxa_deve_retornar_taxa_atual():
    calc = CalculadoraJuros(taxa=0.05)
    assert calc.getTaxa() == 0.05


def test_set_taxa_deve_atualizar_taxa():
    calc = CalculadoraJuros(taxa=0.05)
    calc.setTaxa(0.15)
    assert calc.getTaxa() == 0.15


def test_set_taxa_negativa_deve_lancar_excecao():
    calc = CalculadoraJuros(taxa=0.05)
    with pytest.raises(ValueError):
        calc.setTaxa(-0.1)


def test_construtor_com_taxa_negativa_deve_lancar_excecao():
    with pytest.raises(ValueError):
        CalculadoraJuros(taxa=-0.1)


def test_calculo_sem_capital_deve_lancar_excecao():
    calc = CalculadoraJuros(taxa=0.1)
    with pytest.raises(ValueError):
        calc.calcularJurosSimples(None, 2)
