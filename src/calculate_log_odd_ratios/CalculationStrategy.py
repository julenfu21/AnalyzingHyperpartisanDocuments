from abc import ABC, abstractmethod
from typing import List


class CalculationStrategy(ABC):

    @abstractmethod
    def calculate_log_odd_ratios(self):
        pass
