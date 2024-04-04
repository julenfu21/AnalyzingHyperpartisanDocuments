from src.calculate_log_odd_ratios.LogOddRatiosCalculator import LogOddRatiosCalculatorV2, TokenType
from src.constant_values.enums import DocumentType
from src.get_hyperpartisan_data.HyperpartisanDocumentsProcessor import HyperpartisanDocumentsProcessorV2


# EXTRACT THIS KIND OF FUNCTION TO ANOTHER CLASS/FILE
def print_document_list_stats(document_list: list[list[str]], document_type: DocumentType) -> None:
    print(f"DOCUMENT LIST STATISTICS ({document_type.value.upper()}):")
    print(f'Number of documents: {len(document_list)}')
    print(f'Document sample after performing preprocessing:')
    print(f'{document_list[0]} \n\n')


def print_section_header(section_header: str = " ", padding: int = 5, delimiter: str = '#') -> None:
    square_length = len(section_header) + padding * 2 + 2
    square_upper_lower_row = delimiter * square_length
    square_middle_row = delimiter + ' ' * (square_length - 2) + delimiter
    text_row = delimiter + ' ' * padding + section_header.upper() + ' ' * padding + delimiter

    print(square_upper_lower_row)
    print(square_middle_row)
    print(text_row)
    print(square_middle_row)
    print(square_upper_lower_row)
    print()


if __name__ == '__main__':
    # Load hyperpartisan documents into txt files (partimos de que están cargados)
    print_section_header(section_header='Data formatting')

    # Process hyperpartisan documents
    print_section_header(section_header='Data loading / preprocessing')
    hyperpartisan_documents_processor = HyperpartisanDocumentsProcessorV2()

    hyperpartisan_document_list = hyperpartisan_documents_processor.get_clean_documents(
        document_type=DocumentType.HYPERPARTISAN
    )
    print_document_list_stats(
        document_list=hyperpartisan_document_list,
        document_type=DocumentType.HYPERPARTISAN
    )

    non_hyperpartisan_document_list = hyperpartisan_documents_processor.get_clean_documents(
        document_type=DocumentType.NON_HYPERPARTISAN
    )
    print_document_list_stats(
        document_list=non_hyperpartisan_document_list,
        document_type=DocumentType.NON_HYPERPARTISAN
    )

    hyperpartisan_document_list, non_hyperpartisan_document_list = (hyperpartisan_documents_processor.
        remove_infrequent_words(
            hyperpartisan_documents=hyperpartisan_document_list,
            non_hyperpartisan_documents=non_hyperpartisan_document_list
        )
    )

    # Calculate log-odd ratios
    print_section_header(section_header='Log-odd ratios calculation')
    log_odd_ratios_calculator = LogOddRatiosCalculatorV2(
        hyperpartisan_documents=hyperpartisan_document_list,
        non_hyperpartisan_documents=non_hyperpartisan_document_list,
        token_type=TokenType.BIGRAM
    )

    log_odd_ratios_calculator.calculate_log_odd_ratios()
    hyperpartisan_most_relevant_words = (log_odd_ratios_calculator.
                                         get_most_relevant_words(document_type=DocumentType.HYPERPARTISAN))
    print(hyperpartisan_most_relevant_words)
    hyperpartisan_most_relevant_words_not_inf = (log_odd_ratios_calculator.
        get_most_relevant_words(
            document_type=DocumentType.HYPERPARTISAN,
            infinite_values=False
        )
    )
    print(hyperpartisan_most_relevant_words_not_inf)
    print()

    non_hyperpartisan_most_relevant_words = (log_odd_ratios_calculator.
                                             get_most_relevant_words(document_type=DocumentType.NON_HYPERPARTISAN))
    print(non_hyperpartisan_most_relevant_words)
    non_hyperpartisan_most_relevant_words_not_inf = (log_odd_ratios_calculator.
        get_most_relevant_words(
            document_type=DocumentType.NON_HYPERPARTISAN,
            infinite_values=False
        )
    )
    print(non_hyperpartisan_most_relevant_words_not_inf)
