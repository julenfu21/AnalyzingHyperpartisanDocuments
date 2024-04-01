import os
from enum import Enum
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from tqdm import tqdm

from src.constants import txt_constants


class DataFileTypesNames(Enum):
    ARTICLES = "articles-validation-bypublisher-20181122"
    GROUND_TRUTH = "ground-truth-validation-bypublisher-20181122"


class HyperpartisanDocumentsLoader:

    def __init__(
            self,
            zip_data_folder_path: str | Path = Path('../data/zip'),
            xml_data_folder_path: str | Path = Path('../data/xml'),
            txt_data_folder_path: str | Path = Path('../data/txt')
    ):
        self.zip_data_folder_path = zip_data_folder_path
        self.xml_data_folder_path = xml_data_folder_path
        self.txt_data_folder_path = txt_data_folder_path

    def load_dataset(self):
        self.__extract_xml_files_from_zip_files__()
        self.__extract_data_from_xml_to_txt__()

    def __extract_xml_files_from_zip_files__(self) -> None:
        data_files_names = [
            DataFileTypesNames.ARTICLES,
            DataFileTypesNames.GROUND_TRUTH
        ]

        for data_file_name in data_files_names:
            # Define path of the current xml file
            xml_file_name = f"{data_file_name.value}.xml"
            xml_file_path = os.path.join(self.xml_data_folder_path, xml_file_name)

            # Extract zip file if necessary
            zip_file_name = f"{data_file_name.value}.zip"
            if os.path.isfile(xml_file_path):
                print(f'The file {zip_file_name} is already extracted')
            else:
                print(f'Extracting file {zip_file_name} ...')
                zip_file_path = os.path.join(self.zip_data_folder_path, zip_file_name)
                with ZipFile(zip_file_path, 'r') as zip_file:
                    zip_file.extractall(path=self.xml_data_folder_path)
                print(f'File {zip_file_name} extracted')

    def __extract_data_from_xml_to_txt__(self) -> None:
        articles_file_name = f'{DataFileTypesNames.ARTICLES.value}.xml'
        articles_file_path = os.path.join(self.xml_data_folder_path, articles_file_name)
        ground_truth_file_name = f'{DataFileTypesNames.GROUND_TRUTH.value}.xml'
        ground_truth_file_path = os.path.join(self.xml_data_folder_path, ground_truth_file_name)

        ground_truths_dict = self.__get_ground_truths_dict_from_xml_data__(xml_file_path=ground_truth_file_path)
        self.__extract_articles_text_from_xml_data__(
            ground_truths_dict=ground_truths_dict,
            xml_file_path=articles_file_path
        )

    @staticmethod
    def __get_ground_truths_dict_from_xml_data__(xml_file_path: str | Path) -> dict[str, bool]:
        # Obtain root node
        xml_parser = etree.XMLParser(remove_blank_text=True)
        xml_tree = etree.parse(xml_file_path, parser=xml_parser)
        articles = xml_tree.getroot()

        # Obtain and store the ground-truth value for each article
        ground_truth_dict = {}
        for article in tqdm(articles, desc="Getting ground truth values..."):
            article_id = article.get('id')
            hyperpartisan_str = article.get('hyperpartisan').capitalize()
            hyperpartisan_bool = eval(hyperpartisan_str)
            ground_truth_dict[article_id] = hyperpartisan_bool

        return ground_truth_dict

    def __extract_articles_text_from_xml_data__(
            self,
            ground_truths_dict: dict[str, bool],
            xml_file_path: str | Path,
    ) -> None:
        # Obtain root node
        xml_parser = etree.XMLParser(remove_blank_text=True)
        xml_tree = etree.parse(source=xml_file_path, parser=xml_parser)
        articles = xml_tree.getroot()

        # Define paths for the output txt files
        hyperpartisan_txt_file_path = os.path.join(self.txt_data_folder_path, 'hyperpartisan.txt')
        non_hyperpartisan_txt_file_path = os.path.join(self.txt_data_folder_path, 'non-hyperpartisan.txt')

        # Delete previous version files to avoid stacking content
        if os.path.exists(self.txt_data_folder_path):
            self.__delete_previous_txt_files__()
        else:
            os.makedirs(self.txt_data_folder_path)

        # Add articles into txt files
        for article in tqdm(articles, desc="Extracting text from articles..."):
            article_id = article.get('id')
            hyperpartisan: bool = ground_truths_dict[article_id]

            if hyperpartisan:
                self.__add_article_to_txt_file__(txt_file_path=hyperpartisan_txt_file_path, article=article)
            else:
                self.__add_article_to_txt_file__(txt_file_path=non_hyperpartisan_txt_file_path, article=article)

    def __delete_previous_txt_files__(self) -> None:
        files_list = os.listdir(self.txt_data_folder_path)
        for file in files_list:
            os.remove(os.path.join(self.txt_data_folder_path, file))

    @staticmethod
    def __add_article_to_txt_file__(txt_file_path, article) -> None:
        with open(txt_file_path, encoding='utf-8', mode='a') as txt_file:
            # Add article metadata
            txt_file.write(f"ID: {article.get('id')} ----> Title: {article.get('title')}\n\n")

            # Add article text
            for paragraph in article:
                text = paragraph.xpath('string()')
                if text:
                    txt_file.write(f"{text}\n\n")

            txt_file.write(f"{txt_constants.ARTICLE_END}\n")
