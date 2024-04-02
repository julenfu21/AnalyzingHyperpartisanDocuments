import math
from collections import defaultdict

from tqdm import tqdm

from src.constant_values.enums import DocumentType
from src.calculate_log_odd_ratios.DocumentGroup import DocumentGroup


class LogOddRatiosCalculator:

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

    def calculate_log_odd_ratios(self):
        # Get tokens frequencies for each of the documents lists
        self.__get_tokens_frequency_on_document_list__(
            document_group=self.hyperpartisan_documents,
            document_type=DocumentType.HYPERPARTISAN,
            tokens_frequencies=self.hyperpartisan_tokens_frequencies
        )
        self.__get_tokens_frequency_on_document_list__(
            document_group=self.non_hyperpartisan_documents,
            document_type=DocumentType.NON_HYPERPARTISAN,
            tokens_frequencies=self.non_hyperpartisan_tokens_frequencies
        )

        # Calculate and store in 'self.calculate_log_odd_ratios'
        p_on_hyperpartisan = self.__get_p_on_document_list__(
            document_group=self.hyperpartisan_documents,
            tokens_frequencies=self.hyperpartisan_tokens_frequencies
        )
        p_on_non_hyperpartisan = self.__get_p_on_document_list__(
            document_group=self.non_hyperpartisan_documents,
            tokens_frequencies=self.non_hyperpartisan_tokens_frequencies
        )

        o_on_hyperpartisan = self.__get_o_on_document_list__(
            p_on_document_list=p_on_hyperpartisan
        )
        o_on_non_hyperpartisan = self.__get_o_on_document_list__(
            p_on_document_list=p_on_non_hyperpartisan
        )

        self.log_odd_ratios = self.__get_r_on_full_corpus__(
            o_on_hyperpartisan=o_on_hyperpartisan,
            o_on_not_hyperpartisan=o_on_non_hyperpartisan
        )

        highest_values = self.__get_n_highest_values_from_dictionary__(dictionary=self.log_odd_ratios)
        print(f'Highest log-odd ratios: {highest_values}')

        lowest_values = self.__get_n_lowest_values_from_dictionary__(dictionary=self.log_odd_ratios)
        print(f'Lowest log-odd ratios: {lowest_values}')

    def __get_tokens_frequency_on_document_list__(
            self,
            document_group: DocumentGroup,
            document_type: DocumentType,
            tokens_frequencies: defaultdict[str, int]
    ) -> None:
        for document in document_group.document_list:
            for token in document:
                tokens_frequencies[token] += 1
                self.all_tokens_list.append(token)

        self.all_tokens_list = list(set(self.all_tokens_list))
        most_frequent_tokens = self.__get_n_highest_values_from_dictionary__(dictionary=tokens_frequencies, n=10)
        print(f'Most frequent tokens ({document_type.value}): {most_frequent_tokens}')

    def __get_p_on_document_list__(
            self,
            document_group: DocumentGroup,
            tokens_frequencies: defaultdict[str, int]
    ) -> dict[str, float]:
        p_on_document_list = {}

        for document in tqdm(document_group.document_list, desc="Calculating p values..."):
            for token in document:
                p_on_document_list[token] = self.__get_p_on_token__(
                    token=token,
                    document_group=document_group,
                    tokens_frequencies=tokens_frequencies
                )

        highest_values = self.__get_n_highest_values_from_dictionary__(dictionary=p_on_document_list, n=10)
        print(f'Highest p values: {highest_values}')

        return p_on_document_list

    @staticmethod
    def __get_p_on_token__(
            token: str,
            document_group: DocumentGroup,
            tokens_frequencies: defaultdict[str, int]
    ) -> float:
        token_frequency = tokens_frequencies[token]
        document_group_size = document_group.word_count

        return token_frequency / document_group_size

    def __get_o_on_document_list__(self, p_on_document_list: dict[str, float]) -> defaultdict[str, float]:
        o_values = {token: self.__get_o_on_token__(p_on_token=p_value) for token, p_value in p_on_document_list.items()}
        highest_values = self.__get_n_highest_values_from_dictionary__(dictionary=o_values, n=10)
        print(f'Highest o values: {highest_values}')
        return defaultdict(float, o_values)

    @staticmethod
    def __get_o_on_token__(p_on_token: float) -> float:
        return p_on_token / (1 - p_on_token)

    def __get_r_on_full_corpus__(
            self,
            o_on_hyperpartisan: dict[str, float],
            o_on_not_hyperpartisan: dict[str, float]
    ) -> dict[str, float]:
        r_on_full_corpus = {}

        for token in self.all_tokens_list:
            try:
                r_on_current_token = self.__get_r_on_token__(
                    o_on_token_and_hyperpartisan=o_on_hyperpartisan[token],
                    o_on_token_and_non_hyperpartisan=o_on_not_hyperpartisan[token]
                )
                r_on_full_corpus[token] = r_on_current_token
            except ValueError:
                continue

        return r_on_full_corpus

    @staticmethod
    def __get_r_on_token__(o_on_token_and_hyperpartisan: float, o_on_token_and_non_hyperpartisan) -> float:
        return math.log(o_on_token_and_hyperpartisan, 10) - math.log(o_on_token_and_non_hyperpartisan, 10)

    @staticmethod
    def __get_n_highest_values_from_dictionary__(dictionary: dict, n: int = 50) -> dict:
        highest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        return dict(list(highest_values.items())[:n])

    @staticmethod
    def __get_n_lowest_values_from_dictionary__(dictionary: dict, n: int = 50) -> dict:
        highest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=False))
        return dict(list(highest_values.items())[:n])
