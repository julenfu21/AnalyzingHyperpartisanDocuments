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

        self.log_odd_ratios = {}

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

    def __get_tokens_frequency_on_document_list__(
            self,
            document_group: DocumentGroup,
            document_type: DocumentType,
            tokens_frequencies: defaultdict[str, int]
    ) -> None:
        for document in document_group.document_list:
            for token in document:
                tokens_frequencies[token] += 1

        most_frequent_tokens = self.__get_n_most_frequent_tokens__(
            tokens_frequencies=tokens_frequencies
        )
        print(f'Most frequent tokens ({document_type.value}): {most_frequent_tokens}')

    @staticmethod
    def __get_n_most_frequent_tokens__(tokens_frequencies: defaultdict[str, int], n: int = 10) -> dict[str, int]:
        sorted_tokens_frequencies = dict(sorted(tokens_frequencies.items(), key=lambda item: item[1], reverse=True))
        return dict(list(sorted_tokens_frequencies.items())[:n])

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

        highest_values = dict(sorted(p_on_document_list.items(), key=lambda item: item[1], reverse=True))
        print(f'Highest p values: {dict(list(highest_values.items())[:10])}')

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

    def __get_o__(self, document_list: list[list[str]]) -> dict[str, int]:
        pass