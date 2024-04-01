from pathlib import Path

from src.get_hyperpartisan_data.HyperpartisanDocumentsLoader import HyperpartisanDocumentsLoader
from src.get_hyperpartisan_data.HyperpartisanDocumentsProcessor import HyperpartisanDocumentsProcessor

if __name__ == '__main__':
    # hyperpartisan_documents_loader = HyperpartisanDocumentsLoader()
    # hyperpartisan_documents_loader.load_dataset()

    hyperpartisan_documents_processor = HyperpartisanDocumentsProcessor(
        hyperpartisan_documents_path=Path('../data/txt/hyperpartisan_short.txt'),
        non_hyperpartisan_documents_path=Path('../data/txt/non-hyperpartisan_short.txt')
    )
    hyperpartisan_document_list, non_hyperpartisan_document_list = (hyperpartisan_documents_processor.
                                                                    get_clean_documents())

    print(f'Number of documents (Hyperpartisan): {len(hyperpartisan_document_list)}')
    print(f'Number of documents (Non-Hyperpartisan): {len(non_hyperpartisan_document_list)}')
    print(len(hyperpartisan_document_list) + len(non_hyperpartisan_document_list))

    print(hyperpartisan_document_list[0])
    print(non_hyperpartisan_document_list[0])

    # Remove infrequent words (appear <20 times) before extracting log-odd ratios
    hyperpartisan_document_list, non_hyperpartisan_document_list = (hyperpartisan_documents_processor.
        remove_infrequent_words(
            documents=(hyperpartisan_document_list, non_hyperpartisan_document_list),
            threshold=3
        )
    )
    print(hyperpartisan_document_list[0])
    print(non_hyperpartisan_document_list[0])
