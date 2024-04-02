from dataclasses import dataclass, field
from functools import cached_property


@dataclass
class DocumentGroup:
    document_list: list[list[str]] = field(default_factory=list)

    @cached_property
    def word_count(self) -> int:
        number_of_words = 0

        for document in self.document_list:
            number_of_words += len(document)

        return number_of_words
