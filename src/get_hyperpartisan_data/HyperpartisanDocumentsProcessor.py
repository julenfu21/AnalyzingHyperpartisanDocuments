from collections import defaultdict
from pathlib import Path

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

from src.constants import txt_constants


class HyperpartisanDocumentsProcessor:

    def __init__(
            self,
            hyperpartisan_documents_path=Path("../data/txt/hyperpartisan.txt"),
            non_hyperpartisan_documents_path=Path("../data/txt/non-hyperpartisan.txt")
    ):
        self.hyperpartisan_documents_path = hyperpartisan_documents_path
        self.non_hyperpartisan_documents_path = non_hyperpartisan_documents_path
        self.token_frequencies = defaultdict(int)

    def get_clean_documents(self) -> tuple[list[list[str]], list[list[str]]]:
        hyperpartisan_documents_list = self.__get_clean_document_list_from_txt_file__(
            txt_file_path=self.hyperpartisan_documents_path
        )
        non_hyperpartisan_documents_list = self.__get_clean_document_list_from_txt_file__(
            txt_file_path=self.non_hyperpartisan_documents_path
        )

        return hyperpartisan_documents_list, non_hyperpartisan_documents_list

    def __get_clean_document_list_from_txt_file__(self, txt_file_path: str | Path) -> list[list[str]]:
        documents = []
        current_document_line_index = 0
        current_document_content = []

        with open(txt_file_path, encoding='utf-8', mode='r') as txt_file:
            # for line in tqdm(txt_file, desc="Getting clean documents..."):
            for line in txt_file:
                # Remove '\n' tokens
                line = line.strip()

                # First two lines are the title with its id and a '\n' line
                if current_document_line_index < 2:
                    current_document_line_index += 1
                else:
                    # The article is over
                    if line == txt_constants.ARTICLE_END:
                        current_document = " ".join(current_document_content)
                        current_clean_document = self.__clean_document__(document=current_document)
                        documents.append(current_clean_document)

                        # Reset line values
                        current_document_line_index = 0
                        current_document_content = []
                    else:
                        # The line is not empty
                        if line:
                            current_document_content.append(line)

                        current_document_line_index += 1

        return documents

    def __clean_document__(self, document: str) -> list[str]:
        clean_document = self.__tokenize_document__(document=document)
        clean_document = self.__remove_stopwords_from_document__(document=clean_document)
        clean_document = self.__lower_case_document__(document=clean_document)
        return clean_document

    @staticmethod
    def __tokenize_document__(document: str) -> list[str]:
        return word_tokenize(document)

    @staticmethod
    def __remove_stopwords_from_document__(document: list[str]) -> list[str]:
        stop_words = stopwords.words('english')
        return [word for word in document if not word.lower() in stop_words]

    @staticmethod
    def __lower_case_document__(document: list[str]) -> list[str]:
        return [word.lower() for word in document]

    def remove_infrequent_words(
            self,
            documents: tuple[list[list[str]], list[list[str]]],
            threshold: int = 20
    ) -> tuple[list[list[str]], list[list[str]]]:
        self.__get_full_corpus_tokens_frequency__(
            hyperpartisan_documents=documents[0],
            non_hyperpartisan_documents=documents[1]
        )

        # Remove infrequent words from each sentence
        hyperpartisan_processed_sentence_list = self.__remove_infrequent_words_on_document_list__(
            document_list=documents[0], threshold=threshold
        )
        non_hyperpartisan_processed_sentence_list = self.__remove_infrequent_words_on_document_list__(
            document_list=documents[1], threshold=threshold
        )

        return hyperpartisan_processed_sentence_list, non_hyperpartisan_processed_sentence_list

    def __get_full_corpus_tokens_frequency__(
            self,
            hyperpartisan_documents: list[list[str]],
            non_hyperpartisan_documents: list[list[str]]
    ) -> None:
        self.__get_tokens_frequency_on_document_list__(document_list=hyperpartisan_documents)
        self.__get_tokens_frequency_on_document_list__(document_list=non_hyperpartisan_documents)
        print(self.token_frequencies)

    def __get_tokens_frequency_on_document_list__(self, document_list: list[list[str]]) -> None:
        for document in document_list:
            for token in document:
                self.token_frequencies[token] += 1

    def __remove_infrequent_words_on_document_list__(
            self,
            document_list: list[list[str]],
            threshold: int = 20
    ) -> list[list[str]]:
        processed_sentence_list = []
        for document in document_list:
            processed_document = [token for token in document if self.token_frequencies[token] >= threshold]
            processed_sentence_list.append(processed_document)

        return processed_sentence_list
