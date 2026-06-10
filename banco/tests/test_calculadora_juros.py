import pytest
from banco.calculadora_juros import CalculadoraJuros


class TestCalculadoraJuros:
    """Testes para a Calculadora de Juros seguindo TDD"""
    
    def setup_method(self):
        """Configuração executada antes de cada teste"""
        self.calculadora = CalculadoraJuros(taxa=0.10)  # 10%
    
    # ==================== TESTES GET/SET TAXA ====================
    
    def test_deve_criar_calculadora_com_taxa_padrao(self):
        """Teste verifica se a taxa é inicializada corretamente"""
        assert self.calculadora.get_taxa() == 0.10
    
    def test_deve_alterar_taxa_corretamente(self):
        """Teste verifica se set_taxa altera o valor da taxa"""
        self.calculadora.set_taxa(0.15)
        assert self.calculadora.get_taxa() == 0.15
    
    def test_nao_deve_aceitar_taxa_negativa(self):
        """Teste verifica se taxa negativa lança exceção"""
        with pytest.raises(ValueError, match="Taxa não pode ser negativa"):
            self.calculadora.set_taxa(-0.05)
    
    def test_nao_deve_aceitar_taxa_maior_que_100_porcento(self):
        """Teste verifica se taxa > 100% lança exceção"""
        with pytest.raises(ValueError, match="Taxa não pode ser maior que 100%"):
            self.calculadora.set_taxa(1.5)  # 150%
    
    # ==================== TESTES JUROS SIMPLES ====================
    
    def test_deve_calcular_juros_simples_corretamente(self):
        """Teste: J = C * i * t = 1000 * 0.10 * 3 = 300"""
        resultado = self.calculadora.calcular_juros_simples(
            capital=1000.0, tempo=3
        )
        assert resultado == 300.0
    
    def test_juros_simples_com_capital_zero(self):
        """Teste: capital zero deve retornar zero"""
        resultado = self.calculadora.calcular_juros_simples(
            capital=0.0, tempo=5
        )
        assert resultado == 0.0
    
    def test_juros_simples_com_tempo_zero(self):
        """Teste: tempo zero deve retornar zero"""
        resultado = self.calculadora.calcular_juros_simples(
            capital=1000.0, tempo=0
        )
        assert resultado == 0.0
    
    def test_juros_simples_nao_deve_aceitar_capital_negativo(self):
        """Teste: capital negativo deve lançar exceção"""
        with pytest.raises(ValueError, match="Capital não pode ser negativo"):
            self.calculadora.calcular_juros_simples(capital=-100.0, tempo=2)
    
    def test_juros_simples_nao_deve_aceitar_tempo_negativo(self):
        """Teste: tempo negativo deve lançar exceção"""
        with pytest.raises(ValueError, match="Tempo não pode ser negativo"):
            self.calculadora.calcular_juros_simples(capital=1000.0, tempo=-1)
    
    # ==================== TESTES JUROS COMPOSTOS ====================
    
    def test_deve_calcular_juros_compostos_corretamente(self):
        """Teste: M = C * (1+i)^t, Juros = M - C
           Capital: 1000, Taxa: 0.10, Tempo: 3
           M = 1000 * (1.10)^3 = 1331, Juros = 331"""
        resultado = self.calculadora.calcular_juros_compostos(
            capital=1000.0, tempo=3
        )
        assert round(resultado, 2) == 331.00
    
    def test_juros_compostos_com_capital_zero(self):
        """Teste: capital zero deve retornar zero"""
        resultado = self.calculadora.calcular_juros_compostos(
            capital=0.0, tempo=5
        )
        assert resultado == 0.0
    
    def test_juros_compostos_com_tempo_zero(self):
        """Teste: tempo zero deve retornar zero"""
        resultado = self.calculadora.calcular_juros_compostos(
            capital=1000.0, tempo=0
        )
        assert resultado == 0.0
    
    def test_juros_compostos_nao_deve_aceitar_capital_negativo(self):
        """Teste: capital negativo deve lançar exceção"""
        with pytest.raises(ValueError, match="Capital não pode ser negativo"):
            self.calculadora.calcular_juros_compostos(capital=-100.0, tempo=2)
    
    def test_juros_compostos_nao_deve_aceitar_tempo_negativo(self):
        """Teste: tempo negativo deve lançar exceção"""
        with pytest.raises(ValueError, match="Tempo não pode ser negativo"):
            self.calculadora.calcular_juros_compostos(capital=1000.0, tempo=-1)