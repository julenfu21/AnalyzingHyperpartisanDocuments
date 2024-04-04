from src.calculate_log_odd_ratios.LogOddRatiosCalculator import LogOddRatiosCalculatorV2, TokenType
from src.constant_values.enums import DocumentType
from src.get_hyperpartisan_data.HyperpartisanDocumentsFormatter import HyperpartisanDocumentsFormatter
from src.get_hyperpartisan_data.HyperpartisanDocumentsProcessor import HyperpartisanDocumentsProcessorV2
from src.utils import console_output_formatter


if __name__ == '__main__':
    # Adapt hyperpartisan documents format into txt files
    console_output_formatter.print_section_header(section_header='Data formatting')
    hyperpartisan_documents_formatter = HyperpartisanDocumentsFormatter()
    hyperpartisan_documents_formatter.adapt_dataset_format()

    # Process hyperpartisan documents (if necessary) and load
    console_output_formatter.print_section_header(section_header='Data loading / preprocessing')
    hyperpartisan_documents_processor = HyperpartisanDocumentsProcessorV2()

    hyperpartisan_document_list = hyperpartisan_documents_processor.get_clean_documents(
        document_type=DocumentType.HYPERPARTISAN
    )
    console_output_formatter.print_document_list_stats(
        document_list=hyperpartisan_document_list,
        document_type=DocumentType.HYPERPARTISAN
    )

    non_hyperpartisan_document_list = hyperpartisan_documents_processor.get_clean_documents(
        document_type=DocumentType.NON_HYPERPARTISAN
    )
    console_output_formatter.print_document_list_stats(
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
    console_output_formatter.print_section_header(section_header='Log-odd ratios calculation')
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
