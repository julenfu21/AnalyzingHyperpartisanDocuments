import math
import os
import pickle
from collections import defaultdict
from itertools import pairwise
from pathlib import Path

from tqdm import tqdm

from src.log_odd_ratios.LogOddRatios import LogOddRatios
from src.log_odd_ratios.DocumentGroup import DocumentGroup
from src.constant_values.enums import DocumentType, TokenType


class LogOddRatiosCalculator:

    def __init__(
            self,
            hyperpartisan_documents: list[list[str]],
            non_hyperpartisan_documents: list[list[str]],
            token_type: TokenType,
            pickle_data_folder_path=Path('../data/pickle')
    ) -> None:
        self.hyperpartisan_document_group = DocumentGroup(
            document_list=hyperpartisan_documents,
            document_type=DocumentType.HYPERPARTISAN
        )
        self.non_hyperpartisan_document_group = DocumentGroup(
            document_list=non_hyperpartisan_documents,
            document_type=DocumentType.NON_HYPERPARTISAN
        )
        self.token_type = token_type
        self.pickle_data_folder_path = os.path.join(pickle_data_folder_path, 'log_odd_ratios')
        if not os.path.exists(self.pickle_data_folder_path):
            os.makedirs(self.pickle_data_folder_path)

        self.all_tokens = set()
        self.log_odd_ratios = LogOddRatios(values={}, type=token_type)

        self.hyperpartisan_tokens_frequency = defaultdict(int)
        self.non_hyperpartisan_tokens_frequency = defaultdict(int)
        self.__set_tokens_frequency__()

    def __set_tokens_frequency__(self) -> None:
        self.hyperpartisan_tokens_frequency = self.__calculate_tokens_frequency__(
            document_group=self.hyperpartisan_document_group
        )

        self.non_hyperpartisan_tokens_frequency = self.__calculate_tokens_frequency__(
            document_group=self.non_hyperpartisan_document_group
        )

        print()

    def __calculate_tokens_frequency__(self, document_group: DocumentGroup) -> defaultdict[str | tuple[str, str], int]:
        tokens_frequency = defaultdict(int)
        progress_bar_description = (f"Calculating {self.token_type.value}s frequency for "
                                    f"{document_group.document_type.value.upper()} ...")

        match self.token_type:
            case TokenType.UNIGRAM:
                for document in tqdm(document_group.document_list, desc=progress_bar_description):
                    for unigram in document:
                        tokens_frequency[unigram] += 1
                        self.all_tokens.add(unigram)
            case TokenType.BIGRAM:
                for document in tqdm(document_group.document_list, desc=progress_bar_description):
                    for token_1, token_2 in pairwise(document):
                        bigram = (token_1, token_2)
                        tokens_frequency[bigram] += 1
                        self.all_tokens.add(bigram)

        return tokens_frequency

    def calculate_log_odd_ratios(self) -> None:
        hyperpartisan_o_values, non_hyperpartisan_o_values = self.__calculate_o_values__()
        print("Calculating log-odd ratios ...")
        self.log_odd_ratios.values = {token: self.__calculate_r_value_on_token__(
            token=token,
            hyperpartisan_o_values=hyperpartisan_o_values,
            non_hyperpartisan_o_values=non_hyperpartisan_o_values
        ) for token in self.all_tokens}
        print("Log-odd ratios calculated successfully.")
        print("Saving log-odd ratios into a pickle file ...")
        self.__save_log_odd_ratios_to_pickle_file__()
        print("Pickle file saved. \n\n")

    def __save_log_odd_ratios_to_pickle_file__(self) -> None:
        pickle_file_name = f'log-odd-ratios-{self.token_type.value}.pkl'
        pickle_file_path = os.path.join(self.pickle_data_folder_path, pickle_file_name)

        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(self.log_odd_ratios, pickle_file)

    def __calculate_r_value_on_token__(
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

    def __calculate_o_values__(self) -> tuple[defaultdict[str, float], defaultdict[str, float]]:
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

        print()
        return defaultdict(float, hyperpartisan_o_values), defaultdict(float, non_hyperpartisan_o_values)

    def __calculate_o_values_on_document_group__(
            self,
            tokens_frequency: defaultdict[str | tuple[str, str], int],
            document_group: DocumentGroup
    ) -> dict[str, float]:
        print(f"Calculating o values for {document_group.document_type.value.upper()} ...")
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
        print(f'Highest values: {dict(list(sorted_values.items())[:20])} ... \n')
