from src.constant_values.enums import DocumentType


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
