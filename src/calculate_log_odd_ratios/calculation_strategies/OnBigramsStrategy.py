from collections import defaultdict

from src.calculate_log_odd_ratios.CalculationStrategy import CalculationStrategy
from src.calculate_log_odd_ratios.DocumentGroup import DocumentGroup


class OnBigramsStrategy(CalculationStrategy):

    def __init__(
            self,
            hyperpartisan_documents_list: list[list[str]],
            non_hyperpartisan_documents_list: list[list[str]]
    ):
        self.hyperpartisan_documents = DocumentGroup(document_list=hyperpartisan_documents_list)
        self.non_hyperpartisan_documents = DocumentGroup(document_list=non_hyperpartisan_documents_list)

        self.hyperpartisan_tokens_frequencies = defaultdict(int)
        self.non_hyperpartisan_tokens_frequencies = defaultdict(int)

        self.all_tokens_list = []

        self.log_odd_ratios: dict[str, float] = {}

    def calculate_log_odd_ratios(self) -> None:
        print("Not implemented yet")
