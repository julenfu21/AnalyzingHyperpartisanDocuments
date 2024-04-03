import os.path
import pickle
from collections import defaultdict
from pathlib import Path

import nltk
from tqdm import tqdm

from src.constant_values import constants
from src.constant_values.enums import DocumentType


class HyperpartisanDocumentsProcessorV2:

    def __init__(
            self,
            txt_data_folder_path=Path('../data/txt/'),
            pickle_data_folder_path=Path('../data/pickle')
    ) -> None:
        self.txt_data_folder_path = txt_data_folder_path
        self.pickle_data_folder_path = pickle_data_folder_path
        self.unigrams_frequency = defaultdict(int)

        if not os.path.exists(pickle_data_folder_path):
            os.makedirs(pickle_data_folder_path)

    def get_clean_documents(self, document_type: DocumentType) -> list[list[str]]:
        if os.path.exists(f'../data/pickle/{document_type.value}.pkl'):
            print(f'The {document_type.value.upper()} document list already exists. Loading it from pickle file ...')
            clean_document_list = self.__get_clean_documents_from_pickle_file__(
                document_type=document_type
            )
            print(f"Clean document list ({document_type.value.upper()}) loaded successfully. \n")

        else:
            clean_document_list = self.__get_clean_documents_from_txt_file__(
                document_type=document_type
            )
            print(f"Clean document list ({document_type.value.upper()}) loaded successfully.")
            print(f"Saving {document_type.value.upper()} document list into pickle file ...")
            self.__save_document_list_to_pickle_file__(
                document_type=document_type,
                document_list=clean_document_list
            )
            print("Pickle file saved. \n")

        return clean_document_list

    def __get_clean_documents_from_pickle_file__(self, document_type: DocumentType) -> list[list[str]]:
        pickle_file_name = f'{document_type.value}.pkl'
        pickle_file_path = os.path.join(self.pickle_data_folder_path, pickle_file_name)

        with open(pickle_file_path, 'rb') as pickle_file:
            documents = pickle.load(pickle_file)

        return documents

    def __save_document_list_to_pickle_file__(
            self,
            document_type: DocumentType,
            document_list: list[list[str]]
    ) -> None:
        pickle_file_name = f'{document_type.value.lower()}.pkl'
        pickle_file_path = os.path.join(self.pickle_data_folder_path, pickle_file_name)

        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(document_list, pickle_file)

    def __get_clean_documents_from_txt_file__(self, document_type: DocumentType) -> list[list[str]]:
        documents = []
        current_document_line_index = 0
        current_document_content = []

        txt_file_name = f'{document_type.value}.txt'
        txt_file_path = os.path.join(self.txt_data_folder_path, txt_file_name)

        with open(txt_file_path, encoding='utf-8', mode='r') as txt_file:
            progress_bar = tqdm(desc=f'Getting clean documents from txt files ...', total=75000)
            for line in txt_file:
                # Remove '\n' tokens
                line = line.strip()

                # First two lines are the title with its id and a '\n' line
                if current_document_line_index < 2:
                    current_document_line_index += 1
                else:
                    # The article is over
                    if line == constants.ARTICLE_END:
                        current_document = " ".join(current_document_content)
                        current_clean_document = self.__clean_document__(document=current_document)
                        documents.append(current_clean_document)
                        progress_bar.update(1)

                        # Reset current document values
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
        return nltk.tokenize.word_tokenize(document)

    @staticmethod
    def __remove_stopwords_from_document__(document: list[str]) -> list[str]:
        stop_words = nltk.corpus.stopwords.words('english')
        return [word for word in document if not word.lower() in stop_words]

    @staticmethod
    def __lower_case_document__(document: list[str]) -> list[str]:
        return [word.lower() for word in document]

    def remove_infrequent_words(
            self,
            hyperpartisan_documents: list[list[str]],
            non_hyperpartisan_documents: list[list[str]],
            threshold_value: int = 20
    ) -> tuple[list[list[str]], list[list[str]]]:
        print('Calculating unigrams frequency for the whole corpus ...')
        self.__set_unigrams_frequency__(
            hyperpartisan_documents=hyperpartisan_documents,
            non_hyperpartisan_documents=non_hyperpartisan_documents
        )
        print('Unigrams frequency calculated successfully.')

        print('Removing infrequent words from the corpus ...')
        hyperpartisan_processed_sentence_list = self.__remove_infrequent_words_on_document_list__(
            document_list=hyperpartisan_documents, threshold_value=threshold_value
        )
        non_hyperpartisan_processed_sentence_list = self.__remove_infrequent_words_on_document_list__(
            document_list=non_hyperpartisan_documents, threshold_value=threshold_value
        )
        print('Infrequent words removed successfully.')

        return hyperpartisan_processed_sentence_list, non_hyperpartisan_processed_sentence_list

    def __set_unigrams_frequency__(
            self,
            hyperpartisan_documents: list[list[str]],
            non_hyperpartisan_documents: list[list[str]]
    ) -> None:
        self.__get_unigrams_frequency_on_document_list__(document_list=hyperpartisan_documents)
        self.__get_unigrams_frequency_on_document_list__(document_list=non_hyperpartisan_documents)

    def __get_unigrams_frequency_on_document_list__(self, document_list: list[list[str]]) -> None:
        for document in document_list:
            for token in document:
                self.unigrams_frequency[token] += 1

    def __print_unigrams_frequency_by_descending_order__(self) -> None:
        sorted_token_frequencies = dict(sorted(
            self.unigrams_frequency.items(),
            key=lambda item: item[1],
            reverse=True)
        )
        print(f'Most frequent tokens: {dict(list(sorted_token_frequencies.items())[:20])} ...')

    def __remove_infrequent_words_on_document_list__(
            self,
            document_list: list[list[str]],
            threshold_value: int
    ) -> list[list[str]]:
        processed_sentence_list = []
        for document in document_list:
            processed_document = [token for token in document if self.unigrams_frequency[token] >= threshold_value]
            processed_sentence_list.append(processed_document)

        return processed_sentence_list
