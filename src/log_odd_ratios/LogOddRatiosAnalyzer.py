import os
import pickle
from pathlib import Path

from src.constant_values.enums import DocumentType, TokenType
from src.log_odd_ratios.LogOddRatios import LogOddRatios


class LogOddRatiosAnalyzer:

    def __init__(
            self,
            token_type: TokenType,
            pickle_data_folder_path=Path('../data/pickle')
    ) -> None:
        self.token_type = token_type
        self.pickle_data_folder_path = os.path.join(pickle_data_folder_path, 'log_odd_ratios')

        self.log_odd_ratios = self.__get_log_odd_ratios_from_pickle_file()

    def __get_log_odd_ratios_from_pickle_file(self) -> LogOddRatios:
        pickle_file_name = f'log-odd-ratios-{self.token_type.value}.pkl'
        pickle_file_path = os.path.join(self.pickle_data_folder_path, pickle_file_name)

        print(f'Loading log-odd ratios for {self.token_type.value}s from pickle file ...')
        with open(pickle_file_path, 'rb') as pickle_file:
            log_odd_ratios = pickle.load(pickle_file)
        print('Log-odd ratios loaded successfully. \n')

        return log_odd_ratios

    def get_most_relevant_words(
            self,
            document_type: DocumentType,
            amount: int = 50,
            infinite_values: bool = True
    ) -> dict[str | tuple[str, str], float]:
        token_type = self.log_odd_ratios.type
        if infinite_values:
            print(f'Obtaining top {amount} most relevant {token_type.value}s for {document_type.value.upper()}:')
        else:
            print(f'Obtaining top {amount} most relevant {token_type.value}s for {document_type.value.upper()} '
                  f'(without infinite values):')

        match document_type:
            case DocumentType.HYPERPARTISAN:
                return self.__get_n_highest_values_from_dictionary__(
                    dictionary=self.log_odd_ratios.values,
                    n=amount,
                    infinite_values=infinite_values
                )
            case DocumentType.NON_HYPERPARTISAN:
                return self.__get_n_lowest_values_from_dictionary__(
                    dictionary=self.log_odd_ratios.values,
                    n=amount,
                    infinite_values=infinite_values
                )

    @staticmethod
    def __get_n_highest_values_from_dictionary__(dictionary: dict, n: int, infinite_values: bool) -> dict:
        highest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        if not infinite_values:
            highest_values = {key: value for key, value in highest_values.items() if value != float('inf')}
        return dict(list(highest_values.items())[:n])

    @staticmethod
    def __get_n_lowest_values_from_dictionary__(dictionary: dict, n: int, infinite_values: bool) -> dict:
        lowest_values = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=False))
        if not infinite_values:
            lowest_values = {key: value for key, value in lowest_values.items() if value != float('-inf')}
        return dict(list(lowest_values.items())[:n])

    # ADD FUNCTIONS TO OBTAIN GRAPHS (BAR-PLOT, ...)
