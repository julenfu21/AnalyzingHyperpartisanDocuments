from src.calculate_log_odd_ratios import CalculationStrategy


class LogOddRatiosCalculator:

    def __init__(self, strategy: CalculationStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> CalculationStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: CalculationStrategy) -> None:
        self._strategy = strategy

    def calculate_log_odd_ratios(self) -> None:
        self._strategy.calculate_log_odd_ratios()
