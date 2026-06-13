import math


class CalculadoraJuros:
    def __init__(self, taxa: float = 0.0):
        self._taxa = 0.0
        self.setTaxa(taxa)

    def calcularJurosSimples(self, capital: float, tempo: float) -> float:
        """Retorna o montante com juros simples: capital * (1 + taxa * tempo)"""
        self._validar_parametros(capital, tempo)
        return capital * (1 + self._taxa * tempo)

    def calcularJurosCompostos(self, capital: float, tempo: float) -> float:
        """Retorna o montante com juros compostos: capital * (1 + taxa) ** tempo"""
        self._validar_parametros(capital, tempo)
        return capital * (1 + self._taxa) ** tempo

    def getTaxa(self) -> float:
        return self._taxa

    def setTaxa(self, nova_taxa: float):
        """Define nova taxa de juros.

        Raises:
            ValueError: Se a taxa for negativa
        """
        self._validar_numero(nova_taxa, "A taxa de juros")
        if nova_taxa < 0:
            raise ValueError("A taxa de juros não pode ser negativa")
        self._taxa = nova_taxa

    @classmethod
    def _validar_parametros(cls, capital, tempo):
        cls._validar_numero(capital, "O capital")
        cls._validar_numero(tempo, "O tempo")
        if capital < 0:
            raise ValueError("O capital não pode ser negativo")
        if tempo < 0:
            raise ValueError("O tempo não pode ser negativo")

    @staticmethod
    def _validar_numero(valor, nome):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"{nome} deve ser numérico")
        if not math.isfinite(valor):
            raise ValueError(f"{nome} deve ser finito")
