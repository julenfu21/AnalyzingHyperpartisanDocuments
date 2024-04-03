import math
from collections import defaultdict
from itertools import pairwise

from tqdm import tqdm

from src.calculate_log_odd_ratios.DocumentGroup import DocumentGroup
from src.constant_values.enums import DocumentType, TokenType


class LogOddRatiosCalculatorV2:

    def __init__(
            self,
            hyperpartisan_documents: list[list[str]],
            non_hyperpartisan_documents: list[list[str]],
            token_type: TokenType
    ) -> None:
        self.hyperpartisan_document_group = DocumentGroup(document_list=hyperpartisan_documents)
        self.non_hyperpartisan_document_group = DocumentGroup(document_list=non_hyperpartisan_documents)
        self.token_type = token_type

        self.all_tokens = set()
        self.log_odd_ratios: dict[str, float] = {}

        self.hyperpartisan_tokens_frequency = defaultdict(int)
        self.non_hyperpartisan_tokens_frequency = defaultdict(int)
        self.__set_tokens_frequency__()

    def __set_tokens_frequency__(self) -> None:
        self.hyperpartisan_tokens_frequency = self.__calculate_tokens_frequency__(
            document_list=self.hyperpartisan_document_group.document_list
        )

        self.non_hyperpartisan_tokens_frequency = self.__calculate_tokens_frequency__(
            document_list=self.non_hyperpartisan_document_group.document_list
        )

    def __calculate_tokens_frequency__(self, document_list: list[list[str]]) -> defaultdict[str | tuple[str, str], int]:
        tokens_frequency = defaultdict(int)

        match self.token_type:
            case TokenType.UNIGRAM:
                for document in tqdm(document_list, desc="Calculating tokens frequency..."):
                    for unigram in document:
                        tokens_frequency[unigram] += 1
                        self.all_tokens.add(unigram)
            case TokenType.BIGRAM:
                for document in tqdm(document_list, desc="Calculating tokens frequency..."):
                    for token_1, token_2 in pairwise(document):
                        bigram = (token_1, token_2)
                        tokens_frequency[bigram] += 1
                        self.all_tokens.add(bigram)

        return tokens_frequency

    def calculate_log_odd_ratios(self) -> None:
        hyperpartisan_o_values, non_hyperpartisan_o_values = self.calculate_o_values()
        print("Calculating log-odd ratios ...")
        self.log_odd_ratios = {token: self.calculate_r_value_on_token(
            token=token,
            hyperpartisan_o_values=hyperpartisan_o_values,
            non_hyperpartisan_o_values=non_hyperpartisan_o_values
        ) for token in self.all_tokens}
        print("log-odd ratios calculated successfully.")

    def calculate_r_value_on_token(
            self,
            token: str | tuple[str, str],
            hyperpartisan_o_values: dict[str, float],
            non_hyperpartisan_o_values: dict[str, float]
    ) -> float:
        return self.__log__(hyperpartisan_o_values[token]) - self.__log__(non_hyperpartisan_o_values[token])

    @staticmethod
    def __log__(number: float) -> float:
        try:
            return math.log(number, 10)
        except ValueError:
            return float('-inf')

    def calculate_o_values(self) -> tuple[defaultdict[str, float], defaultdict[str, float]]:
        hyperpartisan_o_values = self.__calculate_o_values_on_document_group__(
            tokens_frequency=self.hyperpartisan_tokens_frequency,
            document_group=self.hyperpartisan_document_group
        )
        del self.hyperpartisan_document_group
        del self.hyperpartisan_tokens_frequency

        non_hyperpartisan_o_values = self.__calculate_o_values_on_document_group__(
            tokens_frequency=self.non_hyperpartisan_tokens_frequency,
            document_group=self.non_hyperpartisan_document_group
        )
        del self.non_hyperpartisan_document_group
        del self.non_hyperpartisan_tokens_frequency

        return defaultdict(float, hyperpartisan_o_values), defaultdict(float, non_hyperpartisan_o_values)

    def __calculate_o_values_on_document_group__(
            self,
            tokens_frequency: defaultdict[str | tuple[str, str], int],
            document_group: DocumentGroup
    ) -> dict[str, float]:
        print("Calculating o values ...")
        o_values = {token: self.__calculate_o_value_on_token__(
            token=token, tokens_frequency=tokens_frequency, document_group=document_group
        ) for token in tokens_frequency.keys()}
        print("o values calculated successfully.")

        self.__print_tokens_by_descending_order__(dictionary=o_values)
        return o_values

    def __calculate_o_value_on_token__(
            self,
            token: str | tuple[str, str],
            tokens_frequency: defaultdict[str | tuple[str, str], int],
            document_group: DocumentGroup
    ) -> float:
        p_on_token = self.__calculate_p_value_on_token__(
            token=token,
            tokens_frequency=tokens_frequency,
            document_group=document_group
        )
        return p_on_token / (1 - p_on_token)

    @staticmethod
    def __calculate_p_value_on_token__(
            token: str | tuple[str, str],
            tokens_frequency: defaultdict[str | tuple[str, str], int],
            document_group: DocumentGroup
    ) -> float:
        token_frequency = tokens_frequency[token]
        document_group_size = document_group.word_count

        return token_frequency / document_group_size

    @staticmethod
    def __print_tokens_by_descending_order__(dictionary: dict) -> None:
        sorted_values = dict(sorted(
            dictionary.items(),
            key=lambda item: item[1],
            reverse=True)
        )
        print(f'Highest values: {dict(list(sorted_values.items())[:20])} ...')

    def get_most_relevant_words(
            self,
            document_type: DocumentType,
            amount: int = 50,
    ) -> dict[str | tuple[str, str], float]:
        print(f'Obtaining top {amount} most relevant {self.token_type.value}s for {document_type.value.upper()}:')
        match document_type:
            case DocumentType.HYPERPARTISAN:
                return self.__get_n_highest_values_from_dictionary__(dictionary=self.log_odd_ratios, n=amount)
            case DocumentType.NON_HYPERPARTISAN:
                return self.__get_n_lowest_values_from_dictionary__(dictionary=self.log_odd_ratios, n=amount)

    @staticmethod
    def __get_n_highest_values_from_dictionary__(dictionary: dict, n: int) -> dict:
        highest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        return dict(list(highest_values.items())[:n])

    @staticmethod
    def __get_n_lowest_values_from_dictionary__(dictionary: dict, n: int) -> dict:
        lowest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=False))
        return dict(list(lowest_values.items())[:n])
