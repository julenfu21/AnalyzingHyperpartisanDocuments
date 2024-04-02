from src.constant_values.enums import DocumentType
from src.get_hyperpartisan_data.HyperpartisanDocumentsProcessor import HyperpartisanDocumentsProcessor


if __name__ == '__main__':
    # Load hyperpartisan documents into txt files
    # hyperpartisan_documents_loader = HyperpartisanDocumentsLoader()
    # hyperpartisan_documents_loader.load_dataset()

    # Process hyperpartisan documents
    hyperpartisan_documents_processor = HyperpartisanDocumentsProcessor(
        # hyperpartisan_documents_path=Path('../data/txt/hyperpartisan_short.txt'),
        # non_hyperpartisan_documents_path=Path('../data/txt/non-hyperpartisan_short.txt')
    )
    hyperpartisan_document_list, non_hyperpartisan_document_list = (hyperpartisan_documents_processor.
                                                                    get_clean_documents())

    print(f'\n\tNumber of documents ({DocumentType.HYPERPARTISAN.value}): {len(hyperpartisan_document_list)}')
    print(f'\tNumber of documents ({DocumentType.NON_HYPERPARTISAN.value}): {len(non_hyperpartisan_document_list)}')
    print(f'\tTotal number of documents: {len(hyperpartisan_document_list) + len(non_hyperpartisan_document_list)}\n')

    print(f'Document sample after performing preprocessing ({DocumentType.HYPERPARTISAN.value}):')
    print(f'{hyperpartisan_document_list[0]}\n')

    print(f'\nDocument sample after performing preprocessing ({DocumentType.NON_HYPERPARTISAN.value}):')
    print(f'{non_hyperpartisan_document_list[0]}\n')

    # Remove infrequent words (they appear <20 times) before extracting log-odd ratios
    hyperpartisan_document_list, non_hyperpartisan_document_list = (hyperpartisan_documents_processor.
        remove_infrequent_words(
            documents=(hyperpartisan_document_list, non_hyperpartisan_document_list)
        )
    )

    print(f'Document sample after removing infrequent words ({DocumentType.HYPERPARTISAN.value}):')
    print(f'{hyperpartisan_document_list[0]}\n')

    print(f'Document sample after removing infrequent words ({DocumentType.NON_HYPERPARTISAN.value}):')
    print(f'{non_hyperpartisan_document_list[0]}\n')
