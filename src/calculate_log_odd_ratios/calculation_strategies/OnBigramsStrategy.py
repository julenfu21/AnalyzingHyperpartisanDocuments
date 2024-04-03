from collections import defaultdict
from itertools import pairwise

from tqdm import tqdm

from src.calculate_log_odd_ratios.CalculationStrategy import CalculationStrategy
from src.calculate_log_odd_ratios.DocumentGroup import DocumentGroup
from src.constant_values.enums import DocumentType


class OnBigramsStrategy(CalculationStrategy):

    def __init__(
            self,
            hyperpartisan_documents_list: list[list[str]],
            non_hyperpartisan_documents_list: list[list[str]]
    ):
        self.hyperpartisan_documents = DocumentGroup(document_list=hyperpartisan_documents_list)
        self.non_hyperpartisan_documents = DocumentGroup(document_list=non_hyperpartisan_documents_list)

        self.hyperpartisan_bigrams_frequencies = defaultdict(int)
        self.non_hyperpartisan_bigrams_frequencies = defaultdict(int)

        self.all_bigrams_list = []

        self.log_odd_ratios: dict[tuple[str, str], float] = {}

    def calculate_log_odd_ratios(self) -> None:
        # Get bigrams frequencies for each of documents lists
        self.__get_bigrams_frequency_on_document_list__(
            document_group=self.hyperpartisan_documents,
            document_type=DocumentType.HYPERPARTISAN,
            bigrams_frequencies=self.hyperpartisan_bigrams_frequencies
        )
        self.__get_bigrams_frequency_on_document_list__(
            document_group=self.non_hyperpartisan_documents,
            document_type=DocumentType.NON_HYPERPARTISAN,
            bigrams_frequencies=self.non_hyperpartisan_bigrams_frequencies
        )

        # Calculate and store log-odd ratios
        p_on_hyperpartisan = self.__get_p_on_document_list__(
            document_group=self.hyperpartisan_documents,
            bigrams_frequencies=self.hyperpartisan_bigrams_frequencies
        )
        p_on_non_hyperpartisan = self.__get_p_on_document_list__(
            document_group=self.non_hyperpartisan_documents,
            bigrams_frequencies=self.non_hyperpartisan_bigrams_frequencies
        )

    def __get_bigrams_frequency_on_document_list__(
            self,
            document_group: DocumentGroup,
            document_type: DocumentType,
            bigrams_frequencies: defaultdict[tuple[str, str], int]
    ) -> None:
        for document in tqdm(document_group.document_list, desc="GettinGettinGettinGettinGetting bigrams frequencies..."):
            for token_1, token_2 in pairwise(document):
                bigram = (token_1, token_2)
                bigrams_frequencies[bigram] += 1
                self.all_bigrams_list.append(bigram)

        self.all_bigrams_list = list(set(self.all_bigrams_list))
        most_frequent_bigrams = self.__get_n_highest_values_from_dictionary__(dictionary=bigrams_frequencies, n=10)
        # This should only be printed once both document groups are traversed
        print(f'Most frequent tokens ({document_type.value}): {most_frequent_bigrams}')

    def __get_p_on_document_list__(
            self,
            document_group: DocumentGroup,
            bigrams_frequencies: defaultdict[tuple[str, str], int]
    ) -> dict[tuple[str, str], float]:
        for document in tqdm(document_group.document_list, desc="Calculating p values..."):
            p_on_document_list = {}

            for token_1, token2 in pairwise(document):
                bigram = (token_1, token2)
                p_on_document_list[bigram] = self.__get_p_on_bigram__(
                    bigram=bigram,
                    document_group=document_group,
                    bigrams_frequencies=bigrams_frequencies
                )

            highest_values = self.__get_n_highest_values_from_dictionary__(dictionary=p_on_document_list, n=10)
            print(f'Highest p values: {highest_values}')

            return p_on_document_list

    @staticmethod
    def __get_p_on_bigram__(
            bigram: tuple[str, str],
            document_group: DocumentGroup,
            bigrams_frequencies: defaultdict[tuple[str, str], int]
    ) -> float:
        bigram_frequency = bigrams_frequencies[bigram]
        document_group_size = document_group.word_count

        return bigram_frequency / document_group_size

    @staticmethod
    def __get_n_highest_values_from_dictionary__(dictionary: dict, n: int = 50) -> dict:
        highest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        return dict(list(highest_values.items())[:n])
