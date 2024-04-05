import os
import pickle
from pathlib import Path

import plotly.express as px
import pandas as pd

from src.constant_values import constants
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

        self.log_odd_ratios = self.__get_log_odd_ratios_from_pickle_file__()

    def __get_log_odd_ratios_from_pickle_file__(self) -> LogOddRatios:
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

    def plot_infinite_values_proportion(self) -> None:
        values = list(self.log_odd_ratios.values.values())

        log_odd_ratios_distribution_dataframe = pd.DataFrame(
            {
                'log-odd ratios': values,
                'infinite_values': [True if value in constants.INFINITE_VALUES else False for value in values]
            }
        )
        log_odd_ratios_distribution_pie_chart = px.pie(
            data_frame=log_odd_ratios_distribution_dataframe,
            names='infinite_values',
            title='Distribution of infinite and non-infinite values',

        )
        log_odd_ratios_distribution_pie_chart.show()

    def calculate_infinite_values_count(self) -> None:
        log_odd_ratios_values = self.log_odd_ratios.values.values()
        infinite_values_count = 0

        for log_odd_ratio in log_odd_ratios_values:
            if log_odd_ratio in constants.INFINITE_VALUES:
                infinite_values_count += 1

        print(f'Proportion of infinite values for {self.token_type.value}s: {infinite_values_count} / '
              f'{len(log_odd_ratios_values)}')



if __name__ == '__main__':
    log_odd_ratios_analyzer = LogOddRatiosAnalyzer(
        token_type=TokenType.UNIGRAM,
        pickle_data_folder_path=Path('../../data/pickle')
    )
    log_odd_ratios_analyzer.plot_infinite_values_proportion()
