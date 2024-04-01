import os
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from tqdm import tqdm


def extract_xml_files_from_zip_files(
        zip_data_folder_path: str | Path = Path('../data/zip'),
        xml_data_folder_path: str | Path = Path('../data/xml')
) -> None:
    data_files_names = [
        'articles-validation-bypublisher-20181122',
        'ground-truth-validation-bypublisher-20181122'
    ]
    for data_file_name in data_files_names:
        # Define path of the current xml file
        xml_file_name = f"{data_file_name}.xml"
        xml_file_path = os.path.join(xml_data_folder_path, xml_file_name)

        # Extract zip file if necessary
        if os.path.isfile(xml_file_path):
            print(f'The file {xml_file_path} is already extracted')
        else:
            print(f'Extracting file {data_file_name} ...')
            zip_file_name = f"{data_file_name}.zip"
            zip_file_path = os.path.join(zip_data_folder_path, zip_file_name)
            with ZipFile(zip_file_path, 'r') as zip_file:
                zip_file.extractall(path=xml_data_folder_path)
            print(f'File {data_file_name} extracted')


def extract_data_from_xml_to_txt(
        articles_file_path: str | Path = Path('../data/xml/articles-validation-bypublisher-20181122.xml'),
        ground_truth_file_path: str | Path = Path('../data/xml/ground-truth-validation-bypublisher-20181122.xml'),
        txt_data_folder_path: str | Path = Path('../data/txt')
) -> None:
    ground_truths_dict = get_ground_truths_dict_from_xml_data(xml_file_path=ground_truth_file_path)
    extract_articles_text_from_xml_data(
        ground_truths_dict=ground_truths_dict,
        xml_file_path=articles_file_path,
        txt_data_folder_path=txt_data_folder_path
    )


# PRIVATE METHOD
def get_ground_truths_dict_from_xml_data(xml_file_path: str | Path) -> dict[str, bool]:
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


# PRIVATE METHOD
def extract_articles_text_from_xml_data(
        ground_truths_dict: dict[str, bool],
        xml_file_path: str | Path,
        txt_data_folder_path: str | Path
) -> None:
    # Obtain root node
    xml_parser = etree.XMLParser(remove_blank_text=True)
    xml_tree = etree.parse(source=xml_file_path, parser=xml_parser)
    articles = xml_tree.getroot()

    # Define paths for the output txt files
    hyperpartisan_txt_file_path = os.path.join(txt_data_folder_path, 'hyperpartisan.txt')
    non_hyperpartisan_txt_file_path = os.path.join(txt_data_folder_path, 'non-hyperpartisan.txt')

    # Delete previous version files to avoid stacking content
    if os.path.exists(txt_data_folder_path):
        delete_previous_txt_files(txt_data_folder_path)
    else:
        os.makedirs(txt_data_folder_path)

    # Add articles into txt files
    for article in tqdm(articles, desc="Extracting text from articles..."):
        article_id = article.get('id')
        hyperpartisan: bool = ground_truths_dict[article_id]

        if hyperpartisan:
            add_article_to_txt_file(txt_file_path=hyperpartisan_txt_file_path, article=article)
        else:
            add_article_to_txt_file(txt_file_path=non_hyperpartisan_txt_file_path, article=article)


def delete_previous_txt_files(txt_data_folder_path):
    files_list = os.listdir(txt_data_folder_path)
    for file in files_list:
        os.remove(os.path.join(txt_data_folder_path, file))


def add_article_to_txt_file(txt_file_path: str, article: etree.Element) -> None:
    with open(txt_file_path, encoding='utf-8', mode='a') as txt_file:
        # Add article metadata
        txt_file.write(f"ID: {article.get('id')} ----> Title: {article.get('title')} \n \n")

        # Add article text
        for paragraph in article:
            text = paragraph.xpath('string()')
            if text:
                txt_file.write(f"{text} \n \n")

        txt_file.write('\n')


if __name__ == '__main__':
    extract_xml_files_from_zip_files()
    extract_data_from_xml_to_txt()
